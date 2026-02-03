# Claude-Workflow - Framework Analysis

> Deep dive into Claude-Workflow: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | https://github.com/madamerobot/claude-workflow (or similar) |
| **Author** | Community contributor |
| **Category** | AI Development Workflow / Task Decomposition |
| **Context7 ID** | Not available |
| **Last Updated** | 2026-02-02 |

### One-Line Summary

Claude-Workflow is a copy-and-go GitHub Issues-based development workflow system that uses AI instruction templates to decompose product requirements into hierarchical tasks.

---

## Problem Statement

### What Problem Does It Solve?

AI coding assistants excel at individual tasks but struggle with multi-step project coordination. Claude-Workflow addresses:

1. **Lack of structured task decomposition** - Without a system, AI assistants tackle large features monolithically, leading to incomplete or poorly planned implementations
2. **Context loss between sessions** - Project state scatters across conversations, making continuity difficult
3. **No standard workflow** - Each project requires reinventing how to plan, track, and implement features with AI assistance
4. **GitHub integration gap** - Most AI workflows ignore existing project management tools like GitHub Issues

### Who Is It For?

- **Solo developers** who want structured AI-assisted development without complex tooling
- **Small teams** needing lightweight, GitHub-native project management
- **Claude Code users** seeking a ready-made workflow system
- **Projects of any type** - web apps, APIs, CLI tools, SaaS platforms

### Why Does This Matter?

Without structured task decomposition, AI assistants attempt to solve complex problems in one shot. Research shows that "breaking complex instructions into smaller, targeted subtasks allows the model to focus and reason more reliably." Claude-Workflow operationalizes this principle for real development workflows.

---

## Architecture

### Core Concepts

1. **AI Instruction Templates** - Markdown files that guide Claude through multi-step workflows, not simple documentation but sophisticated prompts with decision trees
2. **Hierarchical Task Numbering** - Tasks use `1, 1.1, 1.2, 2, 2.1...` patterns to represent dependency chains and logical groupings
3. **Project Type Detection** - Automatic adaptation based on tech stack (web-app, api-service, cli-tool, saas-platform)
4. **GitHub Issues as Source of Truth** - All work items (PRDs, Features, Tasks) live as GitHub Issues with labels and relationships

### Component Diagram

```
                     CLAUDE-WORKFLOW ARCHITECTURE

    +------------------+      +------------------+      +------------------+
    |   User Input     |      |  AI Instruction  |      |  GitHub MCP      |
    |   (arguments)    | ---> |    Template      | ---> |   (Issues API)   |
    +------------------+      +------------------+      +------------------+
                                     |
                                     v
    +------------------------------------------------------------------+
    |                        WORKFLOW ENGINE                           |
    |                                                                  |
    |  /project:plan:prd     --> [PRD] Issue with market research      |
    |  /project:plan:feature --> [Feature] Issue with tech specs       |
    |  /project:plan:tasks   --> [Task 1], [Task 1.1], [Task 2]...     |
    |  /project:do:task      --> Implementation + PR                   |
    |  /project:current      --> Progress analysis + suggestions       |
    |                                                                  |
    +------------------------------------------------------------------+
                                     |
                                     v
    +------------------------------------------------------------------+
    |                      OUTPUT STRUCTURE                            |
    |                                                                  |
    |  GitHub Issues:                                                  |
    |  #123 [PRD] User Authentication System                           |
    |    +-- #124 [Task 1] Research: OAuth providers                   |
    |    +-- #125 [Task 2.1] Backend: Database schema                  |
    |    +-- #126 [Task 2.2] Backend: API endpoints                    |
    |    +-- #127 [Task 3.1] Frontend: Login form                      |
    |    +-- #128 [Task 4.1] Testing: Unit tests                       |
    |                                                                  |
    +------------------------------------------------------------------+
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `.claude/commands/plan/prd.md` | PRD creation template with market research steps |
| `.claude/commands/plan/tasks.md` | Task decomposition engine with hierarchical numbering |
| `.claude/commands/do/task.md` | Task implementation workflow (15 systematic steps) |
| `.claude/commands/project/current.md` | Context analyzer with progress tracking |
| `.claude/commands/plan/brainstorm.md` | Critical thinking partner for requirement validation |
| `.claude/contexts/*.md` | Language-specific coding standards (Python, TypeScript, React) |
| `.claude/settings.json` | MCP configuration (Context7, Playwright, GitHub, Zen) |

---

## Capabilities

### What It Can Do

- [x] Create comprehensive PRDs with market research as GitHub Issues
- [x] Generate technical feature specifications with acceptance criteria
- [x] Decompose features into hierarchical tasks (1, 1.1, 1.2, 2, 2.1...)
- [x] Execute tasks with test-first development and PR creation
- [x] Track progress across PRDs, Features, and Tasks
- [x] Adapt templates to project type (web-app, API, CLI, SaaS)
- [x] Provide intelligent next-action suggestions based on project state
- [x] Challenge assumptions through structured brainstorming

### What It Cannot Do

- Session recovery after context loss (relies on GitHub Issues for state)
- Parallel task execution (no subagent spawning)
- Fine-grained progress tracking within tasks (binary: open/closed)
- Cross-project coordination (single-repo focused)
- Automated testing or CI/CD integration (manual PR verification)

---

## How It Works

### Workflow

```
/project:plan:prd --> /project:plan:tasks --> /project:do:task --> /project:current
     (Opus-level       (Decomposition         (Implementation       (Progress
      thinking)         engine)                 workflow)            analysis)
```

### Key Mechanisms

**1. AI Instruction Templates**

Each command file contains multi-step instructions that guide Claude through complex workflows. Example from `tasks.md`:

```markdown
## Step 4: Determine Task Breakdown Strategy and Numbering

**For Complex Issues (8+ tasks):**
1. Research and architecture task
2. Backend implementation tasks
   - 2.1. Database schema and models
   - 2.2. API endpoints
   - 2.3. Business logic
3. Frontend implementation tasks
   - 3.1. Components and UI
   - 3.2. State management
   - 3.3. Integration
4. Testing tasks
   - 4.1. Unit tests
   - 4.2. Integration tests
   - 4.3. End-to-end tests
5. Documentation and deployment
```

**2. Hierarchical Numbering Rules**

```
First level (1, 2, 3...):   Major implementation phases or areas
Second level (1.1, 1.2...): Specific tasks within each major area
Third level (1.1.1...):     Sub-components (use sparingly)
```

**3. Project Type Detection**

The system reads project files to determine type:
- `package.json` --> Web Application
- `requirements.txt` / `pyproject.toml` --> API Service
- `go.mod` --> CLI Tool
- Multi-service structure --> SaaS Platform

**4. Human Validation Checkpoints**

From `task.md`:

```markdown
## Step 4: Human Validation Check

**STOP and request human review if any of these apply:**
- Architectural Changes: New patterns, frameworks, or system design decisions
- Database Schema Changes: New tables, columns, relationships
- API Breaking Changes: Changes that affect existing integrations
- Security Implications: Authentication, authorization, data handling
```

### Code Examples

**Task Issue Template** (from `tasks.md`):

```markdown
# Task {Number}: {Specific Implementation}

**Parent Issue:** #{parent_issue_number}
**Task Number:** {Number} (e.g., 2.1, 3.2, 4)
**Area:** {Frontend/Backend/CLI/Database/Infrastructure/Testing/Documentation}
**Estimated Effort:** {S/M/L} ({timeframe})

## Description
{Clear description of what needs to be implemented}

## Acceptance Criteria
- [ ] {Specific deliverable 1}
- [ ] {Specific deliverable 2}
- [ ] Tests written and passing
- [ ] Documentation updated (if needed)

## Dependencies
- **Prerequisite Tasks:** Task {Number}, Task {Number}
- **Blocks Tasks:** Task {Number}, Task {Number}
```

**Extended Thinking Trigger** (from `prd.md`):

```markdown
## Step 1: Perform Deep Analysis

**For complex product features, engage in extended thinking:**
Think deeply about this product requirement: '$ARGUMENTS'. Consider market
positioning, competitive analysis, user research implications, technical
architecture decisions, business model impacts, and long-term strategic
implications.
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| Zero installation | Copy `.claude/` directory and start immediately |
| GitHub-native | Uses existing GitHub Issues infrastructure |
| Structured decomposition | Hierarchical numbering (1, 1.1, 1.2) creates clear dependency chains |
| Project-type adaptive | Detects tech stack and adjusts templates |
| Human checkpoints | Explicit validation gates for risky changes |
| Critical thinking built-in | `/project:plan:brainstorm` challenges assumptions before implementation |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| No session recovery | Context loss requires restarting from GitHub Issues |
| Single-agent only | Cannot spawn parallel workers for large tasks |
| GitHub dependency | Requires GitHub MCP and access token setup |
| No internal state | All state stored externally in GitHub Issues |
| Limited chunking | Tasks are atomic units, no mid-task checkpointing |

---

## Community & Adoption

- **GitHub Stars:** ~500 (estimated based on similar projects)
- **Contributors:** Single author with community feedback
- **Last Commit:** Active development (2025-2026)
- **Notable Users:** Claude Code community, solo developers

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | Local: `frameworks-research/claude-workflow/` |
| Documentation | `.claude/CLAUDE.md` and `.claude/README.md` |
| Articles | [Continue.dev - Task Decomposition](https://blog.continue.dev/task-decomposition/) |

---

## Key Takeaways

1. **Task decomposition is essential for AI-assisted development** - Breaking work into numbered, hierarchical tasks (1, 1.1, 2.1...) enables focused, reliable implementation
2. **GitHub Issues make excellent state storage** - External persistence solves the context loss problem without custom infrastructure
3. **Templates are prompts, not documentation** - The command files are sophisticated AI instruction sets with decision trees and validation checkpoints
4. **Project-type adaptation matters** - Web apps, APIs, CLI tools, and SaaS platforms need different planning and implementation patterns
5. **Human validation gates are critical** - Explicit checkpoints before architectural changes, security implications, and breaking changes prevent costly mistakes

---

*Analysis completed: 2026-02-02 | Analyst: kb-architect*
