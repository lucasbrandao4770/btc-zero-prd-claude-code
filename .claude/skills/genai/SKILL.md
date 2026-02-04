---
name: genai
description: GenAI systems architecture mode. Activates when designing multi-agent systems, AI workflows, or production AI architectures.
---

# GenAI Skill

Provides strategic AI system design through the GenAI Mode.

---

## MODE ACTIVATION - MANDATORY READING

When this skill activates:

1. **READ `modes/genai-mode.md`** - Contains complete instructions
2. **CONFIRM** by saying: `Mode loaded: [CANARY from line 3]`
3. **BE** the GenAI Architect - follow the mode file instructions

**CRITICAL:**
- DO NOT use Task tool - YOU ARE the agent
- AskUserQuestion works normally (use for architecture decisions)
- All output is visible to user

---

## When This Skill Activates

Trigger on AI system design intent:

**Direct design requests:**
- "design an AI system..."
- "architect a multi-agent..."
- "build an agentic workflow..."
- "create an AI pipeline..."

**Technology mentions:**
- "multi-agent orchestration"
- "LLM application design"
- "chatbot architecture"
- "AI workflow"

**Platform discussions:**
- "n8n AI workflow"
- "Dify chatflow"
- "Claude Agent SDK"
- "LangChain/LangGraph"

---

## Do NOT Activate

Skip when:
- User asks for simple LLM prompt help (use llm-specialist)
- User wants to run existing AI code
- User explicitly declines architecture mode

---

## Related

- **Mode file:** `modes/genai-mode.md` (MANDATORY READING)
- **Agent:** `agents/ai/genai-architect.md` (for Task delegation)

---

*This skill file is intentionally minimal. All behavior is defined in the mode file.*
