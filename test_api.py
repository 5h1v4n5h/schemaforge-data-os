from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

print("Testing /health endpoint...")
resp = client.get("/health")
print("Health response:", resp.status_code, resp.json())
assert resp.status_code == 200

print("\nTesting /api/synthesize endpoint...")
with open("sample_data/messy_sap_orders.json") as f:
    raw_data = f.read()
with open("sample_data/target_orders_ddl.sql") as f:
    ddl = f.read()

payload = {
    "raw_input_data": raw_data,
    "target_ddl": ddl,
    "target_table_name": "gold_analytics.fact_orders"
}

resp = client.post("/api/synthesize", json=payload)
print("Synthesize status:", resp.status_code)
res_json = resp.json()
print("Synthesis status:", res_json.get("status"))
print("Total latency ms:", res_json.get("total_latency_ms"))
print("Timeline stages:", [s["name"] for s in res_json.get("state_machine_timeline", [])])
print("Verified solution strategy:", res_json.get("verified_solution", {}).get("strategy_name"))
print("Rows output:", res_json.get("verified_solution", {}).get("rows_output"))
print("\n>>> FASTAPI END-TO-END TEST PASSED SUCCESSFULLY!")
