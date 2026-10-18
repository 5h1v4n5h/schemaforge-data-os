# SchemaForge Data-OS: Interactive Evaluator Showcase Walkthrough

> **Live Working Solution:** [https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app)  
> **Platform Version:** Production v2.0 (Google Cloud Run rev-00012)  
> **Region:** `us-central1`  
> **Backend Stack:** FastAPI, Google Cloud Run, Google Cloud BigQuery, Google Cloud Pub/Sub, Google Gemini 1.5  

---

## 🚀 Live Working Solution Links

| Service | Live Public URL | Status |
|---|---|---|
| **Primary Web Application** | [https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app) | 🟢 Live (99.98% Uptime) |
| **Liveness Health Probe** | [https://schemaforge-app-605335322761.us-central1.run.app/health/live](https://schemaforge-app-605335322761.us-central1.run.app/health/live) | 🟢 HTTP 200 `ALIVE` |
| **Readiness Health Probe** | [https://schemaforge-app-605335322761.us-central1.run.app/health/ready](https://schemaforge-app-605335322761.us-central1.run.app/health/ready) | 🟢 HTTP 200 `READY` |
| **Interactive API Documentation** | [https://schemaforge-app-605335322761.us-central1.run.app/docs](https://schemaforge-app-605335322761.us-central1.run.app/docs) | 🟢 OpenAPI / Swagger |

---

## 🧪 Evaluator Showcase Test Paths (4 Scenarios)

### Test Path 1: Autonomous Schema Drift Self-Healing (View 1)
1. Open the [Live Web Application](https://schemaforge-app-605335322761.us-central1.run.app).
2. Select **Scenario A: Breaking Schema Mutation** in the **Live Pipeline & Drift Chaos Sandbox**.
3. Click **⚡ FIRE REAL CHAOS PAYLOAD INTO PUB/SUB**.
4. **Observe:**
   - **MTTR:** Updates in sub-second time ($~406\text{ ms}$).
   - **Synthesized Python Rule:** Code block renders clean AST transformation.
   - **Status:** Displays `100% Passed` with verified BigQuery Job ID.

### Test Path 2: Continuous Ingestion & DQS Scorecards (View 2)
1. Click **🛡️ Observability & DAG** on the top navigation bar.
2. Observe the 4 real-time ingestion swimlanes:
   - **Lane 1:** TheLook E-Commerce (`orders_stream`)
   - **Lane 2:** Stripe Payment Processor (`charges_stream`)
   - **Lane 3:** Zendesk CRM Support (`tickets_stream`)
   - **Lane 4:** Autonomous Multi-Source Mastering Engine
3. Notice the **Data Quality Scorecards (DQS)** calculating real-time composite health ($99.4\%$ A+).

### Test Path 3: Dead-Letter Queue (DLQ) Quarantine Inspector (View 2)
1. On the Observability view, scroll down to the **Active Dead-Letter Queue (DLQ)** table.
2. Click any quarantined record to reveal the raw malformed payload and invariant violation details.
3. Click **⚡ Synthesize Repair & Re-Inject** to demonstrate zero-data-loss automated recovery.

### Test Path 4: E-Commerce Copilot Tri-Modal Inquiries (View 3)
1. Click **🤖 E-Commerce Copilot** in the top navigation switcher.
2. Select the quick prompt:
   > *"Which payment gateways have the highest processing fees and take-rates this week?"*
3. **Observe the Tri-Modal output:**
   - **Summary:** Concise executive financial analysis.
   - **Chart:** Interactive Vega-Lite data visualization.
   - **SQL Box:** Exact BigQuery SQL executed against `gold_analytics` with millisecond duration.
   - **Lineage:** Complete source-to-warehouse lineage trace.

---

## 🛠️ CLI Direct Verification Commands

Evaluators can also query the live Cloud Run backend directly via terminal:

```bash
# 1. Verify Cloud Run Liveness
curl -X GET "https://schemaforge-app-605335322761.us-central1.run.app/health/live"

# 2. Verify Cloud Run Readiness (BigQuery + Pub/Sub connection pooling)
curl -X GET "https://schemaforge-app-605335322761.us-central1.run.app/health/ready"

# 3. Trigger Chaos Scenario A over HTTP API
curl -X POST "https://schemaforge-app-605335322761.us-central1.run.app/api/v1/chaos/run-scenario" \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "SCENARIO_A_SCHEMA_MUTATION", "tenant_id": "t_nexus_fintech"}'

# 4. Query E-Commerce Copilot over HTTP API
curl -X POST "https://schemaforge-app-605335322761.us-central1.run.app/api/copilot/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which payment gateways have the highest processing fees?", "tenant_id": "t_nexus_fintech"}'
```
