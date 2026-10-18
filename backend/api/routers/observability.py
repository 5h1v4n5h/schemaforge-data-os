"""
API Layer: Ingestion Observability Router.
Provides DAG topology, decoupled DQS matrix, and DLQ quarantine status.
"""
from fastapi import APIRouter
from backend.core.observability import ObservabilityEngine

router = APIRouter(prefix="/api/observability", tags=["Ingestion Observability"])

@router.get("/dag")
def get_topology_dag():
    """Returns the 4-swimlane DAG topology with circuit breakers and stream telemetry."""
    return ObservabilityEngine.get_topology_dag()

@router.get("/dqs")
def get_dqs_scorecard():
    """Returns decoupled Data Quality Scorecard (DQS = wC*SC + wV*SV + wU*SU + wInc*SInc)."""
    return ObservabilityEngine.get_dqs_scorecard()

@router.get("/dlq")
def get_dlq_workbench():
    """Returns Dead-Letter Queue (DLQ) quarantine state and remediation status."""
    return ObservabilityEngine.get_dlq_workbench()
