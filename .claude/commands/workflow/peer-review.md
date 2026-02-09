# Peer Review Command

> Adversarial quality gate for SDD artifacts — spawns parallel specialist reviewers for honest critique

## Usage

```bash
/workflow:peer-review <artifact-path> [--reviewers agent1,agent2] [--max-rounds 3]
```

## Examples

```bash
# Auto-select reviewers based on artifact phase and project context
/workflow:peer-review .claude/sdd/features/BRAINSTORM_CLAUDE_SENSEI.md

# Specify exact reviewers
/workflow:peer-review .claude/sdd/features/DESIGN_INVOICE_PIPELINE.md --reviewers genai-architect,ai-data-engineer

# Review a build report
/workflow:peer-review .claude/sdd/reports/BUILD_REPORT_AUTH.md --reviewers code-reviewer,python-developer

# Limit review rounds
/workflow:peer-review .claude/sdd/features/DEFINE_FEATURE.md --max-rounds 2
```

---

## Overview

This is a **cross-phase quality gate** in the AgentSpec workflow. It can be inserted AFTER any phase:

```text
Phase 0: /brainstorm → BRAINSTORM.md → /peer-review → improved BRAINSTORM.md
Phase 1: /define     → DEFINE.md     → /peer-review → improved DEFINE.md
Phase 2: /design     → DESIGN.md     → /peer-review → improved DESIGN.md
Phase 3: /build      → Code + Report → /peer-review → improved code/report
Phase 4: /ship       → SHIPPED.md    → (no review needed)
```

**Why this exists:** LLMs suffer from "first-draft confidence" — they produce plausible output and self-confirm. This command mitigates that by spawning **independent specialist reviewers** who evaluate the artifact through different expert lenses, creating an adversarial feedback loop that catches blind spots, architectural mistakes, missing requirements, and violations of best practices.

**Inspired by:** [Ralph Wiggum Plugin](https://awesomeclaude.ai/ralph-wiggum) for Claude Code — using the same AI with different specialist system prompts to review its own work from multiple angles.

---

## What This Command Does

1. **Detect** — Identify the artifact type (BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT) and project context
2. **Select** — Choose 2-3 specialist reviewer agents (auto or manual)
3. **Brief** — Prepare a review brief with artifact content + phase-specific evaluation criteria
4. **Spawn** — Launch reviewers as **parallel foreground agents** (each reviews independently)
5. **Collect** — Gather structured feedback from all reviewers
6. **Synthesize** — Merge feedback, resolve conflicts, prioritize changes
7. **Revise** — Update the artifact with improvements
8. **Re-submit** — Send revised artifact back to reviewers for validation
9. **Converge** — Repeat until reviewers approve OR max rounds reached

---

## Process

### Step 1: Load and Identify Artifact

```markdown
Read(<artifact-path>)
```

Determine the artifact type from its filename pattern:
- `BRAINSTORM_*.md` → Phase 0 review criteria
- `DEFINE_*.md` → Phase 1 review criteria
- `DESIGN_*.md` → Phase 2 review criteria
- `BUILD_REPORT_*.md` → Phase 3 review criteria
- Other files → Generic review criteria

### Step 2: Select Reviewers

**If `--reviewers` specified:** Use the named agents directly.

**If auto-selecting:** Choose 2-3 reviewers based on artifact phase AND project domain.

#### Reviewer Selection Matrix

| Artifact Phase | Reviewer 1 (Architecture) | Reviewer 2 (Domain) | Reviewer 3 (Quality) |
|---------------|---------------------------|---------------------|---------------------|
| **BRAINSTORM** | genai-architect | ai-data-engineer | the-planner |
| **DEFINE** | genai-architect | codebase-explorer | meeting-analyst |
| **DESIGN** | genai-architect | python-developer | code-reviewer |
| **BUILD_REPORT** | code-reviewer | python-developer | test-generator |

**Customization:** The reviewer selection should adapt to the project domain. Read the project's `CLAUDE.md` to understand what technologies and domains are involved, then select the most relevant specialist agents.

#### Available Reviewer Agents (by Specialty)

| Category | Agents | Best For Reviewing |
|----------|--------|-------------------|
| **Architecture** | genai-architect, the-planner, strategic-architect | System design, component boundaries, scalability |
| **Data Engineering** | ai-data-engineer, medallion-architect, lakeflow-architect | Data schemas, pipelines, storage decisions |
| **AI/ML** | llm-specialist, ai-prompt-specialist, extraction-specialist | LLM integration, prompt design, model selection |
| **Code Quality** | code-reviewer, python-developer, code-cleaner | Code patterns, maintainability, standards |
| **Testing** | test-generator | Test coverage, testability of design |
| **Infrastructure** | infra-deployer, ci-cd-specialist, aws-lambda-architect | Deployment, IaC, cloud architecture |
| **Communication** | adaptive-explainer, meeting-analyst | Clarity, completeness, audience alignment |
| **Domain** | pipeline-architect, function-developer, dataops-builder | Project-specific concerns |

### Step 3: Prepare Review Brief

For each reviewer, construct a review prompt with:

```markdown
## Review Brief

### Your Role
You are a **senior {specialty} engineer** conducting a rigorous peer review.
Your job is to be **brutally honest** — find problems, gaps, risks, and violations
of best practices. You are NOT here to praise — you are here to improve.

### Artifact Under Review
**Type:** {BRAINSTORM|DEFINE|DESIGN|BUILD_REPORT}
**Feature:** {feature name}
**Phase:** {phase number and name}

### The Artifact
{Full content of the artifact}

### Project Context
{Relevant excerpts from CLAUDE.md — tech stack, architecture, constraints}

### Review Criteria
{Phase-specific criteria — see Step 4}

### Your Review Format
Provide your review in this EXACT structure:

#### Overall Assessment
- **Verdict:** APPROVE | REVISE (minor) | REVISE (major) | REJECT
- **Confidence:** {0-100}%
- **Summary:** {2-3 sentences}

#### Critical Issues (Must Fix)
{Numbered list — things that WILL cause problems if not addressed}

#### Recommendations (Should Fix)
{Numbered list — improvements that significantly enhance quality}

#### Observations (Could Improve)
{Numbered list — nice-to-haves and polish suggestions}

#### Best Practices Violations
{List any violations of industry best practices in your domain}

#### Missing Considerations
{What was NOT addressed but SHOULD have been?}

#### What's Done Well
{Acknowledge 2-3 genuine strengths — but be specific, not generic}
```

### Step 4: Phase-Specific Review Criteria

#### For BRAINSTORM Artifacts
```markdown
Evaluate the brainstorm through these lenses:
1. **Problem Clarity** — Is the problem well-defined? Is it the RIGHT problem?
2. **Approach Validity** — Are the explored approaches realistic? Missing alternatives?
3. **Architecture Soundness** — Does the proposed architecture follow best practices?
4. **Tech Stack Fitness** — Are technology choices justified? Better alternatives?
5. **Scope Management** — Is the MVP scope realistic? Too ambitious? Too narrow?
6. **Risk Identification** — Are risks properly identified? Missing critical risks?
7. **Data Model** — Is the data schema well-designed? Normalized? Extensible?
8. **User Experience** — Is the user journey considered? Pain points addressed?
9. **Scalability** — Can this grow without major rewrites?
10. **Open Questions** — Are there unresolved questions that should be answered before /define?
```

#### For DEFINE Artifacts
```markdown
Evaluate the requirements through these lenses:
1. **Completeness** — Are all functional requirements captured?
2. **Testability** — Can each requirement be verified? Are acceptance tests concrete?
3. **Clarity** — Are requirements unambiguous? Could two engineers interpret them differently?
4. **Feasibility** — Are requirements technically achievable within constraints?
5. **Priority** — Are MUST/SHOULD/COULD properly categorized?
6. **Non-Functional** — Performance, security, scalability requirements present?
7. **Edge Cases** — Are boundary conditions and error cases covered?
8. **Dependencies** — Are external dependencies identified?
9. **Metrics** — Are success criteria measurable?
10. **Scope Creep** — Is anything in-scope that shouldn't be?
```

#### For DESIGN Artifacts
```markdown
Evaluate the design through these lenses:
1. **Architecture** — Is the system architecture sound? Separation of concerns?
2. **Component Design** — Are interfaces clean? Responsibilities clear?
3. **Data Flow** — Is data flow logical? Any bottlenecks?
4. **API Design** — Are APIs consistent, RESTful, well-documented?
5. **Error Handling** — Is failure handling comprehensive? Recovery strategies?
6. **Security** — Authentication, authorization, input validation present?
7. **Testability** — Can components be tested in isolation?
8. **File Manifest** — Is the manifest complete? Agent assignments logical?
9. **Key Decisions** — Are ADRs well-reasoned? Alternatives considered?
10. **Implementation Order** — Does the build sequence make sense? Dependencies respected?
```

#### For BUILD_REPORT Artifacts
```markdown
Evaluate the implementation through these lenses:
1. **Completeness** — Does the code satisfy all DESIGN requirements?
2. **Code Quality** — Clean code, proper patterns, no code smells?
3. **Test Coverage** — Are critical paths tested? Edge cases covered?
4. **Error Handling** — Proper error handling in all components?
5. **Performance** — Any obvious performance issues? N+1 queries? Unnecessary allocations?
6. **Security** — Input validation, SQL injection prevention, auth checks?
7. **Documentation** — Are complex parts documented? Public APIs documented?
8. **Integration** — Do components integrate cleanly? Contract adherence?
9. **Technical Debt** — Any shortcuts that need future cleanup?
10. **Acceptance Tests** — Do acceptance test results match DEFINE criteria?
```

### Step 5: Spawn Parallel Reviewers

Launch ALL reviewers as **parallel foreground agents** in a single message:

```markdown
# Spawn reviewers (PARALLEL, FOREGROUND)
Task(subagent_type="{agent1}", prompt="{review_brief_1}")
Task(subagent_type="{agent2}", prompt="{review_brief_2}")
Task(subagent_type="{agent3}", prompt="{review_brief_3}")  # Optional
```

**CRITICAL:**
- All reviewers MUST be spawned in a SINGLE message (parallel)
- All reviewers MUST be foreground (NOT background — Windows compatibility)
- Each reviewer is INDEPENDENT — they do NOT see each other's feedback
- Each reviewer gets the SAME artifact but through THEIR specialist lens

### Step 6: Synthesize Feedback

After all reviewers return, create a synthesis:

```markdown
## Review Synthesis — Round {N}

### Verdicts
| Reviewer | Agent | Verdict | Confidence |
|----------|-------|---------|------------|
| Architecture | {agent1} | {verdict} | {confidence} |
| Domain | {agent2} | {verdict} | {confidence} |
| Quality | {agent3} | {verdict} | {confidence} |

### Consensus
- **Overall:** {APPROVE if all approve, else REVISE}
- **Agreement Level:** {unanimous / majority / split}

### Critical Issues (Merged & Deduplicated)
{Combined list from all reviewers, deduplicated, prioritized}

### Recommendations (Merged & Deduplicated)
{Combined list}

### Conflicts
{Where reviewers disagreed — how we resolve it}
```

Present this synthesis to the user using AskUserQuestion:

```
AskUserQuestion({
  "questions": [{
    "question": "Peer review complete. {X} critical issues found, {Y} recommendations. How would you like to proceed?",
    "header": "Review",
    "options": [
      {"label": "Accept all feedback", "description": "Apply all critical issues and recommendations to the artifact"},
      {"label": "Apply critical only", "description": "Only fix critical issues, skip recommendations"},
      {"label": "Review individually", "description": "Go through each piece of feedback and decide"},
      {"label": "Override — approve as-is", "description": "Dismiss feedback and approve the artifact as-is"}
    ]
  }]
})
```

### Step 7: Revise Artifact

Based on user's choice:
- Read the original artifact
- Apply accepted feedback
- Write the updated artifact (same path — overwrite)
- Add a revision history entry:

```markdown
## Revision History

| Version | Date | Reviewer(s) | Changes |
|---------|------|-------------|---------|
| 1.0 | {date} | Initial | First draft |
| 1.1 | {date} | {agent1}, {agent2} | Peer review round 1: {summary} |
```

### Step 8: Re-Submit (If Needed)

**Loop condition:** If ANY reviewer gave "REVISE (major)" or "REJECT", re-submit to reviewers.

**Exit conditions (stop looping):**
- All reviewers give "APPROVE" or "REVISE (minor)" → **Done**
- Max rounds reached (default: 3) → **Done with warning**
- User overrides → **Done**

For re-submission, only send to reviewers who had issues (not those who already approved).

### Step 9: Final Report

After convergence, output a summary:

```markdown
## Peer Review Complete

**Artifact:** {path}
**Rounds:** {N}
**Final Verdict:** {APPROVED | APPROVED WITH CAVEATS}

### Changes Made
{Bulleted list of all changes from all rounds}

### Reviewer Sign-Off
| Reviewer | Final Verdict | Notes |
|----------|---------------|-------|
| {agent1} | APPROVED | {note} |
| {agent2} | APPROVED | {note} |

### Remaining Caveats
{Any unresolved recommendations the user chose to defer}
```

---

## Output

| Artifact | Location |
|----------|----------|
| **Revised artifact** | Same path as input (overwritten with improvements) |
| **Review log** | Displayed in conversation (not persisted to file) |

**Next Step:** Proceed to the next SDD phase with the improved artifact.

---

## Quality Gate

Before marking review complete:

```text
[ ] Minimum 2 reviewers spawned in parallel
[ ] Each reviewer used phase-specific evaluation criteria
[ ] All critical issues addressed or explicitly deferred by user
[ ] Artifact updated with revision history
[ ] At least 1 full review round completed
[ ] User confirmed final state
```

---

## Configuration

### Default Settings

| Setting | Default | Override |
|---------|---------|---------|
| Max review rounds | 3 | `--max-rounds N` |
| Min reviewers | 2 | `--reviewers` (list) |
| Max reviewers | 3 | `--reviewers` (list) |
| Auto-select reviewers | Yes | `--reviewers` overrides |
| Re-submit threshold | REVISE (major) or REJECT | Not configurable |

### Adapting to Project Domain

The reviewer selection adapts based on the project's CLAUDE.md:

| Project Signals | Suggested Reviewers |
|----------------|-------------------|
| Python + FastAPI + SQLite | python-developer, code-reviewer |
| AI/LLM integration | genai-architect, llm-specialist |
| Data pipelines | ai-data-engineer, medallion-architect |
| Cloud infrastructure | infra-deployer, aws-lambda-architect |
| Frontend/UI | ui-prototyper (if available) |
| Multi-agent systems | genai-architect, ai-prompt-specialist |

---

## Interaction Style

### Reviewers Must Be Brutally Honest

Each reviewer prompt includes:
- "Your job is to FIND PROBLEMS, not to praise"
- "Assume the author has blind spots — identify them"
- "Challenge assumptions, question trade-offs"
- "If something seems fine but could be better, say so"
- "Do NOT say 'overall this is good' — focus on what needs improvement"

### But Constructive

- Every criticism MUST include a suggested fix or alternative
- Vague feedback like "this could be better" is NOT acceptable
- Each issue must explain WHY it's a problem and WHAT to do instead

---

## Tips

1. **Run after EVERY major phase** — The earlier you catch issues, the cheaper they are to fix
2. **Use domain-specific reviewers** — A data engineer will catch schema issues an architect might miss
3. **Don't skip round 2** — The first revision often introduces new issues
4. **Override sparingly** — If you override reviewers, document why
5. **Let reviewers be harsh** — That's the whole point; comfort is the enemy of quality
6. **Mix perspectives** — Architecture + Domain + Quality gives maximum coverage

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Instead |
|-------------|-------------|---------|
| Only 1 reviewer | Single point of failure, no cross-checking | Minimum 2 reviewers |
| Same reviewer type twice | Redundant perspectives | Mix specialties |
| Ignoring all feedback | Defeats the purpose | At minimum, address critical issues |
| Too many rounds (>3) | Diminishing returns, context waste | Stop at 3, defer remaining to next phase |
| Running in background | Can't iterate in real-time | Always foreground |

---

## References

- Related: `.claude/commands/review/review.md` (code review — different purpose)
- Contracts: `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Inspiration: [Ralph Wiggum Plugin](https://awesomeclaude.ai/ralph-wiggum) for Claude Code
- Pattern: Adversarial review / Red Team methodology
