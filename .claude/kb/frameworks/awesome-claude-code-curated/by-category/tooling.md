# Category: Tooling

> **Total in awesome-claude-code:** 43 resources
> **Selected for adoption:** 6 resources

---

## Overview

Tooling includes applications built on Claude Code. Categories: Orchestrators (9), Usage Monitors (6), IDE Integrations (6), General (23). We focus on session management, multi-agent coordination, and cost tracking.

---

## Selected Resources

### Orchestrators

#### 1. claude-code-tools (ADOPT)
**Link:** [anthropics/claude-code-tools](https://github.com/anthropics/claude-code-tools)

Session continuity, Rust-powered full-text search, cross-agent handoff.

**Why Selected:**
- Solves cross-session context problem
- Full-text search across sessions
- Rust performance

**Integration:** `cargo install claude-code-tools`

---

#### 2. Claude Squad (ADOPT)
**Link:** [anthropics/claude-squad](https://github.com/anthropics/claude-squad)

Manage multiple Claude Code agents in separate workspaces.

**Why Selected:**
- Multi-agent parallel execution
- Complements our sandbox skill
- Workspace isolation

**Integration:** `npm install -g claude-squad`

---

#### 3. viwo-cli (ADOPT)
**Link:** [anthropics/viwo-cli](https://github.com/anthropics/viwo-cli)

Docker + git worktrees for safer `--dangerously-skip-permissions`.

**Why Selected:**
- Safer autonomous execution
- Complements sandbox skill
- Production-safe YOLO mode

**Integration:** Docker + npm install

---

#### 4. Claude Session Restore (WATCH)
**Link:** [anthropics/session-restore](https://github.com/anthropics/session-restore)

Restore context from previous sessions (handles 2GB files).

**Why Selected:**
- Session continuity for long projects
- Large file handling

**Why Watch:** Complexity, stability concerns

---

### Usage Monitors

#### 5. better-ccflare (ADOPT)
**Link:** [anthropics/better-ccflare](https://github.com/anthropics/better-ccflare)

Feature-rich usage dashboard with Tableau-quality visualizations.

**Why Selected:**
- Cost visibility and tracking
- Usage optimization insights
- Budget management

**Integration:** Cloudflare Workers deployment

---

### General

#### 6. VoiceMode MCP (WATCH)
**Link:** [anthropics/voicemode](https://github.com/anthropics/voicemode)

Natural voice conversations with Whisper.cpp.

**Why Selected:**
- Hands-free coding sessions
- Accessibility improvement

**Why Watch:** Complex audio setup

---

## Skipped Resources

| Category | Skipped | Reason |
|----------|---------|--------|
| IDE Integrations | Cursor tools | We use Claude Code |
| Orchestrators | Simple wrappers | We have sandbox skill |
| Usage Monitors | Basic trackers | better-ccflare is superior |
| General | Platform-specific | Limited use |

---

## Tooling Stack

```
Session Management
├── claude-code-tools    # Search, continuity
├── Session Restore      # Long-term (future)
└── viwo-cli             # Safe isolation

Multi-Agent
├── Claude Squad         # Workspace management
└── sandbox skill        # Our existing skill

Monitoring
└── better-ccflare       # Usage dashboard

Voice (Future)
└── VoiceMode MCP        # Hands-free
```

---

## Integration Priority

| Tool | Priority | Complexity | Week |
|------|----------|------------|------|
| claude-code-tools | High | Medium | 2 |
| Claude Squad | High | Medium | 2 |
| better-ccflare | Medium | Medium | 2 |
| viwo-cli | Medium | Medium | 3 |
| Session Restore | Low | Hard | 4+ |
| VoiceMode | Low | Hard | 4+ |

---

*Category Analysis: 2026-02-03*
