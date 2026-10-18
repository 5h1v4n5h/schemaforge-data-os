# SchemaForge Data-OS
> **Autonomous Ingestion, Neuro-Symbolic Self-Healing & Observability Platform for Google Cloud**  
> *Google Cloud AI & Innovation Cup 2026*

<p align="center">
  <img src="docs/assets/schemaforge_brand_icon.jpg" alt="SchemaForge Data-OS Logo" width="280" style="border-radius: 16px; box-shadow: 0 8px 30px rgba(59,130,246,0.3);" />
</p>

<p align="center">
  <a href="https://schemaforge-app-605335322761.us-central1.run.app"><img src="https://img.shields.io/badge/Live%20Demo-Google%20Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Live Demo" /></a>
  <a href="https://cloud.google.com/bigquery"><img src="https://img.shields.io/badge/Warehouse-Google%20BigQuery-669DF6?style=for-the-badge&logo=google-cloud&logoColor=white" alt="BigQuery" /></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/AI%20Engine-Gemini%201.5%20Pro-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" /></a>
  <a href="https://cloud.google.com/pubsub"><img src="https://img.shields.io/badge/Streaming-Cloud%20Pub%2FSub-34A853?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Pub/Sub" /></a>
</p>

---

## 🌟 Executive Summary & Problem Space

Enterprises lose over **$100 Billion annually** to data downtime and broken ETL/ELT pipelines. When upstream payment gateways, CRM systems, or microservices arbitrarily mutate their JSON payloads (e.g. renaming fields, nesting billing dictionaries, changing date formats), standard pipelines (Airflow, dbt, Spark) crash or corrupt downstream data warehouses.

**SchemaForge Data-OS** eliminates manual triage with **Autonomous Neuro-Symbolic Program Synthesis**:
1. **Sub-Second Auto-Drift Healing:** Detects breaking schema mutations, invokes **Google Gemini 1.5** to synthesize pure Python AST transformation code, validates formal invariants inside a sandbox, and deploys the repair in under **406 ms** with zero human intervention.
2. **Multi-Source Golden Mastering:** Reconciles dirty e-commerce orders, Stripe charges, and CRM tickets into unified golden analytics entities in **Google Cloud BigQuery** (`gold_analytics`).
3. **Tri-Modal Conversational Copilot:** Empowered by Gemini 1.5, business and data leaders converse with live warehouse metrics, receiving structured executive summaries, interactive **Vega-Lite** visual charts, and verified BigQuery SQL queries.

---

## 🚀 Live Working Solution

- **Live Application URL:** **[https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app)**
- **Liveness Probe:** `https://schemaforge-app-605335322761.us-central1.run.app/health/live` (HTTP 200 `ALIVE`)
- **Readiness Probe:** `https://schemaforge-app-605335322761.us-central1.run.app/health/ready` (HTTP 200 `READY`)
- **Interactive OpenAPI Documentation:** `https://schemaforge-app-605335322761.us-central1.run.app/docs`

---

## 📚 Competition & System Documentation

| Document | Purpose |
|---|---|
| [**System Architecture & Technical Manual**](docs/ARCHITECTURE_AND_SYSTEM_MANUAL.md) | Comprehensive engineering manual, GCP services matrix, and end-to-end data flow. |
| [**Executive Pitch Deck**](docs/PITCH_DECK.md) | 10-slide enterprise presentation deck with problem-solution narrative and ROI metrics. |
| [**Video Pitch & Demo Script**](docs/DEMO_VIDEO_SCRIPT.md) | Timecoded 5-minute video presentation script with exact narration and click paths. |
| [**Executive Pitch Deck (.pptx)**](docs/SchemaForge_DataOS_PitchDeck.pptx) | **Complete 10-slide PowerPoint Presentation (.pptx)** with 16:9 dark-mode slides and architecture embeds. |
| [**Pitch Deck Transcript (Markdown)**](docs/PITCH_DECK.md) | Markdown transcript of the 10-slide enterprise presentation deck. |
| [**Evaluator Showcase Walkthrough**](docs/SHOWCASE_WALKTHROUGH.md) | Step-by-step evaluator testing paths for live chaos drills, DLQ inspection, and Copilot queries. |
| [**Public GitHub Setup Guide**](docs/GITHUB_SETUP_GUIDE.md) | Step-by-step instructions for publishing this clean, credential-free repository to GitHub. |
| [**Standard Operating Procedures (SOP)**](docs/SOP_OPERATIONAL_RUNBOOK.md) | Operational runbooks for running chaos drills, handling DLQs, and deploying on Cloud Run. |

---

## 🏗️ Google Cloud Native System Architecture

<p align="center">
  <img src="docs/assets/gcp_system_architecture_diagram.jpg" alt="SchemaForge Google Cloud System Architecture Diagram" width="100%" style="border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,0.6); border: 1px solid #26293b;" />
</p>

<p align="center">
  <a href="docs/assets/gcp_service_architecture_blueprint.svg">👉 <strong>Open High-Resolution Vector Blueprint (SVG with Official Google Cloud Logos)</strong></a>
</p>

```
+---------------------------------------------------------------------------------------------+
|                                    CLIENT BROWSER / SPA                                     |
|     - Dark Mode Executive Dashboard (Linear/Vercel/Datadog Aesthetic)                       |
|     - Real-Time DQS Scorecards & Circuit Breakers                                           |
|     - Vega-Lite Declarative Interactive Visualizations                                      |
|     - Tri-Modal E-Commerce Copilot Conversational Drawer                                    |
+---------------------------------------------------------------------------------------------+
                                              |
                                              | HTTPS / WebSockets / SSE
                                              v
+---------------------------------------------------------------------------------------------+
|                            GOOGLE CLOUD RUN (COMPUTE & API TIER)                            |
|  - Stateless Containerized FastAPI Engine (Python 3.11)                                     |
|  - Concurrency: 80 requests/container, Horizontal Autoscaling (0 to 10+ instances)          |
|  - gVisor Container Security Sandbox for Dynamic AST Execution                             |
|  - Clean Modular Layers: /domain, /application, /infrastructure, /api                      |
+---------------------------------------------------------------------------------------------+
           |                                   |                                   |
           v                                   v                                   v
+------------------------+      +-------------------------------+      +----------------------+
|  GOOGLE CLOUD PUB/SUB  |      |   GOOGLE GEMINI 1.5 PRO/FLASH |      | GOOGLE CLOUD LOGGING |
| (STREAMING BUFFER TIER)|      |     (NEURO-SYMBOLIC AI TIER)  |      | (OBSERVABILITY TIER) |
| - Raw Ingestion Topics |      | - Zero-Shot AST Code Gen      |      | - Structured JSON    |
| - Dead-Letter Queues   |      | - Domain Semantics Grounding  |      | - Latency Profiling  |
| - Poison-Pill Shield   |      | - Invariant Verification Loop |      | - Cloud Trace / APM  |
+------------------------+      +-------------------------------+      +----------------------+
           |                                   |
           +-----------------+   +-------------+
                             |   |
                             v   v
+---------------------------------------------------------------------------------------------+
|                             GOOGLE CLOUD BIGQUERY (WAREHOUSE TIER)                          |
|  - Dataset: `gold_analytics`                                                                |
|  - Tables: `fact_reconciled_orders`, `dim_customers_master`, `fact_orders`                  |
|  - Partitioned & Clustered by `tenant_id` and `timestamp`                                   |
|  - High-Throughput Streaming Buffer with Atomic Deduplication                               |
+---------------------------------------------------------------------------------------------+
```

---

## ⚡ Quickstart & Local Development

### 1. Run Server Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/schemaforge-data-os.git
cd schemaforge-data-os

# Configure environment template
cp .env.example .env

# Install dependencies in virtualenv
python -m venv .venv
source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start the FastAPI engine
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```
Open **[http://localhost:8080](http://localhost:8080)** to access the local instance.

### 2. Run Test Suite
```bash
# Run unit and clean architecture tests
pytest tests/test_clean_architecture.py -v
```

### 3. Deploy to Google Cloud Run
```bash
gcloud run deploy schemaforge-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --concurrency 80
```

---

## 🔒 Security & Zero Credential Policy
- **Application Default Credentials (ADC):** Connects to Google Cloud services via IAM roles without embedded keys.
- **Zero Hardcoded Secrets:** Strict `.gitignore` protecting `.env`, certificates, and private tokens.
- **Sandboxed Execution:** Synthesized transformation code is executed inside secure sandboxed environments with strict timeouts and memory boundaries.
