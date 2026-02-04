---
name: lovable
description: Workflow automation for Lovable + Claude Code integration. Activates when building React UIs with Lovable, creating prototypes, or rapid frontend iteration. Provides requirements → design → generate → review pipeline with GitHub sync coordination.
---

# Lovable - AI-Powered UI Prototyping Workflow

Orchestrates rapid UI prototyping through Lovable AI with seamless Claude Code integration. Combines Lovable's visual generation speed with Claude Code's deep engineering capabilities for optimal development workflow.

---

## When This Skill Activates

- User asks to **create UI components** or **prototypes** with Lovable
- Working on **React/frontend projects** that use Lovable
- User mentions **"prototype"**, **"design"**, **"lovable"**, **"rapid UI"**
- Creating **visual mockups** or **UI iterations**
- Planning phase requires **quick MVP validation**
- User wants to **iterate visually** before engineering complexity

## When NOT to Activate

- **Backend-only work** (APIs, databases, services)
- **Non-React projects** (Lovable is React-focused)
- **Simple CSS fixes** that don't need regeneration
- **Complex TypeScript logic** (use Claude Code directly)
- **Database/migration work** (outside Lovable's scope)
- User explicitly wants **manual component creation**

---

## Prerequisites

### Required MCPs

| MCP | Purpose | When to Use |
|-----|---------|-------------|
| **shadcn/ui** | Component discovery and examples | Before generating, to check available primitives |
| **Magic (21st.dev)** | AI component generation | When Claude Code generates components locally |
| **Playwright** | Visual testing and validation | After generation, to verify output |
| **Context7** | React/shadcn documentation lookup | When researching patterns or best practices |

### Required Access

| Tool | Purpose |
|------|---------|
| **Lovable.dev** | AI UI generation platform |
| **GitHub** | Sync repository between Lovable and local |
| **npm/pnpm** | Local development and testing |

---

## Prompting Guidelines (Lovable)

### Be Specific

| Bad Prompt | Good Prompt |
|------------|-------------|
| "Fix the login page" | "On /login, add password visibility toggle and 'Remember me' checkbox below the password field" |
| "Make it look better" | "Change the header background to slate-800, increase padding to p-6, use Inter font" |
| "Add a form" | "Create a contact form with name, email, message fields, all required, with shadcn/ui Input and Textarea" |

### Use Plan Mode for Complex Work

Allocate **60-70% of prompt to planning**, 30-40% to execution:

```
I need to implement user authentication.

PLAN:
1. Create /login page with email/password form
2. Add /register page with email/password/confirm fields
3. Implement password strength indicator on register
4. Add "Forgot Password" flow with email verification
5. Store auth state in context with loading states
6. Redirect authenticated users from login to /dashboard

GUARDRAILS:
- Do NOT modify the existing /dashboard layout
- Do NOT change the Navbar component
- Keep all existing routes functional

START WITH: Step 1 only - login page with form
```

### Set Guardrails

Always specify what NOT to touch:

```
GUARDRAILS:
- Do NOT modify: [file/component names]
- Do NOT change: [specific functionality]
- Do NOT remove: [existing features]
- Preserve: [important patterns/state]
```

### Batch Related Changes

Combine related changes in single prompts to optimize credits:

```
In the PatientCard component:
1. Add status badge (Admitted, Discharged, In Treatment)
2. Show admission date below patient name
3. Add subtle hover animation (scale 1.02)
4. Include action menu with Edit, View History, Transfer options
```

### Use Knowledge Base

Before complex changes, inform Lovable of project context:

```
PROJECT CONTEXT:
- This is a clinical management system
- We use shadcn/ui components
- State management is via React Context
- API calls use React Query with /api prefix
- All dates use date-fns with pt-BR locale

NOW: Add the patient timeline component...
```

---

## GitHub Sync Workflow

```
Lovable (UI) → GitHub (main) → Local (pull) → Claude Code → GitHub (push) → Lovable
     ↑                                                              │
     └──────────────────────────────────────────────────────────────┘
```

### Sync Commands

```bash
# Before starting Claude Code work
git checkout main
git pull origin main

# After Claude Code changes
git add -A
git commit -m "feat(ui): description"
git push origin main

# Verify sync
git status  # Should show "Your branch is up to date"
```

### Critical Sync Rules

1. **Lovable syncs to main only** - Merge feature branches before Lovable can see them
2. **Always pull before editing** - Avoid merge conflicts
3. **Push immediately after Claude Code changes** - Keep Lovable up to date
4. **Check sync before switching tools** - Run `git status` first

---

## Tool Division Matrix

| Use Lovable | Use Claude Code |
|-------------|-----------------|
| Rapid UI prototyping | Complex TypeScript logic |
| Visual design iteration | Database schema/migrations |
| Component scaffolding | Testing infrastructure |
| shadcn/ui styling | Complex state management |
| Quick MVP validation | Multi-file refactoring |
| New page creation | API integration / Business logic |
| Simple forms / animations | Type system / Performance |

**Rule of thumb:** Visual-first and simple? -> Lovable. Logic-heavy or complex? -> Claude Code.

---

## Workflow: 4-Phase Pipeline

### Phase 1: REQUIREMENTS (Host + Jarvis)

**Goal:** Gather complete UI requirements before generation.

Questions to ask:
- What page/component are we building?
- Who are the users and what actions do they need?
- What data will be displayed/collected?
- Any existing design patterns to follow?
- What should NOT be changed?
- Success criteria - how do we know it's done?

**Output:** Clear, specific requirements document.

---

### Phase 2: DESIGN PROPOSAL (Jarvis -> Host) [GATE]

**Goal:** Create detailed spec for user approval before generation.

For each component/page, provide:

```markdown
## Proposal: [ComponentName/PageName]

**Purpose:** [What it does and why]

**Visual Layout:**
- Structure: [layout description]
- Key elements: [list main UI elements]
- Responsive: [mobile/tablet/desktop behavior]

**Components Needed:**
- shadcn/ui: [Button, Card, Input, etc.]
- Custom: [any new components]

**States:**
- Default: [appearance]
- Loading: [skeleton/spinner]
- Empty: [empty state message]
- Error: [error display]

**Data Flow:**
- Inputs: [props/context/API]
- User actions: [clicks, forms, etc.]
- Outputs: [callbacks, mutations]

**Guardrails:**
- Do NOT modify: [list]
- Preserve: [list]
```

**APPROVAL GATE:** Use AskUserQuestion:
- **Approve** -> Proceed to generation
- **Modify** -> Update spec and re-present
- **Reject** -> Return to requirements

---

### Phase 3: GENERATE (Lovable or Claude Code)

**Goal:** Generate approved UI using appropriate tool.

#### If Using Lovable:

1. **Prepare prompt** following guidelines above
2. **Include guardrails** from Phase 2
3. **Reference plan** from design proposal
4. **Submit to Lovable** and wait for generation
5. **Pull changes** to local: `git pull origin main`

#### If Using Claude Code (complex components):

```
Step 1: Pull shadcn/ui Primitives
────────────────────────────────
Use shadcn MCP to check/install needed components:
- npx shadcn-ui@latest add [component]

Step 2: Generate Component
────────────────────────────────
Use Magic MCP or manual creation:
- Follow design proposal spec
- Include TypeScript types
- Add proper documentation

Step 3: Integrate
────────────────────────────────
- Place in correct directory
- Export from index files
- Add to page imports
```

---

### Phase 4: REVIEW & REFINE (Host + Jarvis) [GATE]

**Goal:** Validate output and iterate if needed.

Present results:
```markdown
## Generated: [ComponentName]

**Location:** `src/components/[path]/[file].tsx`

**Changes Made:**
- [Summary of what was created/modified]

**Verification:**
- [ ] TypeScript compiles: `npm run typecheck`
- [ ] Tests pass: `npm test`
- [ ] Build succeeds: `npm run build`
- [ ] Visual review: [screenshot or description]

**Ready for review.**
```

**APPROVAL GATE:** Use AskUserQuestion:
- **Approve** -> Commit and document
- **Request changes** -> Specify modifications, iterate
- **Reject** -> Return to design phase

### After Approval

1. Commit with conventional message:
   ```
   feat(ui): add [ComponentName]

   - [Brief description]
   - Generated via Lovable workflow
   ```

2. Push to sync with Lovable:
   ```bash
   git push origin main
   ```

3. Update any relevant documentation

---

## Quick Reference Commands

### Verification Suite

```bash
# Full verification (run after changes)
npm run typecheck && npm test && npm run build

# Quick type check
npm run typecheck

# Run specific tests
npm test -- --grep "ComponentName"
```

### Git Sync

```bash
# Before Lovable work - ensure clean state
git status

# Pull Lovable changes
git pull origin main

# Push Claude Code changes
git add -A && git commit -m "feat(ui): description" && git push origin main

# Check sync status
git log --oneline -5
```

---

## Known Limitations & Workarounds

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Main branch only sync** | Feature branches invisible to Lovable | Merge to main before Lovable sees changes; use short-lived branches |
| **Debugging loops** | Lovable can get stuck on type errors | After 3 failed attempts, switch to Claude Code for fix |
| **Credit unpredictability** | Complex prompts use more credits | Batch related changes; set spending caps; use Claude Code for iterations |
| **Broad type overrides** | Lovable may use `any` or `as unknown` | Use Claude Code for surgical type fixes |
| **No direct DB access** | Cannot create migrations | Use Claude Code/supabase-migrations skill for DB work |
| **Limited testing** | Lovable doesn't write tests | Use Claude Code for test coverage |
| **Context limits** | Large projects overwhelm context | Use Knowledge Base; reference specific files |

### Debugging Loop Recovery

When Lovable gets stuck (3+ failed attempts):

1. **Stop Lovable attempts** - Don't waste more credits
2. **Pull latest to local**: `git pull origin main`
3. **Use Claude Code** to diagnose and fix
4. **Push fix**: `git push origin main`
5. **Return to Lovable** for continued UI work

---

## Error Handling

| Error | Action |
|-------|--------|
| Lovable sync fails | Check GitHub connection; verify branch is main |
| Type errors after generation | Use Claude Code for targeted type fixes |
| Component not rendering | Check imports/exports; verify shadcn components installed |
| Build fails | Run `npm run typecheck` to identify issues |
| Tests fail | Run `npm test` to see failures; fix with Claude Code |
| Merge conflicts | Resolve locally; push to main before continuing |
| Lovable timeout | Simplify prompt; break into smaller chunks |
| Credit limit reached | Switch to Claude Code; resume Lovable when credits refresh |

---

## Example Session

```
User: "I need to build a patient admission form for the clinical app"

[Phase 1: Requirements]
Jarvis asks: "What fields are needed? What validation?
             Any existing patterns to follow?"

User provides details about fields, validation rules, etc.

[Phase 2: Design Proposal]
Jarvis: "Here's my proposal for the PatientAdmissionForm:

## Proposal: PatientAdmissionForm

**Purpose:** Collect patient information for hospital admission

**Visual Layout:**
- Two-column form on desktop, single column on mobile
- Sections: Personal Info, Medical History, Insurance, Emergency Contact
- Progress indicator at top showing completion

**Components:**
- shadcn/ui: Form, Input, Select, DatePicker, Textarea, Button
- Custom: FormSection, ProgressIndicator

**Guardrails:**
- Do NOT modify existing PatientCard
- Preserve current form validation patterns

Approve this spec?"

User: "Approve, but add a photo upload section too"

Jarvis: "Updated spec with photo upload. Approve?"

User: "Approved"

[Phase 3: Generate]
Jarvis: "This form is primarily visual with standard validation.
        Recommending Lovable for rapid generation.

        Prompt prepared for Lovable:
        [Shows detailed prompt with guardrails]

        Submit to Lovable, then pull changes."

User submits to Lovable, pulls changes

[Phase 4: Review]
Jarvis: "Changes pulled. Running verification...
        - TypeScript: PASS
        - Tests: PASS
        - Build: PASS

        Visual review shows form rendering correctly.

        Approve to commit?"

User: "Approved"

Jarvis: "Committed and pushed to main.
        Lovable sync complete."
```

---

## Related Resources

| Resource | Path/URL | Purpose |
|----------|----------|---------|
| ui-forge skill | skills/ui-forge/ | Local component generation (use with Lovable) |
| frontend-design skill | skills/frontend-design/ | Style direction and anti-AI-slop |
| supabase-migrations skill | skills/supabase-migrations/ | When UI changes need DB updates |
| testing skill | skills/testing/ | Add test coverage to generated components |
| shadcn/ui docs | https://ui.shadcn.com | Component library reference |
| Lovable docs | https://docs.lovable.dev | Platform documentation |
| React docs | https://react.dev | React patterns and hooks |

---

## Notes

- **Tool selection matters** - Lovable for rapid visual iteration, Claude Code for engineering depth
- **Approval gates are mandatory** - Never generate without user sign-off on specs
- **Sync religiously** - Git sync issues are the #1 source of problems
- **Credit awareness** - Batch prompts and set caps; don't iterate endlessly
- **Hybrid workflow** - Best results come from using both tools for their strengths
- Works best with **Jarvis Mode active** for full MCP orchestration capabilities
