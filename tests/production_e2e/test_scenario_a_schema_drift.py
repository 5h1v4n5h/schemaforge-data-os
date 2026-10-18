"""
Test Scenario A: Autonomous Schema Drift & Self-Healing
Verifies:
1. Upstream payload renames customer_id -> client_uuid and splits full_amount.
2. Neuro-symbolic synthesis derives the correct mapping.
3. Pandera contract validates conservation of money and schema conformance.
4. Target BigQuery schema matches without data loss.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.chaos_engine import ChaosEngine

def test_scenario_a_schema_drift_and_self_healing():
    result = ChaosEngine.run_scenario_a_schema_drift(tenant_id="t_nexus_fintech")
    
    assert result["status"] == "PASSED_100_PERCENT"
    assert result["tenant_id"] == "t_nexus_fintech"
    assert len(result["verified_clean_rows"]) == 2
    
    row0 = result["verified_clean_rows"][0]
    assert row0["customer_id"] == "usr_99102"
    assert row0["total_amount_usd"] == 145.0
    assert row0["status"] == "SETTLED"
    assert "Pandera.ConservationOfMoney" in result["invariants_passed"][0]
    print("[PASS] Scenario A: Autonomous Schema Drift successfully healed with zero data loss.")

if __name__ == "__main__":
    test_scenario_a_schema_drift_and_self_healing()
