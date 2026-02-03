# Define Pattern

> Writing precise, measurable specifications (WHAT and WHY)

---

## Purpose

The Define phase captures **what** you're building and **why** it matters—without diving into implementation details. It produces a specification precise enough to:

1. Validate understanding with stakeholders
2. Guide architectural decisions in Design
3. Generate acceptance tests
4. Measure success objectively

---

## The Golden Rules

### 1. Focus on WHAT, Not HOW

| ✅ WHAT (Define) | ❌ HOW (Design) |
|-----------------|-----------------|
| "Users can search products" | "Use Elasticsearch with fuzzy matching" |
| "System handles 1000 concurrent users" | "Deploy on Kubernetes with HPA" |
| "Data persists between sessions" | "Store in PostgreSQL with UUID keys" |

### 2. Make Everything Measurable

| ❌ Vague | ✅ Measurable |
|---------|--------------|
| "System should be fast" | "P95 latency < 100ms" |
| "Handle errors gracefully" | "Retry 3x with exponential backoff; log after final failure" |
| "Good user experience" | "Task completion rate > 90% for first-time users" |

### 3. Mark Uncertainty Explicitly

Never guess. Mark ambiguities clearly:

```markdown
- System MUST authenticate users via
  [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
```

---

## The Pattern

### Step 1: Problem Statement

Clear, specific, with business impact:

```markdown
## Problem Statement

The Finance team spends **80% of their time** on manual data entry
from delivery platform invoices, causing **R$45,000+ in reconciliation
errors** quarterly. This manual process:

- Is error-prone (15% error rate on complex invoices)
- Cannot scale with growing volume (2,000+/month, projected to 3,500)
- Creates compliance risk (delayed reconciliation)
```

**Formula**: Who + What problem + Quantified impact

### Step 2: Target Users

Define personas with specific pain points:

```markdown
## Target Users

| User | Role | Pain Point |
|------|------|------------|
| Finance Team | Invoice processing | 80% time on manual entry; high error rate |
| Operations | Partner management | R$45K quarterly losses from errors |
| Data Engineering | Pipeline maintenance | No automated extraction exists |
```

### Step 3: Goals with MoSCoW

Prioritize explicitly:

```markdown
## Goals

| Priority | Goal |
|----------|------|
| **MUST** | Extract invoice data with ≥90% accuracy |
| **MUST** | Process invoices in <30 seconds (P95) |
| **MUST** | Support all 5 vendors: UberEats, DoorDash, Grubhub, iFood, Rappi |
| **SHOULD** | Achieve pipeline availability >99% |
| **SHOULD** | Keep cost per invoice <$0.01 |
| **COULD** | Archive originals for compliance (7-year retention) |
| **WON'T** | Support PDF format (TIFF only for MVP) |
```

### Step 4: Success Criteria

Measurable outcomes with specific metrics:

```markdown
## Success Criteria

| ID | Criterion | Target | Measurement Method |
|----|-----------|--------|-------------------|
| SC-001 | Extraction accuracy | ≥90% per field | Compare to ground truth dataset |
| SC-002 | Processing latency | P95 < 30s | Cloud Monitoring percentile |
| SC-003 | Vendor coverage | 5/5 vendors | Test with sample from each |
| SC-004 | Pipeline uptime | >99% | Uptime monitoring |
| SC-005 | Cost per invoice | <$0.01 | Cloud billing analysis |
```

### Step 5: Acceptance Tests

Given/When/Then for all scenarios:

```markdown
## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Happy path | Valid UberEats TIFF in input bucket | File triggers pipeline | Data in BigQuery within 30s |
| AT-002 | Multi-page | 2-page invoice TIFF | Pipeline processes | Both pages extracted correctly |
| AT-003 | All vendors | One invoice per vendor | Process all 5 | All extracted correctly |
| AT-004 | Invalid file | Corrupted TIFF | Pipeline attempts | Moved to failed bucket, error logged |
| AT-005 | Duplicate | Same invoice twice | Second submission | Deduplication prevents duplicate |
```

### Step 6: Out of Scope

Explicit boundaries prevent scope creep:

```markdown
## Out of Scope

Explicitly NOT included in this feature:

- **PDF support** - TIFF only for MVP
- **Real-time dashboard** - BigQuery queries available, no custom UI
- **Email notifications** - Manual monitoring for MVP
- **Handwritten invoices** - Focus on printed/digital only
- **Production deployment** - Dev environment until validation complete
```

### Step 7: Constraints and Assumptions

```markdown
## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| **Cloud** | GCP only | No multi-cloud portability |
| **Timeline** | April 1 deadline | MVP must ship before Q2 |
| **Budget** | ~$55/month | Cost per invoice must stay <$0.01 |

## Assumptions

| ID | Assumption | If Wrong, Impact |
|----|------------|------------------|
| A-001 | Gemini achieves ≥90% accuracy | Need fallback LLM |
| A-002 | Volume stays under 3,500/month | Need autoscaling review |
| A-003 | All invoices are 1-2 pages | Need batch handling |
```

---

## Clarity Score

Calculate before proceeding to Design:

| Element | Score (0-3) | Criteria |
|---------|-------------|----------|
| **Problem** | | Clear, specific, quantified impact |
| **Users** | | Defined personas with pain points |
| **Goals** | | Measurable with MoSCoW prioritization |
| **Success** | | Testable criteria with specific metrics |
| **Scope** | | Explicit out-of-scope items |
| **Total** | **/15** | Minimum 12/15 to proceed |

### Scoring Guide

| Score | Meaning |
|-------|---------|
| 0 | Missing or completely vague |
| 1 | Present but incomplete |
| 2 | Adequate but could be clearer |
| 3 | Clear, specific, actionable |

---

## Output Template

```markdown
# DEFINE: {Feature Name}

> {One-line description}

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {date} |
| **Author** | define-agent |
| **Status** | ⏳ In Progress / ✅ Ready for Design |
| **Clarity Score** | {X}/15 |
| **Source** | {BRAINSTORM doc or raw input} |

---

## Problem Statement

{Who + What problem + Quantified impact}

---

## Target Users

| User | Role | Pain Point |
|------|------|------------|
| | | |

---

## Goals

| Priority | Goal |
|----------|------|
| **MUST** | |
| **SHOULD** | |
| **COULD** | |

---

## Success Criteria

| ID | Criterion | Target | Measurement |
|----|-----------|--------|-------------|
| SC-001 | | | |

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | | | | |

---

## Out of Scope

- **{Item}** - {Reason}

---

## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| | | |

---

## Assumptions

| ID | Assumption | If Wrong |
|----|------------|----------|
| | | |

---

## Open Questions

- [NEEDS CLARIFICATION: {question}]

---

## Next Step

`/design .claude/sdd/features/DEFINE_{FEATURE}.md`
```

---

## Common Pitfalls

### 1. Including Implementation Details

❌ **Wrong**:
```markdown
## Goals
- Use Redis for caching
- Deploy on Kubernetes
- Store data in PostgreSQL
```

✅ **Right**:
```markdown
## Goals
- Reduce API latency to <100ms (P95)
- Support 10,000 concurrent users
- Persist data with 99.99% durability
```

### 2. Unmeasurable Criteria

❌ **Wrong**:
```markdown
## Success Criteria
- System is fast
- Users are satisfied
- Code is clean
```

✅ **Right**:
```markdown
## Success Criteria
- P95 latency < 100ms
- NPS score > 40
- 0 critical SonarQube issues
```

### 3. Missing Out of Scope

❌ **Wrong**:
```markdown
## Out of Scope
(not mentioned)
```

✅ **Right**:
```markdown
## Out of Scope
- **Mobile app** - Web only for MVP
- **Offline mode** - Requires network connection
- **Multi-language** - English only initially
```

### 4. Guessing Instead of Marking

❌ **Wrong**:
```markdown
- System authenticates users with OAuth 2.0
  (assuming OAuth since it's common)
```

✅ **Right**:
```markdown
- System authenticates users via
  [NEEDS CLARIFICATION: auth method not specified]
```

---

## Example: Complete DEFINE Document

See the Invoice Pipeline example:
- [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)
- `.claude/sdd/archive/INVOICE_PIPELINE/DEFINE_INVOICE_PIPELINE.md`

---

## Integration with Spec-Kit

Spec-Kit uses `/speckit.specify` for this phase:

```bash
/speckit.specify Build an application that helps organize photos
in albums, grouped by date with drag-and-drop reordering
```

The template structure is similar but emphasizes:
- User Stories with independent testability
- Functional Requirements (FR-001, FR-002, etc.)
- Review checklist for self-validation

---

## Next Steps

- **After Define**: [design-pattern.md](design-pattern.md)
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Example walkthrough**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)

---

*References: AgentSpec 4.2 Phase 1, Spec-Kit spec-template.md*
