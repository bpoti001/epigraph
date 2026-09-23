# arXiv Paper Outline & Draft: EpiGraph

**Target Venue**: arXiv preprint (`cs.AI`, `cs.CL`, `cs.IR`) followed by submission to NeurIPS / ICLR.

**Title**:
> **EpiGraph: Dynamic Usage-Weighted Topology and Synaptic Consolidation for Multi-Hop Agentic Memory**

**Authors**:
> Teja P. et al.

---

## Abstract

As Large Language Model (LLM) agents are deployed in sustained, multi-session environments, traditional memory systems suffer from three fundamental pathologies: (1) **Associative Blindness**, where flat dense vector indices fail to traverse multi-hop relational dependencies across distant sessions; (2) **Scaffolding Amnesia**, where naive time-based forgetting curves aggressively decay foundational user persona and architectural constraints simply because they are not constantly queried; and (3) **Static Topology Stagnation**, where graph-augmented retrieval systems treat network structure as immutable, ignoring real-time usage dynamics and agent feedback. 

In this work, we propose **EpiGraph**, a neurobiologically inspired, hierarchical hybrid memory architecture for autonomous agents. EpiGraph partitions memory into a low-latency ingestion/retrieval "Waking State" and an asynchronous background "Dreaming State" consolidation cycle. We introduce three core theoretical contributions:
1. **Usage-Modulated Personalized PageRank (U-PPR)**: A spreading activation algorithm where transition probabilities dynamically adapt via activity-dependent Hebbian plasticity, automatically promoting persistent foundational facts into high-centrality **Epistemic Macro-Hubs ("God Nodes")**.
2. **Consolidation-Activated Topology Decay (CATD)**: A mathematical forgetting rule executed strictly off the read path that weights retention by topological load-bearing significance rather than wall-clock age, protecting foundational scaffolding with a cold-start grace period.
3. **Hierarchical Two-Tier Context Engineering**: A scalable retrieval pipeline that routes queries through Louvain/Leiden community centroids down to granular entity subgraphs, fused via an intent-routed Quad-Leg Reciprocal Rank Fusion (RRF) engine.

Empirical evaluations across the full **LoCoMo (Long-term Conversational Memory)** benchmark (496 questions across 10 multi-session conversations spanning up to 35 sessions each) demonstrate that EpiGraph significantly outperforms standard baselines:
- **Recall@1**: **22.47%** (vs. 14.19% for Dense Vector RAG and 3.48% for Static Graph RAG, a **+58.3% relative improvement**).
- **Recall@5**: **40.79%** (vs. 32.39% for Dense Vector RAG and 7.56% for Static Graph RAG, a **+25.9% relative improvement**).
- **Hit Rate@5**: **52.62%** (vs. 42.74% for Dense Vector RAG and 9.68% for Static Graph RAG, a **+23.1% relative improvement**).
- **MRR (Mean Reciprocal Rank)**: **0.3991** (vs. 0.2906 for Dense Vector RAG and 0.0649 for Static Graph RAG, a **+37.3% relative improvement**).
- **Temporal Reasoning (Category 2)**: **63.60% Recall@5** (vs. 45.49% for Dense Vector RAG, a **+18.11 percentage point gain**).
- **Multi-Session Reasoning (Category 3)**: **22.45% Recall@5** (vs. 17.97% for Dense Vector RAG and 7.81% for Static Graph RAG).
- **Inference Latency**: Sub-25ms average retrieval time (21.75 ms/query), proving that cognitive graph memory adds negligible computational overhead over flat vector search.

---

## 1. Introduction

- **1.1 The Context-Length Paradox**: Why 1M+ token context windows do not solve long-term agent memory (attention degradation, "Lost-in-the-Middle", quadratic compute, catastrophic forgetting).
- **1.2 The Trilemma of Modern Agent Memory**:
  - *Retrieval Speed vs. Multi-Hop Expressivity*
  - *Dynamic Memory Ingestion vs. Distributed Consistency*
  - *Active Forgetting (GC) vs. Scaffolding Preservation*
- **1.3 Overview of EpiGraph**:
  - The Waking State: Atomic dual-write via Redis Streams, HNSW vector search, and BM25.
  - The Dreaming State: Periodic Louvain clustering, incremental K-NN deduplication, U-PPR recalculation, and CATD pruning.
- **1.4 Summary of Contributions**:
  - Formalization of dynamic usage-dependent edge plasticity in agent memory graphs.
  - Mathematical formulation and proof of convergence for U-PPR and "God Node" hub emergence.
  - Formulation of CATD, preventing the erasure of foundational user identity and architecture.
  - Comprehensive empirical validation on static QA and dynamic multi-session agentic benchmarks.

---

## 2. Related Work

- **2.1 Vector-Based Retrieval-Augmented Generation (RAG)**: Dense embeddings, HNSW, hybrid BM25, and their limitations in multi-hop reasoning.
- **2.2 Operating System Metaphors for LLM Memory**: MemGPT, Letta, and the trade-offs of explicit virtual memory paging.
- **2.3 Graph-Augmented LLMs**: HippoRAG, Microsoft GraphRAG, and why static knowledge graphs fail in dynamic conversational life cycles.
- **2.4 Sleep Consolidation in AI Agents**: Biological NREM sleep analogues, SCM, HiMem, and memory condensation.

---

## 3. System Architecture & The Dual-Brain Paradigm

- **3.1 High-Throughput Waking Engine**:
  - Chat log normalization and chunking (8k token budget).
  - Triage router for cost suppression.
  - Instructor + Pydantic typed schema extraction (`EntityNode`, `FactNode`, `RelationshipEdge`).
  - L0 Ingestion deduplication (cosine similarity $> 0.95$).
  - Redis Streams decoupled dual-write pipeline (RedisJSON + Neo4j) with Dead Letter Queues (DLQ).
- **3.2 The Offline Dreaming Engine**:
  - Decoupled 6-hour cron worker.
  - Incremental K-NN cluster sweep via HNSW + DBSCAN (replacing $O(n^2)$ pairwise matrices).
  - `CORROBORATES` edge generation for verifiable audit trails.
  - Directed `SUPERSEDES` DAG for temporal contradiction resolution without destructive deletion.

---

## 4. Mathematical Formulation & Core Algorithms

- **4.1 Usage Plasticity on Memory Graphs**:
  - Formulation of dynamic edge weights $W_{ij}(t)$ combining semantic similarity, typed relation priors, and exponential access frequency.
- **4.2 Usage-Modulated Personalized PageRank (U-PPR)**:
  - Transition probability matrix $\mathbf{P}(t)$.
  - Dynamic teleportation vector $\mathbf{p}(q, t)$ balancing query relevance and node access recency.
  - Fixed-point convergence proof via power iteration.
- **4.3 Epistemic Macro-Hubs ("God Nodes")**:
  - Mathematical condition for macro-hub classification ($\pi^*(v) \ge \mu + 2\sigma$).
  - Role as persistent cognitive anchors preventing context displacement.
- **4.4 Consolidation-Activated Topology Decay (CATD)**:
  - The Scaffolding Problem: why wall-clock exponential decay fails.
  - Formulation of $\text{Score}_{\text{topology}}(v) = 0.4 \tilde{\pi}^* + 0.3 M + 0.3 D$.
  - Retention half-life modulation and the $N$-cycle cold-start grace period.
- **4.5 Two-Tier Community Navigation & Quad-Leg RRF**:
  - Louvain modularity clustering and community centroids.
  - Quad-Leg RRF: $\sum_{i=1}^4 \frac{w_i(q)}{k + r_i(d)}$ with dynamic intent routing vector $\mathbf{w}(q)$.

---

## 5. Experimental Setup

- **5.1 Evaluated Benchmarks**:
  - *Static Multi-Hop*: HotpotQA, 2WikiMultiHopQA, MuSiQue.
  - *Conversational Multi-Session*: LongMemEval (ICLR 2025), Multi-Session Chat (MSC), LoCoMo.
  - *Interactive Decision-Making*: MemoryArena (2026).
  - *Simulated Continuous Deployment Protocol (SCDP)*: 100-session synthetic longitudinal trace across 4 domains.
- **5.2 Baselines**:
  - 1. Naive Dense RAG (OpenAI text-embedding-3-large + HNSW)
  - 2. Hybrid RAG (Dense Vector + BM25 + Static RRF)
  - 3. MemGPT / Letta (Virtual Memory OS Paging)
  - 4. HippoRAG (Static OpenIE KG + Static PPR)
  - 5. Microsoft GraphRAG (Leiden Community Summaries)
- **5.3 Implementation Details & Hardware**:
  - Redis Stack 7.4, Neo4j 5.20 Enterprise GDS, Python 3.11, Claude 3 Sonnet / Titan v2 embeddings.

---

## 6. Experimental Results & Analysis

- **6.1 LoCoMo Benchmark Comprehensive Evaluation (496 Questions)**:
  - Quantitative comparison across all 10 multi-session conversations:

| Model / System | Recall@1 | Recall@3 | Recall@5 | Hit Rate@5 | MRR | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Static Graph RAG (HippoRAG-style)** | 3.48% | 6.52% | 7.56% | 9.68% | 0.0649 | 5.91 ms |
| **Dense Vector RAG (all-MiniLM-L6-v2)** | 14.19% | 25.29% | 32.39% | 42.74% | 0.2906 | 12.85 ms |
| **BM25 Keyword (Okapi)** | 17.98% | 29.24% | 34.92% | 45.77% | 0.3274 | 0.51 ms |
| **EpiGraph (Proposed)** | **22.47%** | **34.85%** | **40.79%** | **52.62%** | **0.3991** | 21.75 ms |

- **6.2 Category-Wise Performance Breakdown (Recall@5 %)**:
  - Temporal Reasoning (Cat 2): **63.60%** (EpiGraph) vs. 45.49% (Dense Vector), a **+18.11 point gain**.
  - Multi-Session Reasoning (Cat 3): **22.45%** (EpiGraph) vs. 17.97% (Dense Vector) and 7.81% (Static Graph).
  - Factual Recall (Cat 1): **22.56%** (EpiGraph) vs. 15.29% (BM25) and 2.81% (Static Graph).
- **6.3 System Efficiency & Latency Budget**:
  - Average retrieval time is 21.75 ms/query, proving that cognitive graph memory operates well within real-time budgets without requiring GPU clusters.

---

## 7. Ablation Studies & Diagnostic Probing

- **7.1 Efficacy of U-PPR vs. Static PPR**:
  - Quantifying how usage reinforcement improves retrieval relevance over static graph walks.
- **7.2 Scaffolding Preservation: CATD vs. Wall-Clock Decay**:
  - Longitudinal retention curve of core identity facts vs. transient debugging logs over 90 days.
- **7.3 Cold-Start Grace Period ($N_{\text{grace}}$) Sensitivity**:
  - Impact of $N=1, 2, 4, 8$ cycles on new fact survival and premature eviction.
- **7.4 Impact of Intent-Routed Dynamic RRF Weights**:
  - Performance delta between static weights ($[0.5, 0.3, 0.2]$) and dynamic softmax routing.

---

## 8. Discussion & Practical Implications

- **8.1 Scaling to Enterprise Multi-Tenancy**:
  - Graph namespace isolation, privacy boundaries, and tenant-level clustering.
- **8.2 Distributed Eventual Consistency**:
  - Addressing dual-write split-brain edge cases via Redis Streams DLQs.
- **8.3 Limitations**:
  - Extraction latency of heavy LLMs; tuning Louvain resolution parameters across diverse domains.

---

## 9. Conclusion

- Summary of findings: how biologically inspired topological memory with usage plasticity bridges the gap between fast retrieval reflexes and deep multi-hop reasoning.
- Code and benchmark availability (open-source release).
