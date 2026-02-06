# PROMPT: VALID_TEST

> A complete PROMPT file with all sections for testing

---

## Goal

Build a test feature that demonstrates all PROMPT file sections work correctly.

---

## Quality Tier

**Tier:** production

| Tier | Expectations |
|------|--------------|
| `prototype` | Speed over perfection. Skip edge cases. Minimal tests. |
| `production` | Tests required. Best practices. Full verification. |
| `library` | Backward compatibility. Full documentation. API stability. |

---

## Context

This is a test PROMPT file used for validating the parser.

---

## Tasks (Prioritized)

### 🔴 RISKY (Do First)

- [x] **Setup project structure**
  Create the basic folder structure.
  Verify: `python -c "print('OK')"`

- [ ] @python-developer: **Implement core logic**
  Build the main functionality.

### 🟡 CORE

- [ ] **Add configuration module**
  Create config.py with settings.

- [x] @test-generator: **Write unit tests**
  Add comprehensive test coverage.

- [ ] **Build main component**
  Implement the primary feature.

### 🟢 POLISH (Do Last)

- [ ] **Add documentation**
  Write README and docstrings.

- [ ] **Improve error messages**
  Make errors more user-friendly.

---

## Exit Criteria

- [x] All tests pass: `pytest tests/ -v`
- [ ] Lint passes: `ruff check .`
- [ ] Type check passes: `mypy . --ignore-missing-imports`

---

## Progress

**Status:** IN_PROGRESS

| Iteration | Timestamp | Task Completed | Key Decision | Files Changed |
|-----------|-----------|----------------|--------------|---------------|
| 1 | 2026-02-05 | Setup project | Used pathlib | config.py |
| 2 | 2026-02-05 | Unit tests | pytest fixtures | test_*.py |

---

## Config

```yaml
mode: hitl
quality_tier: production
max_iterations: 30
max_retries: 3
circuit_breaker: 3
small_steps: true
feedback_loops:
  - pytest tests/ -v
  - ruff check .
```

---

## Notes

Test notes section.

---

*Generated for testing purposes*
