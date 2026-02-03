# Supermemory - Framework Analysis

> Deep dive into Supermemory: architecture, capabilities, and value proposition

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Repository** | https://github.com/supermemoryai/claude-supermemory |
| **Author** | Supermemory (Dhravya Shah) |
| **Category** | Memory Infrastructure / Claude Code Plugin |
| **Context7 ID** | `/supermemoryai/supermemory` |
| **Last Updated** | 2026-02-03 |

### One-Line Summary

A Claude Code plugin that provides persistent, semantic memory across sessions using hook-based capture and hybrid retrieval.

---

## Problem Statement

### What Problem Does It Solve?

Claude Code sessions are ephemeral - every time you start a new session, the AI has no memory of previous conversations, decisions, or learned preferences. Developers repeatedly explain:

- Coding style preferences ("Use TypeScript", "Prefer functional components")
- Project architecture and conventions
- What they were working on yesterday
- Technical decisions already made

This creates "contextual tax" - wasted time re-establishing context instead of making progress.

### Who Is It For?

- **Power Users**: Developers using Claude Code daily across multiple sessions
- **Teams**: Groups wanting consistent AI behavior aligned with conventions
- **Long-running Projects**: Projects where architectural knowledge must persist
- **Multi-project Developers**: Those working across many codebases

### Why Does This Matter?

- **Time Savings**: Eliminates 5-15 minutes of context setup per session
- **Consistency**: AI responses reflect learned patterns, not generic suggestions
- **Compounding Value**: Memory improves over time as preferences accumulate
- **Personalization**: Claude learns your "engineering taste" and adapts recommendations

---

## Architecture

### Core Concepts

1. **Hook System** - Event-driven capture using Claude Code's plugin hooks (SessionStart, Stop, PostToolUse)
2. **Container Tags** - Project-scoped memory isolation using SHA256 hashes of git roots
3. **Hybrid Memory** - Combines static profile facts, dynamic recent context, and semantic search
4. **Transcript Processing** - Parses Claude's JSONL transcripts to extract meaningful interactions
5. **Memory Compression** - Reduces tool observations to concise summaries before storage

### Component Diagram

```
                    CLAUDE CODE PLUGIN ECOSYSTEM
                    ============================

┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE CODE                                 │
├─────────────────────────────────────────────────────────────────┤
│  SessionStart    UserPromptSubmit    PostToolUse    Stop        │
│       │                │                  │           │         │
│       ▼                ▼                  ▼           ▼         │
│  ┌─────────┐    ┌───────────┐     ┌───────────┐  ┌─────────┐   │
│  │context- │    │ prompt-   │     │observation│  │summary- │   │
│  │hook.js  │    │ hook.js   │     │ -hook.js  │  │hook.js  │   │
│  └────┬────┘    └───────────┘     └───────────┘  └────┬────┘   │
│       │                                               │         │
└───────┼───────────────────────────────────────────────┼─────────┘
        │                                               │
        │  getProfile()                        addMemory()
        │                                               │
        ▼                                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SUPERMEMORY CLIENT                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  SupermemoryClient                                         │  │
│  │  - addMemory(content, containerTag, metadata)             │  │
│  │  - search(query, containerTag, options)                   │  │
│  │  - getProfile(containerTag, query)                        │  │
│  │  - listMemories(containerTag, limit)                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SUPERMEMORY CLOUD                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Vector DB  │  │  Profile     │  │  Hybrid Search       │  │
│  │   (Embeddings)│  │  Extraction │  │  (Semantic+Keyword)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Files/Folders

| Path | Purpose |
|------|---------|
| `plugin/hooks/hooks.json` | Hook registration (SessionStart, Stop, PostToolUse) |
| `src/context-hook.js` | Fetches profile on session start, injects context |
| `src/summary-hook.js` | Saves session transcript at Stop |
| `src/lib/supermemory-client.js` | API wrapper for Supermemory cloud |
| `src/lib/transcript-formatter.js` | Parses JSONL transcripts, extracts turns |
| `src/lib/compress.js` | Compresses tool observations to summaries |
| `src/lib/format-context.js` | Formats retrieved memories for injection |
| `src/lib/container-tag.js` | Generates project-scoped container tags |
| `plugin/skills/super-search/SKILL.md` | Skill for searching past sessions |
| `plugin/commands/index.md` | Codebase indexing command |

---

## Capabilities

### What It Can Do

- [x] **Auto-capture session transcripts** - Saves user/assistant turns at session end
- [x] **Context injection** - Injects relevant memories at session start
- [x] **Hybrid retrieval** - Static profile + dynamic context + semantic search
- [x] **Project isolation** - Memory scoped to git repository via container tags
- [x] **Tool filtering** - Configurable capture/skip lists for tools
- [x] **Codebase indexing** - Command to explore and index project architecture
- [x] **Memory search skill** - `super-search` skill for querying past sessions
- [x] **Deduplication** - Removes duplicate memories before injection
- [x] **Relative time formatting** - Shows "2d ago", "just now" for context

### What It Cannot Do

- Offline operation (requires Supermemory cloud API)
- Local-only storage (all memories go to cloud)
- Free tier (requires Supermemory Pro subscription)
- Real-time streaming capture (captures at Stop hook, not continuously)
- Multi-user collaboration (container tags are per-machine/git config)

---

## How It Works

### Workflow

```
SessionStart                PostToolUse (Edit/Write/Bash/Task)      Stop
     │                              │                                  │
     ▼                              ▼                                  ▼
┌─────────┐                  ┌─────────────┐                    ┌──────────┐
│ Fetch   │                  │ (Currently  │                    │ Read     │
│ Profile │                  │  no-op,     │                    │Transcript│
│   &     │                  │  placeholder│                    │  JSONL   │
│ Search  │                  │  for future)│                    │          │
└────┬────┘                  └─────────────┘                    └────┬─────┘
     │                                                               │
     ▼                                                               ▼
┌─────────────────┐                                          ┌───────────────┐
│ formatContext() │                                          │ formatNew     │
│ - Static facts  │                                          │ Entries()     │
│ - Dynamic facts │                                          │ - Parse turns │
│ - Search results│                                          │ - Track UUID  │
└────────┬────────┘                                          └───────┬───────┘
         │                                                           │
         ▼                                                           ▼
┌──────────────────────────┐                              ┌───────────────────┐
│ <supermemory-context>    │                              │ client.addMemory()│
│ ## User Profile          │                              │ - session_turn    │
│ ## Recent Context        │                              │ - container tag   │
│ </supermemory-context>   │                              │ - timestamp       │
└──────────────────────────┘                              └───────────────────┘
```

### Key Mechanisms

**1. Container Tag Generation**

```javascript
// src/lib/container-tag.js
function getContainerTag(cwd) {
  const gitRoot = getGitRoot(cwd);
  const basePath = gitRoot || cwd;
  return `claudecode_project_${sha256(basePath)}`;  // SHA256 truncated to 16 chars
}
```

This ensures each git repository gets isolated memory, preventing cross-project bleed.

**2. Transcript Parsing**

The `transcript-formatter.js` reads Claude's JSONL transcript files:

```javascript
// Parses each line as JSON, extracts user/assistant entries
function formatNewEntries(transcriptPath, sessionId) {
  const entries = parseTranscript(transcriptPath);
  const lastCapturedUuid = getLastCapturedUuid(sessionId);  // From tracker file
  const newEntries = getEntriesSinceLastCapture(entries, lastCapturedUuid);
  // Format and return
}
```

**3. Memory Compression**

Tool observations are compressed before storage:

```javascript
// src/lib/compress.js
function compressObservation(toolName, toolInput, toolResponse) {
  switch (toolName) {
    case 'Edit':
      return `Edited ${file}: "${oldSnippet}" -> "${newSnippet}"`;
    case 'Bash':
      return `Ran: ${cmd}${success ? '' : ' [FAILED]'}`;
    // ...
  }
}
```

**4. Context Formatting**

Retrieved memories are formatted with sections:

```javascript
// src/lib/format-context.js
function formatContext(profileResult, includeProfile, includeRelevantMemories, maxResults) {
  return `<supermemory-context>
The following is recalled context about the user...

## User Profile (Persistent)
${statics.map(f => `- ${f}`).join('\n')}

## Recent Context
${dynamics.map(f => `- ${f}`).join('\n')}

</supermemory-context>`;
}
```

### Code Examples

**Hook Registration (hooks.json)**

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "node ${CLAUDE_PLUGIN_ROOT}/scripts/context-hook.cjs",
        "timeout": 30
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "node ${CLAUDE_PLUGIN_ROOT}/scripts/summary-hook.cjs",
        "timeout": 30
      }]
    }]
  }
}
```

**Supermemory Client Usage**

```javascript
// Adding a memory
await client.addMemory(
  formatted,           // Content
  containerTag,        // Project scope
  {
    type: 'session_turn',
    project: projectName,
    timestamp: new Date().toISOString(),
  },
  sessionId           // Custom ID for dedup
);

// Searching memories
const result = await client.getProfile(containerTag, query);
// Returns: { profile: { static: [], dynamic: [] }, searchResults: { results: [] }}
```

---

## Strengths & Weaknesses

### Strengths

| Strength | Evidence |
|----------|----------|
| **Hook-native integration** | Uses Claude Code's official plugin hooks (SessionStart, Stop, PostToolUse) |
| **Minimal token overhead** | Context injection is ~200-500 tokens, not thousands |
| **Hybrid retrieval** | Combines profiles + search (81.6% LongMemEval score vs 40-60% for RAG) |
| **Project isolation** | Container tags prevent cross-project memory pollution |
| **Configurable capture** | `skipTools` / `captureTools` settings allow fine-grained control |
| **Incremental capture** | UUID tracking ensures only new content is saved |

### Weaknesses

| Weakness | Impact |
|----------|--------|
| **Cloud dependency** | No offline mode; API latency on SessionStart |
| **Paid requirement** | Requires Supermemory Pro ($9+/month) |
| **PostToolUse underutilized** | Currently a no-op placeholder |
| **No local compression** | Full transcripts sent to cloud for processing |
| **Limited manual control** | No easy way to view/edit/delete specific memories |

---

## Community & Adoption

- **GitHub Stars:** 200+ (claude-supermemory repo)
- **Contributors:** 3-5 core contributors
- **Last Commit:** January 2026 (active development)
- **Notable Users:** Supermemory claims "tens of thousands" of AI applications use their memory API
- **Benchmark:** 81.6% on LongMemEval (vs 40-60% for typical RAG)

---

## Official Resources

| Resource | URL |
|----------|-----|
| Repository | https://github.com/supermemoryai/claude-supermemory |
| Documentation | https://supermemory.ai/docs/integrations/claude-code |
| Blog Post | https://blog.supermemory.ai/we-added-supermemory-to-claude-code-its-insanely-powerful-now/ |
| API Console | https://console.supermemory.ai |
| Memory API Docs | https://supermemory.ai/docs/memory-api/sdks/anthropic-claude-memory |

---

## Key Takeaways

1. **Hook-based architecture is elegant** - Leverages Claude Code's native plugin system without hacks
2. **Hybrid memory outperforms RAG** - Profile extraction + dynamic context + search is more effective than pure similarity search
3. **Project isolation via container tags** - Simple but effective scoping using git root hashes
4. **Transcript capture at Stop** - Batching saves API calls vs per-turn capture
5. **Compression is crucial** - Reducing tool observations to summaries prevents memory bloat

---

*Analysis completed: 2026-02-03 | Analyst: kb-architect*
