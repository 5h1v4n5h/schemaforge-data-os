"""
Test Suite: Clean Architecture & Production Resilience Verification.
Verifies domain models, use-case services, health probes, and API router contracts.
"""
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.domain.entities import ReconciledOrderEntity, DqsScorecardEntity
from backend.domain.exceptions import SchemaDriftException, InvariantViolationException
from backend.infrastructure.config import settings
from backend.infrastructure.gcp_clients import gcp_client_factory

client = TestClient(app)

def test_domain_reconciled_order_invariants():
    """Verifies pure domain entity financial conservation invariant logic."""
    from datetime import datetime, timezone
    order = ReconciledOrderEntity(
        order_id="ORD-TEST-01",
        master_customer_id="MST_CUST_TEST",
        thelook_gross_amount_usd=500.0,
        stripe_charge_amount_usd=500.0,
        stripe_fee_amount_usd=14.50,
        net_realized_revenue_usd=485.50,
        payment_brand="visa",
        reconciliation_status="BALANCED",
        delivery_sla_breached=False,
        order_date=datetime.now(timezone.utc)
    )
    assert order.verify_financial_conservation() is True
    
    # Tamper with net amount
    order.net_realized_revenue_usd = 400.0
    assert order.verify_financial_conservation() is False

def test_domain_dqs_scorecard_calculation():
    """Verifies DQS formula: 0.30*C + 0.30*V + 0.20*U + 0.20*Inc."""
    dqs = DqsScorecardEntity(completeness=1.0, validity=1.0, uniqueness=1.0, incident_resilience=1.0)
    assert dqs.composite_score == 100.0
    
    dqs_degraded = DqsScorecardEntity(completeness=0.8, validity=1.0, uniqueness=1.0, incident_resilience=1.0)
    assert dqs_degraded.composite_score == 94.0

def test_health_probes():
    """Verifies /health/live, /health/ready, and /health."""
    # Liveness probe
    res_live = client.get("/health/live")
    assert res_live.status_code == 200
    assert res_live.json()["status"] == "ALIVE"
    
    # Readiness probe
    res_ready = client.get("/health/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "READY"
    
    # Legacy health
    res_legacy = client.get("/health")
    assert res_legacy.status_code == 200
    assert res_legacy.json()["status"] == "HEALTHY"

def test_api_profile_endpoint():
    """Verifies /api/profile with Pydantic v2 validation."""
    payload = {
        "raw_input_data": '[{"order_id": "ORD-1", "amount": 100.0}]',
        "target_ddl": "CREATE TABLE test (order_id STRING, amount FLOAT64);"
    }
    res = client.post("/api/profile", json=payload)
    assert res.status_code == 200
    assert "input_profile" in res.json()

def test_api_telemetry_live():
    """Verifies /api/v1/telemetry/live returns grounded metrics."""
    res = client.get("/api/v1/telemetry/live?tenant_id=t_nexus_fintech")
    assert res.status_code == 200
    data = res.json()
    assert data["tenant_id"] == "t_nexus_fintech"
    assert data["total_rows_processed"] >= 3500

def test_api_copilot_query():
    """Verifies /api/copilot/query conversational endpoint."""
    res = client.post("/api/copilot/query", json={"query": "What is the fee variance between Amex and Visa?"})
    assert res.status_code == 200
    data = res.json()
    assert "conversational_reply" in data
    assert "layer_1_executive_narrative" in data
    assert "layer_2_vega_lite_spec" in data
    assert "layer_3_code_disclosure" in data

def test_api_chaos_drill_endpoint():
    """Verifies /api/v1/chaos/run-scenario executes drill safely."""
    res = client.post("/api/v1/chaos/run-scenario", json={"scenario": "scenario_a", "tenant_id": "t_nexus_fintech"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PASSED_100_PERCENT"
    assert len(data["verified_clean_rows"]) == 2
