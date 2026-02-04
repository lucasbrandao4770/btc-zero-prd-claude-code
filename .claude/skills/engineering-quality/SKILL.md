---
name: engineering-quality
description: Engineering practices validation skill. Activates after planning phase completion, before HANDOFF generation, during sandbox chunk validation, or when user calls /validate. Ensures professional engineering standards through 26-question checklist.
---

# Engineering Quality Skill

## When This Skill Activates

### Automatic Triggers

- **After planning phase completion** - Validates Strategic, Tactical, or Operational outputs
- **Before HANDOFF.md generation** - Ensures plan is execution-ready
- **During sandbox chunk validation** - Checks chunk outputs meet standards
- **User explicitly calls `/validate`** - On-demand validation

### Trigger Patterns

| Pattern | Action |
|---------|--------|
| Plan phase completes | Run gate-specific questions |
| `HANDOFF.md` about to be generated | Run full pre-handoff validation |
| Sandbox chunk marked complete | Run chunk validation (G6) |
| User says "validate", "check quality", "review plan" | Run targeted or full validation |
| `/validate {gate}` | Run specific gate validation |

## The 26-Question Checklist

Engineering practices are organized into **10 categories** with **26 questions**.

### Categories

| Category | Questions | Focus |
|----------|-----------|-------|
| **Impact Analysis** | Q1-Q3 | What changes, what breaks |
| **Integration** | Q4-Q6 | Fits existing architecture |
| **Cleanup** | Q7-Q9 | Leave it better |
| **Quality** | Q10-Q12 | Code quality standards |
| **Scalability** | Q13-Q14 | Design for growth |
| **Testing** | Q15-Q17 | Verification planning |
| **Dependencies** | Q18-Q20 | External requirements |
| **Resources** | Q21-Q23 | Leverage available tools |
| **Research** | Q24-Q25 | Ground in evidence |
| **Propagation** | Q26 | Standards for subagents |

### Question Severity

- **Critical** - Blocker. Must pass before proceeding.
- **High** - Warning. Should address before proceeding.
- **Medium** - Notice. Consider addressing.
- **Low** - Info. Nice to have.

## Validation Gates Integration

Each validation gate (G1-G7) has specific questions assigned.

### Gate-to-Question Mapping

| Gate | Name | Questions |
|------|------|-----------|
| **G1** | Plan Chain Creation | Structure validation only |
| **G2** | Strategic Phase | Q1, Q2, Q3, Q4, Q15, Q18, Q20, Q22 |
| **G3** | Tactical Phase | Q5, Q6, Q10, Q13, Q14, Q21, Q24 |
| **G4** | Operational Phase | Q7, Q11, Q16, Q17, Q19, Q23, Q25 |
| **G5** | HANDOFF Generation | Q26 |
| **G6** | Sandbox Chunk | Q12 |
| **G7** | Plan Completion | Q8, Q9 |

## Validation Flow

### Phase Validation (G2, G3, G4)

```
1. Load phase output document
2. Load gate-specific questions from checklist.yaml
3. For each question:
   a. Analyze document for evidence of addressing the question
   b. Score: PASS, PARTIAL, FAIL
   c. If FAIL on critical: BLOCK
   d. If FAIL on high: WARNING
4. Generate ValidationResult
5. If blocked: Return issues to phase agent for regeneration
6. If passed: Proceed to next phase
```

### HANDOFF Validation (G5)

```
1. Load HANDOFF.md
2. Verify structure (YAML frontmatter, required sections)
3. Check Q26: Worker bootup includes engineering practices
4. Verify chunk boundaries are clear
5. Verify quality gate protocol specified
6. Generate ValidationResult
```

### Chunk Validation (G6)

```
1. Load chunk output (files created, tests run)
2. Check Q12: Code quality validated
   - Ruff formatting applied
   - Linting passed
   - Type hints present
3. Verify tests pass (if applicable)
4. Generate ValidationResult
5. Update .sandbox-progress.yaml
```

### Plan Completion (G7)

```
1. Load final sandbox state
2. Check Q8: No mess left behind
3. Check Q9: Outdated artifacts removed
4. Verify all success criteria from strategic doc met
5. Generate LearningsReport for /sandbox:learn
6. If chain: Check next plan prerequisites satisfied
```

## Usage

### Running Validation

```bash
# Validate specific gate
jarvis-crud planner validate run --gate G2 --plan {plan_id}

# Get checklist for plan
jarvis-crud planner checklist get {plan_id}
```

### Validation Output

```yaml
validation_result:
  gate: G2
  plan_id: "plan-123"
  timestamp: "2026-01-24T12:00:00Z"
  status: "passed" | "blocked" | "warning"

  questions:
    - id: Q1
      status: "pass"
      evidence: "Impact analysis section present with file list"
    - id: Q2
      status: "fail"
      severity: "critical"
      issue: "No integration impact analysis found"

  summary:
    total: 8
    passed: 7
    failed: 1
    critical_failed: 1

  decision: "BLOCKED - Critical question Q2 failed"
```

## Checklist Reference

### Impact Analysis (Q1-Q3)

| ID | Question | Severity |
|----|----------|----------|
| Q1 | Which files will be affected? | Critical |
| Q2 | Will this break existing references/integrations? | Critical |
| Q3 | What downstream systems depend on changed components? | High |

### Integration (Q4-Q6)

| ID | Question | Severity |
|----|----------|----------|
| Q4 | How does this integrate with existing folder structure? | High |
| Q5 | Does this follow existing naming conventions? | Medium |
| Q6 | Are new patterns consistent with established patterns? | High |

### Cleanup (Q7-Q9)

| ID | Question | Severity |
|----|----------|----------|
| Q7 | Will I need to clean up afterwards? | Medium |
| Q8 | Am I leaving a mess behind? | High |
| Q9 | Are there outdated artifacts that should be removed? | Medium |

### Quality (Q10-Q12)

| ID | Question | Severity |
|----|----------|----------|
| Q10 | How will this affect system performance? | Medium |
| Q11 | Are best practices being followed? | High |
| Q12 | What about code smells? Did I validate what I created? | High |

### Scalability (Q13-Q14)

| ID | Question | Severity |
|----|----------|----------|
| Q13 | Is the approach scalable for future improvements? | Medium |
| Q14 | Is it flexible enough for changing requirements? | Medium |

### Testing (Q15-Q17)

| ID | Question | Severity |
|----|----------|----------|
| Q15 | What about testing? Are test suites planned? | Critical |
| Q16 | What coverage is expected? | High |
| Q17 | Are edge cases considered? | High |

### Dependencies (Q18-Q20)

| ID | Question | Severity |
|----|----------|----------|
| Q18 | Which dependencies and external services are involved? | High |
| Q19 | Are versions specified? | High |
| Q20 | Are there licensing concerns? | Medium |

### Resources (Q21-Q23)

| ID | Question | Severity |
|----|----------|----------|
| Q21 | Am I accounting for all available resources? | High |
| Q22 | Am I reinventing the wheel? | High |
| Q23 | Are available libraries being leveraged? | Medium |

### Research (Q24-Q25)

| ID | Question | Severity |
|----|----------|----------|
| Q24 | Did I properly research before implementing? | High |
| Q25 | Were MCPs consulted for validation? | High |

### Propagation (Q26)

| ID | Question | Severity |
|----|----------|----------|
| Q26 | Will workers (subagents) also follow these standards? | Critical |

## Best Practices

### Always

- Run validation after EVERY planning phase
- Address all critical failures before proceeding
- Document why any high-severity warnings were accepted
- Include engineering practices reference in HANDOFF worker bootup

### Never

- Skip validation gates for "simple" plans
- Ignore critical failures
- Proceed with blocked status
- Forget to propagate standards to subagents

## Integration with Planning Agents

Each planning agent (strategic-architect, tactical-architect, operational-planner) should:

1. Reference this skill in their validation step
2. Include engineering checklist questions in their output
3. Call validation gate before completing phase
4. Handle blocked status by regenerating with issues addressed

## Related Files

- `skills/engineering-quality/checklist.yaml` - Full checklist definition
- `modes/jarvis-planner-mode.md` - Planner mode integration
- `agents/planning/*.md` - Planning agents with gate integration
- `templates/planning/*.md` - Planning templates with checklist sections
