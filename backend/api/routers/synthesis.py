"""
API Layer: Synthesis Router.
Handles single-source and multi-source neuro-symbolic program synthesis.
"""
from fastapi import APIRouter, Body
from typing import Dict, Any

from backend.api.schemas.synthesis import ProfileRequest, SynthesizeRequest, MultiSourceSynthesizeRequest
from backend.application.synthesis_service import synthesis_service
from backend.application.multi_source_service import multi_source_service

router = APIRouter(prefix="/api", tags=["Neuro-Symbolic Synthesis"])

@router.post("/profile")
def run_profiler(req: ProfileRequest):
    """Stage 1: Profiles raw inputs and returns compact contextual schema constraints."""
    return synthesis_service.profile_input(req.raw_input_data, req.target_ddl)

@router.post("/synthesize")
def run_synthesis_loop(req: SynthesizeRequest):
    """Executes the full 6-Stage Neuro-Symbolic State Machine for single-source transformations."""
    return synthesis_service.execute_synthesis(
        raw_input_data=req.raw_input_data,
        target_ddl=req.target_ddl,
        target_table_name=req.target_table_name or "gold_analytics.fact_orders"
    )

@router.post("/synthesize/multi-source")
def run_multi_source_synthesis(req: MultiSourceSynthesizeRequest):
    """Executes the 6-Stage State Machine across Multi-Source Enterprise Payloads."""
    return multi_source_service.execute_multi_source_synthesis(
        sources=req.sources,
        target_ddl=req.target_ddl,
        target_table_name=req.target_table_name or "gold_analytics.fact_reconciled_orders"
    )
