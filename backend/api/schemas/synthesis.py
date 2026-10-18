"""
API Layer: Pydantic v2 Schemas for Synthesis Endpoints.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ProfileRequest(BaseModel):
    raw_input_data: str = Field(..., description="Raw polymorphic JSON or sample strings to profile")
    target_ddl: str = Field(default="", description="Target BigQuery CREATE TABLE DDL")

class SynthesizeRequest(BaseModel):
    raw_input_data: str = Field(..., description="Raw polymorphic sample records")
    target_ddl: str = Field(..., description="Target CREATE TABLE DDL contract")
    target_table_name: Optional[str] = Field(default="gold_analytics.fact_orders", description="Destination table")

class MultiSourceSynthesizeRequest(BaseModel):
    sources: Dict[str, Any] = Field(..., description="Multi-source enterprise payload dictionary")
    target_ddl: str = Field(..., description="Target BigQuery DDL schema")
    target_table_name: Optional[str] = Field(default="gold_analytics.fact_reconciled_orders")
