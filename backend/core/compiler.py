import os
from typing import Dict, Any

class CanonicalCompiler:
    """Stage 6: Compiles verified transformations into standalone Cloud Run microservices."""

    @staticmethod
    def generate_service_bundle(
        python_code: str,
        pandera_code: str,
        target_schema_name: str = "gold_analytics.fact_orders"
    ) -> Dict[str, str]:
        """Generates main.py, Dockerfile, and cloudbuild.yaml for Cloud Run deployment."""

        fastapi_main = f'''"""
SchemaForge Generated Production ETL Microservice
Deployed on Google Cloud Run with Pandera Data Quality Guardrails.
Target Table: {target_schema_name}
"""

import os
from fastapi import FastAPI, HTTPException, Body
from typing import List, Dict, Any
import pandas as pd
import polars as pl
import pandera as pa

app = FastAPI(title="SchemaForge Production ETL Pipeline", version="1.0.0")

# --- Synthesized Invariant Schema ---
{pandera_code}

# --- Synthesized Transformation Function ---
{python_code}

@app.get("/health")
def health_check():
    return {{"status": "HEALTHY", "target_table": "{target_schema_name}"}}

@app.post("/transform")
def run_transform(payload: List[Dict[str, Any]] = Body(...)):
    try:
        # 1. Transform raw payload
        transformed = transform(payload)
        
        # 2. Validate via Pandera if schema exists
        if "schema" in globals() and isinstance(globals()["schema"], pa.DataFrameSchema):
            df = pd.DataFrame(transformed)
            schema.validate(df)
            
        return {{
            "status": "SUCCESS",
            "rows_processed": len(transformed),
            "data": transformed
        }}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Pipeline validation error: {{str(e)}}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''

        dockerfile = '''FROM python:3.11-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
'''

        cloud_run_deploy_sh = f'''#!/bin/bash
# Google Cloud Run One-Command Deployment
SERVICE_NAME="schemaforge-pipeline"
REGION="us-central1"

gcloud run deploy $SERVICE_NAME \\
  --source . \\
  --platform managed \\
  --region $REGION \\
  --allow-unauthenticated \\
  --memory 1Gi \\
  --cpu 1 \\
  --timeout 300
'''

        return {
            "main.py": fastapi_main,
            "Dockerfile": dockerfile,
            "deploy.sh": cloud_run_deploy_sh
        }
