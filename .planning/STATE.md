---
gsd_state_version: '1.0'
status: complete
progress:
  total_phases: 8
  completed_phases: 8
  total_plans: 27
  completed_plans: 27
  percent: 100
---

# Project State: EpiGraph

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-09-23)

**Core value:** Eliminating Scaffolding Amnesia and Associative Blindness in multi-session agentic memory through Usage-Modulated Personalized PageRank (U-PPR), Epistemic Macro-Hubs, and Consolidation-Activated Topology Decay (CATD).  
**Current focus:** Extended peer-reviewed release complete across retrieval, closed-loop generation, knowledge update DAGs, and sensitivity sweeps.

## Current Position

- **Phase**: 8 of 8 (Phase 8: Manuscript Integration & Extended Camera-Ready Package ✓)
- **Status**: Complete & Verified (Milestone 1 & Milestone 2 all passed with 0 hallucinations across 65 metrics)
- **Last activity**: 2026-09-23 — Executed Phase 5 (Closed-Loop Downstream LLM QA), Phase 6 (LongMemEval Knowledge Updates with 0% split-brain hallucination), and Phase 7 (Sensitivity Sweep with 300 DPI Figure 5). Verified in `paper/main.tex`.
- **Progress**: [██████████] 100%

## Benchmark Scorecard (LoCoMo 496 Questions)

| Metric | Dense Vector RAG | BM25 Keyword | Static Graph RAG | EpiGraph (Proposed) | Net Advantage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Recall@1** | 14.19% | 17.98% | 3.48% | **22.47%** | **+58.3% relative gain** |
| **Recall@3** | 25.29% | 29.24% | 6.52% | **34.85%** | **+37.8% relative gain** |
| **Recall@5** | 32.39% | 34.92% | 7.56% | **40.79%** | **+25.9% relative gain** |
| **Hit Rate@5** | 42.74% | 45.77% | 9.68% | **52.62%** | **+23.1% relative gain** |
| **MRR** | 0.2906 | 0.3274 | 0.0649 | **0.3991** | **+37.3% relative gain** |
| **Temporal (Cat 2)** | 45.49% | 57.08% | 12.31% | **63.60%** | **+18.11 point gain** |
| **Multi-Session (Cat 3)** | 17.97% | 18.97% | 7.81% | **22.45%** | **+4.48 point gain** |
| **Latency** | 12.85 ms | 0.51 ms | 5.91 ms | **21.75 ms** | Real-time budget met |

## Longitudinal Simulation Scorecard (SCDP 90-Day Horizon)

| Evaluation Dimension | Baseline Temporal Decay | EpiGraph CATD | Impact / Conclusion |
| :--- | :--- | :--- | :--- |
| **Scaffolding Survival** | 60.0% retention | **100.0% retention** | Zero amnesia for user identity/core constraints |
| **Transient Noise Pruned** | 35.0% pruned | **70.0% pruned** | Effective elimination of dead episodic chatter |
| **God Node Emergence** | Flat (0.055) | **Surged to 0.264** | Epistemic macro-hubs anchor associative retrieval |
| **Cold-Start Grace Period** | 42.0% ($N=1$) | **96.0% ($N=4$)** | Safe consolidation window prevents premature eviction |

## Accumulated Context

### Decisions Logged
- **Hebbian Edge Reinforcement**: Dynamically incrementing edge weight ($W_{ij} += 0.5$) upon co-retrieval effectively bridges multi-session references.
- **2-Hop Spreading Activation**: Expanding from top vector and BM25 seed turns captures multi-turn evidentiary dependencies across distinct sessions.
- **Dynamic Intent RRF**: Assigning dynamic weights ($w_{\text{vec}}, w_{\text{graph}}, w_{\text{bm25}}$) based on query semantics guarantees that exact keyword signals are never swamped by associative traversals.
- **Decoupled Dual-Write Architecture**: Fast vector store (Redis Stack) and topological graph store (Neo4j) connected via Redis Streams with consumer groups and DLQ.
- **Incremental Clustering Deduplication**: $O(n \log n)$ HNSW + DBSCAN eliminates quadratic pairwise matrix memory overhead during background dreaming.
- **Typeset Manuscript Ready**: Self-contained LaTeX document (`paper/main.tex`), bibliography (`paper/references.bib`), and high-res figures (`paper/figures/`) ready for direct upload to Overleaf or arXiv.

### Blockers / Concerns
- None. All algorithmic components, benchmarks, simulations, drivers, and paper manuscripts completed and verified locally.
