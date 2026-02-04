# BRAINSTORM: MedFlow Visualizer MVP

> **Phase:** 0 - Brainstorming | **Status:** Ready for /define
> **Created:** 2026-02-04 | **Deadline:** 2026-02-05 (TOMORROW!)
> **Stakes:** Contract depends on this presentation

---

## Executive Summary

Build a **read-only visualization tool** for pre-processed clinical billing data. The tool displays:
1. **Final Results** with evidence from medical records and AI justifications
2. **Rules Engine** showing which rules activated and why

**Critical Constraints:**
- NO real-time processing - read pre-processed data from Supabase only
- Use mock data for development (no processed samples in DB yet)
- Beautiful, responsive UI - this presentation determines contract closure
- Authenticate via Supabase Auth (webapp user with read-only access)

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

All agents in subsequent phases MUST read these files from `medflow-visualizer/notes/`:

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

### Screen 0: Attendance Selection (Navigation)

**Purpose:** Allow users to find and select a processed attendance

**Features:**
- **Smart list view** with search/filter capabilities
- **Local cache** validated on startup for performance
- **Metadata processing** on startup (tags, status, dates)
- **Columns:** numero_atendimento, tipo_conta, status, created_at
- **Filter by:** tipo_conta (clinico/cirurgico), status, date range
- **Search:** by numero_atendimento

**Implementation Notes:**
- Use IndexedDB or localStorage for cache
- Validate cache against Supabase on startup
- Process additional tags/metadata during sync
- Limit displayed rows (pagination or virtual scrolling)

### Screen 1: Final Results View

**Purpose:** Display the final billing result with evidence and justifications

**Tab 1: Evidence Display**
- **Default view:** Grouped accordion by category (10 categories)
  - Diagnoses, Medications, Patient History, Patient Condition
  - Exam Results, Therapeutic Plan, Vitals, Diet
  - Exams Performed, Therapeutic Procedures
- **Toggle options:** Switch to tabs or flat chronological list
- Each evidence shows:
  - Description (what was found)
  - Source document name
  - Date extracted
- Collapsible sections for large categories

**Tab 2: Justifications Display**
- Main diagnosis (procedimento_principal)
  - Name, justification
  - CID-10 mapping with justification
  - SIGTAP mapping with justification
- Secondary diagnoses with justifications
- Hospitalization summary (`resumo_internacao`)
- Timeline (`linha_do_tempo`)
- Scope parameters (is_gestante, tipo_parto, etc.)

**Tab 3: Billing Summary**
- `lista_faturamento` - Final billing codes
- Processing metrics (time spent, steps completed)

### Screen 2: Rules Engine View

**Purpose:** Show which rules were activated and why

**Content:**
- **Hierarchy view:** Chapter → Group → Category scopes
- Chapter scope rules (e.g., "gestante" -> O00-O99)
- Group scope rules (e.g., "parto_hospitalar" -> O80-O84)
- Category scope rules (e.g., "cesariana_eletiva" -> O82)
- **Effective scope** (most restrictive, final result)
- For each rule:
  - Rule name
  - Activated CID-10 interval
  - Justification (evidence that triggered it)
- `scope_parameters` display (clinical flags like is_gestante)

### What's NOT in MVP

- ❌ Real-time processing
- ❌ SSE streaming
- ❌ FastAPI backend
- ❌ Step-by-step flow visualization
- ❌ Processing new attendances
- ❌ Document upload
- ❌ AWS CodeArtifact integration (not needed)

---

## Technical Approach

### Architecture (Simplified from Previous Plans)

```
React UI (Lovable/medflow-visualizer)
         |
         | Direct Supabase Client
         v
    Supabase Auth
         |
         v
    Supabase DB (read-only)
    - contas_faturadas.result (JSONB)
```

**Key Insight:** No backend needed! The React app can:
1. Authenticate user via Supabase Auth
2. Query `contas_faturadas` directly
3. Parse the JSONB `result` field
4. Display evidence and rules

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
# Already configured in .env
VITE_SUPABASE_URL=https://wqqicdvcuihdkwjyvufq.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
HOSPITAL_ID=047089be-2165-4af9-b933-433de1f2a850

# For authenticated access
WEBAPP_USER_EMAIL=<configured>
WEBAPP_USER_PASSWORD=<configured>
```

### Data Source

**For Development:** Use mock data in `notes/samples/`:
- `mock-atendimento-clinico.json` - Complete sample
- `mock-resultados-ia.json` - Just AI results

**For Demo:**
- Option A: Continue with mock data (recommended if no processed samples)
- Option B: Process one sample with clinical flow, then visualize

### Key Data Structures

**Design Principle:** Use FlowState/FlowOutput required fields as baseline, but design UI to dynamically handle extra fields. This prevents breaking when schema evolves.

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

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | **Attendance selection** - List/search processed attendances | P0 |
| FR-002 | **Local cache** - Cache attendance list, validate on startup | P0 |
| FR-003 | Display final CID-10 result with name and justification | P0 |
| FR-004 | Display evidence grouped by 10 categories (accordion default) | P0 |
| FR-005 | Toggle evidence view (accordion/tabs/flat list) | P1 |
| FR-006 | Display SIGTAP mapping with justification | P0 |
| FR-007 | Display activated rules per scope level (chapter/group/category) | P0 |
| FR-008 | Show rule justification (why it activated) | P0 |
| FR-009 | Display scope_parameters (clinical flags) | P1 |
| FR-010 | Navigate between Results and Rules views | P1 |
| FR-011 | Show hospitalization summary/timeline | P1 |
| FR-012 | Show billing summary (lista_faturamento) | P1 |
| FR-013 | Show processing metrics (time, steps) | P2 |
| FR-014 | Handle dynamic/extra fields gracefully | P1 |
| FR-015 | Responsive design for demo presentation | P1 |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | Page load time | < 2 seconds |
| NFR-002 | Visual polish | Demo-ready, professional |
| NFR-003 | Mobile responsive | Works on tablet |
| NFR-004 | Loading states | Spinners during data fetch |
| NFR-005 | Error handling | Graceful error messages |
| NFR-006 | Cache performance | < 500ms list render |

### Constraints

| ID | Constraint |
|----|------------|
| C-001 | Must work with mock data (fallback if no DB samples) |
| C-002 | Deadline: Feb 5, 2026 |
| C-003 | Read-only - no data modification |
| C-004 | Use existing Lovable codebase |
| C-005 | Design for FlowOutput schema flexibility |

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

```
medflow-visualizer/
├── notes/
│   ├── planning-artifacts-analysis.md     # Requirements evolution
│   ├── codebase-flow-internacao-clinica.md # Workflow schemas
│   ├── codebase-faturamento-core.md       # API patterns
│   ├── codebase-medflow-visualizer.md     # Current UI
│   ├── supabase-schema-analysis.md        # DB schema
│   └── samples/
│       ├── mock-atendimento-clinico.json  # Full sample
│       ├── mock-api-response.json         # API format
│       ├── mock-resultados-ia.json        # AI results only
│       └── mock-data-schema-summary.json  # Schema docs
├── scripts/
│   ├── generate_mock_data.py              # Mock generator
│   └── analyze_sample_data.py             # Data analysis
└── .env                                   # All env vars configured
```

---

## AI Data Engineer Review Outcomes

**Review Status:** CONDITIONAL PASS → RESOLVED

### Critical Issues (Resolved)

| Issue | Resolution |
|-------|------------|
| JSONB Schema Mismatch | **Clarified:** FlowState/FlowOutput is the actual structure. Design for required fields + dynamic extras |
| Missing Screen 0 | **Added:** Attendance selection with local cache, search/filter |
| TypeScript Interfaces Incomplete | **Updated:** Full interfaces matching mock data structure |
| 10 Evidence Categories | **Decided:** Grouped accordion (default) + view toggle |

### Warnings Addressed

| Warning | Resolution |
|---------|------------|
| No loading/error states | Added NFR-004, NFR-005 |
| scope_parameters not in UI | Added FR-009 |
| Execution logs excluded | Added FR-013 (P2) |

### Tech Debt Acknowledged

- Frontend auth with hardcoded credentials (acceptable for demo)
- Mock data placeholders need realistic content for demo polish

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
*Reviewed: 2026-02-04 by ai-data-engineer agent*
*Agent: Brainstorm Phase (Manual orchestration)*
*Ready for: /define phase*
