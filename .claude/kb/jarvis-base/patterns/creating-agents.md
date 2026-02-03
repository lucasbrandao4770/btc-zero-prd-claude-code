# Creating Agents Pattern

> **MCP Validated:** 2026-02-01

---

## Overview

This pattern describes how to create new agents for the Jarvis system.

---

## Step 1: Choose Category

Select the appropriate category for your agent:

| Category | Use For |
|----------|---------|
| ai | AI/ML, LLM, prompt engineering |
| automation | Workflow, orchestration |
| career | Job applications, resumes |
| communication | Explanations, presentations |
| core | System-level agents |
| data | Data platforms (Airflow, Lakeflow) |
| engineering | Code quality, review |
| exploration | Codebase analysis |
| fabric | Microsoft Fabric |
| faturamento | Healthcare billing |
| meta | System management |
| personal | User-specific tasks |
| planning | Strategic/tactical planning |
| scientific-research | Academic work |
| spark | Apache Spark |
| ui | Frontend, UI prototyping |

---

## Step 2: Create Agent File

Create `agents/{category}/{agent-name}.md`.

### Minimal Template

```markdown
---
name: agent-name
description: One-line description of what this agent does
tools: Read, Write, Edit, Grep, Glob, Bash
---

# Agent Name

You are {agent-name}, a specialist in [domain].

## When to Use

- Trigger condition 1
- Trigger condition 2

## Capabilities

- Capability 1
- Capability 2

## Usage

[Example usage instructions]
```

### Full Template

```markdown
---
name: agent-name
description: One-line description
tools: Read, Write, Edit, Grep, Glob, Bash, Task, mcp__*
model: sonnet
proactive: true
---

# Agent Name

You are {agent-name}, [detailed description of role and expertise].

## Core Philosophy

[Key principles guiding agent behavior]

---

## Your Knowledge Base

[What KB or documentation this agent uses]

---

## Capabilities

### Capability 1: [Name]

**Description:** What it does
**When to use:** Trigger conditions
**Checklist:**
- [ ] Item 1
- [ ] Item 2

### Capability 2: [Name]

...

---

## Execution Patterns

### Pattern 1: [Name]

```
User: "[typical request]"

Step 1: [action]
Step 2: [action]
Step 3: [action]

Response: "[example response]"
```

---

## Best Practices

### Always Do
1. ...
2. ...

### Never Do
1. ...
2. ...

---

## Remember

[Mission statement or key takeaway]
```

---

## Step 3: Choose Tools

Select minimal necessary tools:

### Core Tools

| Tool | Purpose | When to Include |
|------|---------|-----------------|
| Read | Read files | Almost always |
| Write | Create files | If agent creates content |
| Edit | Modify files | If agent modifies code |
| Grep | Search content | If agent searches |
| Glob | Find files | If agent explores |
| Bash | Run commands | If agent needs shell |
| Task | Spawn agents | If agent orchestrates |

### MCP Tools

| Pattern | Purpose |
|---------|---------|
| `mcp__upstash-context-7-mcp__*` | Library documentation |
| `mcp__exa__*` | Code examples |
| `mcp__cclsp__*` | LSP code intelligence |
| `mcp__krieg-2065-firecrawl-mcp-server__*` | Web scraping |

### Tool Access Examples

```yaml
# Explorer (read-only)
tools: Read, Grep, Glob

# Developer (full access)
tools: Read, Write, Edit, Bash, Grep, Glob

# Reviewer (read + LSP)
tools: Read, Grep, Glob, mcp__cclsp__*

# Researcher (read + MCPs)
tools: Read, WebSearch, WebFetch, mcp__exa__*, mcp__upstash-context-7-mcp__*

# Orchestrator (full + Task)
tools: Read, Write, Edit, Bash, Grep, Glob, Task
```

---

## Step 4: Update Catalog

Add agent to `catalogs/agents-catalog.yaml`:

```yaml
categories:
  {category}:
    agents:
      # ... existing agents ...

      - name: agent-name
        path: {category}/agent-name.md
        description: "One-line description"
        proactive: true  # or false
        tools:
          - Read
          - Write
          - Edit
```

---

## Step 5: Validate

### Validation Checklist

- [ ] **Frontmatter complete** - name, description, tools present
- [ ] **Clear triggers** - When should this agent be used?
- [ ] **Defined capabilities** - What can this agent do?
- [ ] **Usage examples** - How to use this agent?
- [ ] **Minimal tools** - Only necessary tools included
- [ ] **No overlap** - Doesn't duplicate existing agents
- [ ] **Catalog updated** - Entry in agents-catalog.yaml

### Testing

```bash
# Test invocation
Task(subagent_type="agent-name", prompt="Test the agent")
```

---

## Examples

### Simple Agent (code-cleaner)

```markdown
---
name: code-cleaner
description: Python code cleaning, DRY principles, modernization
tools: Read, Write, Edit, Grep, Glob, Bash
---

# Code Cleaner

You are code-cleaner, a Python code quality specialist.

## When to Use

- Before committing Python code
- User mentions "clean up" or "refactor"
- Code review identifies quality issues

## Capabilities

- Apply DRY principles
- Modernize Python syntax
- Improve code organization
- Add type hints and docstrings

## Workflow

1. Analyze current code structure
2. Identify improvement areas
3. Apply changes incrementally
4. Verify with ruff check
```

### Complex Agent (code-reviewer)

See `agents/engineering/code-reviewer.md` for a comprehensive example including:
- Severity classification
- Multiple capabilities
- MCP integration
- Execution patterns
- Report format

---

## Anti-Patterns

### Avoid These Mistakes

| Anti-Pattern | Why It's Bad | Do Instead |
|--------------|--------------|------------|
| Generic description | Unclear when to use | Specific, actionable description |
| All tools enabled | Security risk | Minimal necessary tools |
| No triggers | Unclear invocation | Explicit trigger conditions |
| Duplicate functionality | Confusion | Use existing agent or merge |
| Missing examples | Hard to use | Include usage examples |
| Too long (>500 lines) | Hard to maintain | Split into multiple agents |
