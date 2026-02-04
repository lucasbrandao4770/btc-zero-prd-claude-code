---
name: ui-forge
description: Autonomous UI component generation workflow using MCP orchestration. Activates when building React UIs, creating components, or designing frontend interfaces. Provides brainstorm → approve → generate → review pipeline.
---

# UI Forge - Autonomous Component Generation

Orchestrates AI-powered UI component generation through a structured approval workflow. Uses 21st.dev Magic MCP, shadcn/ui MCP, frontend-design skill, and Playwright for a complete design-to-code pipeline.

---

## When This Skill Activates

- User asks to **create UI components** or **build frontend interfaces**
- Working on **React component design** tasks
- User mentions **"generate components"**, **"create UI"**, **"design interface"**
- Planning phase includes UI/frontend deliverables
- User wants to **prototype UI** before full implementation

## When NOT to Activate

- Simple CSS fixes or styling tweaks (use frontend-design skill directly)
- Backend-only work
- Non-React projects (skill is React-focused)
- User explicitly wants manual component creation

---

## Prerequisites

### Required MCPs

| MCP | Purpose | Installation |
|-----|---------|--------------|
| **21st.dev Magic** | AI component generation | `npx @21st-dev/cli@latest install claude --api-key <key>` |
| **shadcn/ui** | Component library access | Add to mcp_config.json |
| **Playwright** | Visual validation | `npx @playwright/mcp@latest` |

### Required Skills

| Skill | Purpose |
|-------|---------|
| **frontend-design** | Style direction and anti-AI-slop aesthetics |

---

## Workflow: 5-Phase Pipeline

### Phase 1: BRAINSTORM (Host + Jarvis)

**Goal:** Understand what components are needed and why.

Questions to ask:
- What is the user trying to build?
- Who are the users of this interface?
- What interactions/states are needed?
- Any existing design systems or style guides?
- Reference designs or inspirations?

**Output:** Clear understanding of component requirements.

---

### Phase 2: DESIGN PROPOSAL (Jarvis → Host)

**Goal:** Describe each component before generation for user approval.

For each component, provide:

```markdown
## Component: [ComponentName]

**Purpose:** [What it does and why it's needed]

**Visual Description:**
- Layout: [horizontal/vertical/grid, dimensions]
- Colors: [primary colors, backgrounds, accents]
- Typography: [font sizes, weights, hierarchy]
- Spacing: [padding, margins, gaps]

**States:**
- Default: [appearance]
- Hover: [changes]
- Active/Selected: [changes]
- Disabled: [changes]
- Loading: [changes]
- Error: [changes]

**Interactions:**
- [User action] → [Result]
- [User action] → [Result]

**Data:**
- Inputs: [props the component accepts]
- Outputs: [events it emits]

**Dependencies:**
- shadcn/ui primitives: [Button, Card, etc.]
- Icons: [if any]
```

**Approval Gate:** Use AskUserQuestion to confirm each component spec:
- Approve → Proceed to generation
- Modify → Update spec and re-present
- Reject → Remove from generation queue

---

### Phase 3: AUTONOMOUS GENERATION (Jarvis)

**Goal:** Generate approved components using MCP orchestration.

For each approved component:

```
Step 1: Generate Base Component
────────────────────────────────
Use 21st.dev Magic MCP:
"/ui create [detailed natural language description from Phase 2]"

Include in description:
- Visual details (colors, spacing, layout)
- States and interactions
- TypeScript props interface
- Tailwind CSS styling

Step 2: Pull Primitives
────────────────────────────────
Use shadcn/ui MCP to fetch any needed base components:
- Check if Button, Input, Card, Dialog, etc. are needed
- Pull components not yet in project

Step 3: Apply Style Direction
────────────────────────────────
Invoke frontend-design skill guidance:
- Ensure distinctive typography (not generic Inter/Roboto)
- Apply meaningful color palette
- Add purposeful animations
- Avoid "AI slop" patterns

Step 4: Integrate
────────────────────────────────
- Place component in correct directory
- Add proper TypeScript types
- Export from index files
- Add JSDoc documentation
```

---

### Phase 4: REVIEW & ITERATE (Host + Jarvis)

**Goal:** Present generated components for feedback.

Present results:
```markdown
## Generated: [ComponentName]

**File:** `src/components/[path]/[ComponentName].tsx`

**Preview:** [If Playwright snapshot available]

**Code Summary:**
- Lines: [X]
- Props: [list]
- Dependencies: [list]

**Ready for review.**
```

Use AskUserQuestion:
- Approve → Move to finalize
- Request changes → Iterate generation
- Reject → Remove or redesign

---

### Phase 5: FINALIZE (Jarvis)

**Goal:** Commit and document approved components.

Actions:
1. Ensure all components pass type checks
2. Run Playwright visual snapshot (optional)
3. Update component index exports
4. Add to component documentation (if exists)
5. Commit with conventional commit message:
   ```
   feat(ui): add [ComponentName] component

   - [Brief description]
   - Generated via UI Forge workflow
   ```

---

## MCP Command Reference

### 21st.dev Magic MCP

```
/ui create a [component type] with [visual details]

Examples:
/ui create a flow node card with rounded corners, subtle shadow, status indicator dot in top-right, title and subtitle text, and connection handles on left and right edges

/ui create a sliding panel from the right side with tabs for Input, Output, Logs, and LLM sections, dark theme, close button in header
```

### shadcn/ui MCP

```
Browse available components
Search for specific component patterns
Install components to project
```

### Playwright MCP

```
Take screenshot of rendered component
Compare against baseline
Report visual differences
```

---

## Design Direction Guidelines

When describing components to 21st.dev Magic, include style direction:

| Direction | Description Keywords |
|-----------|---------------------|
| **Minimal** | clean, whitespace, subtle shadows, muted colors |
| **Technical** | monospace fonts, code-like, precise borders, data-dense |
| **Workflow** | node-based, connectors, status indicators, execution states |
| **Dashboard** | cards, metrics, charts, responsive grid |

For Clinical Flow Visualization specifically:
- Use **workflow/technical** direction
- Node states: pending (gray), running (blue pulse), completed (green), error (red)
- Dark theme friendly (works in both modes)
- Data-dense but scannable

---

## Error Handling

| Error | Action |
|-------|--------|
| 21st.dev MCP not configured | Guide user to install: `npx @21st-dev/cli@latest install claude` |
| API key invalid | Direct to 21st.dev/magic/console for new key |
| Component generation fails | Simplify description, break into smaller pieces |
| shadcn component missing | Install via shadcn/ui MCP or CLI |
| Type errors in generated code | Fix manually or regenerate with more specific types |

---

## Example Session

```
User: "I need to build the flow visualization components"

[Phase 1: Brainstorm]
Jarvis asks clarifying questions about nodes, panels, states...

[Phase 2: Design Proposal]
Jarvis: "Here are the 4 components I plan to generate:
1. FlowNode - The 12-step node representation
2. DetailPanel - Sliding right panel with tabs
3. FlowCanvas - Container with React Flow
4. UploadZone - JSON file drop area

[Detailed specs for each...]

Approve these specs?"

User: "Approve"

[Phase 3: Autonomous Generation]
Jarvis: "Generating FlowNode..."
→ Uses 21st.dev: "/ui create a workflow node card..."
→ Pulls shadcn/ui Card, Badge
→ Applies frontend-design styling
→ Integrates into src/components/flow/

[Phase 4: Review]
Jarvis: "FlowNode generated. Review the result..."

User: "Looks good, approved"

[Phase 5: Finalize]
Jarvis: Commits component, updates exports
```

---

## Related Resources

| Resource | Path | Purpose |
|----------|------|---------|
| frontend-design skill | skills/frontend-design/ | Style guidance |
| 21st.dev docs | https://21st.dev/docs | MCP reference |
| shadcn/ui | https://ui.shadcn.com | Component library |
| React Flow | https://reactflow.dev | Node-based UI library |

---

## Notes

- This skill is most effective when **brainstorming is thorough** - the more context gathered, the better the component descriptions for generation
- **Approval gates are mandatory** - never skip to autonomous generation without user sign-off on specs
- Generated components are **starting points** - expect iteration and refinement
- Works best with **Jarvis Mode active** for full MCP orchestration capabilities
