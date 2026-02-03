# Cipher - Learning Guide

> Educational resource for mastering Cipher concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand how dual memory (knowledge + reflection) improves AI coding assistance
- [x] Learn how to design composable prompt provider systems
- [x] Be able to configure Cipher as an MCP memory layer for Claude Code
- [x] Apply workspace memory patterns for team collaboration
- [x] Evaluate when vector-based memory is better than file-based memory

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| MCP Protocol basics | Cipher is MCP-native | [MCP Documentation](https://modelcontextprotocol.io) |
| Vector embeddings concept | Core to semantic memory | [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) |
| Claude Code familiarity | Primary use case | Claude Code documentation |
| Basic YAML | Configuration files | Any YAML tutorial |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Dual memory and semantic search require understanding |
| Implementation | Beginner | Zero-config setup, npm install |
| Time Investment | 2-4 hours | Full understanding including hands-on |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Cipher is and why it matters

1. **Read the README**
   - Location: https://github.com/campfirein/cipher
   - Time: 15 min
   - Key concepts to note:
     - Dual Memory Layer (System 1 + System 2)
     - MCP integration for IDE compatibility
     - Workspace memory for teams

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram and key mechanisms

3. **Try the Quick Start**
   - Instructions:
     ```bash
     # Install globally
     npm install -g @byterover/cipher

     # Set API key
     export OPENAI_API_KEY=your_key

     # Run interactive mode
     cipher

     # Or run as MCP server
     cipher --mode mcp
     ```
   - Expected outcome: Interactive chat or MCP server running

**Checkpoint:** Can you explain what Cipher does in one sentence?

> "Cipher is a persistent memory layer that gives coding agents semantic memory across sessions."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Dual Memory Architecture**
   - What it is: Two distinct memory types inspired by cognitive science
   - Why it matters: Different information needs different retrieval patterns

   **Knowledge Memory (System 1):**
   - Fast, factual recall
   - Code patterns, API usage, business logic
   - High-confidence stored facts

   **Reflection Memory (System 2):**
   - Reasoning traces and problem-solving patterns
   - How the AI arrived at solutions
   - Useful for similar future problems

   ```yaml
   # Configuration for both memory types
   VECTOR_STORE_COLLECTION=knowledge_memory
   REFLECTION_VECTOR_STORE_COLLECTION=reflection_memory
   DISABLE_REFLECTION_MEMORY=false  # Enable System 2
   ```

2. **Deep Dive: Prompt Provider System**
   - What it is: Composable system prompt generation with priorities
   - Why it matters: Modular, maintainable prompt construction

   ```yaml
   # memAgent/cipher-advanced-prompt.yml
   providers:
     # Static provider - always included
     - name: built-in-memory-search
       type: static
       priority: 100  # Highest priority
       config:
         content: |
           Use memory search before answering if relevant.

     # Dynamic provider - LLM-generated
     - name: summary
       type: dynamic
       priority: 50
       config:
         generator: summary
         history: all

     # File-based provider - project rules
     - name: project-guidelines
       type: file-based
       priority: 40
       config:
         filePath: ./memAgent/project-guidelines.md
         summarize: false

   settings:
     maxGenerationTime: 10000
     failOnProviderError: false
     contentSeparator: "\n\n---\n\n"
   ```

3. **Hands-on Exercise: Configure Cipher for Claude Code**
   - Task: Set up Cipher as memory layer for Claude Code
   - Steps:
     1. Install Cipher: `npm install -g @byterover/cipher`
     2. Create `.mcp.json` in project root:
        ```json
        {
          "mcpServers": {
            "cipher": {
              "type": "stdio",
              "command": "cipher",
              "args": ["--mode", "mcp"],
              "env": {
                "MCP_SERVER_MODE": "aggregator",
                "OPENAI_API_KEY": "your_key"
              }
            }
          }
        }
        ```
     3. Start Claude Code and verify Cipher tools appear
     4. Ask: "Remember that we use Pydantic v2 in this project"
     5. Start new session, ask: "What validation library do we use?"
   - Success criteria: Cipher recalls stored memory in new session

**Checkpoint:** Can you configure Cipher with Claude Code and store/retrieve a memory?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: MCP Aggregator Mode**
   - When to use: You want multiple MCP servers through single endpoint
   - Implementation:
     ```yaml
     # cipher.yml with aggregator
     mcpServers:
       exa:
         type: stdio
         command: npx
         args: ["-y", "exa-mcp-server"]
         env:
           EXA_API_KEY: $EXA_API_KEY

       context7:
         type: "streamable-http"
         url: "https://mcp.context7.com/mcp"

       semgrep:
         type: "streamable-http"
         url: "https://mcp.semgrep.ai/mcp/"
     ```
   - Pitfalls:
     - Tool name conflicts (use `AGGREGATOR_CONFLICT_RESOLUTION=prefix`)
     - Timeout issues with slow servers (increase `AGGREGATOR_TIMEOUT`)

2. **Pattern: Workspace Memory for Teams**
   - When to use: Team collaboration, shared project context
   - Implementation:
     ```bash
     # .env for workspace memory
     USE_WORKSPACE_MEMORY=true
     CIPHER_USER_ID=my-team
     CIPHER_PROJECT_NAME=our-project
     WORKSPACE_VECTOR_STORE_COLLECTION=team_memory
     ```
   - Extracted payload structure:
     ```typescript
     {
       teamMember: "John",
       currentProgress: {
         feature: "authentication",
         status: "in-progress",
         completion: 75
       },
       bugsEncountered: [{
         description: "login timeout issue",
         severity: "high",
         status: "fixed"
       }]
     }
     ```

3. **Real-World Exercise: Build Memory-Enhanced Coding Workflow**
   - Scenario: You're working on a project with repeated patterns
   - Challenge: Configure Cipher to learn and recall:
     - Project coding standards
     - Common debugging solutions
     - Architecture decisions
   - Hints:
     - Use file-based provider for standards
     - Let knowledge memory capture debugging patterns
     - Use reflection memory for complex problem-solving

**Checkpoint:** Can you set up workspace memory and aggregator mode?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| Knowledge Memory | Fast recall of facts, patterns, code snippets | "Use Pydantic v2 computed_field for derived values" |
| Reflection Memory | Reasoning traces and problem-solving patterns | "When debugging OAuth issues, check token expiry first" |
| Workspace Memory | Team-level shared context | "John is working on auth feature (75% complete)" |
| Prompt Provider | Composable system prompt component | Static, dynamic, or file-based content |
| MCP Aggregator | Mode that unifies multiple MCP servers | Cipher + Exa + Context7 through single endpoint |
| Semantic Search | Vector-based similarity search | Finding relevant memories by meaning, not keywords |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Not Exporting Environment Variables in MCP Mode

**What happens:** Cipher fails to start with "API key not found" errors.

**Why it happens:** MCP mode doesn't read from `.env` file automatically.

**How to avoid:** Always export variables or include in MCP config:
```json
{
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "VECTOR_STORE_TYPE": "qdrant"
  }
}
```

**How to fix:** Export variables before starting MCP client:
```bash
export OPENAI_API_KEY=sk-...
```

---

### Mistake 2: Using Default Mode When You Need Tools

**What happens:** Only `ask_cipher` tool appears, no memory tools.

**Why it happens:** Default mode exposes single tool for simplicity.

**How to avoid:** Set `MCP_SERVER_MODE=aggregator` for full tool access.

---

### Mistake 3: Vector Dimension Mismatch

**What happens:** Memory operations fail with dimension errors.

**Why it happens:** Embedding model dimension doesn't match vector store config.

**How to avoid:** Ensure `VECTOR_STORE_DIMENSION` matches embedding model:
- text-embedding-3-small: 1536
- voyage-3-large: 1024
- text-embedding-v3 (Qwen): 1024

---

## Practice Exercises

### Exercise 1: Basic Memory (Beginner)

**Objective:** Store and retrieve a project pattern

**Instructions:**
1. Start Cipher in interactive mode: `cipher`
2. Tell it: "In our project, we use snake_case for Python functions"
3. Start new session
4. Ask: "What naming convention do we use for Python?"

**Solution:** Memory should return the snake_case convention.

---

### Exercise 2: Claude Code Integration (Intermediate)

**Objective:** Set up persistent memory for Claude Code

**Instructions:**
1. Create `.mcp.json` with Cipher config
2. Configure aggregator mode with memory tools
3. Use Claude Code to store 3 project decisions
4. Restart Claude Code and verify recall

---

### Exercise 3: Team Workflow (Advanced)

**Objective:** Configure workspace memory for team

**Challenge:** Set up Cipher so that:
- Team members can store progress updates
- Bug reports are captured with severity
- Project context is shared across sessions

Configure environment, test with sample team updates, verify search.

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Vector embeddings | RAG systems, document search, recommendation systems |
| MCP integration | Any MCP-compatible tool or agent |
| Prompt composition | LLM prompt engineering, system design |
| Dual memory pattern | Cognitive AI systems, chatbot memory |
| Semantic search | Search engines, knowledge bases |

---

## Study Resources

### Essential Reading

1. **Cipher Documentation** - Complete reference for all features
   - https://docs.byterover.dev/cipher/overview

2. **MCP Protocol Spec** - Understanding the underlying protocol
   - https://modelcontextprotocol.io

### Supplementary Materials

- YouTube Tutorial: Claude Code + Cipher Integration
  - https://www.youtube.com/watch?v=AZh9Py6g07Y
- AI Engineering Newsletter: Building Memory Layers
  - https://aiengineering.beehiiv.com/p/hands-on-make-coding-agents-10x-smarter-1

### Community Resources

- Discord: https://discord.com/invite/UMRrpNjh5W
- GitHub Issues: https://github.com/campfirein/cipher/issues

---

## Self-Assessment

### Quiz Yourself

1. What problem does Cipher solve?
   > Session amnesia - AI coding assistants lose context between sessions

2. How does the dual memory system work?
   > Knowledge Memory (System 1) stores facts; Reflection Memory (System 2) stores reasoning patterns

3. When would you use aggregator mode vs default mode?
   > Aggregator when you need full tool access and multiple MCP servers; Default for simple chat

4. What are the main trade-offs of Cipher?
   > Pros: Persistent semantic memory, cross-IDE, team support
   > Cons: External DB dependency, API costs, cold start latency

### Practical Assessment

Build: A Cipher-powered development workflow

Success criteria:
- [ ] Cipher configured with Claude Code via MCP
- [ ] At least 5 project patterns stored in knowledge memory
- [ ] Memory recall works across sessions
- [ ] (Bonus) Aggregator mode with one additional MCP server

---

## What's Next?

After mastering Cipher, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for adaptation ideas
2. **Related Frameworks:** Study mem0, Zep, LangMem for memory layer comparisons
3. **Advanced Topics:**
   - Knowledge graph integration
   - Custom embedding models
   - Multi-tenant workspace memory
   - Self-hosted vector databases

---

*Learning guide created: 2026-02-03 | For: Cipher by Byterover*
