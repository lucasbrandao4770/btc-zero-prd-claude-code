# Superpowers - Learning Guide

> Educational resource for mastering Superpowers concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand how composable skills enforce mandatory development workflows
- [x] Learn the TDD Iron Law and why "delete and restart" matters
- [x] Be able to implement two-stage code review (spec compliance + quality)
- [x] Apply rationalization prevention techniques in your own skill design
- [x] Master the verification-before-completion discipline

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Superpowers is a Claude Code plugin | [Claude Code docs](https://claude.ai/code) |
| TDD concepts | Core workflow enforces TDD | [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) |
| Git workflows | Uses worktrees and branches | Basic git knowledge |
| Markdown | Skills are markdown files | Any markdown guide |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Requires understanding of TDD and software development workflows |
| Implementation | Beginner | Just install plugin and follow skills |
| Time Investment | 2-4 hours | To understand core patterns; ongoing practice for mastery |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Superpowers is and why it matters

1. **Read the README**
   - Location: [github.com/obra/superpowers](https://github.com/obra/superpowers)
   - Time: 15 min
   - Key concepts to note: skills, subagent-driven development, TDD enforcement

2. **Read Jesse Vincent's Blog Post**
   - URL: [blog.fsck.com/2025/10/09/superpowers/](https://blog.fsck.com/2025/10/09/superpowers/)
   - Time: 30 min
   - Focus on: Why he created it, what problems it solves

3. **Install and Try Basic Workflow**
   - Instructions:
     ```bash
     # In Claude Code
     /plugin marketplace add obra/superpowers-marketplace
     /plugin install superpowers@superpowers-marketplace
     /help  # Verify commands appear
     ```
   - Expected outcome: See `/superpowers:brainstorm`, `/superpowers:write-plan`, `/superpowers:execute-plan`

**Checkpoint:** Can you explain what Superpowers does in one sentence?

> *"Superpowers enforces mandatory TDD, planning, and review workflows for AI coding agents through auto-activating skills."*

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Skills System**
   - What it is: Markdown files with YAML frontmatter that auto-activate based on context
   - Why it matters: Skills are mandatory, not suggestions
   - Key file: `skills/using-superpowers/SKILL.md`

   ```markdown
   ---
   name: using-superpowers
   description: Use when starting any conversation - establishes how to find and use skills
   ---

   <EXTREMELY-IMPORTANT>
   If you think there is even a 1% chance a skill might apply to what you are doing,
   you ABSOLUTELY MUST invoke the skill.
   </EXTREMELY-IMPORTANT>
   ```

2. **Deep Dive: TDD Iron Law**
   - What it is: Non-negotiable rule that code cannot be written before tests
   - Why it matters: Prevents agents from skipping tests "just this once"
   - Key file: `skills/test-driven-development/SKILL.md`

   ```markdown
   ## The Iron Law

   NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

   Write code before the test? Delete it. Start over.

   **No exceptions:**
   - Don't keep it as "reference"
   - Don't "adapt" it while writing tests
   - Delete means delete
   ```

3. **Deep Dive: Subagent-Driven Development**
   - What it is: Fresh subagent dispatched per task with two-stage review
   - Why it matters: Prevents context pollution; ensures quality
   - Key file: `skills/subagent-driven-development/SKILL.md`

   **Two-Stage Review:**
   1. Spec Reviewer - "Does code match specification exactly?"
   2. Code Quality Reviewer - "Is implementation well-built?"

4. **Hands-on Exercise: Run the Full Workflow**
   - Task: Build a simple utility using Superpowers
   - Steps:
     1. Start with `/superpowers:brainstorm "Create a URL shortener"`
     2. Answer questions one at a time
     3. Approve design sections
     4. Run `/superpowers:write-plan`
     5. Execute with subagent-driven development
   - Success criteria: Completed utility with tests, passing two-stage review

**Checkpoint:** Can you implement a basic feature using the full Superpowers workflow?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Rationalization Prevention**
   - When to use: Creating skills that enforce discipline
   - Implementation: Build rationalization tables from baseline testing

   ```markdown
   ## Common Rationalizations

   | Excuse | Reality |
   |--------|---------|
   | "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
   | "I'll test after" | Tests passing immediately prove nothing. |
   | "Already manually tested" | Ad-hoc =/= systematic. |
   ```

   - Pitfalls: Missing rationalizations agents will find

2. **Pattern: Verification-Before-Completion**
   - When to use: Before ANY completion claim
   - Implementation:

   ```markdown
   BEFORE claiming any status:

   1. IDENTIFY: What command proves this claim?
   2. RUN: Execute the FULL command (fresh, complete)
   3. READ: Full output, check exit code, count failures
   4. VERIFY: Does output confirm the claim?
   5. ONLY THEN: Make the claim
   ```

   - Pitfalls: Using "should pass" instead of actual evidence

3. **Pattern: Writing Skills (TDD for Documentation)**
   - When to use: Creating new skills
   - Implementation:
     1. RED: Run pressure scenario WITHOUT skill, document baseline failures
     2. GREEN: Write skill addressing those specific rationalizations
     3. REFACTOR: Close loopholes found in testing
   - Pitfalls: Writing skills without baseline testing

4. **Real-World Exercise: Create a Custom Skill**
   - Scenario: Your team has a code review checklist that agents skip
   - Challenge: Create a skill that enforces the checklist
   - Hints:
     - Start with pressure testing current behavior
     - Document exact rationalizations agents use
     - Build rationalization table
     - Add red flags list
     - Test under multiple pressure types (time, sunk cost, exhaustion)

**Checkpoint:** Can you create a new skill that passes pressure testing?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Skill** | Auto-activating markdown file with mandatory workflow | `test-driven-development/SKILL.md` |
| **Iron Law** | Non-negotiable rule that cannot be rationalized | "NO PRODUCTION CODE WITHOUT FAILING TEST FIRST" |
| **Subagent** | Fresh agent instance dispatched for specific task | Implementer subagent, spec reviewer subagent |
| **Two-Stage Review** | Spec compliance review followed by code quality review | First: "Does it match spec?" Then: "Is it well-built?" |
| **Rationalization Table** | Explicit counters to common excuses | "Too simple" --> "Simple code breaks" |
| **Red Flags** | Self-check patterns indicating rule violation | "Using 'should', 'probably', 'seems to'" |
| **Bite-Sized Task** | 2-5 minute implementation step with exact paths | "Step 1: Write failing test for X" |
| **CSO** | Claude Search Optimization - making skills discoverable | Description starts with "Use when..." |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Skipping Baseline Testing

**What happens:** Skill doesn't address actual agent behavior; loopholes remain

**Why it happens:** Developer assumes they know what agents will do

**How to avoid:** Always run pressure scenario WITHOUT skill first; document exact failures

**How to fix:** Re-run baseline, collect rationalizations, add counters

---

### Mistake 2: Writing Workflow Summaries in Descriptions

**What happens:** Agent follows description instead of reading full skill

**Why it happens:** Helpful intent - "let me summarize for quick reference"

**How to avoid:** Description should ONLY say "Use when..." - no process details

**Example:**
```yaml
# BAD - Agent may follow this instead of skill body
description: Use when executing plans - dispatches subagent per task with code review

# GOOD - Just triggering conditions
description: Use when executing implementation plans with independent tasks
```

---

### Mistake 3: Trusting Agent Completion Claims

**What happens:** Agent says "done" but code doesn't work

**Why it happens:** No verification requirement

**How to avoid:** Require fresh test output before ANY completion claim

**How to fix:** Add verification-before-completion as mandatory skill

---

## Practice Exercises

### Exercise 1: Install and Explore (Beginner)

**Objective:** Understand skill file structure

**Instructions:**
1. Clone the Superpowers repo
2. Read `skills/test-driven-development/SKILL.md`
3. Identify: Iron Law, Red Flags, Rationalization Table
4. Note: How does the skill prevent shortcuts?

**Solution:** The skill uses three mechanisms: (1) Iron Law states non-negotiable rule, (2) Red Flags help agent self-check, (3) Rationalization Table closes loopholes

---

### Exercise 2: Trace a Workflow (Intermediate)

**Objective:** Understand subagent-driven development flow

**Instructions:**
1. Read `skills/subagent-driven-development/SKILL.md`
2. Diagram the flow: Implementer --> Spec Review --> Quality Review
3. Identify: What happens if spec review fails? Quality review fails?
4. Note: Why two separate reviews instead of one?

**Answer:** Two reviews catch different problems - spec review prevents under/over-building (requirements mismatch), quality review ensures good implementation. If either fails, implementer fixes and review loops until approved.

---

### Exercise 3: Create a Verification Skill (Advanced)

**Objective:** Apply Superpowers patterns to new domain

**Challenge:** Create a skill that prevents agents from claiming "deployment complete" without verification

**Requirements:**
- Iron Law for deployment verification
- Red Flags list (what indicates rationalization)
- Rationalization table (excuses and counters)
- Verification checklist

---

## Transferable Skills

What you learn here applies to:

| Skill from Superpowers | Where Else It Applies |
|-------|----------------------|
| **Rationalization prevention** | Any AI instruction writing; prompt engineering |
| **Iron Laws** | Policy documents; team standards |
| **Two-stage review** | Human code review; QA processes |
| **Verification-before-completion** | CI/CD pipelines; deployment checklists |
| **TDD discipline** | All software development |
| **Skill composability** | Modular documentation; runbooks |

---

## Study Resources

### Essential Reading

1. **Superpowers README** - [github.com/obra/superpowers](https://github.com/obra/superpowers) - Start here
2. **Jesse Vincent's Blog** - [blog.fsck.com/2025/10/09/superpowers/](https://blog.fsck.com/2025/10/09/superpowers/) - Philosophy and origin

### Supplementary Materials

- [Simon Willison's Coverage](https://simonwillison.net/2025/Oct/10/superpowers/) - External perspective
- [Hacker News Discussion](https://news.ycombinator.com/item?id=45547344) - Community feedback
- [Cialdini's Influence](https://www.amazon.com/Influence-Psychology-Persuasion-Robert-Cialdini/dp/006124189X) - Persuasion principles used in skills

### Community Resources

- **GitHub Issues** - [github.com/obra/superpowers/issues](https://github.com/obra/superpowers/issues)
- **Anthropic Marketplace** - Official plugin listing

---

## Self-Assessment

### Quiz Yourself

1. What is the TDD Iron Law in Superpowers?
   > *"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" - delete and restart if violated*

2. Why does subagent-driven development use fresh subagents per task?
   > *Prevents context pollution; each task gets clean context*

3. What's the difference between spec review and code quality review?
   > *Spec review: "Does it match requirements exactly?" Quality review: "Is it well-implemented?"*

4. Why should skill descriptions NOT include workflow summaries?
   > *Agent may follow description instead of reading full skill body*

### Practical Assessment

Build: A documentation review skill that prevents agents from claiming "docs updated" without verification

Success criteria:
- [ ] Has Iron Law for documentation verification
- [ ] Includes rationalization table with 5+ counters
- [ ] Has red flags list
- [ ] Passes pressure testing (agent follows skill under time pressure)

---

## What's Next?

After mastering Superpowers, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas
2. **Related Frameworks:** Study Aider, Cursor Rules, Claude Code native skills
3. **Advanced Topics:**
   - Writing skills with pressure testing
   - Customizing subagent prompts
   - Extending for new platforms (beyond Claude Code)

---

*Learning guide created: 2026-02-02 | For: Superpowers Framework*
