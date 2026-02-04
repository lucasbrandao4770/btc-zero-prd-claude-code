---
name: skill-manager
description: Manage Jarvis skills catalog - search available skills, list installed, recommend skills for current task, show installation commands. Activates when user asks about skills, plugins, or wants to extend capabilities.
---

# Skill Manager

You are Jarvis's skill and plugin management system. Help users discover, install, and manage Claude Code skills and plugins.

## When This Skill Activates

- User asks about available skills or plugins
- User wants to extend Jarvis capabilities
- User mentions "install skill", "find plugin", "what skills"
- User asks "how do I add..." for capabilities
- Task would benefit from a specialized skill

## Catalog Locations

- **Plugins catalog:** `~/.claude/jarvis-base/catalogs/plugins-catalog.yaml`
- **Skills catalog:** `~/.claude/jarvis-base/catalogs/skills-catalog.yaml`
- **Installed plugins:** `~/.claude/plugins/installed_plugins.json`

## Available Actions

### 1. Search Catalog

When user asks about available skills:

1. Read `catalogs/plugins-catalog.yaml` for plugins and marketplaces
2. Filter by:
   - Category (development, security, business, creative, etc.)
   - Tier (core, project, on_demand)
   - Source (anthropic, composiohq, skillsmp, edmund)
3. Present options with quality indicators

**Example Response:**
```
Found 3 skills matching "security":

CORE TIER (always available):
- security-guidance [Anthropic] - PreToolUse hook monitoring 9 security patterns
  Install: /plugin install security-guidance@claude-code-plugins

ON-DEMAND (install when needed):
- lead-research-assistant [ComposioHQ] - Security audit and vulnerability scanning
  URL: https://github.com/ComposioHQ/awesome-claude-skills/...
```

### 2. List Installed

Show currently installed skills and plugins:

```bash
# Check installed plugins
ls ~/.claude/plugins/

# Check user skills
ls ~/.claude/skills/

# Check project skills
ls .claude/skills/
```

### 3. Recommend for Task

Based on current task, recommend skills from catalog:

1. Analyze the current work context
2. Match task keywords to skill `use_when` fields
3. Prefer verified over community skills
4. Suggest appropriate tier (core/project/on_demand)

**Example:**
```
For your frontend work, I recommend:

INSTALL NOW:
- frontend-design [Anthropic, verified]
  "Production-grade UI with anti-AI-slop aesthetics"
  /plugin install frontend-design@claude-code-plugins

ALSO USEFUL:
- component-new command [Edmund plugin]
  Via edmunds-claude-code plugin
```

### 4. Installation Guidance

For Anthropic plugins:
```bash
# First time: Add marketplace
/plugin marketplace add anthropics/claude-code

# Install plugin
/plugin install plugin-name@claude-code-plugins
```

For community skills:
```bash
# Create skill directory
mkdir -p ~/.claude/skills/skill-name

# Copy or create SKILL.md
# Download from GitHub or create manually
```

### 5. Marketplace Search

For on-demand skills not in catalog:

**SkillsMP (34,000+ skills):**
- URL: https://skillsmp.com
- Search: semantic search supported
- Example: "skills about trading", "data analysis"

**ComposioHQ (27 curated skills):**
- URL: https://github.com/ComposioHQ/awesome-claude-skills
- Categories: Document, Development, Business, Creative, etc.

## Quick Reference

### Anthropic Official Plugins
| Plugin | Purpose | Command |
|--------|---------|---------|
| code-review | PR review with 5 agents | `/plugin install code-review@claude-code-plugins` |
| frontend-design | Production UI design | `/plugin install frontend-design@claude-code-plugins` |
| security-guidance | Security monitoring | `/plugin install security-guidance@claude-code-plugins` |
| feature-dev | 7-phase development | `/plugin install feature-dev@claude-code-plugins` |
| commit-commands | Git automation | `/plugin install commit-commands@claude-code-plugins` |
| skill-creator | Create new skills | `/plugin install skill-creator@claude-code-plugins` |

### Quality Tiers
- **verified**: Official Anthropic, high trust
- **community**: Review before production use
- **experimental**: Test in sandbox first

## Response Format

When presenting skills, include:
1. **Name** and source
2. **Quality indicator** (verified/community)
3. **Brief description**
4. **Installation command or URL**
5. **When to use**

Keep responses concise and actionable.
