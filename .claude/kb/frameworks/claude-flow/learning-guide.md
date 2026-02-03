# Claude-Flow - Learning Guide

> Educational resource for mastering Claude-Flow concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand multi-agent swarm orchestration with queen-led hierarchical coordination
- [x] Learn how to configure anti-drift defaults for reliable long-horizon agent work
- [x] Be able to implement 3-tier model routing to reduce API costs 75%
- [x] Apply consensus protocols (Raft, Byzantine) for fault-tolerant coordination
- [x] Master MCP tool integration for Claude Code extension

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Framework extends Claude Code | claude.ai/code documentation |
| MCP understanding | Claude-Flow is MCP-native | Model Context Protocol spec |
| Node.js 20+ | Required runtime | nodejs.org |
| Multi-agent concepts | Framework is agent-centric | KB: agentic-ai/01-best-practices/ |
| TypeScript familiarity | Source code is TypeScript | typescriptlang.org |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Intermediate | Multi-agent orchestration requires understanding coordination patterns |
| Implementation | Advanced | Full feature set requires MCP setup, memory configuration, consensus tuning |
| Time Investment | Days | Basic usage in hours; mastery requires days of experimentation |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Claude-Flow is and why it matters

1. **Read the README Overview**
   - Location: Repository README.md, first 500 lines
   - Time: 30 min
   - Key concepts to note: 60+ agents, swarm topologies, 3-tier routing, anti-drift

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, core concepts, workflow section

3. **Try the Quick Start**
   - Instructions:
     ```bash
     # Install globally
     npm install -g claude-flow@alpha

     # Initialize project
     npx claude-flow@alpha init --wizard

     # Check system health
     npx claude-flow@alpha doctor

     # List available agents
     npx claude-flow@alpha agent list
     ```
   - Expected outcome: See agent list with 60+ types, doctor shows green checks

**Checkpoint:** Can you explain what Claude-Flow does in one sentence?

> Claude-Flow transforms Claude Code into a coordinated swarm of 60+ specialized agents with self-learning, fault-tolerant consensus, and 175+ MCP tools.

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Swarm Topologies**
   - What it is: Organizational patterns for multi-agent coordination
   - Why it matters: Right topology prevents drift and optimizes coordination
   - Topologies:
     - `hierarchical` - Queen controls workers, prevents drift
     - `mesh` - Fully connected peer network, high redundancy
     - `ring` - Sequential processing pipeline
     - `star` - Hub-and-spoke pattern
     - `hierarchical-mesh` - Hybrid (recommended for coding)
   - Code example:
   ```javascript
   // Anti-drift coding swarm configuration
   mcp__claude-flow__swarm_init({
     topology: "hierarchical",  // Single coordinator
     maxAgents: 8,              // Smaller = less drift
     strategy: "specialized"    // Clear role boundaries
   })
   ```

2. **Deep Dive: 3-Tier Model Routing**
   - What it is: Automatic task classification to optimal handler
   - Why it matters: 75% cost reduction, 2.5x Claude Max extension
   - Tiers:
     | Tier | Handler | Latency | Cost | Use Cases |
     |------|---------|---------|------|-----------|
     | 1 | Agent Booster (WASM) | <1ms | $0 | var->const, add-types, remove-console |
     | 2 | Haiku/Sonnet | ~500ms | $0.0002-0.003 | Bug fixes, refactoring |
     | 3 | Opus | 2-5s | $0.015 | Architecture, security |
   - Detection signals:
     ```bash
     # Hook output shows routing recommendation
     [AGENT_BOOSTER_AVAILABLE] Intent: var-to-const
     [TASK_MODEL_RECOMMENDATION] Use model="haiku"
     ```

3. **Deep Dive: Anti-Drift Defaults**
   - What it is: Configuration preventing multi-agent goal divergence
   - Why it matters: Long-running swarms maintain focus
   - Key settings:
     - `topology: hierarchical` - Coordinator validates outputs
     - `maxAgents: 6-8` - Smaller team, easier alignment
     - `strategy: specialized` - Clear boundaries
     - `consensus: raft` - Leader maintains authoritative state
   - Agent routing by task type:
     | Code | Task | Agents |
     |------|------|--------|
     | 1 | Bug Fix | coordinator, researcher, coder, tester |
     | 3 | Feature | coordinator, architect, coder, tester, reviewer |
     | 5 | Refactor | coordinator, architect, coder, reviewer |
     | 9 | Security | coordinator, security-architect, auditor |

4. **Hands-on Exercise: Initialize Swarm**
   - Task: Set up and run your first coordinated swarm
   - Steps:
     1. Initialize project: `npx claude-flow@alpha init`
     2. Add MCP server: `claude mcp add claude-flow -- npx claude-flow@alpha mcp start`
     3. Verify MCP: `claude mcp list`
     4. In Claude Code, run: `swarm_init` with anti-drift config
     5. Spawn agents using Task tool in parallel
   - Success criteria: See agents coordinating via memory hooks

**Checkpoint:** Can you configure an anti-drift swarm for a refactoring task?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: SONA Self-Learning**
   - When to use: Projects benefiting from learned patterns
   - Implementation:
     ```bash
     # Enable learning hooks
     npx claude-flow@v3alpha hooks pretrain --model-type moe --epochs 10

     # Post-task stores patterns
     npx claude-flow@v3alpha hooks post-task --task-id "123" --success true

     # Routing learns from success rates
     npx claude-flow@v3alpha hooks route --task "auth implementation"
     ```
   - Intelligence pipeline: RETRIEVE -> JUDGE -> DISTILL -> CONSOLIDATE
   - Pitfalls: Requires warm-up period; don't expect immediate learning

2. **Pattern: Hive Mind Consensus**
   - When to use: Critical decisions requiring multi-agent agreement
   - Implementation:
     ```bash
     # Initialize hive mind with Byzantine consensus
     npx claude-flow hive-mind init
     npx claude-flow hive-mind spawn "Design API schema" \
       --queen-type strategic \
       --consensus byzantine

     # Check consensus status
     npx claude-flow hive-mind status
     ```
   - Consensus algorithms:
     - `byzantine` - Tolerates 1/3 faulty agents
     - `raft` - Leader-based, strong consistency
     - `gossip` - Eventually consistent, partition tolerant
     - `crdt` - Conflict-free replicated data types

3. **Pattern: Background Workers**
   - When to use: Automating optimization, security, test coverage
   - Implementation:
     ```bash
     # Start daemon
     npx claude-flow@v3alpha daemon start

     # Dispatch specific worker
     npx claude-flow@v3alpha worker dispatch --trigger audit --context "./src"

     # Check worker status
     npx claude-flow@v3alpha worker status
     ```
   - Auto-triggers:
     | Worker | Triggers On |
     |--------|-------------|
     | `audit` | Security-related file changes |
     | `testgaps` | Code changes without tests |
     | `optimize` | Slow operations detected |
     | `document` | New functions/classes created |

4. **Real-World Exercise: Enterprise Feature Implementation**
   - Scenario: Implement user authentication with OAuth2 across 10+ files
   - Challenge: Configure swarm, spawn agents, coordinate via consensus, verify no drift
   - Hints:
     1. Use anti-drift config with hierarchical topology
     2. Spawn: coordinator, security-architect, coder, tester, reviewer
     3. Enable post-task hooks for pattern learning
     4. Check swarm status periodically
     5. Use claims system for human-agent handoff

**Checkpoint:** Can you implement a complex feature using a Byzantine-consensus swarm without goal drift?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| Swarm | Coordinated group of AI agents working together | 8-agent hierarchical swarm for refactoring |
| Queen | Coordinator agent in hierarchical topology | Strategic queen for planning, tactical for execution |
| Anti-Drift | Configuration preventing goal divergence | Hierarchical + specialized + raft |
| SONA | Self-Optimizing Neural Architecture | <0.05ms adaptation to new patterns |
| HNSW | Hierarchical Navigable Small World graph | 150x faster vector search |
| EWC++ | Elastic Weight Consolidation | Prevents forgetting learned patterns |
| Agent Booster | WASM-based transform handler | var->const in <1ms |
| Claims | Work ownership between human and agents | Claim/release/handoff protocols |
| MCP | Model Context Protocol | 175+ tools for orchestration |
| Consensus | Agreement protocol among agents | Byzantine (2/3 majority), Raft (leader) |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Spawning Too Many Agents

**What happens:** Coordination overhead exceeds benefit; drift increases

**Why it happens:** Assumption that more agents = better performance

**How to avoid:** Follow anti-drift defaults: maxAgents 6-8 for coding tasks

**How to fix:** Reduce agent count, use hierarchical topology

---

### Mistake 2: Using Mesh Topology for Complex Tasks

**What happens:** No central coordination leads to conflicting outputs

**Why it happens:** Mesh is collaborative but lacks authority structure

**How to avoid:** Use hierarchical or hierarchical-mesh for coding; mesh only for research

**How to fix:** Switch topology, assign coordinator agent

---

### Mistake 3: Ignoring Pre-Task Hook Signals

**What happens:** Expensive LLM calls for simple transforms

**Why it happens:** Not checking for `[AGENT_BOOSTER_AVAILABLE]` signals

**How to avoid:** Always run pre-task hook; use Edit directly when Agent Booster available

**How to fix:** Add pre-task analysis to workflow

---

### Mistake 4: Not Persisting Session State

**What happens:** Context lost between sessions; patterns not learned

**Why it happens:** Skipping session-start and session-end hooks

**How to avoid:** Always wrap work in session lifecycle:
```bash
npx claude-flow@v3alpha hooks session-start --session-id "my-feature"
# ... work ...
npx claude-flow@v3alpha hooks session-end --export-metrics true
```

---

## Practice Exercises

### Exercise 1: Basic Swarm Setup (Beginner)

**Objective:** Initialize and run a simple agent swarm

**Instructions:**
1. Install Claude-Flow: `npm install -g claude-flow@alpha`
2. Initialize project: `npx claude-flow@alpha init --wizard`
3. Add MCP server: `claude mcp add claude-flow -- npx claude-flow@alpha mcp start`
4. Run doctor: `npx claude-flow@alpha doctor`
5. In Claude Code, spawn 3 agents using Task tool

**Solution:** Successfully see 3 agents working in parallel

---

### Exercise 2: Anti-Drift Refactoring (Intermediate)

**Objective:** Refactor a module using coordinated swarm without drift

**Instructions:**
1. Configure anti-drift swarm (hierarchical, 6 agents, specialized)
2. Spawn: coordinator, architect, coder, reviewer, tester
3. Enable post-task hooks
4. Monitor swarm status during execution
5. Verify all agents stayed aligned to original goal

**Success criteria:** Refactoring complete, no conflicting outputs, tests pass

---

### Exercise 3: Self-Learning Optimization (Advanced)

**Objective:** Set up learning pipeline and observe routing improvement

**Challenge:**
1. Enable SONA learning
2. Run 10 similar tasks
3. Observe routing decisions improve over time
4. Measure cost savings from learned patterns

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Swarm coordination patterns | Any multi-agent AI system (CrewAI, AutoGen, LangGraph) |
| Consensus algorithms | Distributed systems, blockchain, microservices |
| Anti-drift configuration | Long-running autonomous pipelines |
| 3-tier routing | Cost optimization in any API-heavy system |
| MCP integration | Claude Desktop, VS Code Copilot, other MCP clients |
| Vector memory (HNSW) | RAG systems, semantic search, embeddings |

---

## Study Resources

### Essential Reading

1. **Repository README** - Comprehensive but dense; focus on Quick Start and Architecture sections
2. **CLAUDE.md** - Integration rules for Claude Code; essential for proper usage
3. **v3/index.ts** - Module architecture and ADR documentation

### Supplementary Materials

- Anthropic MCP documentation: https://modelcontextprotocol.io
- HNSW paper: "Efficient and robust approximate nearest neighbor search using HNSW"
- Raft consensus paper: "In Search of an Understandable Consensus Algorithm"
- Byzantine fault tolerance: PBFT paper by Castro and Liskov

### Community Resources

- Agentics Foundation Discord
- GitHub Issues for Q&A
- Author's Twitter: @ruv

---

## Self-Assessment

### Quiz Yourself

1. What problem does Claude-Flow solve that Claude Code alone cannot?
   > Coordinated multi-agent orchestration with shared memory, consensus, and self-learning

2. How does anti-drift configuration work?
   > Hierarchical topology + specialized strategy + raft consensus + maxAgents 6-8

3. When would you use Agent Booster instead of spawning an agent?
   > Simple transforms like var->const, add-types, remove-console (Tier 1 tasks)

4. What are the main trade-offs of Claude-Flow?
   > Power vs complexity; enterprise features vs setup overhead; Node.js only

### Practical Assessment

Build: A coordinated swarm that implements a new feature with tests and documentation

Success criteria:
- [ ] Anti-drift configuration active
- [ ] 5+ agents spawned in parallel
- [ ] Post-task hooks storing patterns
- [ ] Swarm stays aligned to original goal
- [ ] Feature implemented with tests passing
- [ ] Session state persisted for future learning

---

## What's Next?

After mastering Claude-Flow, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for adaptation ideas
2. **Related Frameworks:** Study CrewAI, AutoGen, LangGraph for comparison
3. **Advanced Topics:**
   - Byzantine fault tolerance in depth
   - HNSW indexing optimization
   - EWC++ for catastrophic forgetting prevention
   - Plugin development for Claude-Flow

---

*Learning guide created: 2026-02-03 | For: Claude-Flow v3*
