# Hook Patterns

> **MCP Validated:** 2026-02-01

---

## Overview

This document covers common patterns for implementing Claude Code hooks.

---

## Hook Script Template

```bash
#!/bin/bash
# Hook Name - Brief description
#
# Purpose: What this hook does
# Event: PreToolUse | PostToolUse | UserPromptSubmit | PreCompact | Stop
#
# CRITICAL: Must ALWAYS exit 0 - never crash Claude Code.

set -uo pipefail

# Security: restrict file permissions
umask 077

# Configuration
LOG_FILE="${HOME}/.claude/jarvis/hooks.log"

# Ensure log directory exists
mkdir -p "$(dirname "${LOG_FILE}")" 2>/dev/null || true

# Function: Log message with timestamp
log_msg() {
    echo "[$(date -Iseconds)] HookName: $1" >> "${LOG_FILE}" 2>/dev/null || true
}

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Main logic
main() {
    # Parse input
    # Process
    # Output result
    exit 0
}

# Execute with error handling (CRITICAL: always exit 0)
{
    main
} || {
    log_msg "ERROR: Hook failed"
    echo '{}'
    exit 0
}
```

---

## Pattern 1: PreToolUse - Large File Warning

Warn before reading large files to preserve context.

```bash
#!/bin/bash
# PreToolUse - Large file warning
set -uo pipefail

SOFT_THRESHOLD=500   # Lines - warning
HARD_THRESHOLD=2000  # Lines - strong warning

INPUT_JSON=$(cat)
TOOL_NAME=$(echo "${INPUT_JSON}" | jq -r '.tool_name // ""')

# Only process Read operations
if [[ "${TOOL_NAME}" != "Read" ]]; then
    exit 0
fi

FILE_PATH=$(echo "${INPUT_JSON}" | jq -r '.tool_input.file_path // ""')

# Skip if file doesn't exist
[[ ! -f "${FILE_PATH}" ]] && exit 0

# Count lines
LINE_COUNT=$(wc -l < "${FILE_PATH}" 2>/dev/null || echo "0")

# Generate warning
if (( LINE_COUNT >= HARD_THRESHOLD )); then
    echo "WARNING: File has ${LINE_COUNT} lines. Consider delegation." >&2
    echo "{\"hookSpecificOutput\":{\"additionalContext\":\"Large file warning\"}}"
elif (( LINE_COUNT >= SOFT_THRESHOLD )); then
    echo "NOTE: File has ${LINE_COUNT} lines." >&2
fi

exit 0
```

---

## Pattern 2: StatusLine - Context Display

Display session status in the terminal.

```bash
#!/bin/bash
# StatusLine - Context usage display
set -uo pipefail

# Colors
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
RESET='\033[0m'

INPUT_JSON=$(cat)

# Parse context percentage
CONTEXT_PCT=$(echo "${INPUT_JSON}" | jq -r '.context_window.used_percentage // 0')

# Determine color
if (( ${CONTEXT_PCT%.*} >= 80 )); then
    COLOR="$RED"
elif (( ${CONTEXT_PCT%.*} >= 60 )); then
    COLOR="$YELLOW"
else
    COLOR="$GREEN"
fi

# Build bar
WIDTH=10
FILLED=$(( (${CONTEXT_PCT%.*} * WIDTH + 50) / 100 ))
BAR="["
for ((i=0; i<FILLED; i++)); do BAR+="="; done
for ((i=FILLED; i<WIDTH; i++)); do BAR+="-"; done
BAR+="]"

echo -e "Context: ${COLOR}${BAR} ${CONTEXT_PCT%.*}%${RESET}"
exit 0
```

---

## Pattern 3: SessionStart - Initialize Cache

Populate session cache from jarvis-crud.

```bash
#!/bin/bash
# SessionStart - Initialize session cache
set -uo pipefail

SESSIONS_DIR="${HOME}/.claude/jarvis/sessions"

INPUT_JSON=$(cat)
SESSION_ID=$(echo "${INPUT_JSON}" | jq -r '.session_id // "unknown"')
SOURCE=$(echo "${INPUT_JSON}" | jq -r '.source // "startup"')

# Sanitize session_id
SESSION_ID="${SESSION_ID//[^a-zA-Z0-9_-]/}"

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
CACHE_FILE="${SESSION_DIR}/cache.json"

mkdir -p "${SESSION_DIR}" 2>/dev/null || true

# Fetch data from jarvis-crud
if command -v jarvis-crud &>/dev/null; then
    SPRINT=$(jarvis-crud sprint get 2>/dev/null | jq -r '.data.sprint_id // ""')
    PERSONALITY=$(jarvis-crud config get 2>/dev/null | jq -r '.data.personality.default // ""')
else
    SPRINT=""
    PERSONALITY=""
fi

# Write cache
cat > "$CACHE_FILE" << EOF
{
  "mode": "",
  "sprint": "${SPRINT}",
  "personality": "${PERSONALITY}",
  "threshold": 80
}
EOF

echo '{}'
exit 0
```

---

## Pattern 4: PreCompact - Preserve Context

Save critical context before auto-compact.

```bash
#!/bin/bash
# PreCompact - Preserve context before compact
set -uo pipefail

SESSIONS_DIR="${HOME}/.claude/jarvis/sessions"

INPUT_JSON=$(cat)
SESSION_ID=$(echo "${INPUT_JSON}" | jq -r '.session_id // "unknown"')
SESSION_ID="${SESSION_ID//[^a-zA-Z0-9_-]/}"

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
CONTEXT_FILE="${SESSION_DIR}/pre-compact-context.json"

mkdir -p "${SESSION_DIR}" 2>/dev/null || true

# Save current context info
echo "${INPUT_JSON}" > "$CONTEXT_FILE" 2>/dev/null || true

# Return context restoration message
echo '{"hookSpecificOutput":{"additionalContext":"=== CONTEXT PRESERVED ==="}}'
exit 0
```

---

## Pattern 5: Stop - Save Session State

Save final session state when exiting.

```bash
#!/bin/bash
# Stop - Save session state
set -uo pipefail

INPUT_JSON=$(cat)
SESSION_ID=$(echo "${INPUT_JSON}" | jq -r '.session_id // "unknown"')

# Save session via jarvis-crud
if command -v jarvis-crud &>/dev/null; then
    jarvis-crud session save --json "{\"session_id\": \"${SESSION_ID}\"}" 2>/dev/null || true
fi

exit 0
```

---

## Pattern 6: UserPromptSubmit - Input Processing

Process user input before Claude sees it.

```bash
#!/bin/bash
# UserPromptSubmit - Process user input
set -uo pipefail

INPUT_JSON=$(cat)
USER_PROMPT=$(echo "${INPUT_JSON}" | jq -r '.user_prompt // ""')

# Example: Detect mode activation commands
if [[ "${USER_PROMPT}" == "/jarvis"* ]]; then
    echo '{"hookSpecificOutput":{"additionalContext":"Jarvis mode requested"}}'
fi

exit 0
```

---

## Configuring Hooks

### In settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/hook.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "StatusLine": {
      "type": "command",
      "command": "bash /path/to/statusline.sh"
    }
  }
}
```

### Hook Matchers

| Matcher | Matches |
|---------|---------|
| `"Read"` | Read tool only |
| `"Write"` | Write tool only |
| `"*"` | All tools |
| `["Read", "Edit"]` | Read or Edit |

---

## Best Practices

### Performance

```bash
# Cache jq availability
HAS_JQ=0
command -v jq &>/dev/null && HAS_JQ=1

# Pure bash regex (zero forks)
if [[ $json =~ \"field\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
    value="${BASH_REMATCH[1]}"
fi

# Throttle frequent hooks
THROTTLE_FILE="${SESSION_DIR}/.throttle"
if [[ -f "$THROTTLE_FILE" ]]; then
    LAST=$(cat "$THROTTLE_FILE")
    if (( $(date +%s) - LAST < 5 )); then
        exit 0  # Skip if < 5s since last
    fi
fi
echo "$(date +%s)" > "$THROTTLE_FILE"
```

### Error Handling

```bash
# ALWAYS wrap in error handler
{
    main
} || {
    echo '{}'
    exit 0  # NEVER exit non-zero
}
```

### Security

```bash
# Restrict file permissions
umask 077

# Sanitize session IDs
session_id="${raw_id//[^a-zA-Z0-9_-]/}"
```

---

## Pattern 7: Notification - Audio Alert

Play sound when Claude waits for user input (Duolingo-style).

```bash
#!/bin/bash
# Notification - Play sound when Claude waits for input
# Windows-compatible using PowerShell MediaPlayer
set -uo pipefail

SOUND_FILE="C:/Users/Lucas/.claude/sounds/duolingo-correct.mp3"

# Try MP3 playback via PowerShell, fallback to beep
if command -v powershell &>/dev/null; then
    powershell -ExecutionPolicy Bypass -Command "
        Add-Type -AssemblyName presentationCore
        \$mp = New-Object system.windows.media.mediaplayer
        \$mp.open('$SOUND_FILE')
        Start-Sleep -Milliseconds 300
        \$mp.Play()
        Start-Sleep -Seconds 2
    " 2>/dev/null || {
        # Fallback: System beep
        powershell -Command "[console]::beep(800,200);[console]::beep(1000,200)" 2>/dev/null || true
    }
fi

exit 0
```

**Cross-platform alternatives:**
- **Mac:** `afplay ~/.claude/sounds/duolingo-correct.mp3`
- **Linux:** `mpg123 -q ~/.claude/sounds/duolingo-correct.mp3`

---

## Debugging

### Enable Logging

```bash
LOG_FILE="${HOME}/.claude/jarvis/hooks.log"

log_msg() {
    echo "[$(date -Iseconds)] $1" >> "${LOG_FILE}" 2>/dev/null || true
}
```

### View Logs

```bash
tail -f ~/.claude/jarvis/hooks.log
```

### Manual Testing

```bash
# Test with sample input
echo '{"tool_name":"Read","tool_input":{"file_path":"test.py"}}' | bash hooks/pre-tool-use.sh
```
