# Supermemory - Learning Guide

> Educational resource for mastering Supermemory concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand how hook-based plugins extend Claude Code
- [x] Learn how to implement persistent memory for AI coding assistants
- [x] Be able to design transcript capture and compression pipelines
- [x] Apply container tag patterns for project isolation
- [x] Understand hybrid memory retrieval vs pure RAG

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| JavaScript/Node.js | Plugin is written in JS | https://nodejs.org/docs |
| Claude Code basics | Must understand the host system | https://claude.ai/code |
| Plugin hooks | Core integration mechanism | Claude Code plugin docs |
| REST APIs | Communication with Supermemory cloud | MDN Web Docs |
| Git basics | Container tags use git roots | https://git-scm.com/book |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Hook lifecycle and memory systems |
| Implementation | Intermediate | JS/Node.js with async patterns |
| Time Investment | 3-4 hours | To understand core mechanisms |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Supermemory is and why it matters

1. **Read the README**
   - Location: `D:/Workspace/Claude Code/Repositorios/frameworks-research/supermemory/README.md`
   - Time: 15 min
   - Key concepts to note:
     - Context injection at session start
     - Automatic conversation capture
     - Codebase indexing capability

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, core concepts section

3. **Try the Quick Start**
   - Instructions:
     1. Get API key at https://console.supermemory.ai
     2. `/plugin marketplace add supermemoryai/claude-supermemory`
     3. `/plugin install claude-supermemory`
     4. `export SUPERMEMORY_CC_API_KEY="sm_..."`
     5. Start a new Claude Code session
   - Expected outcome: See `<supermemory-context>` injected at start

**Checkpoint:** Can you explain what Supermemory does in one sentence?

> "Supermemory is a Claude Code plugin that provides persistent semantic memory across sessions using cloud-based storage and hook-driven capture."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Hook System**

   What it is: Claude Code exposes lifecycle events that plugins can listen to

   Why it matters: Enables automatic capture without user intervention

   Code example:

   ```json
   // plugin/hooks/hooks.json
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

   Key events:
   - `SessionStart` - Fetch and inject memories
   - `UserPromptSubmit` - (Reserved for future use)
   - `PostToolUse` - (Reserved for future use)
   - `Stop` - Capture session transcript

2. **Deep Dive: Container Tags**

   What it is: A unique identifier scoping memories to a project

   Why it matters: Prevents TypeScript project memories appearing in Python projects

   Code example:

   ```javascript
   // src/lib/container-tag.js
   function getContainerTag(cwd) {
     const gitRoot = getGitRoot(cwd);      // /home/user/my-project
     const basePath = gitRoot || cwd;
     return `claudecode_project_${sha256(basePath)}`;
     // Returns: claudecode_project_a1b2c3d4e5f6g7h8
   }
   ```

3. **Deep Dive: Transcript Formatting**

   What it is: Parsing Claude's JSONL transcript into structured memory

   Why it matters: Raw transcripts are noisy; formatting extracts signal

   Code example:

   ```javascript
   // src/lib/transcript-formatter.js
   function formatEntry(entry) {
     if (entry.type === 'user') {
       return `[role:user]\n${cleanContent(entry.message.content)}\n[user:end]`;
     } else if (entry.type === 'assistant') {
       return `[role:assistant]\n${cleanContent(entry.message.content)}\n[assistant:end]`;
     }
   }

   // Cleans system reminders and injected context
   function cleanContent(text) {
     return text
       .replace(/<system-reminder>[\s\S]*?<\/system-reminder>/g, '')
       .replace(/<supermemory-context>[\s\S]*?<\/supermemory-context>/g, '')
       .trim();
   }
   ```

4. **Hands-on Exercise: Trace the Session Flow**

   Task: Follow data flow from SessionStart to Stop

   Steps:
   1. Open `src/context-hook.js` - read top to bottom
   2. Identify: Where does API key come from?
   3. Identify: What does `getProfile()` return?
   4. Open `src/summary-hook.js`
   5. Identify: How does it know what's new (not already captured)?

   Success criteria: Can explain the `lastCapturedUuid` tracking mechanism

**Checkpoint:** Can you implement a basic session capture using Supermemory's patterns?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Hybrid Memory Retrieval**

   When to use: When pure semantic search isn't enough

   Implementation:
   ```javascript
   // src/lib/supermemory-client.js
   async getProfile(containerTag, query) {
     const result = await this.client.profile({
       containerTag: containerTag || this.containerTag,
       q: query,  // Query for context
     });
     return {
       profile: {
         static: result.profile?.static || [],   // Persistent facts
         dynamic: result.profile?.dynamic || [], // Recent context
       },
       searchResults: result.searchResults,      // Semantic matches
     };
   }
   ```

   Pitfalls:
   - Don't over-rely on semantic search alone
   - Static facts (user preferences) are more reliable than search
   - Dynamic facts change; don't treat as permanent

2. **Pattern: Observation Compression**

   When to use: Storing tool usage without bloating memory

   Implementation:
   ```javascript
   // src/lib/compress.js
   function compressObservation(toolName, toolInput, toolResponse) {
     switch (toolName) {
       case 'Edit':
         // "Edited auth/login.js: 'useState' -> 'useReducer'"
         return `Edited ${file}: "${oldSnippet}" -> "${newSnippet}"`;
       case 'Bash':
         // "Ran: npm install lodash [FAILED]"
         return `Ran: ${cmd}${success ? '' : ' [FAILED]'}`;
     }
   }
   ```

   Pitfalls:
   - Don't store full file contents
   - Truncate to fixed length (50 chars default)
   - Skip read-only tools (Read, Glob, Grep)

3. **Pattern: Deduplication**

   When to use: Before injecting context to avoid repetition

   Implementation:
   ```javascript
   // src/lib/format-context.js
   function deduplicateMemories(staticFacts, dynamicFacts, searchResults) {
     const seen = new Set();

     const uniqueStatic = staticFacts.filter((m) => {
       if (seen.has(m)) return false;
       seen.add(m);
       return true;
     });
     // ... same for dynamic and search
   }
   ```

4. **Real-World Exercise: Build a Local Memory System**

   Scenario: You want Supermemory-like behavior but fully local

   Challenge: Implement a Python-based local memory with:
   - SQLite storage
   - Container tag isolation
   - Stop hook capture
   - Context injection

   Hints:
   - Use `jarvis-integration.md` code patterns
   - Start with schema: `CREATE TABLE memories (id, project_id, content, created_at)`
   - Hook script can be Python with `#!/usr/bin/env python3`

**Checkpoint:** Can you solve memory retrieval without cloud APIs using local vectors?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Container Tag** | Unique project identifier based on git root hash | `claudecode_project_a1b2c3d4` |
| **Hook** | Claude Code lifecycle event plugins can respond to | `SessionStart`, `Stop` |
| **Profile** | User's extracted preferences and patterns | "Prefers TypeScript", "Uses Bun" |
| **Static Facts** | Long-term persistent user information | "Works at Acme Corp" |
| **Dynamic Facts** | Recent context that may change | "Working on auth feature" |
| **Hybrid Memory** | Combining profiles + search + keywords | Profile + RAG + keyword search |
| **Transcript** | JSONL log of Claude Code session | User/assistant message pairs |
| **Compression** | Reducing tool output to summary | "Edited file.js: X -> Y" |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Capturing Too Much

**What happens:** Memory fills with noise (file reads, grep patterns)

**Why it happens:** No tool filtering configured

**How to avoid:** Set `skipTools` in settings:
```json
{
  "skipTools": ["Read", "Glob", "Grep", "TodoWrite"]
}
```

**How to fix:** Delete noisy memories, reconfigure, re-index

---

### Mistake 2: Cross-Project Pollution

**What happens:** Python project memories appear in JavaScript project

**Why it happens:** Not understanding container tag scoping

**How to avoid:** Ensure git repos are properly initialized, check container tag generation

---

### Mistake 3: Injecting Too Much Context

**What happens:** Claude becomes confused with too many memories

**Why it happens:** No `maxProfileItems` limit set

**How to avoid:** Set limits in settings:
```json
{
  "maxProfileItems": 5
}
```

---

### Mistake 4: Missing API Key

**What happens:** Plugin fails silently with "No previous memories"

**Why it happens:** Environment variable not exported

**How to avoid:** Add to shell profile:
```bash
# ~/.bashrc or ~/.zshrc
export SUPERMEMORY_CC_API_KEY="sm_..."
```

---

## Practice Exercises

### Exercise 1: Trace the Data Flow (Beginner)

**Objective:** Understand how memories flow through the system

**Instructions:**
1. Draw a diagram showing: SessionStart -> API -> Context Injection
2. Draw another showing: Stop -> Transcript -> API -> Storage
3. Label each component with the source file

**Solution:** See Component Diagram in `analysis.md`

---

### Exercise 2: Implement Tool Compression (Intermediate)

**Objective:** Learn to reduce tool observations to summaries

**Instructions:**
1. Write a function that takes tool name, input, and output
2. Return a one-line summary for each tool type
3. Handle at least: Edit, Write, Bash, Task

**Starting point:**
```python
def compress_observation(tool_name: str, tool_input: dict, tool_response: dict = None) -> str:
    # Your implementation here
    pass

# Test
print(compress_observation("Edit", {
    "file_path": "/home/user/project/auth/login.js",
    "old_string": "useState",
    "new_string": "useReducer"
}))
# Expected: "Edited auth/login.js: 'useState' -> 'useReducer'"
```

---

### Exercise 3: Local Memory Store (Advanced)

**Objective:** Build Supermemory-like system locally

**Challenge:** Create a Python module with:
- `add_memory(content, project_id)` - Store memory
- `search_memory(query, project_id)` - Keyword search
- `get_recent(project_id, limit)` - Recent memories
- Container tag generation from git root

**Bonus:** Add SQLite-backed vector search using sentence-transformers

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Hook-based plugin architecture | VSCode extensions, Cursor plugins, any IDE |
| Transcript parsing | Log analysis, conversation analytics |
| Memory compression | Context window management, summarization |
| Container/namespace isolation | Multi-tenant systems, Kubernetes |
| Hybrid retrieval | RAG systems, knowledge bases |
| Profile extraction | User modeling, personalization systems |

---

## Study Resources

### Essential Reading

1. **Supermemory Blog Post** - https://blog.supermemory.ai/we-added-supermemory-to-claude-code-its-insanely-powerful-now/
   - Why it's essential: Explains the "why" behind the design

2. **Source Code** - `D:/Workspace/Claude Code/Repositorios/frameworks-research/supermemory/src/`
   - Why it's essential: The implementation is the documentation

### Supplementary Materials

- Supermemory Docs: https://supermemory.ai/docs/integrations/claude-code
- Claude Code Plugin Hooks: (Claude Code documentation)
- LongMemEval Benchmark: Understanding hybrid memory performance

### Community Resources

- GitHub Issues: https://github.com/supermemoryai/claude-supermemory/issues
- Supermemory Discord: (check supermemory.ai for links)

---

## Self-Assessment

### Quiz Yourself

1. What problem does Supermemory solve?
   > Context loss between Claude Code sessions - users must re-explain preferences, projects, and decisions.

2. How does the container tag mechanism work?
   > SHA256 hash of git root directory, truncated to 16 chars, prefixed with `claudecode_project_`.

3. When would you use compression vs full capture?
   > Compression for tool observations (Edit, Bash); full capture for user messages and decisions.

4. What are the main trade-offs of Supermemory?
   > Pros: Automatic, semantic search, hybrid retrieval. Cons: Cloud dependency, cost, data ownership.

### Practical Assessment

Build: A local session memory system for Jarvis

Success criteria:
- [x] Uses SQLite for storage
- [x] Implements container tag isolation
- [x] Captures sessions via Stop hook
- [x] Injects context via SessionStart hook
- [x] Compresses tool observations
- [x] Works offline (no cloud dependency)

---

## What's Next?

After mastering Supermemory, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas
2. **Related Frameworks:** Study `claude-mem`, `mcp-memory-service`
3. **Advanced Topics:**
   - Local vector embeddings (sentence-transformers, nomic-embed)
   - Profile extraction using local LLMs
   - Multi-modal memory (images, diagrams)

---

*Learning guide created: 2026-02-03 | For: Supermemory*
