"""
API Layer: Pydantic v2 Schemas for Telemetry & Simulator Endpoints.
"""
from pydantic import BaseModel, Field

class SimulatorPulseRequest(BaseModel):
    tenant_id: str = Field(default="t_nexus_fintech", description="Target workspace tenant identifier")
    count: int = Field(default=15, ge=1, le=1000, description="Micro-batch event burst count")

class DlqReplayRequest(BaseModel):
    tenant_id: str = Field(default="t_nexus_fintech", description="Target workspace tenant identifier")
