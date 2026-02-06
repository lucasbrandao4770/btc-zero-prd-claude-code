# SDD (Spec-Driven Development) Complete Guide

> **AgentSpec 4.2** - A 5-phase development workflow for AI-assisted software engineering

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Our SDD vs Industry SDD](#2-our-sdd-vs-industry-sdd-github-spec-kit)
3. [The 5-Phase Pipeline Overview](#3-the-5-phase-pipeline-overview)
4. [Phase 0: /brainstorm](#4-phase-0-brainstorm-optional-but-recommended)
5. [Phase 1: /define](#5-phase-1-define-requirements)
6. [Phase 2: /design](#6-phase-2-design-architecture)
7. [Phase 3: /build](#7-phase-3-build-implementation)
8. [Phase 4: /ship](#8-phase-4-ship-archive)
9. [Cross-Phase: /iterate](#9-cross-phase-iterate)
10. [Folder Structure](#10-folder-structure---why-it-works)
11. [Context Engineering](#11-context-engineering---how-sdd-prevents-drift)
12. [Rollbacks & Traceability](#12-rollbacks--traceability)
13. [Validation Summary](#13-validation-summary---all-quality-gates)
14. [Key Takeaways](#14-key-takeaways)

---

## 1. Introduction

### The Core Philosophy

SDD treats **specifications as the source of truth** - not code, not conversations. Every decision is captured, versioned, and traceable. This isn't bureaucracy; it's **context engineering** for AI agents.

### Why SDD Matters

When working with AI coding assistants, the biggest challenges are:
- **Context rot** - The AI "forgets" earlier context as conversations grow
- **Requirement drift** - Original intent gets lost over multiple iterations
- **Scope creep** - Features get added without explicit decisions
- **Implementation drift** - Code diverges from intended design

SDD solves these by making specifications **persistent, structured, and machine-readable**.

---

## 2. Our SDD vs Industry SDD (GitHub Spec Kit)

Here's how AgentSpec 4.2 compares to [GitHub's Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/):

| Aspect | GitHub Spec Kit | AgentSpec 4.2 |
|--------|-----------------|---------------|
| **Phases** | 3: Specify → Tasks → Implement | 5: Brainstorm → Define → Design → Build → Ship |
| **Exploration** | Minimal - jumps to spec | **Phase 0 Brainstorm** - explicit exploration |
| **Task Generation** | Pre-generated task list | **On-the-fly** from file manifest |
| **Architecture** | Implicit in spec | **Explicit DESIGN phase** with decisions |
| **Agent Matching** | None | **Agent assignment** per file |
| **Cross-Phase Changes** | Not explicit | **`/iterate`** with cascade awareness |
| **Archival** | Not included | **`/ship`** with lessons learned |

**Key Difference:** Spec Kit assumes you know what to build. AgentSpec has an **optional brainstorm phase** for when requirements are vague.

As [ThoughtWorks notes](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices): *"Spec-driven development is where specs drive implementation... but tools like Cursor or Claude Code need workflows that suit your needs."*

---

## 3. The 5-Phase Pipeline Overview

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Phase 0    │──▶│   Phase 1    │───▶│   Phase 2    │───▶│   Phase 3    │───▶│   Phase 4    │
│  BRAINSTORM  │    │   DEFINE     │    │   DESIGN     │    │    BUILD     │    │    SHIP      │
│  (Explore)   │    │  (What+Why)  │    │    (How)     │    │     (Do)     │    │   (Close)    │
│  [Optional]  │    │              │    │              │    │              │    │              │
│    Opus      │    │    Opus      │    │    Opus      │    │   Sonnet     │    │    Haiku     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼                   ▼
  BRAINSTORM_*.md     DEFINE_*.md         DESIGN_*.md        Code + Report       archive/
                                                             BUILD_REPORT_*.md   SHIPPED_*.md
```

### Model Assignment Rationale

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Brainstorm** | Opus | Creative thinking, nuanced dialogue |
| **Define** | Opus | Nuanced understanding of requirements |
| **Design** | Opus | Architectural decisions require depth |
| **Build** | Sonnet | Fast, accurate code generation |
| **Ship** | Haiku | Simple archival operations |
| **Iterate** | Sonnet | Balanced speed and understanding |

---

## 4. Phase 0: /brainstorm (Optional but Recommended)

### Purpose

Explore ideas through **collaborative dialogue** before capturing formal requirements. Prevents the common mistake of diving into implementation before understanding the problem.

### When to Use

- Vague idea that needs exploration
- Multiple possible approaches to consider
- Uncertain about scope or users
- Need to apply YAGNI before diving in

### When to Skip

- Clear requirements already known
- Meeting notes with explicit asks
- Simple feature request

### The Process

```
	Raw Idea ("I want to build a notification system")
			 │
			 ▼
    ┌─────────────────┐
    │ 1. ASK ONE      │  Never dump all questions at once!
    │    QUESTION     │  Multiple-choice preferred.
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. EXPLORE      │  Present 2-3 approaches with trade-offs
    │    APPROACHES   │  Include recommendation
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. VALIDATE     │  Every 200-300 words, confirm understanding
    │    INCREMENTALLY│  Minimum 2 validations
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 4. APPLY YAGNI  │  What features should we NOT build?
    │                 │  This section cannot be empty!
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. GET USER     │  User confirms selected approach
    │    CONFIRMATION │
    └────────┬────────┘
             │
             ▼
    BRAINSTORM_{FEATURE}.md
```

### Quality Gate

```
[ ] Minimum 3 discovery questions asked
[ ] 2-3 approaches explored with trade-offs
[ ] YAGNI applied (features removed section not empty)
[ ] Minimum 2 incremental validations completed
[ ] User confirmed selected approach
[ ] Draft requirements ready for /define
```

### Output Contents

- **Discovery Q&A** - The questions asked and answers given
- **Approaches Explored** - With trade-offs for each
- **Selected Approach** - With reasoning
- **Features Removed** - YAGNI list
- **Draft Requirements** - For next phase

---

## 5. Phase 1: /define (Requirements)

### Purpose

Transform **any input** into **structured requirements** with built-in validation. This is the "WHAT and WHY" phase.

### Input Types

| Input Type | Pattern | Focus |
|------------|---------|-------|
| `brainstorm_document` | BRAINSTORM_*.md | Pre-validated, extract directly |
| `meeting_notes` | Bullet points, action items | Decisions, requirements |
| `email_thread` | Re:, Fwd:, signatures | Requests, constraints |
| `conversation` | Informal language | Core problem, users |
| `direct_requirement` | Structured request | All elements present |

**Key Insight:** When input is a BRAINSTORM document, extraction is streamlined because discovery is already done.

### The Process

```
	Input (brainstorm, notes, email)
			 │
			 ▼
    ┌─────────────────┐
    │ 1. CLASSIFY     │  What type of input is this?
    │    INPUT        │  (brainstorm_document, meeting_notes, etc.)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. EXTRACT      │  Pull: Problem, Users, Goals, Success Criteria,
    │    ENTITIES     │  Acceptance Tests, Constraints, Out of Scope
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. CALCULATE    │  Score each element 0-3
    │    CLARITY      │  Total must be ≥ 12/15 to proceed
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
Score ≥ 12       Score < 12
    │                 │
    ▼                 ▼
Generate        Ask clarifying
DEFINE doc      questions
                     │
                     └──────► Loop until ≥ 12
```

### The Clarity Score - Your Quality Gate

| Element | What It Measures | Score 3 Example |
|---------|------------------|-----------------|
| **Problem** (0-3) | Is it specific and actionable? | "Users spend 2 hours daily on manual data entry" ✓ |
| **Users** (0-3) | Are pain points identified? | "Support team struggles with ticket routing" ✓ |
| **Goals** (0-3) | Are outcomes measurable? | "Reduce response time from 4h to 30min" ✓ |
| **Success** (0-3) | Can we test it? | "≥95% routing accuracy" ✓ |
| **Scope** (0-3) | Are boundaries explicit? | "NOT including: mobile app, analytics dashboard" ✓ |

**Scoring Guide:**

- **0** = Missing entirely
- **1** = Vague or incomplete
- **2** = Clear but missing details
- **3** = Crystal clear, actionable

**Why 12/15 (80%)?** This threshold ensures:

- No missing elements (would score 0)
- No completely vague elements (would score 1)
- At least "clear but missing details" across all elements

### Output Contents (DEFINE_*.md)

- **Problem Statement** - The pain point being solved
- **Target Users** - Who and their pain points
- **Goals** - MUST/SHOULD/COULD prioritization
- **Success Criteria** - Measurable (must include numbers)
- **Acceptance Tests** - Given/When/Then format
- **Out of Scope** - Explicit exclusions
- **Constraints** - Technical, timeline, resource
- **Technical Context** - Deployment location, KB domains
- **Assumptions** - What if wrong could invalidate design

### Quality Gate

```
[ ] Problem statement is clear and specific
[ ] At least one user persona identified
[ ] Success criteria are measurable
[ ] Acceptance tests are testable
[ ] Out of scope is explicit
[ ] Clarity Score >= 12/15
```

---

## 6. Phase 2: /design (Architecture)

### Purpose

Create a **complete technical design** with **inline decisions**. This is the "HOW" phase - translating requirements into architecture.

### What It Does

1. **Analyze** - Understand requirements from DEFINE
2. **Architect** - Design high-level solution with diagrams
3. **Decide** - Document key decisions with rationale (inline ADRs)
4. **Specify** - Create file manifest and code patterns
5. **Plan Testing** - Define testing strategy

### The Process

```
	DEFINE_{FEATURE}.md
			 │
			 ▼
    ┌─────────────────┐
    │ 1. LOAD         │  Read DEFINE + DESIGN_TEMPLATE
    │    CONTEXT      │  Explore codebase for existing patterns
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. CREATE       │  ASCII diagram of system
    │    ARCHITECTURE │  Components, data flow, integrations
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. DOCUMENT     │  For each significant choice:
    │    DECISIONS    │  Context, Choice, Rationale, Alternatives, Consequences
    │    (Inline ADRs)│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 4. CREATE FILE  │  THE CRITICAL ARTIFACT!
    │    MANIFEST     │  Every file to create, ordered by dependencies
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. DEFINE CODE  │  Copy-paste ready snippets
    │    PATTERNS     │  For consistent implementation
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 6. PLAN         │  Unit, Integration, E2E
    │    TESTING      │  Coverage goals per type
    └────────┬────────┘
             │
             ▼
    DESIGN_{FEATURE}.md
```

### The File Manifest - Heart of the Design

This is what `/build` uses to execute:

```markdown
| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|--------------|
| 1 | `src/schemas/user.py` | Create | Pydantic models | @python-developer | None |
| 2 | `src/adapters/database.py` | Create | DB adapter | @python-developer | None |
| 3 | `src/handlers/auth.py` | Create | Auth handler | @python-developer | 1, 2 |
| 4 | `tests/test_auth.py` | Create | Unit tests | @test-generator | 3 |
```

**Key Elements:**

- **#** - Execution order number
- **File** - Exact path (matches project structure)
- **Action** - Create, Modify, Delete
- **Purpose** - What this file does
- **Agent** - Which specialist to use
- **Dependencies** - Must be completed first (enables parallel where possible)

### Inline ADRs (Architecture Decision Records)

Instead of separate ADR files, decisions are inline:

```markdown
### Decision: Use PostgreSQL instead of MongoDB

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-02-05 |

**Context:** Need to store user data with complex relationships.

**Choice:** Use PostgreSQL with SQLAlchemy ORM.

**Rationale:**
- Strong consistency required for financial data
- Complex joins needed for reporting
- Team has PostgreSQL expertise

**Alternatives Rejected:**
1. MongoDB - Rejected: eventual consistency not acceptable
2. SQLite - Rejected: doesn't scale for concurrent users

**Consequences:**
- Need to manage database migrations
- Must configure connection pooling
```

### Output Contents (DESIGN_*.md)

- **Architecture Overview** - ASCII system diagram
- **Components** - List with purpose and technology
- **Key Decisions** - Inline ADRs with full rationale
- **File Manifest** - The execution plan for build
- **Agent Assignment Rationale** - Why each agent
- **Code Patterns** - Copy-paste ready snippets
- **Data Flow** - Step-by-step data movement
- **Integration Points** - External dependencies
- **Testing Strategy** - By type with coverage goals
- **Error Handling** - Strategy per error type
- **Configuration** - Keys, types, defaults
- **Security Considerations** - Threat mitigations
- **Observability** - Logging, metrics, tracing

### Quality Gate

```
[ ] Architecture diagram is clear
[ ] All major decisions documented with rationale
[ ] File manifest is complete (all files listed)
[ ] Code patterns are copy-paste ready
[ ] Testing strategy covers requirements
[ ] No circular dependencies in architecture
[ ] No shared dependencies across deployable units
```

---

## 7. Phase 3: /build (Implementation)

### Purpose

Execute the implementation by creating files **in dependency order** with verification after each step. This is the "DO" phase.

### What It Does

1. **Parse** - Extract file manifest from DESIGN
2. **Prioritize** - Order files by dependencies
3. **Execute** - Create each file with verification
4. **Validate** - Run tests after each significant change
5. **Report** - Generate build report

### The Process

```
	 DESIGN_{FEATURE}.md
			 │
			 ▼
    ┌─────────────────┐
    │ 1. PARSE FILE   │  Extract the file manifest table
    │    MANIFEST     │  (file, action, purpose, agent, dependencies)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. ORDER BY     │  Topological sort based on dependencies
    │    DEPENDENCIES │  (files with no deps first)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. EXECUTE      │  For each file in order:
    │    LOOP         │
    │                 │  ┌────────────────────────────┐
    │                 │  │ a. Read task from manifest │
    │                 │  │ b. Write code (use DESIGN  │
    │                 │  │    patterns!)              │
    │                 │  │ c. Run verification        │
    │                 │  │    └─ If FAIL → Fix (max 3)│
    │                 │  │ d. Mark complete           │
    │                 │  │ e. Next task               │
    │                 │  └────────────────────────────┘
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 4. FULL         │  ruff check . && mypy . && pytest
    │    VALIDATION   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. GENERATE     │  BUILD_REPORT_{FEATURE}.md
    │    REPORT       │
    └─────────────────┘
```

### The Execution Loop

```
┌─────────────────────────────────────────────────────┐
│                    EXECUTE TASK                     │
├─────────────────────────────────────────────────────┤
│  1. Read task from manifest                         │
│  2. Write code following DESIGN patterns            │
│  3. Run verification command                        │
│     └─ If FAIL → Fix and retry (max 3)              │
│  4. Mark task complete                              │
│  5. Move to next task                               │
└─────────────────────────────────────────────────────┘
```

### Handling Issues During Build

| Issue | Action |
|-------|--------|
| Missing requirement | Use `/iterate` to update DEFINE |
| Architecture problem | Use `/iterate` to update DESIGN |
| Simple bug | Fix immediately and continue |
| Major blocker | Stop and report in build report |

### Output Contents (BUILD_REPORT_*.md)

- **Summary** - What was built
- **Tasks Completed** - Each manifest item with status
- **Verification Results** - Lint, type check, test outcomes
- **Issues Encountered** - Any problems and resolutions
- **Metrics** - Files created, lines of code, time taken
- **Blockers** (if any) - What prevented completion

### Quality Gate

```
[ ] All files from manifest created
[ ] All verification commands pass
[ ] Lint check passes
[ ] Tests pass
[ ] No TODO comments left in code
[ ] Build report generated
```

---

## 8. Phase 4: /ship (Archive)

### Purpose

Archive completed feature with **lessons learned**. This is the "CLOSE" phase - capturing institutional knowledge for future work.

### When to Ship

- All acceptance tests from DEFINE pass
- Build report shows 100% completion
- No blocking issues remain
- Code deployed (if applicable)

### What It Does

1. **Verify** - Confirm all artifacts exist and build passed
2. **Archive** - Move feature documents to archive folder
3. **Document** - Create SHIPPED summary with lessons learned
4. **Clean** - Remove working files from features folder

### The Process

```
	All Feature Artifacts
			 │
			 ▼
    ┌─────────────────┐
    │ 1. VERIFY       │  Check BUILD_REPORT shows success
    │    COMPLETION   │  All acceptance tests passing
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 2. CREATE       │  mkdir -p .claude/sdd/archive/{FEATURE}/
    │    ARCHIVE DIR  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 3. COPY         │  BRAINSTORM_*.md (if used)
    │    ARTIFACTS    │  DEFINE_*.md
    │                 │  DESIGN_*.md
    │                 │  BUILD_REPORT_*.md
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 4. GENERATE     │  Summary, Timeline, Metrics
    │    SHIPPED DOC  │  LESSONS LEARNED (critical!)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 5. UPDATE       │  Status → "✅ Shipped"
    │    STATUSES     │  Add revision entry
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ 6. CLEAN UP     │  Remove from features/ and reports/
    │    WORKING FILES│  (archive is now source of truth)
    └────────┬────────┘
             │
             ▼
    archive/{FEATURE}/
    ├── BRAINSTORM_*.md
    ├── DEFINE_*.md
    ├── DESIGN_*.md
    ├── BUILD_REPORT_*.md
    └── SHIPPED_{DATE}.md
```

### Lessons Learned Categories

| Category | Example |
|----------|---------|
| **Process** | "Breaking tasks into smaller chunks helped" |
| **Technical** | "Config files work better than env vars" |
| **Communication** | "Early clarification saved rework" |
| **Tools** | "Using X library simplified Y" |

### Why This Matters

The archive becomes your **institutional memory**:

- Future features can reference patterns that worked
- Lessons learned prevent repeating mistakes
- Complete traceability from idea → shipped code
- Onboarding new team members (or fresh AI sessions)

### Output Structure

```
.claude/sdd/archive/{FEATURE}/
├── BRAINSTORM_{FEATURE}.md   ← Original exploration
├── DEFINE_{FEATURE}.md       ← Requirements
├── DESIGN_{FEATURE}.md       ← Architecture
├── BUILD_REPORT_{FEATURE}.md ← Execution results
└── SHIPPED_{DATE}.md         ← Final summary + lessons
```

### Quality Gate

```
[ ] BUILD_REPORT shows all tasks completed
[ ] No critical issues in build report
[ ] All tests passing
[ ] Code deployed (if applicable)
[ ] Lessons learned documented (be honest!)
```

---

## 9. Cross-Phase: /iterate

### Purpose

Update any phase document when requirements or design changes. Handles **cascade checking** to maintain consistency.

### When to Use

- New requirement discovered
- Architecture needs adjustment
- Scope change requested
- Bug found that affects design

### Cascade Awareness

```
	/iterate DEFINE_*.md "add PDF support"
			 │
			 ▼
    ┌─────────────────┐
    │ DETECT PHASE    │  This is a DEFINE document
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ APPLY CHANGE    │  Add PDF support to requirements
    │ + VERSION       │  Update revision history
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ CASCADE CHECK   │  Does this affect DESIGN?
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
No Impact       DESIGN needs update
    │                 │
    ▼                 ▼
Done            Prompt user:
                "Update DESIGN automatically?"
```

### Cascade Rules

| Source Change | May Affect |
|---------------|------------|
| BRAINSTORM | DEFINE (scope/approach changes) |
| DEFINE | DESIGN (new requirements) |
| DESIGN | Code (architecture changes) |

---

## 10. Folder Structure - Why It Works

```
.claude/sdd/
├── features/           ← ACTIVE WORK (hot)
│   ├── BRAINSTORM_*.md    ← Phase 0 artifacts
│   ├── DEFINE_*.md        ← Phase 1 artifacts
│   └── DESIGN_*.md        ← Phase 2 artifacts
│
├── reports/            ← BUILD OUTPUTS (warm)
│   └── BUILD_REPORT_*.md  ← Phase 3 artifacts
│
├── archive/            ← COMPLETED (cold)
│   └── {FEATURE}/
│       ├── All artifacts
│       └── SHIPPED_*.md   ← Phase 4 final record
│
├── templates/          ← PATTERNS (reference)
│   └── *_TEMPLATE.md
│
├── examples/           ← LEARNING RESOURCE
│   └── Complete worked examples
│
└── architecture/       ← SYSTEM DOCS (reference)
    ├── ARCHITECTURE.md
    └── WORKFLOW_CONTRACTS.yaml
```

### Design Choices

| Choice | Rationale |
|--------|-----------|
| **`features/` for active** | LLM reads this first - contains current context |
| **`reports/` separate** | Build outputs don't pollute planning artifacts |
| **`archive/` by feature** | Complete history per feature, easy to reference |
| **Templates at root** | Agents load these when generating documents |
| **Examples folder** | Learn from real completed workflows |

### Trade-offs

| Pro | Con |
|-----|-----|
| Clear separation of concerns | More navigation when searching |
| Easy to see "what's active" | Multiple folders to check |
| Archive preserves full history | Disk space grows over time |
| Templates ensure consistency | Templates need maintenance |

---

## 11. Context Engineering - How SDD Prevents Drift

Based on [LangChain's context engineering research](https://blog.langchain.com/context-engineering-for-agents/):

> *"Context engineering is the art and science of filling the context window with just the right information at each step."*

### SDD's Context Engineering Strategies

| Strategy | How SDD Implements It |
|----------|----------------------|
| **Write** (persist outside context) | Documents ARE persistent memory |
| **Select** (relevant info only) | Each phase loads only its inputs |
| **Compress** (summarize) | BRAINSTORM → DEFINE reduces exploratory noise |
| **Isolate** (separate contexts) | Each agent has narrow scope |

### How Documents Prevent Context Rot

**Problem:** LLMs "forget" earlier context as conversations grow.

**SDD Solution:**

```
Conversation: "I want to build..." ← May get lost in 50k tokens

     vs.

DEFINE_*.md:
  Problem: [written down]
  Users: [written down]
  Success Criteria: [written down] ← Always retrievable
```

**Each command re-reads the source documents.** `/build` doesn't rely on conversation history - it reads DESIGN fresh.

### How SDD Prevents Requirement Drift

| Risk | SDD Mitigation |
|------|----------------|
| **Original request changes** | BRAINSTORM captures original intent with user confirmation |
| **Scope creep** | "Out of Scope" section is explicit |
| **Feature drift** | YAGNI applied in brainstorm, enforced in DEFINE |
| **Implementation drift** | DESIGN file manifest is the execution spec |

---

## 12. Rollbacks & Traceability

### Traceability Chain

```
Code change
    ↓
BUILD_REPORT shows which manifest item
    ↓
DESIGN shows why this file exists
    ↓
DEFINE shows which requirement it fulfills
    ↓
BRAINSTORM shows why we chose this approach
```

### Version History in Documents

Each document has:

```markdown
## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-04 | brainstorm-agent | Initial version |
| 1.1 | 2026-02-05 | iterate-agent | Added new requirements |
```

### Rollback Mechanisms

1. **Git rollback** - All documents are files, standard git revert works
2. **Archive reference** - Previous features show proven patterns
3. **Iterate to previous** - `/iterate` can "undo" changes by specifying old state

---

## 13. Validation Summary - All Quality Gates

| Phase | Validation | Blocks Progress If |
|-------|------------|-------------------|
| **Brainstorm** | 3+ questions, 2+ approaches, user confirmation | User didn't confirm |
| **Define** | Clarity Score ≥ 12/15 | Score < 12 |
| **Design** | Complete manifest, no shared deps, patterns present | Manifest incomplete |
| **Build** | Lint passes, tests pass, all files created | Any verification fails |
| **Ship** | 100% build completion, acceptance tests pass | Blocking issues exist |

---

## 14. Key Takeaways

1. **Documents ARE the context** - Not just documentation, they're AI memory
2. **Quality gates enforce discipline** - 12/15 clarity score, complete manifests
3. **Cascade awareness prevents drift** - Changes propagate with awareness
4. **File manifest is the execution plan** - Build reads it like instructions
5. **Archive enables learning** - Shipped features show what worked
6. **Iterate is your friend** - Mid-stream changes are expected, not failures
7. **Each phase has a model** - Opus for thinking, Sonnet for doing, Haiku for closing

---

## Quick Reference

### Commands

| Command | Phase | Purpose |
|---------|-------|---------|
| `/brainstorm` | 0 | Explore ideas through dialogue |
| `/define` | 1 | Capture and validate requirements |
| `/design` | 2 | Create architecture and specification |
| `/build` | 3 | Execute implementation with verification |
| `/ship` | 4 | Archive with lessons learned |
| `/iterate` | Any | Update documents when changes needed |

### Artifacts

| Artifact | Phase | Location |
|----------|-------|----------|
| `BRAINSTORM_{FEATURE}.md` | 0 | `.claude/sdd/features/` |
| `DEFINE_{FEATURE}.md` | 1 | `.claude/sdd/features/` |
| `DESIGN_{FEATURE}.md` | 2 | `.claude/sdd/features/` |
| `BUILD_REPORT_{FEATURE}.md` | 3 | `.claude/sdd/reports/` |
| `SHIPPED_{DATE}.md` | 4 | `.claude/sdd/archive/{FEATURE}/` |

---

## References

- [GitHub Spec Kit - Spec-Driven Development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [ThoughtWorks - Spec-Driven Development in 2025](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [LangChain - Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/)
- [LlamaIndex - Context Engineering Techniques](https://www.llamaindex.ai/blog/context-engineering-what-it-is-and-techniques-to-consider)
- [Kubiya - Context Engineering Best Practices 2025](https://www.kubiya.ai/blog/context-engineering-best-practices)

---

*Created: 2026-02-05*
*Version: 1.0*
*AgentSpec Version: 4.2*
