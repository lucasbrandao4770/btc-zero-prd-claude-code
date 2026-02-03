# Beads - Jarvis Integration Analysis

> Evaluating Beads for integration with or inspiration for Jarvis system

---

## Integration Summary

| Aspect | Assessment |
|--------|------------|
| **Integration Difficulty** | Medium |
| **Value to Jarvis** | High |
| **Conflict Level** | Minor |
| **Recommendation** | **Learn From** |

---

## Comparison Matrix

### Feature-by-Feature

| Feature | Beads | Jarvis Current | Winner | Notes |
|---------|-------|----------------|--------|-------|
| **Persistent Memory** | SQLite + JSONL with git sync | jarvis-crud SQLite | Beads | Beads adds git distribution |
| **Session Recovery** | `bd prime` + hooks | PreCompact/Stop hooks | Tie | Both use hooks for context injection |
| **Task Tracking** | Graph-based issues with deps | PROGRESS.md files | Beads | Graph enables dependency-aware execution |
| **Sprint/Goal Management** | Priority-based queues | Sprint/goal tracking | Jarvis | Jarvis has richer goal semantics |
| **Multi-Agent Support** | Hash IDs prevent collisions | Not explicitly designed | Beads | Beads handles parallel agent creation |
| **Offline Support** | Git-backed, full offline | SQLite local | Beads | Beads adds git portability |
| **Context Window Mgmt** | Compaction/decay | Auto-compact recovery | Tie | Different approaches, both effective |
| **Workflow Templates** | Molecules/Wisps | Agent catalog + skills | Jarvis | Jarvis has richer agent composition |

### Architectural Comparison

| Aspect | Beads | Jarvis |
|--------|-------|--------|
| **Core Philosophy** | Git-backed issue tracker for agents | Comprehensive AI assistant ecosystem |
| **State Management** | Three-layer: CLI -> SQLite -> JSONL -> Git | Two-layer: hooks -> SQLite (jarvis-crud) |
| **Agent Model** | Single agent per session, sync via git | Multi-agent with catalogs and specialization |
| **Memory System** | JSONL in git + local SQLite cache | SQLite via jarvis-crud + CLAUDE.md |
| **Planning Approach** | Dependency graph + ready-work queue | Sprint/goal hierarchy + session planning |

---

## What Jarvis Can Learn

### Ideas to Adopt

1. **Dependency-Aware Task Graph**
   - What: Model tasks as DAG with `blocks`, `parent-child`, `related` relationships
   - Why: Enables `ready-work` computation - always know what's actionable
   - How: Extend jarvis-crud schema with `dependencies` table and relationship types
   - Effort: Medium (schema change + query logic)

2. **Hash-Based IDs for Collision-Free Creation**
   - What: Use content-derived hashes instead of sequential IDs
   - Why: Enables parallel task creation without coordination
   - How: Generate UUID, derive short hash, scale length as database grows
   - Effort: Low (ID generation change)

3. **"Landing the Plane" Protocol**
   - What: Mandatory session completion workflow: sync -> push -> verify
   - Why: Ensures no work stranded locally, enables multi-session continuity
   - How: Add to Jarvis Stop hook: verify all changes committed and pushed
   - Effort: Low (hook enhancement)

4. **Compaction for Context Management**
   - What: Summarize old closed tasks to reduce context window usage
   - Why: Maintains history awareness without token overhead
   - How: Add `jarvis-crud compact` that digests old completed items
   - Effort: Medium (new command + summarization logic)

### Patterns to Study

| Pattern | Beads Implementation | Jarvis Adaptation |
|---------|----------------------|-------------------|
| **Three-Layer Sync** | SQLite -> JSONL -> Git | Could add JSONL export for portability |
| **Ready-Work Queue** | `bd ready` with blocked cache | Add `jarvis-crud ready` for unblocked tasks |
| **Prime Context** | `bd prime` injects ~1-2K tokens | Similar to CLAUDE.md loading |
| **Content Hashing** | Detect changes by hash comparison | Use for sync conflict detection |
| **Debounced Export** | 5-second batch window | Apply to jarvis-crud writes |

---

## Conflicts & Incompatibilities

### Philosophical Conflicts

| Jarvis Principle | Beads Approach | Resolution |
|------------------|---------------|------------|
| **Rich Agent Ecosystem** | Single-agent focus with git sync | Keep Jarvis multi-agent, adopt sync patterns |
| **Integrated Assistant** | Pure issue tracker | Beads complements, doesn't replace |
| **CLAUDE.md as Truth** | JSONL + SQLite as truth | Can coexist - different purposes |

### Technical Conflicts

| Jarvis Component | Beads Conflict | Impact |
|------------------|---------------|--------|
| **jarvis-crud** | Different schema | Minor - can extend, not replace |
| **PROGRESS.md** | Replaced by graph | Minor - migration path exists |
| **Sprint tracking** | No direct equivalent | None - Jarvis feature, not conflict |

---

## Integration Options

### Option A: Full Integration

**Description:** Replace jarvis-crud with Beads as primary task/memory system

| Pros | Cons |
|------|------|
| Git sync for distributed Jarvis | Lose custom Jarvis schema extensions |
| Dependency-aware execution | Learning curve for Beads concepts |
| Community tooling | Two systems to maintain during transition |

**Effort:** 3-4 weeks
**Risk:** High - major architectural change

### Option B: Partial Adoption

**Description:** Keep jarvis-crud, add Beads-inspired features

| Components to Adopt | Components to Skip |
|--------------------|-------------------|
| Dependency tracking | Full JSONL sync |
| Hash-based IDs | Molecule/wisp system |
| Ready-work query | Daemon architecture |
| Landing protocol | MCP server |

**Effort:** 1-2 weeks
**Risk:** Low - additive changes only

### Option C: Learn & Adapt (Recommended)

**Description:** Study Beads patterns, implement key concepts natively in Jarvis

**Key Learnings to Apply:**

1. **Add dependency table to jarvis-crud**
   ```sql
   CREATE TABLE task_dependencies (
     from_id TEXT NOT NULL,
     to_id TEXT NOT NULL,
     dep_type TEXT NOT NULL,  -- blocks, related, parent-child
     PRIMARY KEY (from_id, to_id)
   );
   ```

2. **Implement ready-work query**
   ```bash
   jarvis-crud tasks ready  # Tasks with no open blockers
   ```

3. **Add landing-the-plane to Stop hook**
   ```markdown
   ## Session Completion Checklist
   - [ ] All changes committed
   - [ ] Pushed to remote
   - [ ] Next session handoff documented
   ```

4. **Hash-based task IDs**
   - Generate: `jarvis-{short-hash}` instead of sequential
   - Enables parallel creation without conflicts

---

## Cost-Benefit Analysis

### Benefits

| Benefit | Impact | Confidence |
|---------|--------|------------|
| Dependency-aware task execution | High | High |
| Collision-free multi-agent creation | Medium | High |
| Better session handoff protocol | Medium | High |
| Context window optimization via compaction | Medium | Medium |
| Git-portable state (optional) | Low | Medium |

### Costs

| Cost | Type | Estimate |
|------|------|----------|
| Schema migration | Time | 2-3 days |
| Learning Beads concepts | Complexity | 1 day |
| Testing dependency logic | Time | 2-3 days |
| Documentation updates | Time | 1 day |

### ROI Assessment

**High ROI for Option C (Learn & Adapt).**

Beads solves real problems (agent amnesia, dependency tracking, collision-free IDs) that would benefit Jarvis. However, full integration would be disruptive and Jarvis already has a working memory system.

The sweet spot is adopting key patterns (dependency graph, ready-work, landing protocol) while keeping Jarvis's richer ecosystem (agents, skills, sprints, goals).

---

## Implementation Roadmap

If proceeding with Option C (Learn & Adapt):

### Phase 1: Foundation (Week 1)
- [ ] Add `task_dependencies` table to jarvis-crud schema
- [ ] Implement `jarvis-crud tasks ready` command
- [ ] Add hash-based ID generation option
- [ ] Document new dependency model

### Phase 2: Integration (Week 2)
- [ ] Update PROGRESS.md format to include dependencies
- [ ] Add "landing the plane" checklist to Stop hook
- [ ] Implement blocked-issues cache for performance
- [ ] Add `jarvis-crud compact` for old task summarization

### Phase 3: Polish (Week 3)
- [ ] Update agent catalogs to use dependency-aware tasks
- [ ] Add dependency visualization to status commands
- [ ] Write migration guide for existing workflows
- [ ] Performance testing with large task sets

---

## Decision

### Recommendation

**Learn From**

### Rationale

1. **Beads solves real problems** - Dependency tracking and collision-free IDs would genuinely improve Jarvis task management.

2. **Full integration is overkill** - Jarvis already has a working memory system (jarvis-crud) with features Beads lacks (sprints, goals, rich agent ecosystem).

3. **Key patterns are portable** - The valuable innovations (graph-based deps, hash IDs, landing protocol, compaction) can be implemented in jarvis-crud without adopting the full Beads system.

4. **Maintain ecosystem coherence** - Jarvis is more than task tracking; it's an integrated assistant platform. Adding another full system would fragment the architecture.

### Next Steps

1. **Study Beads internals** - Read `blocked_cache.go` and `dependencies.go` for implementation patterns
2. **Prototype dependency table** - Add to jarvis-crud and test with existing workflows
3. **Implement ready-work query** - Most valuable single feature to adopt
4. **Add landing protocol** - Low-effort, high-value session completion improvement

---

*Integration analysis completed: 2026-02-03 | Analyst: kb-architect*
