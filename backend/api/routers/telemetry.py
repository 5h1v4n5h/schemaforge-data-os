"""
API Layer: Multi-Tenant Telemetry & Chaos Drill Router.
"""
from fastapi import APIRouter, HTTPException

from backend.api.schemas.chaos import ChaosDrillRequest
from backend.api.schemas.telemetry import SimulatorPulseRequest, DlqReplayRequest
from backend.application.chaos_service import chaos_service
from backend.application.dlq_service import dlq_service
from backend.core.multitenant import MultiTenantEngine

router = APIRouter(prefix="/api/v1", tags=["Multi-Tenant Telemetry & Chaos"])

@router.get("/tenants")
def get_all_tenants():
    """Returns the 15 simulated enterprise tenants with active pipeline stats."""
    return {"tenants": MultiTenantEngine.list_tenants()}

@router.get("/telemetry/live")
def get_live_telemetry(tenant_id: str = "t_nexus_fintech"):
    """Returns dynamic, high-precision operational metrics bound to real database records."""
    return MultiTenantEngine.get_tenant_telemetry(tenant_id)

@router.post("/simulator/pulse")
def trigger_simulator_pulse(req: SimulatorPulseRequest):
    """
    Continuous Traffic Daemon: Ingests realistic streaming micro-batches,
    simulates drift/anomalies, and produces real BigQuery Job IDs.
    """
    return MultiTenantEngine.pulse_continuous_traffic(req.tenant_id, req.count)

@router.post("/chaos/run-scenario")
def run_chaos_scenario(req: ChaosDrillRequest):
    """
    Triggers live verification chaos scenarios on-demand:
    - scenario_a: Schema Drift & Self-Healing
    - scenario_b: Neuro-Symbolic Edge Cases
    - scenario_c: High-Concurrency Burst & DLQ Recovery
    - scenario_d: Multi-Tenant Cryptographic Isolation
    """
    try:
        return chaos_service.execute_drill(
            scenario=req.scenario,
            tenant_id=req.tenant_id,
            event_count=req.event_count or 1000
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dlq/auto-diagnose-replay")
def auto_diagnose_and_replay_dlq(req: DlqReplayRequest):
    """Auto-diagnoses quarantined records, synthesizes Pandera repair rules, and redrives queue."""
    return dlq_service.redrive_quarantined_records(req.tenant_id)
