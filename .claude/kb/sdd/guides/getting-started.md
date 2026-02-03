# Getting Started with SDD

> Your first Spec-Driven Development project

---

## Prerequisites

Before starting:

1. **Claude Code CLI** installed and configured
2. **Project folder** initialized (git recommended)
3. **Basic understanding** of what you want to build

---

## Quick Start (5 Minutes)

### 1. Start with a Clear Idea

Think about:
- What problem are you solving?
- Who will use this?
- What does "done" look like?

**Example**: "I want to build a CLI tool that converts Markdown to HTML"

### 2. Choose Your Entry Point

| If your idea is... | Start with... |
|-------------------|---------------|
| Vague, exploratory | `/brainstorm` |
| Clear requirements | `/define` |
| Already planned | `/design` |

### 3. Follow the Pipeline

```bash
# For most features
/define "Build a CLI tool that converts Markdown to HTML"

# After DEFINE is complete
/design .claude/sdd/features/DEFINE_MD_TO_HTML.md

# After DESIGN is complete
/build .claude/sdd/features/DESIGN_MD_TO_HTML.md

# After BUILD is complete
/ship .claude/sdd/features/DEFINE_MD_TO_HTML.md
```

---

## Your First SDD Feature

### Step 1: Define Requirements

```bash
/define "Build a CLI tool that converts Markdown to HTML files"
```

**What happens**:
- AI asks clarifying questions
- Creates `DEFINE_MD_TO_HTML.md`
- Calculates Clarity Score

**You'll see**:

```markdown
# DEFINE: Markdown to HTML Converter

## Problem Statement
Developers need to convert Markdown documentation to HTML
for web publishing. Manual conversion is tedious and error-prone.

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Convert .md files to .html |
| **MUST** | Preserve heading structure |
| **SHOULD** | Support code syntax highlighting |
| **COULD** | Generate table of contents |

## Success Criteria
| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Conversion accuracy | 100% valid HTML output |
| SC-002 | Processing speed | <1s for files under 100KB |

## Acceptance Tests
| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Basic conversion | A .md file | Run converter | Valid .html created |
| AT-002 | Code blocks | .md with ```python | Convert | Syntax highlighted |

## Clarity Score: 13/15 ✅
```

### Step 2: Create Technical Design

```bash
/design .claude/sdd/features/DEFINE_MD_TO_HTML.md
```

**What happens**:
- Creates architecture from requirements
- Generates file manifest
- Adds code patterns

**You'll see**:

```markdown
# DESIGN: Markdown to HTML Converter

## Architecture
```text
Input (.md) → Parser → Renderer → Output (.html)
```

## File Manifest
| # | File | Purpose |
|---|------|---------|
| 1 | src/parser.py | Markdown parsing |
| 2 | src/renderer.py | HTML rendering |
| 3 | src/cli.py | CLI interface |
| 4 | tests/test_parser.py | Parser tests |
| 5 | tests/test_renderer.py | Renderer tests |

## Code Patterns
```python
from markdown import Markdown

def convert(md_content: str) -> str:
    """Convert Markdown to HTML."""
    md = Markdown(extensions=['fenced_code', 'tables'])
    return md.convert(md_content)
```
```

### Step 3: Build Implementation

```bash
/build .claude/sdd/features/DESIGN_MD_TO_HTML.md
```

**What happens**:
- Creates files in order from manifest
- Verifies each component
- Generates BUILD_REPORT

**You'll see**:
- Code files being created
- Tests being written and run
- Verification output

### Step 4: Ship and Archive

```bash
/ship .claude/sdd/features/DEFINE_MD_TO_HTML.md
```

**What happens**:
- Moves all artifacts to archive
- Creates SHIPPED document
- Documents lessons learned

---

## Common First-Project Mistakes

### 1. Jumping to Code

❌ **Wrong**:
```text
"Let me just write the code, I know what I want"
```

✅ **Right**:
```text
"Let me define what I want first, then design, then build"
```

**Why**: SDD's power comes from specification-first. Skip it, lose the benefits.

### 2. Vague Requirements

❌ **Wrong**:
```markdown
## Goals
- Make it work
- Make it fast
- Make it good
```

✅ **Right**:
```markdown
## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Convert files in <1s (files under 100KB) |
| **MUST** | Output valid HTML5 |
| **SHOULD** | Support GFM extensions |
```

**Why**: Measurable goals enable verification.

### 3. Skipping Acceptance Tests

❌ **Wrong**:
```markdown
## Acceptance Tests
- It should work
```

✅ **Right**:
```markdown
## Acceptance Tests
| ID | Given | When | Then |
|----|-------|------|------|
| AT-001 | A .md file with headers | Convert | HTML has <h1>-<h6> tags |
| AT-002 | A .md file with code blocks | Convert | Code is syntax highlighted |
```

**Why**: Acceptance tests become verification criteria in Build.

### 4. Incomplete File Manifest

❌ **Wrong**:
```markdown
## Files
- Some source files
- Tests
```

✅ **Right**:
```markdown
## File Manifest
| # | File | Purpose | Dependencies |
|---|------|---------|--------------|
| 1 | src/parser.py | Parse MD | None |
| 2 | src/renderer.py | Render HTML | parser |
| 3 | src/cli.py | CLI | parser, renderer |
| 4 | tests/test_parser.py | Tests | parser |
```

**Why**: Build phase needs complete, ordered list.

---

## Practice Project Ideas

### Beginner (1-2 hours)

| Project | Complexity |
|---------|-----------|
| TODO list CLI | Low |
| File organizer | Low |
| Markdown to HTML | Low |
| Simple calculator | Low |

### Intermediate (2-4 hours)

| Project | Complexity |
|---------|-----------|
| URL shortener | Medium |
| API client wrapper | Medium |
| Log analyzer | Medium |
| Config file validator | Medium |

### Advanced (Multi-day)

| Project | Complexity |
|---------|-----------|
| Event-driven pipeline | High |
| Multi-agent system | High |
| Full-stack app | High |

---

## Checklist for Your First Feature

### Before Starting

- [ ] Clear idea of what to build
- [ ] Claude Code configured
- [ ] Project folder ready

### During Define

- [ ] Problem statement has numbers
- [ ] Goals use MoSCoW prioritization
- [ ] Success criteria are measurable
- [ ] Acceptance tests use Given/When/Then
- [ ] Out of scope is explicit
- [ ] Clarity Score ≥ 12/15

### During Design

- [ ] Architecture diagram present
- [ ] All decisions have rationale
- [ ] File manifest is complete
- [ ] Dependencies are clear
- [ ] Code patterns are copy-paste ready

### During Build

- [ ] Following manifest order
- [ ] Verifying each component
- [ ] All tests passing
- [ ] BUILD_REPORT complete

### During Ship

- [ ] All gates passed
- [ ] Artifacts archived
- [ ] Lessons documented

---

## Next Steps

After completing your first feature:

1. **Review lessons learned** - What worked? What didn't?
2. **Try a larger feature** - Apply what you learned
3. **Explore advanced patterns** - [advanced-sdd.md](advanced-sdd.md)
4. **Consider team adoption** - [migrating-to-sdd.md](migrating-to-sdd.md)

---

## Resources

- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)
- **Define pattern**: [../patterns/define-pattern.md](../patterns/define-pattern.md)
- **Real example**: [../examples/invoice-pipeline.md](../examples/invoice-pipeline.md)
- **Quick reference**: [../quick-reference.md](../quick-reference.md)

---

*Start small, learn the rhythm, then scale up.*
