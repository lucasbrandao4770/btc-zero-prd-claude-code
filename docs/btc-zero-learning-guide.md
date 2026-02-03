# btc-zero Learning Guide

> A comprehensive guide to mastering AI-Native development with the btc-zero-prd-claude-code repository.
> Based on the Zero to Production Bootcamp by Luan Moreno.

---

## Table of Contents

1. [The Paradigm Shift](#1-the-paradigm-shift)
2. [The Development Spectrum](#2-the-development-spectrum)
3. [Spec-Driven Development (SDD)](#3-spec-driven-development-sdd)
4. [Dev Loop System](#4-dev-loop-system)
5. [Agent System](#5-agent-system)
6. [Knowledge Base System](#6-knowledge-base-system)
7. [Best Practices](#7-best-practices)
8. [Common Mistakes](#8-common-mistakes)
9. [Progressive Skill Building](#9-progressive-skill-building)

---

## 1. The Paradigm Shift

### From Coder to Orchestrator

The traditional model of software engineering is being fundamentally transformed:

```
TRADITIONAL MODEL              AI-NATIVE MODEL
------------------              ---------------
80% coding, 20% thinking  -->  20% coding, 80% thinking
Write code manually       -->  Orchestrate AI agents
Debug line by line        -->  Validate and review
Stack Overflow lookup     -->  Agent-assisted development
Knowledge in heads        -->  Knowledge in bases
```

### The New Role: AI-Native Engineer

An AI-Native Engineer has three core competencies:

1. **Orchestration**
   - Understand domain deeply
   - Write specifications
   - Curate knowledge bases
   - Train agents with domain-specific knowledge

2. **Investigation**
   - Be curious about what is NOT shown
   - Question AI outputs
   - Validate beyond surface level
   - Understand the "why" behind decisions

3. **Context Curation**
   - Reduce context window waste
   - Provide precise, relevant information
   - Optimize attention mechanism effectiveness
   - Time knowledge appropriately

### Key Mindset Shifts

| Old Thinking | New Thinking |
|--------------|--------------|
| "I am paid to write code" | "I am paid to think, decide, and validate" |
| "Speed of typing matters" | "Quality of questions matters" |
| "More code = more value" | "Better decisions = more value" |
| "AI is a helper" | "AI is my fleet of specialized agents" |
---

## 2. The Development Spectrum

This repository supports three distinct levels of development, each suited to different tasks:

```
+-------------------------------------------------------------------------+
|                          DEVELOPMENT SPECTRUM                            |
+-------------------------------------------------------------------------+
|                                                                          |
|   LEVEL 1              LEVEL 2                   LEVEL 3                |
|   Vibe Coding          Dev Loop                  Spec-Driven Dev (SDD)  |
|   -----------          --------                  --------------------   |
|                                                                          |
|   - Just prompts       - PROMPT.md driven        - 5-phase pipeline     |
|   - No structure       - Question-first          - Full traceability    |
|   - Hope it works      - Verification loops      - Quality gates        |
|   - Quick fixes        - Agent leverage          - Enterprise audit     |
|                        - Memory bridge           - ADRs and specs       |
|                        - Priority execution                             |
|                                                                          |
|   Time: < 30 min       Time: 1-4 hours           Time: Multi-day       |
|   Command: (none)      Command: /dev             Command: /brainstorm   |
|                                                   to /ship              |
+-------------------------------------------------------------------------+
```

### Level 1: Vibe Coding

**What it is:** Ad-hoc prompting without structure. You describe what you want and hope AI produces it correctly.

**When to use:**
- Quick fixes (fix this typo, add this log)
- Experiments and prototypes
- Solo work with no documentation needs
- Tasks under 30 minutes

**Characteristics:**
- Intelligence lives in your head
- Depends on your mood/productivity that day
- Fast but not repeatable
- No documentation trail

**Key Quote:**
> "When you write code just for yourself, it is one thing. When you write code for a team, things start entering a negative loop."

### Level 2: Dev Loop

**What it is:** Structured iteration using PROMPT.md files, specialized agents, and session recovery.

**When to use:**
- Knowledge base creation
- Utility and parser development
- Single feature implementation
- Prototypes that need some structure

**Key Components:**

1. **Prompt Crafter** - Transforms your description into a structured PROMPT.md
2. **PROMPT.md Files** - Version-controlled task specifications
3. **Priority Execution** - RISKY first, then CORE, then POLISH
4. **Memory Bridge** - PROGRESS.md persists state between iterations
5. **Session Recovery** - Resume interrupted work with --resume

### Level 3: Spec-Driven Development (SDD)

**What it is:** A comprehensive 5-phase methodology with complete traceability.

**When to use:**
- Production features
- Multi-component features
- Team collaboration
- Features requiring documentation
- Regulated environments needing audit trails

**Benefits:**
- Complete traceability from requirements to code
- Team visibility into decisions
- Clear scope boundaries
- Documentation stays current
- Easy onboarding for new team members
---

## 3. Spec-Driven Development (SDD)

### The 5-Phase Pipeline

SDD is a structured workflow that takes features from idea to archive:

```
Phase 0        Phase 1        Phase 2        Phase 3        Phase 4
BRAINSTORM --> DEFINE    --> DESIGN    --> BUILD     --> SHIP
(Explore)      (What+Why)     (How)         (Do)          (Close)
[Optional]
    |             |             |             |             |
    v             v             v             v             v
BRAINSTORM   DEFINE_*.md   DESIGN_*.md   Code +       SHIPPED_*.md
  _*.md                                  Report        (archive)

Model:         Model:         Model:        Model:        Model:
Opus           Opus           Opus          Sonnet        Haiku
```

### Phase 0: Brainstorm (Optional)

**Purpose:** Explore ideas through collaborative dialogue before capturing requirements.

**Command:** `/brainstorm "your idea here"`

**Process:**
1. Ask one question at a time (never dump questions)
2. Use multiple-choice when options are clear
3. Present 2-3 approaches with trade-offs
4. Apply YAGNI ruthlessly (remove unnecessary features)
5. Validate understanding incrementally

**Output:** `BRAINSTORM_{FEATURE}.md`

**Skip this phase when:**
- Requirements are already clear
- You have meeting notes with explicit asks
- It is a simple feature request

### Phase 1: Define

**Purpose:** Capture and validate requirements from any input.

**Command:** `/define <input>`

**Input can be:**
- BRAINSTORM document
- Raw notes or emails
- Direct requirements text
- Meeting transcripts

**Output:** `DEFINE_{FEATURE}.md` containing:
- Problem statement
- Target users
- Success criteria (measurable)
- Acceptance tests (Given/When/Then)
- Out of scope

### Phase 2: Design

**Purpose:** Create complete technical design with inline decisions.

**Command:** `/design <DEFINE_doc>`

**Output:** `DESIGN_{FEATURE}.md` containing:
- Architecture diagram (ASCII)
- Key decisions with rationale
- File manifest (all files to create)
- Code patterns (copy-paste ready)
- Testing strategy

### Phase 3: Build

**Purpose:** Execute implementation following the design.

**Command:** `/build <DESIGN_doc>`

**Process:**
1. Parse file manifest from DESIGN
2. Order by dependencies
3. Create each file with verification
4. Run full validation (lint, tests)

**Output:** Code files + `BUILD_REPORT_{FEATURE}.md`

### Phase 4: Ship

**Purpose:** Archive completed feature with lessons learned.

**Command:** `/ship <DEFINE_doc>`

**Output:**
- All documents moved to `.claude/sdd/archive/{FEATURE}/`
- `SHIPPED_{DATE}.md` with lessons learned

### The /iterate Command

Use `/iterate` to update any document mid-stream when requirements change:

```bash
# Update brainstorm with new approach
/iterate BRAINSTORM_USER_AUTH.md "Consider using OAuth instead"

# Update define with new requirement
/iterate DEFINE_DATA_EXPORT.md "Add support for CSV format"

# Update design with architecture change
/iterate DESIGN_DATA_EXPORT.md "Components need to be self-contained"
```
---

## 4. Dev Loop System

### How It Works

```
/dev "description"                      /dev tasks/PROMPT_*.md
        |                                        |
        v                                        v
+-------------------+                    +-------------------+
|  PROMPT CRAFTER   |                    |  DEV LOOP         |
|                   |                    |  EXECUTOR         |
|  1. Explore       |                    |                   |
|  2. Ask           | -- generates -->   |  1. Load          |
|  3. Design        |    PROMPT.md       |  2. Pick (RISKY)  |
|  4. Confirm       |                    |  3. Execute       |
+-------------------+                    |  4. Verify        |
                                         |  5. Update        |
                                         |  6. Loop          |
                                         +---------+---------+
                                                   |
                                                   v
                                         +-------------------+
                                         |   EXIT_COMPLETE   |
                                         +-------------------+
```

### PROMPT.md Structure

A PROMPT.md file has these key sections:

1. **Goal** - One sentence describing what "done" looks like
2. **Quality Tier** - prototype, production, or library
3. **Context** - Background info, constraints, references
4. **Tasks** - Prioritized tasks with agent assignments
5. **Exit Criteria** - Objective, verifiable completion conditions
6. **Config** - Mode, max iterations, safeguards

### Priority Execution

Tasks are executed in priority order:

```
RISKY (Red)    --> Execute FIRST
                   Architectural decisions, unknowns, integrations
                   Fail fast on hard problems

CORE (Yellow)  --> Execute SECOND
                   Main feature implementation
                   The bulk of the work

POLISH (Green) --> Execute LAST
                   Cleanup, optimization, nice-to-haves
                   Only after core is working
```

### Task Syntax

Tasks can include agent references and verification commands:

```markdown
### RISKY (Do First)
- [ ] Validate API connectivity: Verify: `curl -I https://api.example.com`

### CORE
- [ ] @python-developer: Implement main parsing logic
- [ ] @test-generator: Add unit tests for parser
- [ ] Write integration tests: Verify: `pytest tests/integration/`

### POLISH (Do Last)
- [ ] @code-documenter: Update README with usage examples
- [ ] @code-reviewer: Final quality check
```

### Memory Bridge

The Memory Bridge (PROGRESS.md) prevents token burn from re-exploration:

- Records completed tasks
- Stores key decisions
- Tracks files changed
- Enables session recovery

### Session Recovery

If your session is interrupted (timeout, network issue, context rot):

```bash
# Resume from where you left off
/dev tasks/PROMPT_MY_FEATURE.md --resume

# The executor will:
# 1. Load the PROGRESS file
# 2. Skip completed tasks
# 3. Restore key decisions context
# 4. Continue from next incomplete task
```

### Quality Tiers

| Tier | Expectations | Use For |
|------|--------------|---------|
| `prototype` | Speed over perfection. Skip edge cases. Minimal tests. | Experiments, POCs |
| `production` | Tests required. Best practices. Full verification. | Real features |
| `library` | Backward compatibility. Full documentation. API stability. | Shared code |

### Safeguards

Built-in safeguards prevent runaway execution:

| Safeguard | Default | Purpose |
|-----------|---------|---------|
| `max_iterations` | 30 | Stop after N loops |
| `max_retries` | 3 | Retry failed tasks N times |
| `circuit_breaker` | 3 | Stop if no progress for N loops |
---

## 5. Agent System

### What Are Agents?

Agents are specialized AI configurations optimized for specific tasks. Each agent has:

- **System Prompt** - Role, capabilities, constraints
- **Tool Access** - File ops, search, execution
- **Validation System** - Confidence scoring and thresholds
- **Output Templates** - Structured formats for results

### Agent Categories

The repository contains 40+ agents organized by category:

#### Workflow Agents (SDD)

| Agent | Purpose |
|-------|---------|
| `brainstorm-agent` | Explore ideas through dialogue |
| `define-agent` | Capture and validate requirements |
| `design-agent` | Create technical architecture |
| `build-agent` | Execute implementation |
| `ship-agent` | Archive completed features |
| `iterate-agent` | Update documents mid-stream |

#### Code Quality Agents

| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Review code for quality issues |
| `code-cleaner` | Refactor and clean up code |
| `code-documenter` | Add documentation and comments |
| `python-developer` | Write Python code following standards |
| `test-generator` | Generate unit and integration tests |

#### Communication Agents

| Agent | Purpose |
|-------|---------|
| `meeting-analyst` | Extract structured info from meetings |
| `the-planner` | Create implementation roadmaps |
| `adaptive-explainer` | Explain concepts for any audience |

#### AI/ML Agents

| Agent | Purpose |
|-------|---------|
| `llm-specialist` | LLM integration and optimization |
| `genai-architect` | Design AI systems |
| `ai-prompt-specialist` | Craft and improve prompts |

#### Dev Loop Agents

| Agent | Purpose |
|-------|---------|
| `prompt-crafter` | Transform descriptions into PROMPT.md |
| `dev-loop-executor` | Execute PROMPT.md with verification |

### How to Use Agents

#### In PROMPT.md Files

Reference agents with `@agent-name`:

```markdown
### CORE
- [ ] @python-developer: Implement cache wrapper
- [ ] @test-generator: Add unit tests for caching
- [ ] @code-reviewer: Review the implementation
```

#### Direct Invocation

You can also invoke agents directly in conversation:

```
@meeting-analyst: Analyze notes/meeting-notes.md
                  Extract requirements for invoice processor
                  Write to design/requirements.md
```

### Agent Structure

Agents are defined in `.claude/agents/{category}/{agent-name}.md`:

```markdown
---
name: agent-name
description: |
  What this agent does and when to use it.
tools: [Read, Write, Edit, Grep, Glob]
---

# Agent Name

## Quick Reference
[Decision flow and key info]

## Validation System
[Confidence scoring rules]

## Capabilities
[What the agent can do]

## Output Formats
[Templates for results]
```
---

## 6. Knowledge Base System

### What Are Knowledge Bases?

Knowledge Bases (KBs) are domain-specific documentation organized for optimal AI comprehension. They provide:

- Consistent context for all agents
- Domain expertise extraction from human experts
- Single source of truth for development patterns
- Faster onboarding for new team members

### KB Structure

Each KB domain follows a standard structure:

```
.claude/kb/{domain}/
  index.md           # Domain overview and entry point
  quick-reference.md # Cheat sheet for common tasks
  concepts/          # Core concept explanations
    concept-a.md
    concept-b.md
  patterns/          # Implementation patterns
    pattern-x.md
    pattern-y.md
  specs/             # YAML specifications (optional)
```

### Available Domains

The repository includes 8 KB domains:

| Domain | Purpose | Key Topics |
|--------|---------|------------|
| `pydantic` | Data validation | Structured output, model validators |
| `gcp` | Google Cloud Platform | Cloud Run, GCS, BigQuery, Pub/Sub |
| `gemini` | Gemini LLM | Multimodal extraction, prompting |
| `langfuse` | LLM Observability | Tracing, cost tracking, analytics |
| `terraform` | Infrastructure as Code | Modules, state management |
| `terragrunt` | Multi-environment | DRY configs, dependency management |
| `crewai` | Multi-agent AI | Crews, tasks, agent coordination |
| `openrouter` | LLM Gateway | Model routing, fallbacks |

### Using Knowledge Bases

Agents automatically load relevant KBs based on task context. You can also explicitly reference them:

```
Use the pydantic KB to understand how to create
validated extraction schemas for invoice data.
```

### Creating New Knowledge Bases

Use the `/create-kb` command or Dev Loop:

```bash
# Interactive creation
/create-kb

# Using Dev Loop
/dev "Create a Redis KB with caching patterns"
```

---

## 7. Best Practices

### Reading and Patience

**Key Quote from Bootcamp:**
> "Social media took our patience away. We scroll for quick dopamine hits. Now we need to slow down our minds again. Reading is the critical skill for 2026."

**Practice:**
- Read entire specifications before coding
- Review agent outputs carefully
- Understand the "why" behind decisions
- Take time to validate, not just accept

### Choosing the Right Level

| Situation | Level | Reason |
|-----------|-------|--------|
| Quick typo fix | 1 | No structure needed |
| Building a utility | 2 | Needs some tracking but not full traceability |
| Production feature | 3 | Needs documentation, team visibility, audit trail |
| Multi-day feature | 3 | SDD handles interruptions and context |
| Experimenting | 1 or 2 | Speed matters more than documentation |

### Effective Agent Use

1. **Use the right agent for the task**
   - meeting-analyst for requirements extraction
   - the-planner for roadmaps
   - python-developer for code
   - test-generator for tests

2. **Provide context**
   - Reference relevant KB domains
   - Include constraints and requirements
   - Specify output format expectations

3. **Validate outputs**
   - Do not blindly accept AI code
   - Check against requirements
   - Run verification commands

### Structured Logging

When building systems, use structured JSON logs:

```
UNSTRUCTURED (avoid):
"Invoice 123 processed with amount 45"

STRUCTURED (prefer):
{
  "invoice_id": "123",
  "amount": 45,
  "status": "processed"
}
```

**Why structured logs matter:**
- 20-30% token reduction for LLM processing
- Better attention mechanism focus
- Enables pattern detection
- Critical for AI-based validation
---

## 8. Common Mistakes

### Using Level 1 for Everything

**Mistake:** Using vibe coding for production features.

**Problem:** No documentation, no traceability, hard to maintain.

**Solution:** Use Level 2 (Dev Loop) or Level 3 (SDD) for anything non-trivial.

### Skipping /brainstorm

**Mistake:** Jumping straight to /define with a vague idea.

**Problem:** Unclear requirements lead to rework.

**Solution:** Use /brainstorm when the idea is vague or multiple approaches are possible.

### Starting /build Without /design

**Mistake:** Going directly from requirements to implementation.

**Problem:** No architecture decisions, no file manifest, inconsistent implementation.

**Solution:** Always create a DESIGN document first.

### Ignoring Priority Order

**Mistake:** Starting with POLISH tasks or random task order.

**Problem:** Wasted effort on polish before core works.

**Solution:** Always execute in order: RISKY -> CORE -> POLISH

### Not Using Verification Commands

**Mistake:** Tasks without objective verification.

**Problem:** Cannot determine if task actually succeeded.

**Solution:** Add verification commands to tasks.

### Forgetting to Check KBs

**Mistake:** Implementing without leveraging existing knowledge bases.

**Problem:** Reinventing patterns, inconsistent approaches.

**Solution:** Before implementing, check relevant KBs.
---

## 9. Progressive Skill Building

### Week 1: Foundation

**Goal:** Understand the development spectrum.

**Tasks:**
1. Read .claude/CLAUDE.md thoroughly
2. Read .claude/sdd/_index.md and .claude/dev/_index.md
3. Try a simple task with Level 1 (vibe coding)
4. Try the same task with Level 2 (/dev)
5. Compare the experience and output quality

### Week 2: Dev Loop Mastery

**Goal:** Master the Dev Loop system.

**Tasks:**
1. Create 3 different PROMPT.md files from scratch
2. Practice using priority markers (RISKY, CORE, POLISH)
3. Use agent references (@agent-name)
4. Practice session recovery with --resume

### Week 3: SDD Fundamentals

**Goal:** Learn the full SDD workflow.

**Tasks:**
1. Complete one feature using all 5 phases
2. Practice /brainstorm conversation skills
3. Write clear DEFINE documents
4. Create comprehensive DESIGN documents
5. Ship and archive the feature

### Week 4: Advanced Patterns

**Goal:** Combine systems and handle complex scenarios.

**Tasks:**
1. Use /iterate to handle requirement changes
2. Work with multiple agents in sequence
3. Create custom agents for project-specific tasks
4. Build or extend knowledge bases

### Ongoing: Daily Practice

**Habits to Build:**

1. Before coding, ask: What level should this be?
2. Before prompting, think: What context does the AI need?
3. After AI output, validate: Does this meet the requirements?
4. After completing work, document: What did I learn?
---

## Summary

The btc-zero-prd-claude-code repository provides a complete framework for AI-Native development:

| Component | Purpose |
|-----------|---------|
| **3-Level Spectrum** | Match approach to task complexity |
| **Dev Loop** | Structured iteration with recovery |
| **SDD** | Full traceability for production features |
| **40+ Agents** | Specialized AI configurations |
| **8 Knowledge Bases** | Domain expertise codified |
| **13 Commands** | Streamlined workflows |

**Key Quote:**
> "You will think and AI will execute. You will design and AI will implement. You will validate and it will produce."

---

## Getting Started

1. Read .claude/CLAUDE.md for project-specific context
2. Read this guide for conceptual understanding
3. Read docs/btc-zero-quick-reference.md for command reference
4. Try /dev "simple task description" to start
5. Graduate to SDD (/brainstorm to /ship) for production features

---

*Learning Guide v1.0 - btc-zero-prd-claude-code*

*Based on Zero to Production Bootcamp by Luan Moreno*