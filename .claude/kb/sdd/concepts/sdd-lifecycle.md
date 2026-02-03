# The SDD Development Lifecycle

> From idea to deployed software through specification-driven phases

---

## Overview

The SDD lifecycle consists of **5 phases** (with Phase 0 optional), each with a clear purpose, inputs, outputs, and quality gates:

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

## Phase 0: Brainstorm (Optional)

> **Purpose**: Explore ideas through collaborative dialogue before capturing requirements

### When to Use

| Use Brainstorm | Skip Brainstorm |
|----------------|-----------------|
| Vague idea that needs exploration | Clear requirements already known |
| Multiple possible approaches | Meeting notes with explicit asks |
| Uncertain about scope or users | Simple, well-defined feature request |
| Need to apply YAGNI before diving in | Urgency requires direct implementation |

### Process

```text
1. Present initial idea
   ↓
2. AI asks ONE question at a time (never dumps questions)
   ↓
3. Explore 2-3 approaches with trade-offs
   ↓
4. Apply YAGNI ruthlessly (remove speculative features)
   ↓
5. Draft requirements for Define phase
   ↓
6. User validates understanding
```

### Quality Gate

- Minimum 3 clarifying questions asked
- 2+ approaches explored with pros/cons
- 2+ validation checkpoints passed
- User confirmed selected approach

### Output

**BRAINSTORM_{FEATURE}.md** containing:
- Discovery questions and answers
- Approaches explored with trade-offs
- Selected approach with reasoning
- Features removed (YAGNI applied)
- Draft requirements for Define

---

## Phase 1: Define

> **Purpose**: Capture and validate requirements (WHAT and WHY)

### Input

- BRAINSTORM document, OR
- Raw notes, emails, conversations, OR
- Direct requirements description

### Process

```text
1. Analyze input for requirements
   ↓
2. Structure into user stories
   ↓
3. Define acceptance criteria (Given/When/Then)
   ↓
4. Identify success criteria (measurable)
   ↓
5. Mark out-of-scope items explicitly
   ↓
6. Document assumptions and constraints
   ↓
7. Calculate Clarity Score
```

### Clarity Score

The Define phase uses a 15-point scoring system:

| Element | Max Score | Criteria |
|---------|-----------|----------|
| Problem | 3 | Clear, specific, with business impact |
| Users | 3 | Defined personas with pain points |
| Goals | 3 | Measurable with MoSCoW prioritization |
| Success | 3 | Testable criteria with specific metrics |
| Scope | 3 | Explicit out-of-scope items |
| **Total** | **15** | Minimum 12/15 required |

### Quality Gate

- Clarity Score ≥ 12/15
- All acceptance tests defined (Given/When/Then)
- No unresolved `[NEEDS CLARIFICATION]` markers
- Out of scope clearly defined

### Output

**DEFINE_{FEATURE}.md** containing:
- Problem statement
- Target users
- Prioritized goals (MoSCoW)
- Success criteria (measurable)
- Acceptance tests
- Out of scope
- Constraints and assumptions
- Technical context for Design

---

## Phase 2: Design

> **Purpose**: Create complete technical design (HOW)

### Input

- DEFINE_{FEATURE}.md

### Process

```text
1. Analyze requirements for technical implications
   ↓
2. Create architecture (diagrams, decisions)
   ↓
3. Define file manifest (all files to create/modify)
   ↓
4. Document key decisions with rationale (inline ADRs)
   ↓
5. Create code patterns (copy-paste ready examples)
   ↓
6. Define testing strategy
   ↓
7. Sequence implementation phases
```

### Architecture Decision Records (ADRs)

In SDD, ADRs are **inline** within the Design document, not separate files:

```markdown
### Decision: Database Choice

**Status**: Accepted

**Context**: Need persistent storage for invoice data

**Options Considered**:
1. PostgreSQL - Relational, ACID compliance
2. MongoDB - Document store, flexible schema
3. BigQuery - Analytics-optimized, serverless

**Decision**: BigQuery

**Rationale**:
- Serverless aligns with Cloud Run architecture
- Native GCP integration reduces complexity
- Analytics queries are primary use case

**Consequences**:
- Cannot use traditional JOINs efficiently
- Must denormalize data model
```

### File Manifest

The Design includes a complete list of files to create:

```markdown
## File Manifest

| File | Purpose | Dependencies |
|------|---------|--------------|
| `src/schemas/invoice.py` | Pydantic models | None |
| `src/adapters/storage.py` | GCS adapter | schemas |
| `src/functions/extractor/main.py` | Cloud Run function | adapters, schemas |
| `tests/unit/test_schemas.py` | Schema tests | schemas |
```

### Quality Gate

- Complete file manifest with dependencies
- All architectural decisions documented with rationale
- Code patterns included (not pseudo-code)
- Testing strategy defined
- No shared dependencies that could cause coupling issues

### Output

**DESIGN_{FEATURE}.md** containing:
- Architecture diagram (ASCII or Mermaid)
- Key decisions with rationale
- File manifest with dependencies
- Code patterns (copy-paste ready)
- Testing strategy
- Implementation phases

---

## Phase 3: Build

> **Purpose**: Execute implementation following the design

### Input

- DESIGN_{FEATURE}.md

### Process

```text
1. Parse file manifest from Design
   ↓
2. Order files by dependencies
   ↓
3. For each file:
   │
   ├── Create/modify the file
   ├── Write associated tests
   ├── Verify with acceptance criteria
   └── Log progress
   ↓
4. Run full validation (lint, type-check, tests)
   ↓
5. Generate BUILD_REPORT
```

### Verification Loop

Each task in Build follows a verification loop:

```text
┌─────────────────────────────────────────┐
│           BUILD VERIFICATION            │
├─────────────────────────────────────────┤
│                                         │
│   Create ─▶ Test ─▶ Verify ─▶ Log      │
│      ↑                  │               │
│      │                  │               │
│      └──── Retry ◀──────┘               │
│           (if failed)                   │
│                                         │
└─────────────────────────────────────────┘
```

### Quality Gate

- All files from manifest created
- All tests passing
- Lint and type-check passing
- Acceptance tests from Define pass
- No `TODO` or `FIXME` comments added

### Output

- **Code files** as specified in manifest
- **Tests** for all new functionality
- **BUILD_REPORT_{FEATURE}.md** containing:
  - Summary of work completed
  - Files created/modified
  - Test results
  - Any deviations from Design
  - Issues encountered and resolutions

---

## Phase 4: Ship

> **Purpose**: Archive completed feature with lessons learned

### Input

- All feature artifacts (BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT)
- Working code with tests

### Process

```text
1. Verify all quality gates passed
   ↓
2. Move artifacts to archive folder
   ↓
3. Document lessons learned
   ↓
4. Update project documentation
   ↓
5. Create SHIPPED summary
```

### Lessons Learned

The Ship phase captures institutional knowledge:

```markdown
## Lessons Learned

### What Went Well
- Pydantic validation caught 15 edge cases during development
- File manifest prevented scope creep

### What Could Improve
- Should have added more acceptance tests for error paths
- Design phase underestimated BigQuery schema complexity

### Recommendations for Next Time
- Include explicit error handling scenarios in Define
- Add data model diagram to Design
```

### Quality Gate

- All previous phase gates passed
- Lessons learned documented
- Archive organized correctly
- Project documentation updated

### Output

**archive/{FEATURE}/** folder containing:
- BRAINSTORM_{FEATURE}.md (if used)
- DEFINE_{FEATURE}.md
- DESIGN_{FEATURE}.md
- BUILD_REPORT_{FEATURE}.md
- **SHIPPED_{DATE}.md** with lessons learned

---

## The /iterate Command

Throughout any phase, the `/iterate` command allows mid-stream updates:

```bash
# Update BRAINSTORM with new approach
/iterate BRAINSTORM_USER_AUTH.md "Consider using OAuth instead of custom tokens"

# Update DEFINE with new requirement
/iterate DEFINE_DATA_EXPORT.md "Add support for CSV format"

# Update DESIGN with architecture change
/iterate DESIGN_DATA_EXPORT.md "Components need to be self-contained"
```

### Iteration Triggers

| Trigger | Action |
|---------|--------|
| Stakeholder feedback | Update relevant phase document |
| Technical discovery | Update Design with new constraints |
| Scope change | Update Define, then cascade to Design |
| Implementation blocker | Document in Build Report, iterate Design if needed |

---

## Phase Duration Guidelines

| Phase | Typical Duration | Factors |
|-------|------------------|---------|
| Brainstorm | 15-30 min | Complexity of idea, number of approaches |
| Define | 30-60 min | Clarity of requirements, stakeholder alignment |
| Design | 1-2 hours | System complexity, integration points |
| Build | Hours to days | Scope, testing requirements |
| Ship | 15-30 min | Documentation completeness |

---

## Model Assignment (AgentSpec)

Different AI models are optimized for different phases:

| Phase | Model | Rationale |
|-------|-------|-----------|
| Brainstorm | Opus | Creative thinking, nuanced dialogue |
| Define | Opus | Nuanced understanding of requirements |
| Design | Opus | Architectural decisions require depth |
| Build | Sonnet | Fast, accurate code generation |
| Ship | Haiku | Simple archival operations |
| Iterate | Sonnet | Balanced speed and understanding |

---

## Lifecycle Visualization

```text
TIME ──────────────────────────────────────────────────────────────────────▶

PHASE    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────────┐ ┌─────────┐
         │BRAINSTORM│ │ DEFINE  │ │ DESIGN  │ │     BUILD     │ │  SHIP   │
         │(optional)│ │         │ │         │ │               │ │         │
         └────┬────┘ └────┬────┘ └────┬────┘ └───────┬───────┘ └────┬────┘
              │           │           │               │              │
              ▼           ▼           ▼               ▼              ▼
OUTPUT   BRAINSTORM_  DEFINE_     DESIGN_       Code + Tests    SHIPPED_
         {FEATURE}    {FEATURE}   {FEATURE}     BUILD_REPORT    {DATE}
         .md          .md         .md           {FEATURE}.md    .md

                              │
                              ▼
                    ┌─────────────────┐
                    │    /iterate     │
                    │  (any phase)    │
                    └─────────────────┘
```

---

## Next Steps

- **Learn specific patterns**: [../patterns/](../patterns/)
- **See real examples**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)
- **Understand terminology**: [terminology.md](terminology.md)

---

*References: AgentSpec 4.2 _index.md, Spec-Kit workflow documentation*
