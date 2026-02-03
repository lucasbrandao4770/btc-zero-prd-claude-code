# Example: UberEats Invoice Pipeline

> Real-world SDD walkthrough from the Bootcamp project

---

## Overview

The Invoice Pipeline is a production feature built using SDD during the AI Data Engineering Bootcamp. It demonstrates the full SDD lifecycle with real artifacts.

| Attribute | Value |
|-----------|-------|
| **Feature** | INVOICE_PIPELINE |
| **Duration** | 4 days (Jan 27-30, 2026) |
| **Phases** | Brainstorm → Define → Design → Build → Ship |
| **Complexity** | High (4 Cloud Run functions, multi-service) |
| **Archive** | `.claude/sdd/archive/INVOICE_PIPELINE/` |

---

## Business Context

### The Problem

The Finance team at a restaurant group spent **80% of their time** on manual data entry from delivery platform invoices, causing:

- **R$45,000+ in reconciliation errors** quarterly
- **15% error rate** on complex invoices
- Inability to scale (2,000+ invoices/month, growing to 3,500)
- Compliance risk from delayed reconciliation

### The Solution

AI-powered serverless pipeline using Gemini 2.0 Flash for document extraction:

```text
TIFF Input → PNG Conversion → Classification → Extraction → BigQuery
```

---

## Phase 0: Brainstorm

### Initial Prompt

```text
/brainstorm "I need to automate invoice processing from delivery
platforms like UberEats, DoorDash, etc."
```

### Key Questions Asked

1. **Volume**: "How many invoices per month?"
   - Answer: 2,000 currently, projected 3,500

2. **Formats**: "What file formats do you receive?"
   - Answer: TIFF files from scanning

3. **Accuracy**: "What accuracy level is acceptable?"
   - Answer: 90%+ per field, critical for reconciliation

4. **Vendors**: "Which platforms to support?"
   - Answer: UberEats, DoorDash, Grubhub, iFood, Rappi

### Approaches Explored

| Approach | Pros | Cons |
|----------|------|------|
| **Vendor-by-vendor** | Lower initial risk | Slow to full coverage |
| **Function-by-function** | Parallel development | More complex testing |
| **All-at-once** | Fastest to feature-complete | Higher risk |

**Selected**: Function-by-function with all 5 vendors from day 1

### YAGNI Applied

| Removed | Reason |
|---------|--------|
| Email notifications | Not in initial requirements |
| Real-time dashboard | BigQuery queries sufficient |
| PDF support | TIFF only for MVP |
| Handwritten invoices | Focus on printed/digital |

---

## Phase 1: Define

### Problem Statement

```markdown
The Finance team spends **80% of their time** on manual data entry
from delivery platform invoices, causing **R$45,000+ in reconciliation
errors** quarterly.
```

### Goals (MoSCoW)

| Priority | Goal |
|----------|------|
| **MUST** | Extract invoice data with ≥90% accuracy |
| **MUST** | Process invoices in <30 seconds (P95) |
| **MUST** | Support all 5 vendors |
| **SHOULD** | Achieve pipeline availability >99% |
| **SHOULD** | Keep cost per invoice <$0.01 |
| **COULD** | Archive originals for 7-year compliance |

### Success Criteria

| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Extraction accuracy | ≥90% per field |
| SC-002 | Processing latency | P95 < 30s |
| SC-003 | Vendor coverage | 5/5 vendors |
| SC-004 | Pipeline uptime | >99% |
| SC-005 | Cost per invoice | <$0.01 |

### Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Happy path | Valid UberEats TIFF | Upload to GCS | Data in BigQuery in 30s |
| AT-002 | Multi-page | 2-page invoice | Process | Both pages extracted |
| AT-003 | All vendors | 5 vendor invoices | Process all | All extracted correctly |
| AT-004 | Invalid file | Corrupted TIFF | Process | Moved to failed bucket |
| AT-005 | Duplicate | Same invoice twice | Process | Deduplication prevents duplicate |

### Clarity Score

| Element | Score | Notes |
|---------|-------|-------|
| Problem | 3 | Clear with numbers |
| Users | 3 | Three personas defined |
| Goals | 3 | MoSCoW prioritized |
| Success | 3 | Measurable criteria |
| Scope | 3 | 7 items out of scope |
| **Total** | **15/15** | ✅ |

---

## Phase 2: Design

### Architecture

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                            GCP Cloud Run Functions                         │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │ TIFF→PNG │───▶│ CLASSIFY │───▶│ EXTRACT  │───▶│  WRITE   │           │
│  │          │    │          │    │ (Gemini) │    │          │           │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘           │
│       │               │               │               │                   │
│       └───────────────┴───────────────┴───────────────┘                   │
│                          Pub/Sub Events                                    │
│                               │                                            │
│                          ┌────┴────┐                                      │
│                          │   DLQ   │                                      │
│                          │Processor│                                      │
│                          └─────────┘                                      │
└───────────────────────────────────────────────────────────────────────────┘
```

### Key Decisions

#### D-001: Cloud Provider

**Decision**: GCP

**Rationale**: Native Vertex AI (Gemini) integration reduces latency and auth complexity. Cloud Run Functions align with serverless, event-driven architecture.

#### D-002: Function Architecture

**Decision**: 4 separate Cloud Run Functions

**Rationale**:
- Independent scaling per stage
- Easier debugging and monitoring
- Event-driven via Pub/Sub
- Failure isolation

#### D-003: LLM Selection

**Decision**: Gemini 2.0 Flash via Vertex AI

**Rationale**:
- Multimodal (handles images directly)
- Fast inference for <30s latency
- GCP-native integration
- Cost-effective for volume

### File Manifest

| # | File | Purpose |
|---|------|---------|
| 1 | `shared/schemas/invoice.py` | Pydantic extraction models |
| 2 | `shared/schemas/messages.py` | Pub/Sub message schemas |
| 3 | `shared/adapters/storage.py` | GCS adapter |
| 4 | `shared/adapters/messaging.py` | Pub/Sub adapter |
| 5 | `shared/adapters/llm.py` | Gemini adapter |
| 6 | `shared/utils/logging.py` | Structured logging |
| 7 | `functions/tiff_to_png/main.py` | Image conversion |
| 8 | `functions/classifier/main.py` | Vendor detection |
| 9 | `functions/extractor/main.py` | LLM extraction |
| 10 | `functions/writer/main.py` | BigQuery persistence |
| 11 | `tests/unit/test_schemas.py` | Schema tests |
| 12 | `tests/integration/test_pipeline.py` | E2E tests |

### Code Patterns

```python
# Pattern: Pydantic Model with Computed Fields
class LineItem(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0)

    @computed_field
    @property
    def amount(self) -> Decimal:
        return self.quantity * self.unit_price

# Pattern: Model Validator
class Invoice(BaseModel):
    line_items: list[LineItem]
    total: Decimal

    @model_validator(mode='after')
    def validate_total(self) -> Self:
        calculated = sum(item.amount for item in self.line_items)
        if abs(calculated - self.total) > Decimal('0.01'):
            raise ValueError(f"Total mismatch")
        return self
```

---

## Phase 3: Build

### Execution Summary

| Phase | Duration | Files | Tests |
|-------|----------|-------|-------|
| Shared Library | Day 1 | 6 files | 12 tests |
| Functions | Days 2-3 | 4 files | 8 tests |
| Integration | Day 4 | 2 files | 6 tests |

### Verification Results

```text
tests/unit/test_schemas.py .................... PASSED (12/12)
tests/unit/test_adapters.py ................... PASSED (8/8)
tests/integration/test_pipeline.py ............ PASSED (6/6)

======================== 26 passed in 12.45s ========================
```

### Deviations from Design

| ID | Design Said | Changed To | Reason |
|----|-------------|-----------|--------|
| D-001 | Single retry on failure | 3 retries with backoff | Vertex AI rate limits |
| D-002 | JSON logging | Structured + Cloud Logging | Better GCP integration |

### Acceptance Test Results

| ID | Scenario | Status |
|----|----------|--------|
| AT-001 | Happy path | ✅ PASS |
| AT-002 | Multi-page | ✅ PASS |
| AT-003 | All vendors | ✅ PASS |
| AT-004 | Invalid file | ✅ PASS |
| AT-005 | Duplicate | ✅ PASS |

---

## Phase 4: Ship

### Lessons Learned

#### What Went Well

1. **Pydantic validation** caught 15 edge cases during development
2. **File manifest** prevented scope creep
3. **Adapter pattern** enabled testing without cloud dependencies
4. **Clarity Score** forced clear requirements upfront

#### What Could Improve

1. **Design underestimated** BigQuery schema complexity
2. **Missing error path tests** in initial acceptance tests
3. **Late discovery** of Vertex AI quota limits

#### Recommendations

1. Add data model diagrams to Design template
2. Include explicit error path acceptance tests
3. Add "cloud quotas" to Define constraints checklist
4. Start integration tests earlier in Build phase

### Metrics Achieved

| Metric | Target | Actual |
|--------|--------|--------|
| Extraction accuracy | ≥90% | 92% |
| P95 latency | <30s | 18s |
| Vendor coverage | 5/5 | 5/5 |
| Test coverage | >80% | 87% |

---

## Artifacts

All artifacts archived at:

```text
.claude/sdd/archive/INVOICE_PIPELINE/
├── BRAINSTORM_INVOICE_PIPELINE.md
├── DEFINE_INVOICE_PIPELINE.md
├── DESIGN_INVOICE_PIPELINE.md
├── BUILD_REPORT_INVOICE_PIPELINE.md
└── SHIPPED_2026-01-30.md
```

---

## Key Takeaways

### For SDD Practitioners

1. **High Clarity Score pays off** - 15/15 meant no surprises in Design
2. **File manifest is critical** - Every file listed, no scope creep
3. **Acceptance tests become verification** - AT-001 through AT-005 guided Build
4. **Lessons learned improve future work** - Recommendations already applied to next features

### For This Domain (Invoice Processing)

1. **Multimodal LLMs work** - Gemini handled varied invoice formats
2. **Event-driven suits batch** - Pub/Sub handled burst uploads well
3. **Pydantic essential** - Structured outputs prevent downstream errors

---

## Related Features

Built after Invoice Pipeline using SDD:

| Feature | Purpose | Shipped |
|---------|---------|---------|
| GCS_UPLOAD | Invoice generator GCS integration | 2026-01-31 |
| LANGFUSE_OBSERVABILITY | LLM observability | 2026-01-31 |
| SMOKE_TEST | E2E testing framework | 2026-01-31 |
| TERRAFORM_TERRAGRUNT_INFRA | Infrastructure as Code | 2026-01-31 |

---

## Resources

- **Full Define document**: `.claude/sdd/archive/INVOICE_PIPELINE/DEFINE_INVOICE_PIPELINE.md`
- **Full Design document**: `.claude/sdd/archive/INVOICE_PIPELINE/DESIGN_INVOICE_PIPELINE.md`
- **Bootcamp materials**: `D:/Work/25.12 - xx.xx Plumbers/Bootcamp/`
- **Project CLAUDE.md**: Project context and architecture

---

*This example demonstrates SDD's value: 4-day delivery with 92% accuracy and full documentation.*
