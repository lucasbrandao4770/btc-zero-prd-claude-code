---
name: git-workflow
description: Git workflow automation and best practices. Activates when git operations are mentioned (commit, push, branch, merge, PR), when preparing code for version control, or when user asks about git workflows. Provides conventional commit formats and branching strategies.
---

# Git Workflow

## When This Skill Activates

- Git operations mentioned (commit, push, branch, merge, PR)
- Preparing code for version control
- User asks about git best practices
- Creating pull requests

## Commit Message Format

### Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add login endpoint` |
| `fix` | Bug fix | `fix(billing): correct tax calculation` |
| `docs` | Documentation only | `docs(readme): update installation steps` |
| `style` | Code style (no logic change) | `style: apply ruff formatting` |
| `refactor` | Code restructure | `refactor(api): extract validation logic` |
| `test` | Adding tests | `test(billing): add unit tests for totals` |
| `chore` | Maintenance | `chore(deps): update dependencies` |

### Good Commit Examples

```bash
# Feature
git commit -m "feat(faturamento): add CPF validation to patient model

Implements regex-based CPF validation with checksum verification.
Handles both formatted (xxx.xxx.xxx-xx) and unformatted input.

Closes #123"

# Bug fix
git commit -m "fix(billing): use Decimal for financial calculations

Fixes floating point precision errors in billing totals.
All money values now use Decimal type."

# Refactor
git commit -m "refactor(api): extract ETL logic to pipeline module

Separates data processing from API endpoints for better testability.
No functional changes."
```

## Branching Strategy

```
main (production)
  │
  └── develop (integration)
        │
        ├── feature/billing-validation
        ├── feature/api-endpoints
        ├── fix/data-import-bug
        └── refactor/pipeline-cleanup
```

### Branch Naming

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feature/` | New features | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/login-timeout` |
| `refactor/` | Code restructuring | `refactor/database-layer` |
| `hotfix/` | Critical production fixes | `hotfix/security-patch` |
| `docs/` | Documentation updates | `docs/api-reference` |

## Pre-Commit Checklist

Before committing:

- [ ] Code quality checks passed (ruff format, ruff check)
- [ ] Type checking passes (pyright/mypy)
- [ ] Tests added/updated for changes
- [ ] No debug code (print statements, commented code)
- [ ] Documentation updated if needed
- [ ] Commit message follows convention

## Common Workflows

### Start New Feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
```

### Commit Changes
```bash
# Stage specific files
git add path/to/file.py

# Or stage all changes
git add .

# Commit with conventional message
git commit -m "feat(scope): description"
```

### Push Feature Branch
```bash
git push -u origin feature/my-feature
```

### Create Pull Request
```bash
# Using GitHub CLI
gh pr create --title "feat(scope): description" --body "## Summary
- Change 1
- Change 2

## Testing
- [ ] Unit tests
- [ ] Manual testing"
```

### Merge to Develop
```bash
git checkout develop
git pull origin develop
git merge feature/my-feature --no-ff
git push origin develop
```

## Pull Request Template

```markdown
## Summary
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## Git Configuration

```bash
# Useful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate"

# Line endings (Windows)
git config --global core.autocrlf input

# Default branch name
git config --global init.defaultBranch main
```

## Troubleshooting

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Discard Local Changes
```bash
git checkout -- path/to/file.py
```

### Update Feature Branch with Develop
```bash
git checkout feature/my-feature
git rebase develop
# Or merge if you prefer
git merge develop
```

### Fix Commit Message
```bash
# Only if not pushed yet!
git commit --amend -m "corrected message"
```
