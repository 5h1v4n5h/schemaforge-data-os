"""
API Layer: Ingestion Connectors Router.
Handles file uploads, SFTP polling, GCS buckets, and automated scheduling.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Body
from typing import Dict, Any

from backend.core.connectors import (
    FileUploadHandler,
    SFTPConnector,
    GCSBucketConnector,
    IngestionAutomationManager
)

router = APIRouter(prefix="/api/connectors", tags=["Ingestion Connectors"])

@router.post("/upload")
async def upload_ingestion_file(file: UploadFile = File(...)):
    """Uploads and auto-detects CSV, JSON, TSV, or Parquet payloads."""
    content = await file.read()
    result = FileUploadHandler.parse_uploaded_file(file.filename, content)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/sftp/test")
def test_sftp_connection(payload: Dict[str, Any] = Body(...)):
    """Tests SFTP connectivity, lists files, and filters using regex patterns."""
    host = payload.get("host", "sftp.partner-vendor.com")
    port = int(payload.get("port", 22))
    username = payload.get("username", "vendor_user")
    password = payload.get("password")
    remote_path = payload.get("remote_path", "/inbound/orders/")
    file_regex = payload.get("file_regex") or payload.get("regex_pattern") or r"^vendor_orders_\d{8}\.(csv|json)$"
    return SFTPConnector.test_and_list_files(host, port, username, password, remote_path, file_regex)

@router.post("/gcs/test")
def test_gcs_connection(payload: Dict[str, Any] = Body(...)):
    """Tests Google Cloud Storage connectivity and lists blobs by pattern."""
    bucket_uri = payload.get("bucket_uri")
    if not bucket_uri and payload.get("bucket_name"):
        prefix = payload.get("prefix", "").strip("/")
        bucket_uri = f"gs://{payload.get('bucket_name')}/{prefix}/" if prefix else f"gs://{payload.get('bucket_name')}/"
    if not bucket_uri:
        bucket_uri = "gs://vendor-inbound-data/orders/"

    file_pattern = payload.get("file_pattern") or payload.get("pattern") or "*.json"
    credentials_type = payload.get("credentials_type", "Application Default Credentials (ADC)")
    return GCSBucketConnector.test_and_list_blobs(bucket_uri, file_pattern, credentials_type)

@router.post("/automation")
def register_automation_job(payload: Dict[str, Any] = Body(...)):
    """Registers an automated ingestion pipeline (Scheduled Cron or Event-Driven Eventarc)."""
    return IngestionAutomationManager.register_job(payload)

@router.get("/automation")
def list_automation_jobs():
    """Returns active scheduled and event-driven ingestion pipelines."""
    jobs = IngestionAutomationManager.list_jobs()
    return {"jobs": jobs, "active_jobs": jobs}
