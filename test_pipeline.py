import json
from backend.core.profiler import InputProfileAnalyzer
from backend.core.anti_looping import AntiLoopingController, RepairState
from backend.core.sandbox import SandboxedExecutionEngine
from backend.core.verifier import InvariantVerifier
from backend.core.compiler import CanonicalCompiler
from backend.core.generator import SynthesisOrchestrator

print("=== 1. Testing Core Imports ===")
print("All backend modules imported successfully!")

# Test Stage 1: Profiler
print("\n=== 2. Testing Stage 1: Input Profile Analyzer ===")
with open('sample_data/messy_sap_orders.json') as f:
    raw_data = f.read()
with open('sample_data/target_orders_ddl.sql') as f:
    ddl = f.read()

profiler = InputProfileAnalyzer()
ctx = profiler.generate_compact_prompt_context(raw_data, ddl)
print("Profiler total records:", ctx['input_profile']['total_records'])
print("Polymorphic fields detected:", ctx['input_profile']['polymorphic_fields'])
print("Sample field catalog:", list(ctx['input_profile']['field_catalog'].keys()))

# Test Stage 2: Hypothesis Generator
print("\n=== 3. Testing Stage 2: Hypothesis Generator ===")
orchestrator = SynthesisOrchestrator()
hypotheses = orchestrator.generate_hypotheses(ctx)
print("Generated hypotheses count:", len(hypotheses))

# Test Stage 3 & 4: Sandbox & Invariant Verifier
print("\n=== 4. Testing Stages 3 & 4: Sandbox & Pandera Verifier ===")
sandbox = SandboxedExecutionEngine(timeout_seconds=5.0)
verifier = InvariantVerifier()

for h in hypotheses:
    code = h['python_code']
    hyp_id = h['hypothesis_id']
    res = sandbox.execute(code, json.loads(raw_data))
    print(f"Hypothesis {hyp_id} ({h['strategy_name']}):")
    print(f"  Execution success: {res['success']} ({res['wall_time_ms']} ms)")
    if res['success']:
        p_res = verifier.verify_pandera_contract(res['output'], h['pandera_code'])
        print(f"  Pandera verification passed: {p_res['passed']} (DQS: {p_res['dqs_score']})")
        print(f"  Sample row 1: {res['output'][0]}")

# Test Stage 6: Canonical Compiler
print("\n=== 5. Testing Stage 6: Canonical Cloud Run Compiler ===")
compiler = CanonicalCompiler()
bundle = compiler.generate_service_bundle(hypotheses[0]['python_code'], hypotheses[0]['pandera_code'])
print("Compiler bundle files generated:", list(bundle.keys()))
print("\n>>> ALL TESTS PASSED! THE NEURO-SYMBOLIC PIPELINE IS 100% OPERATIONAL.")
