---
name: code-quality-pipeline
description: Automated code quality checks for Python projects. Activates when Python files are created or modified, when user mentions quality/lint/format/type-check, or when preparing for git commits. Ensures ruff formatting, linting, type hints, and docstrings.
---

# Code Quality Pipeline

## When This Skill Activates

- Python files (`.py`) are created or modified
- User mentions: quality, lint, format, type check, clean code
- Preparing for git commit
- Code review requested

## Quality Workflow

### Step 1: Format with Ruff
```bash
# Format code
ruff format {file_or_directory}

# Check formatting without applying
ruff format --check {file_or_directory}
```

### Step 2: Lint with Ruff
```bash
# Check and auto-fix
ruff check {file_or_directory} --fix

# Check without fixing
ruff check {file_or_directory}
```

### Step 3: Type Check
```bash
# Pyright (recommended)
pyright {file_or_directory}

# Or mypy
mypy {file_or_directory} --strict
```

## Quality Checklist

Before marking Python code complete:

- [ ] **Ruff formatting** applied (no changes needed)
- [ ] **Ruff linting** passes (0 errors, minimal warnings)
- [ ] **Type hints** on all function signatures
- [ ] **Docstrings** on public APIs (classes, functions)
- [ ] **No print statements** (use logging instead)
- [ ] **Error handling** for external calls
- [ ] **No commented-out code** (delete or document why kept)

## Type Hints Standard

```python
from typing import Any
from collections.abc import Sequence

def process_data(
    items: list[dict[str, Any]],
    config: dict[str, str] | None = None,
) -> list[str]:
    """Process items and return results.

    Args:
        items: List of item dictionaries to process
        config: Optional configuration overrides

    Returns:
        List of processed item identifiers

    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")

    return [item["id"] for item in items]
```

## Docstring Format (Google Style)

```python
def calculate_total(
    items: list[BillingItem],
    apply_tax: bool = True,
) -> Decimal:
    """Calculate total billing amount.

    Sums all item amounts and optionally applies tax.
    Uses Decimal for financial precision.

    Args:
        items: List of billing items to sum
        apply_tax: Whether to apply tax rate (default: True)

    Returns:
        Total amount as Decimal

    Raises:
        ValueError: If items list is empty

    Example:
        >>> items = [BillingItem(amount=Decimal("10.00"))]
        >>> calculate_total(items)
        Decimal('10.50')  # With 5% tax
    """
```

## Common Ruff Configuration

```toml
# pyproject.toml or ruff.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
```

## Pre-Commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## VS Code Settings

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  }
}
```

## Quick Commands

| Action | Command |
|--------|---------|
| Format file | `ruff format path/to/file.py` |
| Format directory | `ruff format .` |
| Lint and fix | `ruff check . --fix` |
| Type check | `pyright .` |
| All checks | `ruff format . && ruff check . && pyright .` |
