# AgentSpec - Framework Analysis

> Deep dive into AgentSpec: a 5-phase Spec-Driven Development workflow with agent orchestration

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | Internal (this repository: btc-zero-prd-claude-code) |
| **Author** | Custom development for Claude Code workflows |
| **Category** | Agentic Development / Spec-Driven Development |
| **Version** | 4.2.0 |
| **Last Updated** | 2026-02-03 |

### One-Line Summary

AgentSpec is a 5-phase structured development workflow (Brainstorm, Define, Design, Build, Ship) that transforms vague ideas into shipped features through collaborative dialogue, artifact-driven handoffs, and specialized agent delegation.

---

## Problem Statement

### What Problem Does It Solve?

AI-assisted development often suffers from:

1. **Context loss** - Large features overwhelm context windows, causing hallucinations and forgotten requirements
2. **Scope creep** - Without structured phases, features expand beyond original intent
3. **Quality inconsistency** - Ad-hoc coding produces varying quality across files
4. **Traceability gaps** - No audit trail from requirement to implementation
5. **Knowledge silos** - Decisions and lessons learned disappear after shipping

AgentSpec addresses these by enforcing phase gates, producing persistent artifacts, and delegating to specialized agents.

### Who Is It For?

| User | Use Case |
|------|----------|
| Solo developers | Structured feature development with AI assistance |
| AI-first teams | Consistent workflow for Claude Code projects |
| Complex projects | Multi-component features requiring traceability |
| Production systems | Audit trail and quality gates for enterprise needs |

### Why Does This Matter?

- **45-file features shipped in 2 days** - The INVOICE_PIPELINE feature created 45 files, ~2,500 lines of code, with 69 tests in just 2 days using AgentSpec phases
- **Eliminates "vibe coding"** - Provides structure between "just prompting" and heavyweight enterprise processes
- **Preserves context** - Artifacts persist across sessions, preventing re-exploration

---

## Architecture

### Core Concepts

1. **5-Phase Pipeline** - Sequential phases with quality gates: Brainstorm (optional) -> Define -> Design -> Build -> Ship
2. **Artifact-Driven Handoffs** - Each phase produces a Markdown document that feeds the next phase
3. **Agent Delegation** - Build phase invokes specialized agents (@function-developer, @extraction-specialist, etc.) based on file purpose
4. **Inline Decisions** - Architecture Decision Records (ADRs) embedded in DESIGN documents, not separate files
5. **On-the-Fly Task Generation** - Build phase generates tasks from the file manifest, no pre-planning overhead
6. **Cross-Phase Iteration** - `/iterate` command updates any phase document and cascades changes

### Component Diagram

```text
                               AgentSpec 4.2 Pipeline

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                                                                              │
  │   Phase 0          Phase 1         Phase 2         Phase 3         Phase 4  │
  │   (Optional)                                                                 │
  │                                                                              │
  │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
  │   │BRAINSTORM│───>│  DEFINE  │───>│  DESIGN  │───>│  BUILD   │───>│  SHIP  ││
  │   │  (Opus)  │    │  (Opus)  │    │  (Opus)  │    │ (Sonnet) │    │(Haiku) ││
  │   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └───┬────┘│
  │        │               │               │               │              │      │
  │        v               v               v               v              v      │
  │   BRAINSTORM_     DEFINE_         DESIGN_         Code +          SHIPPED_  │
  │   {FEATURE}.md    {FEATURE}.md    {FEATURE}.md    BUILD_REPORT    {DATE}.md │
  │                                                                              │
  │   ◀──────────────────────────────────────────────────────────────────────▶   │
  │                          /iterate (any phase)                                │
  │                                                                              │
  └─────────────────────────────────────────────────────────────────────────────┘

  ARTIFACT LOCATIONS:
  ├── .claude/sdd/features/       ← Active BRAINSTORM, DEFINE, DESIGN documents
  ├── .claude/sdd/reports/        ← BUILD_REPORT documents
  └── .claude/sdd/archive/        ← Shipped feature archives with SHIPPED summary
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `.claude/sdd/_index.md` | Main documentation and quick reference |
| `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml` | Machine-readable workflow specification |
| `.claude/sdd/templates/` | Document templates for each phase |
| `.claude/sdd/features/` | Active feature documents (BRAINSTORM, DEFINE, DESIGN) |
| `.claude/sdd/reports/` | Build reports |
| `.claude/sdd/archive/{FEATURE}/` | Shipped feature archives |
| `.claude/agents/workflow/` | Phase-specific agents (brainstorm-agent, define-agent, etc.) |
| `.claude/commands/workflow/` | Slash commands (/brainstorm, /define, /design, /build, /ship, /iterate) |

---

## Capabilities

### What It Can Do

- [x] Transform vague ideas into structured requirements through collaborative dialogue
- [x] Produce 15-point clarity-scored requirement documents
- [x] Generate architecture diagrams with inline ADRs
- [x] Create file manifests with dependency ordering
- [x] Delegate file creation to specialized agents
- [x] Verify code after each file creation (lint, type check, tests)
- [x] Archive features with lessons learned for future reference
- [x] Update any phase document with cascading changes via `/iterate`
- [x] Apply YAGNI during brainstorming to prevent scope creep

### What It Cannot Do

- Does not replace human judgment on requirements prioritization
- Does not automatically deploy code (IaC and CI/CD are separate concerns)
- Does not handle runtime monitoring (CrewAI is used for that)
- Not designed for trivial one-off fixes (use direct prompts or Dev Loop instead)

---

## How It Works

### Workflow

```text
User Idea ─> /brainstorm ─> BRAINSTORM.md ─> /define ─> DEFINE.md (Clarity: 15/15)
                                                            │
                                                            v
             Code Files <── /build <── DESIGN.md <── /design
                 │
                 v
            BUILD_REPORT.md ─> /ship ─> archive/{FEATURE}/SHIPPED.md
```

### Key Mechanisms

**Phase 0 - Brainstorm (Optional):**
- One question at a time (never dumps multiple questions)
- Presents 2-3 approaches with trade-offs and recommendation
- Applies YAGNI to remove unnecessary features
- Collects sample data for LLM grounding

**Phase 1 - Define:**
- Extracts structured requirements from any input (notes, emails, conversations)
- Calculates clarity score (0-15) across 5 dimensions
- Quality gate: Minimum 12/15 to proceed

**Phase 2 - Design:**
- Creates ASCII architecture diagrams
- Records inline decisions with rationale
- Produces file manifest with dependencies and agent assignments

**Phase 3 - Build:**
- Parses file manifest, orders by dependencies
- Delegates to specialized agents or executes directly
- Verifies each file (import, lint, tests)
- Generates BUILD_REPORT with agent attribution

**Phase 4 - Ship:**
- Archives all artifacts to `archive/{FEATURE}/`
- Records lessons learned by category (process, technical, tools)
- Updates document statuses to "Shipped"

### Code Examples

**Invoking the workflow:**

```bash
# Start with exploration (optional)
/brainstorm "Build invoice extraction pipeline"

# Define requirements (from brainstorm or directly)
/define .claude/sdd/features/BRAINSTORM_INVOICE_PIPELINE.md

# Create technical design
/design .claude/sdd/features/DEFINE_INVOICE_PIPELINE.md

# Build the code
/build .claude/sdd/features/DESIGN_INVOICE_PIPELINE.md

# Archive when complete
/ship .claude/sdd/features/DEFINE_INVOICE_PIPELINE.md
```

**Agent delegation in Build phase:**

```markdown
# File Manifest in DESIGN document
| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|--------------|
| 1 | `shared/schemas/invoice.py` | Create | Pydantic models | @extraction-specialist | None |
| 2 | `functions/extractor/main.py` | Create | Cloud Run handler | @function-developer | 1 |
| 3 | `tests/test_extractor.py` | Create | Unit tests | @test-generator | 2 |
```

**DEFINE clarity scoring:**

```markdown
## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---------|-------------|-------|
| Problem | 3 | Clear pain point with measurable impact |
| Users | 3 | Finance team specifically identified |
| Goals | 3 | MUST/SHOULD/COULD prioritized |
| Success | 3 | Quantified metrics (90% accuracy, <30s) |
| Scope | 3 | Clear out-of-scope items listed |
| **Total** | **15/15** | Ready for Design |
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| Rapid complex feature delivery | INVOICE_PIPELINE: 45 files, 2,500 LOC, 69 tests in 2 days |
| Prevents scope creep | YAGNI phase removes 2-5 features per brainstorm |
| Preserves context across sessions | Artifacts persist; no re-exploration needed |
| Quality consistency | Agent delegation ensures specialist patterns applied |
| Full traceability | DEFINE -> DESIGN -> BUILD_REPORT -> SHIPPED chain |
| Lessons captured | Ship phase records learnings for future reference |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| Overhead for simple tasks | Not worth it for <1 hour tasks (use Dev Loop instead) |
| Learning curve | 6 commands and 5 templates to understand |
| Model cost | Opus for Brainstorm/Define/Design phases |
| Sequential phases | Cannot parallelize across phases (by design) |

---

## Community & Adoption

- **GitHub Stars:** N/A (internal framework)
- **Contributors:** Custom development
- **Last Commit:** 2026-01-29 (v4.2.0)
- **Notable Users:** btc-zero-prd-claude-code project (this repository)

**Shipped Features Using AgentSpec:**
1. INVOICE_PIPELINE (45 files, 2 days)
2. GCS_UPLOAD
3. LANGFUSE_OBSERVABILITY
4. SMOKE_TEST
5. TERRAFORM_TERRAGRUNT_INFRA

---

## Official Resources

| Resource | URL |
|----------|-----|
| Index | `.claude/sdd/_index.md` |
| Contracts | `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml` |
| Templates | `.claude/sdd/templates/` |
| Examples | `.claude/sdd/examples/` |
| Archive | `.claude/sdd/archive/` |

---

## Key Takeaways

1. **AgentSpec is a 5-phase pipeline** (Brainstorm -> Define -> Design -> Build -> Ship) with optional exploration and cross-phase iteration
2. **Artifact-driven handoffs** enable context preservation across sessions and prevent the "lost context" problem of long AI conversations
3. **Agent delegation during Build** ensures specialist patterns are applied, producing higher quality code than generalist prompts
4. **Quality gates at each phase** (clarity score >= 12, file verification, lessons captured) prevent low-quality features from shipping
5. **Real-world proven** with 5 shipped features including a 45-file, 2,500 LOC pipeline delivered in 2 days

---

*Analysis completed: 2026-02-03 | Analyst: kb-architect*
