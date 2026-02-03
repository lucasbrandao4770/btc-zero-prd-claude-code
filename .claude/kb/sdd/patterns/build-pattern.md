# Build Pattern

> Implementing with verification (EXECUTE)

---

## Purpose

The Build phase executes the implementation defined in Design. It's not just "write code"—it's a **structured process** with:

1. **File manifest execution** in dependency order
2. **Verification loops** for each component
3. **Continuous validation** against acceptance tests
4. **Progress tracking** for session recovery
5. **BUILD_REPORT** documenting what was done

---

## The Golden Rules

### 1. Follow the File Manifest

Build in the order specified:

```text
Design says:          Build executes:
1. schemas/           ✓ Create schemas
2. adapters/          ✓ Create adapters (after schemas)
3. functions/         ✓ Create functions (after adapters)
4. tests/             ✓ Create tests (with each component)
```

### 2. Verify Each Component

Don't move on until verified:

```text
Create ──▶ Test ──▶ Verify ──▶ Next
   ↑                   │
   └───── Retry ◀──────┘
         (if failed)
```

### 3. No Deviations Without Documentation

If Design needs changes:

```markdown
## Deviation D-001

**Design Said**: Use synchronous processing
**What Changed**: Switched to async for performance
**Rationale**: Sync approach caused 45s latency (exceeds 30s SLA)
**Impact**: Added asyncio dependency
```

---

## The Pattern

### Step 1: Parse the File Manifest

Extract from DESIGN document:

```python
# File manifest from Design
files = [
    ("shared/schemas/invoice.py", []),
    ("shared/schemas/messages.py", ["invoice.py"]),
    ("shared/adapters/storage.py", ["schemas"]),
    ("shared/adapters/messaging.py", ["schemas"]),
    ("functions/extractor/main.py", ["adapters"]),
    ("tests/unit/test_schemas.py", ["schemas"]),
]
```

### Step 2: Order by Dependencies

```text
Level 0 (no deps):   schemas/invoice.py
Level 1:             schemas/messages.py
Level 2:             adapters/storage.py, adapters/messaging.py
Level 3:             functions/extractor/main.py
Level 4:             tests/unit/test_schemas.py
```

### Step 3: Create Each File with Verification

For each file in order:

```markdown
### Creating: shared/schemas/invoice.py

**Following Pattern**: Design Section 4.1 (Pydantic Model with Validation)

**Verification**:
```bash
python -c "from shared.schemas.invoice import Invoice; print('OK')"
pytest tests/unit/test_schemas.py::test_invoice_valid -v
```

**Result**: ✅ PASS

---

### Creating: shared/adapters/storage.py

**Following Pattern**: Design Section 4.2 (Adapter Pattern)

**Verification**:
```bash
python -c "from shared.adapters.storage import GCSAdapter; print('OK')"
pytest tests/unit/test_adapters.py::test_storage -v
```

**Result**: ✅ PASS
```

### Step 4: Run Full Validation

After all files created:

```bash
# Lint check
ruff check src/

# Type check
mypy src/

# All tests
pytest -v --tb=short

# Acceptance tests
pytest tests/acceptance/ -v
```

### Step 5: Generate BUILD_REPORT

Document everything:

```markdown
# BUILD_REPORT: Invoice Pipeline

## Summary

| Metric | Value |
|--------|-------|
| Files Created | 12 |
| Files Modified | 2 |
| Tests Added | 28 |
| Test Coverage | 87% |
| Build Duration | 3.5 hours |

## Files Created

| File | Lines | Status |
|------|-------|--------|
| shared/schemas/invoice.py | 145 | ✅ |
| shared/schemas/messages.py | 67 | ✅ |
| shared/adapters/storage.py | 89 | ✅ |
| ... | ... | ... |

## Deviations from Design

### D-001: Async Processing

**Design Said**: Synchronous function calls
**Changed To**: Async with asyncio
**Rationale**: Sync caused 45s latency, exceeding 30s SLA
**Impact**: Added asyncio dependency

## Test Results

```
tests/unit/test_schemas.py .................... PASSED
tests/unit/test_adapters.py ................... PASSED
tests/integration/test_pipeline.py ............ PASSED

======================== 28 passed in 4.32s ========================
```

## Acceptance Test Verification

| ID | Scenario | Status |
|----|----------|--------|
| AT-001 | Happy path | ✅ PASS |
| AT-002 | Multi-page | ✅ PASS |
| AT-003 | All vendors | ✅ PASS |
| AT-004 | Invalid file | ✅ PASS |
| AT-005 | Duplicate | ✅ PASS |
```

---

## Verification Loop

### The Cycle

```text
┌─────────────────────────────────────────────────────────┐
│                 BUILD VERIFICATION LOOP                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   1. CREATE ──────▶ Write file following Design pattern │
│        │                                                 │
│        ▼                                                 │
│   2. TEST ────────▶ Run verification command            │
│        │                                                 │
│        ▼                                                 │
│   3. VERIFY ──────▶ Check: Does it pass?                │
│        │                    │                            │
│        │    YES ◀───────────┘                           │
│        │    │                                            │
│        ▼    ▼                                            │
│   4. LOG ─────────▶ Record in BUILD_REPORT              │
│        │                                                 │
│        ▼                                                 │
│   5. NEXT ────────▶ Move to next file                   │
│        │                                                 │
│        ▼                                                 │
│   (If VERIFY = NO)                                      │
│        │                                                 │
│   6. RETRY ───────▶ Fix and loop back to TEST           │
│        │            (max 3 retries)                      │
│        │                                                 │
│   (If max retries exceeded)                             │
│        │                                                 │
│   7. ESCALATE ────▶ Document blocker, continue or halt  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Retry Strategy

```markdown
## Retry: shared/adapters/storage.py

**Attempt 1**: ImportError - missing google-cloud-storage
**Fix**: Added to requirements.txt
**Result**: ❌ FAIL

**Attempt 2**: TypeError - wrong bucket name format
**Fix**: Changed bucket name to lowercase with hyphens
**Result**: ✅ PASS
```

### When to Escalate

| Situation | Action |
|-----------|--------|
| 3 consecutive failures | Document blocker in BUILD_REPORT |
| Missing dependency not in Design | Add to Deviations, continue |
| Design impossible to implement | Halt, run /iterate on DESIGN |
| Test reveals requirement gap | Document, create follow-up task |

---

## Progress Tracking

### For Long Sessions

Track progress for recovery:

```markdown
## Build Progress

| # | File | Status | Timestamp |
|---|------|--------|-----------|
| 1 | schemas/invoice.py | ✅ Complete | 10:15 |
| 2 | schemas/messages.py | ✅ Complete | 10:32 |
| 3 | adapters/storage.py | ✅ Complete | 10:58 |
| 4 | adapters/messaging.py | 🔄 In Progress | 11:15 |
| 5 | functions/extractor/main.py | ⏳ Pending | - |
```

### Session Recovery

If interrupted, resume from last complete file:

```bash
# Resume build from where we left off
/build .claude/sdd/features/DESIGN_INVOICE_PIPELINE.md --resume

# Reads progress, skips completed files, continues
```

---

## Quality Gate

Before proceeding to Ship:

| Criteria | Check |
|----------|-------|
| All files from manifest created | ☐ |
| All verification commands pass | ☐ |
| Lint check passes (ruff/eslint) | ☐ |
| Type check passes (mypy/tsc) | ☐ |
| All tests pass | ☐ |
| Acceptance tests pass | ☐ |
| No unresolved blockers | ☐ |
| BUILD_REPORT complete | ☐ |

---

## Output Template

```markdown
# BUILD_REPORT: {Feature Name}

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {date} |
| **Author** | build-agent |
| **Source** | DESIGN_{FEATURE}.md |
| **Duration** | {X hours} |

---

## Summary

| Metric | Value |
|--------|-------|
| Files Created | |
| Files Modified | |
| Tests Added | |
| Test Coverage | |

---

## Files Created

| File | Lines | Status |
|------|-------|--------|
| | | |

---

## Deviations from Design

### D-001: {Title}

**Design Said**: {original}
**Changed To**: {new}
**Rationale**: {why}
**Impact**: {consequences}

---

## Test Results

```
{test output}
```

---

## Acceptance Test Verification

| ID | Scenario | Status |
|----|----------|--------|
| AT-001 | | |

---

## Issues Encountered

### Issue 1: {Title}

**Problem**: {description}
**Resolution**: {how fixed}

---

## Next Step

`/ship .claude/sdd/features/DEFINE_{FEATURE}.md`
```

---

## Common Pitfalls

### 1. Building Without Following Manifest

❌ **Wrong**:
```text
"I'll start with the most interesting part..."
"Let me build this helper file that's not in the manifest..."
```

✅ **Right**:
```text
"Following manifest order: starting with schemas/invoice.py (no deps)"
"All files built per manifest. No additional files created."
```

### 2. Skipping Verification

❌ **Wrong**:
```text
"File looks good, moving on..."
"I'll test everything at the end..."
```

✅ **Right**:
```text
"Verification for schemas/invoice.py:
  $ python -c 'from schemas.invoice import Invoice; print(OK)'
  Result: OK
Moving to next file."
```

### 3. Undocumented Deviations

❌ **Wrong**:
```text
(Silently changes implementation approach without noting it)
```

✅ **Right**:
```markdown
## Deviation D-001: Changed Database

**Design Said**: Use PostgreSQL
**Changed To**: SQLite for MVP
**Rationale**: Local development simplicity; PostgreSQL for prod
**Impact**: Need migration script for prod deployment
```

### 4. Continuing Past Blockers

❌ **Wrong**:
```text
"Test failed but probably fine, continuing..."
```

✅ **Right**:
```text
"Test failed (attempt 2/3). Analyzing error...
Fix applied: [description]
Re-running verification..."
```

---

## Model Assignment

| Task Type | Recommended Model |
|-----------|-------------------|
| Code generation | Sonnet (fast, accurate) |
| Complex debugging | Opus (deep analysis) |
| Test writing | Sonnet |
| Documentation | Haiku or Sonnet |

---

## Integration with Dev Loop

Build phase aligns with Dev Loop's execution model:

```text
Dev Loop                    SDD Build
────────                    ─────────
PROMPT.md tasks       ≈     File manifest
Verification loops    ≈     Build verification
PROGRESS.md           ≈     Build progress tracking
LOG.md                ≈     BUILD_REPORT.md
```

Both emphasize verification before proceeding.

---

## Next Steps

- **After Build**: [ship-pattern.md](ship-pattern.md)
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Example**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)

---

*References: AgentSpec 4.2 Phase 3, Dev Loop verification patterns*
