# Category: Slash Commands

> **Total in awesome-claude-code:** 59 resources
> **Selected for adoption:** 4 resources (selective - we have 13 commands)

---

## Overview

Slash Commands control Claude's behavior. Our Jarvis setup already has 13 custom commands, so we're highly selective - only adding commands that fill gaps.

---

## Selected Resources

### 1. /prd-generator (ADOPT)
**Link:** [anthropics/prd-generator](https://github.com/anthropics/prd-generator)

Generates full PRDs from conversation context.

**Why Selected:**
- Complements our /brainstorm → /define workflow
- Faster PRD creation
- Consistent format

**Our Gap:** We have /define but no dedicated PRD generator

**Integration:**
```bash
cp prd-generator.md .claude/commands/
```

---

### 2. /tdd (ADOPT)
**Link:** [anthropics/tdd-command](https://github.com/anthropics/tdd-command)

Guides TDD Red-Green-Refactor with git workflow integration.

**Why Selected:**
- Structured TDD workflow
- Git integration
- Complements testing skill

**Our Gap:** We have testing skill but no dedicated TDD command

**Integration:**
```bash
cp tdd.md .claude/commands/
```

---

### 3. n8n_agent Commands (CHERRY-PICK)
**Link:** [anthropics/n8n-agent](https://github.com/anthropics/n8n-agent)

88+ commands covering every SDLC aspect.

**Why Selected:**
- Massive command library
- Cherry-pick specific commands we lack
- Reference for command patterns

**Cherry-Pick Candidates:**
- /code-review (if different from ours)
- /security-scan
- /dependency-check
- /changelog

**Integration:** Selective adoption only

---

### 4. Linux Desktop Commands (WATCH)
**Link:** [anthropics/linux-commands](https://github.com/anthropics/linux-commands)

Specialized commands for Linux environments.

**Why Selected:**
- Linux-specific optimizations
- System administration tasks

**Integration:** Platform-specific, adopt if needed

---

## Skipped Resources

| Resource | Reason |
|----------|--------|
| Basic /commit variants | We have git:commit skill |
| /review variants | We have review:review skill |
| /plan variants | We have planning skill |
| Platform-specific | Limited cross-platform use |
| Duplicate functionality | Our commands cover it |

---

## Command Comparison

| Category | Our Commands | Curated Additions |
|----------|--------------|-------------------|
| Planning | /brainstorm, /define, /design | /prd-generator |
| Building | /build, /ship | - |
| Testing | testing skill | /tdd |
| Review | /review | n8n security commands |
| Git | git:commit | - |
| Documentation | /readme-maker | - |

---

## Integration Priority

| Command | Priority | Complexity | Week |
|---------|----------|------------|------|
| /prd-generator | High | Easy | 3 |
| /tdd | Medium | Easy | 4 |
| n8n cherry-picks | Low | Medium | 4+ |
| Linux Desktop | Low | Easy | 4+ |

---

## Command Structure

When adopting commands, follow our structure:

```
.claude/commands/
├── core/                    # Core commands
├── dev/                     # Development commands
│   └── tdd.md              # NEW: TDD workflow
├── knowledge/               # KB commands
├── review/                  # Review commands
└── workflow/                # Workflow commands
    └── prd-generator.md    # NEW: PRD generation
```

---

*Category Analysis: 2026-02-03*
