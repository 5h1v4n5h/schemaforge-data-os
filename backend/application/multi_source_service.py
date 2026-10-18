"""
Application Layer: Multi-Source Mastering & Financial Reconciliation Service.
"""
import time
import json
from typing import Dict, Any, List, Optional

from backend.core.profiler import InputProfileAnalyzer
from backend.core.sandbox import SandboxedExecutionEngine
from backend.core.verifier import InvariantVerifier
from backend.core.compiler import CanonicalCompiler
from backend.core.generator import SynthesisOrchestrator
from backend.infrastructure.logging import logger

class MultiSourceService:
    def __init__(
        self,
        profiler: Optional[InputProfileAnalyzer] = None,
        sandbox: Optional[SandboxedExecutionEngine] = None,
        verifier: Optional[InvariantVerifier] = None,
        compiler: Optional[CanonicalCompiler] = None,
        orchestrator: Optional[SynthesisOrchestrator] = None,
    ):
        self.profiler = profiler or InputProfileAnalyzer()
        self.sandbox = sandbox or SandboxedExecutionEngine(timeout_seconds=5.0)
        self.verifier = verifier or InvariantVerifier()
        self.compiler = compiler or CanonicalCompiler()
        self.orchestrator = orchestrator or SynthesisOrchestrator()

    def execute_multi_source_synthesis(
        self, sources: Dict[str, Any], target_ddl: str, target_table_name: str = "gold_analytics.fact_reconciled_orders"
    ) -> Dict[str, Any]:
        """Executes multi-source entity mastering and invariant checks."""
        start_time = time.perf_counter()
        timeline = []

        # 1. Multi-Source Profiling
        t0 = time.perf_counter()
        multi_profile = self.profiler.profile_multi_source(sources, target_ddl)
        timeline.append({
            "stage": 1,
            "name": "Multi-Source Profile Analyzer",
            "duration_ms": round((time.perf_counter() - t0) * 1000, 2),
            "status": "COMPLETED",
            "details": f"Analyzed {len(sources)} disparate enterprise sources. Detected {len(multi_profile.get('detected_cross_links', []))} cross-source linkage candidates."
        })

        # 2. Hypothesis Generation
        t1 = time.perf_counter()
        hypotheses = self.orchestrator.generate_multi_source_mastering_hypotheses(multi_profile)
        timeline.append({
            "stage": 2,
            "name": "Mastering & Alignment Generator",
            "duration_ms": round((time.perf_counter() - t1) * 1000, 2),
            "status": "COMPLETED",
            "details": f"Synthesized {len(hypotheses)} candidate entity resolution, survivorship, and reconciliation strategies."
        })

        thelook_data = sources.get("thelook_orders") or sources.get("source1_thelook_orders") or sources.get("source1") or []
        stripe_data = sources.get("stripe_charges") or sources.get("source2_stripe_charges") or sources.get("source2") or []
        crm_data = sources.get("crm_tickets") or sources.get("source3_crm_tickets") or sources.get("source3") or []

        if isinstance(thelook_data, str):
            try: thelook_data = json.loads(thelook_data)
            except Exception: pass
        if isinstance(stripe_data, str):
            try: stripe_data = json.loads(stripe_data)
            except Exception: pass
        if isinstance(crm_data, str):
            try: crm_data = json.loads(crm_data)
            except Exception: pass

        input_tuple = (thelook_data, stripe_data, crm_data)
        verified_solution = None
        all_evaluations = []

        for hyp in hypotheses:
            hyp_id = hyp.get("hypothesis_id", "HYP_01")
            code = hyp.get("python_code", "")
            pandera_code = hyp.get("pandera_code", "")

            # 3. Sandbox Execution
            t2 = time.perf_counter()
            exec_res = self.sandbox.execute(code, input_tuple)
            timeline.append({
                "stage": 3,
                "name": f"Sandboxed Execution ({hyp_id})",
                "duration_ms": round((time.perf_counter() - t2) * 1000, 2),
                "status": "COMPLETED" if exec_res["success"] else "FAILED",
                "details": f"Executed multi-source pipeline inside gVisor isolate in {exec_res['wall_time_ms']}ms."
            })

            if exec_res["success"] and isinstance(exec_res["output"], dict):
                output = exec_res["output"]
                dim_customers = output.get("dim_master_customer", [])
                fact_orders = output.get("fact_reconciled_orders", [])

                # 4. Invariant Verification Gate
                t3 = time.perf_counter()
                recon_res = self.verifier.verify_multi_source_reconciliation(sources, dim_customers, fact_orders)
                timeline.append({
                    "stage": 4,
                    "name": "Metamorphic Invariant Gate",
                    "duration_ms": round((time.perf_counter() - t3) * 1000, 2),
                    "status": "PASSED" if recon_res["reconciliation_passed"] else "VIOLATED",
                    "details": f"Data Quality Score: {recon_res['data_quality_score'] * 100}%. Financial reconciliation: {recon_res['financial_summary']}."
                })

                eval_record = {
                    "hypothesis_id": hyp_id,
                    "strategy_name": hyp.get("strategy_name", ""),
                    "description": hyp.get("description", ""),
                    "exec_success": True,
                    "reconciliation_passed": recon_res["reconciliation_passed"],
                    "data_quality_score": recon_res["data_quality_score"],
                    "financial_summary": recon_res["financial_summary"],
                    "mastering_summary": recon_res["mastering_summary"],
                    "dim_master_customer": dim_customers,
                    "fact_reconciled_orders": fact_orders,
                    "python_code": code,
                    "pandera_code": pandera_code
                }
                all_evaluations.append(eval_record)

                if recon_res["reconciliation_passed"]:
                    verified_solution = eval_record
                    break
            else:
                all_evaluations.append({
                    "hypothesis_id": hyp_id,
                    "exec_success": False,
                    "error": exec_res.get("exception_type"),
                    "traceback": exec_res.get("traceback_lines")[:3],
                    "python_code": code
                })

        # 6. Canonical Compilation
        t5 = time.perf_counter()
        if verified_solution:
            deployment_bundle = self.compiler.generate_service_bundle(
                verified_solution["python_code"],
                verified_solution["pandera_code"],
                target_table_name
            )
            compilation_status = "READY_FOR_BIGQUERY_AND_CLOUD_RUN"
        else:
            deployment_bundle = {}
            compilation_status = "PENDING_REFINEMENT"

        timeline.append({
            "stage": 6,
            "name": "Canonical Cloud Run & BigQuery Compiler",
            "duration_ms": round((time.perf_counter() - t5) * 1000, 2),
            "status": compilation_status,
            "details": "Compiled production BigQuery DDL, Dataform transforms, and Cloud Run deployment microservices."
        })

        total_duration = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "status": "SUCCESS" if verified_solution else "FAILED",
            "total_latency_ms": total_duration,
            "state_machine_timeline": timeline,
            "detected_cross_links": multi_profile.get("detected_cross_links", []),
            "verified_solution": verified_solution,
            "all_candidates": all_evaluations,
            "deployment_bundle": deployment_bundle
        }

multi_source_service = MultiSourceService()
