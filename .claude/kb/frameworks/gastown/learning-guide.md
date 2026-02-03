# Gas Town - Learning Guide

> Educational resource for mastering Gas Town concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand the Propulsion Principle and why immediate execution matters
- [x] Learn how Convoys track work across multiple agents and projects
- [x] Be able to design multi-agent workflows with proper state persistence
- [x] Apply external state patterns to your own orchestration systems
- [x] Recognize when massive parallelism (20-30 agents) is appropriate

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Multi-agent experience | Gas Town is "level 6+" | Practice with Task tool first |
| Git proficiency | Hooks and Beads are git-backed | Any git fundamentals guide |
| CLI comfort | Gas Town is CLI-first | Terminal practice |
| Claude Code familiarity | Primary runtime | claude.ai/code |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Novel ideas but well-documented |
| Implementation | Advanced | Requires infrastructure setup |
| Time Investment | Days | 1-2 days to understand, longer to deploy |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Gas Town is and why it matters

1. **Read the README**
   - Location: `gastown/README.md`
   - Time: 30 min
   - Key concepts to note: Mayor, Rigs, Polecats, Hooks, Convoys

2. **Study the Glossary**
   - Location: `gastown/docs/glossary.md`
   - Time: 20 min
   - Focus on: MEOW, GUPP (Propulsion), NDI, role taxonomy

3. **Review the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, workflow, three-layer architecture

**Checkpoint:** Can you explain what Gas Town does in one sentence?

> "Gas Town coordinates 20-30 Claude Code agents with persistent git-backed state, enabling autonomous multi-agent workflows at scale."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: The Propulsion Principle (GUPP)**

   What it is: The rule that when work appears on your Hook, you MUST execute immediately - no waiting, no confirmation.

   Why it matters: Eliminates coordination overhead. Gas Town is a "steam engine" where agents are "pistons" - the system only works when pistons fire immediately.

   Key quote:
   > "There is no supervisor polling asking 'did you start yet?' The hook IS your assignment - it was placed there deliberately."

   Code pattern:
   ```bash
   # Startup behavior
   1. Check hook (gt hook)
   2. Work hooked -> EXECUTE immediately
   3. Hook empty -> Check mail
   4. Nothing anywhere -> ERROR: escalate
   ```

2. **Deep Dive: Convoy Model**

   What it is: A persistent tracking unit that monitors related issues across multiple rigs and agents.

   Why it matters: Provides unified visibility into batched work. The "swarm" is ephemeral (just workers on issues), but the Convoy is persistent and trackable.

   Visual:
   ```
                    Convoy (hq-cv-abc)
                          |
           +--------------+--------------+
           |              |              |
        gt-xyz         gt-def         bd-abc
        (issue)        (issue)        (issue)
           |              |              |
        polecat-1      polecat-2      polecat-3
                          |
                     "the swarm"
                     (ephemeral)
   ```

3. **Deep Dive: Three-Layer Polecat Architecture**

   What it is: Polecats have three distinct lifecycle layers:

   | Layer | Component | Lifecycle |
   |-------|-----------|-----------|
   | Session | Claude instance | Ephemeral - cycles on handoff/compact |
   | Sandbox | Git worktree | Persistent until nuke |
   | Slot | Name (Toast, Shadow) | Persistent until nuke |

   Why it matters: Session cycling is NORMAL. The polecat continues working - only the Claude context refreshes. Work is preserved in the Sandbox.

4. **Hands-on Exercise: Trace a Workflow**

   Task: Trace through Gas Town's workflow manually

   Steps:
   1. Human tells Mayor: "Build feature X"
   2. Mayor creates Convoy tracking issues gt-a, gt-b
   3. Mayor slings gt-a to polecat Toast
   4. Toast finds work on Hook, executes immediately (GUPP)
   5. Toast completes step, calls `bd close step --continue`
   6. Toast finishes molecule, calls `gt done`
   7. Refinery merges Toast's branch
   8. Convoy detects all issues closed, notifies subscribers

   Success criteria: You can explain each step and why it matters

**Checkpoint:** Can you implement the Propulsion loop from memory?

```bash
1. gt hook                    # What's hooked?
2. bd mol current             # Where am I?
3. Execute step
4. bd close <step> --continue # Close and advance
5. GOTO 2
6. gt done                    # Done
```

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Molecule Navigation**

   When to use: Multi-step workflows with audit requirements

   Implementation:
   ```bash
   # Find your place
   bd mol current              # Where am I?

   # Seamless transition
   bd close gt-abc.3 --continue  # Close AND advance (1 command)

   # vs. the old way (3 commands)
   bd close gt-abc.3
   bd ready --parent=gt-abc
   bd update gt-abc.4 --status=in_progress
   ```

   Pitfalls:
   - CRITICAL: Close steps in real-time, not batch at end
   - Batch-closing corrupts timeline and CV accuracy

2. **Pattern: Self-Cleaning Workers**

   When to use: Any ephemeral worker agent

   Implementation: Polecats handle their own cleanup:
   ```bash
   gt done
   # -> Push branch to origin
   # -> Submit to merge queue (MR bead)
   # -> Request self-nuke
   # -> Exit immediately
   ```

   Key insight: "Sandbox dies with session" - no idle state ever

3. **Pattern: Redundant Observation**

   When to use: Critical workflows needing reliability

   Implementation: Multiple agents can check convoy status
   ```go
   // From convoy/observer.go
   // CheckConvoysForIssue finds any convoys tracking the given issue
   // This enables redundant convoy observation from multiple agents
   // (Witness, Refinery, Daemon).
   //
   // The check is idempotent - running it multiple times is safe.
   ```

4. **Real-World Exercise: Design a Gas Town Workflow**

   Scenario: You need to implement a 5-file feature across 2 repos

   Challenge:
   - Design the Convoy structure
   - Decide how many Polecats to spawn
   - Define the Molecule steps
   - Plan error handling (what if Polecat crashes?)
   - Map the merge strategy (sequential vs. parallel)

   Hints:
   - Create one Convoy tracking all issues
   - Spawn Polecats for parallel work
   - Use Molecules for sequential dependencies
   - Witness will respawn crashed Polecats
   - Refinery handles merge conflicts

**Checkpoint:** Can you design a multi-agent workflow with proper state persistence?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **GUPP** | Gas Town Universal Propulsion Principle: "If there is work on your Hook, YOU MUST RUN IT." | Polecat starts immediately when slung |
| **MEOW** | Molecular Expression of Work: Breaking goals into trackable atomic units | Feature -> Tasks -> Beads |
| **Convoy** | Persistent tracking unit for batched work | `hq-cv-abc` tracking 3 issues |
| **Swarm** | Ephemeral collection of workers on a convoy | Polecats Toast, Shadow, Copper |
| **Hook** | Agent's pinned work assignment | Issue gt-xyz on Toast's hook |
| **Molecule** | Durable chained workflow with tracked steps | 5-step feature implementation |
| **Wisp** | Ephemeral molecule for patrol cycles | Deacon patrol (not persisted) |
| **Bead** | Git-backed atomic work unit | Issue, task, epic in JSONL |
| **Seance** | Querying previous sessions for context | `gt seance` to talk to past self |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Waiting for Confirmation

**What happens:** Agent checks hook, finds work, then asks "should I start?"

**Why it happens:** Human habits - we're trained to confirm before acting

**How to avoid:** Internalize GUPP. The Hook IS your assignment. Execute immediately.

**How to fix:** Remove confirmation loops from your agents

---

### Mistake 2: Batch-Closing Molecule Steps

**What happens:** Agent completes all steps, then closes them all at once

**Why it happens:** Seems efficient to batch operations

**How to avoid:** Close steps in real-time as they complete

**Why it matters:** Molecules ARE the ledger - each step closure is timestamped. Batch-closing corrupts the timeline.

---

### Mistake 3: Thinking "Idle Polecats" Exist

**What happens:** Looking for unused Polecats to assign work to

**Why it happens:** Mental model from traditional job pools

**How to avoid:** Understand there is NO idle state. Polecats are spawned for work, execute, then self-destruct.

**Correct model:**
- Work assigned -> Polecat spawned
- Work done -> `gt done` -> Polecat nuked
- No step 3 where they wait around

---

### Mistake 4: Confusing Session with Sandbox

**What happens:** Thinking session restart = lost work

**Why it happens:** Not understanding three-layer architecture

**How to avoid:** Remember:
- Session (Claude) = ephemeral, cycles frequently
- Sandbox (worktree) = persistent, survives session cycles
- Work is NOT lost because sandbox persists

---

## Practice Exercises

### Exercise 1: Propulsion Audit (Beginner)

**Objective:** Identify propulsion violations in existing workflows

**Instructions:**
1. Review your current agent workflows
2. Find all places where agents wait for confirmation
3. List which could be converted to propulsion-style execution

**Solution:** Any "do you want me to continue?" or "ready to proceed?" should be eliminated in autonomous mode

---

### Exercise 2: Design a Convoy (Intermediate)

**Objective:** Practice work decomposition and tracking

**Instructions:**
1. Pick a real feature you need to build
2. Break it into 3-5 atomic issues
3. Design the Convoy structure
4. Identify which issues can parallelize vs. must sequence
5. Sketch the Molecule if sequential

---

### Exercise 3: Implement Self-Cleaning (Advanced)

**Objective:** Add self-cleanup to your agent system

**Challenge:** Design a completion protocol where agents:
- Signal completion explicitly
- Clean up their own resources
- Never sit idle waiting for external cleanup

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| External state patterns | Any distributed system |
| Propulsion principle | Async job queues, event systems |
| Work attribution | Enterprise audit systems |
| Convoy tracking | Project management, CI/CD pipelines |
| Self-cleaning workers | Kubernetes, serverless |
| Molecule workflows | BPM, workflow engines |

---

## Study Resources

### Essential Reading

1. **Gas Town README** - Start here for the overview
2. **docs/glossary.md** - Master the vocabulary
3. **docs/concepts/propulsion-principle.md** - Core philosophy
4. **docs/concepts/convoy.md** - Work tracking model
5. **docs/concepts/polecat-lifecycle.md** - Three-layer architecture

### Supplementary Materials

- Steve Yegge's Medium articles on agentic coding
- Hacker News discussion thread
- Justin Abrahms: "Wrapping my head around Gas Town"
- paddo.dev: "GasTown and the Two Kinds of Multi-Agent"

### Community Resources

- GitHub Issues for questions
- Pull requests for contributing
- Watch repo for updates (very active development)

---

## Self-Assessment

### Quiz Yourself

1. What problem does Gas Town solve that single-agent systems don't?
2. What is GUPP and why is it non-negotiable?
3. How do Convoys differ from Swarms?
4. What are the three layers of a Polecat and which survives session restart?
5. When would you use a Molecule vs. a Wisp?

### Practical Assessment

Build: A mock multi-agent workflow design (no actual Gas Town needed)

Success criteria:
- [ ] Proper work decomposition into trackable units
- [ ] Clear propulsion triggers (no confirmation loops)
- [ ] Convoy tracking for visibility
- [ ] Self-cleaning worker pattern
- [ ] Error handling for worker failures

---

## What's Next?

After mastering Gas Town concepts, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for adaptation ideas
2. **Related Frameworks:** Study Claude Workflow, Spec Kit, SuperMemory
3. **Advanced Topics:**
   - Federation across multiple Towns
   - Model A/B testing via different Polecats
   - Enterprise audit and compliance patterns
   - Building your own Beads formulas

---

*Learning guide created: 2026-02-03 | For: Gas Town Multi-Agent Orchestration*
