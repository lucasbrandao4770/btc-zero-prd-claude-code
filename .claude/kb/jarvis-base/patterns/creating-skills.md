# Creating Skills Pattern

> **MCP Validated:** 2026-02-01

---

## Overview

Skills are auto-activating workflow modules. Unlike agents (invoked explicitly), skills activate automatically based on context triggers.

---

## Step 1: Identify Skill Need

Ask yourself:
- Is this a **recurring workflow** (not one-time task)?
- Should it activate **automatically** (not manually invoked)?
- Does it provide **patterns/commands** (not execute complex tasks)?

If yes to all, create a skill. Otherwise, consider an agent.

---

## Step 2: Choose Category

| Category | Use For |
|----------|---------|
| code-quality | Linting, formatting, testing |
| version-control | Git workflows |
| research | Documentation lookup |
| workflow | Planning, organization |
| automation | Sandbox, parallel processing |
| frontend | UI generation, prototyping |
| modes | Domain-specific modes |
| utilities | YouTube, mindmap, reports |
| career | Job applications |

---

## Step 3: Create Skill Directory

```bash
mkdir -p skills/{skill-name}
touch skills/{skill-name}/SKILL.md
```

---

## Step 4: Write SKILL.md

### Minimal Template

```markdown
---
name: skill-name
description: Description of what this skill does and when it activates.
---

# Skill Name

## When This Skill Activates

- Trigger 1
- Trigger 2
- Trigger 3

## What This Skill Provides

[Instructions, patterns, commands]
```

### Full Template

```markdown
---
name: skill-name
description: Multi-line description explaining what the skill does, when it activates, and what value it provides to the user.
---

# Skill Name

## When This Skill Activates

- Trigger condition 1 (file type, user phrase, context)
- Trigger condition 2
- Trigger condition 3

## Prerequisites

[What needs to be in place before using this skill]

## Workflow

### Step 1: [Name]

[Instructions]

```bash
# Example command
```

### Step 2: [Name]

[Instructions]

### Step 3: [Name]

[Instructions]

## Quick Commands

| Action | Command |
|--------|---------|
| Action 1 | `command 1` |
| Action 2 | `command 2` |

## Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Common Patterns

### Pattern 1: [Name]

[Description and example]

### Pattern 2: [Name]

[Description and example]

## Related

- [Agent Name](../agents/...) - For complex tasks
- [Other Skill](./other-skill/) - Related workflow
```

---

## Step 5: Define Triggers

Triggers determine when the skill activates. Be specific.

### Good Triggers

```yaml
activates_when:
  - Python files (.py) created or modified      # Specific file type
  - User mentions: quality, lint, format        # Specific keywords
  - Preparing for git commit                    # Specific action
  - User mentions quality, lint, format, type check  # Related terms
```

### Bad Triggers

```yaml
activates_when:
  - User asks for help           # Too vague
  - Any Python work              # Too broad
  - Coding tasks                 # Not specific
```

---

## Step 6: Update Catalog

Add to `catalogs/skills-catalog.yaml`:

```yaml
skills:
  # ... existing skills ...

  - name: skill-name
    path: ~/.claude/skills/skill-name/SKILL.md
    category: category-name
    description: |
      Multi-line description of what this skill does.
    activates_when:
      - Trigger 1
      - Trigger 2
    provides:
      - What it gives 1
      - What it gives 2
    added: "2026-02-01"
```

---

## Step 7: Validate

### Validation Checklist

- [ ] **Frontmatter complete** - name, description present
- [ ] **Clear triggers** - When does this skill activate?
- [ ] **Actionable content** - Commands, checklists, patterns
- [ ] **Under 500 lines** - Focused, not bloated
- [ ] **No agent overlap** - Doesn't duplicate agent functionality
- [ ] **Catalog updated** - Entry in skills-catalog.yaml

### Testing

Perform an action that should trigger the skill and verify it activates.

---

## Examples

### Simple Skill (git-workflow)

```markdown
---
name: git-workflow
description: Git workflow automation. Activates when git operations mentioned (commit, push, branch, merge), preparing for version control, or creating PRs.
---

# Git Workflow

## When This Skill Activates

- Git operations mentioned (commit, push, branch, merge)
- Preparing code for version control
- Creating pull requests

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

### Types

| Type | When |
|------|------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| refactor | Code restructure |
| test | Tests |
| chore | Maintenance |

## Quick Commands

| Action | Command |
|--------|---------|
| Status | `git status` |
| Stage all | `git add .` |
| Commit | `git commit -m "type: description"` |
| Push | `git push origin branch` |
```

### Mode-Activating Skill (sensei)

```markdown
---
name: sensei
description: Interactive learning sessions. Activates when user says "teach me", "learn about", "quiz me", or mentions practice/preparation.
---

# Sensei Skill

## When This Skill Activates

- User says "teach me", "learn about", "explain"
- "Quiz me", "test my knowledge"
- "Practice" or "prepare for" something

## Mode Activation

When triggered, load Sensei Mode:

1. Read `modes/sensei-mode.md`
2. Confirm canary: `SENSEI_PROTOCOL_v2`
3. Begin interactive learning session

## Session Types

| Type | Purpose |
|------|---------|
| Lesson | Teach new concept |
| Quiz | Test knowledge |
| Practice | Apply learning |
| Review | Spaced repetition |
```

---

## Skills vs Agents Decision

| Question | Skill | Agent |
|----------|-------|-------|
| Auto-activate on context? | Yes | No |
| Provide patterns/commands? | Yes | Maybe |
| Execute complex tasks? | No | Yes |
| Domain expertise needed? | No | Yes |
| Workflow automation? | Yes | No |
| Single responsibility? | Yes | Maybe |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|--------------|--------------|------------|
| Too many triggers | Always active | Specific triggers |
| Vague triggers | Unpredictable | Explicit conditions |
| Over 500 lines | Context bloat | Split or simplify |
| Duplicates agent | Confusion | Use agent instead |
| No actionable content | Useless | Add commands/checklists |
| No catalog entry | Undiscoverable | Update catalog |
