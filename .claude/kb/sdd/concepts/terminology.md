# SDD Terminology Glossary

> Definitions for Spec-Driven Development concepts and terms

---

## Core Concepts

### Spec-Driven Development (SDD)

A software development methodology where **specifications generate implementation** rather than merely guiding it. The specification is the source of truth; code is its expression.

### Executable Specification

A specification precise, complete, and unambiguous enough to **generate working code**. Not just documentation—a specification that produces implementation.

### Intent-Driven Development

Development where intent is expressed in natural language as specifications, with code as the "last-mile" translation. The *lingua franca* of development moves to a higher abstraction level.

### Power Inversion

The fundamental shift in SDD where **specifications don't serve code—code serves specifications**. Inverting the traditional relationship between documentation and implementation.

---

## Phases

### Phase 0: Brainstorm (Optional)

Exploratory dialogue phase to clarify vague ideas before capturing formal requirements. Uses questioning techniques to identify scope, approaches, and apply YAGNI.

**Output**: BRAINSTORM_{FEATURE}.md

### Phase 1: Define

The phase where **WHAT and WHY** are captured. Produces structured requirements with user stories, acceptance criteria, success metrics, and explicit scope boundaries.

**Output**: DEFINE_{FEATURE}.md

### Phase 2: Design

The phase where **HOW** is determined. Creates technical architecture, file manifests, inline decisions, and code patterns that guide implementation.

**Output**: DESIGN_{FEATURE}.md

### Phase 3: Build

The execution phase where code is **generated following the Design**. Includes verification loops, test creation, and progress tracking.

**Output**: Code, Tests, BUILD_REPORT_{FEATURE}.md

### Phase 4: Ship

The archival phase where completed features are **documented with lessons learned** and moved to the archive for future reference.

**Output**: archive/{FEATURE}/, SHIPPED_{DATE}.md

---

## Quality Metrics

### Clarity Score

A 15-point scoring system used in the Define phase to measure specification quality:

| Element | Points | Criteria |
|---------|--------|----------|
| Problem | 0-3 | Specificity and business impact |
| Users | 0-3 | Defined personas and pain points |
| Goals | 0-3 | Measurability and prioritization |
| Success | 0-3 | Testable criteria with metrics |
| Scope | 0-3 | Explicit out-of-scope items |

**Minimum for Design**: 12/15

### Quality Gate

A checkpoint between phases that must be passed before proceeding. Each phase has specific gate criteria that ensure specification quality.

### Acceptance Test

A formal test scenario using Given/When/Then format that defines expected system behavior:

```
Given [initial state]
When [action]
Then [expected outcome]
```

---

## Artifacts

### Feature Artifact

Any document produced during the SDD lifecycle (BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT, SHIPPED).

### File Manifest

A complete list in the Design document of all files to be created or modified, including dependencies and implementation order.

### Inline ADR (Architecture Decision Record)

Architecture decisions documented directly within the Design document (not as separate files) with context, options, decision, and consequences.

### Constitution

A set of immutable principles governing development decisions. Used in Spec-Kit to enforce architectural discipline across all specifications.

---

## Workflow Terms

### Iteration (/iterate)

The process of updating any phase document mid-stream when requirements change, new information emerges, or refinement is needed.

### Memory Bridge

A mechanism (used in Dev Loop) for preserving progress and context across interrupted sessions, enabling recovery and continuation.

### Agent Matching

The process of assigning specialized AI agents to different phases based on their strengths (e.g., Opus for creative phases, Sonnet for execution).

### Agent Delegation

Invoking specialized agents (like @kb-architect or @test-generator) during the Build phase to handle specific tasks.

---

## Validation Terms

### [NEEDS CLARIFICATION]

A marker in specifications indicating uncertain or ambiguous areas that require user input before proceeding.

### YAGNI (You Aren't Gonna Need It)

Principle applied especially in Brainstorm to ruthlessly remove speculative or "might need" features that aren't explicitly required.

### MoSCoW Prioritization

Prioritization scheme used in Define:
- **MUST**: Non-negotiable requirements
- **SHOULD**: Important but not critical
- **COULD**: Nice to have
- **WON'T**: Explicitly out of scope

---

## Implementation Terms

### Spec-Kit

GitHub's official SDD toolkit providing commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) and templates for structured development.

### AgentSpec

An adaptation of SDD for Claude Code workflows, featuring 5 phases with slash commands (`/brainstorm`, `/define`, `/design`, `/build`, `/ship`).

### Dev Loop

A "Level 2" development methodology using PROMPT.md files with structured iteration, verification loops, and session recovery. Less formal than full SDD.

### Vibe Coding

"Level 1" ad-hoc development through direct prompts without structure. Suitable for quick fixes (<30 min) but not complex features.

---

## Pattern Terms

### Template-Driven Quality

Using structured templates to constrain AI output, ensuring consistent, high-quality specifications that follow established patterns.

### Continuous Refinement

Quality validation as an ongoing process rather than discrete gates, with AI analyzing specifications for ambiguity, contradictions, and gaps continuously.

### Bidirectional Feedback

Production metrics and incidents informing specification evolution, creating a loop from deployment back to specification refinement.

---

## Development Spectrum

### Level 1: Vibe Coding

- Unstructured prompts
- No documentation
- Quick fixes (<30 min)
- Hope-based verification

### Level 2: Dev Loop (Agentic Development)

- PROMPT.md driven
- Verification loops
- Agent leverage
- Memory bridge for recovery
- 1-4 hour tasks

### Level 3: Spec-Driven Development

- 5-phase pipeline
- Full traceability
- Quality gates
- Enterprise audit capability
- Multi-day features

---

## Spec-Kit Specific Terms

### /speckit.constitution

Command to create project governing principles that guide all subsequent development decisions.

### /speckit.specify

Command to create feature specifications from descriptions, focusing on WHAT and WHY.

### /speckit.plan

Command to create technical implementation plans with technology choices and architecture.

### /speckit.tasks

Command to generate actionable task lists from implementation plans with dependency ordering.

### /speckit.implement

Command to execute all tasks and build the feature according to the plan.

### /speckit.clarify

Command to systematically clarify underspecified areas before planning (optional but recommended).

### /speckit.analyze

Command to perform cross-artifact consistency and coverage analysis.

---

## AgentSpec Specific Terms

### /brainstorm

Command to explore ideas through collaborative dialogue (Phase 0, optional).

### /define

Command to capture and validate requirements (Phase 1).

### /design

Command to create technical architecture and specification (Phase 2).

### /build

Command to execute implementation with verification (Phase 3).

### /ship

Command to archive completed features with lessons learned (Phase 4).

---

## Related Terms

### PRD (Product Requirements Document)

Traditional document capturing product requirements. In SDD, this becomes the DEFINE artifact.

### ADR (Architecture Decision Record)

Document capturing important architecture decisions. In SDD, these are inline within DESIGN documents.

### TDD (Test-Driven Development)

Methodology where tests are written before code. SDD incorporates TDD principles with acceptance tests from specifications.

### Greenfield Development

Building new systems from scratch. SDD's "0-to-1" development phase.

### Brownfield Development

Enhancing or modernizing existing systems. SDD's "Iterative Enhancement" phase.

---

## Quick Reference Table

| Term | Definition | Phase |
|------|------------|-------|
| BRAINSTORM | Exploratory dialogue | Phase 0 |
| DEFINE | Requirements capture | Phase 1 |
| DESIGN | Technical architecture | Phase 2 |
| BUILD | Implementation | Phase 3 |
| SHIP | Archival | Phase 4 |
| Clarity Score | Specification quality metric | Phase 1 |
| File Manifest | List of files to create | Phase 2 |
| Inline ADR | Embedded architecture decision | Phase 2 |
| Acceptance Test | Given/When/Then scenario | Phase 1 |
| Quality Gate | Phase transition checkpoint | All |
| /iterate | Mid-stream update command | Any |

---

*References: Spec-Kit documentation, AgentSpec 4.2, Dev Loop specification*
