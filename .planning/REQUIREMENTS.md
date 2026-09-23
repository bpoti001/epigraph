# Requirements: EpiGraph

**Defined:** 2026-09-23  
**Core Value:** Eliminating Scaffolding Amnesia and Associative Blindness in multi-session agentic memory through Usage-Modulated Personalized PageRank (U-PPR), Epistemic Macro-Hubs, and Consolidation-Activated Topology Decay (CATD).

## v1 Requirements (Initial Release & Validation)

### Core Algorithmic Engine

- [x] **CORE-01**: Embedding engine with in-memory caching supporting batch inference via `all-MiniLM-L6-v2` on MPS/CPU.
- [x] **CORE-02**: Okapi BM25 indexer with configurable $k_1=1.5$ and $b=0.75$, tokenization, and IDF weighting.
- [x] **CORE-03**: Dynamic Cognitive Graph with typed nodes (`turn`, `entity`, `speaker`, `session_anchor`) and directed edges.
- [x] **CORE-04**: Hebbian usage plasticity dynamically reinforcing co-activated edge weights ($W_{ij} += 0.5$) upon retrieval.
- [x] **CORE-05**: Usage-Modulated Personalized PageRank (U-PPR) balancing query seed vectors with usage recency and intensity.
- [x] **CORE-06**: Epistemic Macro-Hub ("God Node") classification via centrality distribution thresholding ($\pi^*(v) \ge \mu + 1.2\sigma, \text{deg} \ge 3$).
- [x] **CORE-07**: Consolidation-Activated Topology Decay (CATD) with $N$-cycle cold-start grace period ($N=4$).
- [x] **CORE-08**: Dynamic Intent Router classifying temporal and relational queries, coupled with Quad-Leg Reciprocal Rank Fusion ($k=60$).

### Empirical Benchmarking Suite

- [x] **BENCH-01**: Automated LoCoMo benchmark runner ingesting multi-session conversations from `data/locomo/locomo10.json`.
- [x] **BENCH-02**: Baseline 1: Standard Flat Dense Vector RAG implementation.
- [x] **BENCH-03**: Baseline 2: Pure Okapi BM25 keyword search implementation.
- [x] **BENCH-04**: Baseline 3: HippoRAG-style Static Knowledge Graph RAG with static PPR.
- [x] **BENCH-05**: Full evaluation across 496 questions spanning 10 multi-session conversations with category breakdowns (Recall@K, HitRate@5, MRR, Latency).

## v2 Requirements (Distributed Scaling & Paper Release)

### Distributed Storage & Ingestion

- [ ] **DIST-01**: Production Redis Stack driver (RedisJSON + RediSearch HNSW) supporting sub-millisecond vector querying.
- [ ] **DIST-02**: Neo4j Graph Data Science (GDS) enterprise integration with Cypher transactional batching and Louvain projections.
- [ ] **DIST-03**: Redis Streams dual-write queue (`XREADGROUP`, `XPENDING`, retry up to 3 times, Dead Letter Queue).
- [ ] **DIST-04**: Incremental K-NN deduplication & clustering (HNSW + DBSCAN) replacing $O(n^2)$ pairwise matrix.

### Longitudinal & Ablation Studies

- [ ] **EVAL-01**: 100-Session Simulated Continuous Deployment Protocol (SCDP) logging God Node emergence curves.
- [ ] **EVAL-02**: Scaffolding retention stress test: CATD vs. Wall-clock exponential decay over 90 simulated days.
- [ ] **EVAL-03**: LongMemEval (ICLR 2025) test harness validating directed `SUPERSEDES` temporal contradiction filtering.
- [ ] **EVAL-04**: Component ablation analysis (U-PPR vs. static PPR, impact of Grace Period $N=1, 2, 4, 8$).

### Academic Publication & Dissemination

- [ ] **PAPER-01**: Full LaTeX manuscript using NeurIPS/ICLR formatting template (`neurips_2026.sty`).
- [ ] **PAPER-02**: Professional vector diagrams (TikZ / SVG) illustrating the Dual-Brain Waking/Dreaming workflow and U-PPR spreading activation.
- [ ] **PAPER-03**: Empirical results tables and LaTeX plots rendering LoCoMo and SCDP curves.
- [ ] **PAPER-04**: Compile self-contained arXiv submission bundle with `.bbl` bibliography and submit to `cs.AI` / `cs.CL`.

## Traceability Matrix

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 - CORE-08 | Phase 1: Local Engine & LoCoMo Validation | Completed ✓ |
| BENCH-01 - BENCH-05 | Phase 1: Local Engine & LoCoMo Validation | Completed ✓ |
| DIST-01 - DIST-04 | Phase 2: Distributed Storage & Scale | Pending |
| EVAL-01 - EVAL-04 | Phase 3: Longitudinal & Ablation Suite | Pending |
| PAPER-01 - PAPER-04 | Phase 4: arXiv Manuscript & Publication | Pending |

**Coverage:**
- Total Requirements: 21
- Completed: 13 (61.9%)
- Active / In Progress: 8 (38.1%)
- Unmapped: 0 ✓
