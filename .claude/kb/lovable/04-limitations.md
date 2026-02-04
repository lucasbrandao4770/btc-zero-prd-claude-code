---
title: "Lovable Known Limitations"
description: "Comprehensive list of Lovable constraints with workarounds"
layer: "lovable"
source_refs: ["LOV004"]
source_urls:
  - "https://lovable.dev/docs"
created: "2026-01-30"
updated: "2026-01-30"
keywords: [lovable, limitations, constraints, workarounds, troubleshooting]
related:
  - "./02-github-workflow.md"
  - "./03-tool-division.md"
complexity: "intermediate"
---

# Lovable Known Limitations

## Overview

Lovable is a powerful prototyping tool, but understanding its limitations is crucial for effective use. This document catalogs known constraints and provides practical workarounds.

**Key Insight:** Lovable typically delivers 60-70% of a solution. Plan for a "hardening" phase in Claude Code to reach production quality.

---

## Limitations Summary

| # | Limitation | Severity | Has Workaround |
|---|------------|----------|----------------|
| 1 | Default branch only sync | High | Partial |
| 2 | Debugging loops | High | Yes |
| 3 | Supabase revert issues | High | Yes |
| 4 | 60-70% solution quality | Medium | Yes |
| 5 | Credit unpredictability | Medium | Partial |
| 6 | AI forgets context | Medium | Yes |
| 7 | Broad type overrides | Medium | Yes |
| 8 | Cannot import existing repos | High | No |
| 9 | Repository renaming breaks sync | High | Yes |
| 10 | Limited scalability | Medium | Yes |
| 11 | No rate limiting/observability | Low | Yes |

---

## Detailed Limitations

### 1. Default Branch Only Sync

| Aspect | Details |
|--------|---------|
| **Limitation** | GitHub sync only works with main/master branch |
| **Impact** | Cannot use feature branches from Lovable; all Lovable commits go to main |
| **Severity** | High |
| **Workaround** | Use Claude Code for branch-based development; treat Lovable as main-only tool |

**Best Practice:**
```
1. Lovable edits -> main branch
2. Clone locally
3. Create feature branches in Claude Code
4. Merge to main
5. Lovable syncs latest main
```

**Why It Matters:** Branch protection strategies common in team workflows don't apply. Consider Lovable for early prototyping before strict branching policies are needed.

---

### 2. Debugging Loops

| Aspect | Details |
|--------|---------|
| **Limitation** | Lovable can enter infinite fix loops, attempting the same solution repeatedly |
| **Impact** | Wastes credits; never resolves the actual issue |
| **Severity** | High |
| **Workaround** | Recognize the pattern early; switch to Claude Code for debugging |

**Detection Signs:**
- Same error appears after 2-3 "fix" attempts
- Lovable suggests reverting then re-applying changes
- Error messages contain the same stack trace

**Recovery Steps:**
```
1. Stop iterating in Lovable
2. Sync to GitHub
3. Clone/pull in Claude Code
4. Debug with proper tools (console, breakpoints)
5. Fix and push
6. Resume in Lovable
```

**Prevention:**
- Don't ask Lovable to fix complex logic bugs
- Provide more context when errors occur
- Break complex changes into smaller steps

---

### 3. Supabase Revert Issues

| Aspect | Details |
|--------|---------|
| **Limitation** | Reverting Lovable changes may not properly revert Supabase database changes |
| **Impact** | Database schema mismatch; orphaned tables/columns; broken references |
| **Severity** | High |
| **Workaround** | Manual Supabase cleanup; use migrations in Claude Code |

**Problem Scenario:**
```
1. Lovable creates table "orders" with columns
2. User reverts Lovable change
3. Code reverted, but "orders" table still exists in Supabase
4. Re-running causes "table already exists" errors
```

**Mitigation:**
```sql
-- Check for orphaned objects
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Manual cleanup if needed
DROP TABLE IF EXISTS orphaned_table CASCADE;
```

**Best Practice:**
- Use Claude Code for Supabase migrations
- Keep migration files in version control
- Test database changes in development first

---

### 4. 60-70% Solution Quality

| Aspect | Details |
|--------|---------|
| **Limitation** | Lovable outputs are functional but not production-ready |
| **Impact** | Missing error handling, loose types, no tests, potential security gaps |
| **Severity** | Medium |
| **Workaround** | Plan hardening phase in Claude Code |

**What's Typically Missing:**

| Category | Missing Elements |
|----------|------------------|
| Type Safety | Uses `any`, loose interfaces |
| Error Handling | Happy path only, no edge cases |
| Testing | No unit or integration tests |
| Security | Basic auth, missing validation |
| Performance | No optimization, potential N+1 queries |
| Accessibility | Missing ARIA labels, keyboard nav |

**Hardening Checklist:**
- [ ] Replace all `any` types
- [ ] Add try/catch blocks
- [ ] Implement loading/error states
- [ ] Add input validation
- [ ] Write critical path tests
- [ ] Security review
- [ ] Performance audit

---

### 5. Credit Unpredictability

| Aspect | Details |
|--------|---------|
| **Limitation** | Credit consumption varies significantly; hard to predict costs |
| **Impact** | Budget planning difficult; surprise credit exhaustion |
| **Severity** | Medium |
| **Workaround** | Set credit alerts; use Lovable strategically |

**Cost Factors:**
- Complex prompts consume more credits
- Failed iterations still cost credits
- Debugging loops can rapidly drain credits

**Mitigation Strategies:**
```
1. Write clear, specific prompts (fewer iterations)
2. Stop debugging loops early (switch to Claude Code)
3. Use Lovable for UI, not logic (more predictable)
4. Set weekly credit budgets
5. Monitor usage dashboard regularly
```

---

### 6. AI Forgets Context

| Aspect | Details |
|--------|---------|
| **Limitation** | Lovable may forget previous context in long sessions |
| **Impact** | Inconsistent outputs; repeated explanations needed |
| **Severity** | Medium |
| **Workaround** | Reference specific files; restart sessions for complex work |

**Symptoms:**
- Lovable ignores previously established patterns
- Asks questions already answered
- Creates duplicate components

**Solutions:**
```
1. Reference specific file paths:
   "Update the component in src/components/PatientCard.tsx"

2. Provide explicit context:
   "Following our established design system with blue (#3B82F6)
   primary color and 8px border radius..."

3. Start fresh sessions for major new features

4. Keep documentation in project files that Lovable can reference
```

---

### 7. Broad Type Overrides

| Aspect | Details |
|--------|---------|
| **Limitation** | Lovable often uses `any` or overly broad types |
| **Impact** | Loss of type safety; hidden bugs; IDE autocomplete broken |
| **Severity** | Medium |
| **Workaround** | Type refinement pass in Claude Code |

**Common Patterns:**
```typescript
// Lovable output
const handleData = (data: any) => { ... }
interface Props { data: any; }

// Should be
const handleData = (data: PatientRecord) => { ... }
interface Props { data: PatientRecord; }
```

**Refinement Process:**
```bash
# Find all 'any' types
grep -r ": any" src/

# TypeScript strict check
npx tsc --noEmit --strict

# Fix each instance with proper types
```

**Prevention:**
- Define types in Claude Code FIRST
- Reference types in Lovable prompts
- Run type checks after each sync

---

### 8. Cannot Import Existing Repositories

| Aspect | Details |
|--------|---------|
| **Limitation** | Cannot connect Lovable to pre-existing React codebases |
| **Impact** | Must start fresh or manually migrate code |
| **Severity** | High |
| **Workaround** | None - architectural limitation |

**What Works:**
- New repository created by Lovable
- Empty repository connected to Lovable
- Repository previously created by Lovable

**What Doesn't Work:**
- Importing existing Next.js project
- Connecting arbitrary React codebase
- Migrating from other frameworks

**Alternative Approach:**
```
1. Start new Lovable project
2. Recreate UI components via prompts
3. Copy business logic from old repo manually
4. Integrate in Claude Code
```

---

### 9. Repository Renaming Breaks Sync

| Aspect | Details |
|--------|---------|
| **Limitation** | Renaming GitHub repository breaks Lovable sync |
| **Impact** | Sync fails silently or with cryptic errors |
| **Severity** | High |
| **Workaround** | Reconnect repository manually |

**Recovery Steps:**
```
1. Go to Lovable project settings
2. Disconnect GitHub
3. Reconnect with new repository name
4. Verify sync works
5. Force sync if needed
```

**Prevention:**
- Choose final repository name before connecting
- If renaming needed, plan reconnection

---

### 10. Limited Scalability

| Aspect | Details |
|--------|---------|
| **Limitation** | Performance degrades with large codebases |
| **Impact** | Slower responses; context limitations; inconsistent outputs |
| **Severity** | Medium |
| **Workaround** | Modular architecture; move mature code to Claude Code |

**Threshold Signs:**
- Responses noticeably slower
- Lovable misses existing components
- Increased hallucination/inconsistency

**Mitigation:**
```
1. Keep Lovable projects focused (single feature area)
2. Extract stable modules to separate packages
3. Use Lovable for active development areas only
4. Archive completed features to reduce context
```

**Architecture Pattern:**
```
Main repo (Claude Code managed):
├── packages/
│   ├── auth/        # Mature, extracted
│   ├── ui-library/  # Mature, extracted
│   └── utils/       # Mature, extracted
└── apps/
    └── web/         # Lovable-connected for active dev
```

---

### 11. No Built-in Rate Limiting/Observability

| Aspect | Details |
|--------|---------|
| **Limitation** | No built-in API rate limiting, logging, or monitoring |
| **Impact** | Production apps need these added manually |
| **Severity** | Low |
| **Workaround** | Add via Claude Code or external services |

**What to Add:**
```typescript
// Rate limiting (example with Supabase Edge Functions)
const rateLimit = {
  windowMs: 60000,
  maxRequests: 100
};

// Observability
import { logger } from '@/lib/logger';
logger.info('API request', { endpoint, userId, duration });
```

**Recommended Stack:**
| Concern | Solution |
|---------|----------|
| Rate Limiting | Supabase Edge Functions, Upstash |
| Logging | Axiom, LogTail, Supabase Logs |
| Monitoring | Sentry, Vercel Analytics |
| APM | Vercel, Datadog |

---

## Risk Assessment Matrix

| Limitation | Probability | Impact | Risk Level | Mitigation Priority |
|------------|-------------|--------|------------|---------------------|
| Default branch only | Certain | Medium | Medium | Low (accept) |
| Debugging loops | Likely | High | High | High (process) |
| Supabase reverts | Possible | High | Medium | High (process) |
| 60-70% quality | Certain | Medium | Medium | High (planning) |
| Credit unpredictability | Likely | Medium | Medium | Medium (budget) |
| Context forgetting | Possible | Low | Low | Low (technique) |
| Type overrides | Certain | Medium | Medium | High (automation) |
| No import | Certain | Low | Low | Low (accept) |
| Rename breaks sync | Unlikely | High | Low | Low (documentation) |
| Scalability | Possible | Medium | Medium | Medium (architecture) |
| No observability | Certain | Low | Low | Medium (add later) |

---

## Mitigation Summary

### Process Changes
1. **Recognize debugging loops** - Switch to Claude Code after 2 failed attempts
2. **Plan hardening phase** - Never ship Lovable output directly
3. **Use Claude Code for Supabase** - Migrations via version control

### Technical Measures
1. **Type-first development** - Define types before Lovable
2. **Automated type checks** - CI/CD pipeline validation
3. **Modular architecture** - Keep Lovable projects small

### Operational Practices
1. **Credit monitoring** - Weekly budget reviews
2. **Session management** - Fresh sessions for major features
3. **Documentation** - Keep patterns in project files

---

## NPM Security Notes for Lovable Projects

Lovable-generated projects often show npm audit warnings. Here's how to assess them:

### Common False Positives

| Vulnerability | Why It's Usually Safe |
|--------------|----------------------|
| React Router XSS | Only affects `createBrowserRouter` with loaders, not `<BrowserRouter>` |
| esbuild dev server | Dev-only, never in production bundle |
| glob CLI injection | Only CLI tool, not the library API |
| Deprecated packages | Usually dev/test dependencies (jsdom ecosystem) |

### Safe Update Commands

```bash
# Safe fixes (no breaking changes)
npm update lodash js-yaml

# Check router type first
grep -r "createBrowserRouter" src/

# NEVER run blindly - can downgrade to vulnerable versions!
# npm audit fix --force  ← AVOID
```

### When to Actually Worry

- Vulnerabilities in **production dependencies** that handle **user input**
- Anything affecting your actual code paths (not dev tooling)
- Critical severity with known exploits in the wild

### CI/CD Recommendation

```bash
# Use audit-level to reduce noise
npm audit --audit-level=high

# Use npm ci for reproducible builds
npm ci
```

---

## Related Resources

- [GitHub Workflow](./02-github-workflow.md) - Sync best practices
- [Tool Division](./03-tool-division.md) - When to use Claude Code
- [Prompting Guide](./01-prompting-guide.md) - Reduce iteration cycles

---

*Know the limitations. Plan around them. Build confidently.*
