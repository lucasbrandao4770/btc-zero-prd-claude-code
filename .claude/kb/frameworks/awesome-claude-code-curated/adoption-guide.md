# Adoption Guide: Step-by-Step Installation

> Concrete steps to adopt each recommended resource into your Jarvis/AgentSpec setup

---

## Prerequisites

Before adopting any resources, ensure you have:

```bash
# Python 3.11+ for hooks
python --version

# Node.js for some tools
node --version

# Rust for claude-code-tools (optional)
rustc --version

# Docker for viwo-cli (optional)
docker --version
```

---

## Week 1: Quick Wins

### 1. Everything Claude Code (15 min)

```bash
# Clone or download the repository
git clone https://github.com/coltho/everything-claude-code.git /tmp/ecc

# Review the skills
ls /tmp/ecc/skills/

# Copy relevant skills to your setup
cp /tmp/ecc/skills/*.md .claude/skills/reference/

# Add to your CLAUDE.md
cat >> CLAUDE.md << 'EOF'

## Reference Skills
See `.claude/skills/reference/` for comprehensive Claude Code feature documentation.
EOF
```

**Verification:**
```bash
# Skills should be accessible
ls .claude/skills/reference/
```

---

### 2. cc-devops-skills (15 min)

```bash
# Clone the repository
git clone https://github.com/anthropics/cc-devops-skills.git /tmp/devops

# Copy DevOps skills
mkdir -p .claude/skills/devops
cp /tmp/devops/skills/*.md .claude/skills/devops/

# Update skills index
cat >> .claude/skills/index.md << 'EOF'

## DevOps Skills
- terraform-validator: Validate Terraform configurations
- k8s-generator: Generate Kubernetes manifests
- cicd-templates: CI/CD pipeline templates
EOF
```

**Verification:**
```bash
# DevOps skills available
ls .claude/skills/devops/
```

---

### 3. cchooks Python SDK (20 min)

```bash
# Install the SDK
pip install cchooks

# Create hooks directory if not exists
mkdir -p .claude/hooks

# Create a sample hook
cat > .claude/hooks/security_check.py << 'EOF'
from cchooks import hook, HookType

@hook(HookType.POST_TOOL)
def check_sensitive_data(tool_name: str, result: str) -> bool:
    """Block output containing sensitive patterns."""
    sensitive_patterns = ['password', 'api_key', 'secret', 'token']
    result_lower = result.lower()

    for pattern in sensitive_patterns:
        if pattern in result_lower:
            print(f"[SECURITY] Blocked: {pattern} found in output")
            return False
    return True
EOF

# Register the hook
cchooks register .claude/hooks/security_check.py
```

**Verification:**
```bash
# Hook should be registered
cchooks list
```

---

### 4. Claude Code Tips (10 min)

```bash
# Clone the tips repository
git clone https://github.com/anthropics/claude-code-tips.git /tmp/tips

# Create a tips summary in your KB
mkdir -p .claude/kb/claude-code-tips
cp /tmp/tips/README.md .claude/kb/claude-code-tips/index.md

# Add key tips to your CLAUDE.md
cat >> CLAUDE.md << 'EOF'

## Quick Tips (from claude-code-tips)
- Use `/compact` to reduce context usage
- Use `--resume` to continue previous sessions
- Use voice input with Whisper for hands-free coding
- Clone conversations for parallel exploration
EOF
```

**Verification:**
```bash
# Tips KB created
cat .claude/kb/claude-code-tips/index.md | head -20
```

---

### 5. Context Engineering Kit (15 min)

```bash
# Clone the kit
git clone https://github.com/context-engineering/kit.git /tmp/context-kit

# Review patterns
ls /tmp/context-kit/patterns/

# Copy relevant patterns
mkdir -p .claude/kb/context-engineering
cp /tmp/context-kit/patterns/*.md .claude/kb/context-engineering/

# Add to R&D Framework section in CLAUDE.md
cat >> CLAUDE.md << 'EOF'

## Context Engineering Patterns
See `.claude/kb/context-engineering/` for advanced patterns:
- Token compression techniques
- Progressive disclosure
- Memory management strategies
EOF
```

**Verification:**
```bash
# Patterns available
ls .claude/kb/context-engineering/
```

---

## Week 2: Tool Evaluation

### 6. claude-code-tools (30 min)

```bash
# Install via cargo (requires Rust)
cargo install claude-code-tools

# Or via npm if available
npm install -g claude-code-tools

# Initialize in your project
claude-code-tools init

# Configure session persistence
cat > .claude-code-tools.yaml << 'EOF'
persistence:
  enabled: true
  path: .claude/sessions/
search:
  enabled: true
  index_path: .claude/search-index/
EOF
```

**Verification:**
```bash
# Tool should be available
claude-code-tools --version
claude-code-tools status
```

---

### 7. TDD Guard Hook (20 min)

```bash
# Clone TDD Guard
git clone https://github.com/anthropics/tdd-guard.git /tmp/tdd-guard

# Copy hook files
cp /tmp/tdd-guard/hooks/* .claude/hooks/

# Configure rules
cat > .claude/hooks/tdd-guard-config.yaml << 'EOF'
rules:
  require_test_first: true
  test_patterns:
    - "test_*.py"
    - "*_test.py"
    - "tests/**/*.py"
  source_patterns:
    - "src/**/*.py"
  ignore_patterns:
    - "__init__.py"
    - "conftest.py"
EOF

# Enable the hook
chmod +x .claude/hooks/tdd-guard.sh
```

**Verification:**
```bash
# Try creating a source file without test
# TDD Guard should warn/block
```

---

### 8. better-ccflare (45 min)

```bash
# Requires Cloudflare account
# Clone the dashboard
git clone https://github.com/anthropics/better-ccflare.git /tmp/ccflare

# Follow Cloudflare Workers deployment
cd /tmp/ccflare
npm install
npx wrangler login
npx wrangler publish

# Configure your API proxy
cat > wrangler.toml << 'EOF'
name = "claude-usage-dashboard"
main = "src/index.js"
compatibility_date = "2024-01-01"
EOF
```

**Verification:**
```bash
# Dashboard should be accessible at your Cloudflare Workers URL
curl https://your-dashboard.workers.dev/health
```

---

### 9. Claude Squad (30 min)

```bash
# Install Claude Squad
npm install -g claude-squad

# Initialize in your workspace
claude-squad init

# Create agent workspaces
claude-squad create-workspace --name research --branch feature/research
claude-squad create-workspace --name implementation --branch feature/impl

# List active workspaces
claude-squad list
```

**Verification:**
```bash
# Workspaces should be listed
claude-squad status
```

---

### 10. Trail of Bits Security (30 min)

```bash
# Install prerequisites
brew install codeql semgrep  # macOS
# or
pip install semgrep && gh extension install github/codeql

# Clone security skills
git clone https://github.com/trailofbits/claude-code-security.git /tmp/security

# Copy skills
mkdir -p .claude/skills/security
cp /tmp/security/skills/*.md .claude/skills/security/

# Add CodeQL queries
mkdir -p .claude/security/codeql
cp /tmp/security/codeql/*.ql .claude/security/codeql/

# Add Semgrep rules
mkdir -p .claude/security/semgrep
cp /tmp/security/semgrep/*.yaml .claude/security/semgrep/
```

**Verification:**
```bash
# Run a security scan
semgrep --config .claude/security/semgrep/ src/
```

---

## Week 3: Integration

### 11. viwo-cli (30 min)

```bash
# Install viwo-cli
npm install -g viwo-cli

# Initialize Docker-based workspace
viwo init --docker

# Create isolated environment
viwo create --name sandbox-dev --branch feature/sandbox

# Run Claude Code in isolation
viwo run --workspace sandbox-dev --allow-network
```

**Verification:**
```bash
viwo list
viwo status sandbox-dev
```

---

### 12. /prd-generator Command (10 min)

```bash
# Download the command
curl -o .claude/commands/prd-generator.md \
  https://raw.githubusercontent.com/anthropics/prd-generator/main/command.md

# Add to commands index
cat >> .claude/commands/index.md << 'EOF'

## /prd-generator
Generate PRDs from conversation context.
Usage: /prd-generator [topic]
EOF
```

**Verification:**
```bash
# Command should be available
cat .claude/commands/prd-generator.md | head -10
```

---

### 13. HCOM Multi-Agent (25 min)

```bash
# Clone HCOM
git clone https://github.com/anthropics/hcom.git /tmp/hcom

# Copy hooks and protocol
cp /tmp/hcom/hooks/* .claude/hooks/
cp /tmp/hcom/protocol.md .claude/kb/hcom-protocol.md

# Configure agent registry
cat > .claude/hcom-agents.yaml << 'EOF'
agents:
  - name: researcher
    workspace: .worktrees/research
  - name: implementer
    workspace: .worktrees/impl
  - name: reviewer
    workspace: .worktrees/review
EOF
```

**Verification:**
```bash
# HCOM should be configured
cat .claude/hcom-agents.yaml
```

---

## Week 4: Polish

### 14. Claudio Sounds (10 min)

```bash
# Clone Claudio
git clone https://github.com/anthropics/claudio.git /tmp/claudio

# Copy sound hook
cp /tmp/claudio/hooks/sound-hook.sh .claude/hooks/

# Configure sounds
cat > .claude/hooks/claudio-config.yaml << 'EOF'
sounds:
  session_start: /System/Library/Sounds/Glass.aiff
  task_complete: /System/Library/Sounds/Hero.aiff
  error: /System/Library/Sounds/Basso.aiff
EOF

chmod +x .claude/hooks/sound-hook.sh
```

---

### 15. /tdd Command (10 min)

```bash
# Download TDD command
curl -o .claude/commands/tdd.md \
  https://raw.githubusercontent.com/anthropics/tdd-command/main/tdd.md
```

---

## Verification Checklist

After adoption, verify each resource:

```bash
# Week 1 Quick Wins
[ ] ls .claude/skills/reference/        # Everything Claude Code
[ ] ls .claude/skills/devops/           # cc-devops-skills
[ ] cchooks list                         # cchooks SDK
[ ] cat .claude/kb/claude-code-tips/    # Tips Collection
[ ] ls .claude/kb/context-engineering/  # Context Engineering Kit

# Week 2 Tools
[ ] claude-code-tools --version         # Session tools
[ ] cat .claude/hooks/tdd-guard-config.yaml  # TDD Guard
[ ] curl your-dashboard.workers.dev     # better-ccflare
[ ] claude-squad list                   # Claude Squad
[ ] semgrep --version                   # Trail of Bits prereq

# Week 3 Integration
[ ] viwo list                           # viwo-cli
[ ] cat .claude/commands/prd-generator.md    # /prd-generator
[ ] cat .claude/hcom-agents.yaml        # HCOM

# Week 4 Polish
[ ] cat .claude/hooks/claudio-config.yaml    # Claudio
[ ] cat .claude/commands/tdd.md         # /tdd command
```

---

## Troubleshooting

### Common Issues

**cchooks not found:**
```bash
pip install --upgrade cchooks
# Ensure Python scripts are in PATH
```

**claude-code-tools cargo error:**
```bash
# Install Rust first
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

**viwo Docker issues:**
```bash
# Ensure Docker is running
docker ps
# Reset viwo
viwo reset --all
```

**Semgrep rules not loading:**
```bash
# Validate YAML syntax
semgrep --validate --config .claude/security/semgrep/
```

---

*Adoption Guide: 2026-02-03 | Sprint: S03 | Task: QW-011*
