---
name: pm
description: Project management mode. Activates when managing sprints, issues, milestones, or project coordination with Linear integration.
---

# PM Skill

Provides comprehensive project management through the PM Mode.

---

## MODE ACTIVATION - MANDATORY READING

When this skill activates:

1. **READ `modes/pm-mode.md`** - Contains complete instructions
2. **CONFIRM** by saying: `Mode loaded: [CANARY from line 3]`
3. **BE** the Project Manager - follow the mode file instructions

**CRITICAL:**
- DO NOT use Task tool - YOU ARE the agent
- AskUserQuestion works normally (use for planning decisions)
- All output is visible to user

---

## When This Skill Activates

Trigger on project management intent:

**Sprint management:**
- "plan the sprint..."
- "sprint review..."
- "what's in the backlog..."
- "sprint status..."

**Issue tracking:**
- "create an issue..."
- "prioritize tasks..."
- "what are the blockers..."
- "update issue status..."

**Project coordination:**
- "milestone progress..."
- "project status..."
- "team capacity..."
- "resource planning..."

**Linear mentions:**
- "Linear issues..."
- "sync with Linear..."
- "Linear project..."

---

## Do NOT Activate

Skip when:
- User asks for simple task creation (use /workflow:task)
- User wants sprint template only
- User explicitly declines PM mode

---

## Related

- **Mode file:** `modes/pm-mode.md` (MANDATORY READING)
- **Agent:** `agents/automation/linear-pm.md` (for Task delegation)
- **MCP:** Linear MCP for issue tracking

---

*This skill file is intentionally minimal. All behavior is defined in the mode file.*
