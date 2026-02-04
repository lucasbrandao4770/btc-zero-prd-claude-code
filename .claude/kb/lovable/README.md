# Lovable AI Knowledge Base

> **Version:** 1.0.0
> **Last Updated:** 2026-01-30
> **Quality:** HIGH (Official docs, hands-on experience)
> **Maintainer:** Jarvis AI System

---

## Overview

This Knowledge Base provides comprehensive guidance for using Lovable (lovable.dev), an AI-powered web application builder, effectively in hybrid workflows with Claude Code. Content is derived from official Lovable documentation and practical integration experience.

**Primary Users:**
- `ui-forge` agent - For UI prototyping workflows
- `strategic-architect` agent - For tool selection decisions
- `tactical-architect` agent - For implementation planning
- Human developers - For Lovable best practices reference

---

## KB Structure

```
kb/lovable/
├── README.md                 <- You are here
├── 01-prompting-guide.md     <- Effective prompting techniques
├── 02-github-workflow.md     <- GitHub sync configuration
├── 03-tool-division.md       <- Lovable vs Claude Code decisions
└── 04-limitations.md         <- Known issues and workarounds
```

---

## Quick Start

### For UI Prototyping
```
Start: 01-prompting-guide.md -> Core prompting principles
Then:  03-tool-division.md -> When to use Lovable vs Claude Code
Next:  04-limitations.md -> Understand constraints
```

### For GitHub Integration
```
Start: 02-github-workflow.md -> Setup and workflow
Then:  04-limitations.md -> Sync limitations to avoid
```

### For Tool Selection
```
Start: 03-tool-division.md -> Comprehensive decision matrix
Then:  01-prompting-guide.md -> Maximize Lovable effectiveness
Next:  04-limitations.md -> Risk assessment
```

---

## File Index

| File | Purpose | Key Topics |
|------|---------|------------|
| [01-prompting-guide.md](./01-prompting-guide.md) | How to write effective Lovable prompts | CTGC structure, meta prompting, common mistakes |
| [02-github-workflow.md](./02-github-workflow.md) | GitHub sync setup and best practices | Setup, sync flow, conflict resolution |
| [03-tool-division.md](./03-tool-division.md) | When to use Lovable vs Claude Code | Decision matrix, hybrid workflow, examples |
| [04-limitations.md](./04-limitations.md) | Known constraints and workarounds | 11 major limitations with solutions |

---

## When to Use This KB

### Use Lovable When:
- Building UI prototypes or MVPs
- Creating visual interfaces quickly
- Exploring design directions
- Need rapid iteration without local setup
- Building Supabase-integrated apps

### Use Claude Code When:
- Implementing complex business logic
- Type-safe production code needed
- Multi-file refactoring required
- Backend/API development
- Debugging complex issues

### Use Both (Hybrid) When:
- Building full-stack applications
- Prototyping then hardening
- UI first, logic second approach

---

## Key Concepts

| Concept | Description | File |
|---------|-------------|------|
| CTGC Framework | Context, Task, Guidelines, Constraints prompt structure | 01-prompting-guide.md |
| Meta Prompting | Asking Lovable to generate its own prompts | 01-prompting-guide.md |
| Default Branch Sync | GitHub sync only works with main/master | 02-github-workflow.md |
| 60-70% Solution | Lovable gets you most of the way there | 04-limitations.md |
| Three-Phase Hybrid | Plan -> Prototype -> Harden workflow | 03-tool-division.md |

---

## Integration with Jarvis

### UI Forge Workflow
This KB supports the `ui-forge` agent and `/ui-forge` skill for automated UI prototyping:

```
1. User describes UI need
2. ui-forge agent creates HANDOFF with Lovable instructions
3. User executes in Lovable (external)
4. User syncs via GitHub
5. Claude Code hardens and integrates
```

### Related Agents
- `ui-forge` - UI prototyping coordinator
- `strategic-architect` - High-level tool selection
- `tactical-architect` - Implementation planning
- `code-reviewer` - Post-Lovable code review

---

## Content Standards

### Every File Contains
1. **YAML Frontmatter** - Metadata for indexing
2. **Overview Section** - What and why
3. **Tables for Quick Reference** - Decision matrices, limitation tables
4. **Practical Examples** - Real prompts and scenarios
5. **Cross-References** - Links to related KB files

### Example Format
All examples follow this structure:
```markdown
### Pattern: {Name}

**Scenario:** {When to use this}

**Prompt Example:**
```
[Actual prompt text]
```

**Result:** {What to expect}
```

---

## Sources & References

### Primary Sources
| Source | URL | Use For |
|--------|-----|---------|
| Lovable Docs | lovable.dev/docs | Official documentation |
| Lovable Tips | lovable.dev/tips | Prompting best practices |
| GitHub Integration | lovable.dev/github | Sync documentation |

### Related Resources
- [UI Forge Skill](../../skills/ui-forge.md) - Automated UI workflow
- [Agentic AI KB](../agentic-ai/README.md) - Agent patterns
- [Python KB](../python/README.md) - Backend code standards

---

## Version Information

| Aspect | Value |
|--------|-------|
| KB Version | 1.0.0 |
| Created | 2026-01-30 |
| Files | 5 |
| Quality | HIGH |

---

*For the full Jarvis experience, run `/jarvis` to activate all features.*
