#!/usr/bin/env python3
"""
SchemaForge Production-Grade Multi-Tenant Seeding Engine
Generates 50,000+ realistic operational events across 15 enterprise tenants
spanning a 30-day historical window with realistic diurnal load curves,
authentic production anomalies, and BigQuery job execution lineage.
"""

import os
import sys
import json
import sqlite3
import random
import uuid
from datetime import datetime, timedelta, timezone

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.core.multitenant import DB_PATH, TENANT_CONFIGS

def init_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            vertical TEXT NOT NULL,
            tier TEXT NOT NULL,
            active_pipelines INTEGER NOT NULL DEFAULT 3,
            primary_table TEXT NOT NULL,
            dqs_score REAL DEFAULT 99.4,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS telemetry_events (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            status TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            payload_json TEXT NOT NULL,
            anomaly_type TEXT NOT NULL,
            FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
        );

        CREATE INDEX IF NOT EXISTS idx_telemetry_tenant_time ON telemetry_events(tenant_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_telemetry_status ON telemetry_events(status);

        CREATE TABLE IF NOT EXISTS pipeline_execution_logs (
            job_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            pipeline_name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration_ms REAL NOT NULL,
            rows_processed INTEGER NOT NULL,
            status TEXT NOT NULL,
            bigquery_job_id TEXT NOT NULL,
            schema_drift_detected INTEGER NOT NULL DEFAULT 0,
            auto_healed INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
        );

        CREATE INDEX IF NOT EXISTS idx_exec_tenant_time ON pipeline_execution_logs(tenant_id, start_time);

        CREATE TABLE IF NOT EXISTS dead_letter_queue (
            dlq_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            topic TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            error_reason TEXT NOT NULL,
            raw_payload TEXT NOT NULL,
            status TEXT NOT NULL,
            diagnosis TEXT,
            auto_replay_available INTEGER DEFAULT 1,
            FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
        );

        CREATE INDEX IF NOT EXISTS idx_dlq_tenant ON dead_letter_queue(tenant_id, status);
    """)
    conn.commit()

def seed_database(target_records_per_tenant: int = 3500):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_schema(conn)
    cur = conn.cursor()

    # Clear existing data for idempotent re-runs
    cur.execute("DELETE FROM dead_letter_queue")
    cur.execute("DELETE FROM pipeline_execution_logs")
    cur.execute("DELETE FROM telemetry_events")
    cur.execute("DELETE FROM tenants")

    now = datetime.now(timezone.utc)
    print(f"[*] Seeding 15 enterprise tenants into {DB_PATH}...")

    # 1. Insert Tenants
    for t in TENANT_CONFIGS:
        created_at = (now - timedelta(days=random.randint(60, 180))).isoformat()
        cur.execute("""
            INSERT INTO tenants (tenant_id, name, vertical, tier, active_pipelines, primary_table, dqs_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["id"], t["name"], t["vertical"], t["tier"],
            random.randint(3, 8), t["primary_table"], round(random.uniform(98.8, 100.0), 1), created_at
        ))

    conn.commit()

    total_events_seeded = 0
    total_dlq_seeded = 0
    total_logs_seeded = 0

    # 2. Seed 30-Day Historical Telemetry Events with Diurnal Waves
    for tenant_idx, t in enumerate(TENANT_CONFIGS, 1):
        tenant_id = t["id"]
        vertical = t["vertical"]
        print(f"  [{tenant_idx}/15] Generating {target_records_per_tenant} events for {t['name']} ({vertical})...")

        event_batch = []
        dlq_batch = []
        log_batch = []

        # Generate timestamps distributed across 30 days
        for i in range(target_records_per_tenant):
            # Pick a day in the last 30 days
            day_offset = random.uniform(0, 30)
            # Diurnal curve: peak between 14:00 - 18:00 UTC
            hour = int((random.triangular(0, 24, 15) + random.uniform(0, 2)) % 24)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            event_time = (now - timedelta(days=day_offset)).replace(hour=hour, minute=minute, second=second)
            event_iso = event_time.isoformat()
            evt_id = f"evt_{uuid.uuid4().hex[:10]}"

            # Anomaly injection logic (approx 8% overall anomaly rate)
            r_anom = random.random()
            if r_anom < 0.03: # 3% Renamed keys (Schema Drift)
                status = "HEALED"
                anomaly = "SCHEMA_DRIFT_RENAMED_KEYS"
                latency = random.uniform(140.0, 260.0)
                payload = {
                    "event_id": evt_id,
                    "tenant_id": tenant_id,
                    "client_uuid": f"uuid_{uuid.uuid4().hex[:8]}", # renamed from customer_id
                    "tx_hash": f"0x{uuid.uuid4().hex}",
                    "amount_cents": random.randint(1500, 85000),
                    "currency": "USD",
                    "origin_system": "v2_rest_api"
                }
            elif r_anom < 0.05: # 2% Type Mismatch
                status = "HEALED"
                anomaly = "TYPE_MISMATCH_STRING_FLOAT"
                latency = random.uniform(120.0, 210.0)
                payload = {
                    "event_id": evt_id,
                    "tenant_id": tenant_id,
                    "customer_id": f"CUST_{random.randint(1000, 9999)}",
                    "total_amount_usd": f"{round(random.uniform(20.0, 600.0), 2)}", # string instead of float
                    "items_count": str(random.randint(1, 10)),
                    "currency": "USD"
                }
            elif r_anom < 0.07: # 2% Split Currencies / Nested Mutations
                status = "HEALED"
                anomaly = "NESTED_CURRENCY_STRUCT"
                latency = random.uniform(150.0, 280.0)
                payload = {
                    "event_id": evt_id,
                    "tenant_id": tenant_id,
                    "customer_id": f"CUST_{random.randint(1000, 9999)}",
                    "pricing": {
                        "gross_amount": round(random.uniform(50.0, 900.0), 2),
                        "fee_deducted": 4.50,
                        "currency_iso": "USD"
                    }
                }
            elif r_anom < 0.075: # 0.5% Poison-Pill Quarantine
                status = "QUARANTINED"
                anomaly = "DESERIALIZATION_CORRUPTION"
                latency = random.uniform(310.0, 520.0)
                payload = {
                    "corrupt_byte_sequence": "\x00\xFF\xFE_MALFORMED",
                    "tenant_id": tenant_id,
                    "unparseable_raw": "{broken_json: missing_quotes}"
                }
                dlq_id = f"dlq_{uuid.uuid4().hex[:8]}"
                dlq_batch.append((
                    dlq_id, tenant_id, f"inbound.{vertical.lower()}.v1", event_iso,
                    "MalformedPayloadException: Unrecognized byte encoding in legacy stream",
                    json.dumps(payload), "QUARANTINED", "Awaiting Automated Pandera Rule Redrive", 1
                ))
            else: # Standard healthy record (92.5%)
                status = "SUCCESS"
                anomaly = "NONE"
                latency = random.uniform(45.0, 115.0)
                payload = {
                    "event_id": evt_id,
                    "tenant_id": tenant_id,
                    "customer_id": f"CUST_{random.randint(1000, 9999)}",
                    "amount_usd": round(random.uniform(10.0, 1200.0), 2),
                    "currency": "USD",
                    "order_status": "PROCESSED",
                    "timestamp": event_iso
                }

            event_batch.append((
                evt_id, tenant_id, event_iso, f"{vertical.upper()}_TX",
                status, round(latency, 2), json.dumps(payload), anomaly
            ))

        # 3. Create Daily Batch Execution Logs for this tenant (approx 60 jobs)
        for d in range(30):
            job_date = now - timedelta(days=d)
            for batch_num in range(2): # 2 batches per day
                job_time = job_date.replace(hour=8 + (batch_num * 8), minute=random.randint(0, 30))
                drift = random.random() < 0.20 # 20% of batches encountered and auto-healed drift
                bq_uuid = f"bqjob_r{uuid.uuid4().hex[:12]}_{int(job_time.timestamp())}"
                
                log_batch.append((
                    f"job_{uuid.uuid4().hex[:8]}",
                    tenant_id,
                    f"{t['primary_table']}_microbatch_sync",
                    job_time.isoformat(),
                    round(random.uniform(90.0, 220.0), 1),
                    random.randint(45, 95),
                    "COMPLETED",
                    bq_uuid,
                    1 if drift else 0,
                    1 if drift else 0
                ))

        cur.executemany("""
            INSERT INTO telemetry_events (event_id, tenant_id, timestamp, event_type, status, latency_ms, payload_json, anomaly_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, event_batch)

        if dlq_batch:
            cur.executemany("""
                INSERT INTO dead_letter_queue (dlq_id, tenant_id, topic, timestamp, error_reason, raw_payload, status, diagnosis, auto_replay_available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dlq_batch)

        cur.executemany("""
            INSERT INTO pipeline_execution_logs (job_id, tenant_id, pipeline_name, start_time, duration_ms, rows_processed, status, bigquery_job_id, schema_drift_detected, auto_healed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, log_batch)

        conn.commit()
        total_events_seeded += len(event_batch)
        total_dlq_seeded += len(dlq_batch)
        total_logs_seeded += len(log_batch)

    conn.close()
    print("\n" + "="*70)
    print("[SUCCESS] PRODUCTION-GRADE SEEDING COMPLETE!")
    print(f"[*] Total Operational Records Ingested : {total_events_seeded:,}")
    print(f"[*] Active Enterprise Tenants         : {len(TENANT_CONFIGS)}")
    print(f"[*] Historical Execution Logs Created : {total_logs_seeded:,}")
    print(f"[*] Quarantined DLQ Poison-Pills       : {total_dlq_seeded:,}")
    print(f"[*] Database Path                      : {DB_PATH}")
    print("="*70)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3500
    seed_database(target_records_per_tenant=count)
