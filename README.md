# UberEats Invoice Processing Pipeline

> AI-powered serverless invoice extraction with 40+ specialized Claude Code agents for restaurant partner reconciliation

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![GCP](https://img.shields.io/badge/cloud-GCP-4285F4.svg)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This project automates invoice data extraction using **Gemini 2.0 Flash** for document processing, deployed on **GCP serverless infrastructure**. It includes a comprehensive **Claude Code agent ecosystem** with 40 specialized AI agents, 8 knowledge base domains, and structured development workflows.

**Business Impact:**
- **Problem:** 3 FTEs spend 80% of time on manual data entry, causing R$45,000+ in quarterly reconciliation errors
- **Solution:** Automated extraction pipeline achieving 90%+ accuracy with autonomous monitoring
- **Timeline:** Production launch April 1, 2026

## Features

- **AI-Powered Extraction** - Gemini 2.0 Flash multimodal LLM for document understanding
- **Event-Driven Pipeline** - Cloud Run functions orchestrated via Pub/Sub
- **Autonomous Monitoring** - CrewAI agents for self-healing operations
- **40+ Specialized Agents** - Code review, testing, Spark, Lakeflow, LLM prompts, and more
- **8 Knowledge Domains** - Pydantic, GCP, Gemini, LangFuse, Terraform, Terragrunt, CrewAI, OpenRouter
- **Structured Development** - AgentSpec 4.1 (SDD) and Dev Loop workflows

---

## Quick Start

### Prerequisites

- Python 3.11+
- [Claude Code CLI](https://claude.ai/claude-code) installed
- GCP account (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/owshq-academy/btc-zero-prd-claude-code.git
cd btc-zero-prd-claude-code

# Launch Claude Code
claude

# Explore the codebase
/readme-maker    # Generate documentation
/sync-context    # Update project context
```

### Using the Invoice Generator

```bash
cd gen/synthetic-invoice-gen

# Install dependencies
pip install -e .

# Generate test invoices
invoice-gen generate --count 10 --output invoices/
```

---

## Architecture

```text
INGESTION          PROCESSING                              STORAGE
---------          ----------                              -------

+-------+   +----------+   +----------+   +----------+   +----------+
| TIFF  |-->| TIFF->PNG|-->| CLASSIFY |-->| EXTRACT  |-->|  WRITE   |--> BigQuery
| (GCS) |   |          |   |          |   | (Gemini) |   |          |
+-------+   +----------+   +----------+   +----------+   +----------+
    |           |              |              |              |
    +-----------+--------------+--------------+--------------+
                          Pub/Sub (events)

OBSERVABILITY                              AUTONOMOUS OPS
-------------                              --------------

+-----------+  +-----------+  +-----------+    +---------+  +-----------+  +----------+
| LangFuse  |  |Cloud Logs |  | Metrics   |    | TRIAGE  |->|ROOT CAUSE |->| REPORTER |--> Slack
+-----------+  +-----------+  +-----------+    +---------+  +-----------+  +----------+
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Cloud | GCP | Primary infrastructure |
| Compute | Cloud Run | Serverless functions |
| Messaging | Pub/Sub | Event-driven pipeline |
| Storage | GCS + BigQuery | Files and data warehouse |
| LLM | Gemini 2.0 Flash | Document extraction |
| Fallback | OpenRouter | LLM redundancy |
| Observability | LangFuse | LLMOps monitoring |
| Validation | Pydantic | Structured output |
| IaC | Terraform + Terragrunt | Infrastructure |
| Autonomous Ops | CrewAI | AI monitoring agents |

---

## Project Structure

```text
btc-zero-prd-claude-code/
|-- src/                           # Main source code (Python)
|-- gen/                           # Code generation tools
|   +-- synthetic-invoice-gen/     # Test data generator
|-- notes/                         # Meeting notes (6 sessions)
|-- design/                        # Architecture documents
|-- examples/                      # Sample invoices
|-- .claude/                       # Claude Code ecosystem
    |-- agents/                    # 40 specialized agents
    |   |-- ai-ml/                 # LLM, GenAI specialists (4)
    |   |-- aws/                   # Lambda, CI/CD (4)
    |   |-- code-quality/          # Review, test, clean (6)
    |   |-- communication/         # Docs, planning (3)
    |   |-- data-engineering/      # Spark, Lakeflow (8)
    |   |-- dev/                   # Dev Loop (2)
    |   |-- domain/                # Pipeline-specific (5)
    |   |-- exploration/           # Codebase analysis (2)
    |   +-- workflow/              # SDD pipeline (6)
    |-- commands/                  # 13 slash commands
    |-- kb/                        # 8 knowledge domains
    +-- sdd/                       # Spec-Driven Development
```

---

## Claude Code Agents

### Agent Categories

| Category | Count | Key Agents |
|----------|-------|------------|
| **Workflow** | 6 | `brainstorm-agent`, `define-agent`, `design-agent`, `build-agent`, `ship-agent` |
| **Code Quality** | 6 | `code-reviewer`, `test-generator`, `code-documenter`, `python-developer` |
| **Data Engineering** | 8 | `spark-specialist`, `lakeflow-architect`, `medallion-architect` |
| **AI/ML** | 4 | `llm-specialist`, `genai-architect`, `ai-prompt-specialist` |
| **Domain** | 5 | `extraction-specialist`, `pipeline-architect`, `function-developer` |
| **Exploration** | 2 | `codebase-explorer`, `kb-architect` |

### Available Commands

| Command | Purpose |
|---------|---------|
| `/brainstorm` | Explore ideas through dialogue |
| `/define` | Capture requirements |
| `/design` | Create architecture |
| `/build` | Execute implementation |
| `/ship` | Archive completed features |
| `/dev` | Dev Loop for structured iteration |
| `/review` | Code review workflow |
| `/readme-maker` | Generate comprehensive README |
| `/sync-context` | Update CLAUDE.md |
| `/memory` | Save session insights |

---

## Knowledge Base

8 MCP-validated domains with patterns, concepts, and quick references:

| Domain | Purpose |
|--------|---------|
| **pydantic** | Data validation for LLM output parsing |
| **gcp** | GCP serverless data engineering |
| **gemini** | Multimodal LLM for document extraction |
| **langfuse** | LLMOps observability platform |
| **terraform** | Infrastructure as Code |
| **terragrunt** | Multi-environment orchestration |
| **crewai** | Multi-agent AI orchestration |
| **openrouter** | Unified LLM API gateway |

---

## Development Workflows

### AgentSpec 4.1 (Spec-Driven Development)

For features requiring traceability:

```text
/brainstorm --> /define --> /design --> /build --> /ship
   (Opus)       (Opus)      (Opus)    (Sonnet)   (Haiku)
```

### Dev Loop (Level 2)

For utilities, prototypes, and KB building:

```bash
/dev "I want to build a date parser"    # Guided creation
/dev tasks/PROMPT_PARSER.md             # Execute PROMPT
/dev tasks/PROMPT_PARSER.md --resume    # Resume session
```

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_CLOUD_PROJECT` | GCP project ID |
| `GCP_REGION` | GCP region (us-central1) |
| `LANGFUSE_PUBLIC_KEY` | LangFuse observability |
| `LANGFUSE_SECRET_KEY` | LangFuse secret |
| `OPENROUTER_API_KEY` | Fallback LLM provider |

### GCP Projects

| Environment | Project |
|-------------|---------|
| Development | `invoice-pipeline-dev` |
| Production | `invoice-pipeline-prod` |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Extraction accuracy | >= 90% |
| Processing latency P95 | < 30 seconds |
| Pipeline availability | > 99% |
| Cost per invoice | < $0.01 |
| Manual processing reduction | > 80% |

---

## Timeline

| Date | Milestone |
|------|-----------|
| Jan 15, 2026 | Project kickoff |
| Feb 7, 2026 | All 4 functions implemented |
| Feb 28, 2026 | MVP demo to stakeholders |
| Mar 15, 2026 | Accuracy validation complete |
| **Apr 1, 2026** | **Production launch** |
| Apr 30, 2026 | CrewAI pilot complete |

---

## Documentation

| Resource | Description |
|----------|-------------|
| [Summary Requirements](notes/summary-requirements.md) | Consolidated project specs |
| [Architecture](design/gcp-cloud-run-fncs.md) | Cloud Run functions design |
| [CLAUDE.md](.claude/CLAUDE.md) | AI assistant context |
| [KB Index](.claude/kb/_index.yaml) | Knowledge base registry |
| [Agent Template](.claude/agents/_template.md.example) | Create new agents |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Use `/define` and `/design` for significant features
4. Run `/review` before submitting
5. Create a Pull Request with `/create-pr`

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*Generated with `/readme-maker` - Claude Code Agent Ecosystem*
