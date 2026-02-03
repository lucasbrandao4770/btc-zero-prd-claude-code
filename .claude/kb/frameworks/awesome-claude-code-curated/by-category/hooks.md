# Category: Hooks

> **Total in awesome-claude-code:** 11 resources
> **Selected for adoption:** 4 resources

---

## Overview

Hooks are scripts activated at Claude Code lifecycle points. Our current setup has basic hooks (Duolingo sound notification). These selections significantly enhance our hook capabilities.

---

## Selected Resources

### 1. cchooks Python SDK (ADOPT)
**Link:** [anthropics/cchooks](https://github.com/anthropics/claude-code-hooks)

Lightweight Python SDK for writing Claude Code hooks with clean API.

**Why Selected:**
- Simplifies hook development beyond bash scripts
- Better error handling and testing
- Type hints and Pythonic API

**Example:**
```python
from cchooks import hook, HookType

@hook(HookType.POST_TOOL)
def validate_output(tool_name: str, result: str) -> bool:
    # Custom validation logic
    return True
```

**Integration:** `pip install cchooks`

---

### 2. TDD Guard (ADOPT)
**Link:** [anthropics/tdd-guard](https://github.com/anthropics/tdd-guard)

Real-time monitoring to block TDD violations.

**Why Selected:**
- Enforces testing discipline automatically
- Complements our testing skill
- Quality gate for development

**Integration:** Copy hooks, configure rules

---

### 3. HCOM - Hook Communications (EVALUATE)
**Link:** [anthropics/hcom](https://github.com/anthropics/hcom)

Multi-agent collaboration with @-mention targeting.

**Why Selected:**
- Agent-to-agent communication
- Future multi-agent enhancement
- Coordination protocols

**Integration:** Medium complexity, requires agent registry

---

### 4. Claudio (WATCH)
**Link:** [anthropics/claudio](https://github.com/anthropics/claudio)

OS-native sounds for Claude Code lifecycle events.

**Why Selected:**
- Audio feedback (we have Duolingo sound, could enhance)
- Easy to try
- Better awareness of agent activity

**Integration:** Simple hook installation

---

## Skipped Resources

| Resource | Reason |
|----------|--------|
| Basic notification hooks | We have Duolingo sound |
| Platform-specific hooks | Limited cross-platform use |
| Experimental hooks | Not mature enough |

---

## Hook Architecture

```
.claude/hooks/
├── pre-session/         # Before session starts
├── post-session/        # After session ends
├── pre-tool/            # Before tool execution
├── post-tool/           # After tool execution
├── security_check.py    # cchooks security hook
├── tdd-guard.sh         # TDD enforcement
└── claudio.sh           # Sound notifications
```

---

## Integration Priority

| Hook | Priority | Complexity | Week |
|------|----------|------------|------|
| cchooks | High | Easy | 1 |
| TDD Guard | High | Medium | 2 |
| HCOM | Medium | Medium | 3 |
| Claudio | Low | Easy | 4 |

---

*Category Analysis: 2026-02-03*
