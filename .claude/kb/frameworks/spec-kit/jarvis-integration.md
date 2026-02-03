# Spec-Kit - Jarvis Integration Analysis

> Evaluating Spec-Kit for integration with or inspiration for Jarvis SDD system (AgentSpec 4.2)

---

## Integration Summary

| Aspect | Assessment |
|--------|------------|
| **Integration Difficulty** | Medium |
| **Value to Jarvis** | High |
| **Conflict Level** | Minor |
| **Recommendation** | **Learn From** - Adopt specific patterns without full integration |

---

## Comparison Matrix

### Feature-by-Feature

| Feature | Spec-Kit | Jarvis (AgentSpec 4.2) | Winner | Notes |
|---------|----------|------------------------|--------|-------|
| **Workflow Phases** | 6 phases: Constitution, Specify, Clarify, Plan, Tasks, Implement | 5 phases: Brainstorm, Define, Design, Build, Ship | Tie | Similar philosophy, different naming |
| **Spec Creation** | `/speckit.specify` - Natural language to spec.md | `/define` - Requirements to DEFINE_*.md | Spec-Kit | More structured template with P1/P2/P3 priorities |
| **Tech Planning** | `/speckit.plan` - Separate from spec | Part of `/design` - Inline with architecture | Jarvis | Design doc is more comprehensive |
| **Task Breakdown** | `/speckit.tasks` - Explicit phase with tasks.md | On-the-fly from file manifest in DESIGN | Spec-Kit | Explicit task ordering is more traceable |
| **Clarification** | `/speckit.clarify` - Max 3 questions, structured | Inline in /brainstorm or /define | Spec-Kit | Structured clarification prevents question dumps |
| **User Stories** | Priority-ordered (P1, P2, P3) with independence | Goals with MUST/SHOULD/COULD priority | Spec-Kit | User story independence enables incremental MVPs |
| **Constitutional Governance** | Explicit constitution.md with Articles | Implicit in CLAUDE.md and agent rules | Spec-Kit | Explicit principles are more discoverable |
| **Branch Management** | Auto-creates NNN-feature-name branches | Manual branch creation | Spec-Kit | Automation reduces cognitive load |
| **Quality Gates** | Checklists before each phase | Clarity Score (12/15) before Design | Tie | Both have quality gates, different mechanisms |
| **Agent Support** | 17+ AI assistants | Claude Code only | Spec-Kit | Multi-agent support is more flexible |
| **Iteration** | Re-run any command | `/iterate` for any phase | Jarvis | Dedicated iteration command is cleaner |
| **Agent Delegation** | None - single execution stream | Agent Matching + Delegation in Build | Jarvis | Specialist agents per file is powerful |
| **Archival** | No explicit archival | `/ship` with lessons learned | Jarvis | Archival preserves institutional knowledge |
| **Exploratory Phase** | Via clarify or iterative specify | `/brainstorm` for vague ideas | Jarvis | Brainstorm for discovery is valuable |

### Architectural Comparison

| Aspect | Spec-Kit | Jarvis |
|--------|----------|--------|
| **Core Philosophy** | Specifications are executable; code serves specs | Specs guide implementation; on-the-fly execution |
| **State Management** | Files only (spec.md, plan.md, tasks.md) | Files only (DEFINE, DESIGN, BUILD_REPORT) |
| **Agent Model** | Single AI assistant executes all phases | Multiple specialists per file (Agent Matching) |
| **Memory System** | constitution.md as persistent rules | CLAUDE.md + kb/ as persistent context |
| **Planning Approach** | Separate specification and planning phases | Unified Design phase with inline decisions |
| **Task Generation** | Explicit task file before implementation | On-the-fly from file manifest during Build |

---

## What Jarvis Can Learn

### Ideas to Adopt

1. **Explicit Task Breakdown Phase**
   - What: Add a `/tasks` command between Design and Build that generates a tasks.md file
   - Why: Makes execution order explicit and traceable; enables parallel task markers [P]
   - How: Create a TASKS_TEMPLATE.md that parses DESIGN file manifest into ordered tasks
   - Effort: Medium (new command + template + agent)

2. **User Story Independence Pattern**
   - What: Structure DEFINE to ensure each goal/requirement can be independently testable
   - Why: Enables incremental MVP delivery; reduces risk of blocked features
   - How: Add "Independent Test" section to DEFINE template for each goal
   - Effort: Low (template update)

3. **Structured Clarification with Limits**
   - What: Cap clarification questions at 3, require structured options table format
   - Why: Prevents "question dump" anti-pattern that overwhelms users
   - How: Add clarification limit rule to /brainstorm and /define agents
   - Effort: Low (agent prompt update)

4. **Explicit Constitutional Governance**
   - What: Create a CONSTITUTION.md with immutable project principles
   - Why: Makes architectural decisions explicit and enforceable across sessions
   - How: Template for constitution with Articles structure, referenced by all agents
   - Effort: Medium (new file type + cross-agent reference)

5. **Automatic Branch Naming**
   - What: Auto-generate feature branches with sequential numbering (001-feature-name)
   - Why: Reduces cognitive load; ensures consistent naming
   - How: Add script to /define that creates branch from feature name
   - Effort: Low (script addition)

### Patterns to Study

| Pattern | Spec-Kit Implementation | Jarvis Adaptation |
|---------|-------------------------|-------------------|
| **Priority Ordering** | P1/P2/P3 user story priorities | Add priority field to Goals in DEFINE template |
| **Checklist Gates** | checklists/*.md before each phase | Add checklist validation to phase transitions |
| **Technology-Agnostic Specs** | Strict WHAT/WHY separation in spec.md | Enforce "no tech stack" rule in DEFINE more strictly |
| **Cross-Artifact Analysis** | `/speckit.analyze` for consistency | Add /analyze command to check DEFINE-DESIGN consistency |
| **Research Documents** | Separate research.md for tech decisions | Add research section to DESIGN or create RESEARCH_*.md |

---

## Conflicts & Incompatibilities

### Philosophical Conflicts

| Jarvis Principle | Spec-Kit Approach | Resolution |
|------------------|-------------------|------------|
| On-the-fly task generation | Explicit tasks.md file | **Adopt Spec-Kit**: Explicit tasks improve traceability |
| Agent delegation per file | Single execution stream | **Keep Jarvis**: Specialist agents are a strength |
| BRAINSTORM for exploration | Clarify for gaps only | **Keep Both**: Brainstorm for discovery, clarify for gaps |

### Technical Conflicts

| Jarvis Component | Spec-Kit Conflict | Impact |
|------------------|-------------------|--------|
| File Naming | `DEFINE_*.md` vs `spec.md` | Minor - naming preference only |
| Directory Structure | `.claude/sdd/` vs `.specify/specs/` | Minor - can coexist or migrate |
| Branch Workflow | Manual | None - Jarvis can adopt auto-branching |
| Agent System | Multi-agent | None - Spec-Kit has no agent system to conflict |

---

## Integration Options

### Option A: Full Integration

**Description:** Replace Jarvis SDD with Spec-Kit wholesale, adopting their templates and commands.

| Pros | Cons |
|------|------|
| Leverage active community | Lose agent delegation capability |
| Multi-AI support | Lose /brainstorm exploration phase |
| Established templates | Lose /ship archival with lessons |
| GitHub backing | Requires team retraining |

**Effort:** 2-3 days migration
**Risk:** High - loses Jarvis-specific capabilities

### Option B: Partial Adoption

**Description:** Adopt specific Spec-Kit patterns while keeping Jarvis architecture.

| Components to Adopt | Components to Skip |
|--------------------|-------------------|
| Explicit task breakdown (tasks.md) | Directory restructuring |
| User story independence pattern | Multi-AI support (not needed) |
| Structured clarification limits | Constitutional articles (use CLAUDE.md instead) |
| Priority ordering (P1/P2/P3) | Branch auto-naming (can add later) |
| Cross-artifact analysis | New file naming conventions |

**Effort:** 1-2 days
**Risk:** Low - additive changes only

### Option C: Learn & Adapt (Recommended)

**Description:** Study Spec-Kit patterns and selectively incorporate the best ideas into Jarvis without direct integration.

**Key Learnings to Apply:**

1. **Add /tasks command** - Create explicit task breakdown phase between Design and Build
2. **Clarification limits** - Cap at 3 questions with structured options table
3. **Priority ordering** - Add P1/P2/P3 to Goals in DEFINE template
4. **Independence validation** - Add "Independent Test" field to each goal
5. **Cross-artifact analysis** - Add /analyze command for consistency checking

**Effort:** 3-5 days (spread across multiple improvements)
**Risk:** Low - incremental improvements

---

## Cost-Benefit Analysis

### Benefits

| Benefit | Impact | Confidence |
|---------|--------|------------|
| Better task traceability | High | High |
| Reduced question overload | Medium | High |
| Clearer prioritization | Medium | Medium |
| Incremental MVP delivery | High | Medium |
| Consistency validation | Medium | Medium |

### Costs

| Cost | Type | Estimate |
|------|------|----------|
| Template updates | Time | 2-4 hours |
| New /tasks command | Complexity | 4-6 hours |
| Agent prompt updates | Time | 1-2 hours |
| Documentation updates | Time | 2-3 hours |
| Team communication | Time | 1 hour |

### ROI Assessment

**High ROI for targeted adoption.** The explicit task breakdown and user story independence patterns address real gaps in Jarvis workflow without requiring architectural changes. The structured clarification limits improve user experience immediately.

Full integration is **not recommended** because Jarvis's agent delegation system and /brainstorm exploration phase are unique strengths that Spec-Kit lacks.

---

## Implementation Roadmap

If proceeding with Option C (Learn & Adapt):

### Phase 1: Template Enhancements (Week 1)

- [ ] Add P1/P2/P3 priority field to DEFINE template Goals section
- [ ] Add "Independent Test" field to each goal in DEFINE template
- [ ] Add clarification limit (max 3) rule to brainstorm-agent and define-agent
- [ ] Update DEFINE_TEMPLATE.md with structured clarification table format

### Phase 2: Task Breakdown Command (Week 2)

- [ ] Create TASKS_TEMPLATE.md based on Spec-Kit tasks-template.md
- [ ] Create /tasks command that parses DESIGN file manifest
- [ ] Add [P] parallel markers and user story grouping
- [ ] Update build-agent to consume tasks.md if present

### Phase 3: Analysis & Validation (Week 3)

- [ ] Create /analyze command for cross-artifact consistency checking
- [ ] Add phase gate checklists to command transitions
- [ ] Document new patterns in SDD _index.md

---

## Decision

### Recommendation

**Learn From** - Adopt specific patterns without full integration

### Rationale

1. **Complementary Strengths**: Spec-Kit excels at structured specification and task breakdown; Jarvis excels at agent delegation and exploratory brainstorming. Combining the best of both creates a stronger system.

2. **Low Migration Risk**: Adopting patterns (task breakdown, clarification limits, priority ordering) is additive and doesn't require replacing existing Jarvis infrastructure.

3. **Preserves Jarvis Uniqueness**: Agent Matching and Delegation in Build phase is a key differentiator that Spec-Kit doesn't have. Full integration would lose this capability.

4. **Active Development Alignment**: Both systems are actively evolving. Learning patterns is more sustainable than tight coupling to an external project.

### Next Steps

1. **Immediate** - Add clarification limits (max 3) to brainstorm-agent and define-agent prompts
2. **Short-term** - Create TASKS_TEMPLATE.md and /tasks command prototype
3. **Medium-term** - Update DEFINE template with priority ordering and independence testing
4. **Long-term** - Evaluate creating CONSTITUTION.md for explicit project principles (relates to future SDD KB, QW-010)

---

## Related Work

- **QW-010: SDD Knowledge Base** - Future KB domain for documenting Jarvis SDD methodology, incorporating learnings from Spec-Kit analysis
- **AgentSpec 4.2** - Current Jarvis SDD workflow documented in `.claude/sdd/_index.md`
- **Spec-Kit Analysis** - See `analysis.md` in this directory for full framework evaluation

---

*Integration analysis completed: 2026-02-02 | Analyst: kb-architect*
