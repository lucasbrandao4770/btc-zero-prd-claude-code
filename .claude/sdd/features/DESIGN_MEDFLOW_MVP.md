# DESIGN: MedFlow Visualizer MVP

> Technical design for connecting Pesdrinho's UI to real Supabase data

> **External Repo:** `D:\Workspace\BANQUETE\Faturamento IA\Repositorios\medflow-visualizer`

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | MEDFLOW_MVP |
| **Date** | 2026-02-05 |
| **Author** | design-agent |
| **DEFINE** | [DEFINE_MEDFLOW_MVP.md](./DEFINE_MEDFLOW_MVP.md) |
| **Status** | Ready for Build |

---

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        MEDFLOW VISUALIZER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [React App]                                                             │
│       │                                                                  │
│       ├─► useAuth ─────────────► Supabase Auth                          │
│       │                              │                                   │
│       │                         [JWT with claims]                        │
│       │                              │                                   │
│       └─► useContasFaturadas ───► Supabase DB ◄─── RLS (hospital_id)   │
│                │                     │                                   │
│                │              contas_faturadas                          │
│                │              ├── result (JSONB)  ◄─── Path B: Full     │
│                │              └── complete_result_path ─┐               │
│                │                                        │               │
│                └─► Storage SDK ─────────────────────────┘               │
│                        │                                                 │
│                        ▼                                                 │
│                  result.faturado bucket                                 │
│                  └── FlowOutput JSON ◄─── Path A: Full data            │
│                                                                          │
│  [Transform Layer]                                                       │
│       │                                                                  │
│       ├─► flowOutputTransformer ─► Flatten evidences (10 categories)   │
│       ├─► extractCID ────────────► Unwrap Suggested<T>                  │
│       └─► mapFlags ──────────────► Convert to ActivatedRule[]          │
│                                                                          │
│  [UI Components] (Already Built by Pesdrinho)                           │
│       │                                                                  │
│       ├─► Results.tsx ──────► ResultSummary + EvidenceTimeline          │
│       ├─► RulesExplorer.tsx ► RulesList + RuleCard                      │
│       └─► AtendimentoSelector                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| `useAuth` hook | Supabase Auth login | @supabase/supabase-js |
| `useContasFaturadas` hook | Query + Storage download | React Query + Supabase |
| `flowOutputTransformer` | FlowOutput → UI types | TypeScript |
| `evidenceFlattener` | 10 categories → flat array | TypeScript |
| Existing UI components | Display results | React + shadcn/ui |

---

## Key Decisions

### Decision 1: Two-Path Data Strategy

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-02-05 |

**Context:** The upstream pipeline stores data in two ways:
- **Path A (Lambda):** Concise `result` column + full FlowOutput in S3 (`complete_result_path`)
- **Path B (Worker):** Full FlowOutput directly in `result` column

**Choice:** Support both paths with automatic detection:
1. Check if `result` has full structure (Path B)
2. If not, fetch from Storage using `complete_result_path` (Path A)
3. Fall back to mock data if both fail

**Rationale:** Defensive approach ensures demo works regardless of which path was used.

**Consequences:**
- Slightly more complex hook logic
- Graceful degradation built-in

---

### Decision 2: Transform in Hook, Not Component

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-02-05 |

**Context:** FlowOutput structure differs significantly from UI types.

**Choice:** Transform data in `useContasFaturadas` hook, not in components.

**Rationale:**
- Components receive ready-to-render data
- Single transformation point
- Easier testing
- Matches existing Pesdrinho pattern

**Alternatives Rejected:**
1. Transform in components - Rejected: duplicated logic, harder to test
2. Create separate transform hook - Rejected: over-engineering for MVP

---

### Decision 3: Auth via Environment Variables (Demo)

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted (temporary) |
| **Date** | 2026-02-05 |

**Context:** Need Supabase Auth for RLS to work.

**Choice:** Auto-login using `VITE_WEBAPP_USER_EMAIL` and `VITE_WEBAPP_USER_PASSWORD` from .env.

**Rationale:** Fastest path for demo. No login UI needed.

**Consequences:**
- Credentials in .env (acceptable for demo)
- Tech debt: Replace with proper login UI post-demo

---

### Decision 4: Minimal New Files

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-02-05 |

**Context:** Deadline is TODAY. Must minimize changes.

**Choice:**
- Add transform logic to existing `useContasFaturadas.ts`
- Create only essential new files (auth hook, types)
- NO new UI components (Pesdrinho's are complete)

**Rationale:** Risk reduction. Fewer files = fewer things to break.

---

## File Manifest

| # | File | Action | Purpose | Dependencies |
|---|------|--------|---------|--------------|
| 1 | `src/lib/supabase.ts` | Modify | Add auth initialization | None |
| 2 | `src/hooks/useAuth.ts` | Create | Supabase Auth hook | 1 |
| 3 | `src/types/flowOutput.ts` | Create | FlowOutput TypeScript types | None |
| 4 | `src/lib/transforms.ts` | Create | Transform functions | 3 |
| 5 | `src/hooks/useContasFaturadas.ts` | Modify | Add Storage download + transforms | 1, 3, 4 |
| 6 | `src/types/results.ts` | Modify | Add missing fields if needed | None |
| 7 | `src/App.tsx` | Modify | Add AuthProvider wrapper | 2 |

**Total Files:** 7 (3 create, 4 modify)

---

## Code Patterns

### Pattern 1: Supabase Auth Hook

```typescript
// src/hooks/useAuth.ts
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import type { User } from '@supabase/supabase-js';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const initAuth = async () => {
      if (!supabase) {
        setLoading(false);
        return;
      }

      // Check existing session
      const { data: { session } } = await supabase.auth.getSession();

      if (session?.user) {
        setUser(session.user);
        setLoading(false);
        return;
      }

      // Auto-login with env credentials
      const email = import.meta.env.VITE_WEBAPP_USER_EMAIL;
      const password = import.meta.env.VITE_WEBAPP_USER_PASSWORD;

      if (email && password) {
        const { data, error: authError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (authError) {
          console.error('Auth error:', authError);
          setError(authError);
        } else {
          setUser(data.user);
        }
      }

      setLoading(false);
    };

    initAuth();
  }, []);

  return { user, loading, error, isAuthenticated: !!user };
}
```

### Pattern 2: Storage Download

```typescript
// In useContasFaturadas.ts
async function downloadFlowOutput(path: string): Promise<FlowOutput | null> {
  if (!supabase) return null;

  try {
    const { data, error } = await supabase.storage
      .from('result.faturado')
      .download(path);

    if (error) {
      console.error('Storage download error:', error);
      return null;
    }

    const text = await data.text();
    return JSON.parse(text) as FlowOutput;
  } catch (e) {
    console.error('FlowOutput parse error:', e);
    return null;
  }
}
```

### Pattern 3: Evidence Flattener

```typescript
// src/lib/transforms.ts
import type { FlowOutput, ClinicalEvidences } from '@/types/flowOutput';
import type { Evidence } from '@/types/results';

const EVIDENCE_CATEGORIES = [
  'diagnoses', 'medications', 'patient_history', 'patient_condition',
  'exam_results', 'therapeutic_plan', 'vitals', 'diet',
  'exams_performed', 'therapeutic_procedures'
] as const;

export function flattenEvidences(clinicalEvidences: ClinicalEvidences): Evidence[] {
  const result: Evidence[] = [];

  for (const category of EVIDENCE_CATEGORIES) {
    const items = clinicalEvidences[category] || [];

    for (const item of items) {
      result.push({
        id: `${category}-${result.length}`,
        documentText: item.source_document?.content || '',
        highlightedText: item.description,
        justification: '', // May not exist in all categories
        source: item.source_document_name,
        documentType: item.source_document?.doc_type || category,
        timestamp: item.date,
        relatedCodes: [],
        confidence: 0.8, // Default confidence
        category, // NEW: Add category tag
      });
    }
  }

  return result;
}
```

### Pattern 4: CID Extraction from Suggested<T>

```typescript
// src/lib/transforms.ts
import type { Suggested, CID10Category } from '@/types/flowOutput';
import type { CIDCode } from '@/types/results';

export function extractCID(
  suggested: Suggested<CID10Category> | null | undefined,
  isPrincipal: boolean = false
): CIDCode | null {
  if (!suggested?.entity) return null;

  return {
    codigo: suggested.entity.code,
    descricao: suggested.entity.name,
    capitulo: suggested.entity.chapter || '',
    grupo: suggested.entity.group || '',
    categoria: suggested.entity.category || '',
    confidence: 0.9, // Default
    isPrincipal,
    justification: suggested.justificativa || '',
    evidences: [],
  };
}
```

### Pattern 5: Flags to Rules Mapper

```typescript
// src/lib/transforms.ts
import type { Flag } from '@/types/flowOutput';
import type { ActivatedRule } from '@/types/results';

export function mapFlagsToRules(flags: Flag[]): ActivatedRule[] {
  return flags.map((flag, index) => ({
    id: `flag-${index}`,
    ruleName: flag.tipo,
    ruleDescription: flag.valor?.toString() || '',
    category: 'validacao' as const,
    evidences: [],
    justification: flag.justificativa || '',
    result: 'applied' as const,
  }));
}
```

### Pattern 6: Main Transform Function

```typescript
// src/lib/transforms.ts
export function transformFlowOutput(
  row: ContaFaturadaRow,
  flowOutput: FlowOutput | null
): ContaFaturadaResult {
  // If no FlowOutput, try to use result column
  const data = flowOutput || row.result as FlowOutput | null;

  if (!data) {
    // Return minimal result with error status
    return {
      id: row.id,
      contaId: row.conta_id,
      // ... minimal fields
      status: 'error',
      validationMessages: ['Dados não disponíveis'],
    };
  }

  const info = data.informacoes_faturamento;

  // Flatten evidences
  const evidences = info?.evidencias_clinicas
    ? flattenEvidences(info.evidencias_clinicas)
    : [];

  // Extract CID
  const cidPrincipal = info?.resultado_cid10?.procedimento_principal?.mapeamento_CID10
    ? extractCID(info.resultado_cid10.procedimento_principal.mapeamento_CID10, true)
    : null;

  // Map flags to rules
  const activatedRules = data.flags
    ? mapFlagsToRules(data.flags)
    : [];

  // ... rest of transformation

  return {
    id: row.id,
    contaId: row.conta_id,
    atendimentoId: row.atendimento_id,
    hospitalId: row.hospital_id,
    tipoConta: row.tipo_conta as ContaFaturadaResult['tipoConta'],
    numeroAtendimento: '',
    numeroConta: '',
    cidPrincipal,
    cidsSecundarios: [],
    procedures: [],
    evidences,
    activatedRules,
    totalValue: 0,
    timeSpentSeconds: row.time_spent_seconds || 0,
    processedAt: row.created_at,
    status: data.is_success ? 'success' : 'error',
    validationMessages: data.error_message ? [data.error_message] : undefined,
  };
}
```

---

## Data Flow

```text
1. App.tsx loads
   │
   ▼
2. useAuth() auto-logs in with env credentials
   │
   ▼
3. User navigates to /results/:contaId
   │
   ▼
4. useContasFaturadas() queries Supabase:
   │
   ├─► SELECT * FROM contas_faturadas
   │   JOIN atendimentos, hospitals
   │   WHERE tipo_conta = 'clinico'
   │
   ▼
5. For each row:
   │
   ├─► Check: Does result column have full FlowOutput?
   │   │
   │   ├── YES (Path B) ──► Use result directly
   │   │
   │   └── NO (Path A) ───► Download from Storage:
   │                        supabase.storage
   │                          .from('result.faturado')
   │                          .download(complete_result_path)
   │
   ▼
6. transformFlowOutput(row, flowOutput)
   │
   ├─► flattenEvidences() - 10 categories → Evidence[]
   ├─► extractCID() - Suggested<T> → CIDCode
   └─► mapFlagsToRules() - Flag[] → ActivatedRule[]
   │
   ▼
7. Returns ContaFaturadaResult[] to UI
   │
   ▼
8. Components render (already built by Pesdrinho)
```

---

## Integration Points

| External System | Integration Type | Authentication |
|-----------------|-----------------|----------------|
| Supabase Auth | SDK | Email/Password (env vars) |
| Supabase DB | SDK + RLS | JWT (from Auth) |
| Supabase Storage | SDK + RLS | JWT (from Auth) |

---

## Testing Strategy

| Test Type | Scope | Files | Tools | Coverage Goal |
|-----------|-------|-------|-------|---------------|
| Manual | Full flow | - | Browser | Happy path + fallback |
| Unit | Transform functions | `transforms.test.ts` | vitest | Core transforms |
| Integration | Hook + Supabase | - | Manual | Auth + query + download |

**MVP Testing Priority:**
1. ✅ Manual test: Mock data fallback works
2. ✅ Manual test: Auth login succeeds
3. ✅ Manual test: Storage download works
4. ✅ Manual test: Transforms render correctly

---

## Error Handling

| Error Type | Handling Strategy | Retry? |
|------------|-------------------|--------|
| Auth failure | Log + continue with mock | No |
| DB query error | Log + return mock data | No |
| Storage download fail | Log + use result column | No |
| Transform error | Log + skip item | No |
| JSON parse error | Log + return null | No |

**Fallback Chain:**
```
Storage FlowOutput → result column → mock data
```

---

## Configuration

| Config Key | Type | Default | Description |
|------------|------|---------|-------------|
| `VITE_SUPABASE_URL` | string | - | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | string | - | Supabase anon key |
| `VITE_WEBAPP_USER_EMAIL` | string | - | Auto-login email |
| `VITE_WEBAPP_USER_PASSWORD` | string | - | Auto-login password |
| `VITE_HOSPITAL_ID` | string | - | Default hospital filter |
| `VITE_FORCE_MOCK_DATA` | bool | false | Force mock mode |

---

## Security Considerations

- ✅ RLS policies enforce hospital_id filtering (already deployed)
- ✅ Anon key + RLS (not service role key)
- ⚠️ Credentials in .env (acceptable for demo, fix post-demo)
- ✅ Read-only access (no mutations)
- ✅ Storage RLS restricts bucket access

---

## Observability

| Aspect | Implementation |
|--------|----------------|
| Logging | Console.log with emoji prefixes (🔍, ✅, ❌) |
| Errors | Caught and logged, graceful fallback |
| Performance | React Query caching (5 min stale time) |

---

## Build Sequence

Execute in this order:

```text
1. src/types/flowOutput.ts      ─── Create FlowOutput types
2. src/lib/transforms.ts        ─── Create transform functions
3. src/lib/supabase.ts          ─── Modify: add auth helpers
4. src/hooks/useAuth.ts         ─── Create auth hook
5. src/hooks/useContasFaturadas.ts ─── Modify: integrate transforms + storage
6. src/App.tsx                  ─── Modify: add AuthProvider
7. Manual Testing               ─── Verify full flow
```

---

## Acceptance Test Mapping

| AT | File(s) | Verification |
|----|---------|--------------|
| AT-001 | useAuth.ts | Console shows login success |
| AT-002 | useContasFaturadas.ts | List filters by tipo_conta |
| AT-003 | transforms.ts | Results page shows data |
| AT-004 | transforms.ts (flattenEvidences) | Evidence cards render |
| AT-005 | transforms.ts (extractCID) | CID shows code + justification |
| AT-006 | transforms.ts (mapFlagsToRules) | Rules page works |
| AT-007 | useContasFaturadas.ts | Storage download completes |
| AT-008 | useContasFaturadas.ts | Falls back to mock |
| AT-009 | useContasFaturadas.ts | Join data shows |
| AT-010 | (existing UI) | Text is collapsible |
| AT-011 | transforms.ts | Handles missing fields |

---

## Build Notes (From Review)

> Issues identified during ai-data-engineer review. Address during /build phase.

### Must Address

| # | Issue | Where | Fix |
|---|-------|-------|-----|
| 1 | Path detection logic undefined | Data Flow step 5 | Add `hasFullFlowOutput()` helper to detect if result column has full FlowOutput structure |
| 2 | Pattern 6 incomplete | `transformFlowOutput` | Complete the function with all field mappings |
| 3 | Storage path format unclear | Pattern 2 | Clarify if `complete_result_path` has leading slash |

### Should Address

| # | Issue | Where | Fix |
|---|-------|-------|-----|
| 4 | Hardcoded confidence values | Pattern 3, 4 | Extract from FlowOutput if available, or document as intentional defaults |
| 5 | .env security not mentioned | Decision 3 | Ensure `.env` in `.gitignore`, create `.env.example` |

### Detection Helper (Copy-paste ready)

```typescript
// Add to src/lib/transforms.ts
const hasFullFlowOutput = (result: unknown): result is FlowOutput => {
  return (
    result !== null &&
    typeof result === 'object' &&
    'informacoes_faturamento' in result
  );
};
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-02-05 | iterate-agent | Added Build Notes from review |
| 1.0 | 2026-02-05 | design-agent | Initial version |

---

## Next Step

**Ready for:** `/build .claude/sdd/features/DESIGN_MEDFLOW_MVP.md`
