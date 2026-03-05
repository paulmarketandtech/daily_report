# 📊 Daily Report

**Personal Financial Intelligence Platform** — An end-to-end AI/ML system that transforms SEC filings, earnings calls, and financial news into structured, actionable investment intelligence.

> A working system processing real financial documents through LLM pipelines with full observability, cost tracking, and production-grade infrastructure.

---

## 🎯 What It Does

```
SEC 10-K Filing ──→ Ingestion ──→ LLM Extraction ──→ Structured Facts ──→ Dashboard
Earnings Call ──→ Pipeline ──→ Sentiment Score ──→ Risk Analysis ──→ Alerts
Financial News ──→ Workers ──→ Entity Mapping ──→ Cross-Company ──→ Reports
Intelligence
```

- **Ingests** SEC 10-K filings, earnings call transcripts, and financial news
- **Extracts** structured financial facts (revenue, margins, guidance) using LLM pipelines with confidence scoring
- **Tracks** sentiment shifts across sources — detects narrative changes over time
- **Maps** company relationships — automatically identifies suppliers, competitors, partners from filing text
- **Answers** natural language questions about company fundamentals via RAG-powered semantic search
- **Monitors** everything — token usage, processing latency, error rates, cost per document

---

```
## 🏗️ Architecture
┌──────────────────────────────────────────────────────────┐
│                     PROXMOX HOST                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              DEBIAN VM (GPU Passthrough)           │  │
│  │                                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌────────┐  │  │
│  │  │  Ollama  │ │ Postgres │ │  Redis  │ │Workers │  │  │
│  │  │  (LLM)   │ │+pgvector │ │ (Queue) │ │(Python)│  │  │
│  │  │  ┌────┐  │ │          │ │         │ │        │  │  │
│  │  │  │GPU │  │ │          │ │         │ │        │  │  │
│  │  │  └────┘  │ │          │ │         │ │        │  │  │
│  │  └──────────┘ └──────────┘ └─────────┘ └────────┘  │  │
│  │         Docker Network (internal)                  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

Everything runs in Docker containers on a single VM. The LLM server exposes an internal API. Workers process document queues. PostgreSQL with pgvector handles both structured queries and semantic search. No cloud dependencies.

### Data Pipeline
```
10-Ks (.md) ───┐
Earnings (PDF)─┤──→ Document ──→ Section-Aware ──→ PostgreSQL
News (yfinance)┤    Registry     LLM Processing     ├─ raw_facts
Manual Notes ──┘    & Queue      & Python Math      ├─ derived_metrics
                                                  ├─ summaries+embeddings
                                                    ├─ sentiment
                                                    ├─ risk_factors
                                                  ├─ company_relationships
                                                    └─ processing_logs
                                                          │
                                    ┌─────────────────────┤
                                    ▼                     ▼
                              Morning Paper        Interactive Query
                              (scheduled)          (on-demand briefing)
```



### Core Design Principles 

```
|    Principle                | Implementation                                                                                   |
|-----------------------------|--------------------------------------------------------------------------------------------------|
| **Raw facts are immutable** | LLM-extracted data never changes. Derived metrics can be recomputed.                             |
| **Two-tier processing**     | Watchlist tickers get priority. Background tickers processed in batch. Optimizes GPU limitations |
| **Full observability**      | Every LLM call logged — tokens, latency, model, success/failure.                                 |
| **Semantic + structured**   | Vector search (pgvector HNSW) combined with relational queries for hybrid retrieval.             |
| **Schema-first**            | 12-table relational schema with migrations, constraints, and materialized views.                 |
```



```
## 🛠️ Tech Stack
|------------------------------------------------------------------------------------------------------------------------------|
| Layer          | Technology                            | Why                                                                 |
|------------------------------------------------------------------------------------------------------------------------------|
| Infrastructure | Proxmox → Debian VM → Docker          | Single-machine, full GPU control, container isolation without VM overhead |
| LLM Serving    | Ollama + Qwen2.5 7B (Q4_K_M)          | Fits in 6GB VRAM, strong at structured extraction                   |
| Database       | PostgreSQL 16 + pgvector              | Structured data + vector search in one engine                       |
| Queue          | Redis                                 | Lightweight, reliable task distribution                             |
| Processing     | Python workers                        | Document parsing, LLM orchestration, metric computation             |
| GPU            | NVIDIA RTX 3060 (6GB)                 | Consumer hardware running production workloads                      |
```

### The Constraint-Driven Design
This project runs on a gaming laptop. That constraint shaped every architectural decision:

6GB VRAM → Model must be 7B parameters at 4-bit quantization. Context window limited to ~2-4K tokens. Every document chunk is carefully sized. KV cache management matters.

32GB system RAM → Single VM instead of multiple. Docker containers share the kernel. Every GB is budgeted across services.

Single GPU → Sequential processing, not parallel. Queue-based architecture makes this a feature: perfect resumability, complete processing logs, no race conditions.

No cloud budget → Everything local. The upside: no API costs even when processing millions of pages. The system pays for itself in the first month versus commercial API pricing.

These are engineering constraints that led to a cleaner, more thoughtful design than "just throw it at GPT"


## 📁 Project Structure



## 📊 Database Schema
```
┌──────────┐    ┌───────────┐    ┌──────────────────┐
│ sectors  │◄───│ companies │◄───│   documents      │
└──────────┘    └─────┬─────┘    └────────┬─────────┘
                      │                   │
          ┌───────────┼───────────┐       │
          ▼           ▼           ▼       ▼
    ┌──────────┐ ┌──────────┐ ┌──────────────────┐
    │raw_facts │ │sentiment │ │document_sections │
    └──────────┘ └──────────┘ └──────────────────┘
          │
          ▼
    ┌───────────────┐    ┌──────────┐    ┌──────────┐
    │derived_metrics│    │summaries │    │ theses   │
    └───────────────┘    │(+vector) │    └──────────┘
                         └──────────┘
    ┌──────────┐    ┌──────────────────────┐
    │mentions  │    │ company_relationships│
    └──────────┘    └──────────────────────┘

    ┌─────────────────┐
    │processing_logs  │  ← every LLM call tracked
    └─────────────────┘
```


### Key design decisions:

- raw_facts — immutable. What the LLM extracted stays forever.
- derived_metrics — computed by Python. Can be recomputed from raw facts.
- summaries.embedding — 384-dim vectors with HNSW index for sub-millisecond similarity search.
- processing_logs — full audit trail of every LLM API call (tokens, cost, latency).

## 🗺️ Roadmap
 - [x] Database schema design + migrations
 - [x] PostgreSQL + pgvector + Docker infrastructure
 - [x] Seed data pipeline
 - [x] Ollama local LLM server setup (GPU passthrough)
 - [x] SEC 10-K ingestion pipeline (EDGAR API)
 - [x] LLM extraction pipeline (structured output parsing)
 - [] Earnings call transcript processing
 - [x] Sentiment analysis + narrative classification
 - [x] RAG query engine (vector + structured hybrid search)
 - [x] FastAPI endpoints
 - [] Cross-company relationship mapping
 - [x] GitHub Actions CI/CD pipeline
 - [x] Terraform cloud deployment configs
 - [] Monitoring dashboard (Grafana)
 - [] CLI interface for daily reports

## 📄 License
MIT
