# Category: Workflows & Knowledge Guides

> **Total in awesome-claude-code:** 30 resources
> **Selected for adoption:** 4 resources

---

## Overview

Workflows & Knowledge Guides are tightly coupled resource sets for projects. Our Jarvis setup already has extensive workflows (SDD, Dev Loop), so we focus on unique patterns and deep knowledge.

---

## Selected Resources

### 1. Claude Code System Prompts (ADOPT)
**Link:** [anthropics/claude-code-prompts](https://github.com/anthropics/claude-code-prompts)

Complete system prompts including ALL subagent prompts.

**Why Selected:**
- Deep understanding of Claude Code internals
- Reference for prompt engineering
- Validates our agent assumptions

**Contents:**
- Main agent system prompt
- Plan subagent prompt
- Explore subagent prompt
- Tool definitions
- Behavior guidelines

**Integration:** Study material, reference in KB

---

### 2. Claude CodePro (EVALUATE)
**Link:** [anthropics/claude-codepro](https://github.com/anthropics/claude-codepro)

TDD enforcement, cross-session memory, semantic search.

**Why Selected:**
- Patterns for planning and testing skills
- Memory management insights
- Quality enforcement patterns

**Integration:** Pattern adoption, not direct install

---

### 3. Claude Code Tips Collection (ADOPT)
**Link:** [anthropics/claude-code-tips](https://github.com/anthropics/claude-code-tips)

35+ tips including voice input, container workflows, conversation cloning.

**Why Selected:**
- Immediate productivity improvements
- User training material
- Patterns for our KB

**Key Tips:**
- Voice input with Whisper
- Container-based development
- Conversation cloning
- Memory management
- Context optimization

**Integration:** KB entry, CLAUDE.md tips section

---

### 4. Learn Claude Code (WATCH)
**Link:** [anthropics/learn-claude-code](https://github.com/anthropics/learn-claude-code)

Analysis of Claude Code agent design - reconstructs in few hundred lines.

**Why Selected:**
- Deep understanding for custom agent building
- Architecture insights
- Educational value

**Integration:** Study material

---

## Skipped Resources

| Resource | Reason |
|----------|--------|
| Ralph-Wiggum variants | Already in QW-009 |
| Ralph-Orchestrator | Already in QW-009 |
| Superpowers workflows | Already in QW-009 |
| Basic tutorials | Our KB is more comprehensive |
| Platform-specific guides | Limited use |

---

## Workflow Comparison

| Aspect | Our Setup | Curated Resources |
|--------|-----------|-------------------|
| Planning | SDD phases, Dev Loop | Claude CodePro patterns |
| Testing | testing skill | TDD enforcement patterns |
| Memory | Context hooks | Cross-session memory ideas |
| Agents | 40+ custom agents | System prompts reference |

---

## Knowledge Integration

```
.claude/kb/
├── claude-code-tips/
│   └── index.md          # 35+ tips
├── system-prompts/
│   ├── main-agent.md     # Main prompt
│   └── subagents.md      # Subagent prompts
└── patterns/
    └── codepro.md        # CodePro patterns
```

---

## Integration Priority

| Resource | Priority | Complexity | Week |
|----------|----------|------------|------|
| System Prompts | High | Easy | 2 |
| Tips Collection | High | Easy | 1 |
| Claude CodePro | Medium | Medium | 3 |
| Learn Claude Code | Low | Medium | 4+ |

---

*Category Analysis: 2026-02-03*
