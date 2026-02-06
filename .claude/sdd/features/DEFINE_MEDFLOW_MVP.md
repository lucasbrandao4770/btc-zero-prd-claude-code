# DEFINE: MedFlow Visualizer MVP

> **External Repo:** `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer`

> Connect Pesdrinho's UI to real Supabase data for healthcare billing result visualization demo

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | MEDFLOW_MVP |
| **Date** | 2026-02-05 |
| **Author** | define-agent (from BRAINSTORM_MEDFLOW_MVP.md v1.3) |
| **Status** | Ready for Design |
| **Clarity Score** | 15/15 |
| **Source** | `.claude/sdd/features/BRAINSTORM_MEDFLOW_MVP.md` |

---

## Problem Statement

The MedFlow Visualizer UI is already built (2,931 lines by Pesdrinho), but it uses mock data. **The contract-deciding demo is TODAY (Feb 5, 2026)** and requires connecting the UI to real pre-processed healthcare billing data from Supabase. Without this data connection, we cannot demonstrate the value of the AI billing system to stakeholders.

---

## Target Users

| User | Role | Pain Point |
|------|------|------------|
| **Demo Stakeholders** | Contract decision-makers | Need to see AI billing results in action to approve contract |
| **Healthcare Billing Analysts** | Future daily users | Currently spend 80% of time on manual data entry; need to review AI-extracted evidences and rules |
| **Hospital IT Staff** | System administrators | Need confidence that system respects hospital data boundaries (RLS) |

---

## Goals

What success looks like (prioritized):

| Priority | Goal |
|----------|------|
| **MUST** | Display pre-processed billing results from `contas_faturadas` table |
| **MUST** | Download and parse full FlowOutput from Supabase Storage (`result.faturado` bucket) |
| **MUST** | Show evidences grouped by category with AI justifications |
| **MUST** | Show activated rules on RulesExplorer page |
| **MUST** | Authenticate via Supabase Auth (webapp user credentials) |
| **MUST** | Fall back to mock data if real data unavailable |
| **SHOULD** | Get hospital metadata via FK joins (atendimentos, hospitals) |
| **SHOULD** | Filter to `tipo_conta = 'clinico'` only |
| **SHOULD** | Handle large justification text (collapsible) |
| **COULD** | Polish error handling for auth/network failures |

---

## Success Criteria

Measurable outcomes:

- [x] ~~RLS policies deployed~~ ✅ Done (migration 20260205192037)
- [ ] User can authenticate with webapp credentials
- [ ] Results page (`/results/:contaId`) displays real data from Supabase
- [ ] Evidence cards show data from all 10 FlowOutput categories
- [ ] RulesExplorer (`/rules`) displays rules from `flags[]` array
- [ ] FlowOutput downloads from Storage in < 3 seconds
- [ ] Mock fallback activates automatically when real data unavailable
- [ ] Demo runs successfully for stakeholders

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Auth Login | App is loaded | User credentials auto-login | User is authenticated, RLS applies |
| AT-002 | List Attendances | User is authenticated | App loads attendance list | Shows `contas_faturadas` filtered by `tipo_conta='clinico'` |
| AT-003 | View Results | User selects an attendance | Results page loads | Shows CID, SIGTAP, evidences from FlowOutput |
| AT-004 | Evidence Display | FlowOutput downloaded | Evidence section renders | All 10 categories flattened into timeline with tags |
| AT-005 | CID Extraction | FlowOutput has `Suggested<CID10>` | CID displays | Shows `.entity.code` and `.justificativa` correctly |
| AT-006 | Rules Display | User navigates to `/rules` | RulesExplorer loads | Shows rules from `flags[]` with status badges |
| AT-007 | Storage Download | `complete_result_path` exists | App fetches FlowOutput | Downloads via Storage SDK, parses JSON |
| AT-008 | Mock Fallback | Real data unavailable | App detects failure | Falls back to mock data, shows warning |
| AT-009 | FK Joins | Query executes | Results include metadata | Shows hospital name, CNES, attendance dates |
| AT-010 | Large Text | Justification > 10 lines | Text renders | Shows collapsible "Read more" UI |
| AT-011 | Partial FlowOutput | FlowOutput missing optional fields | Transform executes | Renders available data, gracefully omits missing |

---

## Out of Scope

Explicitly NOT included in this MVP:

- Real-time processing (read pre-processed only)
- SSE streaming
- FastAPI backend
- Step-by-step flow visualization
- Processing new attendances
- Document upload
- Export to PDF/Excel
- Comparison between accounts
- Surgical flow (`tipo_conta = 'cirurgico'`)
- Building new UI components (Pesdrinho's code is complete)

---

## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| **Timeline** | Deadline: Feb 5, 2026 (TODAY) | No time for new features, focus on data connection only |
| **Codebase** | Use existing Pesdrinho UI (rewrite transforms only) | Cannot restructure components, only adapt data layer |
| **Security** | Least privilege: anon key + RLS, NOT service role | Must use Storage SDK with RLS, not raw S3 credentials |
| **Data** | Read-only access | No INSERT/UPDATE/DELETE operations |
| **Auth** | Webapp user needs `role: 'web_app'` or `'dev'` | User must have correct app_metadata for cross-hospital access |
| **Bucket** | Storage bucket is `result.faturado` (NOT `result-faturamento`) | Correct bucket name critical for downloads |
| **Fallback** | Must work with mock data (C-001) | If transforms incomplete, demo uses mocks |

---

## Technical Context

> Essential context for Design phase - prevents misplaced files and missed infrastructure needs.
> **Note:** This feature targets an EXTERNAL repository, NOT this btc-zero-prd-claude-code repo.

| Aspect | Value | Notes |
|--------|-------|-------|
| **Deployment Location** | `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer\src\` | React frontend, Vite build (EXTERNAL REPO) |
| **KB Domains** | N/A (not in btc-zero repo) | Uses Supabase JS SDK patterns |
| **IaC Impact** | ✅ None - RLS already deployed | Migrations 20260205192037, 20260205192817 applied |

**Key Files to Modify (in external repo):**

| File | Change |
|------|--------|
| `D:\...\medflow-visualizer\src\hooks\useContasFaturadas.ts` | Add FK joins, tipo_conta filter, Storage download |
| `D:\...\medflow-visualizer\src\hooks\useAuth.ts` | New - Supabase Auth login |
| `D:\...\medflow-visualizer\src\lib\supabase.ts` | Verify Storage SDK configuration |
| `D:\...\medflow-visualizer\src\lib\transforms.ts` | New - FlowOutput → UI type transforms |
| `D:\...\medflow-visualizer\src\types\results.ts` | May need updates for FlowOutput fields |

**Data Flow:**

```
1. Auth: supabase.auth.signInWithPassword(webapp_credentials)
2. Query: supabase.from('contas_faturadas')
   .select('*, atendimentos(*), hospitals(*)')
   .eq('tipo_conta', 'clinico')
3. Storage: supabase.storage.from('result.faturado').download(complete_result_path)
4. Transform: FlowOutput → ContaFaturadaResultJSON (flatten evidences, extract CID)
5. Render: Existing Pesdrinho components
```

---

## Functional Requirements

### P0 - Must Have (Demo Blockers)

| ID | Requirement | Component | Acceptance |
|----|-------------|-----------|------------|
| DC-001 | Supabase Auth login with webapp credentials | `useAuth` hook | AT-001 |
| DC-002 | Transform FlowOutput to UI types | `transforms.ts` | AT-003, AT-005 |
| DC-003 | Flatten 10 evidence categories into array with tags | `transforms.ts` | AT-004 |
| DC-004 | Extract CID from `Suggested<T>` wrapper | `transforms.ts` | AT-005 |
| DC-009 | Download FlowOutput via Storage SDK | `useContasFaturadas` | AT-007 |
| DC-012 | ~~Storage RLS setup~~ | ✅ DONE | N/A |

### P1 - Should Have (Demo Quality)

| ID | Requirement | Component | Acceptance |
|----|-------------|-----------|------------|
| DC-005 | Get hospitalId from auth context | `useAuth` | AT-002 |
| DC-006 | Collapsible text for large justifications | UI components | AT-010 |
| DC-007 | Error handling for auth/network | Hooks | AT-008 |
| DC-008 | Map `flags[]` to rules display | `transforms.ts` | AT-006 |
| DC-010 | FK joins (atendimentos, hospitals) | `useContasFaturadas` | AT-009 |
| DC-011 | Filter `tipo_conta = 'clinico'` | `useContasFaturadas` | AT-002 |
| DC-013 | End-to-end validation test | Manual | All ATs |

---

## Schema Mapping Reference

Critical for DC-002/DC-003/DC-004 transforms:

| UI Field | Pesdrinho Expected | Actual FlowOutput Path |
|----------|-------------------|------------------------|
| Evidence list | `evidencias[]` (flat) | `informacoes_faturamento.evidencias_clinicas.{diagnoses,medications,...}[]` |
| CID code | `cid_principal.codigo` | `informacoes_faturamento.resultado_cid10.procedimento_principal.mapeamento_CID10.entity.code` |
| CID justification | `cid_principal.justificativa` | `...mapeamento_CID10.justificativa` |
| Rules | `regras_ativadas[]` | `flags[]` (Flag model with different structure) |

---

## Assumptions

Assumptions that if wrong could invalidate the design:

| ID | Assumption | If Wrong, Impact | Validated? |
|----|------------|------------------|------------|
| A-001 | Webapp user has `role: 'web_app'` or `'dev'` in app_metadata | Cannot read cross-hospital data | [ ] Verify before demo |
| A-002 | `complete_result_path` contains valid Storage object path | Cannot download FlowOutput | [ ] Need processed sample |
| A-003 | FlowOutput JSON structure matches Pydantic schemas | Transform functions fail | [ ] Test with real data |
| A-004 | Supabase Storage SDK works with `result.faturado` bucket | Downloads fail | [ ] Test after RLS |
| A-005 | At least one processed sample exists for demo | Nothing to display | [ ] Process sample or use mock |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| No processed samples available | Use mock data fallback (C-001) |
| Transform functions fail with real data | Demo proceeds with mock data |
| Storage download fails | Show `result` column data (concise version) |
| Auth fails | Have backup credentials ready |

---

## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---------|-------------|-------|
| Problem | 3 | Crystal clear: contract demo today, need data connection |
| Users | 3 | Three personas identified with specific pain points |
| Goals | 3 | 10 prioritized goals with MUST/SHOULD/COULD |
| Success | 3 | 8 measurable criteria with acceptance tests |
| Scope | 3 | 10 explicit exclusions, YAGNI applied |
| **Total** | **15/15** | Ready for Design |

---

## Open Questions

None - ready for Design.

All questions were resolved during BRAINSTORM:
- ✅ RulesExplorer in scope (DC-008 at P1)
- ✅ Storage method: SDK + RLS (not raw S3)
- ✅ Bucket name: `result.faturado`
- ✅ RLS migrations: Applied (20260205192037, 20260205192817)

---

## Context Files

Design phase MUST read these files from the EXTERNAL repo at `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\`:

| File | Purpose |
|------|---------|
| `medflow-visualizer\notes\flowoutput-data-flow-analysis.md` | ⭐ CRITICAL: Schema mapping details |
| `medflow-visualizer\notes\pesdrinho-code-analysis.md` | Existing component structure |
| `medflow-visualizer\notes\supabase-schema-analysis.md` | Database schema reference |
| `medflow-visualizer\src\types\results.ts` | Current TypeScript types |
| `medflow-visualizer\src\hooks\useContasFaturadas.ts` | Hook to modify |
| `medflow-visualizer\src\data\mockResultsData.ts` | Mock data structure reference |
| `flow-internacao-clinica\schemas\flow.py` | Source Pydantic schemas |

---

## Defensive Development (Propagated from BRAINSTORM)

**Quality Gates:**
1. Spawn `ai-data-engineer` agent for senior review
2. Stop for approval at major decisions
3. Be educational and communicative
4. MVP focus - no over-engineering

**Mock Fallback Rule:**
If transforms incomplete by demo time, proceed with mock data (C-001). UI quality is already proven.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-05 | define-agent | Initial version from BRAINSTORM v1.2 |
| 1.1 | 2026-02-05 | define-agent | Fixed AT-09→AT-009 typo, added AT-011, expanded context files (ai-data-engineer review) |
| 1.2 | 2026-02-05 | iterate-agent | Corrected external repo path |

---

## Next Step

**Ready for:** `/design .claude/sdd/features/DEFINE_MEDFLOW_MVP.md`
