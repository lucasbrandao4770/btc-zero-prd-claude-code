# Design Pattern

> Creating architecture from specifications (HOW)

---

## Purpose

The Design phase transforms requirements (WHAT) into technical architecture (HOW). It produces:

1. **Architecture diagrams** showing component relationships
2. **File manifest** listing all files to create
3. **Inline decisions** with rationale (ADRs)
4. **Code patterns** that are copy-paste ready
5. **Testing strategy** aligned with acceptance tests

---

## The Golden Rules

### 1. Stay Grounded in Define

Every Design element traces back to a requirement:

```text
DEFINE: "System MUST process invoices in <30s"
        ↓
DESIGN: "Use async processing with Pub/Sub to handle burst load"
        (Decision rationale: Async enables horizontal scaling
         to meet 30s SLA under burst conditions)
```

### 2. File Manifest is Complete

Before Build starts, every file is identified:

| ✅ Complete Manifest | ❌ Incomplete Manifest |
|---------------------|----------------------|
| All source files listed | "And other supporting files" |
| Dependencies clear | "Components as needed" |
| Creation order defined | Files listed randomly |

### 3. Decisions Have Rationale

No unexplained choices:

```markdown
### Decision: Message Queue

**Options Considered**:
1. Pub/Sub - GCP native, serverless
2. RabbitMQ - Feature-rich, self-hosted
3. Kafka - High throughput, complex

**Selected**: Pub/Sub

**Rationale**: Native GCP integration reduces operational burden;
serverless aligns with Cloud Run architecture; sufficient for
2,000 messages/month volume.
```

---

## The Pattern

### Step 1: Architecture Diagram

Visual overview of the system:

```markdown
## Architecture

```text
                    ┌─────────────────────────────────────────────────────┐
                    │                    GCP                               │
                    │                                                      │
┌──────────┐        │  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  TIFF    │───────▶│  │  TIFF→   │───▶│ CLASSIFY │───▶│ EXTRACT  │      │
│  Input   │        │  │  PNG     │    │          │    │ (Gemini) │      │
└──────────┘        │  └──────────┘    └──────────┘    └──────────┘      │
                    │        │              │               │             │
                    │        └──────────────┴───────────────┴───▶ Pub/Sub │
                    │                                             │       │
                    │                                             ▼       │
                    │  ┌──────────────────────────────────────────────┐  │
                    │  │                  BigQuery                     │  │
                    │  │              (Invoice Data)                   │  │
                    │  └──────────────────────────────────────────────┘  │
                    └─────────────────────────────────────────────────────┘
```
```

### Step 2: Key Decisions (Inline ADRs)

Document decisions within the Design document:

```markdown
## Key Decisions

### D-001: Cloud Provider

**Context**: Need serverless compute with LLM integration

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| GCP | Native Vertex AI, Cloud Run | Smaller ecosystem |
| AWS | Lambda mature, broad services | Bedrock less integrated |
| Azure | Enterprise features | Higher complexity |

**Decision**: GCP

**Rationale**: Gemini (Vertex AI) is primary LLM; native integration
reduces latency and authentication complexity.

**Consequences**:
- Locked to GCP for MVP
- Team needs GCP skills
- Easy Gemini integration

---

### D-002: Function Architecture

**Context**: Processing pipeline with multiple stages

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| Monolith | Simple deployment | Hard to scale stages independently |
| Microservices | Independent scaling | Operational overhead |
| Functions | Event-driven, serverless | Cold start latency |

**Decision**: Cloud Run Functions (serverless)

**Rationale**: Event-driven pipeline naturally maps to functions;
independent scaling per stage; no infrastructure management.

**Consequences**:
- Need to manage cold starts
- Function-to-function communication via Pub/Sub
- Stateless design required
```

### Step 3: File Manifest

Complete list with dependencies and order:

```markdown
## File Manifest

### Shared Library

| # | File | Purpose | Dependencies |
|---|------|---------|--------------|
| 1 | `shared/schemas/invoice.py` | Pydantic models | None |
| 2 | `shared/schemas/messages.py` | Pub/Sub message models | invoice.py |
| 3 | `shared/adapters/storage.py` | GCS adapter | schemas |
| 4 | `shared/adapters/messaging.py` | Pub/Sub adapter | schemas |
| 5 | `shared/adapters/llm.py` | Gemini adapter | schemas |
| 6 | `shared/utils/logging.py` | Structured logging | None |

### Functions

| # | File | Purpose | Dependencies |
|---|------|---------|--------------|
| 7 | `functions/tiff_to_png/main.py` | Image conversion | shared/adapters |
| 8 | `functions/classifier/main.py` | Vendor detection | shared/adapters |
| 9 | `functions/extractor/main.py` | LLM extraction | shared/adapters |
| 10 | `functions/writer/main.py` | BigQuery write | shared/adapters |

### Tests

| # | File | Purpose | Dependencies |
|---|------|---------|--------------|
| 11 | `tests/unit/test_schemas.py` | Schema tests | schemas |
| 12 | `tests/unit/test_adapters.py` | Adapter tests | adapters |
| 13 | `tests/integration/test_pipeline.py` | E2E tests | all |
```

### Step 4: Code Patterns

Copy-paste ready examples:

```markdown
## Code Patterns

### Pattern: Pydantic Model with Validation

```python
from pydantic import BaseModel, Field, computed_field, model_validator
from decimal import Decimal
from datetime import date
from typing import Self

class LineItem(BaseModel):
    """Single line item from invoice."""

    description: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0)

    @computed_field
    @property
    def amount(self) -> Decimal:
        return self.quantity * self.unit_price

class Invoice(BaseModel):
    """Extracted invoice data."""

    vendor: str
    invoice_number: str
    invoice_date: date
    line_items: list[LineItem] = Field(..., min_length=1)
    total: Decimal

    @model_validator(mode='after')
    def validate_total(self) -> Self:
        calculated = sum(item.amount for item in self.line_items)
        if abs(calculated - self.total) > Decimal('0.01'):
            raise ValueError(f"Total mismatch: {calculated} != {self.total}")
        return self
```

### Pattern: Cloud Run Function Entry Point

```python
import functions_framework
from cloudevents.http import CloudEvent
from shared.adapters.storage import GCSAdapter
from shared.adapters.messaging import PubSubAdapter
from shared.utils.logging import get_logger

logger = get_logger(__name__)

@functions_framework.cloud_event
def handle_event(cloud_event: CloudEvent) -> None:
    """Process incoming cloud event."""
    logger.info("Processing event", extra={
        "event_id": cloud_event["id"],
        "event_type": cloud_event["type"]
    })

    try:
        # Process the event
        result = process(cloud_event.data)
        logger.info("Processing complete", extra={"result": result})
    except Exception as e:
        logger.error("Processing failed", exc_info=True)
        raise
```
```

### Step 5: Testing Strategy

Map acceptance tests to test types:

```markdown
## Testing Strategy

### Test Coverage Matrix

| Acceptance Test | Unit Test | Integration Test | E2E Test |
|-----------------|-----------|------------------|----------|
| AT-001: Happy path | ✓ | ✓ | ✓ |
| AT-002: Multi-page | ✓ | ✓ | |
| AT-003: All vendors | ✓ | ✓ | ✓ |
| AT-004: Invalid file | ✓ | ✓ | |
| AT-005: Duplicate | | ✓ | |

### Test Structure

```text
tests/
├── unit/
│   ├── test_schemas.py      # Pydantic model tests
│   ├── test_extraction.py   # Extraction logic tests
│   └── conftest.py          # Fixtures
├── integration/
│   ├── test_storage.py      # GCS adapter tests
│   ├── test_messaging.py    # Pub/Sub adapter tests
│   └── test_llm.py          # Gemini adapter tests (mocked)
└── e2e/
    └── test_pipeline.py     # Full pipeline tests
```
```

### Step 6: Implementation Phases

Sequence the work:

```markdown
## Implementation Phases

### Phase 1: Shared Library (Day 1)

| Task | Files | Verification |
|------|-------|--------------|
| Create schemas | schemas/*.py | pytest test_schemas.py |
| Create adapters | adapters/*.py | pytest test_adapters.py |
| Create utilities | utils/*.py | Import succeeds |

### Phase 2: Functions (Days 2-3)

| Task | Files | Verification |
|------|-------|--------------|
| TIFF converter | functions/tiff_to_png/* | Manual test with sample |
| Classifier | functions/classifier/* | Vendor detection test |
| Extractor | functions/extractor/* | LLM extraction test |
| Writer | functions/writer/* | BigQuery write test |

### Phase 3: Integration (Day 4)

| Task | Files | Verification |
|------|-------|--------------|
| Wire Pub/Sub | Deploy all functions | E2E test passes |
| Error handling | Add DLQ | Invalid file test |
| Metrics | Add logging | Metrics visible |
```

---

## Quality Gate

Before proceeding to Build:

| Criteria | Check |
|----------|-------|
| Architecture diagram present | ☐ |
| All decisions documented with rationale | ☐ |
| File manifest complete (no "etc.") | ☐ |
| Dependencies between files clear | ☐ |
| Code patterns included (not pseudo-code) | ☐ |
| Testing strategy maps to acceptance tests | ☐ |
| Implementation phases sequenced | ☐ |

---

## Output Template

```markdown
# DESIGN: {Feature Name}

> Technical architecture for {feature}

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {date} |
| **Author** | design-agent |
| **Source** | DEFINE_{FEATURE}.md |

---

## Architecture

{ASCII/Mermaid diagram}

---

## Key Decisions

### D-001: {Decision Title}

**Context**: {Why this decision is needed}

**Options**:
| Option | Pros | Cons |
|--------|------|------|

**Decision**: {Selected option}

**Rationale**: {Why this option}

**Consequences**: {Impact of this choice}

---

## File Manifest

{Complete table of files}

---

## Code Patterns

{Copy-paste ready examples}

---

## Testing Strategy

{Test coverage matrix and structure}

---

## Implementation Phases

{Sequenced phases with verification}

---

## Next Step

`/build .claude/sdd/features/DESIGN_{FEATURE}.md`
```

---

## Common Pitfalls

### 1. Incomplete File Manifest

❌ **Wrong**:
```markdown
- Main application files
- Supporting utilities
- Tests as needed
```

✅ **Right**:
```markdown
| File | Purpose | Dependencies |
|------|---------|--------------|
| src/main.py | Entry point | config.py |
| src/config.py | Configuration | None |
| tests/test_main.py | Main tests | main.py |
```

### 2. Decisions Without Rationale

❌ **Wrong**:
```markdown
We'll use PostgreSQL for the database.
```

✅ **Right**:
```markdown
### Decision: Database

**Options**: PostgreSQL, MongoDB, SQLite
**Decision**: PostgreSQL
**Rationale**: ACID compliance required for financial data;
team has PostgreSQL expertise; mature tooling.
```

### 3. Pseudo-code Instead of Real Code

❌ **Wrong**:
```markdown
// pseudocode
for each invoice:
    extract data
    validate
    save to database
```

✅ **Right**:
```python
async def process_invoice(invoice: Invoice) -> Result:
    extracted = await extractor.extract(invoice.image)
    validated = InvoiceSchema.model_validate(extracted)
    await repository.save(validated)
    return Result(success=True, invoice_id=validated.id)
```

---

## Next Steps

- **After Design**: [build-pattern.md](build-pattern.md)
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Example**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)

---

*References: AgentSpec 4.2 Phase 2, Spec-Kit plan-template.md*
