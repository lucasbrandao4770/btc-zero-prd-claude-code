# Spec-Kit - Learning Guide

> Educational resource for mastering Spec-Driven Development concepts and applying them to AI-assisted workflows

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand the Spec-Driven Development (SDD) paradigm and how it inverts traditional code-first workflows
- [x] Learn how to write technology-agnostic specifications with prioritized user stories
- [x] Be able to structure clarification workflows with limits and options tables
- [x] Apply task breakdown patterns with parallel markers and user story grouping
- [x] Understand constitutional governance for enforcing immutable development principles

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Git basics | Spec-Kit uses feature branches for each specification | [Git Handbook](https://guides.github.com/introduction/git-handbook/) |
| AI coding assistant | Framework requires Claude Code, Copilot, or similar | Install your preferred AI assistant |
| Markdown familiarity | All specs are written in Markdown | [Markdown Guide](https://www.markdownguide.org/) |
| Given/When/Then format | Acceptance scenarios use BDD format | [BDD Introduction](https://cucumber.io/docs/bdd/) |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Requires shifting from code-first to spec-first mindset |
| Implementation | Beginner | CLI commands are simple; templates guide structure |
| Time Investment | 2-4 hours | Initial learning; ongoing practice refines skills |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Spec-Driven Development is and why it matters

1. **Read the README**
   - Location: https://github.com/github/spec-kit/blob/main/README.md
   - Time: 15 min
   - Key concepts to note:
     - "Specifications become executable"
     - "Intent-driven development"
     - The 6-step process overview

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Core Concepts, Component Diagram, Key Files/Folders

3. **Try the Quick Start**
   - Instructions:
     ```bash
     # Install Specify CLI
     uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

     # Initialize a test project
     specify init my-test-project --ai claude

     # Navigate to project
     cd my-test-project

     # Launch Claude Code
     claude

     # Try your first specification
     /speckit.specify Build a simple todo list application
     ```
   - Expected outcome: A `spec.md` file with user stories and requirements

**Checkpoint:** Can you explain what Spec-Driven Development does in one sentence?

> **Answer:** SDD transforms natural language specifications into executable implementations through structured AI-assisted workflows, making specifications the source of truth rather than scaffolding.

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Specification Structure**
   - What it is: The spec.md file captures WHAT and WHY without HOW
   - Why it matters: Technology-agnostic specs enable parallel implementations and tech stack pivots
   - Code example:
   ```markdown
   # Feature Specification: Photo Album Organizer

   ## User Scenarios & Testing *(mandatory)*

   ### User Story 1 - Create Album (Priority: P1)

   User can create a new photo album with a name and optional description.

   **Why this priority**: Core functionality; app is useless without albums.

   **Independent Test**: Can test by creating an album without photos.

   **Acceptance Scenarios**:
   1. **Given** no albums exist, **When** user creates "Vacation 2025",
      **Then** album appears in list with that name
   2. **Given** an album exists, **When** user creates duplicate name,
      **Then** system shows error message

   ## Requirements *(mandatory)*

   ### Functional Requirements
   - **FR-001**: System MUST allow users to create albums
   - **FR-002**: System MUST validate album names are unique
   - **FR-003**: System MUST persist albums across sessions

   ## Success Criteria *(mandatory)*
   - **SC-001**: Users can create an album in under 30 seconds
   - **SC-002**: 95% of users successfully create their first album
   ```

2. **Deep Dive: Task Breakdown**
   - What it is: Ordered, parallelizable task lists grouped by user story
   - Why it matters: Explicit tasks improve traceability and enable incremental delivery
   - Key patterns:
     - `[P]` marker for parallelizable tasks
     - `[US1]`, `[US2]` tags for user story grouping
     - Phase organization: Setup > Foundational > User Stories > Polish

   ```markdown
   ## Phase 3: User Story 1 - Create Album (Priority: P1)

   ### Implementation for User Story 1
   - [ ] T012 [P] [US1] Create Album model in src/models/album.py
   - [ ] T013 [P] [US1] Create AlbumService in src/services/album_service.py
   - [ ] T014 [US1] Implement create_album endpoint (depends on T012, T013)
   - [ ] T015 [US1] Add validation for duplicate names

   **Checkpoint**: At this point, User Story 1 should be fully functional
   ```

3. **Deep Dive: Constitutional Governance**
   - What it is: Immutable principles that govern all development decisions
   - Why it matters: Prevents drift, ensures consistency, enforces quality
   - Example constitution articles:
   ```markdown
   ### III. Test-First (NON-NEGOTIABLE)

   TDD mandatory: Tests written → User approved → Tests fail → Then implement
   Red-Green-Refactor cycle strictly enforced

   ### VII. Simplicity

   - Maximum 3 projects for initial implementation
   - Additional projects require documented justification
   - No "might need" features allowed
   ```

4. **Hands-on Exercise: Write Your First Spec**
   - Task: Create a specification for a bookmark manager
   - Steps:
     1. Launch Claude Code in your Spec-Kit project
     2. Run `/speckit.specify Build a browser bookmark manager that organizes bookmarks into folders`
     3. Review the generated spec.md
     4. Run `/speckit.clarify` to resolve any `[NEEDS CLARIFICATION]` markers
     5. Verify all user stories have P1/P2/P3 priorities and acceptance scenarios
   - Success criteria: spec.md has no `[NEEDS CLARIFICATION]` markers and all user stories are independently testable

**Checkpoint:** Can you write a specification with prioritized user stories and Given/When/Then scenarios?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Structured Clarification**
   - When to use: When specifications have ambiguities that impact scope or user experience
   - Implementation:
     - Maximum 3 `[NEEDS CLARIFICATION]` markers allowed
     - Present clarifications as options tables with implications
     - Prioritize: scope > security > UX > technical details
   - Pitfalls:
     - Don't ask about reasonable defaults (auth method, data retention)
     - Don't dump 10+ questions at once
     - Don't ask implementation questions in specification phase

   ```markdown
   ## Question 1: Authentication Method

   **Context**: "Users must authenticate" in FR-003

   **What we need to know**: Which authentication method should be used?

   **Suggested Answers**:

   | Option | Answer | Implications |
   |--------|--------|--------------|
   | A | Email/password | Simple; requires password recovery flow |
   | B | OAuth (Google/GitHub) | No passwords to manage; requires API setup |
   | C | Passwordless (magic link) | Modern UX; requires email sending capability |
   | Custom | Provide your own | Explain how to provide custom input |

   **Your choice**: _[Wait for user response]_
   ```

2. **Pattern: User Story Independence**
   - When to use: Every specification should apply this pattern
   - Implementation:
     - Each user story must be independently testable
     - Each story should deliver standalone value
     - Stories can be developed and deployed in isolation
   - Pitfalls:
     - Don't create stories that depend on other stories to function
     - Don't mix multiple concerns in one story
     - Don't defer critical functionality to later stories

3. **Pattern: Phase Gate Validation**
   - When to use: Before transitioning between phases (Specify > Plan > Tasks > Implement)
   - Implementation:
     - Run checklists before proceeding
     - All checklist items must pass or be explicitly waived
     - Document any exceptions in the spec
   - Checklist example:
   ```markdown
   ## Requirement Completeness
   - [ ] No [NEEDS CLARIFICATION] markers remain
   - [ ] Requirements are testable and unambiguous
   - [ ] Success criteria are measurable
   - [ ] All acceptance scenarios are defined
   ```

4. **Real-World Exercise: Multi-Story Feature**
   - Scenario: Build a specification for a team calendar application
   - Challenge:
     1. Define 3+ user stories with P1/P2/P3 priorities
     2. Ensure each story is independently testable
     3. Use structured clarification for any ambiguities (max 3)
     4. Generate a technical plan with `/speckit.plan`
     5. Break down into tasks with `/speckit.tasks`
   - Hints:
     - P1 might be "View Calendar" (essential)
     - P2 might be "Create Event" (important)
     - P3 might be "Share Calendar" (nice-to-have)

**Checkpoint:** Can you create a complete specification-to-tasks flow for a multi-story feature?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **SDD** | Spec-Driven Development - methodology where specs generate code | `/speckit.specify` creates spec.md |
| **Constitution** | Immutable principles governing development | "Test-First is NON-NEGOTIABLE" |
| **User Story** | Independent slice of functionality with acceptance scenarios | "As a user, I can create albums" |
| **P1/P2/P3** | Priority levels for user stories (P1 = critical) | P1 = MVP, P3 = nice-to-have |
| **Task Breakdown** | Ordered list of implementation tasks | tasks.md with T001, T002... |
| **Parallel Marker** | `[P]` indicates tasks that can run concurrently | `- [ ] T005 [P] Create model` |
| **Clarification Limit** | Maximum 3 `[NEEDS CLARIFICATION]` markers per spec | Prevents question overload |
| **Phase Gate** | Checklist validation before phase transition | All specs complete before plan |
| **Independence** | Each user story can be tested/deployed alone | US1 doesn't need US2 to work |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Mixing WHAT and HOW in Specifications

**What happens:** Spec includes "Use React with Redux" instead of "Users need real-time updates"

**Why it happens:** Developers naturally think in implementation terms

**How to avoid:** Review spec for any technology mentions; move them to plan.md

**How to fix:** Replace "Implement using PostgreSQL" with "System must persist data reliably"

---

### Mistake 2: Question Dumping in Clarification

**What happens:** 10+ `[NEEDS CLARIFICATION]` markers that overwhelm the user

**Why it happens:** LLM tries to be thorough; no constraint on question count

**How to avoid:** Enforce max 3 clarifications; make informed guesses for the rest

**How to fix:** Prioritize by impact (scope > security > UX) and keep only top 3

---

### Mistake 3: Dependent User Stories

**What happens:** US2 can't be tested without US1 being complete

**Why it happens:** Natural to think of features as building blocks

**How to avoid:** Ask "Can this story be demonstrated alone?" for each story

**How to fix:** Split dependent stories into smaller independent units

---

### Mistake 4: Skipping Phase Gates

**What happens:** Implement phase starts with incomplete specifications

**Why it happens:** Eagerness to see results; pressure to deliver

**How to avoid:** Run checklist validation before each phase transition

**How to fix:** Add `/speckit.checklist` before `/speckit.implement`

---

## Practice Exercises

### Exercise 1: Spec Review (Beginner)

**Objective:** Identify issues in an existing specification

**Instructions:**
1. Read this spec excerpt:
   ```markdown
   ## User Story 1 - User Management (Priority: P1)

   Build a user management system using Node.js and PostgreSQL
   with JWT authentication.

   **Acceptance Scenarios**:
   1. Given a user exists, When they login, Then they are authenticated
   ```
2. Identify 3 problems with this spec
3. Rewrite it following SDD principles

**Solution:**
1. Problems: (a) includes tech stack (Node.js, PostgreSQL, JWT), (b) vague acceptance scenario, (c) missing "Independent Test" section
2. Corrected version:
   ```markdown
   ## User Story 1 - User Login (Priority: P1)

   Users can authenticate with their credentials to access the system.

   **Independent Test**: Can test login flow without other features.

   **Acceptance Scenarios**:
   1. **Given** a registered user with email "test@example.com",
      **When** they enter correct password,
      **Then** they are redirected to dashboard within 2 seconds
   ```

---

### Exercise 2: Prioritization (Intermediate)

**Objective:** Practice user story prioritization

**Instructions:**
1. Given these features for a note-taking app:
   - Create notes
   - Share notes with others
   - Search notes
   - Export notes to PDF
   - Sync across devices
2. Assign P1/P2/P3 priorities with justifications
3. Write "Independent Test" for each

**Solution:**
- P1: Create notes (core functionality, app is useless without it)
- P1: Search notes (essential for finding content as notes grow)
- P2: Sync across devices (important for multi-device users, but can use single device)
- P3: Share notes (nice-to-have, workaround is copy-paste)
- P3: Export to PDF (nice-to-have, can screenshot)

---

### Exercise 3: Task Breakdown (Advanced)

**Objective:** Create a complete task breakdown for a user story

**Challenge:**
Given this user story:
```markdown
### User Story 2 - Image Upload (Priority: P1)

Users can upload images to their albums.

**Acceptance Scenarios**:
1. Given an album exists, When user uploads a JPG under 10MB,
   Then image appears in album
2. Given user uploads file over 10MB, Then error message appears
```

Create a tasks.md excerpt with:
- At least 5 tasks
- Proper [P] markers for parallel tasks
- [US2] tags
- Dependencies noted
- A checkpoint

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Writing Given/When/Then scenarios | BDD testing, Cucumber, pytest-bdd |
| Priority ordering (P1/P2/P3) | Product management, sprint planning |
| Task breakdown with dependencies | Project management, Gantt charts |
| Technology-agnostic requirements | PRD writing, stakeholder communication |
| Structured clarification | User interviews, requirements gathering |
| Constitutional governance | Architecture decision records (ADRs) |

---

## Study Resources

### Essential Reading

1. **Spec-Driven Methodology** - https://github.com/github/spec-kit/blob/main/spec-driven.md
   - The philosophical foundation of SDD; explains "why" not just "how"

2. **Thoughtworks: Spec-driven development** - https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices
   - Industry perspective on SDD as an emerging practice

### Supplementary Materials

- **Video Overview**: https://www.youtube.com/watch?v=a9eR1xsfvHg (30 min)
- **InfoQ Article**: https://www.infoq.com/articles/spec-driven-development/
- **Martin Fowler on SDD Tools**: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- **Microsoft Developer Blog**: https://developer.microsoft.com/blog/spec-driven-development-spec-kit

### Community Resources

- **GitHub Discussions**: https://github.com/github/spec-kit/discussions
- **Issues for Questions**: https://github.com/github/spec-kit/issues

---

## Self-Assessment

### Quiz Yourself

1. What problem does Spec-Driven Development solve?
   > Eliminates the gap between specifications and implementation by making specs executable

2. How does user story independence work?
   > Each story can be developed, tested, and deployed without depending on other stories

3. When would you use `/speckit.clarify` vs `/speckit.specify`?
   > `/speckit.specify` creates initial spec; `/speckit.clarify` resolves ambiguities afterward

4. What are the main trade-offs of Spec-Driven Development?
   > Pros: Traceable, regenerable, technology-independent; Cons: Requires upfront thinking, Git-centric, file-based state only

### Practical Assessment

Build: A complete specification-to-implementation flow for a "Recipe Manager" application

Success criteria:
- [ ] spec.md with 3+ user stories (P1, P2, P3 priorities)
- [ ] All user stories have "Independent Test" sections
- [ ] No `[NEEDS CLARIFICATION]` markers remain (use structured clarification)
- [ ] plan.md with technical stack and architecture
- [ ] tasks.md with ordered tasks and [P] markers
- [ ] At least one phase gate checklist passed

---

## What's Next?

After mastering Spec-Kit, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas
   - Add /tasks command
   - Adopt clarification limits
   - Use priority ordering

2. **Related Frameworks:** Study these complementary tools
   - **Amazon Kiro** - AWS's SDD implementation
   - **Tessl** - Alternative specification-first tool
   - **Jarvis SDD** - This project's AgentSpec 4.2 workflow

3. **Advanced Topics:** Deeper areas to explore
   - Constitutional amendments and governance
   - Multi-feature coordination
   - Brownfield modernization patterns
   - Parallel implementation exploration

---

*Learning guide created: 2026-02-02 | For: Spec-Kit*
