# Roadmap: EpiGraph

## Overview

EpiGraph transitions from mathematical formulation and local algorithmic validation on the LoCoMo benchmark to a distributed, production-grade memory system and peer-reviewed arXiv pre-print. The roadmap spans 4 distinct phases: local algorithmic validation (completed), distributed dual-store scaling, longitudinal evaluation & ablations, and LaTeX manuscript preparation for arXiv submission.

## Phases

- [x] **Phase 1: Local Algorithmic Engine & LoCoMo Benchmark Validation** - Core graph algorithms, baselines, and empirical validation across 496 LoCoMo questions.
- [ ] **Phase 2: Distributed Dual-Store & Ingestion Reliability** - Redis Stack (HNSW) + Neo4j (GDS) dual-brain integration mediated by Redis Streams with incremental deduplication.
- [ ] **Phase 3: Longitudinal SCDP Simulation & Ablation Suite** - 100-session synthetic longitudinal simulation, God Node emergence tracking, CATD scaffolding retention tests, and ablation profiling.
- [ ] **Phase 4: LaTeX Manuscript Preparation & arXiv Pre-Print Submission** - Publication-grade LaTeX paper compilation (`neurips_2026.sty`), TikZ vector architecture diagrams, and arXiv submission to `cs.AI` / `cs.CL`.

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
- [ ] 02-01: Implement Redis Stack adapter with RedisJSON documents and RediSearch HNSW indexing.
- [ ] 02-02: Implement Neo4j GDS driver with Cypher queries for directed `SUPERSEDES` and `CORROBORATES` edges.
- [ ] 02-03: Implement Redis Streams ingestion worker with retry logic and Dead Letter Queue.
- [ ] 02-04: Implement incremental HNSW + DBSCAN entity deduplication for the background Dreaming worker.

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
- [ ] 03-01: Build longitudinal simulation harness (100 multi-session conversations with fact mutations and transient logs).
- [ ] 03-02: Run comparative Scaffolding Test: CATD vs. Wall-clock exponential decay over simulated 90 days.
- [ ] 03-03: Run LongMemEval Knowledge Update evaluation suite for `SUPERSEDES` validation.
- [ ] 03-04: Run component ablations (U-PPR vs. static PPR, Grace Period variations $N=1, 2, 4, 8$).

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
- [ ] 04-01: Set up LaTeX document repository (`neurips_2026.sty`, `references.bib`, KaTeX math definitions).
- [ ] 04-02: Render professional vector figures (Dual-Brain architecture, Spreading Activation, Centrality curves).
- [ ] 04-03: Write full paper sections (Abstract, Intro, Related Work, Methods, Empirical Setup, Results, Ablations, Conclusion).
- [ ] 04-04: Compile final PDF, verify typesetting, and prepare arXiv submission package.
