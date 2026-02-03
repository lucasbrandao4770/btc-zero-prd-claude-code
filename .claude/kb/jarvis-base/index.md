# Jarvis Base Knowledge Base

> **MCP Validated:** 2026-02-01
> **Source Repository:** `D:\Workspace\Claude Code\Repositorios\claude-agents`

This KB provides essential context for understanding and extending the Jarvis AI Operations Hub - a comprehensive framework for agents, knowledge bases, personalities, and automation built on Claude Code.

---

## Quick Navigation

| Topic | File | Purpose |
|-------|------|---------|
| **Architecture** | [concepts/architecture.md](concepts/architecture.md) | System structure and component interaction |
| **Agents** | [concepts/agents.md](concepts/agents.md) | Agent system, structure, invocation |
| **Skills** | [concepts/skills.md](concepts/skills.md) | Auto-activating skills system |
| **Hooks** | [concepts/hooks.md](concepts/hooks.md) | Event hooks (PreToolUse, StatusLine, etc.) |
| **Configuration** | [concepts/configuration.md](concepts/configuration.md) | settings.json, CLAUDE.md, rules |
| **Creating Agents** | [patterns/creating-agents.md](patterns/creating-agents.md) | How to create new agents |
| **Creating Skills** | [patterns/creating-skills.md](patterns/creating-skills.md) | How to create new skills |
| **Hook Patterns** | [patterns/hook-patterns.md](patterns/hook-patterns.md) | Common hook implementations |
| **Quick Reference** | [quick-reference.md](quick-reference.md) | Cheat sheet for common operations |

---

## Repository Structure

```
claude-agents/
|-- CLAUDE.md                  # Main instruction file (user-level)
|-- README.md                  # Repository readme
|-- agents/                    # 44 specialized agents (18 categories)
|   |-- ai/                    # AI/ML specialists (8 agents)
|   |-- automation/            # Workflow automation (3)
|   |-- career/                # Job applications (4)
|   |-- communication/         # Explanations, planning (3)
|   |-- core/                  # Jarvis, planner, onboarding (3)
|   |-- data/                  # Airflow, Lakeflow (2)
|   |-- engineering/           # Code quality (3)
|   |-- exploration/           # Codebase exploration (2)
|   |-- fabric/                # Microsoft Fabric (6)
|   |-- faturamento/           # Healthcare billing (5)
|   |-- finance/               # Finance specialist (1)
|   |-- meta/                  # KB creator (1)
|   |-- personal/              # Taiwan supervisor (1)
|   |-- planning/              # 3-phase planning (3)
|   |-- scientific-research/   # Academic research (7)
|   |-- spark/                 # Apache Spark (4)
|   `-- ui/                    # UI prototyping (1)
|
|-- catalogs/                  # System inventories
|   |-- agents-catalog.yaml    # Full agent registry
|   |-- agents-summary.yaml    # Compact agent list (~200 tokens)
|   |-- skills-catalog.yaml    # Full skill registry
|   |-- skills-summary.yaml    # Compact skill list (~100 tokens)
|   |-- commands-catalog.yaml  # Slash commands
|   `-- kb-catalog.md          # Knowledge base index
|
|-- commands/                  # Custom slash commands
|   |-- jarvis.md              # Main /jarvis entry point
|   |-- jarvis/                # Session commands (morning, resume, exit, etc.)
|   |-- sandbox/               # Sandbox commands
|   |-- sensei/                # Learning commands
|   |-- system/                # Config commands (menu, personality, profile)
|   `-- workflow/              # Sprint/task commands
|
|-- docs/                      # Architecture documentation
|-- hooks/                     # Event hook scripts (bash)
|-- integrations/              # MCP setup guides
|-- jarvis-crud/               # SQLite data management CLI
|-- kb/                        # Knowledge bases (14 domains)
|-- modes/                     # Interactive mode definitions
|-- personalities/             # Output formatting styles
|-- rules/                     # Auto-loading behavior rules
|-- skills/                    # Auto-activating skill definitions
`-- templates/                 # Config and workflow templates
```

---

## Key Entry Points

### Starting Jarvis

| Entry | What It Does |
|-------|--------------|
| `claude --agent jarvis` | Start dedicated Jarvis session |
| `/jarvis` | Activate Jarvis mode in existing session |
| `/jarvis:morning` | Morning briefing with priorities |
| `/jarvis:resume` | Resume from last session |
| `/jarvis:exit` | Save state and exit |

### Agent Invocation

Agents are invoked via the Task tool:

```python
# Direct agent invocation
Task(subagent_type="code-reviewer", prompt="Review the changes")

# Agent file loaded from agents/{category}/{name}.md
```

### Skill Activation

Skills auto-activate based on context triggers - no manual invocation needed.

---

## Component Relationships

```
                    CLAUDE.md (User Instructions)
                            |
            /--------------+---------------\
           v               v                v
       /jarvis         Agents            Skills
       command         (Task)           (auto-activate)
           |               |                |
           v               v                v
      jarvis-mode     Agent File        SKILL.md
           |          (agents/*.md)     (skills/*/SKILL.md)
           |               |                |
           |      +--------+--------+       |
           v      v                 v       v
         Rules         Hooks          jarvis-crud
    (rules/*.md)   (hooks/*.sh)       (SQLite DB)
```

---

## Data Flow

**User Data:** All persistent data goes through `jarvis-crud` CLI to SQLite database at `~/.claude/jarvis/jarvis.db`.

**Static Files:** Personalities, modes, and plans can be read directly.

**Session State:** Managed by hooks (SessionStart, PreCompact, Stop).

---

## Related Documentation

- **Full CLAUDE.md:** `D:\Workspace\Claude Code\Repositorios\claude-agents\CLAUDE.md`
- **Agent Catalog:** `D:\Workspace\Claude Code\Repositorios\claude-agents\catalogs\agents-catalog.yaml`
- **Skills Catalog:** `D:\Workspace\Claude Code\Repositorios\claude-agents\catalogs\skills-catalog.yaml`
- **System Overview:** `D:\Workspace\Claude Code\Repositorios\claude-agents\docs\system-overview.md`
