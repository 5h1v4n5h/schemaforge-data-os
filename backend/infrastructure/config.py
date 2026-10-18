"""
Infrastructure Layer: Validated Application & Cloud Settings.
Uses Pydantic v2 / BaseSettings pattern with safe defaults for Cloud Run.
"""
import os
from pydantic import BaseModel, Field

class AppSettings(BaseModel):
    """Centralized, immutable application configuration with environment validation."""
    app_name: str = "SchemaForge Data-OS"
    version: str = "1.0.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENV", "production"))
    
    # Google Cloud Platform Parameters
    gcp_project_id: str = Field(default_factory=lambda: os.getenv("GCP_PROJECT", os.getenv("GOOGLE_CLOUD_PROJECT", "project-29e65474-32d7-45e0-803")))
    gcp_region: str = Field(default_factory=lambda: os.getenv("GOOGLE_CLOUD_REGION", "us-central1"))
    bq_dataset_gold: str = Field(default_factory=lambda: os.getenv("BQ_DATASET_GOLD", "gold_analytics"))
    
    # Execution & Sandbox Limits
    sandbox_timeout_seconds: float = 5.0
    max_concurrent_tasks: int = 80
    circuit_breaker_error_threshold: int = 5
    retry_max_attempts: int = 3
    retry_base_delay_seconds: float = 0.2
    
    # BigQuery Warehouse Tables
    tbl_fact_reconciled_orders: str = "fact_reconciled_orders"
    tbl_dim_customers_master: str = "dim_customers_master"
    tbl_fact_orders: str = "fact_orders"

# Global singleton settings
settings = AppSettings()
