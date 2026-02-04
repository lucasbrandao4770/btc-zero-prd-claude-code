---
title: "Lovable GitHub Workflow"
description: "Setting up and managing GitHub sync with Lovable projects"
layer: "lovable"
source_refs: ["LOV002"]
source_urls:
  - "https://lovable.dev/docs/github"
  - "https://lovable.dev/docs/integrations/github"
created: "2026-01-30"
updated: "2026-01-30"
keywords: [lovable, github, sync, workflow, version-control, integration]
related:
  - "./03-tool-division.md"
  - "./04-limitations.md"
complexity: "intermediate"
---

# Lovable GitHub Workflow

## Overview

Lovable integrates with GitHub to enable version control and hybrid development workflows. This allows teams to prototype in Lovable, then refine and extend code in traditional development environments like Claude Code.

Understanding the sync mechanism and its constraints is critical for avoiding data loss and merge conflicts.

---

## Setup Requirements

### Prerequisites

| Requirement | Details |
|-------------|---------|
| GitHub Account | Personal or organization account |
| Lovable Account | Active subscription (free tier has limitations) |
| Repository Access | Ability to install GitHub Apps |

### Step-by-Step Setup

#### 1. Connect GitHub Account

```
Lovable Settings -> Integrations -> GitHub -> Connect
```

- Authorize Lovable GitHub App
- Grant repository access (all repos or select repos)
- Verify connection status shows "Connected"

#### 2. Install Lovable GitHub App

The app requires these permissions:
- **Contents**: Read and write (for sync)
- **Metadata**: Read (for repo listing)
- **Pull requests**: Read and write (optional, for PR workflow)

#### 3. Create or Connect Repository

**Option A: New Repository (Recommended)**
```
Lovable Project -> Settings -> GitHub -> Create New Repository
```
- Lovable creates repo with correct structure
- Initial commit includes all project files
- Sync is automatically configured

**Option B: Connect Existing (Limited)**
```
Lovable Project -> Settings -> GitHub -> Connect Existing
```
- Repository must be empty or Lovable-compatible
- Cannot import arbitrary React projects
- See [Limitations](./04-limitations.md) for details

---

## Critical Constraints

### Default Branch Only

| Constraint | Impact | Workaround |
|------------|--------|------------|
| **Sync only works with main/master** | Cannot use feature branches from Lovable | Use Claude Code for branch-based development |
| **Branch changes in GitHub ignored** | Lovable only reads default branch | Merge to main before Lovable edits |
| **No branch selection in UI** | Cannot switch branches in Lovable | N/A - architectural limitation |

### Sync Direction

```
Lovable <---> GitHub (main branch only)
             |
             v
        Claude Code (any branch)
```

**Key Points:**
- Lovable commits go directly to main
- Changes in feature branches are invisible to Lovable
- Always pull before working in Lovable after Claude Code changes

### Repository Requirements

| Requirement | Why |
|-------------|-----|
| No pre-created structure | Lovable needs specific folder structure |
| Empty or Lovable-created | Cannot import arbitrary codebases |
| Write access | Lovable needs to push commits |
| No branch protection on main | Or configure bypass for Lovable app |

---

## Sync Workflow Diagram

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|     LOVABLE      |     |      GITHUB      |     |   CLAUDE CODE    |
|                  |     |                  |     |                  |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         |  1. Make UI changes    |                        |
         +----------------------->|                        |
         |     (auto-commit)      |                        |
         |                        |  2. Pull changes       |
         |                        |<-----------------------+
         |                        |                        |
         |                        |  3. Create feature     |
         |                        |     branch             |
         |                        |<-----------------------+
         |                        |                        |
         |                        |  4. Implement logic    |
         |                        |<-----------------------+
         |                        |                        |
         |                        |  5. Merge to main      |
         |                        |<-----------------------+
         |                        |                        |
         |  6. Pull latest        |                        |
         |<-----------------------+                        |
         |     (auto-sync)        |                        |
         |                        |                        |
         |  7. Continue UI work   |                        |
         +----------------------->|                        |
         |                        |                        |
```

---

## Branch Handling Strategies

### Strategy 1: Lovable-First (Recommended for Prototypes)

```
1. Build UI in Lovable (commits to main)
2. Clone repo locally
3. Create feature branch for logic
4. Implement in Claude Code
5. Merge to main
6. Return to Lovable for UI refinements
```

**Best for:** Early-stage prototypes, UI-heavy apps

### Strategy 2: Claude-First (Recommended for Production)

```
1. Initialize repo in Claude Code
2. Build core structure and logic
3. Push to main
4. Connect Lovable for UI polish
5. Sync and refine
```

**Best for:** Complex apps, backend-heavy projects

### Strategy 3: Parallel Development (Advanced)

```
1. Lovable handles UI on main
2. Claude Code works on feature branches
3. Scheduled sync points (daily merge to main)
4. Clear ownership: UI = Lovable, Logic = Claude Code
```

**Best for:** Teams with clear role separation

---

## Conflict Prevention

### Before Working in Lovable

```bash
# Always ensure main is up to date
git checkout main
git pull origin main

# Ensure no uncommitted changes
git status
```

### Before Working in Claude Code

```
1. Check Lovable project status
2. Ensure no pending Lovable edits
3. Pull latest from main
4. Create feature branch immediately
```

### Sync Checkpoint Checklist

Before switching between tools:

- [ ] All Lovable changes committed (check project status)
- [ ] All Claude Code changes pushed
- [ ] Feature branches merged to main (if switching to Lovable)
- [ ] `git pull` executed in both environments
- [ ] No uncommitted local changes

---

## Conflict Resolution

### When Conflicts Occur

| Scenario | Resolution |
|----------|------------|
| Lovable overwrites Claude changes | Restore from git history, re-merge |
| Claude changes break Lovable UI | Fix in Claude Code, push to main |
| Simultaneous edits to same file | Manual merge using git |

### Recovery Commands

```bash
# View recent commits to find last good state
git log --oneline -20

# Restore specific file from previous commit
git checkout <commit-hash> -- path/to/file

# View diff between commits
git diff <old-commit> <new-commit>

# Create recovery branch before fixing
git checkout -b recovery-$(date +%Y%m%d)
```

### Prevention Best Practices

1. **Designate file ownership**
   - Lovable: `src/components/ui/*`, `src/pages/*`
   - Claude Code: `src/lib/*`, `src/hooks/*`, `src/types/*`

2. **Use sync markers**
   ```typescript
   // LOVABLE-MANAGED: Do not edit directly
   // Edit in Lovable, then sync
   ```

3. **Regular sync points**
   - Before starting new feature
   - After completing any feature
   - Daily if parallel development

---

## Best Practices

### Commit Messages

Lovable auto-generates commit messages. For Claude Code commits:

```
# Format
[claude-code] <type>: <description>

# Examples
[claude-code] feat: add authentication logic
[claude-code] fix: resolve type errors in patient model
[claude-code] refactor: extract API client to separate module
```

### File Organization

```
src/
├── components/
│   └── ui/           # Lovable-managed (shadcn components)
├── pages/            # Lovable-managed (route components)
├── lib/              # Claude Code-managed (utilities)
├── hooks/            # Claude Code-managed (custom hooks)
├── types/            # Claude Code-managed (TypeScript types)
└── services/         # Claude Code-managed (API layer)
```

### Sync Frequency

| Development Phase | Recommended Frequency |
|-------------------|----------------------|
| Initial prototype | After each major UI change |
| Active development | 2-3 times per day |
| Stabilization | Once per feature completion |
| Maintenance | As needed |

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Sync button disabled | No GitHub connection | Reconnect GitHub in settings |
| Changes not appearing | Branch mismatch | Ensure changes are on main |
| "Repository not found" | Permission revoked | Reinstall GitHub App |
| Merge conflicts | Parallel edits | Manual git merge required |

### Diagnostic Steps

1. **Check connection status**
   ```
   Lovable Settings -> Integrations -> GitHub
   Status should show "Connected"
   ```

2. **Verify repository access**
   ```
   GitHub Settings -> Applications -> Lovable
   Check repository permissions
   ```

3. **Review commit history**
   ```bash
   git log --oneline --all --graph -20
   ```

4. **Check for divergence**
   ```bash
   git fetch origin
   git status
   # Look for "Your branch is behind/ahead"
   ```

---

## Related Resources

- [Tool Division](./03-tool-division.md) - When to use each tool
- [Limitations](./04-limitations.md) - GitHub sync constraints
- [Prompting Guide](./01-prompting-guide.md) - Effective Lovable prompts

---

*GitHub sync is the bridge between rapid prototyping and production code. Use it intentionally.*
