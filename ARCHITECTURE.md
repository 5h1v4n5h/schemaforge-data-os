# SchemaForge (NeuroETL)
## Autonomous Neuro-Symbolic Program Synthesis and Data Engineering Architecture

### 1. Academic and Theoretical Foundations

#### 1.1 Inductive Program Synthesis and Programming-by-Example (PBE)
Inductive program synthesis—and its pragmatic realization, Programming-by-Example (PBE)—addresses the problem of automatically constructing an executable function $\rho$ drawn from a target language $\mathcal{L}$ such that for a finite set of input-output specification pairs $\{(X_i, Y_i)\}_{i=1}^K$, the synthesized program satisfies $\rho(X_i) = Y_i$ for all $i \in \{1, \dots, K\}$ while generalizing accurately to unseen holdout test inputs $X'_j$. In enterprise data engineering, where business teams routinely provide raw, malformed sample payloads alongside desired target table schemas, PBE shifts the engineering paradigm from imperative manual scripting to specification-driven code synthesis.

The first generation of industrial PBE systems achieved tractability by severely restricting the hypothesis space $\mathcal{L}$ via handcrafted Domain-Specific Languages (DSLs):
* **FlashFill & FlashFill++ (Gulwani 2011; Cambronero et al., 2023):** Built on Version Space Algebras (VSA) for string transformations. Fails on arithmetic, nested JSONs, or complex joins.
* **Syntax-Guided Synthesis (SyGuS) & Bee (Alur et al.; Xu et al., TOSEM 2024):** Explores Context-Free Grammars over SMT theories and relational meta-DSLs. Suffers from state-space explosion on deep ASTs.
* **DreamCoder (Ellis et al., PLDI 2021 / Nature 2023):** Bayesian wake-sleep learning using recognition networks and e-graph refactoring. Lacks broad zero-shot world knowledge of messy enterprise ERP/API formats.
* **ARC-AGI Breakthroughs (Greenblatt 2024; Wang et al., 2024; BARC ICLR 2025; Tufa Labs 2025-2026):** Proved that pairing frontier LLMs operating over unrestricted Python with deterministic execution verifiers and live REPL scaffolding achieves state-of-the-art results:
  $$\hat{y}_{\text{test}} = \begin{cases} f(x_{\text{test}}) \text{ where } f \sim \text{Uniform}(F) & \text{if } F \neq \emptyset \\ \arg\max_y t_\theta(y \mid x_{\text{train}}, y_{\text{train}}, x_{\text{test}}) & \text{if } F = \emptyset \end{cases}$$

---

#### 1.2 Iterative Code Repair and Reflection in Agentic Loops
Zero-shot LLM code generation is inherently brittle. SchemaForge embeds the LLM inside an execution-guided closed loop where runtime feedback (stdout, stderr, exception tracebacks, and test assertion diffs) conditions subsequent refinements:
* **CodeRL (Le et al., NeurIPS 2022):** Actor-critic framework with runtime error signals.
* **Self-Debugging (Chen et al., ICLR 2024):** Rubber-duck explanation combined with traceback analysis.
* **Reflexion (Shinn et al., NeurIPS 2023):** Verbal reinforcement learning persisting diagnostic critiques $sr_t$ in episodic memory.
* **Convergence Dynamics:** 75%–85% of repairs succeed within turns 1–3. Single-path loops are capped at $D_{\max} = 3$ to prevent infinite cycling.

---

#### 1.3 Neuro-Symbolic Invariants and Formal Verification
SchemaForge pairs neural program synthesis with a three-tier formal verification contract:
1. **Tier 1: Row-Level Structural Contracts (Pydantic v2):** Enforces strict types, nullability, and regex constraints on every record.
2. **Tier 2: Columnar & Statistical Distribution Invariants (Pandera):** Validates deterministic column bounds and statistical hypotheses (Kolmogorov-Smirnov two-sample tests, Student's $t$-tests).
3. **Tier 3: Metamorphic Property-Based Testing (Hypothesis):** Fuzzes 100 synthetic variations to prove mathematical invariants (e.g. Conservation of Financial Sums: $\sum_{\text{input}} \text{amount} == \sum_{\text{output}} \text{amount}$).

---

### 2. Enterprise Market Landscape & Problem Validation
* **Cost of Bad Data:** $12.9M annual average cost per organization (Gartner); $3.1T economy-wide drag (HBR).
* **Engineering Tax:** Data engineers spend 40% of their workweek (2 days/week) triaging, debugging, and patching broken pipelines (Monte Carlo & Wakefield Research).
* **Mean Time to Resolve (MTTR):** 15 hours per data incident; 67 data incidents per month.
* **Failure Modes of Existing Tools:**
  * *Fivetran/Airbyte:* Rigid 1:1 replication; dumps polymorphic payloads as raw unparsed JSON.
  * *dbt/Dataform:* Declarative SQL DAGs break on upstream schema drift.
  * *Zero-Shot Copilots:* Hallucinate column names and fail silently on semantic scale shifts (e.g., dollars vs. cents).
  * *SchemaForge:* Autonomous synthesis, sandboxed verification, zero hallucinations.

---

### 3. Six-Stage Synthesis & Verification Architecture

```
  [ Raw Input Data & Target Schema ]
                 │
                 ▼
     [ Stage 1: Profiler ] ──────► Computes statistical moments, null %, JSON path tree, PII mask
                 │
                 ▼
  [ Stage 2: Hypothesis Gen ] ───► Gemini 1.5 Pro generates 3 structural hypotheses + Pandera contract
                 │
                 ▼
    [ Stage 3: gVisor Sandbox ] ─► Isolated Cloud Run execution (sub-second, memory & CPU capped)
                 │
                 ▼
  [ Stage 4: Invariant Checker ] ─► Cell diffs == 0 AND 100% Pandera/Hypothesis checks pass?
          │               │
         NO              YES
          │               │
          ▼               ▼
 [ Stage 5: Refiner ]   [ Stage 6: Canonical Compiler ]
  - Rubber-duck diff     - Wrap in FastAPI + Pandera @check_io
  - Reflexion memory     - Deploy serverless Cloud Run endpoint
  - AST deduplication    - Bind Eventarc / Pub/Sub triggers to BigQuery
```

---

### 4. Google Cloud Stack & Implementation Blueprint

* **LLM Layer:**
  * **Gemini 1.5 Pro:** Outer loop architect for complex schema reasoning, documentation ingestion, and hypothesis generation.
  * **Gemini 1.5 Flash:** Inner loop debugger for sub-second REPL repairs and AST patch generation.
* **Compute & Execution Plane:**
  * **Google Cloud Run:** Hosts the Agent Control Plane and isolated execution sandbox (gVisor/runsc with zero-network egress).
* **Data & Storage Plane:**
  * **Google Cloud Firestore:** Real-time state store for sessions, checkpoints, and Reflexion memory.
  * **Google BigQuery:** Analytical telemetry warehouse and target data lakehouse.
  * **Google Cloud Storage (GCS):** Raw payload landing zone and dead-letter queue.
* **Integration Layer:**
  * **Vertex AI Agent Builder:** OpenAPI 3.0 tool registration for `inspect_schema`, `run_code`, `diff_output`, `verify_invariants`.
  * **Google Antigravity SDK:** Real-time streaming of `response.thoughts` and `response.tool_calls`.
