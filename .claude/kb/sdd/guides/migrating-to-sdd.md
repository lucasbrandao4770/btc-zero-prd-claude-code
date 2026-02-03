# Migrating to SDD

> Transitioning from vibe coding to structured development

---

## Why Migrate?

### The Vibe Coding Experience

Sound familiar?

```text
Day 1:  "Claude, build me a user auth system"
Day 2:  "Now add password reset"
Day 3:  "Wait, that broke login"
Day 4:  "Start over, but better this time"
Day 5:  "What did we even build?"
```

**Symptoms**:
- Features drift from original intent
- No documentation to explain decisions
- Debugging is "detective work"
- Onboarding new people is painful
- Changes break unrelated features

### The SDD Experience

```text
Day 1:  /define "User authentication system"
        - Clear requirements captured
        - Acceptance tests defined

Day 2:  /design
        - Architecture documented
        - File manifest created

Day 3-4: /build
        - Code follows manifest
        - Verification at each step

Day 5:  /ship
        - Lessons learned documented
        - Ready for next feature
```

**Benefits**:
- Intent preserved in specifications
- Decisions documented with rationale
- Debugging traces to acceptance tests
- Onboarding = read the DEFINE
- Changes start with spec updates

---

## The Migration Path

### Stage 1: Document Current State

Before changing anything, capture where you are:

```markdown
# Current State Assessment

## Existing Features
| Feature | Documented? | Tests? | Clear Owner? |
|---------|-------------|--------|--------------|
| Auth | No | Partial | Unknown |
| Payments | README only | None | John |
| Reports | Comments | Yes | Maria |

## Technical Debt
- No clear architecture diagram
- Tests scattered and incomplete
- Comments outdated or missing

## Pain Points
- "What does this code do?"
- "Why was it built this way?"
- "Who do I ask about X?"
```

### Stage 2: Start New Features with SDD

**Don't rewrite everything.** Just start new features with SDD:

```bash
# New feature request comes in
/define "Add export to PDF functionality"

# Follow the full pipeline
/design → /build → /ship
```

### Stage 3: Document Critical Paths

For critical existing features, create retroactive documentation:

```markdown
# DEFINE: Authentication (Retroactive)

## Problem Statement
Users need secure login and session management.
(Originally built Jan 2024, documenting retroactively Feb 2026)

## Current Implementation
- JWT-based authentication
- 24-hour token expiry
- Email/password only

## Acceptance Tests (derived from existing behavior)
| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Valid login | User exists | Correct password | JWT returned |
| AT-002 | Invalid password | User exists | Wrong password | 401 error |
```

### Stage 4: Refactor with SDD

When refactoring becomes necessary:

```bash
# Don't just "fix it"
/define "Refactor authentication to support OAuth"

# Design the change
/design → /build → /ship
```

---

## The Mindset Shift

### From: "Just Code It"

```text
Request → Code → Hope it works → Fix bugs → Repeat
```

### To: "Specify First"

```text
Request → Specify → Design → Build with verification → Ship with lessons
```

### Key Mental Changes

| Old Thinking | New Thinking |
|--------------|--------------|
| "I know what to build" | "Let me document what to build" |
| "Code is documentation" | "Specification is documentation" |
| "Tests prove it works" | "Acceptance tests define done" |
| "Fix it if it breaks" | "Verify as we go" |
| "Move fast" | "Move with confidence" |

---

## Common Resistance (and Responses)

### "SDD is too slow"

**Reality**: SDD frontloads work that you'd do anyway:
- Clarifying requirements (otherwise: rework)
- Documenting decisions (otherwise: tribal knowledge)
- Defining tests (otherwise: bugs in production)

**The math**:
```text
Vibe Coding:    Build (2 days) + Fix (3 days) + Document (never) = 5+ days
SDD:            Define (2hrs) + Design (2hrs) + Build (1.5 days) + Ship (30min) = 2 days
```

### "We don't have time to document"

**Reality**: You don't have time NOT to document:
- Every "what does this do?" question = lost time
- Every "why was it built this way?" = archaeology expedition
- Every new team member = weeks of onboarding

**SDD makes documentation automatic**, not additional.

### "It won't work for our team"

**Reality**: SDD scales from solo to enterprise:
- Solo: Personal clarity and future-you documentation
- Small team: Shared understanding without meetings
- Enterprise: Audit trail and compliance

### "We're too far along to change"

**Reality**: You don't have to change everything:
1. Start new features with SDD
2. Document critical paths retroactively
3. Refactor with SDD when needed

---

## Practical Steps

### Week 1: Learn

- [ ] Read [concepts](../concepts/) folder
- [ ] Complete [getting-started.md](getting-started.md) tutorial
- [ ] Try SDD on a small personal project

### Week 2: Experiment

- [ ] Apply SDD to one new feature
- [ ] Follow the full pipeline (define → ship)
- [ ] Note friction points and benefits

### Week 3: Evaluate

- [ ] Compare effort: SDD feature vs. recent vibe-coded feature
- [ ] Compare quality: documentation, tests, clarity
- [ ] Decide: expand SDD or adjust approach

### Week 4+: Expand

- [ ] Apply SDD to all new features
- [ ] Start retroactive documentation for critical paths
- [ ] Iterate on process based on learnings

---

## Hybrid Approach

You don't have to go all-in immediately:

### Tier 1: Full SDD (Complex Features)

```text
Multi-day features
Multiple files affected
Team handoff needed
Production deployment
         ↓
Use full SDD pipeline
```

### Tier 2: Dev Loop (Medium Tasks)

```text
1-4 hour tasks
Single feature/utility
Personal projects
KB building
         ↓
Use Dev Loop with PROMPT.md
```

### Tier 3: Vibe Coding (Quick Fixes)

```text
<30 minute tasks
Obvious bug fixes
Trivial changes
Experiments
         ↓
Just prompt and verify
```

### Decision Guide

```text
Is it > 4 hours of work?
├── Yes → SDD
└── No
    └── Does it need documentation?
        ├── Yes → Dev Loop
        └── No
            └── Is it a quick fix?
                ├── Yes → Vibe Coding
                └── No → Dev Loop
```

---

## Retroactive Documentation Template

For existing features that need documentation:

```markdown
# DEFINE: {Feature Name} (Retroactive)

## Metadata
| Attribute | Value |
|-----------|-------|
| **Original Build** | {date} |
| **Documented** | {today} |
| **Status** | Retroactive documentation |

## Problem Statement (Reconstructed)
{Why was this feature built? What problem did it solve?}

## Current Implementation
{What does it actually do? How does it work?}

## Known Behaviors (from testing/usage)
| Scenario | Behavior |
|----------|----------|
| | |

## Technical Debt
| Issue | Impact | Effort to Fix |
|-------|--------|---------------|
| | | |

## Future Considerations
{What would we do differently if rebuilding?}
```

---

## Success Metrics

Track these to measure migration success:

| Metric | Before SDD | After SDD | Target |
|--------|-----------|-----------|--------|
| Time to onboard (new feature) | X days | ? | 50% reduction |
| Bugs in first week post-deploy | X bugs | ? | 75% reduction |
| "What does this do?" questions | X/week | ? | 90% reduction |
| Rework due to unclear requirements | X% | ? | 80% reduction |
| Time spent in post-mortems | X hours/month | ? | 50% reduction |

---

## Migration Checklist

### Individual

- [ ] Completed SDD tutorial
- [ ] Applied SDD to one feature
- [ ] Documented lessons learned
- [ ] Created personal SDD folder structure

### Team

- [ ] Team introduced to SDD concepts
- [ ] Pilot project completed with SDD
- [ ] Retrospective on pilot results
- [ ] Decision on broader adoption
- [ ] Templates customized for team

### Organization

- [ ] SDD integrated with existing tools
- [ ] Training materials created
- [ ] Success metrics defined
- [ ] Rollout plan established

---

## Resources

- **Getting started**: [getting-started.md](getting-started.md)
- **Advanced patterns**: [advanced-sdd.md](advanced-sdd.md)
- **Real example**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)
- **Quick reference**: [../quick-reference.md](../quick-reference.md)

---

*The best time to start SDD was yesterday. The second best time is now.*
