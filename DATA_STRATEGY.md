# SchemaForge (NeuroETL) — Enterprise Data Availability Strategy
## Sourcing, Staging, Multi-Layer Storage & Google Cloud Migration Blueprint

---

## 1. Executive Summary & Strategy Objectives

This document establishes the official **Data Strategy** for SchemaForge. It defines how data from three disparate enterprise sources—**theLook eCommerce (Storefront/ERP)**, **Stripe (Financial Gateway)**, and **CRM/Zendesk (Customer Support)**—is sourced, staged locally for zero-cost development, and migrated to **Google Cloud Platform (GCP)** for production execution.

### Core Objectives:
1. **Dual-Environment Portability:** Enable instant local execution (via DuckDB / Parquet fixtures) and seamless 1-command migration to Google Cloud (BigQuery, GCS, Cloud Pub/Sub).
2. **Realistic Multi-Source Heterogeneity:** Demonstrate genuine cross-system schema drift, entity mastering, semantic alignment, and financial reconciliation.
3. **Enterprise Compliance by Design:** Ensure automated PII masking (Cloud DLP), immutable raw archiving, and OpenLineage cataloging across all tiers.

---

## 2. The 3-Source Enterprise Dataset Ecosystem

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               3 HETEROGENEOUS ENTERPRISE SOURCES                                 │
├──────────────────────────────┬──────────────────────────────────┬────────────────────────────────┤
│ SOURCE 1: Web Storefront     │ SOURCE 2: Payment Gateway        │ SOURCE 3: Customer Helpdesk    │
│ theLook eCommerce (Google)   │ Stripe API Webhooks              │ Zendesk / Salesforce CRM       │
├──────────────────────────────┼──────────────────────────────────┼────────────────────────────────┤
│ • users, orders, order_items │ • charges, refunds, fees         │ • tickets, users, sentiment    │
│ • Key: `user_id`, `order_id` │ • Key: `cus_id`, `charge_id`     │ • Key: `requester_email`, `id` │
│ • Currency: USD (float)      │ • Currency: USD cents (int)      │ • Channel: Web, Mobile, Email  │
│ • Format: Nested JSON & SQL  │ • Format: Polymorphic Webhook    │ • Format: REST API JSON Dumps  │
└──────────────────────────────┴──────────────────────────────────┴────────────────────────────────┘
```

### Source Specifications:
1. **Source 1: theLook eCommerce (Storefront / Orders ERP)**
   * **Origin:** Google Cloud Public Datasets (`bigquery-public-data.thelook_ecommerce`).
   * **Slices Used:** `orders`, `order_items`, `users`, and `events` (clickstream webhooks).
   * **Role:** Provides baseline customer profiles, items purchased, and promised delivery dates.
2. **Source 2: Stripe Billing & Payment Gateway**
   * **Origin:** Open-source synthetic Stripe API event fixtures.
   * **Slices Used:** `charge.succeeded`, `charge.refunded`, `payment_intent.created`.
   * **Role:** Acts as the external financial ledger. Provides actual payments, card brands, payment method types (credit card, Apple Pay, voucher), and fee breakdowns.
3. **Source 3: Enterprise Customer Support (Zendesk / Salesforce)**
   * **Origin:** Open-source customer service ticket dumps.
   * **Slices Used:** Support tickets, requester contact details, satisfaction ratings (CSAT), and escalation flags.
   * **Role:** Enables **Master Data Management (Entity Mastering)** by introducing customer identity overlap, name variations, corporate domains, and customer support cost metrics.

---

## 3. Two-Stage Data Availability Workflow

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE A: LOCAL STAGING & DEVELOPMENT (Zero Cloud Cost)                                           │
│ Local JSONL / Parquet fixtures in `sample_data/` ──► Ingested via local DuckDB / Polars           │
└───────────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                                │
                                                ▼  GCP Migration Pipeline
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE B: GOOGLE CLOUD PRODUCTION LAKEHOUSE                                                       │
│                                                                                                  │
│ [GCS Raw Landing Buckets]  ◄── Ingestion (Batch Uploads & Datastream CDC)                        │
│           │                                                                                      │
│           ▼                                                                                      │
│ [Cloud Run / Cloud DLP]    ──► PII Redaction & Conformance                                       │
│           │                                                                                      │
│           ▼                                                                                      │
│ [BigQuery Lakehouse]       ──► Bronze (Raw) ──► Silver (Cleaned) ──► Gold (Mastered & Reconciled)│
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Stage A: Local Development Staging (Current Environment)
To build and validate the agent locally without incurring cloud egress or compute charges:
* High-fidelity, representative sample slices (1,000–5,000 records per source) are committed to `sample_data/`:
  * `sample_data/source1_thelook_orders.jsonl`
  * `sample_data/source1_thelook_users.jsonl`
  * `sample_data/source2_stripe_charges.jsonl`
  * `sample_data/source3_crm_tickets.jsonl`
* Local execution uses **DuckDB & Polars**, providing BigQuery-identical SQL semantics directly in Python.

### Stage B: Google Cloud Production Staging (Target Environment)
When deploying to GCP, data availability is orchestrated via native Google Cloud services:

1. **Bronze Landing Lake (Google Cloud Storage):**
   * Raw payloads are written directly to Cloud Storage buckets with customer-managed encryption (CMEK):
     * `gs://schemaforge-{project_id}-bronze/thelook/YYYY/MM/DD/*.json.gz`
     * `gs://schemaforge-{project_id}-bronze/stripe/YYYY/MM/DD/*.json.gz`
     * `gs://schemaforge-{project_id}-bronze/crm/YYYY/MM/DD/*.json.gz`
   * Lifecycle rule: Move to Coldline after 90 days; retain raw immutable audit log for 7 years.

2. **Real-Time Streaming Replay (Cloud Pub/Sub):**
   * Three Pub/Sub topics simulate live webhook arrival:
     * `projects/{project_id}/topics/thelook-orders`
     * `projects/{project_id}/topics/stripe-charges`
     * `projects/{project_id}/topics/crm-tickets`
   * Cloud Run microservices consume messages and trigger SchemaForge profiling and drift analysis.

3. **In-Warehouse Analytical Fabric (BigQuery):**
   * Dataset `schemaforge_bronze`: External tables mapped over GCS files.
   * Dataset `schemaforge_silver`: Conformed, strongly-typed partitioned tables.
   * Dataset `schemaforge_gold`: Mastered Star Schemas and Reconciled Fact tables.

---

## 4. Multi-Layer Storage, Partitioning & Table Layout

| Layer | BigQuery Dataset / Table | Partitioning & Clustering | Retention | Schema Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Bronze** | `schemaforge_bronze.raw_thelook_orders`<br>`schemaforge_bronze.raw_stripe_charges`<br>`schemaforge_bronze.raw_crm_tickets` | Partition by `_ingested_at: DAY`<br>Cluster by `_source_system` | 90 Days active | Schema-on-read; payload stored as native BigQuery `JSON` data type with metadata envelope. |
| **Silver** | `schemaforge_silver.orders`<br>`schemaforge_silver.payments`<br>`schemaforge_silver.support_tickets` | Partition by `event_timestamp: DAY`<br>Cluster by `customer_id` | Permanent | Strong typing; normalized UTC dates; currency converted to base USD; PII masked by Cloud DLP. |
| **Gold** | `schemaforge_gold.dim_master_customer`<br>`schemaforge_gold.fact_reconciled_orders` | Partition by `order_date: MONTH`<br>Cluster by `master_customer_id` | Permanent | **Mastered Golden Records** (via Splink/MinHash linkage); cross-system financial reconciliation ledger. |
| **Metrics** | `schemaforge_metrics.executive_kpis` | Materialized Views with BigQuery BI Engine | In-Memory | Looker Modeler / BI Engine semantic views for sub-second dashboard rendering. |

---

## 5. Google Cloud Migration Runbook (Step-by-Step)

When ready to migrate SchemaForge from the local environment to Google Cloud, execute the following automated steps:

### Step 1: GCP Infrastructure Provisioning
```bash
# Set environment variables
export PROJECT_ID="schemaforge-ai-2026"
export REGION="us-central1"
gcloud config set project $PROJECT_ID

# 1. Enable Required GCP APIs
gcloud services enable \
  bigquery.googleapis.com \
  storage.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  dlp.googleapis.com \
  pubsub.googleapis.com \
  dataplex.googleapis.com

# 2. Create Storage Buckets
gcloud storage buckets create gs://schemaforge-${PROJECT_ID}-bronze \
  --location=$REGION \
  --uniform-bucket-level-access

# 3. Create BigQuery Datasets
bq --location=$REGION mk -d ${PROJECT_ID}:schemaforge_bronze
bq --location=$REGION mk -d ${PROJECT_ID}:schemaforge_silver
bq --location=$REGION mk -d ${PROJECT_ID}:schemaforge_gold
bq --location=$REGION mk -d ${PROJECT_ID}:schemaforge_metrics
```

### Step 2: Seed theLook Data Directly inside BigQuery
Rather than downloading gigabytes locally and re-uploading, execute a zero-copy direct BigQuery ingestion:
```sql
-- Seed Bronze Orders from BigQuery Public Dataset into our Bronze layer
CREATE OR REPLACE TABLE `schemaforge_bronze.raw_thelook_orders`
PARTITION BY DATE(_ingested_at)
AS
SELECT 
  GENERATE_UUID() AS _record_id,
  'thelook_ecommerce' AS _source_system,
  CURRENT_TIMESTAMP() AS _ingested_at,
  TO_JSON_STRING(t) AS _raw_payload
FROM `bigquery-public-data.thelook_ecommerce.orders` t
LIMIT 10000;
```

### Step 3: Deploy SchemaForge Control Plane to Cloud Run
```bash
# Build and deploy the SchemaForge container
gcloud run deploy schemaforge-engine \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION
```

---

## 6. Governance, Security & Lineage

1. **Automated PII Isolation (Cloud DLP):**
   * Before raw customer records transition from Bronze to Silver, **Cloud DLP (Sensitive Data Protection)** inspects payloads for emails, credit cards, and addresses, replacing them with salted cryptographic tokens or masked strings (`j***@acme.com`).
2. **Dataplex Catalog & OpenLineage:**
   * Every dataset registers under a Dataplex Lake (`lakehouse-retail`).
   * Column-level lineage graphs are emitted automatically whenever the Canonical Compiler promotes a Dataform model from Silver to Gold.
3. **Audit Provenance Ledger:**
   * Every field in `schemaforge_gold.dim_master_customer` records:
     * `_winning_source_system` (e.g. `sap_s4hana` vs `stripe`)
     * `_confidence_score` (e.g. `0.98`)
     * `_survivorship_rule_applied` (e.g. `MOST_RECENT_VERIFIED`)
