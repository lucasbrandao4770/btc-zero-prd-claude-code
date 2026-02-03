# Advanced SDD Patterns

> Complex project patterns and team coordination

---

## Multi-Phase Features

Large features often span multiple Define → Ship cycles.

### Pattern: Phase-Based Delivery

```text
FEATURE: Invoice Processing Pipeline
├── Phase 1: Core Extraction
│   └── Define → Design → Build → Ship
├── Phase 2: Observability
│   └── Define → Design → Build → Ship
├── Phase 3: Autonomous Monitoring
│   └── Define → Design → Build → Ship
└── Phase 4: Production Hardening
    └── Define → Design → Build → Ship
```

### How to Structure

```markdown
# DEFINE: Invoice Pipeline Phase 1 (Core Extraction)

## Context
This is Phase 1 of a 4-phase feature.

## Phase Dependencies
| Phase | Status | Depends On |
|-------|--------|------------|
| Phase 1: Core | This phase | None |
| Phase 2: Observability | Not started | Phase 1 |
| Phase 3: Monitoring | Not started | Phase 2 |
| Phase 4: Production | Not started | Phase 3 |

## Scope for THIS Phase
- TIFF to PNG conversion
- Vendor classification
- Data extraction
- BigQuery storage

## Deferred to Later Phases
- LangFuse observability (Phase 2)
- CrewAI monitoring (Phase 3)
- Multi-environment deployment (Phase 4)
```

### Benefits

- Deliverable value at each phase
- Clear boundaries prevent scope creep
- Each phase can be re-prioritized independently

---

## Team Coordination

### Pattern: Parallel Feature Development

Multiple features can be developed simultaneously:

```text
Week 1:
├── Dev A: Feature X (Phase: Design)
├── Dev B: Feature Y (Phase: Define)
└── Dev C: Feature Z (Phase: Build)

Week 2:
├── Dev A: Feature X (Phase: Build)
├── Dev B: Feature Y (Phase: Design)
└── Dev C: Feature Z (Phase: Ship)
```

### Coordination via Artifacts

```markdown
# DEFINE: Feature X

## Integration Points
| System | Interface | Owner |
|--------|-----------|-------|
| Feature Y | EventPublisher | Dev B |
| Feature Z | DataSchema | Dev C |

## External Dependencies
- Feature Y must publish UserCreated event
- Feature Z must provide InvoiceSchema v2
```

### Handoff Protocol

When passing between team members:

```markdown
## Handoff: Feature X (Define → Design)

**From**: Dev A (Define complete)
**To**: Dev B (Design starting)

**Artifacts Delivered**:
- DEFINE_FEATURE_X.md (Clarity Score: 14/15)
- All acceptance tests defined
- Out of scope clearly documented

**Key Decisions Made**:
- Using PostgreSQL (not MongoDB) - rationale in Define
- API-first approach - contracts defined in acceptance tests

**Open Questions**:
- None - ready for Design

**Contact for Clarification**: Dev A available via Slack
```

---

## Cross-Feature Dependencies

### Pattern: Shared Component Extraction

When multiple features need the same component:

```text
Feature A: Invoice Pipeline
Feature B: Receipt Scanner
Feature C: Document Classifier
         ↓
All need: Image Processing Library
         ↓
Extract: Shared Component with its own SDD cycle
```

```markdown
# DEFINE: Shared Image Processing Library

## Consuming Features
| Feature | Required Capability |
|---------|-------------------|
| Invoice Pipeline | TIFF → PNG conversion |
| Receipt Scanner | JPEG optimization |
| Document Classifier | Image normalization |

## Interface Contract
```python
class ImageProcessor(Protocol):
    def convert(self, input: bytes, output_format: str) -> bytes: ...
    def optimize(self, image: bytes, quality: int) -> bytes: ...
    def normalize(self, image: bytes, size: tuple[int, int]) -> bytes: ...
```

## Versioning Strategy
- Semantic versioning (major.minor.patch)
- Breaking changes require major version bump
- All consumers must migrate within 2 sprints
```

### Dependency Management

```markdown
## DESIGN: Invoice Pipeline

## Dependencies
| Component | Version | Owner | Interface |
|-----------|---------|-------|-----------|
| image-processing | ^1.2.0 | Platform Team | ImageProcessor |
| llm-gateway | ^2.0.0 | AI Team | LLMAdapter |

## Version Pinning Strategy
- Pin to minor version (^1.2.0)
- Auto-update patches
- Review breaking changes in Design phase
```

---

## Large Codebase Strategies

### Pattern: Bounded Contexts

For microservices or modular monoliths:

```text
.claude/sdd/
├── contexts/
│   ├── billing/
│   │   ├── features/
│   │   ├── reports/
│   │   └── archive/
│   ├── authentication/
│   │   ├── features/
│   │   └── archive/
│   └── analytics/
│       ├── features/
│       └── archive/
└── shared/
    └── features/   # Cross-cutting concerns
```

### Context Ownership

```markdown
## Context: Billing

**Owner**: Finance Team
**Scope**: Invoicing, payments, reconciliation

## SDD Rules for This Context
- All features must include compliance check
- Acceptance tests must cover audit trail
- Design must address PCI compliance

## Integration Points
| Context | Interface | Protocol |
|---------|-----------|----------|
| Authentication | UserID | JWT claim |
| Analytics | Events | Pub/Sub |
```

---

## Advanced Quality Patterns

### Pattern: Multi-Level Acceptance Tests

```markdown
## Acceptance Tests

### Unit Level (Build phase)
| ID | Scenario | Verification |
|----|----------|--------------|
| AT-001 | Invoice parsing | pytest test_parser.py |
| AT-002 | Validation rules | pytest test_validator.py |

### Integration Level (Build phase)
| ID | Scenario | Verification |
|----|----------|--------------|
| AT-003 | GCS ↔ Function | pytest test_integration.py |
| AT-004 | Function ↔ Pub/Sub | pytest test_messaging.py |

### E2E Level (Post-Build)
| ID | Scenario | Verification |
|----|----------|--------------|
| AT-005 | Full pipeline | smoke_test.py --env=dev |
| AT-006 | Error handling | smoke_test.py --scenario=errors |

### Manual Verification (Pre-Ship)
| ID | Scenario | Verification |
|----|----------|--------------|
| AT-007 | UI walkthrough | QA checklist |
| AT-008 | Performance | Load test results |
```

### Pattern: Risk-Based Testing

```markdown
## Testing Strategy

### Risk Assessment
| Component | Risk Level | Coverage Required |
|-----------|-----------|-------------------|
| Payment processing | Critical | 95%+ |
| User preferences | Low | 70%+ |
| Reports | Medium | 80%+ |

### Test Distribution
| Risk Level | Unit | Integration | E2E |
|------------|------|-------------|-----|
| Critical | ✓ | ✓ | ✓ |
| Medium | ✓ | ✓ | Sample |
| Low | ✓ | Key paths | — |
```

---

## Advanced Iteration Patterns

### Pattern: Cascading Updates

When a Define change affects Design and Build:

```bash
# Requirement change discovered
/iterate DEFINE_FEATURE.md "Add support for PDF format"

# Automatically trigger
# → Check impact on DESIGN
# → Identify Build components affected
# → Generate change list

# Then update Design
/iterate DESIGN_FEATURE.md "Add PDF parsing component to architecture"

# Build continues with new components
/build .claude/sdd/features/DESIGN_FEATURE.md
```

### Impact Analysis Template

```markdown
## Iteration: Add PDF Support

### Change Request
- Add PDF parsing to existing TIFF pipeline

### Impact Analysis
| Artifact | Impact | Required Changes |
|----------|--------|------------------|
| DEFINE | Medium | Add PDF to requirements |
| DESIGN | High | New parser component, file manifest |
| BUILD | High | 3 new files, 2 modified |
| Tests | Medium | 5 new test cases |

### Effort Estimate
- Define update: 30 min
- Design update: 1 hour
- Additional Build: 4 hours

### Recommendation
Proceed with iteration (manageable scope)
```

---

## Enterprise Patterns

### Pattern: Compliance Integration

```markdown
# DEFINE: Payment Processing

## Compliance Requirements
| Regulation | Requirement | Verification |
|------------|-------------|--------------|
| PCI-DSS | No card storage | Design review |
| SOX | Audit trail | Acceptance test |
| GDPR | Data minimization | Code review |

## Compliance Gates
- [ ] Security review before Design
- [ ] Compliance sign-off before Build
- [ ] Audit trail verification before Ship
```

### Pattern: Change Advisory Board

```markdown
## DESIGN: Database Migration

## CAB Review Required

### Reason
Production database schema change

### Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss | Low | Critical | Backup + rollback |
| Downtime | Medium | High | Blue-green deployment |

### CAB Submission
- [ ] DESIGN document attached
- [ ] Risk assessment complete
- [ ] Rollback plan documented
- [ ] Schedule proposed
```

---

## Automation Patterns

### Pattern: SDD Pipeline Integration

```yaml
# .github/workflows/sdd-validation.yml
name: SDD Validation

on:
  push:
    paths:
      - '.claude/sdd/features/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check Clarity Score
        run: |
          score=$(grep "Clarity Score" $FILE | grep -oP '\d+')
          if [ $score -lt 12 ]; then
            echo "Clarity Score too low: $score/15"
            exit 1
          fi

      - name: Validate File Manifest
        run: |
          # Check all manifested files exist or are planned
          python scripts/validate_manifest.py $FILE
```

### Pattern: Artifact Generation

```bash
# Auto-generate documentation from SDD artifacts
sdd-tools generate-docs \
  --define .claude/sdd/features/DEFINE_*.md \
  --design .claude/sdd/features/DESIGN_*.md \
  --output docs/

# Auto-generate test stubs from acceptance tests
sdd-tools generate-tests \
  --define .claude/sdd/features/DEFINE_*.md \
  --output tests/acceptance/
```

---

## Measuring SDD Success

### Metrics Dashboard

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Clarity Score avg | Mean of all DEFINE scores | ≥ 13/15 |
| First-pass success | Features shipped without /iterate | ≥ 70% |
| Cycle time | Define start → Ship complete | Trend down |
| Rework rate | Post-Ship changes needed | ≤ 10% |
| Documentation coverage | Features with full SDD artifacts | 100% for new |

### Retrospective Questions

After each Ship:

1. **Process**: Did SDD help or hinder?
2. **Phases**: Which phase was hardest? Why?
3. **Iteration**: How many /iterate commands? Why?
4. **Quality**: Were acceptance tests sufficient?
5. **Improvement**: What would we change?

---

## Resources

- **Getting started**: [getting-started.md](getting-started.md)
- **Migration guide**: [migrating-to-sdd.md](migrating-to-sdd.md)
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Real example**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)

---

*Master the basics, then adapt to your context.*
