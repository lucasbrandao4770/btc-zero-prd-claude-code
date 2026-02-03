# Jarvis Skills System

> **MCP Validated:** 2026-02-01

---

## Overview

Skills are auto-activating behavior modules that provide workflow automation based on context. Unlike agents (which are invoked explicitly), skills activate automatically when their trigger conditions are met.

**Key Difference from Agents:**
- **Agents:** Explicitly invoked via Task tool, domain expertise
- **Skills:** Auto-activated by context, workflow automation

---

## Skill File Structure

Skills are located in `skills/{skill-name}/SKILL.md`.

### SKILL.md Format

```markdown
---
name: skill-name
description: Multi-line description of what the skill does and when it activates.
---

# Skill Name

## When This Skill Activates

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## What This Skill Provides

[Instructions, patterns, workflows, commands]

## Quick Commands

| Action | Command |
|--------|---------|
| ... | ... |
```

---

## Example: code-quality Skill

```markdown
---
name: code-quality-pipeline
description: Automated code quality checks for Python projects. Activates when Python files are created or modified, when user mentions quality/lint/format, or preparing for git commits.
---

# Code Quality Pipeline

## When This Skill Activates

- Python files (.py) are created or modified
- User mentions: quality, lint, format, type check, clean code
- Preparing for git commit
- Code review requested

## Quality Workflow

### Step 1: Format with Ruff
```bash
ruff format {file_or_directory}
```

### Step 2: Lint with Ruff
```bash
ruff check {file_or_directory} --fix
```

### Step 3: Type Check
```bash
pyright {file_or_directory}
```

## Quality Checklist

- [ ] Ruff formatting applied
- [ ] Ruff linting passes
- [ ] Type hints on all function signatures
- [ ] Docstrings on public APIs
```

---

## Skill Categories

### Code Quality (3 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| code-quality-pipeline | Python files | Ruff, type hints, docstrings |
| testing | Business logic created | Pytest patterns |
| agent-quality | Agent files modified | Agent validation |

### Version Control (1 skill)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| git-workflow | Git operations | Conventional commits |

### Research (1 skill)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| context7-research | Library work | Documentation lookup |

### Workflow (1 skill)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| planning | Complex tasks | Session chunking |

### Automation (3 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| sandbox | "sandbox", "YOLO" | Isolated execution |
| swarm-orchestrator | Parallel processing | Divide-and-conquer |
| bash-devcontainer | DevContainer work | Docker/bash patterns |

### Modes (7 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| sensei | "teach me", "learn" | Learning mode |
| taiwan | Taiwan universities | Taiwan mode |
| pm | Sprint, backlog | PM mode |
| finances | Budget, expenses | Finance mode |
| fabric | Microsoft Fabric | Fabric mode |
| faturamento | Healthcare billing | Faturamento mode |
| genai | Multi-agent systems | GenAI mode |

### Frontend (2 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| ui-forge | React components | Magic MCP orchestration |
| lovable | UI prototyping | Lovable.dev patterns |

### Utilities (5 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| youtube | YouTube URLs | Transcript extraction |
| mindmap | Mind map text | Structure parsing |
| work-report | Weekly report | Sprint-aligned reports |
| skill-manager | "what skills" | Catalog search |
| system-audit | "audit system" | Component validation |

### Career (2 skills)

| Skill | Triggers On | Purpose |
|-------|-------------|---------|
| taiwan-career | Taiwan job | Taiwan context |
| job-application | Job application | Application workflow |

---

## Skill Activation Mechanics

### How Skills Activate

1. User input or context matches trigger conditions
2. Claude Code loads the SKILL.md content
3. Instructions become available in context
4. Claude follows the skill's workflow

### Trigger Examples

```yaml
# From skills-catalog.yaml
activates_when:
  - Python files created or modified
  - User mentions quality, lint, format, type check
  - Preparing for git commit
```

### No Manual Invocation Needed

Unlike agents, skills don't need explicit invocation:

```
# Agents - explicit invocation required
Task(subagent_type="code-reviewer", prompt="...")

# Skills - auto-activate based on context
# Just modify a Python file, and code-quality skill activates
```

---

## Skill Catalog

The authoritative list is in `catalogs/skills-catalog.yaml`:

```yaml
skills:
  - name: code-quality-pipeline
    path: ~/.claude/skills/code-quality/SKILL.md
    category: code-quality
    description: |
      Automated code quality checks for Python projects.
    activates_when:
      - Python files created or modified
      - User mentions quality, lint, format, type check
    provides:
      - Ruff formatting commands
      - Linting workflow
      - Type checking guide
```

---

## Skills vs Agents

| Aspect | Skills | Agents |
|--------|--------|--------|
| Invocation | Auto-activated by context | Explicit via Task tool |
| Purpose | Workflow automation | Domain expertise |
| Scope | Provide patterns/commands | Execute complete tasks |
| File Location | `skills/{name}/SKILL.md` | `agents/{cat}/{name}.md` |
| Complexity | Usually simpler | More complex behavior |

### When to Use Skills

- Recurring workflow patterns (code quality, git)
- Context-dependent behavior (research, testing)
- Mode activation (sensei, taiwan)
- Utility functions (youtube, mindmap)

### When to Use Agents

- Domain expertise needed (Spark, Fabric)
- Complex multi-step tasks (code review)
- Specialized knowledge (healthcare billing)
- Planning and architecture

---

## Best Practices

### SKILL.md Guidelines

1. **Keep under 500 lines** - Skills should be focused
2. **Clear triggers** - Explicit activation conditions
3. **Actionable content** - Commands, checklists, patterns
4. **No overlap** - Don't duplicate agent functionality

### Skill Design Principles

- **Single responsibility** - One workflow per skill
- **Context-aware** - Activate only when relevant
- **Complementary** - Work with agents, not replace
- **Minimal footprint** - Don't bloat context
