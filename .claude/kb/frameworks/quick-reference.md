# Frameworks Quick Reference

> Cheat sheet for all 11 Claude Code ecosystem frameworks

---

## At a Glance

| Framework | One-Line Summary | Best For |
|-----------|------------------|----------|
| **Superpowers** | Composable skills with mandatory TDD enforcement | Discipline & verification |
| **Spec-Kit** | GitHub's spec-first toolkit with user story independence | Structured specification |
| **Claude-Workflow** | GitHub Issues-based task decomposition | Hierarchical task breaking |
| **Beads** | Git-backed graph issue tracker for agent memory | Persistent task tracking |
| **Supermemory** | Cloud semantic memory with hybrid retrieval | Cross-session memory |
| **Claude-Mem** | Context compression with progressive disclosure | Token optimization |
| **Gas Town** | 20-30 agent orchestration with tmux convoys | Large-scale swarms |
| **Claude-Flow** | Enterprise swarm with consensus protocols | Fault-tolerant coordination |
| **Cipher** | Memory layer with MCP aggregation | Tool unification |
| **Ralph-Wiggum** | Stop hook for self-referential development loops | Autonomous iteration |
| **AgentSpec** | 5-phase SDD pipeline with quality gates | Feature delivery |

---

## Patterns Worth Stealing

### High Priority (Adopt Now)

| Pattern | From | Implementation |
|---------|------|----------------|
| **Verification-before-completion** | Superpowers | Add to all build/ship phases |
| **Completion Promise Protocol** | Ralph-Wiggum | `<promise>DONE</promise>` gates |
| **Propulsion Principle** | Gas Town | Auto-execute on HANDOFF files |
| **Progressive disclosure** | Claude-Mem | `--summary` mode for queries |

### Medium Priority (Plan for Later)

| Pattern | From | Implementation |
|---------|------|----------------|
| **Dependency DAG** | Beads | Add `task_dependencies` table |
| **Two-stage review** | Superpowers | Spec review → quality review |
| **Anti-drift defaults** | Claude-Flow | Hierarchical + specialized + raft |
| **Auto-capture hooks** | Supermemory | Session summary on Stop |

### Lower Priority (Study for Ideas)

| Pattern | From | Potential Use |
|---------|------|---------------|
| **User story independence** | Spec-Kit | MVP increment validation |
| **WASM Agent Booster** | Claude-Flow | Fast simple transforms |
| **Dual memory architecture** | Cipher | Knowledge vs reflection split |
| **Convoy tracking** | Gas Town | Unified swarm progress |

---

## Framework Comparison Matrix

### Planning Approaches

| Framework | Planning Style | Phases | Artifacts |
|-----------|---------------|--------|-----------|
| Superpowers | Skills-driven | Brainstorm → Plan → Execute | plan.md |
| Spec-Kit | Constitution-first | 6 phases | DEFINE.md, DESIGN.md, tasks.md |
| Claude-Workflow | Issues-driven | Detect → Break → Execute | GitHub Issues |
| AgentSpec | Artifact-driven | 5 phases | DEFINE.md, DESIGN.md |

### Memory Approaches

| Framework | Storage | Retrieval | Persistence |
|-----------|---------|-----------|-------------|
| Beads | SQLite + JSONL | Dependency graph | Git-backed |
| Supermemory | Cloud API | Hybrid (81.6%) | Cloud |
| Claude-Mem | SQLite + Chroma | Progressive | Local |
| Cipher | Vector DB | Semantic search | Configurable |

### Orchestration Approaches

| Framework | Scale | Coordination | State |
|-----------|-------|--------------|-------|
| Gas Town | 20-30 agents | Propulsion + Hooks | External (git) |
| Claude-Flow | Enterprise | Consensus protocols | Distributed |
| Cipher | Tool-level | MCP aggregation | Vector DB |

---

## Decision Tree: Which Framework to Study?

```
What do you need?
│
├─ Better discipline/verification?
│  └─ Study: Superpowers, Ralph-Wiggum
│
├─ Better planning/specification?
│  └─ Study: Spec-Kit, AgentSpec
│
├─ Better memory/persistence?
│  └─ Study: Beads (local), Supermemory (cloud), Claude-Mem (compression)
│
├─ Better multi-agent orchestration?
│  └─ Study: Gas Town (scale), Claude-Flow (enterprise)
│
└─ Better tool organization?
   └─ Study: Cipher (MCP aggregation)
```

---

## Key Authors

| Author | Frameworks | Notable For |
|--------|------------|-------------|
| **Steve Yegge** | Beads, Gas Town | External state, scale |
| **Jesse Vincent (obra)** | Superpowers | TDD discipline |
| **GitHub** | Spec-Kit | SDD methodology |
| **Anthropic** | Ralph-Wiggum | Stop hook iteration |
| **ruvnet** | Claude-Flow | Enterprise patterns |
| **Byterover** | Cipher | MCP aggregation |

---

## Integration Status with Jarvis

| Status | Frameworks |
|--------|------------|
| **Already Integrated** | AgentSpec |
| **Adapt (cherry-pick patterns)** | Superpowers, Ralph-Wiggum |
| **Learn From (study patterns)** | All others |

---

## Community Resources (Curated)

The [awesome-claude-code-curated/](awesome-claude-code-curated/) collection identifies top tools from 197 community resources:

| Category | Top Picks | Week |
|----------|-----------|------|
| **Skills** | Everything Claude Code, cc-devops-skills, Trail of Bits | 1-2 |
| **Hooks** | cchooks (Python SDK), TDD Guard, HCOM | 1-3 |
| **Tooling** | claude-code-tools, Claude Squad, viwo-cli | 2-3 |
| **Workflows** | System Prompts, Claude CodePro, Tips Collection | 1-3 |
| **Commands** | /prd-generator, /tdd, n8n cherry-picks | 3-4 |

**Quick Start:** See [RECOMMENDATIONS.md](awesome-claude-code-curated/RECOMMENDATIONS.md)

---

## Links

| Resource | Path |
|----------|------|
| Full KB Index | [index.md](index.md) |
| Curated Resources | [awesome-claude-code-curated/](awesome-claude-code-curated/) |
| Templates | [_templates/](_templates/) |
| Jarvis Base KB | [../jarvis-base/](../jarvis-base/) |
| Local Repos | `D:/Workspace/Claude Code/Repositorios/frameworks-research/` |

---

*Quick reference created: 2026-02-03 | Sprint: S03*
