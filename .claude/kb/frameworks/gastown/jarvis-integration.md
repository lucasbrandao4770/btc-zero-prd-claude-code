# Gas Town - Jarvis Integration Analysis

> Evaluating Gas Town for integration with or inspiration for Jarvis system

---

## Integration Summary

| Aspect | Assessment |
|--------|------------|
| **Integration Difficulty** | Hard |
| **Value to Jarvis** | High |
| **Conflict Level** | Major |
| **Recommendation** | Learn From |

---

## Comparison Matrix

### Feature-by-Feature

| Feature | Gas Town | Jarvis Current | Winner | Notes |
|---------|----------|----------------|--------|-------|
| Agent Spawning | Dedicated Polecats in git worktrees | Task tool spawns subagents | Gas Town | Isolated execution environments |
| State Persistence | Git-backed Beads/Hooks | Domain memory pattern | Gas Town | Survives crashes, restarts |
| Agent Selection | Capability routing from CV | Category-based selection | Gas Town | Data-driven vs. static categories |
| Parallel Execution | 20-30 simultaneous agents | Sandbox SWARM (limited) | Gas Town | Purpose-built for massive parallelism |
| Work Tracking | Convoys with cross-rig visibility | Progress files, logs | Gas Town | First-class tracking primitive |
| Agent Handoff | `gt handoff` with context transfer | Manual session notes | Gas Town | Formal handoff protocol |
| Context Optimization | External state in Beads | R&D Framework in-context | Tie | Different approaches, both effective |
| Ease of Use | Complex setup, tmux required | Simple prompt activation | Jarvis | Jarvis is zero-setup |
| Windows Support | Limited (tmux dependency) | Full Windows support | Jarvis | Critical for our environment |

### Architectural Comparison

| Aspect | Gas Town | Jarvis |
|--------|----------|--------|
| Core Philosophy | External state, massive parallelism | In-context intelligence, delegation chain |
| State Management | Git-backed Beads ledger (external) | Hooks, memory files (semi-external) |
| Agent Model | Named slots with CVs (Toast, Shadow) | 44 specialized agents by category |
| Memory System | Hooks + Seance (talk to past sessions) | Domain memory pattern, CLAUDE.md |
| Planning Approach | Mayor decomposes, Convoys track | User-driven with /brainstorm, /define |
| Coordination | Mail, Nudges, Hooks | Task tool, direct context passing |
| Recovery | `gt prime` after compaction | PreCompact/UserPromptSubmit hooks |

---

## What Jarvis Can Learn

### Ideas to Adopt

1. **The Propulsion Principle**
   - What: "If work appears on your hook, YOU MUST RUN IT" - agents execute immediately without waiting for confirmation
   - Why: Eliminates coordination overhead and "are you ready?" loops
   - How: Add propulsion-style triggers to Sandbox mode - when a HANDOFF file appears, agent should auto-execute
   - Effort: Low

2. **Agent CVs / Work History**
   - What: Track each agent's completions, success rates, and demonstrated skills
   - Why: Enable data-driven agent selection instead of static category matching
   - How: Add completion tracking to Task tool results; query history for agent selection
   - Effort: Medium

3. **Convoy-Style Work Tracking**
   - What: First-class tracking unit for batched work across multiple agents
   - Why: Jarvis SWARM lacks unified progress visibility
   - How: Enhance HANDOFF v3.0 with convoy-like tracking across chunks
   - Effort: Medium

4. **Self-Cleaning Agents**
   - What: Agents responsible for their own cleanup on completion
   - Why: Reduces coordination burden on main orchestrator
   - How: Standardize "completion protocol" for subagents (cleanup, notify, exit)
   - Effort: Low

### Patterns to Study

| Pattern | Gas Town Implementation | Jarvis Adaptation |
|---------|-------------------------|-------------------|
| External State | Git-backed Beads ledger | Enhance domain memory with structured work tracking |
| Handoff Protocol | `gt handoff` transfers context to fresh session | Formalize handoff between subagents |
| Seance | Query previous sessions for context | Add "past session query" capability |
| Molecule Navigation | `bd mol current` shows step progress | Add step tracking to Dev Loop |
| Redundant Observation | Multiple agents can check convoy status | Allow multiple reviewers in SWARM |

---

## Conflicts & Incompatibilities

### Philosophical Conflicts

| Jarvis Principle | Gas Town Approach | Resolution |
|------------------|-------------------|------------|
| Zero-setup activation | Requires `gt install`, tmux, beads | Cannot reconcile - learn concepts, not tooling |
| Windows-first | macOS/Linux with tmux | Cannot adopt core execution model |
| In-context state | External git-backed state | Adopt select external patterns (work tracking) |
| Single coordinator | Distributed coordination (Mayor, Witness, Deacon) | Keep Jarvis's simpler model |

### Technical Conflicts

| Jarvis Component | Gas Town Conflict | Impact |
|------------------|-------------------|--------|
| Task tool | Assumes in-process subagents | Cannot use Gas Town's worktree isolation |
| Windows terminal | Tmux dependency | Fundamental incompatibility |
| Agent catalog | Gas Town uses dynamic CV routing | Would need to rewrite agent selection |
| Context hooks | Gas Town uses mail/nudge system | Different IPC mechanism |

---

## Integration Options

### Option A: Full Integration

**Description:** Replace Jarvis orchestration with Gas Town entirely

| Pros | Cons |
|------|------|
| Proven at scale (20-30 agents) | Breaks Windows support |
| Enterprise-grade audit trails | Complete rewrite of agent system |
| Persistent state | Learning curve for users |
| Capability routing | Requires tmux infrastructure |

**Effort:** 3-4 weeks
**Risk:** High - platform incompatibility

### Option B: Partial Adoption

**Description:** Adopt Gas Town's Beads system for work tracking

| Components to Adopt | Components to Skip |
|--------------------|-------------------|
| Beads work tracking | Polecat execution model |
| Convoy visibility | Tmux session management |
| Agent attribution | Mail/nudge IPC |
| CV work history | Git worktree isolation |

**Effort:** 2-3 weeks
**Risk:** Medium - adds dependency on Beads CLI

### Option C: Learn & Adapt (Recommended)

**Description:** Extract valuable patterns and implement Jarvis-native versions

**Key Learnings to Apply:**

1. **Propulsion Pattern**: Add auto-execution trigger when HANDOFF files appear
2. **Work Tracking**: Enhance SWARM with convoy-like progress tracking
3. **Agent History**: Track subagent completion rates for routing decisions
4. **Self-Cleanup**: Standardize subagent completion protocol
5. **Handoff Protocol**: Formalize context transfer between sessions

**Effort:** 1-2 weeks for core patterns
**Risk:** Low - incremental improvements

---

## Cost-Benefit Analysis

### Benefits

| Benefit | Impact | Confidence |
|---------|--------|------------|
| Better SWARM visibility | High | High |
| Reduced coordination overhead | Medium | Medium |
| Agent performance insights | Medium | Medium |
| Formal handoff protocol | Medium | High |
| Inspiration for scaling | High | High |

### Costs

| Cost | Type | Estimate |
|------|------|----------|
| Learning Gas Town concepts | Time | 1-2 days |
| Implementing Jarvis adaptations | Time | 1-2 weeks |
| Documentation updates | Time | 2-3 hours |
| Testing new patterns | Time | 1 week |

### ROI Assessment

**High positive ROI for Option C (Learn & Adapt)**. Gas Town represents cutting-edge thinking about multi-agent orchestration from a veteran developer (Yegge). The concepts are valuable even without adopting the tooling. The Propulsion Principle alone could significantly improve Sandbox mode efficiency.

Full integration (Option A) has negative ROI due to platform incompatibility with Windows.

---

## Implementation Roadmap

If proceeding with Option C (Learn & Adapt):

### Phase 1: Propulsion Pattern (1 week)

- [ ] Add trigger detection for HANDOFF files in Sandbox mode
- [ ] Implement auto-execution when work appears
- [ ] Remove confirmation loops in autonomous mode
- [ ] Test with existing SWARM workflows

### Phase 2: Work Tracking (1 week)

- [ ] Design convoy-like tracking for HANDOFF v3.0
- [ ] Add progress visibility across chunks
- [ ] Implement completion notifications
- [ ] Create `gt convoy list`-style command for Jarvis

### Phase 3: Agent History (Future)

- [ ] Track subagent completion rates in memory files
- [ ] Query history during agent selection
- [ ] Build skill profiles from task completions
- [ ] Enable capability-based routing

---

## Decision

### Recommendation

**Learn From**

### Rationale

Gas Town represents sophisticated multi-agent thinking but is fundamentally incompatible with Jarvis's execution environment (Windows, in-process subagents). The conceptual patterns - Propulsion Principle, Convoy tracking, Agent CVs, Self-cleaning workers - are highly valuable and can be adapted to Jarvis without taking on Gas Town's infrastructure dependencies.

Key factors:
1. **Platform mismatch**: Gas Town requires tmux (macOS/Linux) while Jarvis needs Windows support
2. **Architecture difference**: Gas Town uses external processes in git worktrees; Jarvis uses Task tool with in-context subagents
3. **Concept value**: The ideas (propulsion, attribution, convoy tracking) are portable even if the tooling isn't
4. **Risk reduction**: Adopting patterns incrementally preserves Jarvis stability

### Next Steps

1. Read Gas Town's glossary and concept docs for deep understanding
2. Implement Propulsion Pattern in Sandbox mode
3. Design convoy-like tracking for HANDOFF v3.0
4. Document adapted patterns in Jarvis KB
5. Monitor Gas Town evolution for future inspiration

---

*Integration analysis completed: 2026-02-03 | Sources: Local repo, GitHub, Web Search*
