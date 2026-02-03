# Gas Town - Framework Analysis

> Deep dive into Gas Town: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | https://github.com/steveyegge/gastown |
| **Author** | Steve Yegge |
| **Category** | Multi-Agent Orchestration |
| **Language** | Go |
| **Last Updated** | 2026-02 (Active Development) |

### One-Line Summary

Gas Town is a multi-agent workspace manager that coordinates 20-30 Claude Code instances with persistent work tracking via git-backed state, enabling reliable autonomous workflows at scale.

---

## Problem Statement

### What Problem Does It Solve?

Gas Town addresses the chaos that emerges when running multiple AI coding agents simultaneously:

| Challenge | Gas Town Solution |
|-----------|-------------------|
| Agents lose context on restart | Work persists in git-backed hooks |
| Manual agent coordination | Built-in mailboxes, identities, and handoffs |
| 4-10 agents become chaotic | Scale comfortably to 20-30 agents |
| Work state lost in agent memory | Work state stored in Beads ledger |
| Anonymous AI work ("The AI broke it") | Universal attribution with agent identities |
| No visibility into agent performance | Work history (CV) tracks completions, quality |

### Who Is It For?

- **Experienced agentic developers**: Users at "level 6+" who already use multi-agent workflows outside the IDE
- **Enterprise teams**: Organizations needing compliance, audit trails, and accountability for AI-generated code
- **High-throughput projects**: Teams with enough work to keep 20-30 parallel agents busy
- **Claude Code power users**: Those comfortable with the CLI and willing to invest in orchestration infrastructure

### Why Does This Matter?

Gas Town introduces a paradigm shift: **You become a Product Manager, and Gas Town is your "Idea Compiler."** Instead of coding yourself or directing a single agent, you design features, file implementation plans, and distribute work across a fleet of autonomous workers. The system handles coordination, state persistence, quality gates, and merge management.

---

## Architecture

### Core Concepts

1. **Mayor** - The chief-of-staff AI coordinator with full workspace visibility. Your primary interface - just tell the Mayor what you want to accomplish.

2. **Town** - The workspace directory (e.g., `~/gt/`) containing all projects, agents, and configuration.

3. **Rigs** - Project containers wrapping git repositories with their associated agents.

4. **Polecats** - Ephemeral worker agents that spawn, complete a task, and self-destruct. Work in isolated git worktrees.

5. **Hooks** - Git worktree-based persistent storage. When work appears on your Hook, you must run it (the Propulsion Principle).

6. **Convoys** - Work tracking units that bundle related beads/issues across multiple agents and rigs.

7. **Beads** - Git-backed atomic work units (issues, tasks, epics) stored in JSONL format.

8. **Molecules** - Durable chained workflows where each step is tracked as a Bead, surviving agent restarts.

### Component Diagram

```
                          TOWN (~/gt/)
                              |
         +--------------------+--------------------+
         |                    |                    |
      MAYOR              DEACON               RIG(s)
   (Coordinator)        (Watchdog)         (Projects)
                              |                    |
                           DOGS              +-----+-----+
                        (Helpers)            |     |     |
                                          WITNESS REFINERY POLECATS
                                          (Monitor)(Merge) (Workers)
                                                           |
                                                     +-----+-----+
                                                     |           |
                                                   HOOK      SANDBOX
                                                 (State)   (Worktree)

WORK FLOW:
  Convoy -----> Bead(s) -----> Sling -----> Polecat
  (Track)      (Issue)        (Assign)     (Execute)
                                              |
                                          [Work on Hook]
                                              |
                                          gt done
                                              |
                                         Refinery
                                         (Merge)
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `cmd/gt/` | Main CLI entry point |
| `internal/mayor/` | Mayor lifecycle management |
| `internal/convoy/` | Convoy tracking and observation |
| `internal/swarm/` | Swarm state management (workers on a convoy) |
| `internal/polecat/` | Polecat lifecycle, hooks, handoffs |
| `internal/beads/` | Beads integration for work tracking |
| `internal/deacon/` | Background supervisor daemon |
| `internal/refinery/` | Merge queue processor |
| `docs/concepts/` | Core concept documentation |
| `.beads/` | Per-town/rig beads storage |

---

## Capabilities

### What It Can Do

- [x] Coordinate 20-30 parallel Claude Code agents
- [x] Persist work state across agent restarts (git-backed hooks)
- [x] Track work progress via convoys with cross-rig visibility
- [x] Attribute every action to specific agents (accountability)
- [x] Build agent CVs with work history and skill tracking
- [x] Route work based on agent capabilities
- [x] Manage merge queues with conflict resolution
- [x] Enable A/B testing of different LLM models
- [x] Support multiple runtimes (Claude, Codex, Cursor, Gemini)
- [x] Provide real-time activity feeds
- [x] Execute workflow templates via Molecules/Formulas
- [x] Federation across multiple workspaces/organizations

### What It Cannot Do

- **Not a low-cost solution**: Burn rate can hit $100/hour with many agents
- **Not for beginners**: Requires significant agentic experience
- **Not self-designing**: You must provide enough design/planning to feed the engine
- **Not Windows-native**: Primary support for macOS/Linux with tmux
- **Not IDE-integrated**: CLI-first, outside-the-IDE orchestration

---

## How It Works

### Workflow

```
You describe goal to Mayor
         |
         v
Mayor breaks down into tasks (Beads)
         |
         v
Mayor creates Convoy to track work
         |
         v
Beads slung to Polecats via gt sling
         |
         v
Polecats execute (GUPP: Hook = immediate execution)
         |
         v
Progress tracked via gt convoy list
         |
         v
Polecats call gt done on completion
         |
         v
Refinery merges work to main branch
         |
         v
Convoy lands, subscribers notified
```

### Key Mechanisms

**1. The Propulsion Principle (GUPP)**

> "If there is work on your Hook, YOU MUST RUN IT."

Agents don't wait for confirmation. The Hook IS the assignment. This creates a "steam engine" where agents are pistons that fire immediately when work appears.

**2. Self-Cleaning Polecats**

Polecats are responsible for their own cleanup. When work completes:
- Signal via `gt done`
- Push branch to origin
- Submit to merge queue
- Exit immediately (no idle state)

**3. Three-Layer Polecat Architecture**

| Layer | Component | Lifecycle |
|-------|-----------|-----------|
| Session | Claude instance | Ephemeral (cycles on handoff/compact) |
| Sandbox | Git worktree | Persistent until nuke |
| Slot | Name from pool | Persistent until nuke |

**4. Stateless Managers**

```go
// Manager is stateless - all swarm state is discovered from beads.
type Manager struct {
    rig       *rig.Rig
    beadsDir  string // Path for beads operations (git-synced)
    gitDir    string // Path for git operations (rig root)
}

// LoadSwarm loads swarm state from beads by querying the epic.
// This is the canonical way to get swarm state - no in-memory caching.
func (m *Manager) LoadSwarm(epicID string) (*Swarm, error) {
    // Query beads for the epic
    cmd := exec.Command("bd", "show", epicID, "--json")
    // ...
}
```

### Code Examples

**Creating and tracking a convoy:**

```bash
# 1. Start the Mayor
gt mayor attach

# 2. Create convoy with issues
gt convoy create "Feature X" gt-abc12 gt-def34 --notify --human

# 3. Assign work to agents
gt sling gt-abc12 myproject

# 4. Track progress
gt convoy list

# 5. Monitor agents
gt agents
```

**Polecat propulsion loop:**

```bash
# The canonical polecat workflow
1. gt hook                    # What's hooked?
2. bd mol current             # Where am I in the molecule?
3. Execute current step
4. bd close <step> --continue # Close and advance
5. If more steps: GOTO 2
6. gt done                    # Signal completion
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| Massive parallelism | Designed for 20-30 simultaneous agents |
| Persistent state | Git-backed hooks survive any failure |
| Universal attribution | Every commit, bead, event tracked to specific agent |
| Multi-runtime support | Claude, Codex, Cursor, Gemini, Amp, Auggie |
| Enterprise-ready audit | Compliance trails, work history, quality signals |
| Capability routing | Route work to agents with proven track records |
| Real-world tested | Yegge's 4th orchestrator, battle-tested |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| High cost | $100/hour burn rate possible |
| Steep learning curve | Requires significant agentic experience |
| Design bottleneck | Engine consumes plans faster than you create them |
| Platform dependency | Tmux-based, macOS/Linux primary |
| Early stage | "Two weeks old and wild" - still maturing |

---

## Community & Adoption

- **GitHub Stars**: Growing rapidly since Jan 2026 release
- **Contributors**: Active development by Yegge and community
- **Last Commit**: Active (Feb 2026)
- **Notable Users**: Early adopters in agentic coding community
- **Discussion**: Active Hacker News thread, multiple blog posts

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/steveyegge/gastown |
| Medium Article | https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04 |
| Beads Dependency | https://github.com/steveyegge/beads |
| Hacker News | https://news.ycombinator.com/item?id=46458936 |

---

## Key Takeaways

1. **Gas Town redefines the developer role**: You become a Product Manager orchestrating an AI workforce rather than writing code yourself.

2. **The Propulsion Principle is core**: Agents must execute immediately when work appears - no waiting, no confirmation loops.

3. **State lives outside agent memory**: Git-backed beads and hooks provide durability that survives any agent failure.

4. **Attribution enables enterprise use**: Every action is traceable, enabling compliance, debugging, and performance management.

5. **Scale requires infrastructure**: This isn't a library you import - it's an operational system requiring setup, configuration, and ongoing feeding with design work.

---

*Analysis completed: 2026-02-03 | Sources: Local repo, GitHub, Web Search*
