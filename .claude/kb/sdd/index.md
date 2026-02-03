# Spec-Driven Development (SDD) Knowledge Base

> Building software from specifications, not the other way around

---

## Overview

Spec-Driven Development (SDD) is a methodology that **inverts the traditional relationship between specifications and code**. Instead of specifications serving as guides for implementation, they become the primary artifact that *generates* implementation.

### The Power Inversion

| Traditional Development | Spec-Driven Development |
|------------------------|------------------------|
| Code is king | Specifications are king |
| Specs guide implementation | Specs **generate** implementation |
| Documentation gets stale | Specs are the source of truth |
| Change = manual propagation | Change = regeneration |
| Intent buried in code | Intent explicit in specs |

---

## Why SDD Matters

### The Problem SDD Solves

For decades, specifications were scaffolding—built and discarded once "real coding" began. This created a persistent gap between **intent** and **implementation**:

- Documentation drifts from reality
- Requirements get lost in translation
- Architecture decisions become tribal knowledge
- Pivots require manual, error-prone rewrites

### The SDD Solution

SDD eliminates this gap by making specifications **executable**:

1. **Define** what you want (WHAT + WHY)
2. **Design** how it should work (HOW)
3. **Generate** code from specifications
4. **Maintain** the spec, not just the code

---

## KB Structure

### Concepts (Theory)

| Document | Purpose |
|----------|---------|
| [what-is-sdd.md](concepts/what-is-sdd.md) | Core philosophy and principles |
| [specs-vs-code.md](concepts/specs-vs-code.md) | Why specification-first matters |
| [sdd-lifecycle.md](concepts/sdd-lifecycle.md) | The full SDD development cycle |
| [terminology.md](concepts/terminology.md) | Glossary of SDD terms |

### Patterns (How-To)

| Document | Purpose |
|----------|---------|
| [brainstorm-pattern.md](patterns/brainstorm-pattern.md) | Effective idea exploration |
| [define-pattern.md](patterns/define-pattern.md) | Writing precise specifications |
| [design-pattern.md](patterns/design-pattern.md) | Architecture from specifications |
| [build-pattern.md](patterns/build-pattern.md) | Implementation with verification |
| [ship-pattern.md](patterns/ship-pattern.md) | Completion, archival, lessons learned |

### Implementations (Reference)

| Document | Purpose |
|----------|---------|
| [spec-kit.md](implementations/spec-kit.md) | GitHub's Spec-Kit deep dive |
| [agentspec.md](implementations/agentspec.md) | AgentSpec (Jarvis/Claude Code) analysis |
| [comparison.md](implementations/comparison.md) | Side-by-side feature comparison |

### Guides (Practical)

| Document | Purpose |
|----------|---------|
| [getting-started.md](guides/getting-started.md) | SDD for beginners |
| [migrating-to-sdd.md](guides/migrating-to-sdd.md) | From vibe coding to SDD |
| [advanced-sdd.md](guides/advanced-sdd.md) | Complex project patterns |

### Examples (Real-World)

| Document | Purpose |
|----------|---------|
| [invoice-pipeline.md](examples/invoice-pipeline.md) | UberEats pipeline walkthrough |
| [feature-examples.md](examples/feature-examples.md) | Additional SDD feature examples |

---

## Quick Navigation

### By Experience Level

| Level | Start Here |
|-------|-----------|
| **New to SDD** | [what-is-sdd.md](concepts/what-is-sdd.md) → [getting-started.md](guides/getting-started.md) |
| **Transitioning** | [migrating-to-sdd.md](guides/migrating-to-sdd.md) → [define-pattern.md](patterns/define-pattern.md) |
| **Implementing** | [comparison.md](implementations/comparison.md) → [agentspec.md](implementations/agentspec.md) |
| **Advanced** | [advanced-sdd.md](guides/advanced-sdd.md) → [invoice-pipeline.md](examples/invoice-pipeline.md) |

### By Task

| Task | Documents |
|------|-----------|
| Understand SDD philosophy | [what-is-sdd.md](concepts/what-is-sdd.md), [specs-vs-code.md](concepts/specs-vs-code.md) |
| Choose an implementation | [spec-kit.md](implementations/spec-kit.md), [agentspec.md](implementations/agentspec.md), [comparison.md](implementations/comparison.md) |
| Write specifications | [define-pattern.md](patterns/define-pattern.md), [brainstorm-pattern.md](patterns/brainstorm-pattern.md) |
| Design architecture | [design-pattern.md](patterns/design-pattern.md), [build-pattern.md](patterns/build-pattern.md) |
| See real examples | [invoice-pipeline.md](examples/invoice-pipeline.md), [feature-examples.md](examples/feature-examples.md) |

---

## Key Concepts at a Glance

### The 3-Level Development Spectrum

```text
LEVEL 1: Vibe Coding          LEVEL 2: Dev Loop           LEVEL 3: Spec-Driven Dev
───────────────────          ──────────────────          ──────────────────────

• Just prompts               • PROMPT.md driven          • 5-phase pipeline
• No structure               • Verification loops        • Full traceability
• Hope it works              • Agent leverage            • Quality gates
• Quick fixes                • Memory bridge             • Enterprise audit
                             • Question-first            • ADRs and specs

Time: < 30 min               Time: 1-4 hours             Time: Multi-day
```

### The SDD Phases

```text
Phase 0        Phase 1        Phase 2        Phase 3        Phase 4
BRAINSTORM  →  DEFINE      →  DESIGN      →  BUILD       →  SHIP
(Explore)      (What+Why)     (How)          (Execute)      (Archive)
[Optional]     [Required]     [Required]     [Required]     [Required]
```

### Core Principles

1. **Specifications as Source of Truth** - The spec generates code, not guides it
2. **Executable Documentation** - Specifications must be precise enough to generate working systems
3. **Continuous Refinement** - Quality validation happens throughout, not just at gates
4. **Research-Driven Context** - Technical decisions backed by investigation
5. **Bidirectional Feedback** - Production reality informs specification evolution

---

## Related Resources

### Internal

- **KB: frameworks** - Spec-Kit brief overview (for framework comparison)
- **SDD folder** - `.claude/sdd/` (AgentSpec implementation)
- **Jarvis Planner Mode** - `modes/jarvis-planner-mode.md` (SDD alignment)

### External

- **Spec-Kit GitHub** - https://github.com/github/spec-kit
- **SDD Philosophy** - `/spec-driven.md` in Spec-Kit repo
- **Video Overview** - https://www.youtube.com/watch?v=a9eR1xsfvHg

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-02 | Initial KB creation |

---

*For quick reference, see [quick-reference.md](quick-reference.md)*
