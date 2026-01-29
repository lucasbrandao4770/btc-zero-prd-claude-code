# UberEats Invoice Processing Pipeline

> AI-powered serverless invoice extraction for restaurant partner reconciliation

---

## Project Context

**Business Problem:** 3 FTEs spend 80% of time on manual data entry from delivery platform invoices, causing R$45,000+ in reconciliation errors quarterly.

**Solution:** Cloud-native serverless pipeline using Gemini 2.0 Flash for document extraction with autonomous monitoring via CrewAI.

**Critical Deadline:** April 1, 2026 (Q2 financial close)

**Requirements:** See [notes/summary-requirements.md](notes/summary-requirements.md) for consolidated requirements from 6 planning meetings.

---

## Architecture Overview

```text
INGESTION          PROCESSING                              STORAGE
─────────          ──────────                              ───────

┌───────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ TIFF  │──▶│ TIFF→PNG │──▶│ CLASSIFY │──▶│ EXTRACT  │──▶│  WRITE   │──▶ BigQuery
│ (GCS) │   │          │   │          │   │ (Gemini) │   │          │
└───────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
    │           │              │              │              │
    └───────────┴──────────────┴──────────────┴──────────────┘
                          Pub/Sub (events)

OBSERVABILITY                              AUTONOMOUS OPS
─────────────                              ──────────────

┌───────────┐  ┌───────────┐  ┌───────────┐    ┌─────────┐  ┌───────────┐  ┌──────────┐
│ LangFuse  │  │Cloud Logs │  │ Metrics   │    │ TRIAGE  │─▶│ROOT CAUSE │─▶│ REPORTER │─▶ Slack
└───────────┘  └───────────┘  └───────────┘    └─────────┘  └───────────┘  └──────────┘
```

| Stage | Technology | Purpose |
| ----- | ---------- | ------- |
| Cloud | GCP | Primary infrastructure |
| Compute | Cloud Run | Serverless functions |
| Messaging | Pub/Sub | Event-driven pipeline |
| Storage | GCS | File storage (input, processed, archive) |
| Data Warehouse | BigQuery | Extracted invoice data |
| LLM | Gemini 2.0 Flash | Document extraction |
| LLM Fallback | OpenRouter | Backup provider |
| LLMOps | LangFuse | LLM observability |
| Validation | Pydantic | Structured output validation |
| IaC | Terraform + Terragrunt | Infrastructure provisioning |
| Autonomous Ops | CrewAI | AI agents for monitoring |

---

## Project Structure

```text
btc-zero-prd-claude-code/
├── src/                           # Main source code (Python)
│   └── __init__.py
│
├── gen/                           # Code generation tools
│   └── synthetic-invoice-gen/     # Synthetic test data generator
│       └── src/invoice_gen/       # Invoice generation library
│
├── design/                        # Architecture design documents
│   └── gcp-cloud-run-fncs.md      # Cloud Run functions v2 architecture
│
├── notes/                         # Project meeting notes
│   ├── 01-business-kickoff.md
│   ├── 02-technical-architecture.md
│   ├── 03-data-pipeline-process.md
│   ├── 04-data-ml-strategy.md
│   ├── 05-devops-infrastructure.md
│   ├── 06-autonomous-dataops.md
│   └── summary-requirements.md    # Consolidated requirements
│
├── archive/                       # Historical versions
│   ├── sdd-agent-spec-v4.2.zip    # Previous SDD specification
│   └── dev-loop-v1.1.zip          # Previous Dev Loop version
│
├── .claude/                       # Claude Code ecosystem
│   ├── agents/                    # 40 specialized agents
│   │   ├── ai-ml/                 # AI/ML specialists (4)
│   │   ├── aws/                   # AWS/cloud specialists (4)
│   │   ├── code-quality/          # Code review, testing (6)
│   │   ├── communication/         # Documentation, planning (3)
│   │   ├── data-engineering/      # Spark, Lakeflow, Medallion (8)
│   │   ├── dev/                   # Dev Loop agents (2)
│   │   ├── domain/                # Project-specific agents (5)
│   │   ├── exploration/           # Codebase exploration (2)
│   │   └── workflow/              # SDD pipeline agents (6)
│   │
│   ├── commands/                  # 12 slash commands
│   │   ├── core/                  # /memory, /sync-context
│   │   ├── dev/                   # /dev (Dev Loop)
│   │   ├── knowledge/             # /create-kb
│   │   ├── review/                # /review
│   │   └── workflow/              # SDD commands
│   │
│   ├── kb/                        # Knowledge Base (8 domains)
│   │   ├── _templates/            # KB domain templates
│   │   ├── pydantic/
│   │   ├── gcp/
│   │   ├── gemini/
│   │   ├── langfuse/
│   │   ├── terraform/
│   │   ├── terragrunt/
│   │   ├── crewai/
│   │   └── openrouter/
│   │
│   ├── sdd/                       # Spec-Driven Development
│   │   ├── architecture/          # Architecture documents
│   │   ├── features/              # Active DEFINE/DESIGN docs
│   │   ├── reports/               # BUILD reports
│   │   ├── archive/               # Shipped features
│   │   ├── examples/              # Reference implementations
│   │   └── templates/             # Document templates
│   │
│   └── dev/                       # Dev Loop (Level 2)
│       ├── tasks/                 # PROMPT files
│       ├── progress/              # Session recovery
│       ├── logs/                  # Execution logs
│       ├── examples/              # Reference PROMPT examples
│       └── templates/             # PROMPT templates
│
└── .gitignore
```

---

## Development Workflows

### AgentSpec 4.1 (Spec-Driven Development)

5-phase structured workflow for features requiring traceability:

```text
/brainstorm → /define → /design → /build → /ship
  (Opus)      (Opus)    (Opus)   (Sonnet)  (Haiku)
```

| Command | Phase | Purpose |
|---------|-------|---------|
| `/brainstorm` | 0 | Explore ideas through dialogue (optional) |
| `/define` | 1 | Capture and validate requirements |
| `/design` | 2 | Create architecture and specification |
| `/build` | 3 | Execute implementation with verification |
| `/ship` | 4 | Archive with lessons learned |
| `/iterate` | Any | Update documents when changes needed |

**Artifacts:** `.claude/sdd/features/` and `.claude/sdd/archive/`

### Dev Loop (Level 2 Agentic Development)

Structured iteration with PROMPT.md files and session recovery:

```bash
# Let the crafter guide you
/dev "I want to build a date parser utility"

# Execute existing PROMPT
/dev tasks/PROMPT_DATE_PARSER.md

# Resume interrupted session
/dev tasks/PROMPT_DATE_PARSER.md --resume
```

**When to use:**
- KB building
- Prototypes
- Single features
- Utilities and parsers

---

## Agent Usage Guidelines

### Available Agents by Category

| Category | Agents | Use When |
| -------- | ------ | -------- |
| **Workflow** | brainstorm-agent, define-agent, design-agent, build-agent, ship-agent, iterate-agent | Building features with SDD |
| **Code Quality** | code-reviewer, code-cleaner, code-documenter, dual-reviewer, python-developer, test-generator | Improving code quality |
| **Data Engineering** | spark-specialist, spark-troubleshooter, spark-performance-analyzer, spark-streaming-architect, lakeflow-architect, lakeflow-expert, lakeflow-pipeline-builder, medallion-architect | Spark/Lakeflow work |
| **AI/ML** | llm-specialist, genai-architect, ai-prompt-specialist, ai-data-engineer | LLM prompts, AI systems |
| **AWS** | aws-deployer, aws-lambda-architect, lambda-builder, ci-cd-specialist | AWS deployments |
| **Communication** | adaptive-explainer, meeting-analyst, the-planner | Explanations, planning |
| **Domain** | pipeline-architect, function-developer, extraction-specialist, infra-deployer, dataops-builder | Project-specific tasks |
| **Exploration** | codebase-explorer, kb-architect | Codebase exploration, KB creation |
| **Dev** | prompt-crafter, dev-loop-executor | Dev Loop workflow |

### Agent Reference Syntax

In PROMPT.md files, reference agents with `@agent-name`:

```markdown
### CORE
- [ ] @kb-architect: Create Redis KB domain
- [ ] @python-developer: Implement cache wrapper
- [ ] @test-generator: Add unit tests
```

---

## Coding Standards

### Language: Python 3.11+

- **Style:** Ruff (line-length 100, select E/F/I/UP/B/SIM)
- **Testing:** pytest with -v --tb=short
- **Validation:** Pydantic v2 for all data models
- **Package Management:** pyproject.toml with hatchling

### Detected Patterns

| Pattern | Usage | Example |
| ------- | ----- | ------- |
| Pydantic Models | Data validation, LLM output | `gen/synthetic-invoice-gen/src/invoice_gen/schemas/` |
| Adapter Pattern | Cloud service abstraction | Architecture for multi-cloud portability |
| Event-Driven | Pipeline communication | Pub/Sub between Cloud Run functions |
| Dataclasses | Simple data containers | Invoice generation models |
| Click CLI | Command-line interfaces | `invoice-gen` CLI tool |

### Code Quality Rules

1. **Pydantic for schemas** - All extraction outputs must use Pydantic models
2. **Type hints required** - All function signatures must be typed
3. **Structured logging** - Use structured JSON logging in Cloud Run
4. **Adapter interfaces** - Use adapters for cloud services (future portability)

---

## Commands

| Command | Purpose |
| ------- | ------- |
| `/brainstorm` | Explore ideas through collaborative dialogue |
| `/define` | Capture and validate requirements |
| `/design` | Create technical architecture |
| `/build` | Execute implementation |
| `/ship` | Archive completed features |
| `/iterate` | Update documents mid-stream |
| `/dev` | Dev Loop for structured iteration |
| `/create-kb` | Create knowledge base domains |
| `/review` | Code review workflow |
| `/create-pr` | Create pull requests |
| `/memory` | Save session insights |
| `/sync-context` | Update CLAUDE.md with project context |

---

## Knowledge Base

8 MCP-validated domains with concepts, patterns, and quick references:

| Domain | Purpose | Entry Point |
| ------ | ------- | ----------- |
| **pydantic** | Data validation for LLM output parsing | `.claude/kb/pydantic/index.md` |
| **gcp** | GCP serverless data engineering | `.claude/kb/gcp/index.md` |
| **gemini** | Gemini multimodal LLM for document extraction | `.claude/kb/gemini/index.md` |
| **langfuse** | LLMOps observability platform | `.claude/kb/langfuse/index.md` |
| **terraform** | Infrastructure as Code for GCP | `.claude/kb/terraform/index.md` |
| **terragrunt** | Multi-environment orchestration | `.claude/kb/terragrunt/index.md` |
| **crewai** | Multi-agent AI orchestration | `.claude/kb/crewai/index.md` |
| **openrouter** | Unified LLM API gateway | `.claude/kb/openrouter/index.md` |

### KB Structure

```text
.claude/kb/{domain}/
├── index.md           # Domain overview
├── quick-reference.md # Cheat sheet
├── concepts/          # Core concepts
├── patterns/          # Implementation patterns
└── specs/             # YAML specifications (optional)
```

---

## MCP Tools Available

| MCP Server | Purpose |
| ---------- | ------- |
| **context7-mcp** | Library documentation lookup |
| **exa** | Code context search |
| **firecrawl** | Web scraping and crawling |
| **magic** | UI component generation |
| **ref-tools** | Documentation search |

---

## Environment Configuration

### Required Environment Variables

| Variable | Purpose |
| -------- | ------- |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID |
| `GCP_REGION` | GCP region (us-central1) |
| `LANGFUSE_PUBLIC_KEY` | LangFuse observability |
| `LANGFUSE_SECRET_KEY` | LangFuse secret |
| `OPENROUTER_API_KEY` | Fallback LLM provider |

### GCP Projects

| Environment | Project | Purpose |
| ----------- | ------- | ------- |
| dev | `invoice-pipeline-dev` | Development and testing |
| prod | `invoice-pipeline-prod` | Production workloads |

---

## Important Dates

| Date | Milestone |
| ---- | --------- |
| Jan 15, 2026 | Project kickoff |
| Feb 7, 2026 | All 4 functions implemented |
| Feb 28, 2026 | MVP demo to stakeholders |
| Mar 15, 2026 | Accuracy validation complete |
| **Apr 1, 2026** | **Production launch** |
| Apr 30, 2026 | CrewAI pilot complete |

---

## Success Metrics

| Metric | Target |
| ------ | ------ |
| Extraction accuracy | ≥ 90% |
| Processing latency P95 | < 30 seconds |
| Pipeline availability | > 99% |
| Cost per invoice | < $0.01 |
| Manual processing reduction | > 80% |

---

## Getting Help

- **Requirements:** Start with [notes/summary-requirements.md](notes/summary-requirements.md)
- **Architecture:** See [.claude/sdd/architecture/ARCHITECTURE.md](.claude/sdd/architecture/ARCHITECTURE.md)
- **Cloud Run Design:** See [design/gcp-cloud-run-fncs.md](design/gcp-cloud-run-fncs.md)
- **SDD Workflow:** See [.claude/sdd/_index.md](.claude/sdd/_index.md)
- **SDD Examples:** See [.claude/sdd/examples/](.claude/sdd/examples/)
- **Dev Loop:** See [.claude/dev/_index.md](.claude/dev/_index.md)
- **Dev Examples:** See [.claude/dev/examples/](.claude/dev/examples/)
- **Agents:** Browse [.claude/agents/](.claude/agents/)
- **KB Index:** See [.claude/kb/_index.yaml](.claude/kb/_index.yaml)

---

## Version History

| Date | Changes |
| ---- | ------- |
| 2026-01-29 | Sync: Added design/, archive/, examples folders; updated agent counts per category |
| 2026-01-29 | Initial CLAUDE.md created via /sync-context |
