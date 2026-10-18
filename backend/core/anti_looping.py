import ast
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

try:
    import sqlglot
    from sqlglot import exp
    HAS_SQLGLOT = True
except ImportError:
    HAS_SQLGLOT = False

@dataclass
class RepairState:
    hypothesis_id: str
    turn: int = 0
    max_turns: int = 3
    best_code: Optional[str] = None
    best_score: float = -1.0
    seen_ast_hashes: Set[str] = field(default_factory=set)
    seen_trace_buckets: Dict[str, int] = field(default_factory=dict)
    episodic_reflections: List[str] = field(default_factory=list)

class AntiLoopingController:
    """Enforces AST deduplication, traceback bucketization, and context eviction."""

    @staticmethod
    def canonical_ast_hash(code_str: str) -> str:
        """Computes a normalized SHA-256 hash of the code's Abstract Syntax Tree."""
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    node.id = "_var"
            normalized = ast.dump(tree, annotate_fields=True, include_attributes=False)
            return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        except SyntaxError:
            return f"SYNTAX_ERR_{hashlib.md5(code_str.encode()).hexdigest()}"

    @staticmethod
    def bucketize_traceback(exc_type: str, tb_lines: List[str], op_sig: str) -> Tuple[str, str]:
        """Prunes library internals and produces a deterministic signature hash."""
        user_frames = [line for line in tb_lines if "site-packages" not in line and "lib" not in line]
        pruned_tb = "\n".join(user_frames[-4:]) if len(user_frames) > 4 else "\n".join(user_frames)
        bucket_raw = f"{exc_type}::{op_sig}::{user_frames[-1] if user_frames else ''}"
        bucket_hash = hashlib.sha1(bucket_raw.encode("utf-8")).hexdigest()[:12]
        return bucket_hash, pruned_tb

    @staticmethod
    def enforce_sql_safety_limit(sql_query: str, max_rows: int = 5_000_000) -> str:
        """Injects LIMIT into unbounded SQL queries via AST rewriting."""
        if HAS_SQLGLOT:
            try:
                ast_expr = sqlglot.parse_one(sql_query)
                if not ast_expr.find(exp.Limit):
                    ast_expr = ast_expr.limit(max_rows)
                return ast_expr.sql()
            except Exception:
                return sql_query
        else:
            if "LIMIT" not in sql_query.upper():
                return f"{sql_query.rstrip(';')} LIMIT {max_rows};"
            return sql_query

    def register_attempt(
        self, state: RepairState, code: str, score: float,
        exc_type: Optional[str], tb_lines: List[str], reflection: str
    ) -> Tuple[bool, str]:
        """Registers a candidate attempt and checks for oscillation or exhaustion."""
        state.turn += 1
        ast_hash = self.canonical_ast_hash(code)
        if ast_hash in state.seen_ast_hashes:
            return False, "ABORT_BRANCH: Exact AST structural oscillation detected."
        state.seen_ast_hashes.add(ast_hash)

        if score > state.best_score:
            state.best_score = score
            state.best_code = code

        if exc_type:
            b_hash, _ = self.bucketize_traceback(exc_type, tb_lines, state.hypothesis_id)
            state.seen_trace_buckets[b_hash] = state.seen_trace_buckets.get(b_hash, 0) + 1
            if state.seen_trace_buckets[b_hash] >= 2:
                return False, f"ABORT_BRANCH: Repeated identical exception bucket {b_hash}."

        if reflection:
            state.episodic_reflections.append(reflection)
            if len(state.episodic_reflections) > 3:
                state.episodic_reflections.pop(0)

        if state.turn >= state.max_turns and score < 1.0:
            return False, "ABORT_BRANCH: Max repair depth (3 turns) reached without convergence."
        return True, "CONTINUE_REPAIR"
