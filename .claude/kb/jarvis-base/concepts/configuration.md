# Jarvis Configuration

> **MCP Validated:** 2026-02-01

---

## Configuration Hierarchy

```
Priority (highest to lowest):
1. Project settings.local.json  (.claude/settings.local.json)
2. User settings.json           (~/.claude/settings.json)
3. CLAUDE.md (project)          (.claude/CLAUDE.md)
4. CLAUDE.md (user)             (~/.claude/CLAUDE.md)
5. Rules (rules/*.md)
```

---

## settings.json Structure

### Location

- **User-level:** `~/.claude/settings.json`
- **Project-level:** `.claude/settings.local.json`

### Full Structure

```json
{
  "permissions": {
    "allow": [
      "Bash(jarvis-crud:*)",
      "Bash(cat:*)",
      "mcp__upstash-context-7-mcp__*"
    ]
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["shadcn"],
  "hooks": {
    "PreToolUse": [...],
    "UserPromptSubmit": [...],
    "PreCompact": [...],
    "Stop": [...]
  },
  "statusLine": {
    "type": "command",
    "command": "bash /path/to/statusline.sh"
  },
  "outputStyle": "Explanatory",
  "plansDirectory": "~/.claude/jarvis/plans"
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `permissions.allow` | Pre-approved tool commands |
| `enableAllProjectMcpServers` | Enable MCP servers |
| `enabledMcpjsonServers` | Specific MCP servers to enable |
| `hooks` | Event hook configuration |
| `statusLine` | Status bar script |
| `outputStyle` | Response style preference |
| `plansDirectory` | Where plans are stored |

---

## CLAUDE.md Patterns

CLAUDE.md is the main instruction file loaded at session start.

### Location

- **User-level:** `~/.claude/CLAUDE.md`
- **Project-level:** `{project}/.claude/CLAUDE.md`

### Typical Structure

```markdown
# Project Name

> One-line description

---

## Quick Start

[Key commands and entry points]

---

## Context Window Optimization

[R&D Framework rules]

---

## Capability Awareness

### Agents
[Available agents by category]

### Skills
[Auto-activated skills]

### MCPs
[Available MCP tools]

### Knowledge Bases
[Available KBs]

---

## Repository Structure

[Directory tree]

---

## Rules System

[Modular rules overview]

---

## Mode System

[Available modes and commands]

---

## Critical Rules (Non-Negotiable)

[Mandatory behavior rules]

---

## Code Standards

[Language and style requirements]
```

### User vs Project CLAUDE.md

| User CLAUDE.md | Project CLAUDE.md |
|----------------|-------------------|
| Personal preferences | Project-specific rules |
| Cross-project settings | Architecture details |
| Jarvis configuration | Technology stack |
| General capabilities | Project structure |

---

## Rules System

Rules are modular instruction files that auto-load based on context.

### Location

`rules/*.md` in the repository root.

### Available Rules

| Rule | Purpose | Applies To |
|------|---------|------------|
| `core-principles.md` | Problem-solving workflow | All work |
| `planning-workflow.md` | Planner usage | Complex tasks |
| `context7-integration.md` | When to use Context7 | Library work |
| `agent-quality.md` | Agent standards | `agents/**/*.md` |
| `python-standards.md` | Python code style | `*.py` |
| `lsp-integration.md` | LSP usage | Code navigation |
| `data-access-rules.md` | jarvis-crud usage | Data access |
| `personalization.md` | Personality system | Output formatting |

### Rule File Structure

```markdown
---
description: One-line description
priority: 100  # Higher = more important
---

# Rule Title

## Section 1
[Instructions]

## Section 2
[Instructions]
```

---

## Mode System

Modes are specialized interactive experiences activated by commands.

### Mode Files

Located in `modes/{name}-mode.md`.

### Mode Structure

```markdown
# Mode Name

**CANARY:** MODE_PROTOCOL_v1

**Activated by:** /command
**Purpose:** What this mode does

---

## YOU ARE [PERSONA]

[Identity and behavior rules]

---

## CRITICAL RULES

[Mandatory behavior]

---

## Data Access

[What data to load]

---

## Capabilities

[What this mode can do]
```

### Available Modes

| Mode | Command | Canary |
|------|---------|--------|
| Jarvis | `/jarvis` | `JARVIS_PROTOCOL_v1` |
| Sensei | `/sensei` | `SENSEI_PROTOCOL_v2` |
| Taiwan | `/taiwan` | `GUARDIAN_PROTOCOL_v2` |
| Sandbox | `/sandbox` | `SANDBOX_PROTOCOL_v2` |
| Planner | `/planner` | `JARVIS_PLANNER_v1` |
| GenAI | `/genai` | `GENAI_ARCHITECT_PROTOCOL_v1` |
| Fabric | `/fabric` | `FABRIC_ARCHITECT_PROTOCOL_v1` |
| PM | `/pm` | `LINEAR_PM_PROTOCOL_v1` |

### Canary Verification

Modes use canary tokens to verify activation:

```markdown
**CANARY:** JARVIS_PROTOCOL_v1

[Claude must confirm seeing this canary to verify mode loaded]
```

---

## jarvis-crud Data Layer

All user data goes through `jarvis-crud` CLI.

### Database Location

`~/.claude/jarvis/jarvis.db` (SQLite)

### Key Operations

```bash
# Configuration
jarvis-crud config get
jarvis-crud config update --json '{"key": "value"}'

# Session
jarvis-crud session get
jarvis-crud session save --json '{"summary": "..."}'

# Sprint
jarvis-crud sprint get
jarvis-crud sprint tasks list

# Goals
jarvis-crud goals list
jarvis-crud goals create --json '{"title": "..."}'

# Context (compound operations)
jarvis-crud context startup    # All startup data
jarvis-crud context resume     # Resume data
jarvis-crud context briefing   # Morning briefing
```

### Data Structure

```json
{
  "profile": {
    "name": "User Name",
    "title": "Title",
    "experience_level": "intermediate"
  },
  "preferences": {
    "verbosity": "balanced",
    "context_threshold": 80
  },
  "personality": {
    "default": "chip-wmw"
  },
  "workflow": {
    "sprints_enabled": true
  },
  "language": "en"
}
```

---

## Permissions

### Pre-Approved Commands

```json
{
  "permissions": {
    "allow": [
      "Bash(jarvis-crud:*)",     // All jarvis-crud commands
      "Bash(cat:*)",             // All cat commands
      "mcp__context7__*"         // All Context7 tools
    ]
  }
}
```

### Pattern Syntax

| Pattern | Matches |
|---------|---------|
| `Bash(cmd:*)` | All args to cmd |
| `Bash(cmd)` | Exact command |
| `mcp__server__*` | All tools from server |
| `mcp__server__tool` | Specific tool |

---

## Directory Structure Summary

```
~/.claude/                      # User directory
|-- CLAUDE.md                   # User instructions
|-- settings.json               # User settings
|-- jarvis/
|   |-- jarvis.db               # SQLite database
|   |-- sessions/               # Session caches
|   |-- plans/                  # Plan files
|   `-- hooks.log               # Hook logs
|-- jarvis-base/                # Symlink to repo (optional)
|-- agents/                     # Symlink to repo/agents
|-- skills/                     # Symlink to repo/skills
`-- commands/                   # Symlink to repo/commands

{project}/.claude/              # Project directory
|-- CLAUDE.md                   # Project instructions
`-- settings.local.json         # Project settings
```
