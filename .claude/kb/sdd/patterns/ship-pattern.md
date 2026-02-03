# Ship Pattern

> Archiving with lessons learned (CLOSE)

---

## Purpose

The Ship phase completes the SDD lifecycle by:

1. **Verifying** all quality gates passed
2. **Archiving** all artifacts for future reference
3. **Documenting** lessons learned for institutional knowledge
4. **Updating** project documentation
5. **Closing** the feature formally

---

## The Golden Rules

### 1. Ship Only When Complete

All quality gates must pass:

```text
☑ Define: Clarity Score ≥ 12/15
☑ Design: Complete file manifest, decisions documented
☑ Build: All tests pass, acceptance tests verified
         ↓
☑ Ship: Archive and document
```

### 2. Capture Lessons Learned

Every feature teaches something:

- What worked well?
- What could improve?
- What would you do differently?

### 3. Archive for Discoverability

Future developers should find and understand past work:

```text
archive/
└── INVOICE_PIPELINE/
    ├── BRAINSTORM_INVOICE_PIPELINE.md
    ├── DEFINE_INVOICE_PIPELINE.md
    ├── DESIGN_INVOICE_PIPELINE.md
    ├── BUILD_REPORT_INVOICE_PIPELINE.md
    └── SHIPPED_2026-01-30.md    # <-- Summary with lessons
```

---

## The Pattern

### Step 1: Verify All Gates

Checklist before shipping:

```markdown
## Pre-Ship Verification

### Define Phase
- [x] Clarity Score: 15/15 (≥12/15 required)
- [x] All acceptance tests defined
- [x] Out of scope documented

### Design Phase
- [x] Architecture diagram present
- [x] All decisions documented with rationale
- [x] Complete file manifest
- [x] Code patterns included

### Build Phase
- [x] All files from manifest created
- [x] Lint check passes
- [x] Type check passes
- [x] All unit tests pass
- [x] All integration tests pass
- [x] Acceptance tests verified

### Overall
- [x] No open blockers
- [x] No unresolved [NEEDS CLARIFICATION] markers
- [x] BUILD_REPORT complete
```

### Step 2: Move to Archive

Organize artifacts:

```bash
# Create archive folder
mkdir -p .claude/sdd/archive/INVOICE_PIPELINE

# Move all feature artifacts
mv .claude/sdd/features/BRAINSTORM_INVOICE_PIPELINE.md \
   .claude/sdd/archive/INVOICE_PIPELINE/

mv .claude/sdd/features/DEFINE_INVOICE_PIPELINE.md \
   .claude/sdd/archive/INVOICE_PIPELINE/

mv .claude/sdd/features/DESIGN_INVOICE_PIPELINE.md \
   .claude/sdd/archive/INVOICE_PIPELINE/

mv .claude/sdd/reports/BUILD_REPORT_INVOICE_PIPELINE.md \
   .claude/sdd/archive/INVOICE_PIPELINE/
```

### Step 3: Document Lessons Learned

Create SHIPPED document:

```markdown
# SHIPPED: Invoice Pipeline

> Shipped 2026-01-30

## Summary

**Feature**: Serverless invoice extraction pipeline
**Duration**: 4 days (Jan 27-30, 2026)
**Phases Completed**: Brainstorm → Define → Design → Build → Ship

---

## What Went Well

### 1. Pydantic Validation Caught Edge Cases
The strict Pydantic models caught 15 edge cases during development
that would have been runtime errors in production.

### 2. File Manifest Prevented Scope Creep
Having every file listed upfront prevented "while I'm here" additions
that could have delayed shipping.

### 3. Adapter Pattern Enabled Testing
Protocol-based adapters made it easy to mock GCS/Pub/Sub for tests,
achieving 87% coverage without cloud dependencies.

---

## What Could Improve

### 1. Design Underestimated Complexity
BigQuery schema design took longer than expected. Should have
included data model diagrams in Design phase.

### 2. Missing Error Path Tests
Acceptance tests covered happy paths well, but error handling
scenarios were discovered during integration.

### 3. Late Discovery of Quota Limits
Vertex AI quota limits weren't checked until Build phase.
Should be a Define-phase constraint.

---

## Recommendations for Next Time

1. **Add data model diagrams to Design template**
2. **Include explicit error path acceptance tests**
3. **Add "cloud quotas" to Define constraints checklist**
4. **Start integration tests earlier in Build phase**

---

## Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Extraction accuracy | ≥90% | 92% |
| P95 latency | <30s | 18s |
| Test coverage | >80% | 87% |
| Deviations from Design | 0 | 2 |

---

## Artifacts

| Document | Location |
|----------|----------|
| Brainstorm | `archive/INVOICE_PIPELINE/BRAINSTORM_INVOICE_PIPELINE.md` |
| Define | `archive/INVOICE_PIPELINE/DEFINE_INVOICE_PIPELINE.md` |
| Design | `archive/INVOICE_PIPELINE/DESIGN_INVOICE_PIPELINE.md` |
| Build Report | `archive/INVOICE_PIPELINE/BUILD_REPORT_INVOICE_PIPELINE.md` |

---

## Related

- Follow-up feature: LangFuse Observability (GCS_UPLOAD)
- Blocked by this: CrewAI Monitoring (deferred to Phase 2)
```

### Step 4: Update Project Documentation

Update relevant docs:

```markdown
## Updates Made

1. **CLAUDE.md**: Added feature to "Shipped Features" section
2. **README.md**: Updated architecture diagram
3. **CHANGELOG.md**: Added entry for v1.0.0
```

### Step 5: Clean Up

Remove working files:

```bash
# Features folder should be clean after Ship
ls .claude/sdd/features/
# (empty or only active features)

# Reports folder archived
ls .claude/sdd/reports/
# (empty or only active reports)
```

---

## Lessons Learned Framework

### Categories

| Category | Questions to Answer |
|----------|-------------------|
| **Process** | Did SDD help? What phase was hardest? |
| **Technical** | What patterns worked? What broke? |
| **Estimation** | Accurate timeline? What took longer? |
| **Quality** | Test coverage adequate? Bugs found? |
| **Collaboration** | Handoffs smooth? Documentation clear? |

### Template for Each Lesson

```markdown
### Lesson: {Title}

**Context**: {What happened}
**Learning**: {What we learned}
**Action**: {What to do differently}
```

### Example Lessons

```markdown
### Lesson: Pydantic Computed Fields Save Time

**Context**: Initially wrote separate calculation functions for
invoice totals and line item amounts.

**Learning**: Pydantic's @computed_field decorator handles derived
values elegantly, reducing code and ensuring consistency.

**Action**: Use computed_field for all derived values in future models.

---

### Lesson: Integration Tests Need Real Infrastructure

**Context**: Unit tests with mocks passed, but integration tests
revealed GCS bucket naming restrictions.

**Learning**: Mocks can hide infrastructure-specific constraints.
Run against real services earlier.

**Action**: Add "infra smoke test" to Build phase, Day 1.
```

---

## Quality Gate

Before marking complete:

| Criteria | Check |
|----------|-------|
| All previous gates passed | ☐ |
| Artifacts moved to archive | ☐ |
| SHIPPED document created | ☐ |
| Lessons learned documented | ☐ |
| Project docs updated | ☐ |
| Working files cleaned up | ☐ |

---

## Output Template

```markdown
# SHIPPED: {Feature Name}

> Shipped {date}

## Summary

**Feature**: {description}
**Duration**: {X days}
**Phases Completed**: {phases}

---

## What Went Well

### 1. {Title}
{Description}

### 2. {Title}
{Description}

---

## What Could Improve

### 1. {Title}
{Description}

### 2. {Title}
{Description}

---

## Recommendations for Next Time

1. {Recommendation}
2. {Recommendation}

---

## Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| | | |

---

## Artifacts

| Document | Location |
|----------|----------|
| | |

---

## Related

- {Related features or follow-ups}
```

---

## Archive Organization

### Folder Structure

```text
.claude/sdd/archive/
├── INVOICE_PIPELINE/           # Feature name as folder
│   ├── BRAINSTORM_*.md
│   ├── DEFINE_*.md
│   ├── DESIGN_*.md
│   ├── BUILD_REPORT_*.md
│   └── SHIPPED_2026-01-30.md   # Date in filename
│
├── GCS_UPLOAD/
│   ├── DEFINE_*.md             # (No brainstorm - skipped)
│   ├── DESIGN_*.md
│   ├── BUILD_REPORT_*.md
│   └── SHIPPED_2026-01-31.md
│
└── LANGFUSE_OBSERVABILITY/
    └── ...
```

### Naming Conventions

| Artifact | Convention |
|----------|-----------|
| Folder | `{FEATURE_NAME}` (UPPER_SNAKE) |
| SHIPPED | `SHIPPED_{YYYY-MM-DD}.md` |
| Others | Original names preserved |

### Discoverability

Make archives searchable:

```bash
# Find all shipped features
ls .claude/sdd/archive/

# Search for specific decisions
grep -r "BigQuery" .claude/sdd/archive/

# Find features by date
find .claude/sdd/archive -name "SHIPPED_2026-01-*.md"
```

---

## Common Pitfalls

### 1. Shipping Incomplete Features

❌ **Wrong**:
```text
"Tests mostly pass, close enough..."
"We can fix that in a follow-up..."
```

✅ **Right**:
```text
"All gates pass. Creating follow-up task for optimization,
but MVP requirements are complete."
```

### 2. Skipping Lessons Learned

❌ **Wrong**:
```text
(Moves files to archive without reflection)
```

✅ **Right**:
```text
"What did this feature teach us?
- Pydantic validation saved time
- Should have added error path tests
Documenting in SHIPPED..."
```

### 3. Not Cleaning Up

❌ **Wrong**:
```text
(Leaves feature docs in features/ folder after shipping)
```

✅ **Right**:
```text
"Moved all INVOICE_PIPELINE artifacts to archive.
Features folder contains only active work."
```

---

## Model Assignment

| Task | Recommended Model |
|------|-------------------|
| Verification | Haiku (simple checks) |
| Lessons writing | Sonnet (balanced) |
| File operations | Haiku (fast) |

Ship phase is intentionally lightweight—most thinking happened in earlier phases.

---

## Integration with Project Management

After Ship:

1. **Close related tickets** (Linear, GitHub Issues)
2. **Update sprint board** (move to Done)
3. **Notify stakeholders** (Slack, email)
4. **Tag release** if applicable (git tag)

---

## Next Steps

- **After Ship**: Start new feature or iterate on existing
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Start new feature**: [brainstorm-pattern.md](brainstorm-pattern.md)

---

*References: AgentSpec 4.2 Phase 4, Spec-Kit post-implementation practices*
