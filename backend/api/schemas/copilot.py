"""
API Layer: Pydantic v2 Schemas for E-Commerce Copilot Endpoints.
"""
from pydantic import BaseModel, Field

class CopilotQueryRequest(BaseModel):
    query: str = Field(default="Show financial revenue and reconciliation", description="Natural language question for e-commerce domain intelligence")
