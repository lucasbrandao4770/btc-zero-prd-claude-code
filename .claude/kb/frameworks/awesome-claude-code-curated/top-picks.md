# Top 20 Picks: Detailed Analysis

> Comprehensive analysis of the 20 most valuable resources from awesome-claude-code

---

## Tier 1: Must-Have (Immediate Adoption)

### 1. Everything Claude Code
**Category:** Agent Skills | **Complexity:** Easy

A comprehensive reference covering ALL Claude Code features with example commands. This is the definitive guide to what Claude Code can do.

**Key Features:**
- Complete feature documentation
- Example commands for every capability
- Best practices and tips
- Regular updates with new features

**Value for Jarvis:**
- Reference documentation for features we might not be using
- Training material for new users
- Validation of our custom implementations

**Installation:**
```bash
# Add to CLAUDE.md or skills folder
cp everything-claude-code/skills/* .claude/skills/
```

---

### 2. cc-devops-skills
**Category:** Agent Skills | **Complexity:** Easy

Detailed DevOps skills including validators, generators, and shell scripts for Infrastructure as Code.

**Key Features:**
- Terraform validators
- Kubernetes manifest generators
- CI/CD pipeline templates
- Security scanning scripts

**Value for Jarvis:**
- Complements our ci-cd-specialist agent
- Adds IaC validation we don't have
- Shell script patterns for automation

**Installation:**
```bash
# Add skills to your setup
cp cc-devops-skills/*.md .claude/skills/devops/
```

---

### 3. cchooks (Python SDK)
**Category:** Hooks | **Complexity:** Easy

Lightweight Python SDK for writing Claude Code hooks with a clean, Pythonic API.

**Key Features:**
- Decorator-based hook definitions
- Type hints throughout
- Easy testing support
- Lifecycle event handling

**Value for Jarvis:**
- Simplifies hook development beyond bash scripts
- Better error handling
- Testable hook code

**Installation:**
```bash
pip install cchooks
# Then define hooks in Python
```

**Example:**
```python
from cchooks import hook, HookType

@hook(HookType.POST_TOOL)
def validate_security(tool_name: str, result: str) -> bool:
    if "password" in result.lower():
        return False  # Block sensitive data
    return True
```

---

### 4. Claude Code Tips Collection
**Category:** Workflows & Knowledge Guides | **Complexity:** Easy

35+ tips for Claude Code productivity including voice input, container workflows, and conversation cloning.

**Key Features:**
- Voice input setup
- Container-based development
- Conversation cloning for parallel work
- Memory management tips
- Context optimization techniques

**Value for Jarvis:**
- Immediate productivity improvements
- Patterns we can document in our KB
- User training material

**Installation:**
```bash
# Read and apply relevant tips
# No installation needed - knowledge resource
```

---

### 5. Context Engineering Kit
**Category:** Agent Skills | **Complexity:** Easy

Advanced context engineering with minimal token footprint. Provides patterns for efficient context management.

**Key Features:**
- Token-efficient prompting patterns
- Context compression techniques
- Memory management strategies
- Progressive disclosure patterns

**Value for Jarvis:**
- Aligns with our R&D Framework (Reduce + Delegate)
- Improves context window utilization
- Reduces costs through efficiency

**Installation:**
```bash
# Adopt patterns into CLAUDE.md
# Study and apply techniques
```

---

## Tier 2: High Value (Short-term Evaluation)

### 6. claude-code-tools
**Category:** Tooling > Orchestrators | **Complexity:** Medium

Session continuity tool with Rust-powered full-text search and cross-agent handoff capabilities.

**Key Features:**
- Session state persistence
- Full-text search across sessions
- Cross-agent context sharing
- Rust performance

**Value for Jarvis:**
- Solves cross-session context problem
- Enables multi-session workflows
- Search through past conversations

**Installation:**
```bash
cargo install claude-code-tools
# Configure for your workflow
```

---

### 7. Claude Squad
**Category:** Tooling > Orchestrators | **Complexity:** Medium

Manage multiple Claude Code agents in separate workspaces using git worktrees.

**Key Features:**
- Multi-agent orchestration
- Workspace isolation
- Parallel task execution
- Agent communication

**Value for Jarvis:**
- Complements our sandbox skill
- Enables parallel development
- Safer multi-agent execution

**Installation:**
```bash
# Requires git worktrees setup
npm install -g claude-squad
claude-squad init
```

---

### 8. TDD Guard Hook
**Category:** Hooks | **Complexity:** Medium

Real-time monitoring to block TDD violations. Ensures test-first development discipline.

**Key Features:**
- Monitors file changes
- Blocks code without tests
- Configurable rules
- CI integration

**Value for Jarvis:**
- Enforces testing discipline automatically
- Complements our testing skill
- Quality gate for development

**Installation:**
```bash
# Add to hooks configuration
cp tdd-guard/* .claude/hooks/
```

---

### 9. Claude Code System Prompts
**Category:** Workflows & Knowledge Guides | **Complexity:** Easy

Complete system prompts including ALL subagent prompts. Deep understanding of Claude Code internals.

**Key Features:**
- Main agent prompt
- Subagent prompts (Plan, Explore, etc.)
- Tool definitions
- Behavior guidelines

**Value for Jarvis:**
- Deep understanding for custom agent building
- Reference for prompt engineering
- Validation of our assumptions

**Installation:**
```bash
# Study material - no installation
# Reference when building agents
```

---

### 10. better-ccflare
**Category:** Tooling > Usage Monitors | **Complexity:** Medium

Feature-rich usage dashboard with Tableau-quality visualizations.

**Key Features:**
- Real-time usage tracking
- Cost analysis
- Token consumption graphs
- Historical trends

**Value for Jarvis:**
- Cost visibility and tracking
- Usage optimization insights
- Budget management

**Installation:**
```bash
# Requires Cloudflare setup
# Follow deployment guide
```

---

### 11. Trail of Bits Security Skills
**Category:** Agent Skills | **Complexity:** Medium

Professional security-focused skills with CodeQL and Semgrep integration.

**Key Features:**
- CodeQL query integration
- Semgrep rule application
- Vulnerability detection
- Security best practices

**Value for Jarvis:**
- Security validation for code-reviewer agent
- Automated vulnerability scanning
- Professional security patterns

**Installation:**
```bash
# Install CodeQL and Semgrep first
brew install codeql semgrep
# Then add skills
cp trail-of-bits-skills/* .claude/skills/security/
```

---

### 12. viwo-cli
**Category:** Tooling > Orchestrators | **Complexity:** Medium

Docker + git worktrees for safer `--dangerously-skip-permissions` execution.

**Key Features:**
- Docker isolation
- Git worktree management
- Safe permission skipping
- Rollback support

**Value for Jarvis:**
- Safer autonomous execution
- Complements sandbox skill
- Production-safe YOLO mode

**Installation:**
```bash
npm install -g viwo-cli
viwo init
```

---

### 13. Claude CodePro
**Category:** Workflows & Knowledge Guides | **Complexity:** Medium

TDD enforcement, cross-session memory, and semantic search capabilities.

**Key Features:**
- TDD workflow enforcement
- Memory persistence
- Semantic code search
- Quality gates

**Value for Jarvis:**
- Patterns for planning and testing skills
- Memory management insights
- Quality enforcement patterns

**Installation:**
```bash
# Pattern adoption - study and apply
# No direct installation
```

---

### 14. HCOM (Hook Communications)
**Category:** Hooks | **Complexity:** Medium

Multi-agent collaboration with @-mention targeting for agent-to-agent communication.

**Key Features:**
- @-mention agent targeting
- Message passing between agents
- Coordination protocols
- Event broadcasting

**Value for Jarvis:**
- Future multi-agent enhancement
- Agent collaboration patterns
- Communication protocols

**Installation:**
```bash
# Add HCOM hooks
cp hcom/* .claude/hooks/
# Configure agent registry
```

---

### 15. /prd-generator Command
**Category:** Slash Commands | **Complexity:** Easy

Generates full PRDs from conversation context.

**Key Features:**
- Context extraction
- PRD template filling
- Requirement organization
- Stakeholder sections

**Value for Jarvis:**
- Complements /brainstorm → /define workflow
- Faster PRD creation
- Consistent format

**Installation:**
```bash
cp prd-generator.md .claude/commands/
```

---

## Tier 3: Watch List (Long-term Evaluation)

### 16. Claude Session Restore
**Category:** Tooling | **Complexity:** Hard

Restore context from previous sessions, handling files up to 2GB.

**Value:** Session continuity for long projects. Watch for stability improvements.

---

### 17. VoiceMode MCP
**Category:** Tooling | **Complexity:** Hard

Natural voice conversations with Whisper.cpp integration.

**Value:** Hands-free coding sessions. Wait for easier setup.

---

### 18. Learn Claude Code
**Category:** Workflows | **Complexity:** Medium

Architecture analysis that reconstructs Claude Code in few hundred lines.

**Value:** Deep understanding for custom agent building. Study material.

---

### 19. n8n_agent Commands
**Category:** Slash Commands | **Complexity:** Medium

88+ commands covering every SDLC aspect.

**Value:** Massive command library to cherry-pick from selectively.

---

### 20. Claudio
**Category:** Hooks | **Complexity:** Easy

OS-native sounds for Claude Code lifecycle events.

**Value:** Audio feedback enhancement. Easy to try.

---

## Quick Reference Table

| Rank | Resource | Category | Complexity | Week |
|------|----------|----------|------------|------|
| 1 | Everything Claude Code | Skills | Easy | 1 |
| 2 | cc-devops-skills | Skills | Easy | 1 |
| 3 | cchooks | Hooks | Easy | 1 |
| 4 | Claude Code Tips | Guides | Easy | 1 |
| 5 | Context Engineering Kit | Skills | Easy | 1 |
| 6 | claude-code-tools | Tooling | Medium | 2 |
| 7 | Claude Squad | Tooling | Medium | 2 |
| 8 | TDD Guard | Hooks | Medium | 2 |
| 9 | System Prompts | Guides | Easy | 2 |
| 10 | better-ccflare | Tooling | Medium | 2 |
| 11 | Trail of Bits | Skills | Medium | 2 |
| 12 | viwo-cli | Tooling | Medium | 3 |
| 13 | Claude CodePro | Guides | Medium | 3 |
| 14 | HCOM | Hooks | Medium | 3 |
| 15 | /prd-generator | Commands | Easy | 3 |
| 16 | Session Restore | Tooling | Hard | 4+ |
| 17 | VoiceMode MCP | Tooling | Hard | 4+ |
| 18 | Learn Claude Code | Guides | Medium | 4+ |
| 19 | n8n_agent Commands | Commands | Medium | 4+ |
| 20 | Claudio | Hooks | Easy | 4+ |

---

*Curated: 2026-02-03 | Sprint: S03 | Task: QW-011*
