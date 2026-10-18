import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

slides_dir = Path("scripts/long_video_slides")
slides_dir.mkdir(parents=True, exist_ok=True)

# Load fonts
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 44)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 23)
font_section = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 21)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 25)
font_card_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 19)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
font_stat_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_stat_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)

def create_base_canvas(scene_num, scene_tag):
    img = Image.new("RGB", (1920, 1080), color=(10, 12, 18))
    draw = ImageDraw.Draw(img)
    
    # Subtle top accent line
    draw.line([(0, 0), (1920, 0)], fill=(59, 130, 246), width=4)
    
    # Top Navbar Bar - Clean, spacious, NO voice badges or emojis!
    draw.rectangle([(60, 35), (1860, 95)], fill=(18, 22, 34), outline=(38, 45, 68), width=1)
    
    # Brand logo icon
    draw.ellipse([(80, 47), (116, 83)], fill=(37, 99, 235))
    draw.polygon([(90, 73), (98, 55), (106, 73)], fill=(255, 255, 255))
    draw.text((130, 52), "SCHEMAFORGE DATA-OS", fill=(255, 255, 255), font=font_section)
    draw.text((395, 52), "|   Google Cloud AI & Innovation Cup 2026", fill=(148, 163, 184), font=font_subtitle)
    
    # Right scene pill - Clean, perfectly sized, no text cutoff
    draw.rounded_rectangle([(1450, 45), (1840, 85)], radius=8, fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    draw.text((1475, 53), f"SCENE 0{scene_num}: {scene_tag}", fill=(56, 189, 248), font=font_badge)
    
    # Bottom Telemetry Status Bar
    draw.rectangle([(60, 985), (1860, 1045)], fill=(18, 22, 34), outline=(38, 45, 68), width=1)
    draw.ellipse([(85, 1007), (97, 1019)], fill=(16, 185, 129))
    draw.text((110, 1003), "LIVE PRODUCTION INSTANCE: schemaforge-app-605335322761.us-central1.run.app", fill=(203, 213, 225), font=font_card_body)
    draw.text((940, 1003), "•   MTTR: 406.8ms   •   DQS: 100%   •   INVARIANTS: PASS 100%", fill=(56, 189, 248), font=font_card_body)
    draw.text((1600, 1003), "WAREHOUSE: gold_analytics", fill=(148, 163, 184), font=font_card_body)
    
    return img, draw

# ==========================================
# SLIDE 1: THE $100B CRISIS
# ==========================================
def make_slide_1():
    img, draw = create_base_canvas(1, "PROBLEM STATEMENT")
    
    draw.text((60, 125), "The $100B Enterprise Data Downtime Crisis", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Why Traditional Ingestion Pipelines (Airflow, dbt, Spark) Crash on Polymorphic Enterprise Files", fill=(148, 163, 184), font=font_subtitle)
    
    # Left: Messy Payload Card
    draw.rounded_rectangle([(60, 245), (930, 785)], radius=12, fill=(18, 22, 34), outline=(239, 68, 68), width=2)
    draw.text((85, 270), "💥 The Raw Ingestion Payload (sample_data/messy_sap_orders.json)", fill=(248, 113, 113), font=font_card_title)
    
    code = (
        "[\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98124\",\n"
        "    \"CUST_INFO\": { \"id\": 10421, \"name\": \"Acro APAC\" },  <-- NESTED OBJECT\n"
        "    \"TX_DATE\": \"2026-09-12T14:30:00Z\",               <-- ISO-8601 STRING\n"
        "    \"LINE_ITEMS\": [{ \"sku\": \"SKU-99\", \"qty\": 4, \"price\": 25.50 }]\n"
        "  },\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98125\",\n"
        "    \"CUST_INFO\": \"CUST_99120\",                       <-- FLAT STRING ID!\n"
        "    \"TX_DATE\": 1789218000,                            <-- UNIX EPOCH INTEGER!\n"
        "    \"LINE_ITEMS\": \"SKU-44:2:45.00,SKU-88:1:15.00\"     <-- COLON DELIMITED!\n"
        "  },\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98126\",\n"
        "    \"CUST_INFO\": { \"cust_code\": \"CUST_5501\" },       <-- ALTERED KEYS!\n"
        "    \"TX_DATE\": \"15/09/2026\"                           <-- SLASH NOTATION!\n"
        "  }\n"
        "]"
    )
    draw.text((85, 315), code, fill=(226, 232, 240), font=font_code)
    
    # Right: Failure Cascade Card
    draw.rounded_rectangle([(970, 245), (1860, 785)], radius=12, fill=(18, 22, 34), outline=(51, 65, 85), width=1)
    draw.text((1000, 270), "⚠️ The Catastrophic Failure Cascade in Enterprise Stacks", fill=(251, 191, 36), font=font_card_title)
    
    bullets = [
        ("❌ Fatal Pipeline Crashes:", "Static DAGs fail immediately on unexpected keys or types, throwing HTTP 500 or ValueError exceptions."),
        ("❌ Silent Data Corruption:", "Permissive parsers ingest unhandled fields as NULLs, poisoning downstream ML feature stores and dashboards."),
        ("❌ Engineering Sprint Drain:", "Data engineers spend over 40% of weekly sprints triage-patching fragile regex and coordinating backfills."),
        ("❌ Zero Self-Correction:", "Traditional ETL architectures lack structural reasoning and require human intervention for every schema shift.")
    ]
    y = 335
    for h, d in bullets:
        draw.text((1000, y), h, fill=(248, 113, 113), font=font_card_title)
        draw.text((1000, y + 34), d, fill=(203, 213, 225), font=font_card_body)
        y += 105
        
    # Bottom Stats Bar
    stat_boxes = [
        (60, 815, 630, 945, "$100B+", "Annual Global Enterprise Data Downtime Cost", (239, 68, 68)),
        (675, 815, 1245, 945, "40% of Sprints", "Data Engineering Velocity Lost to Break-Fix Triage", (245, 158, 11)),
        (1290, 815, 1860, 945, "0 Seconds", "Advance Warning Before Upstream API Payloads Mutate", (59, 130, 246))
    ]
    for x1, y1, x2, y2, val, lbl, col in stat_boxes:
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(18, 22, 34), outline=(38, 45, 68), width=1)
        draw.text((x1 + 30, y1 + 18), val, fill=col, font=font_stat_val)
        draw.text((x1 + 30, y1 + 72), lbl, fill=(148, 163, 184), font=font_stat_lbl)
        
    return img

# ==========================================
# SLIDE 2: TRACK JUSTIFICATION
# ==========================================
def make_slide_2():
    img, draw = create_base_canvas(2, "TRACK JUSTIFICATION")
    
    draw.text((60, 125), "Competition Track Justification & Strategic Fit", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Why Autonomous Data Engineering is the Foundational Pillar of Real-World Enterprise AI", fill=(148, 163, 184), font=font_subtitle)
    
    # Left: The Superficial AI Trap
    draw.rounded_rectangle([(60, 255), (930, 775)], radius=12, fill=(18, 22, 34), outline=(239, 68, 68), width=1)
    draw.text((95, 285), "⚠️ The Superficial GenAI Wrapper Trap", fill=(248, 113, 113), font=font_card_title)
    
    flaws = [
        ("• Naive Prompt Engineering:", "Building chatbots that translate questions directly to SQL without understanding physical schema constraints."),
        ("• Hallucinated Column Mappings:", "LLMs invent non-existent column names, causing queries to fail or return corrupted numbers."),
        ("• Zero Runtime Safety:", "Raw generated code executed without sandboxes or formal mathematical verification."),
        ("• Ignored Ingestion Flaws:", "Assumes data in the warehouse is magically clean, ignoring that upstream pipelines are constantly breaking.")
    ]
    y = 350
    for h, d in flaws:
        draw.text((95, y), h, fill=(255, 255, 255), font=font_badge)
        draw.text((95, y + 28), d, fill=(203, 213, 225), font=font_card_body)
        y += 100
        
    # Right: SchemaForge Data-OS
    draw.rounded_rectangle([(970, 255), (1860, 775)], radius=12, fill=(18, 22, 34), outline=(16, 185, 129), width=2)
    draw.text((1005, 285), "✅ The SchemaForge Autonomous Data-OS Paradigm", fill=(52, 211, 153), font=font_card_title)
    
    pros = [
        ("• Ingestion Boundary Autonomous Defense:", "Interprets and auto-heals incoming messy payloads BEFORE they touch analytical warehouses."),
        ("• Neuro-Symbolic Verification:", "Combines Gemini 1.5 generative program synthesis with deterministic AST checks and Pandera contracts."),
        ("• Mathematical Financial Invariants:", "Guarantees zero data loss, exact schema conformance, and financial reconciliation (∑Gross == ∑Billed)."),
        ("• 100% Serverless Google Cloud Native:", "Cloud Run + Pub/Sub + Gemini + BigQuery delivers sub-second MTTR with zero cold-starts.")
    ]
    y = 350
    for h, d in pros:
        draw.text((1005, y), h, fill=(52, 211, 153), font=font_badge)
        draw.text((1005, y + 28), d, fill=(203, 213, 225), font=font_card_body)
        y += 100

    # Bottom Strategic Banner
    draw.rounded_rectangle([(60, 810), (1860, 945)], radius=10, fill=(24, 30, 48), outline=(59, 130, 246), width=1)
    draw.text((95, 835), "🎯 Core Thesis: Generative AI cannot succeed in the enterprise without an Autonomous Data-OS at the ingestion layer.", fill=(255, 255, 255), font=font_card_title)
    draw.text((95, 885), "SchemaForge solves the root cause of data downtime, delivering self-healing pipelines that protect downstream AI models.", fill=(148, 163, 184), font=font_subtitle)
    
    return img

# ==========================================
# SLIDE 3: ARC-AGI INGESTION AGENT
# ==========================================
def make_slide_3():
    img, draw = create_base_canvas(3, "THE ARC-AGI AGENT")
    
    draw.text((60, 125), "The Novel Approach: ARC-AGI Autonomous File Ingestion", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Adapting the Abstraction & Reasoning Corpus (ARC-AGI) Benchmark to Autonomous Data Engineering", fill=(148, 163, 184), font=font_subtitle)
    
    # 4 Architecture Flow Stages
    stages = [
        (60, 245, 480, 440, "1. Input Profiler", "• Spatial JSONPath extraction\n• Polymorphic type inference\n• Automated PII redaction\n• Null ratio & cardinality metrics", (59, 130, 246)),
        (520, 245, 940, 440, "2. Gemini 1.5 Pro ARC Engine", "• Zero-shot structural reasoning\n• Multi-strategy AST synthesis\n• Vectorized Polars & Pandas\n• Pure dictionary comprehension", (168, 85, 247)),
        (980, 245, 1400, 440, "3. gVisor Security Sandbox", "• Isolated sub-process sandbox\n• Static AST security audit\n• Terminated on os/socket syscalls\n• Strict 5.0s execution ceiling", (16, 185, 129)),
        (1440, 245, 1860, 440, "4. Invariant Gate", "• Pandera Schema contracts\n• Financial conservation check\n• ∑ Gross == ∑ Billed ($0.01)\n• Instant BigQuery Dispatch", (6, 182, 212))
    ]
    for x1, y1, x2, y2, stitle, sdesc, col in stages:
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(18, 22, 34), outline=col, width=2)
        draw.text((x1 + 25, y1 + 18), stitle, fill=col, font=font_card_title)
        draw.text((x1 + 25, y1 + 60), sdesc, fill=(203, 213, 225), font=font_card_body)
        
    # Large Synthesized Code Showcase Card
    draw.rounded_rectangle([(60, 465), (1860, 945)], radius=12, fill=(14, 18, 28), outline=(38, 45, 68), width=1)
    draw.text((90, 490), "⚡ Autonomously Synthesized Python AST Program (Generated by Gemini 1.5 Pro in 406ms)", fill=(56, 189, 248), font=font_card_title)
    
    syn_code = (
        "def transform_sap_orders(raw_records):\n"
        "    clean_orders = []\n"
        "    for r in raw_records:\n"
        "        # 1. Autonomous Customer ID Normalization (resolves polymorphic dict vs flat string)\n"
        "        cust = r.get('CUST_INFO')\n"
        "        cust_id = str(cust.get('id') or cust.get('cust_code')) if isinstance(cust, dict) else str(cust)\n\n"
        "        # 2. Polymorphic Timestamp Parser (resolves ISO-8601 strings, Unix epoch integers, and European slash dates)\n"
        "        dt = r.get('TX_DATE')\n"
        "        order_date = datetime.fromtimestamp(dt, tz=timezone.utc).date() if isinstance(dt, int) else ...\n\n"
        "        # 3. Polymorphic Line Item Parser with Financial Summation\n"
        "        items = r.get('LINE_ITEMS')\n"
        "        total_usd = sum(int(q)*float(p) for _, q, p in [p.split(':') for p in items.split(',')]) if isinstance(items, str) ...\n\n"
        "        clean_orders.append({ 'order_id': r.get('HEADER'), 'customer_id': cust_id, 'total_amount_usd': total_usd, ... })\n"
        "    return clean_orders"
    )
    draw.text((90, 535), syn_code, fill=(226, 232, 240), font=font_code)
    
    return img

# ==========================================
# SLIDE 4: GEMINI UTILIZATION
# ==========================================
def make_slide_4():
    img, draw = create_base_canvas(4, "GEMINI UTILIZATION")
    
    draw.text((60, 125), "Deep Google Gemini 1.5 Neuro-Symbolic Integration", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Dual-Model Architecture: Gemini 1.5 Pro (Program Synthesis) & Gemini 1.5 Flash (Conversational Copilot)", fill=(148, 163, 184), font=font_subtitle)
    
    # Left: Gemini 1.5 Pro
    draw.rounded_rectangle([(60, 255), (930, 940)], radius=12, fill=(18, 22, 34), outline=(168, 85, 247), width=2)
    draw.text((95, 285), "🧠 Google Gemini 1.5 Pro: Synthesis Engine", fill=(192, 132, 252), font=font_card_title)
    
    pro_points = [
        ("• Low-Entropy Determinism:", "Configured with temperature 0.2 for strict, reproducible code generation free of creative hallucination."),
        ("• Multi-Strategy Program Search:", "Generates 3 diverse candidate solutions: Polars vectorized expressions, Pandas DataFrame transformations, and lightweight dict comprehensions."),
        ("• Companion Contract Generation:", "Co-generates formal Pandera schema contracts alongside code to establish deterministic validation assertions."),
        ("• Automated Reflexion Loop:", "If execution fails an invariant, Gemini receives the exact stack trace and schema mismatch matrix to self-correct in <200ms.")
    ]
    y = 350
    for h, d in pro_points:
        draw.text((95, y), h, fill=(255, 255, 255), font=font_badge)
        draw.text((95, y + 28), d, fill=(203, 213, 225), font=font_card_body)
        y += 135

    # Right: Gemini 1.5 Flash
    draw.rounded_rectangle([(970, 255), (1860, 940)], radius=12, fill=(18, 22, 34), outline=(56, 189, 248), width=2)
    draw.text((1005, 285), "⚡ Google Gemini 1.5 Flash: E-Commerce Copilot", fill=(56, 189, 248), font=font_card_title)
    
    flash_points = [
        ("• Live BigQuery Grounding:", "Prompts are deeply grounded in real warehouse schema metadata from gold_analytics without hardcoded table context."),
        ("• Tri-Modal Response Delivery:", "Generates an Executive Narrative summary, interactive Vega-Lite visual charts, and verified executable BigQuery SQL queries."),
        ("• Sub-Second Latency Profiling:", "Delivers real-time responses to business questions in under 800ms, enabling seamless interactive exploration."),
        ("• Complete Lineage Transparency:", "Exposes complete data lineage breadcrumbs from upstream raw Pub/Sub topics to golden reconciled BigQuery fact tables.")
    ]
    y = 350
    for h, d in flash_points:
        draw.text((1005, y), h, fill=(255, 255, 255), font=font_badge)
        draw.text((1005, y + 28), d, fill=(203, 213, 225), font=font_card_body)
        y += 135

    return img

# ==========================================
# SLIDE 5: FORMAL SAFETY & SANDBOX
# ==========================================
def make_slide_5():
    img, draw = create_base_canvas(5, "FORMAL SAFETY & SANDBOX")
    
    draw.text((60, 125), "Formal Verification: gVisor Sandbox & Invariant Gates", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Eliminating Rogue Code: Isolated Container Sandboxing and Mathematical Conservation Proofs", fill=(148, 163, 184), font=font_subtitle)
    
    # Card 1: gVisor Sandbox
    draw.rounded_rectangle([(60, 255), (620, 935)], radius=12, fill=(18, 22, 34), outline=(59, 130, 246), width=2)
    draw.text((90, 285), "🛡️ gVisor Sandbox Security", fill=(96, 165, 250), font=font_card_title)
    draw.text((90, 335), "Candidate code executes in an\nisolated container environment:", fill=(148, 163, 184), font=font_card_body)
    
    bullets1 = [
        ("🔒 Static AST Auditing:", "Statically rejects code with os, sys, subprocess, socket, eval, exec."),
        ("⏱️ Execution Timeouts:", "Enforces hard 5.0s CPU ceiling via POSIX signal termination."),
        ("📦 Memory Bounds:", "Capped at 256 MiB working RAM to prevent memory exhaustion."),
        ("🚫 Quarantine Routing:", "Unsafe code routed directly to Pub/Sub Dead-Letter Queue.")
    ]
    y = 415
    for h, b in bullets1:
        draw.text((90, y), h, fill=(255, 255, 255), font=font_badge)
        draw.text((90, y + 26), b, fill=(203, 213, 225), font=font_card_body)
        y += 115

    # Card 2: Pandera Contracts
    draw.rounded_rectangle([(660, 255), (1260, 935)], radius=12, fill=(18, 22, 34), outline=(168, 85, 247), width=2)
    draw.text((690, 285), "📜 Pandera Schema Contracts", fill=(192, 132, 252), font=font_card_title)
    draw.text((690, 335), "Co-generated formal contracts\nverify types deterministically:", fill=(148, 163, 184), font=font_card_body)
    
    p_code = (
        "schema = pa.DataFrameSchema({\n"
        "  'order_id': Column(str,\n"
        "    Check.str_matches(r'^ORD-\\d+$'),\n"
        "    nullable=False),\n"
        "  'customer_id': Column(str,\n"
        "    nullable=False),\n"
        "  'order_date': Column(pa.Date,\n"
        "    nullable=False),\n"
        "  'total_amount_usd': Column(float,\n"
        "    Check.greater_than(0.0),\n"
        "    nullable=False),\n"
        "  'status': Column(str,\n"
        "    Check.isin(['PLACED', 'SHIPPED',\n"
        "               'DELIVERED']),\n"
        "    nullable=False)\n"
        "})"
    )
    draw.text((690, 415), p_code, fill=(226, 232, 240), font=font_code)

    # Card 3: Mathematical Invariant
    draw.rounded_rectangle([(1300, 255), (1860, 935)], radius=12, fill=(18, 22, 34), outline=(16, 185, 129), width=2)
    draw.text((1330, 285), "⚖️ Financial Invariant Proof", fill=(52, 211, 153), font=font_card_title)
    draw.text((1330, 335), "Mathematical conservation proofs\nprevent financial data leakage:", fill=(148, 163, 184), font=font_card_body)
    
    inv_bullets = [
        ("∑ Gross == ∑ Billed:", "Total calculated line items strictly match order header amount within ε < $0.01 tolerance."),
        ("Zero Null Invariance:", "Primary business identifiers cannot contain NULL or NaN values under any transform."),
        ("Reflexion Feedback Loop:", "Failed invariants feed exact error diffs back to Gemini for sub-200ms self-correction."),
        ("100% Invariant Pass Rate:", "Verified across 46 chaos drills with zero data corruption in production BigQuery.")
    ]
    y = 415
    for h, b in inv_bullets:
        draw.text((1330, y), h, fill=(52, 211, 153), font=font_badge)
        draw.text((1330, y + 26), b, fill=(203, 213, 225), font=font_card_body)
        y += 115

    return img

# ==========================================
# SLIDE 6: GCP ARCHITECTURE
# ==========================================
def make_slide_6():
    img, draw = create_base_canvas(6, "GCP ARCHITECTURE")
    
    draw.text((60, 125), "Google Cloud Native Distributed Architecture", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Serverless Production Topology: Cloud Run Compute, Pub/Sub Event Buffer & DLQ, BigQuery Lakehouse", fill=(148, 163, 184), font=font_subtitle)
    
    # Left: Embed Architecture Topology Image
    jpg_path = Path("docs/assets/gcp_system_architecture_diagram.jpg")
    if jpg_path.exists():
        arch_img = Image.open(jpg_path).convert("RGB")
        arch_img = arch_img.resize((960, 650), Image.Resampling.LANCZOS)
        img.paste(arch_img, (60, 265))
        draw.rectangle([(60, 265), (1020, 915)], outline=(38, 45, 68), width=2)
    
    # Right: Service Cards
    services = [
        ("🚀 Google Cloud Run (Compute Tier)", "Stateless FastAPI 0.110 engine, 80 concurrent requests/container, horizontal autoscaling (1 to 10 instances), gVisor sandbox.", (59, 130, 246)),
        ("⚡ Google Cloud Pub/Sub (Buffer & DLQ)", "Asynchronous decoupled event ingestion buffer with dedicated Dead-Letter Queue (DLQ) for poison-pill quarantine and zero event loss.", (34, 197, 94)),
        ("🧠 Google Gemini 1.5 Pro & Flash (AI Tier)", "Low-entropy neuro-symbolic program synthesis, invariant verification feedback loop, and domain-grounded E-Commerce Copilot.", (168, 85, 247)),
        ("📊 Google Cloud BigQuery (Lakehouse Tier)", "Multi-tenant gold_analytics dataset with fact_reconciled_orders partitioned by date and clustered by tenant. High-throughput streaming.", (6, 182, 212)),
        ("📡 Google Cloud Logging (Observability)", "Centralized structured JSON telemetry with correlation trace IDs, MTTR latency profiling, and audit event tracking.", (245, 158, 11))
    ]
    
    y = 265
    for stitle, sdesc, scol in services:
        draw.rounded_rectangle([(1050, y), (1860, y + 115)], radius=10, fill=(18, 22, 34), outline=scol, width=1)
        draw.text((1075, y + 16), stitle, fill=scol, font=font_card_title)
        draw.text((1075, y + 52), sdesc, fill=(203, 213, 225), font=font_card_body)
        y += 133

    return img

# ==========================================
# SLIDE 7: LIVE DEMONSTRATION
# ==========================================
def make_slide_7():
    img, draw = create_base_canvas(7, "LIVE DEMONSTRATION")
    
    draw.text((60, 125), "Live Production Solution Walkthrough & Real Results", fill=(255, 255, 255), font=font_title)
    draw.text((60, 185), "Live Deployment on Google Cloud Run: Sub-Second Self-Healing, DLQ Quarantine, and Conversational Copilot", fill=(148, 163, 184), font=font_subtitle)
    
    # Left: Chaos Drill Real Screen
    screen1_path = Path("scripts/video_assets/live_view1_chaos_healed.png")
    if screen1_path.exists():
        sc1 = Image.open(screen1_path).convert("RGB")
        sc1 = sc1.resize((920, 650), Image.Resampling.LANCZOS)
        img.paste(sc1, (60, 265))
        draw.rectangle([(60, 265), (980, 915)], outline=(59, 130, 246), width=2)
        
    # Right Top: Observability Real Screen
    screen2_path = Path("scripts/video_assets/live_view2_observability_full.png")
    if screen2_path.exists():
        sc2 = Image.open(screen2_path).convert("RGB")
        sc2 = sc2.resize((840, 310), Image.Resampling.LANCZOS)
        img.paste(sc2, (1020, 265))
        draw.rectangle([(1020, 265), (1860, 575)], outline=(16, 185, 129), width=2)

    # Right Bottom: Copilot Real Screen
    screen3_path = Path("scripts/video_assets/live_copilot_domain_insights.png")
    if screen3_path.exists():
        sc3 = Image.open(screen3_path).convert("RGB")
        sc3 = sc3.resize((840, 310), Image.Resampling.LANCZOS)
        img.paste(sc3, (1020, 605))
        draw.rectangle([(1020, 605), (1860, 915)], outline=(168, 85, 247), width=2)

    return img

print("Rendering 7 high-resolution 1920x1080 scene slides (WITHOUT voice badge)...")
s1 = make_slide_1(); s1.save(slides_dir / "scene_01.png"); print("Saved scene_01.png")
s2 = make_slide_2(); s2.save(slides_dir / "scene_02.png"); print("Saved scene_02.png")
s3 = make_slide_3(); s3.save(slides_dir / "scene_03.png"); print("Saved scene_03.png")
s4 = make_slide_4(); s4.save(slides_dir / "scene_04.png"); print("Saved scene_04.png")
s5 = make_slide_5(); s5.save(slides_dir / "scene_05.png"); print("Saved scene_05.png")
s6 = make_slide_6(); s6.save(slides_dir / "scene_06.png"); print("Saved scene_06.png")
s7 = make_slide_7(); s7.save(slides_dir / "scene_07.png"); print("Saved scene_07.png")
print("All 7 slides generated successfully with pristine clean headers!")
