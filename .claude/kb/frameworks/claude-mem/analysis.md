# Claude-Mem - Framework Analysis

> Deep dive into Claude-Mem: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | https://github.com/thedotmack/claude-mem |
| **Author** | Alex Newman (@thedotmack) |
| **Category** | AI Agent Memory / Context Engineering |
| **Context7 ID** | `/thedotmack/claude-mem` |
| **Last Updated** | 2026-01-28 (v9.0.12) |

### One-Line Summary

A persistent memory compression system for Claude Code that automatically captures tool usage, compresses observations using AI, and injects relevant context into future sessions.

---

## Problem Statement

### What Problem Does It Solve?

Standard Claude Code sessions hit context limits after ~50 tool uses. Each tool call adds 1-10k+ tokens to the context, and Claude re-synthesizes all previous outputs on every response (O(N^2) complexity). When sessions end or context is compacted, valuable working memory is lost.

**Key pain points:**
1. **Context Window Exhaustion** - Sessions become unproductive as context fills
2. **Session Amnesia** - No continuity between sessions on the same project
3. **Repeated Explanations** - Users must re-explain codebase context each time
4. **Lost Decisions** - Previous architectural decisions and debugging steps forgotten

### Who Is It For?

- **Claude Code Users** - Primary target audience using Claude for development
- **Cursor Users** - Cross-IDE support via hooks integration
- **Long-Running Projects** - Teams working on complex codebases over extended periods
- **Multi-Session Workflows** - Developers who return to projects across days/weeks

### Why Does This Matter?

Without persistent memory, AI assistants operate as if every session is their first encounter with your codebase. Claude-Mem transforms this by creating a "living memory" that compounds knowledge over time. As the author states: "Memory isn't storage. It's compression."

---

## Architecture

### Core Concepts

1. **Observations** - Compressed records of tool usage (MCP tools, shell commands, file edits) capturing what Claude did and why
2. **Sessions** - Bounded conversation contexts with content_session_id (user's session) and memory_session_id (SDK's internal session for resume)
3. **Summaries** - AI-generated semantic summaries of session activity for efficient retrieval
4. **Progressive Disclosure** - 3-layer retrieval pattern (search index -> timeline -> full observations) for token efficiency
5. **Lifecycle Hooks** - Integration points: SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd

### Component Diagram

```
                                CLAUDE CODE SESSION
                                        |
        +------------------+------------+------------+------------------+
        |                  |                         |                  |
   SessionStart       UserPrompt              PostToolUse            Stop
        |                  |                         |                  |
        v                  v                         v                  v
+-----------------------------------------------------------------------+
|                         HOOK LAYER (TypeScript)                        |
|   - Tag stripping (<private> content removed)                         |
|   - Session initialization                                             |
|   - Observation capture                                                |
+-----------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------+
|                    WORKER SERVICE (Express API :37777)                 |
|   +------------------+  +------------------+  +------------------+     |
|   |    SDKAgent      |  |  SessionManager  |  |  SearchManager   |     |
|   | (Claude Agent SDK)|  | (Session CRUD)   |  | (FTS5 + Chroma)  |     |
|   +------------------+  +------------------+  +------------------+     |
+-----------------------------------------------------------------------+
                                        |
                    +-------------------+-------------------+
                    |                                       |
                    v                                       v
        +-------------------+                   +-------------------+
        |   SQLite (FTS5)   |                   |   Chroma Vector   |
        | ~/.claude-mem/    |                   | ~/.claude-mem/    |
        | claude-mem.db     |                   | chroma/           |
        +-------------------+                   +-------------------+

                    VIEWER UI                      MCP SERVER
                    :37777/                        (4 tools)
                    +-------------------+          +-------------------+
                    |  React Web App    |          |  search           |
                    |  - Memory Stream  |          |  timeline         |
                    |  - Search         |          |  get_observations |
                    |  - Settings       |          |  __IMPORTANT      |
                    +-------------------+          +-------------------+
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `src/hooks/` | TypeScript hook implementations (built to `plugin/scripts/*-hook.js`) |
| `src/services/worker-service.ts` | Express API server on port 37777 |
| `src/services/worker/SDKAgent.ts` | Claude Agent SDK integration for AI compression |
| `src/services/sqlite/` | SQLite database with FTS5 full-text search |
| `src/services/sync/ChromaSync.ts` | Vector embeddings for semantic search |
| `plugin/skills/mem-search/` | MCP skill for natural language queries |
| `src/ui/viewer/` | React web interface at localhost:37777 |

---

## Capabilities

### What It Can Do

- [x] **Automatic Observation Capture** - Records tool usage without manual intervention
- [x] **AI-Powered Compression** - Uses Claude Agent SDK to generate semantic summaries
- [x] **Cross-Session Context Injection** - Automatically includes relevant history in new sessions
- [x] **Hybrid Search** - FTS5 keyword search + Chroma vector semantic search
- [x] **Progressive Disclosure** - 3-layer token-efficient retrieval (index -> timeline -> details)
- [x] **Privacy Control** - `<private>` tags exclude sensitive content from storage
- [x] **Session Resume** - SDK session persistence for multi-turn memory workflows
- [x] **Web Viewer UI** - Real-time memory stream visualization at localhost:37777
- [x] **Cross-IDE Support** - Works with Cursor via rules file auto-update

### What It Cannot Do

- **No Real-Time Compression** - Observations generated after tool completion (60-90s latency in Endless Mode)
- **No Selective Forgetting** - Cannot easily "forget" specific observations without database manipulation
- **No Cross-Project Memory** - Memory is project-scoped; no global knowledge transfer
- **Windows Chroma Disabled** - Vector search temporarily unavailable on Windows (keyword search works)
- **No Transcript Access in Cursor** - Stop hook lacks transcript data unlike Claude Code

---

## How It Works

### Workflow

```
Tool Execution -> PostToolUse Hook -> Worker API -> SDKAgent (AI Compression) -> SQLite/Chroma
                                                         |
Session Start -> SessionStart Hook -> Worker API -> Context Injection <- Search/Retrieve
```

### Key Mechanisms

**1. Observation Generation (SDKAgent.ts)**

The SDKAgent uses Claude's Agent SDK to compress tool outputs into ~500-token observations:

```typescript
// Simplified observation generation flow
const observation = await sdkAgent.query({
  prompt: observationPrompt(toolName, toolInput, toolOutput),
  options: {
    model: 'claude-sonnet-4-5-20250929',
    ...(hasRealMemorySessionId && { resume: session.memorySessionId })
  }
});

// Store with content session ID (NOT memory session ID)
dbManager.getSessionStore().storeObservation(
  session.contentSessionId,  // User's session for retrieval
  session.project,
  observation
);
```

**2. Context Injection (SessionStart Hook)**

Context is injected via the `additionalContext` field in hook output:

```typescript
// Hook output structure
{
  "status": "success",
  "continue": true,
  "additionalContext": "# Memory Context\n\n## Recent Activity\n..."
}
```

**3. Progressive Disclosure (MCP Tools)**

3-layer workflow for token efficiency:

```typescript
// Layer 1: Compact index (~50-100 tokens/result)
const results = await search({ query: "authentication bug", limit: 10 });

// Layer 2: Chronological context
const timeline = await timeline({ anchor: results[0].id, depth_before: 3 });

// Layer 3: Full details (~500-1000 tokens/result)
const observations = await get_observations({ ids: [123, 456] });
```

### Code Examples

**Privacy Tag Stripping (Edge Processing)**

```typescript
// src/utils/tag-stripping.ts
export function stripPrivateTags(content: string): string {
  return content.replace(/<private>[\s\S]*?<\/private>/gi, '[REDACTED]');
}

// Applied at hook layer BEFORE data reaches worker/database
const sanitizedOutput = stripPrivateTags(toolOutput);
```

**Session ID Architecture (Critical)**

```typescript
// Two distinct session IDs
interface Session {
  contentSessionId: string;  // User's Claude Code session ID
  memorySessionId: string | null;  // SDK's internal session (initially NULL)
}

// CRITICAL: Observations stored with contentSessionId
storeObservation(session.contentSessionId, ...);  // CORRECT
storeObservation(session.memorySessionId, ...);   // WRONG - would break retrieval

// Resume only when real memory session captured
query({
  ...(hasRealMemorySessionId && { resume: session.memorySessionId })
});
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| **Automatic Operation** | No manual tagging or commands required - hooks capture everything |
| **Token-Efficient Retrieval** | 3-layer progressive disclosure achieves ~10x token savings |
| **Cross-Session Continuity** | Context automatically injected into new sessions |
| **Privacy-Aware** | `<private>` tags provide user-level content control |
| **Hybrid Search** | FTS5 + Chroma covers both keyword and semantic queries |
| **Active Development** | v9.0.12 with rapid iteration (GitHub stars: 4,100+) |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| **Latency Overhead** | 60-90s per observation in Endless Mode affects real-time workflows |
| **Windows Limitations** | Chroma disabled, console popup issues (partially fixed in v9.0.6) |
| **Zombie Process Risk** | SDK subprocess management required extensive fixes (v9.0.8) |
| **Complexity** | Dual session ID system requires careful handling to avoid bugs |
| **No Selective Memory** | Cannot easily prune specific observations |

---

## Community & Adoption

- **GitHub Stars:** 4,100+
- **Contributors:** Active community with named contributors (@bigph00t, @Glucksberg, @maxmillienjr)
- **Last Commit:** 2026-01-28 (v9.0.12)
- **Notable Users:** Featured on Awesome Claude Code list, Product Hunt launch

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/thedotmack/claude-mem |
| Documentation | https://docs.claude-mem.ai |
| Web Viewer | http://localhost:37777 (local) |
| Discord | https://discord.com/invite/J4wttp9vDu |
| Twitter | https://x.com/Claude_Memory |

---

## Key Takeaways

1. **Memory is Compression, Not Storage** - The core insight that drives the architecture: compress observations to ~500 tokens while preserving semantic meaning
2. **Progressive Disclosure Saves Tokens** - 3-layer retrieval (index -> timeline -> details) achieves ~10x efficiency over naive full-content retrieval
3. **Dual Session IDs are Critical** - contentSessionId for observation storage, memorySessionId for SDK resume - mixing these causes data loss
4. **Edge Processing for Privacy** - `<private>` tag stripping happens at hook layer, before data reaches storage
5. **Hook-Based Integration** - 5 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) provide clean integration points

---

*Analysis completed: 2026-02-03 | Analyst: kb-architect*

**Sources:**
- [Claude-Mem GitHub Repository](https://github.com/thedotmack/claude-mem)
- [Claude-Mem Documentation](https://docs.claude-mem.ai)
- [Factory.ai Context Compression Evaluation](https://factory.ai/news/evaluating-compression)
- Local repository analysis: `D:/Workspace/Claude Code/Repositorios/frameworks-research/claude-mem/`
