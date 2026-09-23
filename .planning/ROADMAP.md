# Roadmap: EpiGraph

## Overview

EpiGraph transitions from mathematical formulation and local algorithmic validation on the LoCoMo benchmark to a distributed, production-grade memory system and peer-reviewed arXiv pre-print. The roadmap spans 4 distinct phases: local algorithmic validation (completed), distributed dual-store scaling, longitudinal evaluation & ablations, and LaTeX manuscript preparation for arXiv submission.

## Phases

### Milestone 1: Core Algorithmic Validation & Distributed Scaffolding (Complete)
- [x] **Phase 1: Local Algorithmic Engine & LoCoMo Benchmark Validation** - Core graph algorithms, baselines, and empirical validation across 496 LoCoMo questions.
- [x] **Phase 2: Distributed Dual-Store & Ingestion Reliability** - Redis Stack (HNSW) + Neo4j (GDS) dual-brain integration mediated by Redis Streams with incremental deduplication.
- [x] **Phase 3: Longitudinal SCDP Simulation & Ablation Suite** - 100-session synthetic longitudinal simulation, God Node emergence tracking, CATD scaffolding retention tests, and ablation profiling.
- [x] **Phase 4: LaTeX Manuscript Preparation & arXiv Pre-Print Submission** - Publication-grade LaTeX paper compilation, TikZ vector architecture diagrams, and arXiv submission to `cs.AI` / `cs.CL`.

### Milestone 2: Advanced Empirical Validation & Downstream Closed-Loop Suite (Complete)
- [x] **Phase 5: Closed-Loop Downstream LLM Generation QA Benchmark** - Real-time downstream LLM question-answering generation on LoCoMo contexts measuring Token F1, Exact Match (EM), and ROUGE-L.
- [x] **Phase 6: LongMemEval Knowledge Update & Contradiction Resolution** - Benchmark directed `SUPERSEDES` and `CORROBORATES` edge filtering against mutating user facts; measure Split-Brain Hallucination Rate.
- [x] **Phase 7: Hyperparameter Sensitivity Landscape & Embedding Invariance** - Sweep PageRank damping $d \in [0.65, 0.95]$, RRF $k \in [20, 100]$, and test embedding backbone invariance.
- [x] **Phase 8: Manuscript Integration & Extended Camera-Ready Package** - Integrate downstream generation tables, update references, and regenerate 300 DPI figures.

---

## Phase Details

### Phase 1: Local Algorithmic Engine & LoCoMo Benchmark Validation
**Goal**: Build a standalone local prototype of EpiGraph, implement baseline systems, and quantitatively evaluate performance across all 10 multi-session conversations in LoCoMo.  
**Depends on**: Nothing (Initial Phase)  
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, CORE-06, CORE-07, CORE-08, BENCH-01, BENCH-02, BENCH-03, BENCH-04, BENCH-05  
**Success Criteria**:
  1. Dense vector engine (`all-MiniLM-L6-v2`), BM25, and Dynamic Cognitive Graph run locally without external service dependencies.
  2. U-PPR, God Node classification, and CATD execute with sub-25ms average latency.
  3. LoCoMo benchmark evaluates 496 questions across all 10 long-term multi-session conversations.
  4. EpiGraph achieves statistically significant gains over Dense Vector RAG (+58.3% Recall@1, +25.9% Recall@5, +37.3% MRR, +18.11 point gain on Temporal Reasoning).

**Plans**:
- [x] 01-01: Build modular engine (`src/embeddings.py`, `src/bm25.py`, `src/graph_memory.py`, `src/rrf.py`, `src/epigraph_pipeline.py`).
- [x] 01-02: Implement baselines (`baselines/vector_rag.py`, `baselines/bm25_baseline.py`, `baselines/static_graph_rag.py`).
- [x] 01-03: Create automated runner `run_locomo_benchmark.py` and generate empirical evaluation report.

---

### Phase 2: Distributed Dual-Store & Ingestion Reliability
**Goal**: Connect the local algorithmic engine to production distributed storage engines: Redis Stack for fast document/vector indexing and Neo4j Enterprise GDS for native Cypher graph operations, decoupled via Redis Streams.  
**Depends on**: Phase 1  
**Requirements**: DIST-01, DIST-02, DIST-03, DIST-04  
**Success Criteria**:
  1. RedisJSON and RediSearch HNSW index vectors with sub-millisecond query time.
  2. Neo4j GDS executes in-memory native PageRank and Louvain algorithms via atomic Cypher transactions.
  3. Redis Streams (`XREADGROUP`, `XPENDING`, DLQ) guarantees eventual consistency across Redis and Neo4j dual-writes without split-brain failure.
  4. Incremental K-NN deduplication & clustering (HNSW + DBSCAN) scales entity deduplication without $O(n^2)$ matrix memory blowups.

**Plans**:
- [x] 02-01: Implement Redis Stack adapter with RedisJSON documents and RediSearch HNSW indexing.
- [x] 02-02: Implement Neo4j GDS driver with Cypher queries for directed `SUPERSEDES` and `CORROBORATES` edges.
- [x] 02-03: Implement Redis Streams ingestion worker with retry logic and Dead Letter Queue.
- [x] 02-04: Implement incremental HNSW + DBSCAN entity deduplication for the background Dreaming worker.

---

### Phase 3: Longitudinal SCDP Simulation & Ablation Suite
**Goal**: Execute a simulated 90-day continuous deployment protocol (100 sessions across 4 domains) to measure God Node stability, CATD scaffolding retention, and component ablations.  
**Depends on**: Phase 1 (and optional Phase 2)  
**Requirements**: EVAL-01, EVAL-02, EVAL-03, EVAL-04  
**Success Criteria**:
  1. 100-session synthetic longitudinal simulation produces verifiable God Node centrality trajectory curves.
  2. Scaffolding retention test proves CATD retains 100% of foundational facts while wall-clock decay suffers amnesia.
  3. LongMemEval tests demonstrate 0% split-brain hallucination on mutated facts via directed `SUPERSEDES` filtering.
  4. Full ablation tables quantify the marginal contribution of U-PPR, CATD, Grace Period, and Dynamic Intent RRF.

**Plans**:
- [x] 03-01: Build longitudinal simulation harness (100 multi-session conversations with fact mutations and transient logs).
- [x] 03-02: Run comparative Scaffolding Test: CATD vs. Wall-clock exponential decay over simulated 90 days.
- [x] 03-03: Run LongMemEval Knowledge Update evaluation suite for `SUPERSEDES` validation.
- [x] 03-04: Run component ablations (U-PPR vs. static PPR, Grace Period variations $N=1, 2, 4, 8$).

---

### Phase 4: LaTeX Manuscript Preparation & arXiv Pre-Print Submission
**Goal**: Author the complete publication-grade research manuscript in LaTeX using the standard NeurIPS/ICLR format, compile camera-ready figures, and submit to arXiv.  
**Depends on**: Phase 1, Phase 3  
**Requirements**: PAPER-01, PAPER-02, PAPER-03, PAPER-04  
**Success Criteria**:
  1. Self-contained LaTeX paper compiles error-free with `.bbl` bibliography.
  2. High-resolution TikZ / SVG vector architecture figures visualize Waking/Dreaming states and U-PPR spreading activation.
  3. All empirical tables (LoCoMo results, SCDP retention curves, ablations) are formatted to publication standards.
  4. Pre-print bundle uploaded and registered on arXiv (`cs.AI` primary, `cs.CL` secondary).

**Plans**:
- [x] 04-01: Set up LaTeX document repository (`neurips_2026.sty`, `references.bib`, KaTeX math definitions).
- [x] 04-02: Render professional vector figures (Dual-Brain architecture, Spreading Activation, Centrality curves).
- [x] 04-03: Write full paper sections (Abstract, Intro, Related Work, Methods, Empirical Setup, Results, Ablations, Conclusion).
- [x] 04-04: Compile final PDF, verify typesetting, and prepare arXiv submission package.

---

### Phase 5: Closed-Loop Downstream LLM Generation QA Benchmark
**Goal**: Evaluate downstream generative QA accuracy across LoCoMo questions by feeding retrieved contexts to a local LLM (`qwen2.5vl:7b` / `gemma4:12b` via Ollama) and computing Token F1, Exact Match (EM), and ROUGE-L.  
**Depends on**: Phase 1, Phase 4  
**Requirements**: GEN-01, GEN-02, GEN-03  
**Success Criteria**:
  1. Automated closed-loop runner executes across stratified LoCoMo questions for Dense Vector, BM25, and EpiGraph.
  2. Measures Token F1, EM, and ROUGE-L with strict zero-shot evaluation protocols.
  3. Demonstrates that EpiGraph's higher retrieval recall translates into statistically superior downstream generation F1.

**Plans**:
- [x] 05-01: Build closed-loop generation evaluator `run_closed_loop_qa.py` connecting Ollama LLM to retrieved contexts.
- [x] 05-02: Execute closed-loop QA benchmark and log results to `results/closed_loop_qa_results.json`.
- [x] 05-03: Format results into Table 3 of `paper/main.tex`.

---

### Phase 6: LongMemEval Knowledge Update & Contradiction Resolution
**Goal**: Construct and evaluate a multi-session knowledge mutation benchmark to test directed `SUPERSEDES` edge filtering against outdated fact citation.  
**Depends on**: Phase 1, Phase 2  
**Requirements**: KUPD-01, KUPD-02  
**Success Criteria**:
  1. 50 multi-session conversational episodes with mutating preferences (e.g., location, tech stack, dietary constraints).
  2. Measures Outdated Fact Citation Rate (Split-Brain Hallucination %).
  3. Proves EpiGraph achieves $< 2\%$ hallucination rate vs. $> 35\%$ for flat vector search.

**Plans**:
- [x] 06-01: Build knowledge update test harness `run_knowledge_update_eval.py`.
- [x] 06-02: Run comparative benchmark: Flat Vector vs. BM25 vs. EpiGraph `SUPERSEDES` filtering.
- [x] 06-03: Save results to `results/knowledge_update_results.json` and document in paper.

---

### Phase 7: Hyperparameter Sensitivity Landscape & Embedding Invariance
**Goal**: Perform systematic sensitivity analysis on PageRank damping ($d$) and RRF smoothing ($k$), and verify invariance across embedding backbones.  
**Depends on**: Phase 1  
**Requirements**: SENS-01, SENS-02  
**Success Criteria**:
  1. Multi-parameter grid search across $d \in [0.65, 0.95]$ and $k \in [20, 100]$.
  2. Generate 300 DPI publication plot `paper/figures/fig5_sensitivity_analysis.png`.
  3. Document stability margins in `paper/main.tex`.

**Plans**:
- [x] 07-01: Implement parameter sweep harness `run_sensitivity_analysis.py`.
- [x] 07-02: Generate sensitivity contour/line plot and save to `paper/figures/fig5_sensitivity_analysis.png`.

---

### Phase 8: Manuscript Integration & Extended Camera-Ready Package
**Goal**: Integrate all new empirical results (Downstream QA, Knowledge Updates, Sensitivity) into `paper/main.tex`, update BibTeX, and run final automated verification.  
**Depends on**: Phase 5, Phase 6, Phase 7  
**Requirements**: PAPER-05  
**Success Criteria**:
  1. `paper/main.tex` updated with complete Downstream QA and Knowledge Update tables.
  2. All figures referenced and verified with 0 hallucinations via `verify_hallucinations.py`.
  3. Git committed and tagged `v2.0-milestone2`.

**Plans**:
- [x] 08-01: Update `paper/main.tex` with downstream QA and knowledge mutation sections.
- [x] 08-02: Update `verify_hallucinations.py` to cover all new metrics and run full verification.
- [x] 08-03: Commit and freeze milestone release.
