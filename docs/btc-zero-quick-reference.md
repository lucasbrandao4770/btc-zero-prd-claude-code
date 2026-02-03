# btc-zero Quick Reference

> Action-oriented guide for daily use of the btc-zero-prd-claude-code repository.

---

## The Development Spectrum at a Glance

| Level | Approach | Command | Time | Use When |
|-------|----------|---------|------|----------|
| **1** | Vibe Coding | (none) | <30 min | Quick fixes, experiments |
| **2** | Dev Loop | `/dev` | 1-4 hours | KB building, utilities, single features |
| **3** | SDD | `/brainstorm` to `/ship` | Days | Production features, team work |

---

## Command Cheat Sheet

### SDD Commands (Level 3)

```bash
# Start with vague idea - explore first
/brainstorm "I want to build a notification system"

# Clear requirements - skip brainstorm
/define "Build a REST API for user management"

# From existing brainstorm
/define .claude/sdd/features/BRAINSTORM_USER_NOTIFICATIONS.md

# Create technical design
/design .claude/sdd/features/DEFINE_USER_NOTIFICATIONS.md

# Execute implementation
/build .claude/sdd/features/DESIGN_USER_NOTIFICATIONS.md

# Archive when complete
/ship .claude/sdd/features/DEFINE_USER_NOTIFICATIONS.md

# Update any document mid-stream
/iterate DEFINE_DATA_EXPORT.md "Add support for CSV format"
```

### Dev Loop Commands (Level 2)

```bash
# Let crafter guide you (recommended)
/dev "I want to build a date parser utility"

# Execute existing PROMPT
/dev tasks/PROMPT_DATE_PARSER.md

# Resume interrupted session
/dev tasks/PROMPT_DATE_PARSER.md --resume

# Validate without executing
/dev tasks/PROMPT_AUTH.md --dry-run

# Run autonomously
/dev tasks/PROMPT_BULK_WORK.md --mode afk
```

### Utility Commands

```bash
/create-kb        # Create new knowledge base
/review           # Code review workflow
/create-pr        # Create pull request
/memory           # Save session insights
/sync-context     # Update CLAUDE.md with context
/readme-maker     # Generate README
```
---

## Decision Tree: Which Level to Use?

\

### Quick Decision Guide

| Scenario | Level | Command |
|----------|-------|---------|
| Fix a typo | 1 | Just prompt |
| Add logging to function | 1 | Just prompt |
| Build a utility parser | 2 | \ |
| Create knowledge base | 2 | \ |
| Prototype a feature | 2 | \ |
| Production feature | 3 | \ or \ |
| Multi-file feature | 3 | \ or \ |
| Feature needs documentation | 3 | \ or \ |

---

## SDD Workflow Quick Guide

### Phase Flow

\

### Artifacts Location

| Phase | Output File | Location |
|-------|-------------|----------|
| 0 | \ | \ |
| 1 | \ | \ |
| 2 | \ | \ |
| 3 | \ | \ |
| 4 | \ | \ |

### When to Skip /brainstorm

- Clear requirements already known
- Meeting notes with explicit asks
- Simple feature request

### When to Use /brainstorm

- Vague idea needs exploration
- Multiple approaches possible
- Uncertain about scope
---

## Dev Loop Quick Guide

### PROMPT.md Priority Execution

```
Execute order: RISKY --> CORE --> POLISH
                (red)    (yellow)  (green)
                First     Second    Last
```

### Task Syntax in PROMPT.md

```markdown
### RISKY (Do First)
- [ ] Validate API connectivity

### CORE
- [ ] @python-developer: Implement main logic
- [ ] @test-generator: Add unit tests
- [ ] Task with verification: Verify: `pytest tests/`

### POLISH (Do Last)
- [ ] @code-documenter: Update README
```

### Quality Tiers

| Tier | Use For | Expectations |
|------|---------|--------------|
| `prototype` | Experiments | Speed over perfection |
| `production` | Real features | Tests required |
| `library` | Shared code | Full docs, backward compat |

### Session Recovery

```bash
# Resume interrupted work
/dev tasks/PROMPT_*.md --resume
```

---

## Agent Quick Reference

### Key Agents by Task

| Task | Agent |
|------|-------|
| Extract meeting requirements | `@meeting-analyst` |
| Plan implementation | `@the-planner` |
| Write Python code | `@python-developer` |
| Generate tests | `@test-generator` |
| Review code | `@code-reviewer` |
| Create KB | `@kb-architect` |
---

## Knowledge Base Domains

| Domain | Purpose |
|--------|---------|
| `pydantic` | Data validation, LLM output parsing |
| `gcp` | GCP serverless, Cloud Run, BigQuery |
| `gemini` | Gemini multimodal, document extraction |
| `langfuse` | LLMOps observability |
| `terraform` | Infrastructure as Code |
| `terragrunt` | Multi-environment orchestration |
| `crewai` | Multi-agent AI orchestration |
| `openrouter` | Unified LLM API gateway |

---

## Common Workflows

### Building a Production Feature

```bash
# 1. Explore the idea
/brainstorm "Build invoice validation system"

# 2. Answer questions, confirm approach

# 3. Define requirements
/define .claude/sdd/features/BRAINSTORM_INVOICE_VALIDATION.md

# 4. Create technical design
/design .claude/sdd/features/DEFINE_INVOICE_VALIDATION.md

# 5. Build implementation
/build .claude/sdd/features/DESIGN_INVOICE_VALIDATION.md

# 6. Archive when done
/ship .claude/sdd/features/DEFINE_INVOICE_VALIDATION.md
```

### Building a Knowledge Base

```bash
# Let crafter guide you
/dev "Create a Redis KB with caching patterns"
```

---

## File Structure Quick Map

```
.claude/
  CLAUDE.md          # Project instructions (READ THIS FIRST)
  agents/            # 40+ specialized agents
    workflow/        # SDD agents
    code-quality/    # Review, testing
    communication/   # Meeting analysis, planning
  commands/          # Slash commands
    workflow/        # /brainstorm, /define, etc.
    dev/             # /dev
  kb/                # Knowledge bases (8 domains)
  sdd/               # Spec-Driven Development
    features/        # Active work
    reports/         # Build reports
    archive/         # Shipped features
  dev/               # Dev Loop
    tasks/           # PROMPT files
    progress/        # Memory bridge
    templates/       # Starting points
```

---

## Tips

### Do

- Start with `/dev "description"` for anything non-trivial
- Use `@agent-name` syntax for specialized tasks
- Check `.claude/CLAUDE.md` for project context
- Use priority markers in PROMPT.md (RISKY first)

### Avoid

- Skipping /brainstorm for vague ideas
- Using Level 1 for production features
- Starting /build without /design

---

## Reference Links

| Resource | Location |
|----------|----------|
| Project Instructions | `.claude/CLAUDE.md` |
| SDD Documentation | `.claude/sdd/_index.md` |
| Dev Loop Documentation | `.claude/dev/_index.md` |
| PROMPT Templates | `.claude/dev/templates/` |
| Real Examples | `.claude/dev/examples/` |
| Shipped Features | `.claude/sdd/archive/` |

---

*Quick Reference v1.0 - btc-zero-prd-claude-code*