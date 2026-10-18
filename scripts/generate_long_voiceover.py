import os
import subprocess
from pathlib import Path
import imageio_ffmpeg
import soundfile as sf

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {
        "id": "scene_01_problem",
        "title": "The $100B Enterprise Data Downtime Crisis",
        "tag": "PROBLEM STATEMENT",
        "text": (
            "Hello, and welcome. In modern enterprise software, data is the lifeblood of every analytical report, "
            "machine learning model, and executive decision. However, organizations worldwide face a catastrophic silent crisis: "
            "over 100 Billion dollars is lost annually to data downtime and broken ingestion pipelines. "
            "In real-world operations, systems like SAP ERP, Salesforce, Stripe, and customer support portals constantly update. "
            "When an upstream engineering team deploys an update that mutates a schema—such as altering nested billing dictionaries, "
            "switching dates to Unix epoch integers, or converting structured line items into delimited strings—"
            "traditional data tools like Apache Airflow, dbt, Spark Streaming, and Fivetran crash immediately. "
            "This leads to pipeline outages, emergency middle-of-the-night engineering alerts, and silent data corruption "
            "where missing or null values pollute the data warehouse, distorting critical business metrics."
        )
    },
    {
        "id": "scene_02_track_justification",
        "title": "Competition Track Justification & Strategic Fit",
        "tag": "TRACK JUSTIFICATION",
        "text": (
            "To understand our architectural choices, we must examine why we chose this specific competition track. "
            "Many artificial intelligence projects focus on superficial LLM wrappers—building simple chatbots that generate unverified SQL "
            "or summarize text. However, in enterprise environments, generative AI without resilient data infrastructure is fundamentally useless. "
            "If the ingestion layer breaks, downstream analytics and artificial intelligence engines fail instantly. "
            "We chose the autonomous infrastructure track because enterprise data engineering requires a foundational breakthrough. "
            "SchemaForge Data-OS sits directly at the ingestion boundary, replacing fragile manual data plumbing "
            "with an autonomous, self-healing operating system. "
            "By choosing Google Cloud Platform—specifically combining Cloud Run, Pub/Sub, Gemini 1.5, and BigQuery—"
            "we provide a serverless, zero-maintenance architecture that guarantees continuous data availability for modern enterprises."
        )
    },
    {
        "id": "scene_03_arc_agi",
        "title": "The Novel Approach: ARC-AGI Ingestion Agent",
        "tag": "THE ARC-AGI AGENT",
        "text": (
            "Now let us explore our core innovation: the ARC-AGI Autonomous File Ingestion Agent. "
            "Our breakthrough adapts the Abstraction and Reasoning Corpus, known as ARC-AGI, pioneered by AI researcher François Chollet. "
            "Traditional pipelines depend on strict, pre-programmed rules. When an unexpected format appears, static rules fail. "
            "In contrast, the ARC-AGI paradigm treats data ingestion as an autonomous reasoning problem. "
            "When an unlabelled, dirty file arrives—such as raw SAP exports containing mixed dictionaries, timestamps, and unstructured strings—"
            "our agent first constructs a spatial JSONPath profile, detecting polymorphic type variance across records. "
            "Instead of relying on fragile regex or stochastic LLM text rewriting, our agent performs neuro-symbolic program synthesis. "
            "It generates abstract transformation hypotheses in pure Python, complete with formal Pandera schema contracts. "
            "This enables our agent to generalize across unseen schemas without pre-programmed templates or manual intervention."
        )
    },
    {
        "id": "scene_04_gemini_utilization",
        "title": "Deep Google Gemini 1.5 Neuro-Symbolic Integration",
        "tag": "GOOGLE GEMINI ENGINE",
        "text": (
            "Google Gemini is the cognitive backbone of SchemaForge Data-OS, deployed in a dual-model architecture. "
            "For program synthesis, we utilize Google Gemini 1.5 Pro. We configure Gemini with low entropy—a temperature of 0.2—"
            "to ensure deterministic, mathematically rigorous code generation. "
            "Gemini receives the spatial input profile, target BigQuery schema contracts, and sample edge cases. "
            "It then generates multiple candidate transformation strategies: vectorized Polars normalizers, Pandas structural transformers, "
            "and lightweight dictionary comprehensions. "
            "Crucially, Gemini also generates formal Pandera schema validation rules to test its own code. "
            "Meanwhile, for conversational intelligence, we leverage Google Gemini 1.5 Flash. "
            "Gemini Flash powers our real-time E-Commerce Copilot, dynamically grounded in live BigQuery metadata, "
            "translating natural language questions into verified SQL queries and declarative Vega-Lite visualizations."
        )
    },
    {
        "id": "scene_05_formal_safety",
        "title": "Formal Safety Guarantees & gVisor Sandbox",
        "tag": "FORMAL SAFETY & SANDBOX",
        "text": (
            "In enterprise data engineering, relying solely on language model outputs is unacceptable due to hallucination risks. "
            "SchemaForge guarantees safety through deterministic formal verification and sandboxed execution. "
            "Every candidate program synthesized by Gemini must first pass a strict static AST security audit. "
            "Our AST parser blocks unauthorized system modules—including operating system calls, subprocesses, sockets, and dynamic code evaluation. "
            "Next, candidate programs execute inside a secure gVisor container sandbox, constrained by a 5-second timeout and 256 megabyte memory ceiling. "
            "Finally, the output must satisfy our mathematical invariant gate: cell-level mismatch tolerance must be strictly zero, "
            "primary keys must never be null, and financial conservation must hold: the sum of gross line items must strictly equal billed order revenue. "
            "If an invariant fails, an automated reflexion loop feeds the error trace back to Gemini for sub-second self-repair."
        )
    },
    {
        "id": "scene_06_gcp_architecture",
        "title": "Google Cloud Native Distributed Architecture",
        "tag": "GCP ARCHITECTURE",
        "text": (
            "Let us examine how SchemaForge Data-OS is architected on Google Cloud Platform. "
            "Our core compute engine is hosted on Google Cloud Run, running a containerized FastAPI backend. "
            "Cloud Run provides instant horizontal autoscaling from 1 to 10 instances with 80 concurrent connections per container, "
            "enabling high throughput with zero cold starts. "
            "Upstream event streams flow through Google Cloud Pub/Sub, providing at-least-once guaranteed delivery. "
            "If a truly corrupted or malicious poison-pill record is detected, our Pub/Sub Dead-Letter Queue isolates it into quarantine, "
            "preventing pipeline bottlenecks while alerting operators through Cloud Logging. "
            "Our analytical lakehouse is Google Cloud BigQuery, organized into multi-tenant golden datasets. "
            "Reconciled order facts and customer dimensions are partitioned by date and clustered by tenant for lightning-fast queries, "
            "delivering enterprise analytics at fraction-of-a-cent cloud costs."
        )
    },
    {
        "id": "scene_07_live_demonstration",
        "title": "Production Solution Walkthrough & Live Results",
        "tag": "LIVE DEMONSTRATION",
        "text": (
            "Here we see SchemaForge Data-OS operating live on our Google Cloud Run production deployment. "
            "Inside the Synthesis and Chaos console, operators can select an enterprise tenant and trigger live chaos drills. "
            "When we inject a catastrophic schema mutation into Pub/Sub, SchemaForge detects the drift, synthesizes a verified Python AST repair, "
            "and streams clean records into BigQuery in just 406.8 milliseconds—achieving a 100% Data Quality Score. "
            "In our Observability console, a 4-swimlane continuous DAG tracks real-time data freshness, completeness, and circuit breakers. "
            "And inside our E-Commerce Copilot, business leaders can converse with live warehouse analytics, "
            "receiving executive insights, verified BigQuery SQL, and interactive charts within seconds. "
            "SchemaForge Data-OS is deployed and accessible right now at schemaforge-app.run.app. "
            "Thank you for watching."
        )
    }
]

output_dir = Path("scripts/long_audio_scenes")
output_dir.mkdir(parents=True, exist_ok=True)

print("Synthesizing 7 extended audio scenes matching Shivansh's calm presentation cadence...")

total_duration = 0.0

for sc in scenes:
    raw_mp3 = output_dir / f"{sc['id']}_raw.mp3"
    final_wav = output_dir / f"{sc['id']}.wav"
    
    # 1. Synthesize with edge-tts using en-IN-PrabhatNeural, rate=-14% (calm, ~105 WPM), pitch=-8Hz (deep vocal resonance)
    cmd = [
        "edge-tts",
        "--voice", "en-IN-PrabhatNeural",
        "--rate=-14%",
        "--pitch=-8Hz",
        f"--text={sc['text']}",
        f"--write-media={str(raw_mp3)}"
    ]
    subprocess.run(cmd, check=True)
    
    # 2. Master audio with FFmpeg: warm vocal EQ (240Hz warmth boost, 3kHz clarity), soft-knee dynamic compressor
    audio_filter = (
        "equalizer=f=240:width_type=h:width=120:g=2.5,"
        "equalizer=f=3200:width_type=h:width=800:g=1.8,"
        "compand=attacks=0.03:decays=0.25:points=-80/-80|-20/-16|0/-8:soft-knee=6"
    )
    
    master_cmd = [
        ffmpeg_exe, "-y",
        "-i", str(raw_mp3),
        "-af", audio_filter,
        "-ar", "44100",
        "-ac", "2",
        str(final_wav)
    ]
    subprocess.run(master_cmd, check=True, capture_output=True)
    
    # Measure duration
    info = sf.info(str(final_wav))
    total_duration += info.duration
    print(f"[{sc['id']}] Generated: {final_wav.name} -> Duration: {info.duration:.2f}s ({info.duration/60:.2f} min)")

print(f"\nAll 7 scenes synthesized successfully! Total Narration Runtime: {total_duration:.2f}s ({total_duration/60:.2f} minutes)!")
