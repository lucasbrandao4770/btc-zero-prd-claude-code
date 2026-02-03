# Beads - Framework Analysis

> Deep dive into Beads: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | https://github.com/steveyegge/beads |
| **Author** | Steve Yegge (former Google/Amazon engineer) |
| **Category** | AI Agent Memory / Issue Tracking |
| **Context7 ID** | `/steveyegge/beads` |
| **Last Updated** | 2026-02-03 |

### One-Line Summary

Beads is a distributed, git-backed graph issue tracker that provides persistent, structured memory for AI coding agents, solving the "50 First Dates" problem where agents lose context between sessions.

---

## Problem Statement

### What Problem Does It Solve?

AI coding agents suffer from **context amnesia** - they wake up each session with no memory of previous work. This leads to:

1. **Repeated explanations** - Users must re-explain project goals every session
2. **Lost progress** - Work completed yesterday is unknown today
3. **No dependency awareness** - Agents cannot track which tasks block others
4. **Merge conflicts** - Multi-agent workflows create ID collisions
5. **Context window waste** - Agents spend tokens re-learning instead of working

Beads replaces messy markdown plans with a **dependency-aware graph** that persists across sessions and syncs via git.

### Who Is It For?

| User Type | Use Case |
|-----------|----------|
| **AI Coding Agents** | Primary target - Claude Code, Cursor, Windsurf, Codex, AMP |
| **Solo Developers** | Personal task tracking with dependency management |
| **Multi-Agent Teams** | Coordinated autonomous development workflows |
| **Offline Developers** | Git-synced tracking that works without network |

### Why Does This Matter?

**Business Value:**
- Agents maintain continuity across sessions (no re-explaining)
- Dependency tracking prevents working on blocked tasks
- Multi-agent workflows without coordination servers
- Audit trail via git history

**Developer Value:**
- Simple CLI (`bd ready`, `bd create`, `bd close`)
- Works offline with git sync
- Extensible SQLite database for custom integrations

---

## Architecture

### Core Concepts

1. **Three-Layer Data Model** - CLI operates on SQLite (fast), which syncs to JSONL (git-tracked), which distributes via git push/pull

2. **Hash-Based IDs** - Random UUID-derived IDs (`bd-a1b2`) prevent collisions when multiple agents/branches create issues concurrently

3. **Dependency Graph** - Four relationship types control execution flow: `blocks`, `parent-child`, `related`, `discovered-from`

4. **Ready Work Detection** - `bd ready` computes transitive blocking to show only actionable tasks

5. **Molecules & Wisps** - Reusable workflow templates (molecules) and ephemeral execution instances (wisps)

### Component Diagram

```
CLI LAYER                    STORAGE LAYER                    SYNC LAYER
---------                    -------------                    ----------

bd create ───┐
bd ready ────┼───▶ SQLite DB ◀──auto-sync──▶ JSONL File ◀──git──▶ Remote
bd close ────┘     (.beads/beads.db)         (.beads/issues.jsonl)
     │              - Fast queries            - Git-tracked
     │              - Local cache             - One line per entity
     │              - Gitignored              - Merge-friendly
     │
     ▼
 Daemon (bd.sock)
     │
     ├── RPC Server (fast queries)
     ├── Auto-Sync Manager (5s debounce)
     └── FlushManager (write batching)
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `.beads/beads.db` | SQLite database (local cache, gitignored) |
| `.beads/issues.jsonl` | JSONL source of truth (git-tracked) |
| `.beads/bd.sock` | Daemon Unix socket (or TCP on Windows) |
| `cmd/bd/` | CLI commands (Cobra framework) |
| `internal/storage/sqlite/` | SQLite storage implementation |
| `internal/types/types.go` | Core data types (Issue, Dependency, etc.) |

---

## Capabilities

### What It Can Do

- [x] **Persistent Memory** - Issues survive across agent sessions
- [x] **Dependency Tracking** - Four relationship types with blocking semantics
- [x] **Ready Work Queue** - `bd ready` shows unblocked tasks in priority order
- [x] **Hash-Based IDs** - Collision-free multi-agent/branch creation
- [x] **Git Sync** - Automatic export/import with conflict resolution
- [x] **Offline Operation** - Full functionality without network
- [x] **Hierarchical Issues** - Epics with child tasks (bd-a3f8.1, bd-a3f8.2)
- [x] **Compaction** - Semantic "memory decay" summarizes old closed tasks
- [x] **Molecules/Wisps** - Reusable workflow templates
- [x] **Extensible Database** - Add custom SQLite tables for integrations
- [x] **JSON Output** - Every command supports `--json` for programmatic use
- [x] **MCP Server** - Native integration with Claude Desktop

### What It Cannot Do

- **Real-time collaboration** - Uses git sync, not live updates
- **Cross-project references** - Each `.beads/` directory is isolated
- **Central coordination** - No locking for concurrent issue claims
- **Rich UI** - CLI-first design (community UIs available)
- **Complex workflows** - Better suited for DAG execution than state machines

---

## How It Works

### Workflow

```
Session Start           Agent Work              Session End
-------------          -----------              -----------
bd prime ──────▶ bd ready ──▶ bd update ──▶ bd close ──▶ bd sync
(inject context)  (get work)   (claim task)   (complete)   (push to git)
```

### Key Mechanisms

**1. Auto-Import on Pull:**
When `git pull` brings new JSONL, the next `bd` command detects the change and imports updates into SQLite.

**2. Debounced Export:**
After CRUD operations, a 5-second debounce batches changes before exporting to JSONL. `bd sync` forces immediate export.

**3. Blocked Issues Cache:**
A materialized cache table enables O(ms) `bd ready` queries even with 10K+ issues. Cache rebuilds on dependency/status changes.

**4. Content Hashing:**
Each issue has a content hash. During import: same hash = skip, different hash = update, no match = create.

### Code Examples

**Basic Agent Workflow:**
```bash
# Initialize in project
bd init --quiet

# Get ready work (JSON for agents)
bd ready --json

# Create new issue
bd create "Fix auth bug" -p 1 -t bug --json

# Add dependency (B needs A)
bd dep add bd-f14c bd-a1b2

# Claim and work
bd update bd-a1b2 --status in_progress
# ... do work ...
bd close bd-a1b2 --reason "Fixed in commit abc123"

# Sync to git
bd sync
```

**Molecule Workflow (Templates):**
```bash
# Create epic with children
bd create "Feature X" -t epic
bd create "Design" -t task --parent bd-abc
bd create "Implement" -t task --parent bd-abc
bd create "Test" -t task --parent bd-abc

# Add sequence dependencies
bd dep add <implement-id> <design-id>   # implement needs design
bd dep add <test-id> <implement-id>      # test needs implement
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| **Git-Native Sync** | JSONL format enables clean diffs, easy merges, works offline |
| **Collision-Free IDs** | Hash-based IDs proven via birthday paradox math (see COLLISION_MATH.md) |
| **Fast Queries** | SQLite with blocked cache: 29ms vs 752ms for ready-work queries |
| **Agent-First Design** | Every command has `--json`, designed for programmatic use |
| **Minimal Dependencies** | Single Go binary, embedded SQLite, no external services |
| **Extensibility** | Custom SQLite tables can join with issue data |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| **Alpha Status (v0.9.x)** | API may change before 1.0, not for mission-critical use |
| **Git-Only Sync** | No real-time collaboration, requires git workflow discipline |
| **Learning Curve** | Molecule/wisp concepts add complexity for simple use cases |
| **No Central Lock** | Multi-agent claim conflicts possible without external coordination |
| **CLI-Only Core** | No built-in GUI (community alternatives exist) |

---

## Community & Adoption

- **GitHub Stars:** ~5,900+ (as of Feb 2026)
- **Contributors:** 29+ with merged PRs
- **Last Commit:** Active daily development
- **Notable Users:** "Tens of thousands" per Steve Yegge (4 weeks post-release)

**Community Tools:**
- nvim-beads (Neovim plugin)
- beads_viewer (Web UI)
- Multiple MCP integrations

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/steveyegge/beads |
| Documentation | https://github.com/steveyegge/beads/tree/main/docs |
| Steve Yegge Articles | https://steve-yegge.medium.com/ |
| MCP Server | https://playbooks.com/mcp/steveyegge-beads |
| DeepWiki | https://deepwiki.com/steveyegge/beads |

---

## Key Takeaways

1. **Beads solves agent amnesia** - Persistent, structured memory replaces session re-explanation with dependency-aware task graphs that survive across sessions.

2. **Git is the sync layer** - No special servers needed. Issues travel with code, work offline, and merge cleanly with hash-based IDs.

3. **Ready-work is the killer feature** - `bd ready` instantly returns actionable tasks by computing transitive blocking, enabling agents to always know what to work on next.

4. **Three-layer architecture enables speed + portability** - Fast SQLite queries locally, portable JSONL in git, distributed via standard git workflows.

5. **Designed for agents, works for humans** - JSON output on every command, but also a usable CLI for developers who want dependency-aware task management.

---

*Analysis completed: 2026-02-03 | Analyst: kb-architect*
