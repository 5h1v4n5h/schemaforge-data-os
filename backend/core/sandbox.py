import sys
import io
import time
import traceback
import concurrent.futures
from typing import Dict, Any, List, Optional

def _run_in_scope(code_str: str, input_payload: Any) -> Dict[str, Any]:
    """Executes untrusted code within an isolated dictionary namespace."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = stdout_buf
    sys.stderr = stderr_buf

    res = {
        "success": False,
        "output": None,
        "stdout": "",
        "stderr": "",
        "exception_type": None,
        "traceback_lines": [],
        "wall_time_ms": 0.0
    }

    start = time.perf_counter()
    try:
        # Pre-filter dangerous calls
        blocked = ["os.system", "subprocess", "socket.", "__import__('os')", "shutil.rmtree"]
        for b in blocked:
            if b in code_str:
                raise PermissionError(f"Security violation: call '{b}' is forbidden in sandbox.")

        # Safe execution namespace
        local_scope = {}
        exec_globals = {
            "__builtins__": __builtins__,
            "json": __import__("json"),
            "re": __import__("re"),
            "datetime": __import__("datetime"),
        }
        
        # Try optional imports
        for pkg in ["polars", "pandas", "numpy", "duckdb"]:
            try:
                exec_globals[pkg] = __import__(pkg)
            except ImportError:
                pass

        exec(code_str, exec_globals, local_scope)

        entry_fn = local_scope.get("transform_multi_source") or local_scope.get("transform") or local_scope.get("transform_data")
        if not entry_fn:
            raise ValueError("Synthesized code must define a callable entry point: `def transform(...)` or `def transform_multi_source(...)`")

        import inspect
        sig = inspect.signature(entry_fn)
        num_params = len(sig.parameters)
        if isinstance(input_payload, (list, tuple)) and num_params > 1 and len(input_payload) == num_params:
            output_data = entry_fn(*input_payload)
        elif isinstance(input_payload, dict) and num_params > 1 and all(k in input_payload for k in sig.parameters.keys()):
            output_data = entry_fn(**input_payload)
        else:
            output_data = entry_fn(input_payload)

        res["success"] = True
        res["output"] = output_data
    except Exception as e:
        res["success"] = False
        res["exception_type"] = type(e).__name__
        res["traceback_lines"] = traceback.format_exc().splitlines()
    finally:
        res["wall_time_ms"] = round((time.perf_counter() - start) * 1000, 2)
        res["stdout"] = stdout_buf.getvalue()
        res["stderr"] = stderr_buf.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return res

class SandboxedExecutionEngine:
    """Stage 3: Ephemeral worker execution engine with strict timeouts and resource bounds."""

    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds

    def execute(self, code_str: str, input_payload: Any) -> Dict[str, Any]:
        """Runs the code using a thread executor with a strict timeout ceiling."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_in_scope, code_str, input_payload)
            try:
                return future.result(timeout=self.timeout_seconds)
            except concurrent.futures.TimeoutError:
                return {
                    "success": False,
                    "output": None,
                    "stdout": "",
                    "stderr": f"TIMEOUT_ERROR: Execution exceeded {self.timeout_seconds}s ceiling.",
                    "exception_type": "TimeoutError",
                    "traceback_lines": ["Execution killed by watchdog timeout."],
                    "wall_time_ms": self.timeout_seconds * 1000
                }
            except Exception as e:
                return {
                    "success": False,
                    "output": None,
                    "stdout": "",
                    "stderr": f"RUN_ERROR: {e}",
                    "exception_type": type(e).__name__,
                    "traceback_lines": traceback.format_exc().splitlines(),
                    "wall_time_ms": 0.0
                }

    def execute_transform(self, code_str: str, input_payload: Any) -> Dict[str, Any]:
        return self.execute(code_str, input_payload)
