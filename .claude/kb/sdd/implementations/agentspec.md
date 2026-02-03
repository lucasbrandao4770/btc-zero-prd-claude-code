# AgentSpec: SDD for Claude Code

> 5-phase SDD workflow adapted for Jarvis/Claude Code ecosystem

---

## Overview

**AgentSpec** is an adaptation of Spec-Driven Development for the Claude Code ecosystem. It features:

- 5-phase pipeline with optional Brainstorm
- Slash commands integrated with Claude Code
- Model assignment per phase (Opus/Sonnet/Haiku)
- Archive system for shipped features
- Integration with Dev Loop and Jarvis Planner Mode

**Location**: `.claude/sdd/` in projects using AgentSpec

---

## Version History

| Version | Key Changes |
|---------|-------------|
| 4.2 | Agent Matching (Design) + Agent Delegation (Build) |
| 4.1 | Added Phase 0: Brainstorm |
| 4.0 | Complete rewrite: 8→5 phases, single stream |

---

## Commands

| Command | Phase | Purpose | Model |
|---------|-------|---------|-------|
| `/brainstorm` | 0 | Explore ideas through dialogue | Opus |
| `/define` | 1 | Capture and validate requirements | Opus |
| `/design` | 2 | Create architecture and specification | Opus |
| `/build` | 3 | Execute implementation with verification | Sonnet |
| `/ship` | 4 | Archive with lessons learned | Haiku |
| `/iterate` | Any | Update documents when changes needed | Sonnet |

---

## The 5-Phase Pipeline

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Phase 0    │───▶│   Phase 1    │───▶│   Phase 2    │───▶│   Phase 3    │───▶│   Phase 4    │
│  BRAINSTORM  │    │   DEFINE     │    │   DESIGN     │    │    BUILD     │    │    SHIP      │
│  (Explore)   │    │  (What+Why)  │    │    (How)     │    │   (Execute)  │    │   (Archive)  │
│  [Optional]  │    │  [Required]  │    │  [Required]  │    │  [Required]  │    │  [Required]  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼                   ▼
  BRAINSTORM_*.md     DEFINE_*.md         DESIGN_*.md        Code + Tests       SHIPPED_*.md
                                                             BUILD_REPORT_*.md
```

---

## Workflow

### Starting a New Feature (with Brainstorm)

```bash
# Phase 0: Explore the idea
/brainstorm "I want to build a user notification system"

# Phase 1: Define requirements
/define .claude/sdd/features/BRAINSTORM_USER_NOTIFICATIONS.md

# Phase 2: Create technical design
/design .claude/sdd/features/DEFINE_USER_NOTIFICATIONS.md

# Phase 3: Build the code
/build .claude/sdd/features/DESIGN_USER_NOTIFICATIONS.md

# Phase 4: Archive when complete
/ship .claude/sdd/features/DEFINE_USER_NOTIFICATIONS.md
```

### Starting with Clear Requirements (skip Brainstorm)

```bash
# Phase 1: Define requirements directly
/define "Build a REST API for user management"

# Continue with /design → /build → /ship
```

### Making Changes Mid-Stream

```bash
# Update any phase document
/iterate BRAINSTORM_USER_AUTH.md "Consider OAuth instead of custom tokens"
/iterate DEFINE_DATA_EXPORT.md "Add support for CSV format"
/iterate DESIGN_DATA_EXPORT.md "Components need to be self-contained"
```

---

## Artifacts

| Artifact | Phase | Location |
|----------|-------|----------|
| `BRAINSTORM_{FEATURE}.md` | 0 | `.claude/sdd/features/` |
| `DEFINE_{FEATURE}.md` | 1 | `.claude/sdd/features/` |
| `DESIGN_{FEATURE}.md` | 2 | `.claude/sdd/features/` |
| `BUILD_REPORT_{FEATURE}.md` | 3 | `.claude/sdd/reports/` |
| `SHIPPED_{DATE}.md` | 4 | `.claude/sdd/archive/{FEATURE}/` |

---

## Folder Structure

```text
.claude/sdd/
├── _index.md                    # Overview and quick start
├── features/                    # Active feature documents
│   ├── BRAINSTORM_{FEATURE}.md
│   ├── DEFINE_{FEATURE}.md
│   └── DESIGN_{FEATURE}.md
├── reports/                     # Build reports
│   └── BUILD_REPORT_{FEATURE}.md
├── archive/                     # Shipped features
│   └── {FEATURE}/
│       ├── BRAINSTORM_{FEATURE}.md
│       ├── DEFINE_{FEATURE}.md
│       ├── DESIGN_{FEATURE}.md
│       ├── BUILD_REPORT_{FEATURE}.md
│       └── SHIPPED_{DATE}.md
├── examples/                    # Reference examples
│   └── README.md
├── templates/                   # Document templates
│   ├── BRAINSTORM_TEMPLATE.md
│   ├── DEFINE_TEMPLATE.md
│   ├── DESIGN_TEMPLATE.md
│   ├── BUILD_REPORT_TEMPLATE.md
│   └── SHIPPED_TEMPLATE.md
└── architecture/                # Workflow contracts
    ├── WORKFLOW_CONTRACTS.yaml
    └── ARCHITECTURE.md
```

---

## Phase Details

### Phase 0: Brainstorm (Optional)

**Purpose**: Explore ideas through collaborative dialogue

**Process**:
1. One question at a time (never dump questions)
2. Multiple-choice preferred
3. Present 2-3 approaches with recommendation
4. Apply YAGNI ruthlessly
5. Validate understanding incrementally

**Quality Gate**: Min 3 questions, 2+ approaches, user confirmed

**Output**: `BRAINSTORM_{FEATURE}.md`

### Phase 1: Define

**Purpose**: Capture and validate requirements (WHAT and WHY)

**Output includes**:
- Problem statement
- Target users
- Prioritized goals (MoSCoW)
- Success criteria (measurable)
- Acceptance tests (Given/When/Then)
- Out of scope
- Constraints and assumptions

**Quality Gate**: Clarity Score ≥ 12/15

**Output**: `DEFINE_{FEATURE}.md`

### Phase 2: Design

**Purpose**: Create complete technical design (HOW)

**Output includes**:
- Architecture diagram (ASCII)
- Key decisions with rationale (inline ADRs)
- File manifest (all files to create)
- Code patterns (copy-paste ready)
- Testing strategy

**Quality Gate**: Complete file manifest, no shared dependencies

**Output**: `DESIGN_{FEATURE}.md`

### Phase 3: Build

**Purpose**: Execute implementation following the design

**Process**:
1. Parse file manifest from Design
2. Order by dependencies
3. Create each file with verification
4. Run full validation (lint, tests)
5. Generate BUILD_REPORT

**Quality Gate**: All tests pass, all tasks complete

**Output**: Code, Tests, `BUILD_REPORT_{FEATURE}.md`

### Phase 4: Ship

**Purpose**: Archive completed feature with lessons learned

**Output includes**:
- All artifacts moved to archive folder
- Lessons learned documented
- Project documentation updated

**Output**: `archive/{FEATURE}/`, `SHIPPED_{DATE}.md`

---

## Model Assignment

| Phase | Model | Rationale |
|-------|-------|-----------|
| Brainstorm | Opus | Creative thinking, nuanced dialogue |
| Define | Opus | Nuanced understanding of requirements |
| Design | Opus | Architectural decisions require depth |
| Build | Sonnet | Fast, accurate code generation |
| Ship | Haiku | Simple archival operations |
| Iterate | Sonnet | Balanced speed and understanding |

---

## Key Principles

| Principle | Application |
|-----------|-------------|
| **Single Stream** | No mode switching, one unified workflow |
| **Inline Decisions** | ADRs in Design document, not separate files |
| **On-the-Fly Tasks** | Tasks generated from file manifest during build |
| **Self-Contained** | Each deployable unit works independently |
| **Iterate Anywhere** | Changes can be made at any phase via `/iterate` |

---

## Agent Matching (v4.2)

During the Design phase, AgentSpec can reference specialized agents:

```markdown
## Agent Assignments

| Component | Recommended Agent | Rationale |
|-----------|-------------------|-----------|
| Pydantic models | @python-developer | Python expertise |
| Cloud Run functions | @lambda-builder | Serverless patterns |
| Tests | @test-generator | pytest patterns |
| Documentation | @code-documenter | Doc standards |
```

During Build, use `@agent-name` references:

```markdown
### Task: Create Invoice Schema
@python-developer: Create Pydantic models for invoice extraction
```

---

## Integration with Dev Loop

AgentSpec and Dev Loop serve different purposes:

| Aspect | Dev Loop (Level 2) | AgentSpec (Level 3) |
|--------|-------------------|---------------------|
| Scope | Single feature/utility | Complex features |
| Duration | 1-4 hours | Multi-day |
| Structure | PROMPT.md | 5-phase pipeline |
| Traceability | Progress tracking | Full audit trail |
| Use Case | KB building, prototypes | Production features |

**When to use which**:
- Quick utility → Dev Loop
- KB domain → Dev Loop
- Production feature → AgentSpec
- Complex system → AgentSpec

---

## Integration with Jarvis Planner Mode

AgentSpec phases map to Jarvis Planner Mode:

| SDD Phase | Jarvis Phase | Agent |
|-----------|--------------|-------|
| Brainstorm | (Pre-planning) | User + Claude |
| Define | Strategic | strategic-architect |
| Design | Tactical | tactical-architect |
| Build | Operational | operational-planner |
| Ship | (Post-build) | User + Claude |

Both systems emphasize:
- Specification before implementation
- Phase gates for quality
- Document-driven workflow

---

## Templates

### DEFINE Template Key Sections

```markdown
## Problem Statement
{Who + What problem + Quantified impact}

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | |
| **SHOULD** | |

## Success Criteria
| ID | Criterion | Target |
|----|-----------|--------|

## Acceptance Tests
| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|

## Out of Scope
- {Item} - {Reason}

## Clarity Score Breakdown
| Element | Score (0-3) |
|---------|-------------|
| Problem | |
| Users | |
| Goals | |
| Success | |
| Scope | |
| **Total** | /15 |
```

### DESIGN Template Key Sections

```markdown
## Architecture
{ASCII diagram}

## Key Decisions
### D-001: {Title}
**Context**: {Why needed}
**Options**: {Alternatives}
**Decision**: {Choice}
**Rationale**: {Why}

## File Manifest
| # | File | Purpose | Dependencies |
|---|------|---------|--------------|

## Code Patterns
{Copy-paste ready examples}

## Implementation Phases
{Sequenced work with verification}
```

---

## Best Practices

### 1. Use Brainstorm for Vague Ideas

```bash
/brainstorm "I want to add caching somehow"
```

Better than guessing at requirements.

### 2. Achieve High Clarity Scores

Target 14-15/15, not just minimum 12/15:
- Clear problem with numbers
- Specific metrics for success
- Explicit out-of-scope

### 3. Document All Decisions

Every technical choice needs rationale:
- Why this database?
- Why this architecture?
- Why this library?

### 4. Keep File Manifest Complete

No "and others" or "as needed":
- List every file
- Show dependencies
- Define creation order

### 5. Run /iterate Early

When requirements change, update specs immediately:
```bash
/iterate DEFINE_FEATURE.md "Add new requirement X"
```

Don't let code drift from spec.

---

## Shipped Features Example

```text
.claude/sdd/archive/
├── INVOICE_PIPELINE/           # Core extraction pipeline
├── GCS_UPLOAD/                 # GCS integration
├── LANGFUSE_OBSERVABILITY/     # LLM monitoring
├── SMOKE_TEST/                 # E2E testing framework
└── TERRAFORM_TERRAGRUNT_INFRA/ # Infrastructure as Code
```

Each folder contains full artifact history.

---

## Key Differentiators

### vs. Spec-Kit

| Aspect | AgentSpec | Spec-Kit |
|--------|-----------|----------|
| Brainstorm | Dedicated Phase 0 | Via /speckit.clarify |
| Constitution | Optional | Required |
| Model Assignment | Explicit per phase | Not specified |
| Archive | Folder-based | Branch-based |
| Integration | Jarvis ecosystem | General purpose |

### vs. Vibe Coding

| Aspect | AgentSpec | Vibe Coding |
|--------|-----------|-------------|
| Structure | 5-phase pipeline | Ad-hoc prompts |
| Documentation | Full artifacts | None |
| Verification | Quality gates | Hope it works |
| Traceability | Complete | None |

See [comparison.md](comparison.md) for detailed comparison.

---

## Resources

- **SDD Overview**: `.claude/sdd/_index.md`
- **Templates**: `.claude/sdd/templates/`
- **Examples**: `.claude/sdd/examples/`
- **Shipped Features**: `.claude/sdd/archive/`
- **Workflow Contracts**: `.claude/sdd/architecture/`

---

*References: AgentSpec 4.2 _index.md, .claude/sdd/ structure*
