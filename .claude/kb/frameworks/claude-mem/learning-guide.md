# Claude-Mem - Learning Guide

> Educational resource for mastering Claude-Mem concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand memory compression as a context engineering strategy
- [x] Learn how lifecycle hooks enable automatic observation capture
- [x] Be able to implement progressive disclosure patterns for token efficiency
- [x] Apply privacy-aware data handling in AI agent systems
- [x] Recognize the dual session ID pattern for safe agent resume

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Understanding of the host environment | [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) |
| TypeScript fundamentals | Hook scripts are TypeScript | Any TS tutorial |
| HTTP APIs | Worker service exposes REST API | MDN Web Docs |
| SQLite concepts | Database storage layer | SQLite documentation |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Memory compression concept requires understanding context limits |
| Implementation | Intermediate | Hook integration and SDK usage need some experience |
| Time Investment | 2-4 hours | For core concepts; deeper exploration adds more |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Claude-Mem is and why it matters

1. **Read the README**
   - Location: https://github.com/thedotmack/claude-mem or local `README.md`
   - Time: 15 min
   - Key concepts to note: persistent memory, observations, context injection

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component Diagram, Core Concepts section

3. **Try the Quick Start**
   - Instructions:
     ```bash
     # In Claude Code terminal
     /plugin marketplace add thedotmack/claude-mem
     /plugin install claude-mem
     # Restart Claude Code
     ```
   - Expected outcome: Previous session context appears in new sessions automatically

**Checkpoint:** Can you explain what Claude-Mem does in one sentence?

> "Claude-Mem automatically captures tool usage during coding sessions, compresses it with AI, and injects relevant context into future sessions."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Observation Compression**
   - What it is: AI-powered summarization of tool outputs into ~500-token observations
   - Why it matters: Standard tool outputs add 1-10k+ tokens each; compression enables longer effective sessions
   - Code example:
   ```typescript
   // Observation structure (simplified)
   interface Observation {
     id: number;
     title: string;           // AI-generated summary title
     content: string;         // ~500 token compressed content
     tool_name: string;       // Original tool (Bash, Read, Write, etc.)
     created_at: string;
     memory_session_id: string;
   }

   // Compression flow
   const rawOutput = "... 5000 tokens of tool output ...";
   const observation = await sdkAgent.compress(rawOutput);
   // Result: ~500 tokens capturing semantic meaning
   ```

2. **Deep Dive: Progressive Disclosure**
   - What it is: 3-layer retrieval pattern for token-efficient search
   - Why it matters: ~10x token savings by only loading full details when needed
   - Layers:
     ```typescript
     // Layer 1: Index (~50-100 tokens per result)
     search({ query: "auth bug", limit: 10 })
     // Returns: { id, title, created_at, type }

     // Layer 2: Timeline context
     timeline({ anchor: 123, depth_before: 3 })
     // Returns: chronological observations around anchor

     // Layer 3: Full details (~500-1000 tokens per result)
     get_observations({ ids: [123, 456] })
     // Returns: complete observation content
     ```

3. **Deep Dive: Session ID Architecture**
   - What it is: Dual session ID system for safe agent resume
   - Why it matters: Prevents data loss and resume failures
   - The two IDs:
     ```typescript
     // contentSessionId: User's Claude Code session ID
     // - Used for STORING and RETRIEVING observations
     // - Remains constant throughout session lifecycle

     // memorySessionId: SDK's internal session ID
     // - Used for RESUME functionality only
     // - Initially NULL, captured after first SDK message
     // - NEVER use for observation storage

     // CORRECT usage
     storeObservation(session.contentSessionId, obs);

     // WRONG - would break retrieval!
     storeObservation(session.memorySessionId, obs);
     ```

4. **Hands-on Exercise: Explore the Web Viewer**
   - Task: Examine your memory stream and search history
   - Steps:
     1. Ensure Claude-Mem is installed and worker running
     2. Open http://localhost:37777 in browser
     3. Browse the memory stream
     4. Try searching for specific tool uses
     5. Click an observation to see full details
   - Success criteria: Can navigate between summary and detail views

**Checkpoint:** Can you explain the 3-layer progressive disclosure pattern?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Privacy-Aware Data Handling**
   - When to use: Any content that shouldn't be persisted (API keys, personal data)
   - Implementation:
     ```typescript
     // In your prompts, wrap sensitive content:
     "My API key is <private>sk-abc123xyz</private>, use it to..."

     // Claude-Mem strips before storage:
     // Stored: "My API key is [REDACTED], use it to..."

     // Implementation (tag-stripping.ts)
     export function stripPrivateTags(content: string): string {
       return content.replace(/<private>[\s\S]*?<\/private>/gi, '[REDACTED]');
     }
     ```
   - Pitfalls: Tags must be properly closed; nested tags not supported

2. **Pattern: Context Injection Timing**
   - When to use: Understanding when memory becomes available
   - Implementation:
     ```
     Timeline:

     SessionStart Hook
          |
          v
     Context fetched from DB --> additionalContext field
          |
          v
     Claude receives prompt WITH history context
          |
          v
     PostToolUse Hook (captures new observations)
          |
          v
     Stop Hook (generates summary, updates context)
     ```
   - Pitfalls: First session has no history; context is from PREVIOUS sessions

3. **Pattern: Cross-IDE Memory Sharing**
   - When to use: Working on same project in Claude Code and Cursor
   - Implementation:
     ```bash
     # Cursor uses rules file auto-update
     # File: .cursor/rules/claude-mem-context.mdc

     # Context updates at three points:
     # 1. Before prompt (context-inject.sh)
     # 2. After summary (worker auto-update)
     # 3. After session (session-summary.sh)
     ```
   - Pitfalls: Cursor lacks transcript access in stop hook; MCP required for search

4. **Real-World Exercise: Debug a Memory Gap**
   - Scenario: You notice that certain tool outputs aren't appearing in your memory
   - Challenge: Diagnose why observations might be missing
   - Hints:
     - Check if `<private>` tags were used
     - Verify worker is running: `curl http://localhost:37777/api/readiness`
     - Check database directly:
       ```sql
       SELECT * FROM observations
       WHERE memory_session_id = 'your-session-id'
       ORDER BY created_at DESC LIMIT 10;
       ```
     - Review worker logs: `tail -f ~/.claude-mem/logs/worker-$(date +%Y-%m-%d).log`

**Checkpoint:** Can you diagnose why an observation might not appear in search results?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Observation** | Compressed record of tool usage | ~500 token summary of a file edit |
| **Progressive Disclosure** | 3-layer retrieval (index -> timeline -> details) | Search returns IDs first, full content on demand |
| **contentSessionId** | User's Claude Code session identifier | Used for observation storage/retrieval |
| **memorySessionId** | SDK's internal session ID | Used only for resume functionality |
| **Context Injection** | Automatic insertion of relevant history | `additionalContext` field in hook output |
| **Edge Processing** | Data handling at hook layer | Privacy tag stripping before storage |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Using memorySessionId for Observation Storage

**What happens:** Observations become unretrievable; search returns empty results

**Why it happens:** The field names are confusing - "memory" session ID sounds like it's for memory storage

**How to avoid:** Always use `contentSessionId` for `storeObservation()` calls

**How to fix:** Database migration to update affected records

---

### Mistake 2: Expecting Immediate Context in First Session

**What happens:** User wonders why no history appears in a new project

**Why it happens:** Context injection shows PREVIOUS session data, not current

**How to avoid:** Understand the timeline: capture happens now, injection happens next session

---

### Mistake 3: Nesting Private Tags

**What happens:** Inner content still gets stored

**Why it happens:** Regex doesn't handle nested tags

**How to avoid:** Use flat `<private>...</private>` tags without nesting

**How to fix:** Restructure content to avoid nesting

---

## Practice Exercises

### Exercise 1: Observe the Memory Stream (Beginner)

**Objective:** Understand what gets captured automatically

**Instructions:**
1. Start a Claude Code session with Claude-Mem installed
2. Perform several operations (read files, run commands, write code)
3. Open http://localhost:37777
4. Identify each tool use in the memory stream
5. Note the compression ratio (original output vs observation size)

**Solution:** Each tool use should appear as a ~500 token observation with AI-generated title

---

### Exercise 2: Implement Progressive Disclosure (Intermediate)

**Objective:** Practice the 3-layer retrieval pattern

**Instructions:**
1. Use the mem-search skill or MCP tools
2. Search for a topic: `search({ query: "your-topic", limit: 5 })`
3. Note the compact results (IDs and titles only)
4. Get timeline context for an interesting result
5. Fetch full details only for relevant observations

**Success criteria:** You only loaded full content for 1-2 observations, not all 5

---

### Exercise 3: Debug Missing Observations (Advanced)

**Objective:** Develop diagnostic skills for memory issues

**Challenge:** Given a scenario where observations aren't appearing, systematically diagnose the root cause.

**Diagnostic checklist:**
1. Is the worker running? (`curl http://localhost:37777/api/readiness`)
2. Are hooks installed? (Check `~/.claude/settings.json`)
3. Was content wrapped in `<private>` tags?
4. Is the session ID correct in the database?
5. Did the SDKAgent encounter an error? (Check logs)

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Progressive disclosure | Any search interface, API pagination design |
| Context window management | All LLM applications, prompt engineering |
| Privacy-aware data handling | GDPR compliance, secure logging |
| Lifecycle hooks | Plugin systems, middleware patterns |
| Session management | Authentication systems, stateful APIs |

---

## Study Resources

### Essential Reading

1. **Claude-Mem Documentation** (https://docs.claude-mem.ai) - Official reference for all features
2. **SESSION_ID_ARCHITECTURE.md** - Critical understanding of dual ID system (local repo)

### Supplementary Materials

- Factory.ai Context Compression Evaluation (https://factory.ai/news/evaluating-compression)
- Claude Code Hooks Reference (https://code.claude.com/docs/hooks)
- Anthropic Context Engineering blog posts

### Community Resources

- Discord: https://discord.com/invite/J4wttp9vDu
- GitHub Issues: https://github.com/thedotmack/claude-mem/issues
- Twitter: @Claude_Memory

---

## Self-Assessment

### Quiz Yourself

1. What problem does Claude-Mem solve?
   > Context window exhaustion and cross-session amnesia in Claude Code

2. How does progressive disclosure work?
   > 3 layers: search (index) -> timeline (context) -> get_observations (details)

3. When would you use `<private>` tags vs just not saying something?
   > Private tags: content needed for task but shouldn't be stored. Not saying: content truly not needed.

4. What are the main trade-offs of Claude-Mem?
   > Benefits: automatic memory, cross-session continuity. Costs: latency (60-90s), complexity, Windows issues

### Practical Assessment

Build: A debugging session where you intentionally create a "missing observation" scenario and diagnose it.

Success criteria:
- [ ] Can identify when an observation should have been captured
- [ ] Can check worker status and logs
- [ ] Can query the database directly
- [ ] Can explain why the observation is missing

---

## What's Next?

After mastering Claude-Mem, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas and the recommended "Learn From" patterns
2. **Related Frameworks:** Study other context engineering approaches (Factory.ai compression, custom summarization)
3. **Advanced Topics:** Vector embeddings for semantic search, custom observation templates, multi-project memory

---

*Learning guide created: 2026-02-03 | For: Claude-Mem v9.0.12*

**Sources:**
- [Claude-Mem GitHub Repository](https://github.com/thedotmack/claude-mem)
- [Claude-Mem Documentation](https://docs.claude-mem.ai)
- [Factory.ai Context Compression Evaluation](https://factory.ai/news/evaluating-compression)
- Local repository analysis
