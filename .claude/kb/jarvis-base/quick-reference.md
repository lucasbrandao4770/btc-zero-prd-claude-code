# Jarvis Quick Reference

> **MCP Validated:** 2026-02-01

---

## File Locations

| Component | Path Pattern | Example |
|-----------|--------------|---------|
| Agents | `agents/{category}/{name}.md` | `agents/engineering/code-reviewer.md` |
| Skills | `skills/{name}/SKILL.md` | `skills/code-quality/SKILL.md` |
| Modes | `modes/{name}-mode.md` | `modes/jarvis-mode.md` |
| Commands | `commands/{category}/{name}.md` | `commands/jarvis/morning.md` |
| Rules | `rules/{name}.md` | `rules/core-principles.md` |
| Hooks | `hooks/{hook-name}.sh` | `hooks/statusline.sh` |
| Settings | `.claude/settings.local.json` | Project settings |
| User Settings | `~/.claude/settings.json` | User-level settings |

---

## Agent Frontmatter Template

```yaml
---
name: agent-name
description: One-line description of what the agent does
tools: Read, Write, Edit, Grep, Glob, Bash, Task, mcp__*
---
```

**Common Tools:**
- `Read, Write, Edit, Grep, Glob, Bash` - Core file operations
- `Task` - Spawn subagents
- `WebSearch, WebFetch` - Web access
- `mcp__upstash-context-7-mcp__*` - Context7 documentation
- `mcp__exa__*` - Exa code search
- `mcp__cclsp__*` - LSP code intelligence

---

## Skill SKILL.md Template

```yaml
---
name: skill-name
description: Multi-line description of what the skill does and when it activates.
---

# Skill Name

## When This Skill Activates
- Trigger condition 1
- Trigger condition 2

## What This Skill Provides
[Instructions and patterns]
```

---

## Hook Types

| Hook | Event | Configuration Key |
|------|-------|-------------------|
| PreToolUse | Before tool execution | `hooks.PreToolUse` |
| PostToolUse | After tool execution | `hooks.PostToolUse` |
| UserPromptSubmit | User sends message | `hooks.UserPromptSubmit` |
| PreCompact | Before auto-compact | `hooks.PreCompact` |
| Stop | Session ends | `hooks.Stop` |
| StatusLine | Continuous display | `statusLine` |

---

## settings.json Structure

```json
{
  "permissions": {
    "allow": ["Bash(jarvis-crud:*)"]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Read",
      "hooks": [{
        "type": "command",
        "command": "bash /path/to/hook.sh",
        "timeout": 5
      }]
    }]
  },
  "statusLine": {
    "type": "command",
    "command": "bash /path/to/statusline.sh"
  }
}
```

---

## jarvis-crud Commands

| Domain | Operations |
|--------|------------|
| `config` | `get`, `update` |
| `goals` | `list`, `get`, `create`, `update`, `delete` |
| `session` | `get`, `save` |
| `sprint` | `get`, `list`, `tasks`, `log` |
| `context` | `startup`, `resume`, `briefing`, `summary` |
| `personality` | `categories`, `list`, `get` |
| `backup` | `create`, `list`, `restore` |

---

## Mode Canaries

Each mode has a canary token to verify activation:

| Mode | Canary |
|------|--------|
| Jarvis | `JARVIS_PROTOCOL_v1` |
| Sensei | `SENSEI_PROTOCOL_v2` |
| Taiwan | `GUARDIAN_PROTOCOL_v2` |
| Sandbox | `SANDBOX_PROTOCOL_v2` |
| Planner | `JARVIS_PLANNER_v1` |

---

## Key Paths

```bash
# Repository root
D:\Workspace\Claude Code\Repositorios\claude-agents

# User data (SQLite)
~/.claude/jarvis/jarvis.db

# Session cache
~/.claude/jarvis/sessions/{session_id}/

# Hook logs
~/.claude/jarvis/hooks.log

# Plans directory
~/.claude/jarvis/plans/
```

---

## Agent Categories (44 Total)

| Category | Count | Key Agents |
|----------|-------|------------|
| planning | 3 | strategic-architect, tactical-architect, operational-planner |
| core | 3 | jarvis, planner (deprecated), onboarding-guide |
| ai | 8 | sensei, genai-architect, llm-specialist, dify-specialist |
| engineering | 3 | code-reviewer, code-cleaner, code-documenter |
| automation | 3 | sandbox, linear-pm, n8n-specialist |
| spark | 4 | specialist, troubleshooter, performance-analyzer, streaming-architect |
| fabric | 6 | architect, pipeline-developer, logging-specialist, etc. |

---

## Skills (30 Total)

| Category | Skills |
|----------|--------|
| code-quality | code-quality-pipeline, testing, agent-quality |
| version-control | git-workflow |
| research | context7-research |
| automation | sandbox, swarm-orchestrator, bash-devcontainer |
| modes | sensei, taiwan, pm, finances, fabric, faturamento, genai |
| frontend | ui-forge, lovable |
| utilities | youtube, mindmap, work-report, skill-manager, system-audit |
| career | taiwan-career, job-application |

---

## Critical Rules

1. **AskUserQuestion** - Use tool for ALL multiple-choice questions
2. **Always Persist Data** - "Noted" requires actual jarvis-crud command
3. **Verify Before Completion** - Test changes work before marking complete
4. **Structural Change Propagation** - Update all consumers when adding/changing files
5. **Self-Improvement Persistence** - Persist behavioral corrections to instruction files
