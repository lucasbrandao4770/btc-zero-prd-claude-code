# Engineering Quality Skill

Professional engineering practices validation for the Jarvis Planner system.

## Overview

This skill enforces the **26-question engineering checklist** across all planning phases and execution chunks. It integrates with validation gates G1-G7 to ensure professional engineering standards are met at every transition.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition, triggers, and integration docs |
| `checklist.yaml` | 26 questions organized by category and gate |
| `README.md` | This file |

## Quick Reference

### Validation Gates

| Gate | Phase | Questions |
|------|-------|-----------|
| G1 | Chain Creation | Structure only |
| G2 | Strategic | Q1-Q4, Q15, Q18, Q20, Q22 |
| G3 | Tactical | Q5-Q6, Q10, Q13-Q14, Q21, Q24 |
| G4 | Operational | Q7, Q11, Q16-Q17, Q19, Q23, Q25 |
| G5 | HANDOFF | Q26 |
| G6 | Chunk | Q12 |
| G7 | Completion | Q8-Q9 |

### Categories

1. **Impact Analysis** - What changes, what breaks
2. **Integration** - Fits existing architecture
3. **Cleanup** - Leave it better
4. **Quality** - Code quality standards
5. **Scalability** - Design for growth
6. **Testing** - Verification planning
7. **Dependencies** - External requirements
8. **Resources** - Leverage available tools
9. **Research** - Ground in evidence
10. **Propagation** - Standards for subagents

## Usage

```bash
# Validate specific gate
jarvis-crud planner validate run --gate G2 --plan {plan_id}

# Get checklist for plan
jarvis-crud planner checklist get {plan_id}
```

## Integration

This skill is consumed by:
- `modes/jarvis-planner-mode.md` - Planner mode calls gates
- `agents/planning/*.md` - Phase agents run validation
- `templates/sandbox/HANDOFF-template.md` - Worker bootup references

See `SKILL.md` for detailed integration instructions.
