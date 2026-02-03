# SDD Quick Reference

> Cheat sheet for Spec-Driven Development

---

## Commands at a Glance

### AgentSpec (Claude Code)

| Command | Phase | Purpose |
|---------|-------|---------|
| `/brainstorm` | 0 | Explore ideas (optional) |
| `/define` | 1 | Capture requirements (WHAT) |
| `/design` | 2 | Create architecture (HOW) |
| `/build` | 3 | Implement with verification |
| `/ship` | 4 | Archive with lessons |
| `/iterate` | Any | Update documents |

### Spec-Kit (GitHub)

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Create governing principles |
| `/speckit.specify` | Define requirements |
| `/speckit.clarify` | Clarify ambiguities |
| `/speckit.plan` | Create technical plan |
| `/speckit.tasks` | Generate task list |
| `/speckit.implement` | Execute implementation |

---

## Workflow

```text
/brainstorm ──▶ /define ──▶ /design ──▶ /build ──▶ /ship
 (optional)      (WHAT)      (HOW)     (EXECUTE)  (ARCHIVE)
```

---

## Phase Checklists

### Define Checklist

- [ ] Problem statement has numbers
- [ ] Users defined with pain points
- [ ] Goals use MoSCoW (MUST/SHOULD/COULD)
- [ ] Success criteria are measurable
- [ ] Acceptance tests use Given/When/Then
- [ ] Out of scope is explicit
- [ ] **Clarity Score ≥ 12/15**

### Design Checklist

- [ ] Architecture diagram present
- [ ] Decisions have rationale
- [ ] File manifest is complete
- [ ] Dependencies are clear
- [ ] Code patterns are copy-paste ready
- [ ] Testing strategy defined

### Build Checklist

- [ ] Following manifest order
- [ ] Verify each component before moving on
- [ ] Log deviations from Design
- [ ] All tests passing
- [ ] BUILD_REPORT complete

### Ship Checklist

- [ ] All quality gates passed
- [ ] Artifacts moved to archive
- [ ] Lessons learned documented
- [ ] Project docs updated

---

## Clarity Score

| Element | Max Points | Criteria |
|---------|------------|----------|
| Problem | 3 | Specific, with numbers |
| Users | 3 | Personas with pain points |
| Goals | 3 | Measurable, prioritized |
| Success | 3 | Testable metrics |
| Scope | 3 | Explicit out-of-scope |
| **Total** | **15** | **≥12 to proceed** |

---

## MoSCoW Prioritization

| Priority | Meaning |
|----------|---------|
| **MUST** | Non-negotiable requirement |
| **SHOULD** | Important but not critical |
| **COULD** | Nice to have |
| **WON'T** | Explicitly out of scope |

---

## Acceptance Test Format

```text
Given [initial state]
When [action]
Then [expected outcome]
```

**Example**:
```text
Given a valid UberEats TIFF invoice
When the pipeline processes the file
Then extracted data appears in BigQuery within 30 seconds
```

---

## Inline ADR Format

```markdown
### Decision: {Title}

**Context**: {Why this decision is needed}

**Options**:
| Option | Pros | Cons |
|--------|------|------|

**Decision**: {Selected option}

**Rationale**: {Why this option}

**Consequences**: {Impact of choice}
```

---

## Model Assignment (AgentSpec)

| Phase | Model |
|-------|-------|
| Brainstorm | Opus |
| Define | Opus |
| Design | Opus |
| Build | Sonnet |
| Ship | Haiku |
| Iterate | Sonnet |

---

## Folder Structure

### AgentSpec

```text
.claude/sdd/
├── features/         # Active work
│   ├── BRAINSTORM_*.md
│   ├── DEFINE_*.md
│   └── DESIGN_*.md
├── reports/          # Build reports
│   └── BUILD_REPORT_*.md
├── archive/          # Shipped features
│   └── {FEATURE}/
├── templates/        # Document templates
└── examples/         # Reference examples
```

### Spec-Kit

```text
.specify/
├── memory/           # Constitution
├── specs/            # Feature specs
│   └── {feature}/
├── scripts/          # Helper scripts
└── templates/        # Document templates
```

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Vague idea | `/brainstorm` |
| Clear requirements | `/define` (skip brainstorm) |
| Quick fix (<30 min) | Vibe coding |
| Medium task (1-4 hrs) | Dev Loop |
| Complex feature (days) | Full SDD |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to code | Start with `/define` |
| Vague requirements | Add numbers and metrics |
| "Make it fast" | "P95 latency < 100ms" |
| No out-of-scope | List what you're NOT building |
| Incomplete manifest | List EVERY file |
| Skipping verification | Test each component |
| No lessons learned | Always document in Ship |

---

## Quality Tiers

| Tier | Time | Use When |
|------|------|----------|
| Vibe | <30 min | Quick fixes, experiments |
| Dev Loop | 1-4 hrs | Single features, utilities |
| SDD | Days | Production features |

---

## Key Artifacts

| Artifact | Purpose |
|----------|---------|
| `BRAINSTORM_*.md` | Exploration notes |
| `DEFINE_*.md` | Requirements (WHAT) |
| `DESIGN_*.md` | Architecture (HOW) |
| `BUILD_REPORT_*.md` | Implementation record |
| `SHIPPED_*.md` | Lessons learned |

---

## Useful Patterns

### Verification Loop

```text
Create → Test → Verify → Log → Next
```

### Iteration Trigger

```text
Requirement changed? → /iterate DEFINE
Design flawed? → /iterate DESIGN
```

### Handoff

```text
From: Dev A (phase complete)
To: Dev B (next phase)
Artifacts: [list]
Open Questions: [none/list]
```

---

## Resources

| Resource | Location |
|----------|----------|
| Full concepts | `.claude/kb/sdd/concepts/` |
| Patterns | `.claude/kb/sdd/patterns/` |
| Examples | `.claude/kb/sdd/examples/` |
| Templates | `.claude/sdd/templates/` |
| Archive | `.claude/sdd/archive/` |

---

## Emergency Reference

### "I don't know where to start"

```bash
/define "What you want to build"
```

### "Requirements changed mid-build"

```bash
/iterate DEFINE_FEATURE.md "New requirement"
/iterate DESIGN_FEATURE.md "Design change needed"
```

### "Build failed verification"

1. Check error message
2. Fix and retry (max 3 times)
3. If blocked, document and escalate

### "Ready to ship but tests fail"

**Don't ship.** Fix tests first. SDD requires all gates pass.

---

*Print this page. Keep it handy. Master SDD.*
