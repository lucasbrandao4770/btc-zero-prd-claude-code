# Spec-Kit: GitHub's SDD Implementation

> Official SDD toolkit from GitHub

---

## Overview

**Spec-Kit** is GitHub's open-source implementation of Spec-Driven Development. It provides:

- CLI tool (`specify`) for project initialization
- Slash commands for the SDD workflow
- Templates for specifications and plans
- Constitutional principles for architectural discipline
- Multi-agent support (Claude, Gemini, Copilot, and more)

**Repository**: https://github.com/github/spec-kit

---

## Installation

```bash
# Persistent installation (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# One-time usage
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

# Initialize existing project
specify init . --ai claude
```

---

## Commands

### Core Commands

| Command | Purpose | Phase |
|---------|---------|-------|
| `/speckit.constitution` | Create project principles | Setup |
| `/speckit.specify` | Define requirements (WHAT) | Specify |
| `/speckit.plan` | Create technical plan (HOW) | Plan |
| `/speckit.tasks` | Generate task breakdown | Tasks |
| `/speckit.implement` | Execute implementation | Build |

### Optional Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/speckit.clarify` | Clarify underspecified areas | Before planning |
| `/speckit.analyze` | Cross-artifact consistency check | Before implementation |
| `/speckit.checklist` | Generate quality checklists | After specification |

---

## Workflow

### Step 1: Initialize Project

```bash
specify init my-project --ai claude
cd my-project
```

Creates:
```text
.specify/
├── memory/
│   └── constitution.md
├── scripts/
│   ├── create-new-feature.sh
│   └── setup-plan.sh
├── specs/
│   └── (feature specs go here)
└── templates/
    ├── spec-template.md
    ├── plan-template.md
    └── tasks-template.md
```

### Step 2: Establish Constitution

```bash
/speckit.constitution Create principles focused on code quality,
testing standards, and performance requirements
```

Creates `memory/constitution.md` with governing principles that guide all subsequent development.

### Step 3: Create Specification

```bash
/speckit.specify Build an application that helps organize photos
in albums, grouped by date with drag-and-drop reordering
```

Creates:
- New branch (e.g., `001-photo-albums`)
- `specs/001-photo-albums/spec.md`

### Step 4: Clarify (Optional but Recommended)

```bash
/speckit.clarify
```

Systematically identifies and resolves ambiguities before planning.

### Step 5: Create Plan

```bash
/speckit.plan Use Vite with vanilla HTML/CSS/JS.
Images stored locally, metadata in SQLite.
```

Creates:
- `specs/001-photo-albums/plan.md`
- `specs/001-photo-albums/research.md`
- `specs/001-photo-albums/data-model.md`
- `specs/001-photo-albums/contracts/` (API specs)

### Step 6: Generate Tasks

```bash
/speckit.tasks
```

Creates `specs/001-photo-albums/tasks.md` with:
- Tasks organized by user story
- Dependency ordering
- Parallel execution markers `[P]`
- Test-first task ordering

### Step 7: Implement

```bash
/speckit.implement
```

Executes tasks in order, respecting dependencies and running tests.

---

## The Constitution

Spec-Kit's unique feature is the **constitution**—a set of immutable principles governing development.

### The Nine Articles

| Article | Principle | Enforcement |
|---------|-----------|-------------|
| I | Library-First | Every feature starts as standalone library |
| II | CLI Interface | All libraries expose CLI with text I/O |
| III | Test-First | No code before tests (TDD) |
| IV | Single Responsibility | Each component has one purpose |
| V | Dependency Inversion | Depend on abstractions |
| VI | Interface Segregation | Small, focused interfaces |
| VII | Simplicity | Maximum 3 projects initially |
| VIII | Anti-Abstraction | Use framework directly, no wrappers |
| IX | Integration-First | Real environments over mocks |

### How Constitution Enforces Quality

```markdown
### Phase -1: Pre-Implementation Gates

#### Simplicity Gate (Article VII)
- [ ] Using ≤3 projects?
- [ ] No future-proofing?

#### Anti-Abstraction Gate (Article VIII)
- [ ] Using framework directly?
- [ ] Single model representation?

#### Integration-First Gate (Article IX)
- [ ] Contracts defined?
- [ ] Contract tests written?
```

---

## Templates

### Specification Template Key Sections

```markdown
## User Scenarios & Testing (mandatory)

### User Story 1 - [Title] (Priority: P1)
[Description]

**Why this priority**: [Value explanation]
**Independent Test**: [How to test independently]

**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]

## Requirements (mandatory)
- **FR-001**: System MUST [capability]
- **FR-002**: Users MUST be able to [interaction]

## Success Criteria (mandatory)
- **SC-001**: [Measurable metric]
```

### Plan Template Key Sections

```markdown
## Architecture Overview
[High-level architecture]

## Technical Decisions
[Major technology choices]

## File Structure
[Complete file listing]

## Implementation Phases
[Ordered phases with deliverables]

## Pre-Implementation Gates
[Constitutional compliance checks]
```

---

## Template-Driven Quality

Spec-Kit templates constrain LLM behavior for better outcomes:

### 1. Preventing Premature Implementation

```text
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
```

### 2. Forcing Explicit Uncertainty

```text
[NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
```

### 3. Structured Self-Review

Checklists act as "unit tests" for specifications:

```markdown
### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
```

---

## Supported AI Agents

| Agent | Support |
|-------|---------|
| Claude Code | ✅ |
| GitHub Copilot | ✅ |
| Cursor | ✅ |
| Gemini CLI | ✅ |
| Codex CLI | ✅ |
| Windsurf | ✅ |
| Amp | ✅ |
| Amazon Q | ⚠️ (limited) |

---

## Project Structure

After full workflow:

```text
.specify/
├── memory/
│   └── constitution.md          # Governing principles
├── scripts/
│   ├── create-new-feature.sh
│   ├── setup-plan.sh
│   └── update-claude-md.sh
├── specs/
│   └── 001-photo-albums/
│       ├── spec.md              # Requirements
│       ├── plan.md              # Technical plan
│       ├── tasks.md             # Task breakdown
│       ├── research.md          # Tech research
│       ├── data-model.md        # Data structures
│       ├── quickstart.md        # Validation guide
│       └── contracts/
│           ├── api-spec.json    # API contracts
│           └── events.md        # Event definitions
└── templates/
    ├── spec-template.md
    ├── plan-template.md
    └── tasks-template.md
```

---

## Key Differentiators

### vs. Traditional Development

| Aspect | Traditional | Spec-Kit |
|--------|-------------|----------|
| Documentation | Optional, often stale | Executable, always current |
| Governance | Code review only | Constitutional principles |
| Structure | Ad-hoc | Branch-per-feature, templated |
| Quality | Post-implementation | Pre-implementation gates |

### vs. AgentSpec

| Aspect | Spec-Kit | AgentSpec |
|--------|----------|-----------|
| Focus | GitHub/general projects | Claude Code ecosystem |
| Constitution | Required | Optional |
| Phases | Specify → Plan → Tasks → Implement | Brainstorm → Define → Design → Build → Ship |
| Brainstorm | Via /speckit.clarify | Dedicated phase |
| Templates | Markdown-centric | YAML + Markdown |
| Archival | Git branches | Archive folder |

See [comparison.md](comparison.md) for detailed comparison.

---

## Best Practices

### 1. Always Start with Constitution

```bash
/speckit.constitution
```

Even simple projects benefit from explicit principles.

### 2. Use Clarify Before Plan

```bash
/speckit.clarify
```

Reduces downstream rework by catching ambiguities early.

### 3. Review Generated Tasks

Before `/speckit.implement`, review `tasks.md` for:
- Correct ordering
- Appropriate parallelization
- Missing edge cases

### 4. Leverage Research Phase

The `research.md` file captures technology investigation:

```bash
/speckit.plan Research the latest React Server Components
patterns for this implementation
```

---

## Resources

- **GitHub Repository**: https://github.com/github/spec-kit
- **Video Overview**: https://youtube.com/watch?v=a9eR1xsfvHg
- **Documentation**: https://github.github.io/spec-kit/
- **Philosophy**: `/spec-driven.md` in repo

---

*References: Spec-Kit README.md, spec-driven.md, templates/*
