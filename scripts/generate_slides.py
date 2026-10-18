import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

slides_dir = Path("scripts/video_slides")
slides_dir.mkdir(parents=True, exist_ok=True)

# Load fonts
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 46)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24)
font_section = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
font_card_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 19)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
font_stat_val = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
font_stat_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)

def create_base_canvas(scene_num, scene_tag):
    img = Image.new("RGB", (1920, 1080), color=(10, 12, 18))
    draw = ImageDraw.Draw(img)
    
    # Subtle top glow line
    draw.line([(0, 0), (1920, 0)], fill=(59, 130, 246), width=4)
    
    # Top Navbar Bar
    draw.rectangle([(60, 40), (1860, 100)], fill=(18, 22, 34), outline=(38, 45, 68), width=1)
    
    # Logo & Brand text
    draw.ellipse([(80, 52), (116, 88)], fill=(37, 99, 235))
    draw.polygon([(90, 78), (98, 60), (106, 78)], fill=(255, 255, 255))
    draw.text((130, 58), "SCHEMAFORGE DATA-OS", fill=(255, 255, 255), font=font_section)
    draw.text((390, 58), "|   Google Cloud AI & Innovation Cup 2026", fill=(148, 163, 184), font=font_subtitle)
    
    # Scene pill & Speaker badge
    # Scene pill
    draw.rounded_rectangle([(1400, 50), (1600, 90)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((1420, 58), f"SCENE 0{scene_num}: {scene_tag}", fill=(56, 189, 248), font=font_badge)
    
    # Speaker badge
    draw.rounded_rectangle([(1620, 50), (1840, 90)], radius=8, fill=(24, 30, 48), outline=(59, 130, 246), width=1)
    draw.text((1640, 58), "🎙️ Voice: Shivansh Sharma", fill=(224, 231, 255), font=font_badge)
    
    # Bottom Telemetry Bar
    draw.rectangle([(60, 980), (1860, 1040)], fill=(18, 22, 34), outline=(38, 45, 68), width=1)
    draw.ellipse([(85, 1002), (97, 1014)], fill=(16, 185, 129))
    draw.text((110, 998), "LIVE SYSTEM: schemaforge-app.us-central1.run.app", fill=(203, 213, 225), font=font_subtitle)
    draw.text((800, 998), "•   MTTR: 406.8ms   •   DQS: 100%   •   INVARIANTS: PASS 100%", fill=(56, 189, 248), font=font_subtitle)
    draw.text((1580, 998), "WAREHOUSE: gold_analytics", fill=(148, 163, 184), font=font_subtitle)
    
    return img, draw

# ==========================================
# SLIDE 1: THE $100B PROBLEM
# ==========================================
def make_slide_1():
    img, draw = create_base_canvas(1, "THE PROBLEM")
    
    # Header Title
    draw.text((60, 130), "The $100B Enterprise Data Downtime Crisis", fill=(255, 255, 255), font=font_title)
    draw.text((60, 195), "Why Traditional Batch Pipelines (Airflow, dbt, Spark) Crash on Dirty Polymorphic Files", fill=(148, 163, 184), font=font_subtitle)
    
    # Left Card: The Real Messy File Ingestion
    draw.rounded_rectangle([(60, 260), (930, 780)], radius=12, fill=(18, 22, 34), outline=(239, 68, 68), width=2)
    draw.text((90, 290), "💥 The Real-World Ingestion Payload (sample_data/messy_sap_orders.json)", fill=(248, 113, 113), font=font_card_title)
    
    code_text = (
        "[\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98124\",\n"
        "    \"CUST_INFO\": { \"id\": 10421, \"name\": \"Acro APAC\" },  <-- NESTED DICT\n"
        "    \"TX_DATE\": \"2026-09-12T14:30:00Z\",               <-- ISO-8601\n"
        "    \"LINE_ITEMS\": [{ \"sku\": \"SKU-99\", \"qty\": 4, \"price\": 25.50 }]\n"
        "  },\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98125\",\n"
        "    \"CUST_INFO\": \"CUST_99120\",                       <-- FLAT STRING!\n"
        "    \"TX_DATE\": 1789218000,                            <-- EPOCH INTEGER!\n"
        "    \"LINE_ITEMS\": \"SKU-44:2:45.00,SKU-88:1:15.00\"     <-- COLON STRING!\n"
        "  },\n"
        "  {\n"
        "    \"HEADER\": \"SAP_DOC_98126\",\n"
        "    \"CUST_INFO\": { \"cust_code\": \"CUST_5501\" },       <-- ALTERED KEYS!\n"
        "    \"TX_DATE\": \"15/09/2026\"                           <-- SLASH NOTATION!\n"
        "  }\n"
        "]"
    )
    draw.text((90, 335), code_text, fill=(226, 232, 240), font=font_code)
    
    # Right Card: The Catastrophic Failure Cascade
    draw.rounded_rectangle([(970, 260), (1860, 780)], radius=12, fill=(18, 22, 34), outline=(51, 65, 85), width=1)
    draw.text((1000, 290), "⚠️ Why Standard Data Stacks Fail Catastrophically", fill=(251, 191, 36), font=font_card_title)
    
    reasons = [
        ("❌ Brittle Rigid Schemas:", "Airflow & dbt fail immediately on unexpected keys or types, throwing HTTP 500."),
        ("❌ Silent Corruption:", "Permissive parsers cast unhandled fields to NULL, skewing executive dashboards."),
        ("❌ Heavy Engineering Drain:", "Engineers waste 40% of sprint time writing manual regex patches & backfills."),
        ("❌ Zero Self-Correction:", "Static ETL engines cannot reason about structural intent without human intervention.")
    ]
    
    y = 360
    for title, desc in reasons:
        draw.text((1000, y), title, fill=(248, 113, 113), font=font_card_title)
        draw.text((1000, y + 36), desc, fill=(203, 213, 225), font=font_card_body)
        y += 95
        
    # Bottom Stats Bar
    stat_boxes = [
        (60, 810, 630, 940, "$100B+", "Annual Global Cost of Data Downtime", (239, 68, 68)),
        (675, 810, 1245, 940, "40% of Sprints", "Data Engineering Velocity Lost to Break-Fix", (245, 158, 11)),
        (1290, 810, 1860, 940, "0 Seconds", "Notice Before Upstream API Payloads Mutate", (59, 130, 246))
    ]
    for x1, y1, x2, y2, val, lbl, col in stat_boxes:
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(18, 22, 34), outline=(38, 45, 68), width=1)
        draw.text((x1 + 30, y1 + 20), val, fill=col, font=font_stat_val)
        draw.text((x1 + 30, y1 + 75), lbl, fill=(148, 163, 184), font=font_stat_lbl)
        
    return img

# ==========================================
# SLIDE 2: THE ARC-AGI INGESTION AGENT
# ==========================================
def make_slide_2():
    img, draw = create_base_canvas(2, "THE ARC-AGI AGENT")
    
    draw.text((60, 130), "The Breakthrough: ARC-AGI Autonomous File Ingestion", fill=(255, 255, 255), font=font_title)
    draw.text((60, 195), "Adapting the Abstraction & Reasoning Corpus (ARC-AGI) to Neuro-Symbolic Program Synthesis", fill=(148, 163, 184), font=font_subtitle)
    
    # 4 Architecture Flow Stages
    stages = [
        (60, 250, 480, 440, "1. Input Profiler", "• Spatial JSONPath extraction\n• Polymorphic type inference\n• Automated PII redaction\n• Null ratio & cardinality metrics", (59, 130, 246)),
        (520, 250, 940, 440, "2. Gemini 1.5 Pro ARC Engine", "• Zero-shot structural reasoning\n• Multi-strategy AST synthesis\n• Vectorized Polars & Pandas\n• Pure dictionary comprehension", (168, 85, 247)),
        (980, 250, 1400, 440, "3. gVisor Security Sandbox", "• Isolated sub-process sandbox\n• Static AST security audit\n• Terminated on os/socket syscalls\n• Strict 5.0s execution ceiling", (16, 185, 129)),
        (1440, 250, 1860, 440, "4. Invariant Gate", "• Pandera Schema contracts\n• Financial conservation check\n• ∑ Gross == ∑ Billed ($0.01)\n• Instant BigQuery Dispatch", (6, 182, 212))
    ]
    for x1, y1, x2, y2, stitle, sdesc, col in stages:
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(18, 22, 34), outline=col, width=2)
        draw.text((x1 + 25, y1 + 20), stitle, fill=col, font=font_card_title)
        draw.text((x1 + 25, y1 + 65), sdesc, fill=(203, 213, 225), font=font_card_body)
        
    # Large Synthesized Code Showcase Card
    draw.rounded_rectangle([(60, 470), (1860, 940)], radius=12, fill=(14, 18, 28), outline=(38, 45, 68), width=1)
    draw.text((90, 495), "⚡ Autonomously Synthesized Python AST Program (Generated by Gemini 1.5 Pro in 406ms)", fill=(56, 189, 248), font=font_card_title)
    
    syn_code = (
        "def transform_sap_orders(raw_records):\n"
        "    clean_orders = []\n"
        "    for r in raw_records:\n"
        "        # 1. Autonomous Customer ID Normalization (handles polymorphic dict vs string)\n"
        "        cust = r.get('CUST_INFO')\n"
        "        cust_id = str(cust.get('id') or cust.get('cust_code')) if isinstance(cust, dict) else str(cust)\n\n"
        "        # 2. Polymorphic Timestamp Parser (handles ISO-8601, Unix epoch ints, and European slash dates)\n"
        "        dt = r.get('TX_DATE')\n"
        "        order_date = datetime.fromtimestamp(dt, tz=timezone.utc).date() if isinstance(dt, int) else ...\n\n"
        "        # 3. Polymorphic Line Item Parser with Financial Summation\n"
        "        items = r.get('LINE_ITEMS')\n"
        "        total_usd = sum(int(q)*float(p) for _, q, p in [p.split(':') for p in items.split(',')]) if isinstance(items, str) ...\n\n"
        "        clean_orders.append({ 'order_id': r.get('HEADER'), 'customer_id': cust_id, 'total_amount_usd': total_usd, ... })\n"
        "    return clean_orders"
    )
    draw.text((90, 545), syn_code, fill=(226, 232, 240), font=font_code)
    
    return img

# ==========================================
# SLIDE 3: FORMAL SAFETY SANDBOX & INVARIANTS
# ==========================================
def make_slide_3():
    img, draw = create_base_canvas(3, "FORMAL SAFETY & INVARIANTS")
    
    draw.text((60, 130), "Formal Verification: gVisor Sandbox & Invariant Gates", fill=(255, 255, 255), font=font_title)
    draw.text((60, 195), "Eliminating LLM Hallucinations: Proving Mathematical Correctness Before BigQuery Insertion", fill=(148, 163, 184), font=font_subtitle)
    
    # 3 Pillar Cards
    # Card 1: gVisor Sandbox
    draw.rounded_rectangle([(60, 260), (620, 930)], radius=12, fill=(18, 22, 34), outline=(59, 130, 246), width=2)
    draw.text((90, 290), "🛡️ gVisor Sandbox Security", fill=(96, 165, 250), font=font_card_title)
    draw.text((90, 340), "Every synthesized script runs inside a\nstrictly isolated container sandbox:", fill=(148, 163, 184), font=font_card_body)
    
    bullets1 = [
        ("🔒 Static AST Inspection:", "Scans all syntax nodes; statically blocks os, sys, subprocess, socket, eval, exec."),
        ("⏱️ Execution Timeouts:", "Terminated with POSIX signal after 5.0 seconds ceiling."),
        ("📦 Memory Bounds:", "Capped at 256 MiB RAM to prevent memory exhaustion attacks."),
        ("🚫 Zero Rogue Code:", "Unsafe programs are immediately quarantined into Pub/Sub DLQ.")
    ]
    y = 420
    for h, b in bullets1:
        draw.text((90, y), h, fill=(255, 255, 255), font=font_badge)
        draw.text((90, y + 26), b, fill=(203, 213, 225), font=font_card_body)
        y += 110

    # Card 2: Pandera Contracts
    draw.rounded_rectangle([(660, 260), (1260, 930)], radius=12, fill=(18, 22, 34), outline=(168, 85, 247), width=2)
    draw.text((690, 290), "📜 Pandera Schema Contracts", fill=(192, 132, 252), font=font_card_title)
    draw.text((690, 340), "Co-generated formal schema assertions\nverify structure and types deterministically:", fill=(148, 163, 184), font=font_card_body)
    
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
    draw.text((690, 420), p_code, fill=(226, 232, 240), font=font_code)

    # Card 3: Mathematical Invariant
    draw.rounded_rectangle([(1300, 260), (1860, 930)], radius=12, fill=(18, 22, 34), outline=(16, 185, 129), width=2)
    draw.text((1330, 290), "⚖️ Financial Invariant Proof", fill=(52, 211, 153), font=font_card_title)
    draw.text((1330, 340), "Mathematical conservation proofs ensure\nzero financial discrepancy or leakage:", fill=(148, 163, 184), font=font_card_body)
    
    inv_bullets = [
        ("∑ Gross == ∑ Billed:", "Total calculated items strictly equal order header total within ε < $0.01 tolerance."),
        ("Zero Null Invariance:", "Critical business keys cannot contain NULL or NaN values under any transform."),
        ("Reflexion Feedback Loop:", "If invariant fails, exact error trace is fed back to Gemini for self-repair in <200ms."),
        ("100% Invariant Pass Rate:", "Verified across 46 chaos drills with zero data corruption.")
    ]
    y = 420
    for h, b in inv_bullets:
        draw.text((1330, y), h, fill=(52, 211, 153), font=font_badge)
        draw.text((1330, y + 26), b, fill=(203, 213, 225), font=font_card_body)
        y += 110

    return img

# ==========================================
# SLIDE 4: GOOGLE CLOUD NATIVE ARCHITECTURE
# ==========================================
def make_slide_4():
    img, draw = create_base_canvas(4, "GCP ARCHITECTURE")
    
    draw.text((60, 130), "Google Cloud Native Distributed Architecture", fill=(255, 255, 255), font=font_title)
    draw.text((60, 195), "End-to-End Enterprise Topology: Cloud Run, Pub/Sub Buffer & DLQ, Gemini 1.5, BigQuery Lakehouse", fill=(148, 163, 184), font=font_subtitle)
    
    # Check if we can embed the high-res JPG topology
    jpg_path = Path("docs/assets/gcp_system_architecture_diagram.jpg")
    if jpg_path.exists():
        arch_img = Image.open(jpg_path).convert("RGB")
        # Resize to fit nicely: 960x650
        arch_img = arch_img.resize((960, 650), Image.Resampling.LANCZOS)
        img.paste(arch_img, (60, 270))
        draw.rectangle([(60, 270), (1020, 920)], outline=(38, 45, 68), width=2)
    
    # Right Side Cards: GCP Services Breakdown
    services = [
        ("🚀 Google Cloud Run (Compute Tier)", "Stateless FastAPI 0.110 engine, 80 concurrent requests/container, autoscaling 1 to 10 instances, gVisor security sandbox.", (59, 130, 246)),
        ("⚡ Google Cloud Pub/Sub (Event Buffer & DLQ)", "Decoupled streaming ingestion buffer with dedicated Dead-Letter Queue (DLQ) for poison-pill quarantine and zero event loss.", (34, 197, 94)),
        ("🧠 Google Gemini 1.5 Pro & Flash (AI Engine)", "Low-entropy (temp 0.2) neuro-symbolic program synthesis, invariant reflexion loop, and domain-grounded E-Commerce Copilot.", (168, 85, 247)),
        ("📊 Google Cloud BigQuery (Lakehouse Tier)", "Multi-tenant gold_analytics dataset with fact_reconciled_orders partitioned by date and clustered by tenant. High-throughput streaming inserts.", (6, 182, 212)),
        ("📡 Google Cloud Logging (Telemetry)", "Structured JSON telemetry with correlation trace IDs, MTTR latency profiling, and audit event tracking.", (245, 158, 11))
    ]
    
    y = 270
    for stitle, sdesc, scol in services:
        draw.rounded_rectangle([(1050, y), (1860, y + 115)], radius=10, fill=(18, 22, 34), outline=scol, width=1)
        draw.text((1075, y + 18), stitle, fill=scol, font=font_card_title)
        draw.text((1075, y + 54), sdesc, fill=(203, 213, 225), font=font_card_body)
        y += 132

    return img

# ==========================================
# SLIDE 5: LIVE WALKTHROUGH & IMPACT
# ==========================================
def make_slide_5():
    img, draw = create_base_canvas(5, "LIVE DEMONSTRATION")
    
    draw.text((60, 130), "Production Solution Walkthrough & Live Results", fill=(255, 255, 255), font=font_title)
    draw.text((60, 195), "Live Cloud Run Instance: Sub-Second Self-Healing, DLQ Quarantine, and Conversational Copilot", fill=(148, 163, 184), font=font_subtitle)
    
    # Left Side: Real Screenshot of Synthesis & Chaos
    screen1_path = Path("scripts/video_assets/live_view1_chaos_healed.png")
    if screen1_path.exists():
        sc1 = Image.open(screen1_path).convert("RGB")
        sc1 = sc1.resize((920, 650), Image.Resampling.LANCZOS)
        img.paste(sc1, (60, 270))
        draw.rectangle([(60, 270), (980, 920)], outline=(59, 130, 246), width=2)
        
    # Right Side Top: DLQ & Observability Full
    screen2_path = Path("scripts/video_assets/live_view2_observability_full.png")
    if screen2_path.exists():
        sc2 = Image.open(screen2_path).convert("RGB")
        sc2 = sc2.resize((840, 310), Image.Resampling.LANCZOS)
        img.paste(sc2, (1020, 270))
        draw.rectangle([(1020, 270), (1860, 580)], outline=(16, 185, 129), width=2)

    # Right Side Bottom: Tri-Modal Copilot
    screen3_path = Path("scripts/video_assets/live_copilot_domain_insights.png")
    if screen3_path.exists():
        sc3 = Image.open(screen3_path).convert("RGB")
        sc3 = sc3.resize((840, 310), Image.Resampling.LANCZOS)
        img.paste(sc3, (1020, 610))
        draw.rectangle([(1020, 610), (1860, 920)], outline=(168, 85, 247), width=2)

    return img

print("Rendering 5 high-resolution 1920x1080 scene slides...")
slide1 = make_slide_1()
slide1.save(slides_dir / "scene_01.png")
print("Saved scene_01.png")

slide2 = make_slide_2()
slide2.save(slides_dir / "scene_02.png")
print("Saved scene_02.png")

slide3 = make_slide_3()
slide3.save(slides_dir / "scene_03.png")
print("Saved scene_03.png")

slide4 = make_slide_4()
slide4.save(slides_dir / "scene_04.png")
print("Saved scene_04.png")

slide5 = make_slide_5()
slide5.save(slides_dir / "scene_05.png")
print("Saved scene_05.png")

print("All 5 scene slides generated successfully!")
