# Specifications vs. Code: Why Spec-First Matters

> The case for treating specifications as the source of truth

---

## The Traditional Problem

In traditional development, code becomes the de facto source of truth:

```text
Day 1:    PRD ──────────────────────────────▶ Implementation
                                              (aligned)

Day 30:   PRD (stale) ························ Implementation
                      ↑                        (evolved)
                      │
                      └── "We should update the docs someday..."

Day 90:   PRD (fiction) ······················ Implementation
                                               (tribal knowledge)
```

### Symptoms of Code-First Development

| Symptom | Root Cause |
|---------|-----------|
| "What does this code do?" | Intent buried in implementation |
| "Why was it built this way?" | Architecture decisions lost |
| Onboarding takes weeks | Context lives in developers' heads |
| Refactoring is risky | No clear contract to verify against |
| Bug fixes break features | Unknown dependencies |
| Requirements drift | No single source of truth |

---

## The Spec-First Alternative

SDD inverts the relationship:

```text
Day 1:    Specification ──▶ Generated Implementation
                            (aligned by design)

Day 30:   Updated Specification ──▶ Regenerated Implementation
                                    (still aligned)

Day 90:   Evolved Specification ──▶ Current Implementation
                                    (always aligned)
```

### Benefits of Spec-First

| Benefit | How It Works |
|---------|--------------|
| Clear intent | Specifications capture WHAT and WHY |
| Traceable decisions | ADRs and rationale in specs |
| Fast onboarding | Read the spec, understand the system |
| Safe refactoring | Spec defines the contract |
| Confident changes | Regenerate from updated spec |
| Living documentation | Spec IS the documentation |

---

## The Gap Problem

The traditional gap between specification and implementation:

```text
┌─────────────────────────────────────────────────────────────────┐
│                     THE SPECIFICATION GAP                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Requirements  ─────┐                                           │
│                      │                                           │
│   Design Docs   ─────┼────────── GAP ──────────▶ Implementation │
│                      │            ↑                              │
│   Architecture  ─────┘            │                              │
│                                   │                              │
│                          • Translation errors                    │
│                          • Misinterpretation                    │
│                          • Lost context                          │
│                          • Drift over time                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why the Gap Exists

1. **Manual Translation**: Humans convert specs to code, introducing interpretation
2. **Incomplete Specs**: Ambiguity forces developers to make assumptions
3. **Time Pressure**: "Just make it work" overrides "match the spec"
4. **Feedback Delay**: Implementation issues discovered too late
5. **Evolution**: Code changes without spec updates

### SDD Eliminates the Gap

```text
┌─────────────────────────────────────────────────────────────────┐
│                     SDD: NO GAP                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Specification ════════════════════════════▶ Implementation    │
│         │                                           │            │
│         │    (Automated generation)                 │            │
│         │                                           │            │
│         └──────────── Feedback loop ────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Changes with Spec-First

### Development Activities

| Activity | Code-First | Spec-First |
|----------|------------|------------|
| **Starting work** | Read code | Read specification |
| **Making changes** | Edit code | Edit specification |
| **Code review** | "Does this code work?" | "Does this match the spec?" |
| **Debugging** | Trace through code | Check spec alignment |
| **Documentation** | After the fact (if ever) | The spec IS documentation |
| **Handoff** | Explain the code | Share the specification |

### Quality Assurance

| Quality Aspect | Code-First | Spec-First |
|----------------|------------|------------|
| **Completeness** | Test coverage % | Spec validation score |
| **Correctness** | Unit tests pass | Acceptance tests pass |
| **Consistency** | Code review | Spec consistency check |
| **Intent** | Comments (maybe) | Explicit in specification |

### Team Collaboration

| Collaboration | Code-First | Spec-First |
|---------------|------------|------------|
| **Alignment** | Through meetings | Through shared specs |
| **Review** | Pull request | Spec review + generated PR |
| **Conflict resolution** | Merge conflicts | Spec discussion |
| **Knowledge transfer** | Pair programming | Spec walkthrough |

---

## The Economics of Spec-First

### Cost of Changes

```text
TRADITIONAL: Cost increases exponentially with time

     │                                    ╱
Cost │                              ╱ ╱
     │                        ╱ ╱
     │                  ╱ ╱
     │            ╱ ╱
     │      ╱ ╱
     │  ╱
     └──────────────────────────────────────▶
        Req  Design  Build  Test  Prod  Maint


SDD: Cost remains relatively flat

     │
Cost │  ─────────────────────────────────
     │
     └──────────────────────────────────────▶
        Spec  Generate  Validate  Deploy
```

### Why Spec-First Costs Less

1. **Early Error Detection**: Spec validation catches issues before generation
2. **Automated Propagation**: Changes flow from spec to all affected code
3. **Reduced Rework**: No manual synchronization between docs and code
4. **Faster Iteration**: Regenerate instead of manually refactor

---

## Making Specifications Executable

The key to spec-first is making specifications **precise enough to generate code**:

### Specification Quality Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Vague** | Open to interpretation | "Handle user authentication" |
| **Descriptive** | Clear but not actionable | "Users log in with email and password" |
| **Precise** | Implementation-ready | "FR-001: System MUST validate email format per RFC 5322; password MUST be 12+ chars with uppercase, lowercase, number, and special character" |
| **Executable** | Generates working code | Precise spec + acceptance scenarios + test cases |

### What Makes a Spec Executable

1. **Measurable Success Criteria**
   - ❌ "System should be fast"
   - ✅ "P95 latency < 30ms for read operations"

2. **Complete Acceptance Tests**
   - Given/When/Then scenarios for all paths
   - Edge cases explicitly documented

3. **Technical Context**
   - Deployment environment constraints
   - Integration points defined
   - Data models specified

4. **Explicit Ambiguity Markers**
   - `[NEEDS CLARIFICATION]` for uncertain areas
   - No guessing or assumptions

---

## Common Objections (and Responses)

### "Writing specs takes too long"

**Response**: Writing precise specs takes less time than:
- Debugging misunderstood requirements
- Refactoring code that doesn't meet needs
- Explaining intent to new team members
- Maintaining stale documentation

### "Our requirements change too fast"

**Response**: That's exactly why spec-first helps:
- Change the spec, regenerate implementation
- No manual propagation through codebase
- Automatic consistency

### "We can't spec everything upfront"

**Response**: SDD is iterative, not waterfall:
- Start with what you know
- Mark uncertainties explicitly
- Refine as you learn
- Regenerate continuously

### "Developers want to code, not write docs"

**Response**: Specifications in SDD are different:
- They're the primary creative work
- They directly produce results
- They're living, not archival

---

## Spec-First in Practice

### The Workflow

```text
1. SPECIFY (What + Why)
   │
   ▼
2. VALIDATE (Quality check)
   │
   ▼
3. DESIGN (How)
   │
   ▼
4. GENERATE (Code)
   │
   ▼
5. VERIFY (Tests pass)
   │
   ▼
6. DEPLOY
   │
   └──▶ Feedback ──▶ Back to SPECIFY
```

### Time Investment Comparison

| Phase | Code-First | Spec-First |
|-------|-----------|------------|
| Planning | 10% | 30% |
| Implementation | 50% | 20% |
| Testing | 20% | 20% |
| Debugging | 15% | 10% |
| Documentation | 5% | 0% (built in) |
| **Rework** | **+30%** | **+10%** |

---

## Key Takeaway

> **The question isn't "specs vs. code"—it's "where does truth live?" In SDD, truth lives in specifications, and code is just one of many possible expressions of that truth.**

---

## Next Steps

- **Learn the full lifecycle**: [sdd-lifecycle.md](sdd-lifecycle.md)
- **See how to write specs**: [../patterns/define-pattern.md](../patterns/define-pattern.md)
- **Understand terminology**: [terminology.md](terminology.md)

---

*References: Spec-Kit spec-driven.md, AgentSpec workflow documentation*
