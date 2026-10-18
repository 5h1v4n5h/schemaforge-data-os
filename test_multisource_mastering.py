import sys
import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_multi_source_mastering():
    client = TestClient(app)

    # 1. Load the 3 heterogeneous sample sources
    p1 = Path("sample_data/source1_thelook_orders.json")
    p2 = Path("sample_data/source2_stripe_charges.json")
    p3 = Path("sample_data/source3_crm_tickets.json")
    p_ddl = Path("sample_data/target_gold_master.sql")

    assert p1.exists() and p2.exists() and p3.exists() and p_ddl.exists()

    thelook_data = json.loads(p1.read_text(encoding="utf-8"))
    stripe_data = json.loads(p2.read_text(encoding="utf-8"))
    crm_data = json.loads(p3.read_text(encoding="utf-8"))
    target_ddl = p_ddl.read_text(encoding="utf-8")

    payload = {
        "sources": {
            "thelook_orders": thelook_data,
            "stripe_charges": stripe_data,
            "crm_tickets": crm_data
        },
        "target_ddl": target_ddl,
        "target_table_name": "gold_analytics.fact_reconciled_orders"
    }

    print("\n" + "=" * 75)
    print("TESTING SCHEMAFORGE MULTI-SOURCE MASTERING & RECONCILIATION PIPELINE")
    print("=" * 75)

    response = client.post("/api/synthesize/multi-source", json=payload)
    assert response.status_code == 200, f"API error: {response.text}"

    data = response.json()
    assert data["status"] == "SUCCESS", f"Pipeline failed: {data}"

    print(f"\n>>> Total Pipeline Latency: {data['total_latency_ms']} ms")
    print("\n--- 6-Stage Neuro-Symbolic State Machine Execution ---")
    for step in data["state_machine_timeline"]:
        print(f"Stage {step['stage']}: {step['name']:<40} [{step['status']}] ({step['duration_ms']} ms)")
        print(f"  └─ {step['details']}")

    # Inspect detected cross-links
    print("\n--- Cross-Source Entity Linkages Detected ---")
    for link in data.get("detected_cross_links", []):
        print(f"  • {link['source_a']} <-> {link['source_b']} via {link['link_type']}")

    verified = data["verified_solution"]
    assert verified is not None

    print(f"\n>>> Data Quality Score: {verified['data_quality_score'] * 100}%")
    print(f">>> Financial Reconciliation Status: {verified['reconciliation_passed']}")
    print(">>> Financial Summary:")
    for k, v in verified["financial_summary"].items():
        print(f"    - {k}: {v}")

    # Verify Golden Records
    master_customers = verified["dim_master_customer"]
    print(f"\n--- Master Golden Customer Dimension ({len(master_customers)} records) ---")
    for c in master_customers:
        print(f"  [ID: {c['master_customer_id']}] {c['legal_company_name']} | Contact: {c['primary_contact_name']} | Email: {c['primary_billing_email']} | Conf: {c['mastering_confidence_score'] * 100}%")

    assert len(master_customers) == 4
    for c in master_customers:
        assert c["master_customer_id"].startswith("MST_")
        assert "@" in c["primary_billing_email"]
        assert c["mastering_confidence_score"] >= 0.85

    # Verify Reconciled Orders
    reconciled_orders = verified["fact_reconciled_orders"]
    print(f"\n--- Reconciled Fact Orders ({len(reconciled_orders)} records) ---")
    for o in reconciled_orders:
        print(f"  [Order: {o['order_id']}] Gross: ${o['thelook_gross_amount_usd']} | Billed: ${o['stripe_charge_amount_usd']} | Net: ${o['net_realized_revenue_usd']} | Status: {o['reconciliation_status']} | SLA Breached: {o['delivery_sla_breached']}")
        assert o["reconciliation_status"] == "BALANCED"

    assert len(reconciled_orders) == 4

    print("\n" + "=" * 75)
    print(">>> ALL MULTI-SOURCE MASTERING & INVARIANT TESTS PASSED WITH 100% SUCCESS! <<<")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    test_multi_source_mastering()
