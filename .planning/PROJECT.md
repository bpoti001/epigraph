# EpiGraph: Hierarchical Hybrid Memory System for Autonomous AI Agents

## What This Is

EpiGraph is a biologically inspired, production-grade memory architecture and research project designed to provide long-term, multi-session coherence for autonomous AI agents. By coupling low-latency streaming ingestion ("Waking State") with an asynchronous topological consolidation cycle ("Dreaming State"), EpiGraph replaces flat vector memory and static knowledge graphs with an activity-dependent, self-tuning cognitive graph.

## Core Value

Eliminating **Scaffolding Amnesia** (the accidental erasure of foundational user identity and architectural constraints) and **Associative Blindness** (the failure to traverse multi-hop cross-session relational paths) through Usage-Modulated Personalized PageRank (U-PPR), Epistemic Macro-Hubs ("God Nodes"), and Consolidation-Activated Topology Decay (CATD).

## Requirements

### Validated (Completed in Phase 1)
- [x] **CORE-01**: In-memory caching dense semantic vector embedding engine (`sentence-transformers/all-MiniLM-L6-v2` on MPS/CPU).
- [x] **CORE-02**: High-performance Okapi BM25 inverted indexer ($k_1=1.5, b=0.75$) with lexical scoring.
- [x] **CORE-03**: Dynamic Cognitive Graph with Hebbian usage plasticity ($W_{ij}$ edge reinforcement on co-retrieval).
- [x] **CORE-04**: Usage-Modulated Personalized PageRank (U-PPR) balancing query seed relevance with historical usage intensity and access recency.
- [x] **CORE-05**: Epistemic Macro-Hub ("God Node") detection via centrality thresholding ($\pi^*(v) \ge \mu + 1.2\sigma, \text{deg} \ge 3$).
- [x] **CORE-06**: Consolidation-Activated Topology Decay (CATD) with $N$-cycle cold-start grace period.
- [x] **CORE-07**: Dynamic Intent Router with Quad-Leg Reciprocal Rank Fusion ($k=60$).
- [x] **BENCH-01**: Automated LoCoMo benchmark harness running across 10 multi-session conversations (496 questions).
- [x] **BENCH-02**: Baseline implementations (Dense Vector RAG, BM25, HippoRAG-style Static Graph RAG).
- [x] **BENCH-03**: Quantitative validation proving EpiGraph outperforms Dense Vector RAG (+58.3% Recall@1, +25.9% Recall@5, +37.3% MRR, +18.11 point gain on Temporal Reasoning).

### Active (Phase 2 & Phase 3)
- [ ] **DIST-01**: Distributed Redis Stack driver (RedisJSON + RediSearch HNSW 1024d vectors) with atomic dual-write mediated by Redis Streams (`XREADGROUP`, `XPENDING`, DLQ).
- [ ] **DIST-02**: Neo4j Graph Data Science (GDS) enterprise integration with Cypher transactional batching and Louvain community projections.
- [ ] **DIST-03**: Incremental K-NN deduplication & clustering (HNSW + DBSCAN) replacing $O(n^2)$ pairwise similarity.
- [ ] **BENCH-04**: 100-Session Longitudinal Simulation (SCDP) demonstrating God Node emergence curves and CATD scaffolding survival over 90 simulated days.
- [ ] **BENCH-05**: LongMemEval (ICLR 2025) benchmark runner testing directed `SUPERSEDES` contradiction resolution and multi-session reasoning.
- [ ] **PAPER-01**: Publication-grade LaTeX manuscript (`neurips_2026.sty`) with TikZ architecture figures and empirical results tables.
- [ ] **PAPER-02**: Pre-print release and submission to arXiv (`cs.AI`, `cs.CL`, `cs.IR`).

### Out of Scope
- Direct fine-tuning of embedding weights (we operate over frozen embedding spaces to preserve zero-shot generalizability).
- Monolithic single-database architectures (sacrifices either graph traversal efficiency or vector sub-millisecond indexing).
- Destructive deletion of historical user facts (mutations must use directed `SUPERSEDES` DAGs to preserve audit trails).

## Context

- **Source Architecture**: Architectural blueprint discussed in [Gemini Chat f6OE9ofGkK0e](https://share.gemini.google/UySHkKqGOkJr).
- **Primary Workspaces**: `/Users/tejap/memory_paper`
- **Current Milestone**: Validation Phase complete with empirical proof on LoCoMo; entering Distributed Scaling and Manuscript Compilation.

## Constraints

- **Latency**: End-to-end P95 retrieval latency must remain $< 50\text{ ms}$ on local machines and $< 100\text{ ms}$ over network clusters.
- **Compute**: Must execute on commodity CPU and Apple Silicon MPS without requiring high-cost multi-GPU clusters.
- **Reliability**: Dual-write operations must guarantee eventual consistency via Redis Streams without split-brain corruption.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dual-Brain Architecture (Redis + Neo4j) | Combines sub-millisecond vector indexing with deep multi-hop relational graph traversals. | ✓ Validated |
| Usage-Modulated Personalized PageRank (U-PPR) | Standard static PageRank treats graph as frozen; U-PPR dynamically updates centrality based on real-time task utility. | ✓ Validated |
| CATD with Grace Period over Wall-Clock Decay | Prevents the erasure of foundational user identity and architecture simply because they are not mentioned daily. | ✓ Validated |
| Reciprocal Rank Fusion (RRF with $k=60$) | Replaces unnormalized score addition to solve the score incomparability problem across vector distances and BM25 scores. | ✓ Validated |
| Dedicated Git Repository in `/Users/tejap/memory_paper` | Isolates project version control from parent directories. | ✓ Validated |

---
*Last updated: 2026-09-23 after LoCoMo benchmark completion and GSD initialization*
