"""
Domain Layer: Abstract Interfaces & Protocols.
"""
from typing import Protocol, Dict, Any, List, Optional
from backend.domain.entities import SchemaDriftEntity, DqsScorecardEntity

class ISynthesisEngine(Protocol):
    """Protocol for neuro-symbolic program synthesis."""
    def generate_hypotheses(self, profile_context: Dict[str, Any]) -> List[Dict[str, Any]]: ...

class ISandboxExecutor(Protocol):
    """Protocol for isolated execution."""
    def execute(self, code: str, raw_input: Any) -> Dict[str, Any]: ...

class IInvariantVerifier(Protocol):
    """Protocol for formal Pandera and metamorphic verification."""
    def verify_pandera_contract(self, output_records: List[Dict[str, Any]], contract_code: str) -> Dict[str, Any]: ...

class ITenantRepository(Protocol):
    """Protocol for tenant metadata and telemetry storage."""
    def get_telemetry(self, tenant_id: str) -> Dict[str, Any]: ...
    def pulse_traffic(self, tenant_id: str, count: int) -> Dict[str, Any]: ...
    def redrive_dlq(self, tenant_id: str) -> Dict[str, Any]: ...
