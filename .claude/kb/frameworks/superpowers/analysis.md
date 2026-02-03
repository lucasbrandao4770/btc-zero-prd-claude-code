# Superpowers - Framework Analysis

> Deep dive into Superpowers: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | [github.com/obra/superpowers](https://github.com/obra/superpowers) |
| **Author** | Jesse Vincent (obra) |
| **Category** | Agentic Development Workflow |
| **Context7 ID** | `/obra/superpowers` |
| **Last Updated** | 2026-02-02 |

### One-Line Summary

Superpowers is a composable skills framework that enforces mandatory development workflows (TDD, planning, review) for AI coding agents, enabling autonomous operation for hours without deviation.

---

## Problem Statement

### What Problem Does It Solve?

AI coding agents tend to:
1. **Jump straight to code** without understanding requirements
2. **Skip testing** or write tests after implementation
3. **Produce inconsistent results** based on context pollution
4. **Rationalize shortcuts** under time pressure
5. **Claim completion** without verification

Superpowers enforces structured workflows that prevent these failure modes.

### Who Is It For?

- Developers using Claude Code, Codex, or OpenCode for AI-assisted development
- Teams wanting autonomous agent execution with quality guarantees
- Projects requiring strict TDD and code review processes
- Anyone frustrated by agents that "just start coding" without planning

### Why Does This Matter?

Without enforced workflows, AI agents:
- Produce code that compiles but doesn't meet requirements
- Create technical debt through skipped tests
- Require constant human oversight
- Cannot work autonomously for extended periods

With Superpowers, Claude Code can work autonomously for 2+ hours on complex implementations while maintaining code quality.

---

## Architecture

### Core Concepts

1. **Skills** - Markdown files that auto-activate based on context triggers. Skills are mandatory workflows, not suggestions. Each skill has frontmatter (name, description) and structured instructions.

2. **Subagent-Driven Development** - Fresh subagent dispatched per task with two-stage review (spec compliance, then code quality). Prevents context pollution between tasks.

3. **Iron Laws** - Non-negotiable rules that cannot be rationalized away. Examples: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST", "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST".

4. **Rationalization Tables** - Explicit counters to common excuses agents use to skip processes. Built from baseline testing.

5. **Red Flags Lists** - Self-check patterns that indicate an agent is about to violate a skill's discipline.

### Component Diagram

```
USER REQUEST
     |
     v
+--------------------+
| using-superpowers  |  <-- Always runs first
| (skill discovery)  |
+--------------------+
     |
     v
+--------------------+     +--------------------+
|    brainstorming   | --> |   writing-plans    |
| (design refinement)|     | (implementation)   |
+--------------------+     +--------------------+
                                   |
          +------------------------+------------------------+
          v                                                 v
+--------------------+                            +--------------------+
| subagent-driven    |                            |   executing-plans  |
| development        |                            | (parallel session) |
| (same session)     |                            +--------------------+
+--------------------+
          |
          v
+--------------------+
| Per-Task Loop:     |
| - Implementer      |
| - Spec Reviewer    |
| - Code Reviewer    |
+--------------------+
          |
          v
+--------------------+
| finishing-branch   |
| (merge/PR/discard) |
+--------------------+
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `skills/*/SKILL.md` | Individual skill definitions |
| `commands/*.md` | Slash command definitions |
| `agents/*.md` | Subagent prompts (code-reviewer) |
| `hooks/*.sh` | Session lifecycle scripts |
| `docs/plans/` | Generated design and implementation plans |
| `.claude-plugin/` | Plugin marketplace metadata |

---

## Capabilities

### What It Can Do

- [x] Enforce TDD (RED-GREEN-REFACTOR) before any implementation
- [x] Create detailed implementation plans with bite-sized tasks (2-5 min each)
- [x] Dispatch fresh subagents per task to prevent context pollution
- [x] Two-stage code review (spec compliance + code quality)
- [x] Systematic debugging with 4-phase root cause process
- [x] Verification-before-completion enforcement
- [x] Git worktree isolation for parallel development
- [x] Support for Claude Code, Codex, and OpenCode

### What It Cannot Do

- No persistent memory system (uses file-based plans only)
- No specialized domain agents (e.g., Spark, Fabric, healthcare)
- No personality modes or output styling
- No calendar/scheduling integration
- No MCP tool orchestration beyond basic usage
- Cannot prevent all rationalization (agents still find loopholes)

---

## How It Works

### Workflow

```
Idea --> Brainstorm --> Design Doc --> Implementation Plan --> Per-Task Execution --> Merge/PR
          (questions)   (sections)    (bite-sized tasks)    (subagent + 2 reviews)
```

### Key Mechanisms

**1. Skill Auto-Activation**

Skills trigger automatically based on context. The `using-superpowers` skill runs first and checks for relevant skills before ANY response:

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

**2. TDD Iron Law**

From `test-driven-development/SKILL.md`:

```markdown
## The Iron Law

NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

**3. Subagent Dispatch**

Fresh subagent per task with complete context provided upfront:

```markdown
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name]

    ## Task Description
    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context
    [Scene-setting: where this fits, dependencies, architectural context]
```

**4. Two-Stage Review**

After each task:
1. **Spec Reviewer** - Verifies code matches specification exactly
2. **Code Quality Reviewer** - Checks implementation quality

Both must pass before moving to next task.

### Code Examples

**Bite-Sized Task Structure (from writing-plans skill):**

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

**Step 4: Run test to verify it passes**

**Step 5: Commit**
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| **TDD Enforcement** | Iron Law with explicit delete-and-restart mandate; rationalization tables counter all common excuses |
| **Context Hygiene** | Fresh subagent per task prevents context pollution; 2+ hours autonomous operation reported |
| **Psychological Rigor** | Uses Cialdini's persuasion principles; tested with pressure scenarios |
| **Battle-Tested** | 29K+ GitHub stars; accepted into Anthropic marketplace (Jan 2026) |
| **Quality Gates** | Two-stage review (spec + quality) ensures nothing slips through |
| **Skill Composability** | Skills reference each other with explicit REQUIRED markers |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| **TDD Dogmatism** | No flexibility for exploration/prototyping without explicit user permission |
| **No Persistent Memory** | Plans stored in files; no cross-session state management |
| **Limited Agent Specialization** | Generic implementer/reviewer vs. domain experts |
| **Process Overhead** | Every feature requires full brainstorm-plan-execute cycle |
| **Claude Code Focus** | Codex/OpenCode support is secondary, requires manual setup |

---

## Community & Adoption

- **GitHub Stars:** 29,000+
- **Contributors:** Growing open-source community
- **Last Commit:** Active development (January 2026)
- **Notable Users:** Endorsed by Simon Willison, featured on Hacker News
- **Marketplace:** Accepted into Anthropic's official Claude plugins marketplace (Jan 15, 2026)

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | [github.com/obra/superpowers](https://github.com/obra/superpowers) |
| Blog Post | [blog.fsck.com/2025/10/09/superpowers/](https://blog.fsck.com/2025/10/09/superpowers/) |
| Simon Willison Coverage | [simonwillison.net/2025/Oct/10/superpowers/](https://simonwillison.net/2025/Oct/10/superpowers/) |
| Hacker News Discussion | [news.ycombinator.com/item?id=45547344](https://news.ycombinator.com/item?id=45547344) |

---

## Key Takeaways

1. **Skills are mandatory workflows, not suggestions.** The framework uses psychological principles to prevent agents from rationalizing shortcuts.

2. **Fresh subagent per task is the key innovation.** This prevents context pollution and enables hours of autonomous operation.

3. **Two-stage review (spec + quality) catches both under-building and over-building.** Spec review ensures requirements are met exactly; quality review ensures implementation is well-done.

4. **Verification-before-completion prevents false claims.** "Evidence before claims, always" - no completion without fresh test output.

5. **TDD is non-negotiable.** The Iron Law requires deleting any code written before tests, with explicit counters to all rationalization patterns.

---

*Analysis completed: 2026-02-02 | Analyst: kb-architect*
