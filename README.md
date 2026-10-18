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

## 🌟 Executive Summary & Core Innovation

Enterprises lose over **$100 Billion annually** to data downtime and broken ETL/ELT pipelines. When upstream payment gateways, CRM systems, or microservices arbitrarily mutate their JSON payloads (e.g. renaming fields, nesting billing dictionaries, changing date formats), standard pipelines (Airflow, dbt, Spark) crash or corrupt downstream data warehouses.

### 🧠 The Core Breakthrough: The ARC-AGI Autonomous File Ingestion Agent
Instead of relying on brittle manual regex or unverified LLM prompts, SchemaForge adapts the **Abstraction and Reasoning Corpus (ARC-AGI)** paradigm to autonomous data engineering:
- **Ingests Dirty, Polymorphic Files:** Ingests raw, unstructured enterprise files (e.g., [`sample_data/messy_sap_orders.json`](sample_data/messy_sap_orders.json)) containing mixed dictionaries, epoch integers, European slash dates, and stringified line items.
- **Autonomous Structural Profiling:** Extracts spatial JSONPaths, infers polymorphic type distributions, and redacts PII without human intervention.
- **Neuro-Symbolic Program Synthesis (Gemini 1.5 Pro):** Synthesizes candidate Python AST transformation programs alongside formal **Pandera Schema Contracts**.
- **Formal Invariant Verification in gVisor Sandbox:** Proves 100% mathematical correctness (Type Preservation, Non-Null Guarantees, Financial Sum Conservation $\sum \text{Gross} == \sum \text{Billed}$).
- **Instant BigQuery Streaming:** Deploys verified transformations in **406.8 milliseconds** with zero downtime and a **100% Data Quality Score (DQS)**.

👉 **[Read the Complete ARC-AGI File Ingestion Walkthrough](docs/SHOWCASE_WALKTHROUGH.md)**

---

## 🚀 Live Working Solution

- **Live Application URL:** **[https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app)**
- **Liveness Probe:** `https://schemaforge-app-605335322761.us-central1.run.app/health/live` (HTTP 200 `ALIVE`)
- **Readiness Probe:** `https://schemaforge-app-605335322761.us-central1.run.app/health/ready` (HTTP 200 `READY`)
- **Interactive OpenAPI Documentation:** `https://schemaforge-app-605335322761.us-central1.run.app/docs`

---

## 🎬 Comprehensive System Video Pitch & Technical Walkthrough (10:02)

> **Format:** 1080p Full HD (1920x1080) • H.264 / AAC Stereo • Duration: 10:02 (602 Seconds)  
> **Video File:** [`docs/assets/schemaforge_showcase_video.mp4`](docs/assets/schemaforge_showcase_video.mp4) *(also at root: [`schemaforge_showcase_video.mp4`](schemaforge_showcase_video.mp4))*

A broadcast-grade 10-minute technical demonstration and deep architectural walkthrough across 7 structured scenes:
- **Scene 1 (0:00 - 1:25): The $100B Enterprise Data Downtime Crisis:** Breakdown of dirty polymorphic enterprise payloads ([`sample_data/messy_sap_orders.json`](sample_data/messy_sap_orders.json)) and why traditional batch pipelines (Airflow, dbt, Spark) crash.
- **Scene 2 (1:25 - 2:50): Competition Track Justification:** Strategic justification for building an Autonomous Data-OS at the ingestion boundary rather than superficial GenAI chatbots.
- **Scene 3 (2:50 - 4:23): The Novel Approach: ARC-AGI Ingestion Agent:** How SchemaForge adapts François Chollet's Abstraction & Reasoning Corpus (ARC-AGI) to neuro-symbolic program synthesis.
- **Scene 4 (4:23 - 5:50): Deep Google Gemini Utilization:** Dual-model architecture: low-entropy Gemini 1.5 Pro ($T=0.2$) for deterministic Python AST code generation and Gemini 1.5 Flash for conversational analytics.
- **Scene 5 (5:50 - 7:18): Formal Safety Sandbox & Invariants:** gVisor container sandbox security, prohibited AST scanning, Pandera schema contracts, and financial balance conservation ($\sum \text{Gross} \equiv \sum \text{Billed}$).
- **Scene 6 (7:18 - 8:40): Google Cloud Native Architecture:** Stateless Cloud Run compute (80 conns/container), Pub/Sub streaming buffer & Dead-Letter Queue (DLQ), and BigQuery golden analytical lakehouse.
- **Scene 7 (8:40 - 10:02): Live Production Walkthrough & Real Results:** Live demonstration on Google Cloud Run: 406.8ms Mean Time to Self-Heal, DLQ circuit breakers, and Tri-Modal E-Commerce Copilot.

---

## 📚 Competition & System Documentation

| Document | Purpose |
|---|---|
| [**Showcase Video Walkthrough (.mp4)**](docs/assets/schemaforge_showcase_video.mp4) | **1080p Demonstration Video:** 10-minute broadcast presentation covering problem statement, ARC-AGI novelty, track justification, and live solution walkthrough. |
| [**ARC-AGI File Ingestion Walkthrough**](docs/SHOWCASE_WALKTHROUGH.md) | **Core Walkthrough:** Step-by-step evaluation of the ARC-AGI agent ingesting dirty polymorphic files into BigQuery. |
| [**System Architecture & Technical Manual**](docs/ARCHITECTURE_AND_SYSTEM_MANUAL.md) | Comprehensive engineering manual, GCP services matrix, and end-to-end data flow. |
| [**Executive Pitch Deck (.pptx)**](docs/SchemaForge_DataOS_PitchDeck.pptx) | **Complete 10-slide PowerPoint Presentation (.pptx)** with 16:9 dark-mode slides and architecture embeds. |
| [**Video Pitch & Demo Script**](docs/DEMO_VIDEO_SCRIPT.md) | Timecoded video presentation script with exact narration and click paths. |
| [**Public GitHub Setup Guide**](docs/GITHUB_SETUP_GUIDE.md) | Public repository guide with zero-credential verification guarantee. |
| [**Standard Operating Procedures (SOP)**](docs/SOP_OPERATIONAL_RUNBOOK.md) | Operational runbooks for running chaos drills, handling DLQs, and deploying on Cloud Run. |

---

## 🏗️ Google Cloud Native System Architecture

<p align="center">
  <img src="docs/assets/gcp_service_architecture_blueprint.svg" alt="SchemaForge Google Cloud System Architecture Blueprint" width="100%" style="border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,0.6); border: 1px solid #26293b;" />
</p>

*Figure 1: Production Google Cloud Architecture Blueprint featuring official service icons for Cloud Run, BigQuery, Pub/Sub, Gemini 1.5, and Cloud Logging with real-time ingestion and DLQ pathways.*

<p align="center">
  <img src="docs/assets/gcp_system_architecture_diagram.jpg" alt="SchemaForge 3D Isometric Topology" width="100%" style="border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,0.6); border: 1px solid #26293b; margin-top: 15px;" />
</p>

*Figure 2: 3D Isometric Topology rendering of the distributed serverless cloud infrastructure on Google Cloud Platform.*

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
