# Frameworks Knowledge Base

> Research and analysis of Claude Code ecosystem frameworks for Jarvis integration

---

## Purpose

This KB contains deep analysis of 11 frameworks in the Claude Code ecosystem, evaluated for:
1. **Understanding** - What they do, how they work, problems they solve
2. **Integration** - How to integrate with/learn from for Jarvis system
3. **Learning** - Educational value and skill development

---

## Frameworks Catalog

| Framework | Category | Context7 ID | Status | Recommendation |
|-----------|----------|-------------|--------|----------------|
| [Superpowers](superpowers/) | Planning & Skills | `/obra/superpowers` | **Complete** | Adapt |
| [Spec-Kit](spec-kit/) | Specification-First | `/github/spec-kit` | **Complete** | Learn From |
| [Claude-Workflow](claude-workflow/) | Task Breaking | (local only) | **Complete** | Learn From |
| [Beads](beads/) | Issue Tracking & Memory | `/steveyegge/beads` | **Complete** | Learn From |
| [Supermemory](supermemory/) | Memory API | `/supermemoryai/supermemory` | **Complete** | Learn From |
| [Claude-Mem](claude-mem/) | Memory Compression | `/thedotmack/claude-mem` | **Complete** | Learn From |
| [Gas Town](gastown/) | Multi-Agent Orchestration | `/steveyegge/gastown` | **Complete** | Learn From |
| [Claude-Flow](claude-flow/) | Enterprise Orchestration | `/ruvnet/claude-flow` | **Complete** | Learn From |
| [Cipher](cipher/) | System Prompts & Memory | (local only) | **Complete** | Learn From |
| [Ralph-Wiggum](ralph-wiggum/) | Iterative Loops | `/anthropics/claude-code` | **Complete** | Adapt |
| [AgentSpec](agentspec/) | Spec-Driven Development | (local) | **Complete** | Already Integrated |

---

## Integration Summary

### Recommendation Distribution

| Recommendation | Count | Frameworks |
|----------------|-------|------------|
| **Already Integrated** | 1 | AgentSpec |
| **Adapt** | 2 | Superpowers, Ralph-Wiggum |
| **Learn From** | 8 | Spec-Kit, Claude-Workflow, Beads, Supermemory, Claude-Mem, Gas Town, Claude-Flow, Cipher |

### High-Value Patterns to Adopt

| Pattern | Source Framework | Value | Effort |
|---------|------------------|-------|--------|
| Verification-before-completion | Superpowers | High | Low |
| Rationalization tables | Superpowers | High | Low |
| Completion Promise Protocol | Ralph-Wiggum | High | Low |
| Dependency-aware task graph | Beads | High | Medium |
| Progressive disclosure | Claude-Mem | High | Medium |
| Propulsion Principle (GUPP) | Gas Town | High | Low |
| Anti-drift swarm defaults | Claude-Flow | Medium | Low |
| Priority-based prompt composition | Cipher | Medium | Low |

---

## Document Structure Per Framework

Each framework folder contains:

```
{framework}/
├── analysis.md           # Framework deep dive
├── jarvis-integration.md # Comparison & integration with Jarvis
└── learning-guide.md     # Educational resource
```

See `_templates/` for document templates.

---

## Quick Navigation by Use Case

### Need: Better Planning

| Framework | What It Offers |
|-----------|----------------|
| [Superpowers](superpowers/) | Subagent-driven development, mandatory TDD |
| [Spec-Kit](spec-kit/) | User story independence, explicit task breakdown |
| [AgentSpec](agentspec/) | 5-phase pipeline with quality gates |

### Need: Better Memory/Persistence

| Framework | What It Offers |
|-----------|----------------|
| [Beads](beads/) | Git-backed graph issue tracking, dependency DAG |
| [Supermemory](supermemory/) | Hybrid retrieval (81.6% accuracy), auto-capture |
| [Claude-Mem](claude-mem/) | Progressive disclosure, compression |

### Need: Better Orchestration

| Framework | What It Offers |
|-----------|----------------|
| [Gas Town](gastown/) | 20-30 agent scale, convoys, external state |
| [Claude-Flow](claude-flow/) | Swarm topologies, consensus protocols, WASM |
| [Cipher](cipher/) | MCP aggregation, dual memory architecture |

### Need: Better Iteration/Verification

| Framework | What It Offers |
|-----------|----------------|
| [Ralph-Wiggum](ralph-wiggum/) | Self-referential loops, promise gates |
| [Superpowers](superpowers/) | Two-stage review, verification discipline |
| [Claude-Workflow](claude-workflow/) | Hierarchical task numbering, validation gates |

---

## Curated Resources

### Awesome Claude Code Collection

The [awesome-claude-code-curated/](awesome-claude-code-curated/) collection filters the community's 197 resources to identify the **25 highest-value tools, skills, and patterns** for our Jarvis/AgentSpec setup.

| Document | Purpose |
|----------|---------|
| [RECOMMENDATIONS.md](awesome-claude-code-curated/RECOMMENDATIONS.md) | Prioritized adoption roadmap |
| [top-picks.md](awesome-claude-code-curated/top-picks.md) | Detailed analysis of top 20 resources |
| [adoption-guide.md](awesome-claude-code-curated/adoption-guide.md) | Step-by-step installation guides |

**Top Recommendations:**
- **cchooks** - Python SDK for hooks
- **claude-code-tools** - Session continuity
- **TDD Guard** - Test-first enforcement
- **Claude Squad** - Multi-agent workspaces

See [awesome-claude-code-curated/index.md](awesome-claude-code-curated/index.md) for full details.

---

## Related KBs

- **SDD KB** (`.claude/kb/sdd/`) - Deep dive on Spec-Driven Development methodology
- **Jarvis Base KB** (`.claude/kb/jarvis-base/`) - Jarvis system architecture
- **Awesome Claude Code** (`.claude/kb/frameworks/awesome-claude-code-curated/`) - Curated community resources

---

## Research Sources

| Source | Usage |
|--------|-------|
| Context7 MCP | Primary documentation source |
| Local repos | Code analysis (`D:/Workspace/Claude Code/Repositorios/frameworks-research/`) |
| WebSearch | Community resources, tutorials |
| Official docs | Framework-specific documentation |

---

## Completion Statistics

| Metric | Value |
|--------|-------|
| Frameworks Researched | 11/11 |
| Documents Created | 33/33 |
| Total KB Size | ~120 KB |
| Research Duration | ~2 hours |
| Completion Date | 2026-02-03 |

---

*Created: 2026-02-02 | Completed: 2026-02-03 | Sprint: S03*
