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

## 🏗️ Architecture

```
┌──────────────┐   ┌──────────────┐   ┌────────────┐
│ Ingestion    │   │ Processing   │   │   API      │  
│ Workers      │──▶│ Pipeline     │──▶│ + Query    │
│              │   │ (LLM/RAG)    │   │   Engine   │
└──────┬───────┘   └──────┬───────┘   └──────┬─────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌───────────────────────────────────────────────────────┐
│               PostgreSQL + pgvector                   │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │Raw Facts│ │Sentiments│ │Summaries │ │ Embeddings │ │
│  │(immut.) │ │+ Narratv.│ │+ Context │ │ (HNSW idx) │ │
│  └─────────┘ └──────────┘ └──────────┘ └────────────┘ │
└───────────────────────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │    Redis    │
                    │  (queues +  │
                    │  caching)   │
                    └─────────────┘
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

|  Layer              | Technology                         |
|---------------------|------------------------------------|
| **Language**        | Python 3.11+                       |
| **Database**        | PostgreSQL 16 + pgvector           |
| **Cache / Queue**   | Redis 7                            |
| **ORM**             | SQLAlchemy 2.0 (async)             |
| **Migrations**      | Alembic                            |
| **LLM**             | Ollama (local)                     |
| **Embeddings**      | all-MiniLM-L6-v2 (384-dim)         |
| **API**             | FastAPI                            |
| **Validation**      | Pydantic v2                        |
| **Infrastructure**  | Docker Compose, Terraform, Ansible |
| **CI/CD**           | GitHub Actions                     |
| **Package Manager** | uv                                 |
```


## 📁 Project Structure

```
daily_report/
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
├── infrastructure/
│   └── docker/
│       └── postgres/           # Custom PG image with pgvector
├── scripts/
│   ├── seed.py                 # Initial data seeding
│   ├── healthcheck.py          # DB verification
│   └── test_db.py
├── src/
│   └── dailyreport/
│       └── core/
│           ├── config.py       # Pydantic settings
│           └── db/
│               ├── base.py     # SQLAlchemy Base
│               ├── session.py  # Engine & session factory
│               └── models/
│                   ├── company.py      # Sector, Company, Relationships
│                   ├── document.py     # Document, DocumentSection
│                   ├── knowledge.py    # RawFact, DerivedMetric, Summary,
│                   │                   # Sentiment, RiskFactor, Mention
│                   ├── thesis.py       # Investment theses
│                   ├── meta.py         # ProcessingLog (observability)
│                   └── enums.py        # Python-side validation enums
├── tests/
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```



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
