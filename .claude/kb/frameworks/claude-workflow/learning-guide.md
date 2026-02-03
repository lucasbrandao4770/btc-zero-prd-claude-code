# Claude-Workflow - Learning Guide

> Educational resource for mastering Claude-Workflow concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand hierarchical task decomposition patterns (1, 1.1, 1.2...)
- [x] Learn how to create AI instruction templates that guide multi-step workflows
- [x] Be able to design effective human validation checkpoints
- [x] Apply critical thinking pre-planning patterns before implementation
- [x] Understand GitHub Issues as a state persistence mechanism

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Framework runs inside Claude Code | Claude Code documentation |
| GitHub Issues familiarity | State stored as GitHub Issues | GitHub docs |
| Markdown | Templates written in Markdown | Any Markdown tutorial |
| Basic project planning | Understanding PRD/Feature/Task hierarchy | PM fundamentals |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Beginner | Simple concepts, well-documented |
| Implementation | Beginner | Copy-and-go setup |
| Time Investment | 2-4 hours | Full understanding of all patterns |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Claude-Workflow is and why it matters

1. **Read the README**
   - Location: `frameworks-research/claude-workflow/README.md`
   - Time: 15 min
   - Key concepts to note: Slash commands, GitHub Issues workflow, project type detection

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, hierarchical numbering, key mechanisms

3. **Try the Quick Start**
   - Instructions:
     1. Copy `.claude/` to a test project
     2. Set `GITHUB_PERSONAL_ACCESS_TOKEN`
     3. Run `/project:current` to see context analysis
   - Expected outcome: Project type detection and workflow suggestions

**Checkpoint:** Can you explain what Claude-Workflow does in one sentence?

> "Claude-Workflow is a copy-and-go AI instruction template system that decomposes product requirements into hierarchical GitHub Issues for structured implementation."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Hierarchical Task Numbering**
   - What it is: A numbering scheme (1, 1.1, 1.2, 2, 2.1...) that encodes task relationships
   - Why it matters: Makes dependency chains explicit without separate tracking fields
   - Code example:
   ```markdown
   ## Task Breakdown
   1. Research and architecture task
   2. Backend implementation tasks
      - 2.1. Database schema and models
      - 2.2. API endpoints
      - 2.3. Business logic
   3. Frontend implementation tasks
      - 3.1. Components and UI
      - 3.2. State management
   4. Testing tasks
      - 4.1. Unit tests
      - 4.2. Integration tests
   ```

2. **Deep Dive: AI Instruction Templates**
   - What it is: Markdown files that guide Claude through multi-step workflows
   - Why it matters: Transforms simple commands into sophisticated, reliable processes
   - Example structure:
   ```markdown
   ## Step 1: Analyze Requirements
   **Use analysis tools to understand the project:**
   1. Use the Read tool to check for package.json
   2. Identify the technology stack
   3. Determine project type

   ## Step 2: Perform Extended Thinking
   Think deeply about this requirement: '$ARGUMENTS'.
   Consider technical approach, challenges, testing strategy...

   ## Step 3: Human Validation Check
   **STOP and request human review if:**
   - Architectural changes needed
   - Security implications discovered
   ```

3. **Deep Dive: Project Type Detection**
   - What it is: Automatic adaptation based on detected tech stack
   - Why it matters: Different project types need different planning approaches
   - Detection logic:
   ```
   package.json         --> Web Application (React, Next.js)
   requirements.txt     --> API Service (FastAPI, Django)
   go.mod               --> CLI Tool (Go)
   Multiple services    --> SaaS Platform
   ```

4. **Hands-on Exercise**
   - Task: Trace through `/project:plan:tasks` command
   - Steps:
     1. Read `.claude/commands/plan/tasks.md`
     2. Identify each Step section (1-10)
     3. Map which GitHub MCP calls happen at each step
     4. Note the hierarchical numbering rules in Step 4
   - Success criteria: You can explain the full task decomposition flow

**Checkpoint:** Can you create a hierarchical task breakdown for a simple feature?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Critical Thinking Pre-Planning**
   - When to use: Before any feature implementation
   - Implementation: The `/project:plan:brainstorm` command
   - Key questions to ask:
     - "Is this a real problem or just a minor inconvenience?"
     - "How often does this actually happen?"
     - "What's wrong with your current workaround?"
     - "Is this addressing a symptom or the root cause?"
   - Pitfalls: Skipping this phase leads to building solutions for non-problems

2. **Pattern: Human Validation Checkpoints**
   - When to use: Before risky changes
   - Implementation: Explicit STOP gates in AI instruction templates
   - Checkpoint triggers:
   ```markdown
   **STOP and request human review if:**
   - Architectural Changes: New patterns, frameworks, system design
   - Database Schema Changes: New tables, columns, relationships
   - API Breaking Changes: Affects existing integrations
   - Security Implications: Auth, authorization, data handling
   - Performance Critical: Affects scalability
   - External Dependencies: New third-party services
   ```
   - Pitfalls: Making checkpoints optional defeats the purpose

3. **Pattern: Extended Thinking Triggers**
   - When to use: Complex decisions requiring deep analysis
   - Implementation: Natural language prompts that invoke deeper reasoning
   - Example:
   ```markdown
   **For complex features, engage in extended thinking:**
   Think deeply about this technical feature: '$ARGUMENTS'. Consider
   the system architecture, integration patterns, data flow, error
   handling, testing strategy, and how this fits into the overall
   system design. What are the key technical decisions and potential
   challenges?
   ```
   - Pitfalls: Overusing for simple tasks wastes context

4. **Real-World Exercise**
   - Scenario: You need to add user authentication to a FastAPI project
   - Challenge: Design the complete workflow using Claude-Workflow patterns
   - Hints:
     1. Start with `/project:plan:brainstorm` to validate need
     2. Create PRD with `/project:plan:prd "user authentication"`
     3. Break down with `/project:plan:tasks "#123"`
     4. Notice the hierarchical numbering in output
     5. Track progress with `/project:current`

**Checkpoint:** Can you design a custom AI instruction template with validation checkpoints?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **AI Instruction Template** | Markdown file that guides Claude through multi-step workflows | `.claude/commands/plan/tasks.md` |
| **Hierarchical Numbering** | Task numbering that encodes relationships (1, 1.1, 1.2, 2) | "Task 2.1 Backend: API endpoints" |
| **Project Type Detection** | Automatic identification of web-app, API, CLI, SaaS from files | `package.json` --> Web Application |
| **Human Validation Checkpoint** | Explicit STOP gate before risky changes | "STOP if schema changes needed" |
| **Extended Thinking Trigger** | Prompt that invokes deeper analysis | "Think deeply about..." |
| **PRD** | Product Requirements Document as GitHub Issue | `[PRD] User Authentication System` |
| **Task Issue** | Implementation unit linked to parent PRD/Feature | `[Task 2.1] Backend: API endpoints` |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Skipping Task Decomposition

**What happens:** Attempting large features without breaking into tasks leads to incomplete, poorly planned implementations.

**Why it happens:** Seems faster to "just code it."

**How to avoid:** Always run `/project:plan:tasks` before implementation, even for seemingly simple features.

**How to fix:** If already deep in implementation, pause and create tasks for remaining work.

---

### Mistake 2: Flat Task Lists

**What happens:** Creating tasks without hierarchical numbering loses dependency information.

**Why it happens:** Numbered lists feel simpler than hierarchical structures.

**How to avoid:** Use the hierarchical pattern: 1, 1.1, 1.2, 2, 2.1... Major phases get integer numbers, sub-tasks get decimal numbers.

---

### Mistake 3: Missing Human Checkpoints

**What happens:** AI proceeds with risky changes (schema, security) without human review, causing costly mistakes.

**Why it happens:** Trust in AI automation without safety gates.

**How to avoid:** Include explicit STOP conditions in instruction templates for architectural changes, security implications, and breaking changes.

---

### Mistake 4: Documentation Instead of Instructions

**What happens:** Command templates read like documentation, not instructions, reducing AI effectiveness.

**Why it happens:** Natural tendency to document rather than instruct.

**How to avoid:** Write templates as imperative instructions TO the AI:
- Wrong: "This command creates PRDs..."
- Right: "You are creating a comprehensive PRD. Step 1: Analyze..."

---

## Practice Exercises

### Exercise 1: Trace a Command (Beginner)

**Objective:** Understand how AI instruction templates work

**Instructions:**
1. Open `.claude/commands/do/task.md`
2. List all 15 steps
3. Identify which steps involve GitHub MCP calls
4. Mark which steps have human validation checkpoints

**Solution:** Steps 4 (validation), 5 (status update), 13 (complete), 14 (PR), 15 (follow-through) involve GitHub API calls. Step 4 is the primary human checkpoint.

---

### Exercise 2: Design Task Hierarchy (Intermediate)

**Objective:** Practice hierarchical task decomposition

**Instructions:**
1. Feature: "Add dark mode to a React application"
2. Create hierarchical breakdown using 1, 1.1, 1.2 pattern
3. Include: research, frontend, state, testing, documentation
4. Mark estimated effort (S/M/L)

**Example Output:**
```
1. Research: CSS variables and theme switching (S)
2. Frontend implementation
   2.1. CSS variables setup (S)
   2.2. Theme toggle component (M)
   2.3. LocalStorage persistence (S)
3. State management
   3.1. Theme context provider (S)
   3.2. System preference detection (S)
4. Testing
   4.1. Unit tests for toggle (S)
   4.2. Integration tests (M)
5. Documentation (S)
```

---

### Exercise 3: Create Validation Checkpoints (Advanced)

**Objective:** Design effective human validation gates

**Challenge:** You're creating a command template for database migration. Design the validation checkpoint section.

**Expected Elements:**
- Schema change detection
- Data loss risk assessment
- Rollback plan verification
- Staging environment test requirement

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Hierarchical task decomposition | Any project management, Agile sprints, WBS |
| AI instruction design | Prompt engineering, agent frameworks |
| Human validation checkpoints | CI/CD pipelines, approval workflows |
| Critical thinking pre-planning | Product management, requirements engineering |
| GitHub Issues as state | External state management patterns |

---

## Study Resources

### Essential Reading

1. **Task Decomposition Article** - [Continue.dev blog on focused task decomposition](https://blog.continue.dev/task-decomposition/)
2. **Framework Source** - `.claude/commands/plan/tasks.md` in the repo

### Supplementary Materials

- [IBM on Agentic Chunking](https://www.ibm.com/think/topics/agentic-chunking) - Related concept for document processing
- [SparkCo: Agent Task Decomposition Techniques](https://sparkco.ai/blog/deep-dive-into-agent-task-decomposition-techniques)
- [Design Patterns for AI Agents 2025](https://valanor.co/design-patterns-for-ai-agents/)

### Community Resources

- Claude Code Discord
- GitHub Discussions on the framework repo

---

## Self-Assessment

### Quiz Yourself

1. What problem does Claude-Workflow solve?
2. How does hierarchical numbering (1, 1.1, 1.2) differ from flat numbered lists?
3. When should you trigger a human validation checkpoint?
4. What are the four project types the framework detects?
5. Why are AI instruction templates written imperatively, not as documentation?

### Practical Assessment

Build: A custom AI instruction template for code review

Success criteria:
- [ ] Uses numbered steps (minimum 5)
- [ ] Includes extended thinking trigger for complex reviews
- [ ] Has human validation checkpoint for security-sensitive code
- [ ] References appropriate tools (Read, GitHub, etc.)
- [ ] Follows existing template patterns

---

## What's Next?

After mastering Claude-Workflow, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas
2. **Related Frameworks:** Study SDD (Spec-Driven Development), Dev Loop patterns
3. **Advanced Topics:**
   - Multi-agent task decomposition
   - Context-aware chunking strategies
   - Session recovery patterns

---

*Learning guide created: 2026-02-02 | For: Claude-Workflow*
