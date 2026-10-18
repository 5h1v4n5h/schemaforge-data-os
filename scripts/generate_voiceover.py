import os
import subprocess
from pathlib import Path
from gtts import gTTS
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {
        "id": "scene_01_problem",
        "title": "The $100B Crisis & Problem Statement",
        "text": (
            "Hello, I am Shivansh Sharma, presenting SchemaForge Data-OS for the Google Cloud AI and Innovation Cup 2026. "
            "Enterprises lose over 100 Billion dollars every single year to data downtime. "
            "Whenever an upstream SAP ERP, Stripe gateway, or CRM silently mutates a schema—renaming keys, altering date formats, or nesting payloads—"
            "traditional batch pipelines like Airflow and dbt crash instantly, halting analytical operations or corrupting the central data warehouse."
        )
    },
    {
        "id": "scene_02_arc_agi",
        "title": "The Breakthrough: ARC-AGI Ingestion Agent",
        "text": (
            "We solved this crisis with a breakthrough: the ARC-AGI Autonomous File Ingestion Agent. "
            "Drawing inspiration from the Abstraction and Reasoning Corpus benchmark, our agent ingests arbitrary, messy, polymorphic files without brittle regex or pre-programmed templates. "
            "Powered by Google Gemini 1.5 Pro, it profiles spatial JSONPaths, infers polymorphic type distributions, and autonomously synthesizes pure Python AST transformation programs on the fly."
        )
    },
    {
        "id": "scene_03_sandbox_invariants",
        "title": "Formal Safety Sandbox & Mathematical Invariants",
        "text": (
            "Crucially, we never deploy unverified LLM code into production. "
            "Every synthesized hypothesis executes inside an isolated gVisor container sandbox and is verified against strict Pandera schema contracts and formal mathematical invariants. "
            "This mathematically guarantees that the sum of gross line items strictly equals billed revenue, with non-null primary keys and zero data loss."
        )
    },
    {
        "id": "scene_04_gcp_architecture",
        "title": "Google Cloud Native Architecture",
        "text": (
            "SchemaForge is engineered natively on Google Cloud. "
            "Our stateless core runs on Google Cloud Run with autoscaling and gVisor isolation. "
            "High-throughput event streams buffer through Google Cloud Pub/Sub, while unrecoverable poison-pills quarantine into a Dead-Letter Queue. "
            "Clean, verified records stream directly into Google Cloud BigQuery in under 406 milliseconds."
        )
    },
    {
        "id": "scene_05_live_walkthrough",
        "title": "Live Solution Walkthrough & Impact",
        "text": (
            "Here on our live Cloud Run deployment, our Synthesis and Chaos dashboard demonstrates sub-second self-healing with a 100% Data Quality Score across thousands of real enterprise records. "
            "And with our built-in E-Commerce Copilot, business leaders can converse with live warehouse analytics, generating instant Vega-Lite charts. "
            "SchemaForge transforms fragile data pipelines into a resilient, autonomous Data-OS."
        )
    }
]

output_dir = Path("scripts/audio_scenes")
output_dir.mkdir(parents=True, exist_ok=True)

print("Synthesizing audio scenes matching Shivansh's voice profile...")

for sc in scenes:
    mp3_raw = output_dir / f"{sc['id']}_raw.mp3"
    wav_final = output_dir / f"{sc['id']}.wav"
    
    # 1. Synthesize Indian English using gTTS
    tts = gTTS(text=sc["text"], lang="en", tld="co.in", slow=False)
    tts.save(str(mp3_raw))
    
    # 2. Process with ffmpeg: fine-tune pitch ~0.94x to match Shivansh's measured 242Hz, add warm vocal EQ & dynamic compressor
    # asetrate adjusts pitch/speed, aresample restores standard 44.1kHz, atempo fine-tunes cadence, equalizer boosts 240Hz warmth
    audio_filter = (
        "asetrate=44100*0.93,aresample=44100,atempo=1.06,"
        "equalizer=f=240:width_type=h:width=120:g=2.5,"
        "equalizer=f=3500:width_type=h:width=1000:g=1.5,"
        "compand=attacks=0.02:decays=0.2:points=-80/-80|-20/-16|0/-8:soft-knee=6"
    )
    
    cmd = [
        ffmpeg_exe, "-y",
        "-i", str(mp3_raw),
        "-af", audio_filter,
        "-ar", "44100",
        "-ac", "2",
        str(wav_final)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # Measure duration
    dur_cmd = [
        ffmpeg_exe, "-i", str(wav_final)
    ]
    res = subprocess.run(dur_cmd, capture_output=True, text=True)
    dur_line = [l for l in res.stderr.splitlines() if "Duration:" in l]
    print(f"[{sc['id']}] Generated: {wav_final.name} -> {dur_line[0] if dur_line else 'done'}")

print("\nAll audio scenes synthesized successfully!")
