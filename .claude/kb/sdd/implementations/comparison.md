# SDD Implementation Comparison

> Spec-Kit vs. AgentSpec: Feature matrix and decision guide

---

## Overview

Two major implementations of Spec-Driven Development exist:

| Implementation | Origin | Focus |
|---------------|--------|-------|
| **Spec-Kit** | GitHub | General SDD toolkit |
| **AgentSpec** | Jarvis/btc-zero-prd | Claude Code ecosystem |

Both implement SDD principles but with different emphases and workflows.

---

## Feature Matrix

### Phases & Workflow

| Feature | Spec-Kit | AgentSpec |
|---------|----------|-----------|
| **Exploration phase** | `/speckit.clarify` (optional) | `/brainstorm` (Phase 0) |
| **Requirements phase** | `/speckit.specify` | `/define` (Phase 1) |
| **Planning phase** | `/speckit.plan` | `/design` (Phase 2) |
| **Task generation** | `/speckit.tasks` | Built into `/design` |
| **Execution phase** | `/speckit.implement` | `/build` (Phase 3) |
| **Archival phase** | Git branches | `/ship` (Phase 4) |
| **Mid-stream updates** | Manual file editing | `/iterate` command |
| **Consistency check** | `/speckit.analyze` | During Build verification |
| **Quality checklists** | `/speckit.checklist` | Clarity Score in Define |

### Artifacts

| Artifact | Spec-Kit | AgentSpec |
|----------|----------|-----------|
| **Governing principles** | `constitution.md` (required) | Optional principles |
| **Requirements** | `spec.md` | `DEFINE_{FEATURE}.md` |
| **Technical plan** | `plan.md` | `DESIGN_{FEATURE}.md` |
| **Task list** | `tasks.md` | File manifest in Design |
| **Research notes** | `research.md` | In Design decisions |
| **Data models** | `data-model.md` | In Design patterns |
| **API contracts** | `contracts/` folder | In Design patterns |
| **Build report** | (not standard) | `BUILD_REPORT_{FEATURE}.md` |
| **Lessons learned** | (git history) | `SHIPPED_{DATE}.md` |

### Project Structure

| Aspect | Spec-Kit | AgentSpec |
|--------|----------|-----------|
| **Root folder** | `.specify/` | `.claude/sdd/` |
| **Feature organization** | `specs/{branch-name}/` | `features/`, `archive/` |
| **Templates location** | `templates/` | `templates/` |
| **Scripts** | `scripts/` | Commands in `.claude/` |
| **Archival** | Git branches | Archive folder |

### Quality & Governance

| Feature | Spec-Kit | AgentSpec |
|---------|----------|-----------|
| **Constitutional principles** | Required (9 articles) | Optional |
| **Pre-implementation gates** | In plan template | Not formalized |
| **Clarity scoring** | Checklist-based | Numeric (15-point) |
| **TDD enforcement** | Constitution Article III | Recommended |
| **Library-first** | Constitution Article I | Not required |
| **CLI exposure** | Constitution Article II | Not required |

### Model & Agent Support

| Feature | Spec-Kit | AgentSpec |
|---------|----------|-----------|
| **Model assignment** | Not specified | Explicit (Opus/Sonnet/Haiku) |
| **Multi-agent** | Supports many AI agents | Claude Code focused |
| **Agent references** | Not formalized | `@agent-name` syntax |
| **Specialized agents** | General AI agent | Specific agents per phase |

---

## Command Comparison

### Exploration/Clarification

| | Spec-Kit | AgentSpec |
|-|----------|-----------|
| **Command** | `/speckit.clarify` | `/brainstorm` |
| **Timing** | Before `/speckit.plan` | Before `/define` |
| **Output** | Updates `spec.md` | Creates `BRAINSTORM_{FEATURE}.md` |
| **Required** | Optional but recommended | Optional |

### Requirements

| | Spec-Kit | AgentSpec |
|-|----------|-----------|
| **Command** | `/speckit.specify` | `/define` |
| **Focus** | User stories, requirements | Problem, goals, acceptance tests |
| **Priority system** | P1, P2, P3 | MoSCoW (MUST/SHOULD/COULD) |
| **Quality metric** | Checklist | Clarity Score (X/15) |
| **Ambiguity handling** | `[NEEDS CLARIFICATION]` | `[NEEDS CLARIFICATION]` |

### Planning/Design

| | Spec-Kit | AgentSpec |
|-|----------|-----------|
| **Command** | `/speckit.plan` | `/design` |
| **Focus** | Tech stack, research | Architecture, file manifest |
| **Decisions** | `research.md` + `plan.md` | Inline ADRs in Design |
| **Contracts** | Separate `contracts/` folder | In Design code patterns |
| **Tasks** | Separate `/speckit.tasks` | Part of file manifest |

### Implementation

| | Spec-Kit | AgentSpec |
|-|----------|-----------|
| **Command** | `/speckit.implement` | `/build` |
| **Task source** | `tasks.md` | File manifest in Design |
| **Verification** | Post-implementation | Per-component loop |
| **Reporting** | (execution logs) | `BUILD_REPORT_{FEATURE}.md` |
| **Progress tracking** | Git commits | Build report |

### Archival

| | Spec-Kit | AgentSpec |
|-|----------|-----------|
| **Command** | (Git merge to main) | `/ship` |
| **Storage** | Git branch history | `archive/{FEATURE}/` folder |
| **Lessons learned** | (not formalized) | `SHIPPED_{DATE}.md` |
| **Discoverability** | Git branch list | Archive folder browsing |

---

## When to Use Which

### Use Spec-Kit When

| Scenario | Why Spec-Kit |
|----------|--------------|
| **New project setup** | `specify init` creates clean structure |
| **Team projects** | Constitution ensures consistency |
| **Multi-AI-agent teams** | Supports Claude, Gemini, Copilot, etc. |
| **Strict governance needed** | 9 articles enforce discipline |
| **Library development** | Library-first principle required |
| **Open source projects** | GitHub-native workflow |

### Use AgentSpec When

| Scenario | Why AgentSpec |
|----------|---------------|
| **Claude Code primary** | Optimized for Claude Code |
| **Jarvis ecosystem** | Integrates with Jarvis Planner |
| **Flexible governance** | Constitution optional |
| **Model optimization** | Explicit model assignment |
| **Lessons learned focus** | Formal Ship phase |
| **Existing project** | Can add to any `.claude/` folder |
| **Agent delegation** | `@agent-name` references |

### Use Both (Hybrid)

| Scenario | How |
|----------|-----|
| **Spec-Kit init + AgentSpec workflow** | Initialize with Spec-Kit, use AgentSpec commands |
| **Constitution + AgentSpec phases** | Create constitution, then use /define → /ship |
| **Shared team, personal workflow** | Team uses Spec-Kit, you use AgentSpec for your tasks |

---

## Philosophy Differences

### Spec-Kit Philosophy

> **Constitutional governance**: Immutable principles enforce consistent decisions across all features and team members.

Key beliefs:
- Every feature should be a library
- CLI interfaces enable testing
- Tests must come before code
- Simplicity over abstraction

### AgentSpec Philosophy

> **Phase-based workflow**: Clear phases with appropriate models and quality gates guide features from idea to production.

Key beliefs:
- Brainstorming prevents scope creep
- Clarity scores ensure measurable quality
- Build verification catches issues early
- Lessons learned improve future work

---

## Migration Path

### From Spec-Kit to AgentSpec

```text
1. Keep .specify/ for team governance
2. Add .claude/sdd/ for AgentSpec
3. Map: spec.md → DEFINE, plan.md → DESIGN
4. Add Build reports and Ship documents
5. Use /iterate for mid-stream changes
```

### From AgentSpec to Spec-Kit

```text
1. Run specify init . --ai claude
2. Create constitution from team standards
3. Map: DEFINE → spec, DESIGN → plan + tasks
4. Use /speckit.implement for execution
5. Rely on git branches for archival
```

### From Neither (Greenfield)

**Small/Personal Project**: Start with AgentSpec
- Faster setup
- Flexible governance
- Good for learning SDD

**Team/Enterprise Project**: Start with Spec-Kit
- Constitutional consistency
- Multi-agent support
- GitHub-native workflow

---

## Summary Table

| Aspect | Spec-Kit | AgentSpec | Winner |
|--------|----------|-----------|--------|
| **Setup ease** | Needs CLI install | Just folders | AgentSpec |
| **Governance** | Strong (constitution) | Flexible | Spec-Kit for teams |
| **Multi-agent** | Excellent | Claude-focused | Spec-Kit |
| **Model optimization** | None | Explicit | AgentSpec |
| **Lessons learned** | Informal | Formal phase | AgentSpec |
| **Task management** | Dedicated phase | In Design | Spec-Kit |
| **Iteration** | Manual | `/iterate` command | AgentSpec |
| **Research capture** | Excellent | In Design | Spec-Kit |
| **Build verification** | Post-hoc | Per-component | AgentSpec |
| **Jarvis integration** | None | Excellent | AgentSpec |

---

## Recommendation

| If you need... | Use |
|---------------|-----|
| Strict team governance | Spec-Kit |
| Multi-AI-agent workflow | Spec-Kit |
| Claude Code optimization | AgentSpec |
| Formal lessons learned | AgentSpec |
| Quick personal projects | AgentSpec |
| Open source collaboration | Spec-Kit |
| Jarvis/Dev Loop integration | AgentSpec |
| Library-first development | Spec-Kit |

**For this project (btc-zero-prd)**: AgentSpec is already integrated and working well. Use it for all SDD features.

---

## Resources

### Spec-Kit
- Repository: https://github.com/github/spec-kit
- Documentation: https://github.github.io/spec-kit/
- Video: https://youtube.com/watch?v=a9eR1xsfvHg

### AgentSpec
- Overview: `.claude/sdd/_index.md`
- Templates: `.claude/sdd/templates/`
- Archive: `.claude/sdd/archive/`

---

*References: Spec-Kit documentation, AgentSpec 4.2 implementation*
