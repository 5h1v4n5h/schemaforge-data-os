"""
API Layer: Health & Readiness Probes.
Provides Kubernetes & Cloud Run standard liveness and readiness probes.
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from backend.infrastructure.config import settings
from backend.infrastructure.gcp_clients import gcp_client_factory

router = APIRouter(tags=["Health & Probes"])

@router.get("/health/live")
def liveness_probe():
    """Liveness probe: returns 200 immediately if process and event loop are responsive."""
    return {
        "status": "ALIVE",
        "service": settings.app_name,
        "version": settings.version,
        "region": settings.gcp_region
    }

@router.get("/health/ready")
def readiness_probe():
    """Readiness probe: verifies external dependencies (BigQuery, Pub/Sub, DB pool)."""
    checks = gcp_client_factory.is_healthy()
    all_ready = all(checks.values())
    
    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "READY" if all_ready else "NOT_READY",
            "dependencies": checks,
            "project_id": settings.gcp_project_id,
            "region": settings.gcp_region
        }
    )

@router.get("/health")
def legacy_health():
    """Backward-compatible health endpoint."""
    return {
        "status": "HEALTHY",
        "system": settings.app_name,
        "google_cloud_region": settings.gcp_region
    }
