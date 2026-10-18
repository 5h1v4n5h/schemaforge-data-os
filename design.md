# SchemaForge Data-OS: System Architecture & UI/UX Design Specification (`design.md`)

> **Target Audience:** Google Stitch Design Team, UI/UX Engineers, and Solution Architects  
> **Purpose:** Comprehensive functional and visual specification of the implemented SchemaForge Data-OS platform to guide high-fidelity redesign, layout refinement, and interaction polishing in Google Stitch.  
> **Live Deployment:** [Google Cloud Run Live Instance](https://schemaforge-app-605335322761.us-central1.run.app)  
> **GCP Project:** `project-29e65474-32d7-45e0-803` (Region: `us-central1`)  
> **Warehouse:** Google Cloud BigQuery (`gold_analytics`)

---

## 1. Executive Summary & Design Vision

**SchemaForge Data-OS** is an enterprise-grade autonomous data engineering, ingestion observability, and analytical copilot platform. It bridges neuro-symbolic program synthesis (automated transformation code generation under formal invariants) with mission-critical ingestion monitoring and a conversational e-commerce copilot.

### Core Design Philosophy
- **"Bloomberg Terminal Meets Linear":** High data density, crisp dark-mode surfaces, zero fluff, instant responsiveness, and fluid micro-interactions.
- **Anti-Prototype Discipline:** **Zero hardcoded numbers**; every metric, chart, status pill, and log line is grounded in live physical data (Google Cloud BigQuery, Cloud Run, Pub/Sub, SQLite multi-tenant operational records).
- **Progressive Disclosure:** Executive summaries and visual charts at the top; technical artifacts (executed BigQuery SQL, Pandera contracts, AST diffs, JSON envelopes) accessible via collapsible progressive disclosure drawers.
- **Bi-Directional Canvas Coordination:** Actions in the Copilot chat stream dynamically update the Center Canvas visualizations and vice versa.

---

## 2. Information Architecture (IA) & App Shell

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  TOP APPLICATION NAVIGATION BAR                                                                         │
│  [Logo: SchemaForge Data-OS]  [Synthesis Studio]  [Ingestion Observability & DLQ]  [Gemini Copilot]     │
│  [Workspace Tenant Dropdown: 15 Enterprise Tenants]  [Stream Pulse: LIVE]  [BigQuery Live]  [Gemini]   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  GLOBAL LIVE STREAMING TELEMETRY HUD STRIP                                                             │
│  Total Rows: 52,500 | Active Pipelines: 4 | Healed Drifts: 42 | MTTR: 184.2ms | Throughput: ~54.2 eps │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│  VIEW 1: Synthesis Studio           VIEW 2: Ingestion Observability & DLQ   VIEW 3: Gemini Copilot     │
│  • Program Synthesis by Example     • 4-Swimlane Ingestion DAG Topology    • Data Catalog Rail (20%)   │
│  • gVisor Execution Sandbox        • Decoupled DQS Scorecard Breakdown    • Center Canvas (55%)       │
│  • Schema Chaos Drill & Self-Heal   • Tactile DLQ Workbench (Hold Redrive) • Copilot Chat Drawer (25%) │
│  • Pandera Verification Contract    • Verifiable Execution Logs & Hashes   • Draggable Resizer Splitters│
│                                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. View-by-View Detailed Functional Specifications

### 3.1 View 1: Neuro-Symbolic Synthesis Studio (`#viewStudio`)

The synthesis studio allows data engineers to induce robust Python/Pandera transformation pipelines from dirty, malformed multi-source samples without manual scripting.

#### Functional Requirements:
1. **Multi-Source Input Ingestion:**
   - Supports polymorphic enterprise inputs: Shopify JSON, SAP ERP nested orders, Stripe billing settlements, and Zendesk support tickets.
   - Quick-load demo presets: *Polymorphic E-Commerce Orders*, *Financial Stripe Settlement*, *Customer Identity Matching*.
2. **Target Schema & Constraint Configuration:**
   - Allows users to define target column types, nullability rules, and statistical invariant boundaries.
3. **Inductive Synthesis Engine:**
   - Triggers Gemini 1.5 Pro/Flash to formulate transformation hypotheses conditioned on Programming-by-Example (PBE).
   - Executes synthesized code inside an isolated, secure gVisor sandbox container.
   - Generates executable Python code, Pandera schema models, and transformed data preview tables.
4. **Chaos Injection & Self-Healing Drill (`#chaosWorkbench`):**
   - **Drill Scenarios:**
     - `SCENARIO_1`: *Breaking Schema Mutation (Renamed keys + split nested object)*
     - `SCENARIO_2`: *Dirty Unstructured Input (Currency strings with whitespace & symbols)*
     - `SCENARIO_3`: *Multi-Tenant Polymorphic Ingestion (Differing date/currency formats across tenants)*
     - `SCENARIO_4`: *Enterprise Cost Guardrail (Token budget limits with cached inductive rules)*
   - **Self-Healing Execution:** Injects the breaking payload, detects the AST discrepancy, induces a self-healing rule in sub-200ms, verifies the result against Pandera contracts, and commits verified rows directly to BigQuery.

---

### 3.2 View 2: Ingestion Observability & Admin Console (`#viewObservability`)

The operational control plane for monitoring physical ingestion pipelines across bronze, silver, and gold stages.

#### Functional Requirements:
1. **Top HUD Observability Strip:**
   - **Overall DQS Score:** Composite metric (100.0% Grade A+) with incident resilience indicator.
   - **Ingestion Freshness SLA:** Timestamp lag metric (e.g., `14s ago • SLA MET • Threshold < 30min`).
   - **Active Stream Throughput:** Real-time events-per-second (e.g., `61.8 eps across 3 Connectors`).
   - **Dead-Letter Queue (DLQ):** Active quarantined poison-pill counter (`0 Quarantined • ALL CLEAR`).
2. **4-Swimlane Physical DAG Topology Map:**
   - **Swimlane 1 (RAW Ingestion):** Ingestion nodes for Stripe Settlement API, SAP ERP GCS drops, and CRM Zendesk webhooks. Displays buffer lag, circuit breaker status (`CLOSED`), and connector health.
   - **Swimlane 2 (BRONZE Isolation):** Dead-letter routing node with exponential backoff and quarantine custody envelopes.
   - **Swimlane 3 (SILVER Cleansing & Schema Synthesis):** Sandboxed gVisor healing node and Pandera invariant execution node.
   - **Swimlane 4 (GOLD Final Curated Mart):** Physical BigQuery tables (`fact_reconciled_orders`, `dim_customers_master`, `fact_orders`) with row counts and balance status.
3. **Decoupled Data Quality (DQS) Matrix:**
   - Implements the mathematical quality formula:
     $$\text{DQS} = 0.30 \cdot S_{\text{Completeness}} + 0.30 \cdot S_{\text{Validity}} + 0.20 \cdot S_{\text{Uniqueness}} + 0.20 \cdot S_{\text{IncidentResilience}}$$
   - Four progress meters displaying 100% compliance across non-null checks, Pandera range checks, primary key uniqueness, and zero active corruptions.
4. **Dead-Letter Queue (DLQ) & Poison-Pill Workbench:**
   - Displays quarantined payload envelopes with failure reason, raw payload, and stack traces.
   - **Autonomous ADK Agent Replay:** Button to invoke Gemini Agent Builder to diagnose and auto-redrive valid records.
   - **Tactile Hold-to-Approve Button (`#btnRedriveDlq`):** Requires a 1.2-second continuous press-and-hold with visual progress fill to prevent accidental production replays.
5. **Verifiable Audit Trail & BigQuery Execution Logs:**
   - Real-time table rendering jobs with columns: *Job ID*, *BigQuery Job Hash*, *Pipeline / Target*, *Timestamp (UTC)*, *Duration (ms)*, *Rows Processed*, *Status*, and *Self-Heal Badge*.
   - **Interactive Modal Inspection:** Clicking any row triggers a verified Google Cloud execution modal displaying full execution metadata, cryptographic hashes, and BigQuery job links.

---

### 3.3 View 3: Gemini E-Commerce Copilot (`#viewCopilot`)

A bounded, responsive three-pane analytics workspace with fluid splitters and conversational AI intelligence.

```
┌────────────────────┬─┬───────────────────────────────────────────┬─┬───────────────────────────────┐
│ PANE 1: CATALOG    │ │ PANE 2: INTERACTIVE CANVAS                │ │ PANE 3: COPILOT AGENT DRAWER  │
│ Width: 240px (fix) │R│ Flex: 1 1 0% (Min: 320px)                 │R│ Width: 380px (Drag: 280-900)  │
│                    │E│                                           │E│                               │
│ • Medallion Layers │S│ • Proactive Anomaly Banner (SLA Breaches) │S│ • Header: Expand/Compact [⤢]  │
│   - Gold Mart (3)  │I│ • 4 KPI Hero Metric Cards:                │I│ • Trust Pill: BigQuery DQS100%│
│   - Stage Refined  │Z│   - Total Storefront GMV ($1,058.00)      │Z│ • Lineage Breadcrumbs         │
│   - Raw Ingestion  │E│   - Net Realized Revenue ($1,026.11)      │E│ • Persistent Chat Stream:     │
│ • BigQuery Tables  │R│   - Revenue Realization Ratio (97.0%)     │R│   - User Message Bubbles      │
│   - fact_reconciled│ │   - Mastered Customers CSAT (4.25/5.0)    │ │   - Reasoning Indicator       │
│   - dim_customers  │L│ • Vega-Lite Visual Chart Canvas:          │R│   - Conversational AI Prose   │
│   - fact_orders    │E│   - Fee Variance (Amex vs. Visa)          │I│   - Tri-Modal Narrative Card  │
│ • External Sources │F│   - SLA Fulfillment Compliance Arc        │G│   - Clickable Guided Pills    │
│   - Stripe Settlement│   - Customer CSAT by Entity Bar Chart     │H│   - SQL & Contract Drawer     │
│   - SAP ERP Orders │T│   - Strategic Impact Priority Chart       │T│ • Sticky Chat Input & Send    │
│   - Zendesk CRM    │ │ • Chip Switchers (Revenue/SLA/CSAT)       │ │   (Enter key & click binding) │
└────────────────────┴─┴───────────────────────────────────────────┴─┴───────────────────────────────┘
```

#### Functional Requirements:
1. **Draggable Dual Resizer Handles (`.pane-resizer`):**
   - **Left Resizer (`#copilotResizerLeft`):** Draggable divider between Data Catalog and Center Canvas.
   - **Right Resizer (`#copilotResizerRight`):** Draggable divider between Center Canvas and Agent Drawer.
   - **Interaction Specs:**
     - Cursor: `col-resize`.
     - Grip bar with hover transition to Google Blue (`#4285f4`) with radial glow shadow.
     - Supports mouse and touch drag events, clamped between `280px` and container bounds.
     - Double-clicking the right resizer snaps the drawer between `380px` (standard) and `640px` (wide).
     - `#btnExpandAgentPane` in the drawer header provides one-click toggle with icon transition (`⤢` $\leftrightarrow$ `⤡`).
2. **Pane 1: Data Catalog Navigator (`#paneDomainNav`):**
   - Collapsible left rail with `#btnFoldLeftPane` (`⇤` / `⇥`).
   - Categorized asset tree: *Medallion Layers*, *BigQuery Tables (project-29e65474)*, and *External Ingestion Sources*.
   - Live row counts: `fact_reconciled_orders` (4), `dim_customers_master` (4), `fact_orders` (3).
3. **Pane 2: Unified Interactive Canvas (`#paneCenterCanvas`):**
   - **Proactive Anomaly Triage Stream Banner (`#proactiveTriageStream`):** Proactive alert badge for detected anomalies (e.g., *Order ORD-88103 SLA breach delay 48h, $137.50 gross, Chen Logistics*) with a one-click CTA: `Investigate in Copilot ➔`.
   - **E-Commerce KPI Hero Summary Cards:**
     - Storefront Gross GMV: `$1,058.00`
     - Net Realized Revenue: `$1,026.11`
     - Revenue Realization Ratio: `97.0%`
     - Mastered Customers CSAT: `4.25 / 5.0`
   - **Interactive Vega-Lite Chart Canvas (`#vegaChartContainer`):**
     - Renders declarative Vega-Lite v5 SVG/Canvas specifications dynamically delivered by backend queries.
     - Chip buttons for instant toggling: *Revenue Breakdown*, *Fulfillment SLA*, *Customer CSAT*.
4. **Pane 3: Gemini E-Commerce Copilot Drawer (`#paneAgentDrawer`):**
   - **Trust & Provenance Strip (`#copilotTrustBadge`):** Dynamic verification badge: `✓ Verified by BigQuery • Table: fact_reconciled_orders • Freshness: Real-time • DQS: 100%`. Lineage breadcrumb linking Stripe / SAP $\rightarrow$ Pandera $\rightarrow$ BigQuery.
   - **Persistent Multi-Turn Chat Stream (`#copilotChatStream`):**
     - Maintains complete session conversation history.
     - User messages render in right-aligned blue bubbles with `You 👤` author tags.
     - Live pulsating thinking indicator (`Reasoning across BigQuery gold mart & domain semantics...`).
     - Assistant messages render conversational analysis prose with markdown formatting.
   - **Tri-Modal Response Cards:**
     - **Layer 1: Executive Narrative:** Quantified headline takeaway, detailed explanation, and bulleted key drivers.
     - **Guided Exploration Pills:** Dynamic clickable suggestion chips (e.g., *💳 Brand Breakdown*, *⭐ Customer CSAT*, *⚠️ Delivery SLA Breaches*) that auto-execute follow-up queries when clicked.
     - **Layer 3: Progressive Code Disclosure Drawer:** Collapsible button (`</> View Verified BigQuery SQL & Pandera Contract`) revealing exact executed BigQuery SQL and the formal Pandera verification contract.
   - **Sticky Chat Input Bar (`#copilotQueryInput` + `#btnSendCopilotQuery`):**
     - Supports natural language typing with `Enter` key execution and loading button state (`Thinking...`).

---

## 4. Multi-Tenant Enterprise Control Plane

The platform includes a dedicated multi-tenant control plane allowing instant switching across 15 enterprise tenants.

| Tenant ID | Organization Name | Industry Vertical | Subscription Tier | Seeded Volume |
| :--- | :--- | :--- | :--- | :--- |
| `t_nexus_fintech` | Nexus-FinTech-Core | FinTech & Payments | Enterprise Gold | 3,500 rows |
| `t_apex_clearing` | Apex Clearing & Custody | FinTech & Trading | Enterprise Platinum | 3,500 rows |
| `t_sovereign_pay` | Sovereign Global Payments | Cross-Border Payments | Enterprise Gold | 3,500 rows |
| `t_acme_freight` | Acme Global Freight | Logistics & Shipping | Enterprise Gold | 3,500 rows |
| `t_chen_logistics`| Chen Logistics Singapore | Asia-Pac Logistics | Growth Tier | 3,500 rows |
| `t_eurorail_cargo`| EuroRail Intermodal | Supply Chain | Enterprise Standard | 3,500 rows |
| `t_thelook_ecom` | TheLook Apparel Storefront | Fashion E-Commerce | Enterprise Gold | 3,500 rows |
| `t_nordic_retail`| Nordic Living Design | Home Goods Retail | Growth Tier | 3,500 rows |
| `t_acro_electronics`| Acro Direct Consumer Tech | Electronics & IoT | Enterprise Gold | 3,500 rows |
| `t_aegis_clinical`| Aegis Clinical Diagnostics | Healthcare & Labs | Enterprise Platinum | 3,500 rows |
| `t_biogen_thera` | BioGen Therapeutics | Pharma Ingestion | Enterprise Platinum | 3,500 rows |
| `t_omnicare_hlth` | OmniCare Health Systems | Hospital Records | Enterprise Gold | 3,500 rows |
| `t_terra_agri` | Terra Sensor Networks | AgriTech & IoT | Growth Tier | 3,500 rows |
| `t_hydroflow_iot` | HydroFlow Water Utility | Infrastructure IoT | Enterprise Standard | 3,500 rows |
| `t_quantum_labs` | Quantum Materials Discovery| Materials Science | Innovation Lab | 3,500 rows |

### Continuous Streaming Telemetry Daemon:
- Runs in the frontend background every 8 seconds (`startContinuousPulse()`).
- Calls `/api/v1/telemetry/live?tenant_id={active_tenant}` to poll row counts, throughput (45–65 eps), p95 latency (90–125 ms), and auto-resolved drift counters.

---

## 5. Physical Warehouse Schema & Ground Truth Data

### 5.1 Dataset: `gold_analytics` (Project: `project-29e65474-32d7-45e0-803`)

#### Table: `fact_reconciled_orders`
| Column Name | BigQuery Data Type | Description & Domain Role | Sample Value |
| :--- | :--- | :--- | :--- |
| `order_id` | `STRING` | Primary key identifier | `ORD-88104` |
| `master_customer_id` | `STRING` | Foreign key to `dim_customers_master` | `MST_CUST_10422` |
| `thelook_gross_amount_usd` | `FLOAT64` | Storefront gross checkout value | `525.00` |
| `stripe_charge_amount_usd` | `FLOAT64` | Gross settlement amount from Stripe | `525.00` |
| `stripe_fee_amount_usd` | `FLOAT64` | Stripe payment gateway processing fee | `15.53` |
| `net_realized_revenue_usd` | `FLOAT64` | Realized net margin (Gross - Fee) | `509.47` |
| `payment_brand` | `STRING` | Payment card network (`visa`, `mastercard`, `amex`) | `amex` |
| `delivery_sla_breached` | `BOOL` | SLA breach flag (`TRUE` if delivery delay > 0 days) | `FALSE` |
| `reconciliation_status` | `STRING` | Conservation check (`BALANCED` if discrepancy = $0) | `BALANCED` |
| `order_date` | `TIMESTAMP` | Transaction creation timestamp | `2026-09-18 14:10:00 UTC` |

#### Table: `dim_customers_master`
| Column Name | BigQuery Data Type | Description & Domain Role | Sample Value |
| :--- | :--- | :--- | :--- |
| `master_customer_id` | `STRING` | Golden master entity identifier | `MST_CUST_10423` |
| `legal_company_name` | `STRING` | Enterprise business entity name | `Chen Logistics SG` |
| `primary_billing_email` | `STRING` | Finance billing contact | `billing@chenlogistics.sg` |
| `primary_country` | `STRING` | ISO country code | `SG` |
| `total_support_tickets` | `INT64` | Support desk incident count | `1` |
| `average_csat_score` | `FLOAT64` | Customer satisfaction rating (1.0 to 5.0 scale) | `3.0` |
| `mastering_confidence_score` | `FLOAT64` | Entity resolution confidence (0.0 to 1.0) | `0.96` |

---

## 6. Domain Semantic Reasoning & Mathematical Rules

The Copilot engine strictly enforces domain rules grounded in physical data:

1. **Conservation of Financial Revenue (Zero-Drift Invariant):**
   $$\text{Gross Amount} - \text{Gateway Fee} = \text{Net Realized Revenue} \pm \$0.00$$
   - Total Platform GMV: **$1,058.00**
   - Total Gateway Fees: **$31.89**
   - Total Net Realized Revenue: **$1,026.11** (97.0% realization ratio)
2. **Card Network Fee Dispersion & Take-Rate:**
   $$\text{Take Rate} = \frac{\text{Stripe Gateway Fee}}{\text{Gross Order Amount}} \times 100\%$$
   - **American Express (`ORD-88104`):** 2.95% ($15.53 on $525.00 gross) — Accounts for **48.7% of all transaction fees**.
   - **Visa (`ORD-88101`, `ORD-88103`):** 2.45% baseline average ($4.29 to $5.39).
   - **Mastercard (`ORD-88102`):** 3.03% ($6.68 on $220.00 gross).
   - **Margin Impact:** Amex enterprise orders dilute net margins by 55 bps relative to Visa.
3. **Carrier Fulfillment SLA & CSAT Degradation:**
   $$\text{SLA Breach Penalty} = \text{Baseline CSAT (4.5)} - 1.5 = 3.0$$
   - 1 of 4 orders (**25.0%**) breached delivery SLA.
   - Order `ORD-88103` (Chen Logistics SG) suffered a **48-hour carrier transit delay** in the Singapore customs hub.
   - Result: CSAT degraded to **3.0 / 5.0**, creating 1 escalated support ticket.
4. **Decoupled Data Quality (DQS) Formula:**
   $$\text{DQS} = 0.30(100\%) + 0.30(100\%) + 0.20(100\%) + 0.20(100\%) = 100.0\% \text{ (Grade A+)}$$

---

## 7. Backend API Specifications & Contracts

### 7.1 `POST /api/copilot/query`
- **Purpose:** Conversational query engine with Gemini 1.5 / Vertex AI and domain reasoning.
- **Request Body:**
  ```json
  { "query": "What are your strategic recommendations to fix this?" }
  ```
- **Response Structure (Tri-Modal):**
  ```json
  {
    "conversational_reply": "Based on verified BigQuery data, here are your top 3 strategic optimization priorities: 1. Remediate Asia-Pac Carrier SLA...",
    "query_understood": "Strategic E-Commerce Optimization & Action Plan",
    "trust_badge": {
      "verified_by": "BigQuery & Vertex AI",
      "project_id": "project-29e65474-32d7-45e0-803",
      "dataset": "gold_analytics",
      "table": "fact_reconciled_orders & dim_customers_master",
      "dqs_score": 100.0,
      "freshness": "Real-time Verified"
    },
    "layer_1_executive_narrative": {
      "headline": "Strategic Priorities: Recover At-Risk CSAT & Save 55 bps on Payment Fees",
      "summary": "Combining fulfillment metrics and gateway economics reveals clear actionable operational leverage...",
      "key_drivers": [
        "Priority 1: Recover Chen Logistics (Singapore) account by resolving customs transit bottleneck.",
        "Priority 2: Optimize Amex gateway fee drag on large enterprise orders (+$15.53 per order friction).",
        "Priority 3: Formalize VIP enterprise SLAs for 5.0 CSAT accounts (Acme Corp & Cyberdyne)."
      ],
      "guided_exploration_pills": [
        "Inspect Delivery SLA Breaches & Impact",
        "Compare Payment Brand Fee Variance (Amex vs Visa)",
        "Audit Customer CSAT by Revenue Tier",
        "Audit Reconciled Financials ($1,058.00)"
      ]
    },
    "layer_2_vega_lite_spec": {
      "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
      "description": "Margin and CSAT Improvement Impact",
      "data": { "values": [ ... ] },
      "mark": "bar",
      "encoding": { ... }
    },
    "layer_3_code_disclosure": {
      "bigquery_sql": "SELECT ... FROM `project-29e65474-32d7-45e0-803.gold_analytics...`",
      "pandera_verification_contract": "class RecommendationContract(pa.DataFrameModel): ..."
    }
  }
  ```

### 7.2 `GET /api/v1/telemetry/live?tenant_id={tenant_id}`
- **Purpose:** Polling endpoint for real-time HUD strip, execution logs, and DLQ state.
- **Response Structure:**
  ```json
  {
    "tenant_id": "t_nexus_fintech",
    "total_rows_processed": 52500,
    "current_throughput_eps": 54.2,
    "p95_latency_ms": 112.5,
    "auto_resolved_drift_count": 42,
    "mttr_ms": 184.2,
    "dqs_composite": 99.4,
    "recent_execution_logs": [ ... ],
    "dlq_quarantine_items": [ ... ]
  }
  ```

### 7.3 `POST /api/v1/chaos/run-scenario`
- **Request Body:**
  ```json
  { "scenario": "SCENARIO_1", "tenant_id": "t_nexus_fintech" }
  ```
- **Response Structure:**
  ```json
  {
    "scenario": "SCENARIO_1",
    "detected_drift": true,
    "synthesized_ast_code": "def repair_ast(df): ...",
    "verified_clean_rows": [ ... ],
    "duration_ms": 184.2
  }
  ```

### 7.4 `POST /api/v1/dlq/auto-diagnose-replay`
- **Request Body:** `{ "tenant_id": "t_nexus_fintech" }`
- **Response Structure:**
  ```json
  {
    "records_healed_and_replayed": 1,
    "bigquery_job_id": "job_bq_autoredrive_892314a",
    "pandera_contract_applied": "ReconciledOrderContract",
    "remaining_quarantined": 0
  }
  ```

---

## 8. UI/UX Style Guide & Design Tokens (For Google Stitch)

### 8.1 Color Palette & Token Nomenclature
| Token Name | Hex / CSS Value | Semantic Usage |
| :--- | :--- | :--- |
| `--bg-base` | `#0b0f19` | Main application background (Deep Obsidian) |
| `--bg-card` | `#111827` | Primary card & panel container surface |
| `--bg-rail` | `#0d131f` | Navigation bars, side rails, and drawer panels |
| `--bg-translucent` | `rgba(17, 24, 39, 0.75)` | Glassmorphism surfaces with `backdrop-filter: blur(12px)` |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Structural dividers, panel outlines |
| `--border-focus` | `#4285f4` | Focused input rings, active tab indicators |
| `--primary-blue` | `#4285f4` / `#2563eb` | Primary CTA, active selections, resizer drag highlight |
| `--accent-indigo` | `#6366f1` / `#818cf8` | Gemini AI intelligence markers, badges, and pills |
| `--success-emerald`| `#10b981` | 100% DQS compliance, on-time SLA, BALANCED financial ledger |
| `--warning-amber` | `#f59e0b` | Card take-rate variance, elevated gateway fees |
| `--danger-rose` | `#ef4444` | Carrier SLA delivery breach, DLQ poison pill quarantined |
| `--text-primary` | `#f8fafc` | Headers, primary data metrics, chat messages |
| `--text-muted` | `#94a3b8` | Column labels, metadata, timestamps, secondary captions |

### 8.2 Typography Hierarchy
- **Font Families:**
  - Standard UI: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
  - Monospace Data / SQL: `'Fira Code', 'Roboto Mono', Menlo, Consolas, monospace`
- **Scale:**
  - Large Hero Metrics: `1.5rem` / `24px`, Weight: `800`, Letter Spacing: `-0.02em`
  - Section Headers (`h2`, `h3`): `1.05rem` – `1.25rem`, Weight: `700`, Color: `#f8fafc`
  - Component Titles & Tabs: `0.88rem` / `14px`, Weight: `600`, Text Transform: None
  - Data Values & Body: `0.82rem` / `13px`, Line Height: `1.55`, Weight: `400` / `500`
  - Microcopy & Badges: `0.70rem` / `11px`, Weight: `600`, Letter Spacing: `0.04em`

### 8.3 Component Inventory & Interactive States Matrix

| Component | Default State | Hover State | Active / Focus State | Disabled / Loading State |
| :--- | :--- | :--- | :--- | :--- |
| **Top Nav Tab** | Dark gray text, transparent bg | `#1f2937` bg, white text | Bottom border `#4285f4` 2px, blue tint bg | N/A |
| **Tenant Selector Dropdown** | Deep blue-gray pill, border subtle | Outline glow, chevron rotates | Dropdown menu opens (15 items) | Grayed opacity 0.5 |
| **Draggable Pane Splitter** | 8px width, subtle border | Line turns `#4285f4`, radial glow | Cursor `col-resize`, blue guide shadow | N/A |
| **Expand Drawer Button** | Square ghost icon button | Indigo tint bg, tooltip `Expand` | Icon toggles `⤢` $\leftrightarrow$ `⤡`, drawer 640px | Disabled during drag |
| **Guided Exploration Pill** | Indigo badge border, translucent bg | Scale 1.02x, brighter border `#818cf8` | Triggers immediate query dispatch | Dimmed 0.6x during inference |
| **Copilot Send Button** | Solid `#2563eb`, white arrow | Bright `#3b82f6`, shadow glow | Depressed 0.98x scale | Label `Thinking...`, spinner icon |
| **Hold-to-Approve DLQ Button** | Dark crimson border, red text | Red background glow | Track fills over 1.2s linearly | Replaying spinner, button locked |
| **Execution Log Table Row** | Transparent row, subtle bottom border | Row bg `rgba(255,255,255,0.03)` | Click opens Modal Inspector | N/A |

### 8.4 Micro-Interactions & Animation Specifications
1. **Chat Bubble Dynamics:**
   - User messages animate in from bottom-right with `cubic-bezier(0.16, 1, 0.3, 1)` (duration: 220ms).
   - Reasoning indicator pulses with continuous 1.5s opacity oscillation (`opacity: 0.4` $\leftrightarrow$ `1.0`).
   - Assistant answers fade in smoothly with syntax-highlighted code blocks and clickable exploration pills.
2. **Draggable Resizer Drag Physics:**
   - Real-time `pointermove` binding with `user-select: none` on `document.body` to eliminate text selection during drags.
   - Smooth clamp between 280px and container boundary without layout thrashing.
3. **Tactile Safety Guard:**
   - Continuous 1,200ms press required on `#btnRedriveDlq`. If released at 1,199ms, fill resets smoothly to 0% in 150ms.
4. **Vega-Lite Responsive Resize:**
   - Automatically re-renders chart widths upon drawer resize completion using custom window resize hooks.

---

## 9. Target Personas & Core User Journeys

### Persona A: Lead Data Architect & Platform Engineer ("Elena")
- **Goal:** Monitor pipeline health, verify schema synthesis accuracy, and ensure zero schema drift enters production BigQuery tables.
- **Primary Journey:**
  1. Opens **SchemaForge Data-OS** and reviews the top live streaming telemetry HUD (52,500 rows, 0 DLQ).
  2. Navigates to **Synthesis Studio** (`#viewStudio`) and runs `SCENARIO_1` chaos drill.
  3. Watches the system detect the AST discrepancy, induce a self-healing rule in 184ms, and verify against Pandera.
  4. Inspects the **Ingestion Observability DAG** (`#viewObservability`) to verify the self-heal badge in BigQuery execution logs.

### Persona B: E-Commerce Operations & FinOps Lead ("Marcus")
- **Goal:** Reconcile gateway processing fees against gross GMV and eliminate carrier delivery SLA breaches.
- **Primary Journey:**
  1. Navigates to **Gemini E-Commerce Copilot** (`#viewCopilot`).
  2. Clicks the **Proactive Anomaly Banner** warning of the Chen Logistics 48-hour delivery delay.
  3. Asks Copilot: *"What is the gateway fee variance between Amex and Visa?"*
  4. Observes the Center Canvas switch dynamically to the fee distribution chart showing Amex at 2.95% vs Visa at 2.40%.
  5. Reviews the recommendations drawer to adjust carrier contracts and optimize checkout payment routing.

---

## 10. Google Stitch Redesign Recommendations & Guidelines

When importing this specification into **Google Stitch** for redesigning, focus on the following opportunities:

1. **Elevation & Glassmorphism Surfaces:**
   - Upgrade the current flat dark cards to multi-tiered elevations:
     - Level 0: `#0b0f19` (Canvas canvas)
     - Level 1: `rgba(17, 24, 39, 0.85)` with `backdrop-filter: blur(16px)` and `border: 1px solid rgba(255, 255, 255, 0.08)`
     - Level 2 (Modals / Overlays): `rgba(30, 41, 59, 0.95)` with deep ambient shadow `0 20px 40px -10px rgba(0, 0, 0, 0.6)`
2. **Component Unification:**
   - Align all badges (DQS, SLA, Verified, Balanced) to a unified pill shape with a 6px status dot indicator.
   - Standardize all action icon buttons to 36x36px with 8px corner radius.
3. **Draggable Resizer Visual Polish:**
   - In Stitch, design a sleek central grip handle icon (3 vertical dots `⋮` or double vertical bar `||`) centered vertically on the resizer bar that illuminates on hover.
4. **Data Visualization Consistency:**
   - Apply curated color tokens to Vega-Lite SVG charts to match the UI:
     - Blue (`#4285f4`): Gross Volume & Primary Series
     - Emerald (`#10b981`): Net Realized Revenue & CSAT
     - Amber (`#f59e0b`): Stripe Gateway Fees
     - Rose (`#ef4444`): SLA Breaches & Lost Margin
5. **Accessibility Standards (WCAG 2.1 AA):**
   - Ensure all text-to-background contrast ratios exceed `4.5:1` (especially `--text-muted` `#94a3b8` on `#111827`).
   - Implement clear visible `:focus-visible` outline rings (`2px solid #4285f4`) for keyboard accessibility across all interactive controls.

---

## 11. Verification & Live Deployment Links

- **Live Google Cloud Run Instance:** [https://schemaforge-app-605335322761.us-central1.run.app](https://schemaforge-app-605335322761.us-central1.run.app)
- **Direct Link — Gemini Copilot:** [https://schemaforge-app-605335322761.us-central1.run.app/#viewCopilot](https://schemaforge-app-605335322761.us-central1.run.app/#viewCopilot)
- **Direct Link — Ingestion Observability & DLQ:** [https://schemaforge-app-605335322761.us-central1.run.app/#viewObservability](https://schemaforge-app-605335322761.us-central1.run.app/#viewObservability)
- **Direct Link — Neuro-Symbolic Synthesis Studio:** [https://schemaforge-app-605335322761.us-central1.run.app/#viewStudio](https://schemaforge-app-605335322761.us-central1.run.app/#viewStudio)

