# SchemaForge (NeuroETL)
> **Autonomous Neuro-Symbolic Program Synthesis & Data Engineering for Google Cloud**  
> *Google Cloud AI Builder Cup 2026 (JAPAC Hackathon)*

[![Google Cloud Run](https://img.shields.io/badge/Deploy-Google%20Cloud%20Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![Gemini](https://img.shields.io/badge/Models-Gemini%201.5%20Pro%20%26%20Flash-8E75B2?logo=google&logoColor=white)](https://ai.google.dev/)
[![Pandera](https://img.shields.io/badge/Verification-Pandera%20%2B%20Hypothesis-10B981)](https://pandera.readthedocs.io/)

---

## 🌟 Overview

**SchemaForge** shifts enterprise data engineering from brittle, manual scripting to **specification-driven program synthesis**. 

Enterprises lose an average of **$12.9 million annually** to bad data, with data engineers burning **40% of their workweek** fixing broken pipelines and schema drift. Standard ELT tools fail on polymorphic payloads, while zero-shot LLMs hallucinate unverified code that breaks production tables.

Adapting the **Abstraction and Reasoning Corpus (ARC-AGI)** program synthesis breakthrough, SchemaForge uses:
1. **Gemini 1.5 Pro & Flash** to hypothesize transformations.
2. **Deterministic execution sandboxes (Cloud Run / gVisor)** to run code against sample records.
3. **Formal Invariant Verification (Pandera + Metamorphic Hypothesis testing)** to guarantee zero-hallucination transformations.
4. **Canonical Compilation** to deploy immutable, zero-downtime microservices to **Google Cloud Run**.

---

## 🏗️ 6-Stage Neuro-Symbolic Architecture

```
[ Raw Messy Data ] ──► [ 1. Profiler ] ──► [ 2. Hypothesis Gen ] ──► [ 3. gVisor Sandbox ]
                                                                             │
[ BigQuery Gold ]  ◄── [ 6. Cloud Run ] ◄── [ 4. Invariant Gate ] ◄──────────┘
```

1. **Stage 1: Input Profile Analyzer:** Extracts JSON paths, detects polymorphic field types, null ratios, and masks sensitive PII.
2. **Stage 2: Hypothesis Generator:** Formulates distinct structural transformation strategies and co-generates formal Pandera schema contracts.
3. **Stage 3: Sandboxed Execution Engine:** Executes untrusted code inside an isolated environment with strict 5-second timeouts and memory ceilings.
4. **Stage 4: Invariant Checker:** Computes cell-level diffs, executes Pandera statistical contracts, and runs metamorphic property checks (conservation of financial sums).
5. **Stage 5: Reflexion Repair Loop:** Implements rubber-duck explanations and AST structural deduplication (AntiLoopingController) to self-repair failures.
6. **Stage 6: Canonical Compiler:** Wraps verified logic into a FastAPI microservice, generates a Dockerfile, and outputs Google Cloud Run deployment commands.

---

## 🚀 Quickstart & Local Execution

### 1. Run with Python
```bash
# Clone or navigate to the repository
cd "Google AI Cup"

# Start the FastAPI server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to interact with the live SchemaForge dashboard!

### 2. Run Test Suite
```bash
python test_pipeline.py
python test_api.py
```

---

## ☁️ Google Cloud Deployment (Cloud Run)

Deploy the entire platform with one command:
```bash
gcloud run deploy schemaforge-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1
```

---

## 🎥 3-Minute Demo Video Blueprint (Per Official Guidelines)

* **0:00 - 0:30 (Hook):** Demonstrate polymorphic SAP ERP data failing in standard pipelines.
* **0:30 - 1:45 (Architecture):** Walk through the 6-stage state machine on Google Cloud (Cloud Run, Gemini 1.5, Pandera).
* **1:45 - 2:30 (Result):** Trigger SchemaForge synthesis live; showcase verified code and 100% Pandera Data Quality Score.
* **2:30 - 3:00 (Impact):** Highlight $12.9M annual data downtime savings and serverless Cloud Run scaling.
