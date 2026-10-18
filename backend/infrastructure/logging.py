"""
Infrastructure Layer: Structured Google Cloud JSON Logger.
Formats logs as valid single-line JSON with severity levels, component tags, and trace correlation.
"""
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

class CloudLoggingFormatter(logging.Formatter):
    """Formats log records into Google Cloud Logging structured JSON format."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "component": getattr(record, "component", "schemaforge-backend"),
        }
        
        # Add optional correlation attributes
        if hasattr(record, "tenant_id"):
            log_entry["tenant_id"] = record.tenant_id
        if hasattr(record, "job_id"):
            log_entry["job_id"] = record.job_id
        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

def setup_cloud_logger(name: str = "schemaforge") -> logging.Logger:
    """Configures and returns a structured Cloud Logging logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CloudLoggingFormatter())
        logger.addHandler(handler)
        logger.propagate = False
        
    return logger

logger = setup_cloud_logger()
