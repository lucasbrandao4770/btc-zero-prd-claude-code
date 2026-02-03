# Jarvis Hooks System

> **MCP Validated:** 2026-02-01

---

## Overview

Hooks are bash scripts that execute at specific events during a Claude Code session. They enable:
- Custom status displays
- Context preservation
- Tool interception
- Session state management

---

## Hook Types

| Hook | Event | Purpose |
|------|-------|---------|
| **PreToolUse** | Before tool execution | Validate, warn, intercept |
| **PostToolUse** | After tool execution | Log, transform output |
| **UserPromptSubmit** | User sends message | Pre-process input |
| **PreCompact** | Before auto-compact | Preserve critical context |
| **Stop** | Claude finishes responding | Save state, cleanup, **play notification** |
| **StatusLine** | Continuous display | Show session status |
| **SessionStart** | Session begins | Initialize state |
| **Notification** | Claude waiting for input | Play sound, alert user |

### Notification Hook Matchers

The Notification hook supports specific matchers:

| Matcher | Triggers When | Timing |
|---------|---------------|--------|
| `permission_prompt` | Claude needs permission for a tool | **Immediate** ✅ |
| `idle_prompt` | Claude waiting for user input | **After 60s** ⚠️ |
| `elicitation_dialog` | MCP tool needs additional input | **Immediate** ✅ |
| `auth_success` | Authentication succeeds | **Immediate** ✅ |
| `""` (empty) | Any notification type | ⚠️ **AVOID** - catches unwanted events |

**IMPORTANT - "Turn-Based" Notification Pattern:**

For Duolingo-style "your turn" notifications, use this combination:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [{ "type": "command", "command": "bash notification.sh", "timeout": 10 }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "bash notification.sh", "timeout": 10 }]
      }
    ],
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [{ "type": "command", "command": "bash notification.sh", "timeout": 10 }]
      }
    ]
  }
}
```

| Scenario | Hook | Timing |
|----------|------|--------|
| Claude asks a question | `PreToolUse:AskUserQuestion` | Immediate (before shown) |
| Claude needs permission | `Notification:permission_prompt` | Immediate |
| Claude finishes turn | `Stop` | Immediate |

**Known Limitations (GitHub issues #12048, #13024):**
- No dedicated "WaitingForInput" hook exists yet
- `idle_prompt` has hardcoded 60-second delay
- Empty matcher `""` catches all notification types (causes unwanted triggers)

**Reference:** [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)

---

## Hook File Locations

Hooks are bash scripts stored in `hooks/`:

```
hooks/
|-- pre-tool-use.sh       # PreToolUse hook
|-- user-prompt-submit.sh # UserPromptSubmit hook
|-- pre-compact.sh        # PreCompact hook
|-- stop.sh               # Stop hook
|-- statusline.sh         # StatusLine hook
|-- session-start.sh      # SessionStart hook
```

---

## Configuration

Hooks are configured in `settings.json` (user-level) or `settings.local.json` (project-level).

### Basic Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/pre-tool-use.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Full Example (settings.local.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/Lucas/.claude/hooks/pre-tool-use.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/Lucas/.claude/hooks/user-prompt-submit.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/Lucas/.claude/hooks/pre-compact.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/Lucas/.claude/hooks/stop.sh",
            "timeout": 15
          }
        ]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "bash C:/Users/Lucas/.claude/hooks/statusline.sh"
  }
}
```

---

## Hook Input/Output

### Input (JSON via stdin)

Hooks receive JSON input via stdin containing event-specific data:

**PreToolUse:**
```json
{
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/path/to/file"
  }
}
```

**StatusLine:**
```json
{
  "session_id": "abc-123",
  "context_window": {
    "used_percentage": 45
  },
  "cost": {
    "total_cost_usd": 0.50
  }
}
```

### Output

Hooks can:
1. Exit 0 silently (no effect)
2. Output JSON with `additionalContext` for Claude
3. Write to stderr for user display

**Example Output:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "WARNING: Large file detected"
  }
}
```

---

## Critical Rules

### Always Exit 0

**CRITICAL:** Hooks must ALWAYS exit 0. A non-zero exit can crash Claude Code.

```bash
# ALWAYS wrap main in error handling
{
    main
} || {
    echo '{}' # Fallback output
    exit 0   # NEVER exit non-zero
}
```

### Use stderr for User Display

```bash
# Display to user (stderr)
echo "WARNING: Large file" >&2

# Return data to Claude (stdout)
echo '{"additionalContext": "..."}'
```

---

## Jarvis Hooks

### statusline.sh

Displays context usage, mode, sprint, personality:

```
JARVIS SYSTEM | Context: [=====-----] 50% | Mode: Jarvis | Sprint: W05
```

Features:
- Color-coded context percentage
- Mode/sprint/personality display
- Per-session caching
- Throttling (8s between updates)
- Windows-safe with lock file to prevent fork storms

### pre-tool-use.sh

Warns about large file reads:

```
SOFT WARNING: file.py (750 lines)
NOTE: Consider using Task tool with subagent to preserve main context.

HARD WARNING: file.py (2500 lines)
WARNING: Consider delegation to preserve main context.
```

Thresholds:
- Soft: 500 lines
- Hard: 2000 lines

### session-start.sh

Initializes session cache from jarvis-crud:
- Fetches sprint, personality, threshold
- Creates session cache directory
- Writes cache.json for statusline

### pre-compact.sh

Preserves critical context before auto-compact:
- Saves current state to session cache
- Ensures continuity after compact

### stop.sh

Saves final session state:
- Updates jarvis-crud session
- Cleans up temporary files

---

## User-Level vs Project-Level

### User-Level (`~/.claude/settings.json`)

- Applies to ALL sessions
- General preferences
- Personal hooks

### Project-Level (`.claude/settings.local.json`)

- Applies to THIS project only
- Project-specific hooks
- Override user-level settings

### Priority

Project-level settings override user-level settings.

---

## Debugging Hooks

### Hook Logs

Hooks log to `~/.claude/jarvis/hooks.log`:

```bash
tail -f ~/.claude/jarvis/hooks.log
```

### Manual Testing

Test hooks manually:

```bash
# Test statusline
echo '{"session_id":"test","context_window":{"used_percentage":50}}' | bash hooks/statusline.sh

# Test pre-tool-use
echo '{"tool_name":"Read","tool_input":{"file_path":"large.py"}}' | bash hooks/pre-tool-use.sh
```

---

## Common Patterns

### Check Tool Name

```bash
TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name // ""')

if [[ "$TOOL_NAME" != "Read" ]]; then
    exit 0  # Only process Read operations
fi
```

### Extract Session ID (Pure Bash)

```bash
# No jq fork needed
if [[ $json =~ \"session_id\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
    session_id="${BASH_REMATCH[1]}"
fi
```

### Caching for Performance

```bash
# Check cache before expensive operations
if [[ -f "$cache_file" ]]; then
    cat "$cache_file"
    exit 0
fi
```
