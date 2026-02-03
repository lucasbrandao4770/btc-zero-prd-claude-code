# Beads - Learning Guide

> Educational resource for mastering Beads concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand how graph-based issue tracking enables dependency-aware agent execution
- [x] Learn how to design git-backed persistent memory systems
- [x] Be able to implement collision-free ID generation for multi-agent workflows
- [x] Apply the "landing the plane" protocol for reliable session handoffs
- [x] Master the three-layer architecture pattern (CLI -> Cache -> Sync)

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Git basics | Beads syncs via git | [Pro Git Book](https://git-scm.com/book) |
| CLI familiarity | Primary interface | Any terminal tutorial |
| SQLite basics | Understanding storage layer | [SQLite Tutorial](https://www.sqlitetutorial.net/) |
| AI agent concepts | Target use case | [Claude Code docs](https://docs.anthropic.com) |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Graph theory + git sync concepts |
| Implementation | Beginner | Simple CLI, well-documented |
| Time Investment | 2-4 Hours | Basic mastery; days for advanced patterns |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Beads is and why it matters

1. **Read the README**
   - Location: https://github.com/steveyegge/beads/blob/main/README.md
   - Time: 15 min
   - Key concepts to note: Three-layer model, hash IDs, `bd ready`

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, data flow, key mechanisms

3. **Try the Quick Start**
   - Instructions:
     ```bash
     # Install
     curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash

     # Initialize in any project
     cd your-project
     bd init --quiet

     # Create your first issue
     bd create "Learn Beads basics" -p 1 -t task

     # See what's ready
     bd ready
     ```
   - Expected outcome: One issue shown as ready to work

**Checkpoint:** Can you explain what Beads does in one sentence?

> "Beads is a git-backed graph issue tracker that gives AI agents persistent memory with dependency-aware task queues."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: The Three-Layer Model**
   - What it is: CLI -> SQLite (fast local cache) -> JSONL (git-tracked truth)
   - Why it matters: Speed + portability + distribution without central server
   - Code example:
   ```
   Write Path:
   bd create "Task" -> SQLite immediate -> 5s debounce -> JSONL export -> git commit

   Read Path:
   git pull -> JSONL newer? -> auto-import to SQLite -> bd ready (fast query)
   ```

2. **Deep Dive: Dependency Graph**
   - What it is: Four relationship types control execution
   - Why it matters: Enables `bd ready` to compute actionable work

   | Type | Semantics | Blocks? |
   |------|-----------|---------|
   | `blocks` | B can't start until A closes | Yes |
   | `parent-child` | Hierarchy (children blocked if parent blocked) | Yes |
   | `related` | Soft link for reference | No |
   | `discovered-from` | Found during work on parent | No |

   ```bash
   # Create dependency: implement needs design
   bd dep add bd-impl bd-design

   # Check what's blocked
   bd blocked

   # Check what's ready
   bd ready
   ```

3. **Deep Dive: Hash-Based IDs**
   - What it is: IDs derived from random UUIDs (`bd-a1b2`) instead of sequential
   - Why it matters: No collisions when multiple agents create issues
   - Progressive scaling: 4 chars (0-500 issues) -> 5 chars -> 6 chars

4. **Hands-on Exercise: Build a Feature Pipeline**
   - Task: Create an epic with sequential tasks
   - Steps:
     1. `bd create "User Auth Feature" -t epic -p 1`
     2. `bd create "Design auth flow" -t task --parent <epic-id>`
     3. `bd create "Implement login" -t task --parent <epic-id>`
     4. `bd create "Add tests" -t task --parent <epic-id>`
     5. `bd dep add <implement-id> <design-id>`
     6. `bd dep add <test-id> <implement-id>`
     7. `bd ready` (should show only design task)
     8. `bd close <design-id> --reason "Complete"`
     9. `bd ready` (should now show implement task)
   - Success criteria: Only unblocked tasks appear in `bd ready`

**Checkpoint:** Can you implement a basic dependency chain using Beads?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Landing the Plane**
   - When to use: End of every work session
   - Implementation:
     ```bash
     # 1. File remaining work
     bd create "TODO: Add error handling" -p 2

     # 2. Close finished work
     bd close bd-abc --reason "Completed"

     # 3. Sync to git (MANDATORY)
     git pull --rebase
     bd sync
     git push
     git status  # MUST show "up to date with origin"

     # 4. Choose next work
     bd ready --json
     ```
   - Pitfalls: Stopping before `git push` leaves work stranded locally

2. **Pattern: Molecules and Wisps**
   - When to use: Reusable workflow templates
   - Implementation:
     ```bash
     # Create a proto (template)
     bd create "Review Workflow" -t epic --label template
     bd create "Code review" -t task --parent <proto-id>
     bd create "Address feedback" -t task --parent <proto-id>
     bd create "Final approval" -t task --parent <proto-id>

     # Pour (instantiate) the template
     bd mol pour <proto-id> --var ticket=ABC-123

     # Or create ephemeral wisp (not synced)
     bd mol wisp <proto-id>

     # Squash when done (compress to digest)
     bd mol squash <wisp-id>
     ```
   - Pitfalls: Wisps are local-only; don't expect them in other clones

3. **Pattern: Multi-Agent Coordination**
   - When to use: Multiple AI agents working on same project
   - Implementation:
     ```bash
     # Agent claims work
     bd update bd-abc --status in_progress --assignee agent-1

     # Query by assignee
     bd ready --assignee agent-1 --json

     # Discovered work links back to source
     bd create "Found: Edge case bug" --deps discovered-from:bd-abc
     ```
   - Pitfalls: Last writer wins; coordinate via status claims

4. **Real-World Exercise: Autonomous Feature Development**
   - Scenario: You're building an AI agent that autonomously develops features
   - Challenge: Create a workflow where the agent:
     1. Reads requirements from a molecule template
     2. Executes tasks in dependency order
     3. Creates discovered issues for unexpected work
     4. Lands the plane with proper handoff
   - Hints:
     - Use `bd ready --json` in a loop
     - Check `bd blocked` to understand what's waiting
     - Always `bd sync` before session end

**Checkpoint:** Can you design and execute a multi-step workflow using molecules?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Issue** | Work item with ID, title, status, priority | `bd-a1b2: "Fix login bug"` |
| **Dependency** | Relationship between issues | `bd-impl` blocks `bd-test` |
| **Ready Work** | Issues with no open blockers | Output of `bd ready` |
| **Blocked Work** | Issues waiting on dependencies | Output of `bd blocked` |
| **Molecule** | Epic with children and execution intent | Feature workflow template |
| **Wisp** | Ephemeral local-only issue instance | Patrol cycle execution |
| **Proto** | Template molecule with `template` label | Reusable workflow pattern |
| **Compaction** | Summarizing old closed issues | `bd admin compact --days 90` |
| **JSONL** | JSON Lines format, one object per line | `.beads/issues.jsonl` |
| **Landing** | Session completion with mandatory push | `bd sync && git push` |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Forgetting to Sync

**What happens:** Changes stay in local SQLite, never reach git

**Why it happens:** Expecting auto-save without explicit sync

**How to avoid:** Always run `bd sync` before ending session

**How to fix:** Run `bd sync && git push`

---

### Mistake 2: Temporal Language for Dependencies

**What happens:** Dependencies created backwards

**Why it happens:** Saying "A comes before B" instead of "B needs A"

**How to avoid:** Use requirement language: "B depends on A"

**How to fix:** Check with `bd dep tree` and remove/re-add if wrong

---

### Mistake 3: Assuming Order = Sequence

**What happens:** Numbered tasks run in parallel instead of sequence

**Why it happens:** Expecting naming to control execution

**How to avoid:** Explicitly add dependencies between sequential tasks

**How to fix:** Add `bd dep add <later> <earlier>` for each sequence step

---

### Mistake 4: Using `bd edit` in Agents

**What happens:** Agent hangs waiting for interactive editor

**Why it happens:** `bd edit` opens $EDITOR (interactive)

**How to avoid:** Use `bd update <id> --description "..."` instead

---

## Practice Exercises

### Exercise 1: Basic Workflow (Beginner)

**Objective:** Create and complete a simple task chain

**Instructions:**
1. Initialize beads in a test directory
2. Create three tasks: Research, Implement, Test
3. Add dependencies: Test needs Implement, Implement needs Research
4. Verify only Research shows in `bd ready`
5. Close Research, verify Implement becomes ready
6. Close all tasks, run `bd sync`

**Solution:** See Quick Start section above

---

### Exercise 2: Multi-Branch Coordination (Intermediate)

**Objective:** Experience collision-free ID generation

**Instructions:**
1. Create branch A, run `bd create "Feature A" -t task`
2. Create branch B, run `bd create "Feature B" -t task`
3. Note the different hash-based IDs
4. Merge both branches
5. Run `bd list` - both issues should coexist

---

### Exercise 3: Autonomous Agent Simulation (Advanced)

**Objective:** Build a loop that processes ready work

**Challenge:** Write a bash script that:
```bash
while true; do
  READY=$(bd ready --json | jq -r '.[0].id // empty')
  if [ -z "$READY" ]; then
    echo "All work complete!"
    break
  fi
  echo "Working on $READY..."
  bd update $READY --status in_progress
  sleep 2  # Simulate work
  bd close $READY --reason "Completed by script"
done
bd sync
```

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| **Graph-based task modeling** | Any workflow engine (Airflow, Prefect, Temporal) |
| **Git-backed state management** | GitOps, Infrastructure as Code |
| **Three-layer architecture** | Cache patterns, CQRS |
| **Hash-based ID generation** | Distributed systems, CRDTs |
| **Session handoff protocols** | Any stateful agent system |

---

## Study Resources

### Essential Reading

1. [Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a) - Steve Yegge's original introduction explaining the "50 First Dates" problem
2. [ARCHITECTURE.md](https://github.com/steveyegge/beads/blob/main/docs/ARCHITECTURE.md) - Official architecture deep dive

### Supplementary Materials

- [Beads Best Practices](https://steve-yegge.medium.com/beads-best-practices-2db636b9760c) - Multi-agent coordination
- [CLI Reference](https://github.com/steveyegge/beads/blob/main/docs/CLI_REFERENCE.md) - Full command documentation
- [MOLECULES.md](https://github.com/steveyegge/beads/blob/main/docs/MOLECULES.md) - Workflow templates deep dive

### Community Resources

- [GitHub Discussions](https://github.com/steveyegge/beads/discussions) - Q&A and community help
- [nvim-beads](https://github.com/steveyegge/beads/tree/main/examples) - Editor integration examples
- [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) - Web UI alternative

---

## Self-Assessment

### Quiz Yourself

1. What problem does Beads solve for AI agents?
   > Agent amnesia - losing context between sessions

2. How does the three-layer architecture work?
   > CLI -> SQLite (fast cache) -> JSONL (git-tracked) -> Remote (distributed)

3. When would you use `blocks` vs `related` dependencies?
   > `blocks` for sequential execution; `related` for reference without blocking

4. What are the main trade-offs of Beads?
   > Pros: Offline, git-native, collision-free. Cons: Alpha status, no real-time sync, CLI-only core.

### Practical Assessment

Build: A feature development workflow with these criteria:

- [ ] Epic with 4+ child tasks
- [ ] Mix of parallel and sequential dependencies
- [ ] At least one discovered issue created during execution
- [ ] Proper landing-the-plane completion
- [ ] All changes synced to git

---

## What's Next?

After mastering Beads, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas - especially dependency tracking and ready-work patterns

2. **Related Frameworks:** Study these for complementary patterns:
   - **Temporal** - Workflow orchestration with state persistence
   - **Langchain Memory** - Different approach to agent memory
   - **LCEL** - Chain-based execution patterns

3. **Advanced Topics:**
   - Multi-repo agents (federated beads)
   - Custom SQLite extensions
   - MCP server integration
   - Gas Town multi-agent orchestration

---

*Learning guide created: 2026-02-03 | For: Beads*
