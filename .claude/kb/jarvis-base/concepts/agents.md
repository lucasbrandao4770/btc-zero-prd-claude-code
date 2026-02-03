# Jarvis Agent System

> **MCP Validated:** 2026-02-01

---

## Overview

Agents are specialized AI personas that can be invoked via the Task tool. Each agent has:
- A specific domain expertise
- Defined tool access
- Trigger conditions
- Usage instructions

---

## Agent File Structure

Agents are markdown files with YAML frontmatter located in `agents/{category}/{name}.md`.

### Required Frontmatter

```yaml
---
name: agent-name
description: One-line description of what the agent does
tools: Read, Write, Edit, Grep, Glob, Bash, Task
---
```

### Optional Frontmatter Fields

```yaml
---
name: agent-name
description: Description
tools: [List, Of, Tools]
model: sonnet                    # Default model (sonnet, opus, haiku)
proactive: true                  # Can be auto-invoked by Jarvis
cli_access: true                 # Can be used with claude --agent
deprecated: true                 # Mark as deprecated
redirect: "path/to/replacement"  # Redirect to new agent
---
```

### Full Agent File Example

```markdown
---
name: code-reviewer
description: Expert code review specialist ensuring quality, security, and maintainability.
tools: Read, Write, Edit, Grep, Glob, Bash, mcp__exa__*, mcp__cclsp__*
---

# Agent Name

You are {agent-name}, a [brief description].

## When to Use

[Trigger conditions when this agent should be invoked]

## Core Philosophy

[Key principles guiding the agent's behavior]

## Capabilities

### Capability 1: [Name]

**Description:** [What it does]
**When to use:** [Trigger conditions]
**Checklist:** [Items to verify]

### Capability 2: [Name]
...

## Execution Patterns

[Common usage patterns]

## Best Practices

[Do's and Don'ts]

## Remember

[Key takeaway or mission statement]
```

---

## Tool Access Patterns

### Common Tool Combinations

| Agent Type | Typical Tools |
|------------|---------------|
| Explorer | Read, Grep, Glob |
| Developer | Read, Write, Edit, Bash |
| Reviewer | Read, Grep, Glob, mcp__cclsp__* |
| Researcher | WebSearch, WebFetch, mcp__exa__* |
| Planner | Read, Glob, Grep, AskUserQuestion |
| Full Access | Read, Write, Edit, Bash, Task, Grep, Glob, WebSearch, mcp__* |

### MCP Tool Patterns

```yaml
# Context7 - Library documentation
tools: mcp__upstash-context-7-mcp__*

# Exa - Code search
tools: mcp__exa__*

# LSP - Code intelligence
tools: mcp__cclsp__*

# Firecrawl - Web scraping
tools: mcp__krieg-2065-firecrawl-mcp-server__*

# Multiple MCPs
tools: mcp__upstash-context-7-mcp__*, mcp__exa__*, mcp__cclsp__*
```

---

## Agent Invocation

### Via Task Tool

```python
# Basic invocation
Task(subagent_type="code-reviewer", prompt="Review the changes in src/")

# With specific instructions
Task(
    subagent_type="spark-specialist",
    prompt="Analyze the Spark job for performance issues"
)
```

### Via CLI (for agents with cli_access: true)

```bash
claude --agent jarvis
claude --agent sensei "Teach me Python decorators"
claude --agent planner "Design a REST API"
```

### Auto-Invocation by Jarvis

When `proactive: true`, Jarvis can automatically spawn the agent:

```markdown
## Agent Delegation (from jarvis-mode.md)

| User Mentions | Agent to Invoke |
|---------------|-----------------|
| "sandbox", "YOLO" | sandbox |
| "plan", "design" | planner |
| After writing code | code-reviewer |
| "learn", "teach" | sensei |
```

---

## Agent Categories

### Core (3 agents)

| Agent | Purpose |
|-------|---------|
| jarvis | Main AI assistant with personality |
| planner | Strategic planning (deprecated) |
| onboarding-guide | New user setup |

### Planning (3 agents)

| Agent | Phase | Purpose |
|-------|-------|---------|
| strategic-architect | 1 | Requirements discovery |
| tactical-architect | 2 | Language-agnostic design |
| operational-planner | 3 | KB-grounded code patterns |

### Engineering (3 agents)

| Agent | Purpose |
|-------|---------|
| code-reviewer | Quality, security, maintainability |
| code-cleaner | DRY principles, modernization |
| code-documenter | READMEs and API docs |

### AI (8 agents)

| Agent | Purpose |
|-------|---------|
| sensei | Interactive learning |
| genai-architect | Multi-agent AI systems |
| llm-specialist | Prompt engineering |
| dify-specialist | Dify platform |
| data-engineer | GCP data engineering |
| prompt-specialist | Gemini/Vertex AI prompts |

### Exploration (2 agents)

| Agent | Purpose |
|-------|---------|
| codebase-explorer | Codebase analysis |
| kb-architect | Knowledge base creation |

---

## Agent Catalog

The authoritative list is in `catalogs/agents-catalog.yaml`:

```yaml
categories:
  planning:
    description: "3-Phase Planning System"
    agents:
      - name: strategic-architect
        path: planning/strategic-architect.md
        description: "Phase 1 - Requirements discovery"
        proactive: true
        phase: 1
        tools: Read, Glob, Grep, WebSearch, mcp__*
```

### Catalog Fields

| Field | Description |
|-------|-------------|
| `name` | Agent identifier (used in Task tool) |
| `path` | File location relative to agents/ |
| `description` | What the agent does |
| `proactive` | Can be auto-invoked |
| `cli_access` | Can use `claude --agent` |
| `tools` | Available tools |
| `deprecated` | Should not be used |
| `redirect` | Replacement agent |

---

## Agent Quality Standards

From `rules/agent-quality.md`:

### Required Structure

1. YAML frontmatter with name, description, tools
2. Clear trigger conditions
3. Defined capabilities
4. Usage examples

### Validation Checklist

- [ ] Clear, specific description
- [ ] Appropriate tool access (minimal needed)
- [ ] Defined trigger conditions
- [ ] Usage examples provided
- [ ] No overlap with existing agents

### Anti-Patterns

- Generic descriptions ("helps with tasks")
- Excessive tool access
- Missing trigger conditions
- Overlapping with existing agents
