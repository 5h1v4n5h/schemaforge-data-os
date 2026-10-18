"""
Application Layer: E-Commerce Copilot Orchestrator & Domain Query Evaluator.
"""
from typing import Dict, Any, List
from backend.core.ecommerce_copilot import EcommerceCopilotEngine

class CopilotService:
    @staticmethod
    def get_proactive_anomalies() -> List[Dict[str, Any]]:
        return EcommerceCopilotEngine.get_proactive_alerts()

    @staticmethod
    def evaluate_query(query: str) -> Dict[str, Any]:
        return EcommerceCopilotEngine.query_copilot(query)

copilot_service = CopilotService()
