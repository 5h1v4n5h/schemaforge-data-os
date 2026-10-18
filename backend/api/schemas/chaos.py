"""
API Layer: Pydantic v2 Schemas for Chaos & Observability Endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional

class ChaosDrillRequest(BaseModel):
    scenario: str = Field(default="scenario_a", description="Scenario identifier: scenario_a, scenario_b, scenario_c, scenario_d")
    tenant_id: str = Field(default="t_nexus_fintech", description="Enterprise tenant workspace ID")
    event_count: Optional[int] = Field(default=1000, description="Streaming event count for burst tests")
