# Category: Agent Skills

> **Total in awesome-claude-code:** 11 resources
> **Selected for adoption:** 5 resources

---

## Overview

Agent Skills are model-controlled specialized task configurations that extend Claude Code's capabilities. Our Jarvis setup already has 40+ agents, so we're selective about what to add.

---

## Selected Resources

### 1. Everything Claude Code (ADOPT)
**Link:** [coltho/everything-claude-code](https://github.com/coltho/everything-claude-code)

Comprehensive coverage of ALL Claude Code features with example commands.

**Why Selected:**
- Reference documentation for features we might not be using
- Training material for new users
- Validates our custom implementations

**Integration:** Copy skills to `.claude/skills/reference/`

---

### 2. cc-devops-skills (ADOPT)
**Link:** [anthropics/cc-devops-skills](https://github.com/anthropics/courses/tree/main/claude-code/09-skills)

Detailed DevOps skills including validators, generators, and shell scripts for IaC.

**Why Selected:**
- Complements our ci-cd-specialist and aws-deployer agents
- Adds Terraform/K8s validation we don't have
- Shell script patterns for automation

**Integration:** Copy to `.claude/skills/devops/`

---

### 3. Trail of Bits Security Skills (ADOPT)
**Link:** [trailofbits/claude-code-security](https://github.com/trailofbits/claude-code-security)

Professional security-focused skills with CodeQL and Semgrep integration.

**Why Selected:**
- Security validation for our code-reviewer agent
- Automated vulnerability scanning
- Professional security patterns

**Integration:** Requires CodeQL/Semgrep installation first

---

### 4. Context Engineering Kit (ADOPT)
**Link:** [context-engineering/kit](https://github.com/context-engineering/kit)

Advanced context engineering with minimal token footprint.

**Why Selected:**
- Aligns with our R&D Framework (Reduce + Delegate)
- Improves context window utilization
- Reduces costs through efficiency

**Integration:** Pattern adoption into CLAUDE.md

---

### 5. Superpowers (SKIP - Already in QW-009)
**Link:** Already documented in Frameworks KB

Strong SDLC coverage with comprehensive skill set.

**Why Skipped:** Already documented in QW-009 Frameworks KB

---

## Skipped Resources

| Resource | Reason |
|----------|--------|
| Superpowers | Already in QW-009 |
| AgentSpec | Already integrated |
| Basic skill collections | Duplicates our agents |
| Platform-specific skills | Limited cross-platform use |

---

## Integration with Existing Agents

| New Skill | Enhances Agent |
|-----------|----------------|
| Everything Claude Code | All agents (reference) |
| cc-devops-skills | ci-cd-specialist, aws-deployer |
| Trail of Bits | code-reviewer |
| Context Engineering | All agents (efficiency) |

---

*Category Analysis: 2026-02-03*
