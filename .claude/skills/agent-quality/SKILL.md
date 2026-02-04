---
name: agent-quality
description: Validates agent files against quality standards. Activates when creating or modifying agents, running /agents create, or mentioning "create agent", "new agent", "agent quality".
---

# Agent Quality Validation

Validates agent files against quality standards. Auto-activates after agent creation or modification.

## Activation Triggers

This skill activates when:
- User runs `/agents create` or `/agents`
- Agent files in `agents/` are created or modified
- User mentions "create agent", "new agent", "agent quality"

## Validation Checklist

Run this checklist after any agent is created or modified:

### Frontmatter (Required)
```
[ ] name: uses lowercase-with-hyphens
[ ] description: ends with "Use PROACTIVELY when..."
[ ] tools: lists only necessary tools
```

### Structure (Recommended)
```
[ ] Identity section with philosophy
[ ] KB/docs references (if applicable)
[ ] 2+ capabilities with examples
[ ] 1+ execution patterns
[ ] Best practices (Always/Never rules)
```

### Content Quality
```
[ ] No placeholder text ([TODO], {placeholder})
[ ] Code examples are syntax-valid
[ ] KB references point to existing files
[ ] Description is clear and actionable
```

## Quick Validation Command

After creating an agent, validate with:

```
Read the agent file
Check each item in the checklist above
Report any issues found
Suggest fixes for failed items
```

## Integration with /agents

When Claude Code's native `/agents` command creates a new agent:

1. The `agent-quality` rule loads automatically (glob matches agents/**/*.md)
2. This skill should be invoked to validate the created agent
3. Any issues are reported with suggested fixes

## Template Reference

For full agent template with all sections: `docs/agent-template.md`

## Example Validation Output

```
Agent Validation: my-new-agent.md

Frontmatter: PASS
  [x] name: lowercase-with-hyphens
  [x] description: ends with trigger
  [x] tools: appropriate list

Structure: PASS (with suggestions)
  [x] Identity section present
  [x] Capabilities defined (3)
  [ ] Consider adding execution patterns

Content: PASS
  [x] No placeholders
  [x] Code examples valid

Result: READY TO USE
```
