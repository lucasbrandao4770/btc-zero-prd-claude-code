# SDD Feature Examples

> Additional examples from the AgentSpec archive

---

## Overview

This document showcases features built using SDD, demonstrating different patterns and scales.

---

## Example 1: GCS Upload Integration

### Context

Adding GCS upload capability to the synthetic invoice generator.

| Attribute | Value |
|-----------|-------|
| **Feature** | GCS_UPLOAD |
| **Duration** | 1 day |
| **Phases** | Define → Design → Build → Ship (no Brainstorm) |
| **Complexity** | Medium |

### Define Summary

```markdown
## Problem Statement
The invoice generator creates test data locally, but production
testing requires files in GCS. Manual upload is error-prone.

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Upload generated invoices to GCS bucket |
| **MUST** | Maintain local file generation |
| **SHOULD** | Support batch uploads |

## Success Criteria
| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Upload success rate | 100% for valid files |
| SC-002 | Upload latency | <5s per file |

## Clarity Score: 13/15
```

### Design Highlights

```markdown
## Architecture
Generator → Local File → GCS Adapter → GCS Bucket

## File Manifest
| # | File | Purpose |
|---|------|---------|
| 1 | gen/adapters/gcs.py | GCS upload adapter |
| 2 | gen/cli.py | Add --upload flag |
| 3 | tests/test_gcs.py | Upload tests |

## Key Decision: Adapter Pattern
Same adapter pattern as main pipeline for consistency.
Enables future providers (S3, Azure Blob) without CLI changes.
```

### Lessons Learned

- **Reusing patterns accelerates development** - Adapter pattern from main pipeline worked perfectly
- **Small scope = fast delivery** - 1 day with full documentation
- **Skip Brainstorm for clear requests** - Requirements were explicit from start

---

## Example 2: LangFuse Observability

### Context

Adding LLM observability to track extraction performance.

| Attribute | Value |
|-----------|-------|
| **Feature** | LANGFUSE_OBSERVABILITY |
| **Duration** | 1 day |
| **Phases** | Define → Design → Build → Ship |
| **Complexity** | Medium |

### Define Summary

```markdown
## Problem Statement
No visibility into LLM extraction performance. Cannot debug
accuracy issues or optimize prompts without observability.

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Track all Gemini API calls |
| **MUST** | Record input/output pairs |
| **MUST** | Capture latency metrics |
| **SHOULD** | Enable prompt comparison |

## Success Criteria
| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Trace coverage | 100% of LLM calls |
| SC-002 | Dashboard load time | <3s |

## Clarity Score: 14/15
```

### Design Highlights

```markdown
## Integration Point
LLM Adapter → LangFuse Client → LangFuse Cloud

## Code Pattern
```python
from langfuse import Langfuse

langfuse = Langfuse()

def extract_with_trace(image: bytes, vendor: str) -> Invoice:
    trace = langfuse.trace(name="invoice_extraction")
    span = trace.span(name="gemini_call")

    try:
        result = gemini_client.extract(image)
        span.end(output=result.model_dump())
        return result
    except Exception as e:
        span.end(status_message=str(e), level="ERROR")
        raise
```
```

### Lessons Learned

- **Observability as separate feature** - Keeps core pipeline clean
- **Wrapper pattern for tracing** - Minimal invasive to existing code
- **Cloud service = simpler infra** - No self-hosted observability overhead

---

## Example 3: Smoke Test Framework

### Context

Building end-to-end testing framework for pipeline validation.

| Attribute | Value |
|-----------|-------|
| **Feature** | SMOKE_TEST |
| **Duration** | 1 day |
| **Phases** | Define → Design → Build → Ship |
| **Complexity** | Medium-High |

### Define Summary

```markdown
## Problem Statement
No automated way to verify full pipeline works after deployment.
Manual testing is time-consuming and error-prone.

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Test full pipeline end-to-end |
| **MUST** | Validate extraction accuracy |
| **MUST** | Report pass/fail with details |
| **SHOULD** | Support multiple test scenarios |

## Acceptance Tests
| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Happy path | Test invoice | Run smoke test | All stages pass |
| AT-002 | Accuracy check | Known invoice | Extract | Fields match ground truth |
| AT-003 | Error handling | Invalid file | Run test | Failure reported correctly |

## Clarity Score: 14/15
```

### Design Highlights

```markdown
## Architecture
```text
CLI → Stage Runner → [Generate, Upload, Process, Validate, BigQuery, Logging]
                                           ↓
                                    Test Report
```

## File Manifest
| # | File | Purpose |
|---|------|---------|
| 1 | tests/smoke/cli.py | CLI interface |
| 2 | tests/smoke/runner.py | Stage orchestrator |
| 3 | tests/smoke/stages/generate.py | Generate test data |
| 4 | tests/smoke/stages/upload.py | Upload to GCS |
| 5 | tests/smoke/stages/process.py | Trigger pipeline |
| 6 | tests/smoke/stages/validate.py | Validate extraction |
| 7 | tests/smoke/stages/bigquery.py | Check BigQuery |
| 8 | tests/smoke/stages/logging.py | Check logs |
```

### Lessons Learned

- **Stage-based architecture** - Easy to add/remove test stages
- **Dataclass for results** - Clean result aggregation
- **Ground truth comparison** - Essential for accuracy validation

---

## Example 4: Terraform/Terragrunt Infrastructure

### Context

Infrastructure as Code for reproducible deployments.

| Attribute | Value |
|-----------|-------|
| **Feature** | TERRAFORM_TERRAGRUNT_INFRA |
| **Duration** | 1 day |
| **Phases** | Define → Design → Build → Ship |
| **Complexity** | High |

### Define Summary

```markdown
## Problem Statement
Manual gcloud deployments are error-prone and not reproducible.
Team members deploy differently, causing environment drift.

## Goals
| Priority | Goal |
|----------|------|
| **MUST** | Codify all GCP resources |
| **MUST** | Support dev/staging/prod environments |
| **MUST** | Enable terraform plan before apply |
| **SHOULD** | Use least-privilege IAM |

## Success Criteria
| ID | Criterion | Target |
|----|-----------|--------|
| SC-001 | Resource coverage | 100% of pipeline resources |
| SC-002 | Plan/apply cycle | <5 minutes |
| SC-003 | Environment parity | Identical configs except variables |

## Clarity Score: 15/15
```

### Design Highlights

```markdown
## Module Structure
```text
infra/
├── modules/
│   ├── bigquery/       # Dataset + tables
│   ├── cloud-run/      # Functions + triggers
│   ├── gcs/            # Buckets
│   ├── iam/            # Service accounts
│   ├── pubsub/         # Topics + subscriptions
│   └── secrets/        # Secret Manager
└── environments/
    └── prod/
        ├── bigquery/terragrunt.hcl
        ├── cloud-run/terragrunt.hcl
        └── ...
```

## Key Decision: Module per Resource Type
Enables independent lifecycle management.
Team can update buckets without touching functions.
```

### Lessons Learned

- **Terragrunt for DRY** - Eliminated HCL duplication across environments
- **Module boundaries matter** - Wrong boundaries = painful refactoring
- **IAM is complex** - Dedicated module prevented permission sprawl

---

## Pattern Summary

### What These Examples Show

| Pattern | Examples Using It |
|---------|------------------|
| **Adapter Pattern** | GCS_UPLOAD, LANGFUSE |
| **Stage-Based Architecture** | SMOKE_TEST |
| **Module Decomposition** | TERRAFORM_TERRAGRUNT |
| **Skip Brainstorm** | All 4 (clear requirements) |
| **1-Day Delivery** | All 4 (focused scope) |

### Common Success Factors

1. **Clear problem statements** - Numbers and specifics
2. **Focused scope** - One feature per SDD cycle
3. **Reusable patterns** - Adapter, module, stage
4. **High Clarity Scores** - 13-15/15 across all
5. **Immediate lessons capture** - Ship phase documents learning

---

## Archive Locations

```text
.claude/sdd/archive/
├── GCS_UPLOAD/
│   ├── DEFINE_GCS_UPLOAD.md
│   ├── DESIGN_GCS_UPLOAD.md
│   ├── BUILD_REPORT_GCS_UPLOAD.md
│   └── SHIPPED_2026-01-31.md
├── LANGFUSE_OBSERVABILITY/
│   └── ...
├── SMOKE_TEST/
│   └── ...
└── TERRAFORM_TERRAGRUNT_INFRA/
    └── ...
```

---

## When to Reference These Examples

| Situation | Reference |
|-----------|-----------|
| Adding cloud integration | GCS_UPLOAD |
| Adding observability | LANGFUSE_OBSERVABILITY |
| Building test frameworks | SMOKE_TEST |
| Setting up IaC | TERRAFORM_TERRAGRUNT_INFRA |
| Complex multi-function pipeline | INVOICE_PIPELINE |

---

*All examples demonstrate: Define → Design → Build → Ship in 1-4 days with full documentation.*
