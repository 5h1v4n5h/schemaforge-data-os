"""
Domain Layer: Pure enterprise business models, entities, and interfaces.
Zero framework or cloud dependencies.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

class IngestionStatus(str, Enum):
    INGESTED = "INGESTED"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    SYNTHESIZING = "SYNTHESIZING"
    VERIFIED = "VERIFIED"
    QUARANTINED = "QUARANTINED"
    COMMITTED = "COMMITTED"

class ScenarioType(str, Enum):
    SCENARIO_A = "scenario_a"
    SCENARIO_B = "scenario_b"
    SCENARIO_C = "scenario_c"
    SCENARIO_D = "scenario_d"

@dataclass(frozen=True)
class SchemaDriftEntity:
    """Immutable representation of a detected schema drift event."""
    drift_id: str
    tenant_id: str
    scenario: str
    detected_at: datetime
    raw_payload: Dict[str, Any]
    detected_mutations: List[str]
    status: IngestionStatus

@dataclass
class ReconciledOrderEntity:
    """Financial invariant model representing an audited e-commerce order."""
    order_id: str
    master_customer_id: str
    thelook_gross_amount_usd: float
    stripe_charge_amount_usd: float
    stripe_fee_amount_usd: float
    net_realized_revenue_usd: float
    payment_brand: str
    reconciliation_status: str
    delivery_sla_breached: bool
    order_date: datetime

    def verify_financial_conservation(self, tolerance: float = 0.001) -> bool:
        """Enforces invariant: Gross Amount - Fee == Net Realized Revenue +/- $0.00."""
        expected_net = round(self.stripe_charge_amount_usd - self.stripe_fee_amount_usd, 2)
        actual_net = round(self.net_realized_revenue_usd, 2)
        return abs(expected_net - actual_net) <= tolerance

@dataclass
class DqsScorecardEntity:
    """Mathematical decoupled Data Quality Scorecard."""
    completeness: float = 1.0
    validity: float = 1.0
    uniqueness: float = 1.0
    incident_resilience: float = 1.0

    @property
    def composite_score(self) -> float:
        """DQS = 0.30*C + 0.30*V + 0.20*U + 0.20*Inc"""
        score = (
            0.30 * self.completeness +
            0.30 * self.validity +
            0.20 * self.uniqueness +
            0.20 * self.incident_resilience
        )
        return round(score * 100.0, 2)
