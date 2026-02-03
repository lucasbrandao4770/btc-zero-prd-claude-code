# Jarvis Architecture

> **MCP Validated:** 2026-02-01

---

## System Overview

Jarvis is an AI assistant framework built on Claude Code that provides:

- **44 Specialized Agents** - Domain experts for various tasks
- **30 Auto-Activating Skills** - Workflow automation based on context
- **14 Knowledge Bases** - Grounded domain knowledge
- **7 Personalities** - Switchable output formatting styles
- **Mode System** - Specialized interactive modes (Jarvis, Sensei, Taiwan, etc.)
- **Hook System** - Event-driven customization

---

## Directory Structure

```
claude-agents/
|
|-- CLAUDE.md              # Main instruction file (loaded at session start)
|-- README.md              # Repository documentation
|
|-- agents/                # Specialized subagents (44 total)
|   |-- ai/                # AI/ML specialists (8)
|   |-- automation/        # Workflow automation (3)
|   |-- career/            # Job applications (4)
|   |-- communication/     # Explanations, planning (3)
|   |-- core/              # Jarvis, planner, onboarding (3)
|   |-- data/              # Airflow, Lakeflow (2)
|   |-- engineering/       # Code quality (3)
|   |-- exploration/       # Codebase exploration (2)
|   |-- fabric/            # Microsoft Fabric (6)
|   |-- faturamento/       # Healthcare billing (5)
|   |-- finance/           # Finance (1)
|   |-- meta/              # KB creator (1)
|   |-- personal/          # Taiwan supervisor (1)
|   |-- planning/          # 3-phase planning (3)
|   |-- scientific-research/  # Academic (7)
|   |-- spark/             # Apache Spark (4)
|   `-- ui/                # UI prototyping (1)
|
|-- skills/                # Auto-activating skills (30 total)
|   |-- code-quality/      # Ruff, type hints, docstrings
|   |-- git-workflow/      # Conventional commits
|   |-- context7-research/ # Documentation lookup
|   |-- testing/           # Pytest patterns
|   |-- planning/          # Session chunking
|   |-- sandbox/           # Isolated execution
|   `-- ...                # Many more
|
|-- modes/                 # Interactive mode definitions
|   |-- jarvis-mode.md     # Main Jarvis mode
|   |-- sensei-mode.md     # Learning mode
|   |-- taiwan-mode.md     # Taiwan applications
|   |-- sandbox-mode.md    # Autonomous execution
|   `-- ...
|
|-- commands/              # Custom slash commands
|   |-- jarvis.md          # Main /jarvis command
|   |-- jarvis/            # Sub-commands (morning, resume, exit, etc.)
|   |-- sensei/            # /sensei commands
|   `-- system/            # /system commands
|
|-- rules/                 # Auto-loading behavior rules
|   |-- core-principles.md # Problem-solving workflow
|   |-- planning-workflow.md
|   |-- context7-integration.md
|   |-- python-standards.md
|   `-- ...
|
|-- hooks/                 # Event hook scripts
|   |-- pre-tool-use.sh    # PreToolUse hook
|   |-- statusline.sh      # StatusLine hook
|   |-- session-start.sh   # SessionStart hook
|   |-- pre-compact.sh     # PreCompact hook
|   |-- user-prompt-submit.sh
|   `-- stop.sh
|
|-- catalogs/              # System inventories
|   |-- agents-catalog.yaml
|   |-- skills-catalog.yaml
|   |-- commands-catalog.yaml
|   `-- kb-catalog.md
|
|-- kb/                    # Knowledge bases (14 domains)
|-- personalities/         # Output formatting styles
|-- jarvis-crud/           # SQLite data management CLI
|-- templates/             # Config templates
`-- docs/                  # Architecture documentation
```

---

## Component Interaction Flow

```
                          User Session
                               |
                               v
                     +------------------+
                     |    CLAUDE.md     |  <-- Loaded at session start
                     +------------------+
                               |
         +--------------------+--------------------+
         |                    |                    |
         v                    v                    v
   +-----------+        +-----------+        +-----------+
   |  /jarvis  |        |  Skills   |        |   Rules   |
   |  command  |        | (auto)    |        | (auto)    |
   +-----------+        +-----------+        +-----------+
         |                    |                    |
         v                    v                    v
   +-----------+        +-----------+        +-----------+
   |   Mode    |        |  SKILL.md |        |  rule.md  |
   |   File    |        |  triggers |        |  applies  |
   +-----------+        +-----------+        +-----------+
         |
         v
   +-----------+
   |  Agents   |  <-- Spawned via Task tool
   |  (Task)   |
   +-----------+
         |
         v
   +-----------+
   | jarvis-   |  <-- Data persistence
   |   crud    |
   +-----------+
         |
         v
   +-----------+
   |  SQLite   |
   |    DB     |
   +-----------+
```

---

## Key Architectural Concepts

### 1. Native First, Complementary Enhancements

Jarvis leverages Claude Code's native features:
- Native `/agents` command for agent management
- Native memory/context for session persistence
- Native skills for workflow automation
- Custom components complement, not replace, native features

### 2. Two-Tier Catalog Loading

To optimize context window usage:
- **Startup:** Load compact summaries (~300 tokens total)
- **On-Demand:** Load full catalogs only when needed

```yaml
# Startup: agents-summary.yaml (~200 tokens)
# Startup: skills-summary.yaml (~100 tokens)

# On-demand: agents-catalog.yaml (~4,000 tokens)
# On-demand: skills-catalog.yaml (~3,500 tokens)
```

### 3. R&D Framework (Reduce + Delegate)

Context window optimization strategy:

**Reduce:** Minimize tokens entering main context
- Use Explore subagent for codebase exploration
- Load file contents on-demand
- Summarize research results before returning

**Delegate:** Push work to subagents
- Research tasks -> Explore subagent
- Multi-file analysis -> Task with parallelism
- Specialized work -> Domain agents

### 4. Data Access Layer

All user data goes through `jarvis-crud` CLI:

```bash
# CORRECT: Use jarvis-crud
jarvis-crud config get
jarvis-crud session save --json '{...}'

# WRONG: Direct file access
Read tool -> config.yaml  # FORBIDDEN
```

---

## Entry Points

| Entry | Purpose | Loads |
|-------|---------|-------|
| `claude --agent jarvis` | Direct Jarvis session | Agent file |
| `/jarvis` | Activate Jarvis mode | jarvis-mode.md |
| `/jarvis:morning` | Morning briefing | commands/jarvis/morning.md |
| `/jarvis:resume` | Resume session | commands/jarvis/resume.md |
| `/sensei` | Learning mode | sensei-mode.md |
| `/sandbox` | Autonomous mode | sandbox-mode.md |

---

## Session State Management

Session state is managed through hooks:

1. **SessionStart hook** - Initializes session cache with jarvis-crud data
2. **UserPromptSubmit hook** - Processes each user message
3. **PreCompact hook** - Preserves state before auto-compact
4. **Stop hook** - Saves final session state

State persisted in:
- `~/.claude/jarvis/jarvis.db` - SQLite database (primary)
- `~/.claude/jarvis/sessions/{session_id}/cache.json` - Session cache
