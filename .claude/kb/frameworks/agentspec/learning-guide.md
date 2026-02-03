# AgentSpec - Learning Guide

> Educational resource for mastering AgentSpec: the 5-phase Spec-Driven Development workflow

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand the 5-phase development pipeline (Brainstorm, Define, Design, Build, Ship)
- [x] Learn how to transform vague ideas into structured requirements
- [x] Be able to create architecture documents with inline decisions
- [x] Apply agent delegation during the Build phase
- [x] Use /iterate for cross-phase updates without starting over

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Commands, tools, file operations | Claude Code documentation |
| Markdown familiarity | All artifacts are Markdown | Any Markdown guide |
| Basic software architecture | Understanding components, data flow | Experience or tutorials |
| Project context | Understanding the codebase | Read CLAUDE.md first |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Sequential phases are intuitive once learned |
| Implementation | Beginner-Intermediate | Commands guide you through each step |
| Time Investment | 2-4 hours | Full workflow can be learned in one session |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what AgentSpec is and why it matters

1. **Read the Index**
   - Location: `.claude/sdd/_index.md`
   - Time: 15 min
   - Key concepts to note:
     - 5 phases and their purposes
     - 6 commands (/brainstorm, /define, /design, /build, /ship, /iterate)
     - Artifact locations

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 20 min
   - Focus on: Component diagram, workflow section

3. **Review a Shipped Example**
   - Location: `.claude/sdd/archive/INVOICE_PIPELINE/`
   - Read in order:
     1. `BRAINSTORM_INVOICE_PIPELINE.md` - How exploration worked
     2. `DEFINE_INVOICE_PIPELINE.md` - Requirements with clarity score
     3. `DESIGN_INVOICE_PIPELINE.md` - Architecture and file manifest
     4. `BUILD_REPORT_INVOICE_PIPELINE.md` - Execution summary
     5. `SHIPPED_2026-01-30.md` - Lessons learned
   - Time: 30 min

**Checkpoint:** Can you explain what AgentSpec does in one sentence?

> AgentSpec transforms vague ideas into shipped features through 5 phases (Brainstorm, Define, Design, Build, Ship) with quality gates and persistent artifacts.

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: The Brainstorm Phase**
   - What it is: Optional exploration phase using one-question-at-a-time dialogue
   - Why it matters: Prevents scope creep by applying YAGNI before requirements
   - Key elements:
     - Discovery questions (minimum 3)
     - Sample collection for LLM grounding
     - 2-3 approaches with trade-offs
     - Recommended approach with reasoning

   ```bash
   # Example invocation
   /brainstorm "Build invoice extraction pipeline"

   # Output: BRAINSTORM_INVOICE_PIPELINE.md with:
   # - Questions and answers table
   # - Approaches explored
   # - Features removed (YAGNI)
   # - Draft requirements for Define
   ```

2. **Deep Dive: The Define Phase**
   - What it is: Structured requirements capture with clarity scoring
   - Why it matters: Quality gate prevents vague requirements from proceeding

   ```markdown
   ## Clarity Score Breakdown (from a real DEFINE)

   | Element | Score (0-3) | Notes |
   |---------|-------------|-------|
   | Problem | 3 | Clear: "3 FTEs spend 80% time on manual entry" |
   | Users | 3 | Specific: "Finance team" |
   | Goals | 3 | Prioritized: MUST/SHOULD/COULD |
   | Success | 3 | Quantified: ">=90% accuracy, <30s latency" |
   | Scope | 3 | Clear: Out of scope items listed |
   | **Total** | **15/15** | Ready for Design |
   ```

   - Quality gate: Minimum 12/15 to proceed

3. **Deep Dive: The Design Phase**
   - What it is: Architecture with inline decisions and file manifest
   - Why it matters: Build phase executes the manifest, no improvisation

   ```markdown
   ## File Manifest (from a real DESIGN)

   | # | File | Action | Purpose | Agent | Dependencies |
   |---|------|--------|---------|-------|--------------|
   | 1 | shared/schemas/invoice.py | Create | Pydantic models | @extraction-specialist | None |
   | 2 | functions/extractor/main.py | Create | Handler | @function-developer | 1 |
   | 3 | tests/test_extractor.py | Create | Tests | @test-generator | 2 |
   ```

4. **Deep Dive: Agent Delegation in Build**
   - What it is: Build phase invokes specialized agents based on file manifest
   - Why it matters: Specialists apply domain patterns, not generic code

   ```text
   Build Phase Agent Delegation:

   File Manifest Entry              Agent Invoked
   ─────────────────────            ──────────────
   shared/schemas/invoice.py   ->   @extraction-specialist (Pydantic + LLM patterns)
   functions/extractor/main.py ->   @function-developer (Cloud Run patterns)
   tests/test_extractor.py     ->   @test-generator (pytest fixtures)
   ```

5. **Hands-on Exercise**
   - Task: Walk through a complete workflow with a simple feature
   - Steps:
     1. Run `/brainstorm "Add a date parser utility"`
     2. Answer the questions (purpose, users, constraints)
     3. Review the generated BRAINSTORM document
     4. Run `/define` on the brainstorm output
     5. Check the clarity score
   - Success criteria: DEFINE document with clarity score >= 12

**Checkpoint:** Can you create a DEFINE document from a brainstorm session?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Cross-Phase Iteration**
   - When to use: Requirements change after Design is complete
   - Implementation: Use /iterate to update any document

   ```bash
   # Update DEFINE with new requirement
   /iterate DEFINE_DATA_EXPORT.md "Add support for CSV format"

   # Update DESIGN with architecture change
   /iterate DESIGN_DATA_EXPORT.md "Need separate validation function"

   # Cascade: /iterate can propagate changes downstream
   ```

   - Pitfalls:
     - Changes > 50% indicate need for new DEFINE, not iteration
     - Always update downstream documents after upstream changes

2. **Pattern: Sample Collection for LLM Accuracy**
   - When to use: Feature involves LLM extraction or processing
   - Implementation: Collect samples during Brainstorm

   ```markdown
   ## Sample Data Inventory

   | Type | Location | Count | Notes |
   |------|----------|-------|-------|
   | Input | data/invoices/*.tiff | 30 | 6 per vendor |
   | Schema | schemas/invoice.py | 1 | Pydantic model |
   | Ground truth | N/A | 0 | Generate during testing |

   How samples will be used:
   - Few-shot examples in extraction prompts
   - Schema validation reference
   - Test fixtures
   ```

3. **Pattern: When to Skip Brainstorm**
   - When to use: Clear requirements already exist
   - Indicators:
     - Meeting notes with explicit asks
     - Existing PRD or specification
     - Simple feature request

   ```bash
   # Skip directly to Define
   /define "Build a REST API for user management"

   # Or from existing notes
   /define notes/meeting-notes.md
   ```

4. **Real-World Exercise**
   - Scenario: You need to add LangFuse observability to an LLM extraction pipeline
   - Challenge: Complete the full workflow from Brainstorm to Ship
   - Hints:
     - Reference `.claude/sdd/archive/LANGFUSE_OBSERVABILITY/` for a real example
     - Check `.claude/kb/langfuse/` for patterns to include in DESIGN
     - Use @extraction-specialist for LLM-related files

**Checkpoint:** Can you complete a full Brainstorm-to-Ship workflow independently?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Phase Gate** | Quality check before proceeding to next phase | Clarity Score >= 12 for Define |
| **Artifact** | Markdown document produced by each phase | DEFINE_USER_AUTH.md |
| **File Manifest** | Table of files to create with dependencies | In DESIGN document |
| **Agent Delegation** | Invoking specialist agents for file creation | @function-developer for handlers |
| **Clarity Score** | 0-15 score measuring requirement quality | 15/15 = Ready for Design |
| **YAGNI** | "You Aren't Gonna Need It" - remove unnecessary features | Applied in Brainstorm |
| **Inline ADR** | Architecture Decision Record embedded in DESIGN | Key Decisions section |
| **Cascade** | Changes in one document requiring updates to downstream docs | DEFINE change -> DESIGN update |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Skipping Brainstorm for Complex Features

**What happens:** Requirements are vague, scope creeps during Build

**Why it happens:** Seems faster to jump to Define

**How to avoid:** If the idea is vague or has multiple possible approaches, use /brainstorm

**How to fix:** Run /brainstorm retroactively, then /iterate the DEFINE

---

### Mistake 2: Low Clarity Score Ignored

**What happens:** Design is incomplete, Build fails or produces wrong output

**Why it happens:** Rushing through Define phase

**How to avoid:** Quality gate is 12/15 minimum - don't proceed below this

**How to fix:** Use /iterate to improve weak sections

---

### Mistake 3: Improvising During Build

**What happens:** Files created that aren't in manifest, inconsistent patterns

**Why it happens:** Discovered need during implementation

**How to avoid:** Build phase follows manifest exactly

**How to fix:** Use /iterate to update DESIGN, then continue Build

---

### Mistake 4: Not Using Agent Delegation

**What happens:** Generic code without domain patterns

**Why it happens:** Didn't assign agents in file manifest

**How to avoid:** Assign appropriate agents in DESIGN file manifest

**How to fix:** Update manifest with agent assignments, re-run Build

---

## Practice Exercises

### Exercise 1: Read an Archive (Beginner)

**Objective:** Understand artifact relationships

**Instructions:**
1. Navigate to `.claude/sdd/archive/INVOICE_PIPELINE/`
2. Read each document in order (BRAINSTORM -> DEFINE -> DESIGN -> BUILD_REPORT -> SHIPPED)
3. Note how information flows between phases
4. Identify the clarity score and how it was achieved

**Solution:** The INVOICE_PIPELINE achieved 15/15 clarity by:
- Clear problem statement (3 FTEs, 80% manual time)
- Specific users (Finance team)
- Prioritized goals (MUST/SHOULD/COULD)
- Quantified success (90% accuracy, <30s latency)
- Explicit scope (5 vendors, no CrewAI in MVP)

---

### Exercise 2: Write a DEFINE (Intermediate)

**Objective:** Practice requirements capture

**Instructions:**
1. Read `.claude/sdd/templates/DEFINE_TEMPLATE.md`
2. Choose a simple feature (e.g., "Add email notification on errors")
3. Fill in each section
4. Calculate your clarity score
5. Compare with shipped examples

---

### Exercise 3: Complete Workflow (Advanced)

**Objective:** Execute full Brainstorm-to-Ship

**Challenge:** Build a date parsing utility

**Steps:**
1. `/brainstorm "Create a date parser for invoice dates"`
2. `/define` from brainstorm output
3. `/design` from define
4. `/build` from design
5. `/ship` from define

**Success criteria:**
- BRAINSTORM with >= 3 questions answered
- DEFINE with clarity score >= 12
- DESIGN with file manifest and agent assignments
- BUILD_REPORT with all files created
- SHIPPED with lessons learned

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Phase-gated development | Any structured methodology (Agile, Waterfall) |
| Requirements clarity scoring | PRD writing, user story quality |
| Architecture documentation | Technical design documents |
| Agent delegation | Multi-model AI orchestration |
| YAGNI discipline | MVP development, scope management |
| Lessons capture | Post-mortems, retrospectives |

---

## Study Resources

### Essential Reading

1. `.claude/sdd/_index.md` - Complete workflow documentation
2. `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml` - Machine-readable specification
3. `.claude/sdd/archive/INVOICE_PIPELINE/` - Real-world shipped example

### Supplementary Materials

- `.claude/sdd/templates/` - All document templates
- `.claude/agents/workflow/` - Phase-specific agent definitions
- `.claude/commands/workflow/` - Command documentation

### External References

- [11 Tips For AI Coding With Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) - Matt Pocock (referenced in Dev Loop)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - Anthropic

---

## Self-Assessment

### Quiz Yourself

1. What problem does AgentSpec solve?
   > Context loss, scope creep, quality inconsistency, and traceability gaps in AI-assisted development

2. How does the clarity score work?
   > 5 elements (Problem, Users, Goals, Success, Scope) scored 0-3 each, total 0-15, minimum 12 to proceed

3. When would you use /brainstorm vs /define directly?
   > Use /brainstorm for vague ideas needing exploration; /define directly for clear requirements

4. What are the main trade-offs of AgentSpec?
   > Overhead for simple tasks (use Dev Loop instead), learning curve, sequential phases

### Practical Assessment

Build: A complete feature using AgentSpec from Brainstorm to Ship

Success criteria:
- [x] Brainstorm completed with >= 3 questions
- [x] Define document achieves >= 12/15 clarity
- [x] Design includes file manifest with agent assignments
- [x] Build creates all files with verification
- [x] Ship captures at least 3 lessons learned

---

## What's Next?

After mastering AgentSpec, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for how they work together
2. **Dev Loop:** Study `.claude/dev/_index.md` for Level 2 development
3. **Agent Creation:** Learn to create new specialized agents in `.claude/agents/`
4. **KB Building:** Use AgentSpec to build new knowledge base domains

---

## Quick Reference Card

```text
AGENTSPEC COMMANDS
──────────────────
/brainstorm <idea>          Phase 0: Explore (optional)
/define <input>             Phase 1: Requirements
/design <define-file>       Phase 2: Architecture
/build <design-file>        Phase 3: Implementation
/ship <define-file>         Phase 4: Archive
/iterate <file> "<change>"  Cross-phase updates

QUALITY GATES
─────────────
Brainstorm: Min 3 questions, 2 approaches, YAGNI applied
Define: Clarity Score >= 12/15
Design: File manifest with dependencies
Build: All files verified (lint, tests)
Ship: Lessons captured

ARTIFACT LOCATIONS
──────────────────
Active:   .claude/sdd/features/BRAINSTORM_*.md, DEFINE_*.md, DESIGN_*.md
Reports:  .claude/sdd/reports/BUILD_REPORT_*.md
Archive:  .claude/sdd/archive/{FEATURE}/SHIPPED_*.md

WHEN TO USE WHAT
────────────────
Complex feature (multi-day)  -> AgentSpec
Structured task (1-4 hours)  -> Dev Loop (/dev)
Quick fix (<30 min)          -> Direct prompts
```

---

*Learning guide created: 2026-02-03 | For: AgentSpec 4.2*
