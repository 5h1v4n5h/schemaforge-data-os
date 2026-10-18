# SchemaForge Data-OS: Standard Operating Procedures (SOP) & Runbook

> **Target Audience:** On-call Data Engineers, Reliability Architects, Evaluation Judges  
> **Classification:** Production Runbook  
> **Live Instance:** `https://schemaforge-app-605335322761.us-central1.run.app`  

---

## SOP-01: Executing Multi-Tenant Chaos & Drift Drills

### Purpose
To validate autonomous neuro-symbolic self-healing capabilities when upstream ingestion payloads mutate unexpectedly without advance warning.

### Step-by-Step Procedure
1. Navigate to the live web interface: [`https://schemaforge-app-605335322761.us-central1.run.app`](https://schemaforge-app-605335322761.us-central1.run.app).
2. Select an enterprise workspace from the top-left tenant dropdown (e.g., `Nexus-FinTech-Core (FinTech)`).
3. Ensure the active view is set to **⚡ Synthesis & Chaos**.
4. In the **Live Pipeline & Drift Chaos Sandbox** pane, click on one of the pre-configured chaos drill scenarios:
   - **Scenario A: Breaking Schema Mutation** (Simulates upstream renaming of `customer_id` $\to$ `client_uuid` and nesting `billing.amount_cents`).
   - **Scenario B: Dirty Unstructured Input** (Simulates messy cargo text, imperial-to-metric conversions, and date format variance).
   - **Scenario C: High-Volume Burst & Poison Pill** (Simulates 10,000 events/min with malicious malformed JSON).
   - **Scenario D: Multi-Tenant Data Isolation** (Simulates cross-tenant query attempts).
5. Click **⚡ FIRE REAL CHAOS PAYLOAD INTO PUB/SUB**.
6. **Expected Outcome**:
   - The UI displays the live payload mutation.
   - The **Mean Time to Self-Heal (MTTR)** card updates (typically $350\text{ ms} - 450\text{ ms}$).
   - The **Synthesized Python AST Rule** is displayed side-by-side with verified green syntax highlighting.
   - The **BigQuery Ingestion Status** shows `PASSED_100_PERCENT` with the corresponding BigQuery Job ID.

---

## SOP-02: Inspecting and Reprocessing Dead-Letter Queue (DLQ) Records

### Purpose
To inspect, quarantine, and remediate unparseable or malicious poison-pill records that fail formal invariant verification.

### Step-by-Step Procedure
1. On the top navigation bar, click **🛡️ Observability & DAG**.
2. Locate the **Active Dead-Letter Queue (DLQ) & Quarantine Inspector** panel.
3. Review the current quarantined records:
   - Observe the `quarantine_id`, `source_system`, `mutation_type`, and `dqs_penalty`.
4. Click on any quarantined record row to expand the raw payload diff and invariant failure explanation.
5. To execute automated remediation:
   - Click **⚡ Synthesize Repair & Re-Inject to Pub/Sub**.
   - The system triggers Gemini 1.5 to generate an invariant-satisfying transformation AST, verifies it, re-publishes the healed record to the main ingestion stream, and removes it from the DLQ.

---

## SOP-03: Tri-Modal Conversational Inquiries with E-Commerce Copilot

### Purpose
To extract executive business intelligence, financial reconciliation insights, and data lineage directly from live BigQuery tables using natural language.

### Step-by-Step Procedure
1. Click on **🤖 E-Commerce Copilot** in the top navigation switcher.
2. In the copilot interface, click on one of the domain-grounded insight quick-prompts or type a custom question:
   - *"Which payment gateways have the highest processing fees and take-rates this week?"*
   - *"Reconcile cross-border shipping delays with customer support ticket volume."*
   - *"Show me data lineage breadcrumbs for fact_reconciled_orders."*
3. Click **Send** or press `Enter`.
4. **Expected Outcome**:
   - **Executive Conversational Summary**: Crisp analytical assessment.
   - **Interactive Vega-Lite Visualizer**: Dynamic bar/line/scatter chart rendered directly in the chat stream.
   - **Verified BigQuery SQL Box**: Exact SQL executed against `gold_analytics` with execution duration in milliseconds.
   - **Lineage Breadcrumbs**: Source system $\to$ Transformation AST $\to$ BigQuery Table.

---

## SOP-04: Google Cloud Run Deployment & Scaling Operations

### Purpose
To deploy updates to Google Cloud Run, verify probe health, and inspect Cloud Logging telemetry.

### Prerequisites
- Google Cloud SDK (`gcloud`) authenticated with project `project-29e65474-32d7-45e0-803`.

### Commands
```bash
# 1. Build and deploy container directly to Cloud Run
gcloud run deploy schemaforge-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --concurrency 80 \
  --min-instances 1 \
  --max-instances 10

# 2. Verify Liveness and Readiness Probes
curl -s https://schemaforge-app-605335322761.us-central1.run.app/health/live
curl -s https://schemaforge-app-605335322761.us-central1.run.app/health/ready

# 3. Stream real-time structured logs from Cloud Run
gcloud beta run services logs tail schemaforge-app --region us-central1
```
