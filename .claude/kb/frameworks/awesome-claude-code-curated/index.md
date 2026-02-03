# Awesome Claude Code: Curated Collection

> **Source:** [awesome-claude-code](https://github.com/anthropics/awesome-claude-code) repository
> **Curated:** 2026-02-03 | **Resources:** 25 selected from 197

---

## Overview

This curated collection filters the awesome-claude-code repository (197 resources) to identify the **25 highest-value resources** for our Jarvis/AgentSpec setup. Resources are evaluated based on:

1. **Relevance** - Does it solve a problem we have?
2. **Uniqueness** - Does it provide something we don't already have?
3. **Quality** - Is it well-maintained and documented?
4. **Complexity** - How hard is it to adopt?
5. **Integration** - Does it fit our existing setup?

---

## Quick Navigation

| Document | Purpose |
|----------|---------|
| [RECOMMENDATIONS.md](RECOMMENDATIONS.md) | **Start here** - Prioritized adoption roadmap |
| [top-picks.md](top-picks.md) | Detailed analysis of top 20 resources |
| [adoption-guide.md](adoption-guide.md) | Step-by-step installation guides |
| [by-category/](by-category/) | Category-specific deep dives |

---

## Category Summary

| Category | Total | Selected | Top Picks |
|----------|-------|----------|-----------|
| **Agent Skills** | 11 | 5 | Everything Claude Code, cc-devops-skills, Trail of Bits, Context Engineering Kit |
| **Hooks** | 11 | 4 | cchooks, TDD Guard, HCOM, Claudio |
| **Tooling** | 43 | 6 | claude-code-tools, Claude Squad, better-ccflare, viwo-cli, Session Restore, VoiceMode |
| **Workflows & Guides** | 30 | 4 | System Prompts, Claude CodePro, Tips Collection, Learn Claude Code |
| **Slash Commands** | 59 | 4 | /prd-generator, /tdd, n8n_agent, Linux Desktop |
| **CLAUDE.md Files** | 27 | 1 | Architect CLAUDE.md |
| **Status Lines** | 5 | 1 | Orchestrator Status Lines |
| **Output Styles** | 4 | 0 | None selected (our setup is sufficient) |
| **Official Docs** | 3 | 1 | MCP Integration Examples |
| **Alt Clients** | 2 | 0 | None selected (we use Claude Code) |

**Total:** 25 curated resources from 197 available

---

## Adoption Timeline

```
Week 1: Quick Wins (5 resources)
├── Everything Claude Code
├── cc-devops-skills
├── cchooks Python SDK
├── Claude Code Tips
└── Context Engineering Kit

Week 2: Tool Evaluation (5 resources)
├── claude-code-tools
├── TDD Guard
├── better-ccflare
├── Claude Squad
└── Trail of Bits Security

Week 3: Integration (5 resources)
├── viwo-cli
├── /prd-generator
├── Claude Code System Prompts
├── Claude CodePro
└── HCOM

Week 4: Polish (5+ resources)
├── n8n_agent Commands (cherry-pick)
├── Claudio sounds
├── Orchestrator Status Lines
├── /tdd command
└── Linux Desktop Commands
```

---

## Skip List Summary

Resources we intentionally skipped:

| Category | Skipped | Reason |
|----------|---------|--------|
| Already in QW-009 | Superpowers, Ralph-Wiggum, Ralph-Orchestrator | Documented in Frameworks KB |
| Already integrated | AgentSpec | Part of Jarvis system |
| Platform-specific | Windows/macOS tools | Limited cross-platform use |
| IDE-specific | Cursor integrations | We use Claude Code |
| Unmaintained | Various | Stale commits, no updates |

---

## Integration with Existing Setup

Our current Jarvis/AgentSpec setup has:

| Component | Count | How Curated Resources Help |
|-----------|-------|---------------------------|
| Agents | 40+ | Trail of Bits adds security, cc-devops-skills adds IaC |
| Commands | 13 | /prd-generator, /tdd add new workflows |
| KB Domains | 8 | This KB adds ecosystem knowledge |
| Hooks | Basic | cchooks, TDD Guard, HCOM enhance significantly |
| Skills | Multiple | Everything Claude Code documents all features |

---

## See Also

- [Frameworks KB Index](../index.md) - Parent knowledge base
- [Quick Reference](../quick-reference.md) - Framework comparison
- [QW-009 Archive](../../dev/archive/) - Original framework research

---

*Curated: 2026-02-03 | Sprint: S03 | Task: QW-011*
