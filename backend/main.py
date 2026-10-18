"""
SchemaForge Data-OS — Main Application Entry Point.
Stateless, production-hardened FastAPI application with clean layered architecture.
"""
import os
import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.infrastructure.config import settings
from backend.infrastructure.logging import logger

# Import Modular Presentation Layer Routers
from backend.api.routers.health import router as health_router
from backend.api.routers.synthesis import router as synthesis_router
from backend.api.routers.connectors import router as connectors_router
from backend.api.routers.observability import router as observability_router
from backend.api.routers.copilot import router as copilot_router
from backend.api.routers.telemetry import router as telemetry_router

app = FastAPI(
    title=settings.app_name,
    description="Autonomous Neuro-Symbolic Program Synthesis & Data Ingestion Platform on Google Cloud",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cross-Origin Resource Sharing (CORS) Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Telemetry & Request Timing Middleware
@app.middleware("http")
async def add_process_time_and_logging(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    
    # Log requests (excluding high-frequency health probes)
    if not request.url.path.startswith("/health"):
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} in {duration_ms}ms",
            extra={"component": "http_middleware", "duration_ms": duration_ms}
        )
    return response

# Global Error Boundary Middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}",
        exc_info=True,
        extra={"component": "error_boundary"}
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unhandled exception occurred in the SchemaForge backend.",
            "detail": str(exc),
            "path": request.url.path,
            "region": settings.gcp_region
        }
    )

# Register Modular Feature Routers
app.include_router(health_router)
app.include_router(synthesis_router)
app.include_router(connectors_router)
app.include_router(observability_router)
app.include_router(copilot_router)
app.include_router(telemetry_router)

# Mount Static Frontend
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
