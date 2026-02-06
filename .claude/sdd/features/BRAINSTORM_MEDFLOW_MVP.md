# BRAINSTORM: MedFlow Visualizer MVP

> **External Repo:** `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer`

> **Phase:** 0 - Brainstorming | **Status:** Ready for /define
> **Created:** 2026-02-04 | **Updated:** 2026-02-05 (v1.3 - Corrected external repo path)
> **Deadline:** 2026-02-05 (TODAY!)
> **Stakes:** Contract depends on this presentation

---

## Executive Summary

### MAJOR UPDATE: UI Already Implemented!

**Pesdrinho (Pedro) already built the visualization UI** (Commit 7cbeed0, Feb 5, 2026):
- **2,931 lines of code** added
- 6 reusable components (EvidenceCard, RuleCard, ResultSummary, etc.)
- 2 pages (Results at `/results/:contaId`, RulesExplorer at `/rules`)
- 2 data hooks with Supabase + mock fallback
- Complete TypeScript types
- High-quality mock data for development

**See full analysis:** `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer\notes\pesdrinho-code-analysis.md`

### Remaining Work (Data Connection Only)

| Task | Effort | Priority |
|------|--------|----------|
| Verify schema alignment (TS types vs FlowOutput) | Low | P0 |
| Add Supabase Auth (webapp user login) | Medium | P0 |
| ~~Supabase Storage RLS setup~~ ✅ DONE (migration applied) | ~~Low~~ | ✅ |
| **Supabase Storage SDK integration** (download from `complete_result_path`) | Low | P0 |
| Test/fix transform functions for real data | Medium | P1 |
| Ensure hospitalId filtering works | Low | P1 |
| **FK joins** (atendimentos, hospitals tables via Supabase select) | Low | P1 |
| **Filter by `tipo_conta = 'clinico'`** | Low | P1 |
| **RulesExplorer with real data** (connect to flags/rules in FlowOutput) | Medium | P1 |

**Critical Constraints:**
- NO real-time processing - read pre-processed data only
- Use existing mock data for demo (realistic and complete)
- UI is already beautiful and responsive
- Connect via Supabase Auth (webapp user credentials in .env)
- **Supabase Storage SDK** for FlowOutput downloads (NOT raw S3 API)
- **RLS policies** for read-only access (least privilege principle)

---

## CRITICAL: Defensive Development Instructions

**These instructions MUST be propagated to ALL subsequent SDD phases (/define, /design, /build, /ship):**

### Quality Gates

1. **Review Each Step** - Spawn an `ai-data-engineer` agent to act as senior staff reviewer
   - Get brutal, honest feedback on every step
   - Iterate until passing review before proceeding
   - Document review outcomes

2. **Approval Checkpoints** - Stop and ask user approval at:
   - Major architectural decisions
   - Before writing significant code
   - Before creating/modifying multiple files
   - When encountering ambiguity

3. **Communication** - Be educational and communicative:
   - Explain what you're doing and why
   - Teach the user about the SDD workflow
   - At end of each step, concisely explain what to do next

4. **MVP Focus** - Simple is better than complex:
   - Avoid over-engineering
   - No features beyond explicit requirements
   - Use existing patterns from codebase

### Data Understanding Requirements

**BEFORE implementing any data display:**
1. Understand the REAL data schemas (Pydantic models in flow-internacao-clinica)
2. Use mock data generated from schemas for development
3. Never query entire DB (hundreds of thousands of samples)
4. Use `ai-data-engineer` agents for any Supabase interactions
5. Filter by `hospital_id` for RLS compliance

### Available Tools (USE THEM!)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `lovable` skill | UI prototyping workflow | Rapid React component iteration |
| `ui-forge` skill | Autonomous UI generation | Complex component creation |
| `ui-prototyper` agent | React component generation | Detailed component specs |
| Magic MCP | AI component builder | shadcn/ui compositions |
| Context7 MCP | Documentation lookup | Library best practices |
| Playwright MCP | Visual testing | UI validation |
| `frontend-design` plugin | Distinctive UI | Avoid generic AI aesthetics |

### Context Files (MUST READ)

All agents in subsequent phases MUST read these files from the EXTERNAL repo at `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer\notes\`:

| File | Content |
|------|---------|
| `planning-artifacts-analysis.md` | Full requirements evolution (Jan 22 - Feb 2) |
| `codebase-flow-internacao-clinica.md` | Workflow architecture, data models |
| `codebase-faturamento-core.md` | API patterns, auth flow |
| `codebase-medflow-visualizer.md` | Current UI state |
| `supabase-schema-analysis.md` | Database schema |
| `samples/mock-*.json` | Mock data for development |

---

## Requirements Evolution Summary

### Timeline

| Date | Phase | Key Change |
|------|-------|------------|
| Jan 22 | Initial | Ambitious n8n-like debugger with real-time SSE |
| Jan 30 | Planning | Lovable + Cloud Code workflow, Notoria branding |
| Jan 31 | Architecture | FastAPI + SSE, Langfuse, "observability as read-only" |
| **Feb 2** | **PIVOT** | **NO real-time! Pre-processed data only, new screen focus** |

### Final Requirements (Feb 2 - Supersedes All Previous)

From Lucas Brandao team messages:

```
Entrega 05/02:
- Protótipo funcional (MVP) com as funcionalidades principais de visualização
- NÃO VAMOS PROCESSAR REAL TIME -> Vamos apenas ler atendimentos pré-processados (read-only supabase)
- Trazer uma tela nova para visualização do resultado final, destacando evidências e justificativas
- Trazer uma tela nova para visualização das regras ativadas para um atendimento
- UI bonita e responsiva, UX satisfatória

Importante: essa apresentação é o que vai definir se o contrato vai fechar ou não
```

---

## MVP Scope

### What Pesdrinho Already Built (COMPLETE)

| Component | Status | Features |
|-----------|--------|----------|
| `AtendimentoSelector` | ✅ Done | Combobox with search, status dots, account type badges |
| `EvidenceCard` | ✅ Done | Document excerpt, highlighting, AI justification, confidence |
| `EvidenceTimeline` | ✅ Done | Grouping by date or source, collapsible sections |
| `ResultSummary` | ✅ Done | CID principal/secundarios, procedures, metrics, validation |
| `RuleCard` | ✅ Done | Status badge (applied/blocked/modified), evidence links |
| `RulesList` | ✅ Done | Filtering by result type, category badges |
| `Results` page | ✅ Done | Full results view at `/results/:contaId` |
| `RulesExplorer` page | ✅ Done | Rules catalog at `/rules` with search |
| `useAtendimentos` hook | ✅ Done | Fetch with Supabase + mock fallback |
| `useContasFaturadas` hook | ✅ Done | Fetch + transform with mock fallback |
| TypeScript types | ✅ Done | 10+ interfaces in `src/types/results.ts` |
| Mock data | ✅ Done | 2 realistic test cases (obstetric, surgical) |
| Supabase client | ✅ Done | Configured with env vars + auto-mock in dev |

### What Remains (Data Connection)

| Task | Component | Details |
|------|-----------|---------|
| **Schema Verification** | Types vs FlowOutput | Verify `ContaFaturadaResultJSON` matches actual Python output |
| **Auth Flow** | New | Add Supabase Auth login with webapp credentials |
| **hospitalId Context** | Hooks | Get hospitalId from auth context, not hardcoded |
| **Transform Testing** | Hooks | Test `transformContaFaturada()` with real data structure |
| **Rules Explorer Data** | Page | Currently mock-only, may need real hook |

### Screen 0: Attendance Selection ✅ BUILT

**Component:** `AtendimentoSelector` (157 lines)
- Combobox using shadcn Command (cmdk)
- Status indicator dots (green/yellow/red)
- Account type badges
- Search by numero_atendimento
- Uses `useContasFaturadas` hook

### Screen 1: Final Results View ✅ BUILT

**Page:** `Results.tsx` (189 lines) at `/results/:contaId`

**Evidence Display** (`EvidenceTimeline` + `EvidenceCard`):
- Groups by date or source (toggleable)
- Each card shows: documentText, highlightedText, justification
- Source icons by document type
- Confidence badges (high/medium/low)
- Collapsible AI justification

**Results Summary** (`ResultSummary`):
- CID principal with confidence + justification
- CIDs secundarios list
- Procedures with SIGTAP codes and values
- Total value, processing time
- Validation messages with status

### Screen 2: Rules Engine View ✅ BUILT

**Page:** `RulesExplorer.tsx` (311 lines) at `/rules`

**Features:**
- Search rules by name/description
- Filter by category (capitulo, grupo, categoria, procedimento, validacao)
- `RuleCard` shows: name, description, category badge, evidence links
- Status colors: green (applied), red (blocked), amber (modified)
- Collapsible evidence list per rule

### What's NOT in MVP (Confirmed Out of Scope)

- ❌ Real-time processing (read pre-processed only)
- ❌ SSE streaming (not needed)
- ❌ FastAPI backend (direct Supabase)
- ❌ Step-by-step flow visualization (deferred)
- ❌ Processing new attendances (read-only)
- ❌ Document upload (read-only)
- ❌ Export to PDF/Excel (deferred)
- ❌ Comparison between accounts (deferred)

### What's NOW in MVP (Thanks to Pesdrinho)

- ✅ Evidence display with timeline grouping
- ✅ Rules display with filtering
- ✅ CID/SIGTAP display with confidence
- ✅ Attendance selector with search
- ✅ Mock data fallback
- ✅ Responsive UI with shadcn/ui

---

## Technical Approach

### Architecture (Simplified from Previous Plans)

```
React UI (Lovable/medflow-visualizer)
         |
         | Supabase JS Client (anon key + RLS)
         v
    Supabase Auth (webapp user login)
         |
         +------------------+------------------+
         |                  |                  |
         v                  v                  v
    contas_faturadas   atendimentos      hospitals
    (main results)     (via FK join)     (via FK join)
         |
         | complete_result_path column
         v
    Supabase Storage (via Storage SDK + RLS)
    - bucket: result.faturado (NOT result-faturamento!)
    - content: Full FlowOutput JSON
    - RLS: Joins on complete_result_path = storage.objects.name
```

**Data Flow:**
1. Query `contas_faturadas` with FK joins to `atendimentos` and `hospitals`
2. Filter by `tipo_conta = 'clinico'` and `hospital_id`
3. Use `result` column for quick summary display
4. Use `complete_result_path` to download full FlowOutput from Supabase Storage
5. Parse FlowOutput for evidences, rules, detailed justifications

**Key Insight:** No backend needed! The React app can:
1. Authenticate user via Supabase Auth
2. Query `contas_faturadas` with FK joins (single query)
3. Download FlowOutput from Storage via SDK (RLS-protected)
4. Parse and display evidence and rules

### Authentication Flow

```typescript
// 1. Login with webapp credentials
const { data, error } = await supabase.auth.signInWithPassword({
  email: process.env.VITE_WEBAPP_USER_EMAIL,
  password: process.env.VITE_WEBAPP_USER_PASSWORD
});

// 2. Query is now authenticated, RLS applies
const { data: results } = await supabase
  .from('contas_faturadas')
  .select('*')
  .eq('hospital_id', hospitalId);
```

### Environment Variables

```env
# Supabase Database
VITE_SUPABASE_URL=https://wqqicdvcuihdkwjyvufq.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...

# Hospital context
VITE_HOSPITAL_ID=047089be-2165-4af9-b933-433de1f2a850

# Webapp user for authenticated access
VITE_WEBAPP_USER_EMAIL=<configured>
VITE_WEBAPP_USER_PASSWORD=<configured>

# Supabase Storage (for FlowOutput download)
VITE_SUPABASE_S3_ENDPOINT_URL=<configured>
VITE_SUPABASE_S3_REGION=<configured>
VITE_SUPABASE_S3_ACCESS_KEY_ID=<configured>
VITE_SUPABASE_S3_SECRET_ACCESS_KEY=<to be added>
VITE_SUPABASE_S3_BUCKET_NAME_RESULT_FATURAMENTO=<configured>

# Note: Using Storage SDK + RLS is preferred over raw S3 credentials
# The S3 vars above are for reference; actual implementation uses Storage SDK
```

### Data Pipeline Context (How Data Gets to Supabase)

Understanding the upstream pipeline helps clarify what data we're reading:

```
1. faturamento_core → FlowInput → faturamento lambda
2. faturamento lambda → flow_internacao_clinica (runner.py translate_input)
3. runner.py → flow.py (initializes CrewAI Flow + FlowState)
4. CrewAI Flow processes documents → persists to FlowState
5. flow.py → runner.py (translate_output creates FlowOutput from FlowState)
6. runner.py → faturamento lambda (returns FlowOutput)
7. faturamento lambda:
   - Saves FULL FlowOutput to Supabase Storage bucket → stores path in `complete_result_path`
   - Saves CONCISE result to `result` column (for webapp UI consumption)
```

**Key Insight:** The `result` column has a **small, webapp-optimized** output. For the visualizer, we need the **full FlowOutput** from Storage to access:
- All 10 evidence categories
- Detailed justifications
- Applied rules and flags
- Complete CID/SIGTAP mappings

### Data Access Pattern

When reading from `contas_faturadas`:

1. **Filter:** `tipo_conta = 'clinico'` (clinical flow only for now)
2. **FK Joins:**
   - `atendimento_id` → `atendimentos` table (numero_atendimento, tipo_atendimento, data_entrada, data_alta, data_internacao)
   - `hospital_id` → `hospitals` table (name, cnes)
3. **Quick display:** Use `result` column for summary
4. **Full details:** Download `complete_result_path` from Storage for evidences, rules, etc.

### Data Source

**For Development:** Use mock data in `notes/samples/`:
- `mock-atendimento-clinico.json` - Complete sample
- `mock-resultados-ia.json` - Just AI results

**For Demo:**
- Option A: Continue with mock data (recommended if no processed samples)
- Option B: Process one sample with clinical flow, then visualize

### Key Data Structures

**CRITICAL UPDATE:** We traced the actual data flow from FlowOutput → Supabase.
**See full analysis:** `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer\notes\flowoutput-data-flow-analysis.md`

**Design Principle:** Use FlowOutput required fields as baseline, but design UI to dynamically handle extra fields. This prevents breaking when schema evolves.

**Pesdrinho's transforms need rewriting** - his mock assumes a flat Portuguese structure, but actual FlowOutput has:
- 10 nested evidence categories (not flat `evidencias[]`)
- CID codes wrapped in `Suggested<T>` (access via `.entity.code`, `.justificativa`)
- Procedures in single array with `incluir_no_faturamento` boolean filter

**Large text handling required** - justifications can be 10-50+ lines. Use collapsible text or "Read more".

From `flow-internacao-clinica` Pydantic schemas (see `schemas/flow.py`):

```typescript
// Evidence with source document (from clinical_evidences)
interface Evidence {
  description: string;  // alias: name
  date: string;
  source_document_name: string;
  source_document?: {
    doc_type: string;
    content: string;
    size: number;
  };
}

// 10 Evidence Categories (from ClinicalEvidences)
interface ClinicalEvidences {
  diagnoses: Diagnosis[];      // extends Evidence + type
  medications: Medication[];   // extends Evidence + dose, route, frequency
  patient_history: Evidence[];
  patient_condition: Evidence[];
  exam_results: Evidence[];
  therapeutic_plan: Evidence[];
  vitals: Evidence[];
  diet: Evidence[];
  exams_performed: Evidence[];
  therapeutic_procedures: Evidence[];
}

// Justification wrapper (from shared/wrappers.py)
interface Suggested<T> {
  entity: T | null;
  justificativa: string | null;
}

// Main result (from ResultadoFinalCID10)
interface ResultadoFinalCID10 {
  procedimento_principal: {
    nome: string;
    justificativa: string;
    mapeamento_CID10: Suggested<CID10Category>;
    mapeamento_SIGTAP: Suggested<CodigoSIGTAP>;
    possiveis_cid10_encontrados: PossiveisCID10Encontrados;
    incluir_no_faturamento: boolean;
  };
  procedimentos_secundarios: CID10ProcedimentoSecundario[];
  condicoes_adquiridas: CID10CondicaoAdquirida[];
}

// Rules hierarchy (from RuleEngineScope)
interface RuleEngineScope {
  chapter_scope: CID10Scope;
  group_scope: CID10Scope;
  category_scope: CID10Scope;
  scope_parameters: Record<string, any>;  // e.g., is_gestante, tipo_parto
  effective_scope: CID10Scope;  // computed, most restrictive
}

// Each scope level (from CID10Scope)
interface CID10Scope {
  activated_intervals: CID10Interval[];
  justified_intervals: Suggested<CID10Interval>[];  // interval + justificativa
  accepted_rules: RuleProtocol[];
  covered_intervals: CID10Interval[];
}
```

**Dynamic Field Handling:**
- Render known fields with specific components
- Unknown/extra fields render as expandable JSON or key-value list
- This handles FlowOutput schema flexibility

---

## Exploration Questions (Resolved)

| Question | Answer |
|----------|--------|
| Import clinical flow code? | **NO** - Data already in Supabase, no processing needed |
| Need AWS CodeArtifact? | **NO** - Not importing any packages |
| What env vars needed? | `VITE_SUPABASE_*`, `WEBAPP_USER_*`, `HOSPITAL_ID` |
| Real-time SSE? | **NO** - Read pre-processed data only |
| Backend needed? | **NO** - Direct Supabase client in React |
| Mock data available? | **YES** - Generated in `notes/samples/` |

---

## Selected Approach

### Option C: Direct Supabase + Mock Data (RECOMMENDED)

**Why:**
1. Simplest architecture - no backend to build/deploy
2. Mock data ready for immediate development
3. Auth pattern matches production (Supabase Auth)
4. Can switch to real data when processed samples available
5. Fastest path to Feb 5 deadline

**Implementation:**
1. Add Supabase client to React app
2. Create auth context/hook
3. Build Evidence display component
4. Build Rules display component
5. Create responsive layout
6. Polish UI with Notoria branding

---

## Draft Requirements for /define

### UI Requirements (✅ COMPLETE - Pesdrinho)

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | Attendance selection with search | ✅ `AtendimentoSelector` |
| FR-002 | Display final CID-10 with justification | ✅ `ResultSummary` |
| FR-003 | Display evidence grouped by source/date | ✅ `EvidenceTimeline` |
| FR-004 | Evidence cards with highlighting | ✅ `EvidenceCard` |
| FR-005 | Display SIGTAP procedures with values | ✅ `ResultSummary` |
| FR-006 | Display activated rules with status | ✅ `RuleCard` + `RulesList` |
| FR-007 | Filter rules by result type | ✅ `RulesList` |
| FR-008 | Rules explorer with search | ✅ `RulesExplorer` page |
| FR-009 | Confidence badges | ✅ Throughout |
| FR-010 | Validation messages display | ✅ `ResultSummary` |
| FR-011 | Processing metrics (time) | ✅ `ResultSummary` |
| FR-012 | Responsive sidebar navigation | ✅ `AppSidebar` |

### Data Connection Requirements (🔧 REMAINING WORK)

| ID | Requirement | Priority | Effort |
|----|-------------|----------|--------|
| DC-001 | **Supabase Auth login** - Authenticate with webapp credentials | P0 | Medium |
| DC-002 | **Transform rewrite** - Adapt Pesdrinho's transforms to FlowOutput schema | P0 | **High** |
| DC-003 | **Evidence flattening** - Flatten 10 categories into single array with tags | P0 | Medium |
| DC-004 | **CID extraction** - Handle Suggested wrapper (`.entity.code`, `.justificativa`) | P0 | Medium |
| DC-005 | **hospitalId from auth** - Get from user context, not hardcoded | P1 | Low |
| DC-006 | **Large text handling** - Collapsible text for 10+ line justifications | P1 | Medium |
| DC-007 | **Error handling** - Handle auth failures, network errors | P1 | Low |
| DC-008 | **Rules from Flags** - Map `flags[]` to rules display (RulesExplorer page) | **P1** | Medium |
| DC-009 | **Supabase Storage download** - Use Storage SDK to fetch FlowOutput from `complete_result_path` | P0 | Low |
| DC-010 | **FK joins** - Single Supabase query joining `atendimentos` and `hospitals` tables | P1 | Low |
| DC-011 | **Filter tipo_conta** - Only fetch rows where `tipo_conta = 'clinico'` | P1 | Low |
| DC-012 | **Storage RLS setup** - ✅ DONE (migration 20260205192037) - Bucket: `result.faturado` | P0 | ✅ Done |
| DC-013 | **End-to-end validation** - Test full path: Storage download → JSON parse → transform → UI render | P1 | Low |

**Key Schema Differences (Pesdrinho vs FlowOutput):**

| UI Field | Pesdrinho Expected | Actual FlowOutput Path |
|----------|-------------------|------------------------|
| Evidence | `evidencias[]` (flat) | `informacoes_faturamento.evidencias_clinicas.{10 categories}[]` |
| CID Code | `cid_principal.codigo` | `informacoes_faturamento.resultado_cid10.procedimento_principal.mapeamento_CID10.entity.code` |
| CID Justification | `cid_principal.justificativa` | `...mapeamento_CID10.justificativa` |
| Rules | `regras_ativadas[]` | `flags[]` (different structure - uses Flag model) |

### Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-001 | Page load time < 2s | ✅ React Query caching |
| NFR-002 | Visual polish | ✅ shadcn/ui + Tailwind |
| NFR-003 | Mobile responsive | ✅ Responsive design |
| NFR-004 | Loading states | ✅ Implemented in hooks |
| NFR-005 | Error handling | ⚠️ Needs auth error handling |
| NFR-006 | Mock fallback | ✅ Auto-mock in dev mode |

### Constraints

| ID | Constraint |
|----|------------|
| C-001 | Must work with mock data (auto-fallback exists) |
| C-002 | Deadline: Feb 5, 2026 (TODAY) |
| C-003 | Read-only - no data modification |
| C-004 | Use existing Pesdrinho codebase (rewrite transforms only) |
| C-005 | Auth via webapp user (credentials in .env) |
| C-006 | **Supabase Storage access** - Full FlowOutput in `result-faturamento` bucket, accessed via Storage SDK + RLS |
| C-007 | **Least privilege** - Use anon key + RLS, NOT service role key or raw S3 credentials |
| C-008 | **RLS setup** - ✅ Versioned migrations created (20260205192037, 20260205192817) |

---

## YAGNI Analysis (Features Removed)

| Feature | Reason for Removal |
|---------|-------------------|
| Real-time SSE streaming | Not needed - read pre-processed data |
| FastAPI backend | Not needed - direct Supabase |
| Step-by-step visualization | Deferred - focus on final results |
| Document upload | Not in MVP scope |
| Processing new attendances | Not in MVP scope |
| Langfuse integration | Deferred - observability for later |
| Model switching | Not relevant for read-only |

---

## Next Steps

### Immediate (After This Document)

1. **Run `/define`** with this BRAINSTORM as input
   ```
   /define .claude/sdd/features/BRAINSTORM_MEDFLOW_MVP.md
   ```

2. **Define agent will:**
   - Read this document and context files
   - Extract formal requirements
   - Create DEFINE document with acceptance criteria
   - Get AI data engineer review

### SDD Workflow Continuation

```
/brainstorm ✅ (this document)
     ↓
/define → DEFINE_MEDFLOW_MVP.md
     ↓
/design → DESIGN_MEDFLOW_MVP.md
     ↓
/build → Code + BUILD_REPORT
     ↓
/ship → Archive
```

---

## Appendix: Context File Locations

> **Note:** `medflow-visualizer` is an EXTERNAL repository located at:
> `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer`

```
D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer\
├── notes/
│   ├── flowoutput-data-flow-analysis.md   # ⭐ CRITICAL: Actual schema + field mapping
│   ├── pesdrinho-code-analysis.md         # Analysis of Pedro's UI code
│   ├── planning-artifacts-analysis.md     # Requirements evolution
│   ├── codebase-flow-internacao-clinica.md # Workflow schemas
│   ├── codebase-faturamento-core.md       # API patterns
│   ├── codebase-medflow-visualizer.md     # Current UI (pre-Pesdrinho)
│   ├── supabase-schema-analysis.md        # DB schema
│   └── samples/
│       ├── mock-atendimento-clinico.json  # Full sample
│       ├── mock-api-response.json         # API format
│       ├── mock-resultados-ia.json        # AI results only
│       └── mock-data-schema-summary.json  # Schema docs
├── src/
│   ├── components/results/                # ⭐ Pesdrinho's components
│   ├── hooks/                             # ⭐ useAtendimentos, useContasFaturadas
│   ├── pages/                             # ⭐ Results.tsx, RulesExplorer.tsx
│   ├── types/results.ts                   # ⭐ TypeScript interfaces
│   ├── data/mockResultsData.ts            # ⭐ Mock data
│   └── lib/supabase.ts                    # ⭐ Supabase client
├── scripts/
│   └── generate_mock_data.py              # Our mock generator
└── .env                                   # All env vars configured
```

---

## AI Data Engineer Review Outcomes

**Review Status:** ✅ **APPROVED** (2026-02-05, v1.2 - RLS migration completed)

### Review 1: Initial Issues (Resolved)

| Issue | Resolution |
|-------|------------|
| JSONB Schema Mismatch | **Clarified:** FlowState/FlowOutput is the actual structure |
| Missing Screen 0 | **Added:** Attendance selection spec |
| TypeScript Interfaces | **Updated:** Full interfaces matching mock data |
| 10 Evidence Categories | **Decided:** Grouped accordion + toggle |

### Review 2: Scope Change (Pesdrinho's Code)

**Major Update:** On Feb 5, discovered Pesdrinho already implemented the UI!

| Previous Scope | New Scope |
|----------------|-----------|
| Build all UI components | ✅ Already built |
| Build all pages | ✅ Already built |
| Build data hooks | ✅ Already built |
| Define TypeScript types | ✅ Already done |
| Add mock data | ✅ Already done |
| **Remaining:** | Data connection only |

### Review 3: Data Architecture Clarifications (v1.1)

**Key clarifications from user:**

| Topic | Clarification |
|-------|---------------|
| **RulesExplorer scope** | IS in scope for demo → DC-008 upgraded to P1 |
| **Storage access** | Required for full FlowOutput (evidences, rules, etc.) |
| **Storage method** | Supabase Storage SDK + RLS (NOT raw S3 API) |
| **Security approach** | Least privilege: anon key + RLS policies |
| **Data location** | `result` column = concise; `complete_result_path` = full FlowOutput in Storage |
| **FK joins needed** | atendimentos (attendance metadata), hospitals (name, CNES) |
| **Filter required** | `tipo_conta = 'clinico'` for clinical flow only |

**New requirements added:** DC-009 (Storage download), DC-010 (FK joins), DC-011 (tipo_conta filter), DC-012 (Storage RLS)

**New constraints added:** C-007 (least privilege), C-008 (versioned migrations)

### RLS Implementation Notes (from migration 20260205192037)

**Storage access pattern:**
```typescript
// complete_result_path must match storage.objects.name exactly
const { data, error } = await supabase.storage
  .from('result.faturado')  // <-- correct bucket name
  .download(complete_result_path);  // <-- path from DB, not full URL
```

**User role requirement:**
- Webapp user needs `app_metadata.role = 'web_app'` or `'dev'` to read all hospitals
- If role is `'erp'`, user only sees their own hospital's data
- Current webapp user credentials should have appropriate role set

**Performance optimization included:**
- Index on `complete_result_path` for efficient JOINs
- Auth functions use `(SELECT)` wrapper for 1,100x faster RLS evaluation

### Tech Debt Acknowledged

- Frontend auth with hardcoded credentials (acceptable for demo)
- Transform functions assume specific JSON structure (needs verification)
- RulesExplorer uses mock-only data (upgraded to P1 - will connect to real data)
- ~~Dashboard RLS for demo~~ → ✅ Versioned migrations already created!
- DC-002 transform work is HIGH effort - **explicit fallback: if transforms incomplete, demo proceeds with mock data (C-001)**

---

## Validation Checklist

- [x] Minimum 3 discovery questions asked (architecture, data, auth)
- [x] Sample collection completed (mock data generated)
- [x] At least 2 approaches explored (SSE vs direct, backend vs no backend)
- [x] YAGNI applied (7 features removed)
- [x] Requirements evolution documented
- [x] Selected approach justified
- [x] Draft requirements included
- [x] Context files documented
- [x] Defensive instructions included
- [x] **AI Data Engineer review completed**
- [x] **Review issues resolved**
- [x] **User decisions documented**

---

*Generated: 2026-02-04*
*Reviewed: 2026-02-04 by ai-data-engineer agent (v1.0)*
*Updated: 2026-02-05 (v1.1) - Data architecture clarifications*
*Reviewed: 2026-02-05 by ai-data-engineer agent (v1.1) - APPROVED*
*Updated: 2026-02-05 (v1.2) - RLS migration verified (commit 628f8d8)*
*Updated: 2026-02-05 (v1.3) - Corrected external repo path*
*Agent: Brainstorm Phase (Manual orchestration)*
*Ready for: /define phase*
