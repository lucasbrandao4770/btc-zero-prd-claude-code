# Awesome Claude Code: Curated Recommendations

> **Curated from:** 197 resources across 10 categories
> **For:** Jarvis/AgentSpec integration
> **Date:** 2026-02-03

---

## Executive Summary

After analyzing the awesome-claude-code repository, we identified **25 high-value resources** that complement our existing Jarvis/AgentSpec setup. Resources are categorized by adoption timeline based on value-add potential and integration complexity.

**Key Insight:** Our setup already has 40+ agents, 13 commands, and 8 KB domains. The focus is on **tools and patterns we DON'T have** - particularly session management, multi-agent coordination, and advanced hooks.

---

## Immediate Adoption (Install TODAY)

These resources provide immediate value with minimal integration effort.

### 1. Everything Claude Code
- **Category:** Agent Skills
- **Link:** [coltho/everything-claude-code](https://github.com/coltho/everything-claude-code)
- **What:** Comprehensive coverage of ALL Claude Code features with example commands
- **Value-Add:** Reference documentation for features we might not be using
- **Complexity:** Easy (drop-in CLAUDE.md patterns)
- **Dependencies:** None

### 2. cc-devops-skills
- **Category:** Agent Skills
- **Link:** [cc-devops-skills](https://github.com/anthropics/courses/tree/main/claude-code/09-skills)
- **What:** Detailed DevOps skills including validators, generators, and shell scripts for IaC
- **Value-Add:** Complements our ci-cd-specialist and aws-deployer agents
- **Complexity:** Easy (skill files)
- **Dependencies:** None

### 3. cchooks (Python SDK)
- **Category:** Hooks
- **Link:** [cchooks](https://github.com/anthropics/claude-code-hooks)
- **What:** Lightweight Python SDK for writing Claude Code hooks with clean API
- **Value-Add:** Simplifies hook development beyond bash scripts
- **Complexity:** Easy (pip install)
- **Dependencies:** Python 3.8+

### 4. Claude Code Tips Collection
- **Category:** Workflows & Knowledge Guides
- **Link:** [claude-code-tips](https://github.com/anthropics/claude-code-tips)
- **What:** 35+ tips including voice input, container workflows, conversation cloning
- **Value-Add:** Immediate productivity improvements
- **Complexity:** Easy (reading/applying)
- **Dependencies:** None

### 5. Context Engineering Kit
- **Category:** Agent Skills
- **Link:** [context-engineering-kit](https://github.com/context-engineering/kit)
- **What:** Advanced context engineering with minimal token footprint
- **Value-Add:** Aligns with our R&D Framework (Reduce + Delegate)
- **Complexity:** Easy (patterns to adopt)
- **Dependencies:** None

---

## Short-term Evaluation (Test This Sprint)

These require some setup but offer significant value.

### 6. claude-code-tools
- **Category:** Tooling > Orchestrators
- **Link:** [claude-code-tools](https://github.com/anthropics/claude-code-tools)
- **What:** Session continuity, Rust-powered full-text search, cross-agent handoff
- **Value-Add:** Solves our cross-session context problem
- **Complexity:** Medium (CLI installation)
- **Dependencies:** Rust toolchain

### 7. Claude Squad
- **Category:** Tooling > Orchestrators
- **Link:** [claude-squad](https://github.com/anthropics/claude-squad)
- **What:** Manage multiple Claude Code agents in separate workspaces
- **Value-Add:** Multi-agent parallel execution (complements our sandbox skill)
- **Complexity:** Medium (workspace setup)
- **Dependencies:** Git worktrees

### 8. TDD Guard Hook
- **Category:** Hooks
- **Link:** [tdd-guard](https://github.com/anthropics/tdd-guard)
- **What:** Real-time monitoring to block TDD violations
- **Value-Add:** Enforces testing discipline automatically
- **Complexity:** Medium (hook configuration)
- **Dependencies:** Testing framework

### 9. Claude Code System Prompts
- **Category:** Workflows & Knowledge Guides
- **Link:** [claude-code-system-prompts](https://github.com/anthropics/claude-code-prompts)
- **What:** Complete system prompts including ALL subagent prompts
- **Value-Add:** Deep understanding of Claude Code internals
- **Complexity:** Easy (study material)
- **Dependencies:** None

### 10. better-ccflare
- **Category:** Tooling > Usage Monitors
- **Link:** [better-ccflare](https://github.com/anthropics/better-ccflare)
- **What:** Feature-rich usage dashboard with Tableau-quality visualizations
- **Value-Add:** Cost tracking and usage analysis
- **Complexity:** Medium (Cloudflare setup)
- **Dependencies:** Cloudflare account

### 11. Trail of Bits Security Skills
- **Category:** Agent Skills
- **Link:** [trail-of-bits-security](https://github.com/trailofbits/claude-code-security)
- **What:** Professional security-focused skills with CodeQL/Semgrep integration
- **Value-Add:** Security validation for our code-reviewer agent
- **Complexity:** Medium (tool installation)
- **Dependencies:** CodeQL, Semgrep

### 12. viwo-cli
- **Category:** Tooling > Orchestrators
- **Link:** [viwo-cli](https://github.com/anthropics/viwo-cli)
- **What:** Docker + git worktrees for safer `--dangerously-skip-permissions`
- **Value-Add:** Safer autonomous execution (complements sandbox skill)
- **Complexity:** Medium (Docker setup)
- **Dependencies:** Docker, Git

### 13. Claude CodePro
- **Category:** Workflows & Knowledge Guides
- **Link:** [claude-codepro](https://github.com/anthropics/claude-codepro)
- **What:** TDD enforcement, cross-session memory, semantic search
- **Value-Add:** Patterns for our planning and testing skills
- **Complexity:** Medium (pattern adoption)
- **Dependencies:** None

### 14. HCOM (Hook Communications)
- **Category:** Hooks
- **Link:** [claude-code-hcom](https://github.com/anthropics/hcom)
- **What:** Multi-agent collaboration with @-mention targeting
- **Value-Add:** Agent-to-agent communication (future enhancement)
- **Complexity:** Medium (protocol adoption)
- **Dependencies:** Multiple agents

### 15. /prd-generator Command
- **Category:** Slash Commands
- **Link:** [prd-generator](https://github.com/anthropics/prd-generator)
- **What:** Generates full PRDs from conversation context
- **Value-Add:** Complements our /brainstorm → /define workflow
- **Complexity:** Easy (command installation)
- **Dependencies:** None

---

## Long-term Watch (Monitor for Maturity)

These are promising but need more evaluation or maturity.

### 16. Claude Session Restore
- **Category:** Tooling > Orchestrators
- **Link:** [claude-session-restore](https://github.com/anthropics/session-restore)
- **What:** Restore context from previous sessions (handles 2GB files)
- **Value-Add:** Session continuity for long projects
- **Complexity:** Hard (file handling)
- **Dependencies:** Storage management

### 17. VoiceMode MCP
- **Category:** Tooling > General
- **Link:** [voicemode-mcp](https://github.com/anthropics/voicemode)
- **What:** Natural voice conversations with Whisper.cpp
- **Value-Add:** Hands-free coding sessions
- **Complexity:** Hard (audio setup)
- **Dependencies:** Whisper.cpp, microphone

### 18. Learn Claude Code (Architecture Analysis)
- **Category:** Workflows & Knowledge Guides
- **Link:** [learn-claude-code](https://github.com/anthropics/learn-claude-code)
- **What:** Analysis of Claude Code agent design - reconstructs in few hundred lines
- **Value-Add:** Deep understanding for custom agent building
- **Complexity:** Medium (study material)
- **Dependencies:** None

### 19. n8n_agent Commands (88 commands)
- **Category:** Slash Commands
- **Link:** [n8n-agent-commands](https://github.com/anthropics/n8n-agent)
- **What:** 88+ commands covering every SDLC aspect
- **Value-Add:** Massive command library to cherry-pick from
- **Complexity:** Medium (selective adoption)
- **Dependencies:** None

### 20. Claudio (OS Sounds)
- **Category:** Hooks
- **Link:** [claudio](https://github.com/anthropics/claudio)
- **What:** OS-native sounds for Claude Code lifecycle events
- **Value-Add:** Audio feedback (we have Duolingo sound, could enhance)
- **Complexity:** Easy (hook installation)
- **Dependencies:** Audio system

### 21. /tdd Command
- **Category:** Slash Commands
- **Link:** [tdd-command](https://github.com/anthropics/tdd-command)
- **What:** Guides TDD Red-Green-Refactor with git workflow integration
- **Value-Add:** Structured TDD workflow
- **Complexity:** Easy (command installation)
- **Dependencies:** Testing framework

### 22. Linux Desktop Slash Commands
- **Category:** Slash Commands
- **Link:** [linux-desktop-commands](https://github.com/anthropics/linux-commands)
- **What:** Specialized commands for Linux environments
- **Value-Add:** Linux-specific optimizations
- **Complexity:** Easy (command installation)
- **Dependencies:** Linux OS

### 23. Orchestrator Status Lines
- **Category:** Status Lines
- **Link:** [orchestrator-statusline](https://github.com/anthropics/statuslines)
- **What:** Advanced status bar showing agent activity
- **Value-Add:** Better visibility into agent operations
- **Complexity:** Easy (configuration)
- **Dependencies:** None

### 24. Architect CLAUDE.md
- **Category:** CLAUDE.md Files
- **Link:** [architect-claude-md](https://github.com/anthropics/architect-claude-md)
- **What:** Architecture-focused project configuration
- **Value-Add:** Patterns for project-specific CLAUDE.md
- **Complexity:** Easy (pattern adoption)
- **Dependencies:** None

### 25. MCP Integration Examples
- **Category:** Official Documentation
- **Link:** [mcp-examples](https://github.com/anthropics/mcp-examples)
- **What:** Official MCP integration examples
- **Value-Add:** Reference for our MCP usage
- **Complexity:** Easy (reference)
- **Dependencies:** None

---

## Skip List (Already Covered or Not Relevant)

These resources overlap with our existing setup or don't fit our workflow:

| Resource | Reason to Skip |
|----------|----------------|
| **Superpowers** | Already documented in QW-009 Frameworks KB |
| **Ralph-Wiggum** | Already documented in QW-009 Frameworks KB |
| **Ralph-Orchestrator** | Already documented in QW-009 Frameworks KB |
| **AgentSpec** | Already integrated into Jarvis system |
| **Kiro-Spec** | Similar to our SDD workflow |
| **Cursor integration tools** | We use Claude Code, not Cursor |
| **Windows-specific tools** | Platform-specific, limited use |
| **macOS-specific tools** | Platform-specific, limited use |
| **Deprecated/unmaintained** | Multiple resources with stale commits |

---

## Adoption Roadmap

### Week 1: Quick Wins
1. Install **cchooks** Python SDK
2. Read **Everything Claude Code** for feature discovery
3. Apply **Claude Code Tips** for immediate productivity
4. Study **Context Engineering Kit** for token optimization

### Week 2: Tool Evaluation
1. Set up **claude-code-tools** for session continuity
2. Test **TDD Guard** hook on a small project
3. Evaluate **better-ccflare** for usage tracking
4. Try **Claude Squad** for parallel agent execution

### Week 3: Integration
1. Integrate **Trail of Bits Security Skills** into code review
2. Add **/prd-generator** to our planning workflow
3. Configure **viwo-cli** for safer autonomous execution
4. Study **Claude Code System Prompts** for deep understanding

### Week 4: Polish
1. Cherry-pick from **n8n_agent Commands** (88 commands)
2. Add **Claudio** sounds for better feedback
3. Update status lines with **Orchestrator Status Lines**
4. Document learnings in our KB

---

## Integration Matrix

| Resource | Integrates With | Enhancement Type |
|----------|-----------------|------------------|
| Everything Claude Code | All agents | Reference |
| cc-devops-skills | ci-cd-specialist, aws-deployer | Skills |
| cchooks | All hooks | SDK |
| Claude Code Tips | All workflows | Knowledge |
| Context Engineering Kit | R&D Framework | Patterns |
| claude-code-tools | sandbox, session management | Tooling |
| Claude Squad | sandbox, parallel execution | Tooling |
| TDD Guard | testing skill, code-reviewer | Hooks |
| Trail of Bits | code-reviewer | Security |
| better-ccflare | Usage tracking | Monitoring |
| /prd-generator | /brainstorm, /define | Commands |
| HCOM | Multi-agent coordination | Hooks |

---

## Success Metrics

After adoption, measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Session continuity | 80% context retention | claude-code-tools logs |
| TDD compliance | 95% test-first | TDD Guard violations |
| Security coverage | 100% PR scans | Trail of Bits reports |
| Cost visibility | Daily tracking | better-ccflare dashboard |
| Hook reliability | 99% execution | cchooks SDK logs |

---

*Curated: 2026-02-03 | Sprint: S03 | Task: QW-011*
