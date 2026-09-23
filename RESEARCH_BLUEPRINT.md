# Master Research Blueprint: EpiGraph for arXiv Publication

This blueprint synthesizes the architectural discussion from the chat (`https://share.gemini.google/UySHkKqGOkJr`), formalizes the user's novel memory concept, outlines the required competencies, maps the validation datasets, and establishes the end-to-end execution roadmap to publish an academic paper on arXiv.

---

## 1. Executive Summary & Chat Synthesis

In the foundational discussion, an enterprise **Hierarchical Hybrid Memory System for AI Agents** was designed to overcome the core bottlenecks of current retrieval architectures:

```
+-----------------------------------------------------------------------------------+
|                           THE EPIGRAPH DUAL-BRAIN ARCHITECTURE                    |
+-----------------------------------------------------------------------------------+
|  [WAKING STATE: Fast-Path Stream & Ingestion]                                     |
|  Raw Chat (JSONL) -> Triage Classifier -> Claude 3 + Instructor Extraction         |
|  -> Ingestion L0 KNN Dedup (>0.95 cos sim bumps access count)                     |
|  -> Redis Streams (XREADGROUP / XPENDING / DLQ) Dual-Write                        |
|        |                                        |                                 |
|        v                                        v                                 |
|  [Redis LTM Store]                        [Neo4j Topological Graph]               |
|  - RedisJSON Documents                    - Entity & Fact Nodes                   |
|  - HNSW Dense Vector (Titan v2 1024d)     - Typed Directed Edges                  |
|  - RediSearch BM25 Keyword Index          - SUPERSEDES & CORROBORATES Links       |
+-----------------------------------------------------------------------------------+
|  [DREAMING STATE: Offline Consolidation Cycle (e.g., Every 6 Hours)]               |
|  - Incremental HNSW + DBSCAN Dedup (resolving O(n^2) scaling timebomb)            |
|  - Louvain / Leiden Community Partitioning & Centroid Fingerprinting              |
|  - Usage-Modulated Personalized PageRank (U-PPR) Recalculation                    |
|  - Identification of Epistemic Macro-Hubs ("God Nodes")                          |
|  - Consolidation-Activated Topology Decay (CATD) with N-Cycle Grace Period        |
|  - Multi-tier Active Pruning (Confidence Floor + Low Centrality + Orphan Sweep)    |
+-----------------------------------------------------------------------------------+
|  [RETRIEVAL & CONTEXT ENGINEERING: Quad-Leg Dynamic Parallel Search]              |
|  Query -> Dynamic Intent Router (Vector / Graph / BM25 weights)                   |
|        |--> Leg 1: Redis HNSW (Top 30 Dense Neighbors)                            |
|        |--> Leg 2: Neo4j 2-Tier Community Walk + Local U-PPR                      |
|        |--> Leg 3: RediSearch BM25 (Top 20 Exact Keyword Matches)                 |
|        +--> Leg 4: System-2 Agentic Tool Fallback (if conf < 0.75)                |
|        |                                                                          |
|        v                                                                          |
|  Reciprocal Rank Fusion (RRF with k=60) -> Cohere Neural Re-rank (Top 20)         |
|  -> Temporal Contradiction Filtering (Drop nodes with active incoming SUPERSEDES) |
|  -> Strict Token Budget Context Packing into LLM Agent Prompt                     |
+-----------------------------------------------------------------------------------+
```

---

## 2. The Core Scientific Novelty: The User's Concept Formalized

The user's vision connects network science, usage dynamics, and context engineering:
> *"The way I was thinking is to enable some sort of page ranking setup on top of the graph where the graph is created based on the user conversation with the agent, such as the nodes and edges... based on the usage or retrieval of the node, you have some sort of page ranking to make a god node or communities behind the graph to help in navigating and analyzing what the user needs are by the agent on its own agentic memory by doing multi-hop search and then trying to fetch proper information into the agent memory. Context engineering plus agent memory..."*

### 2.1 The Four Scientific Innovations of This Paper
1. **Dynamic Usage Plasticity ($W_{ij}(t)$)**:
   Unlike HippoRAG or Microsoft GraphRAG where edges are static, edge weights in EpiGraph dynamically strengthen through Hebbian co-retrieval and task utility over time.
2. **Epistemic Macro-Hubs ("God Nodes") via U-PPR**:
   Personalized PageRank dynamically promotes high-centrality, cross-session anchors (user core identity, foundational architecture, critical preferences). These hubs serve as gravitational anchors during multi-hop search, preventing context displacement.
3. **Two-Tier Community-to-Node Context Engineering**:
   Scalable multi-hop search routes first through Louvain community centroids, zoom into local semantic neighborhoods, and traverse usage-reinforced paths to compile optimal, token-budgeted prompt contexts.
4. **Consolidation-Activated Topology Decay (CATD)**:
   Synaptic homeostasis where decay is strictly tied to offline consolidation cycles and topological load-bearing weight ($0.4 \times \text{PageRank} + 0.3 \times \text{Modularity} + 0.3 \times \text{Edge Diversity}$), solving the "Scaffolding Amnesia" problem of temporal forgetting.

---

## 3. Required Competency Matrix

To implement, evaluate, and write this paper, the following four pillars are required:

| Competency Area | Essential Skills | Tools & Frameworks |
| :--- | :--- | :--- |
| **Network Science** | Random walks, Personalized PageRank, Louvain/Leiden modularity, graph centrality, Markov convergence. | NetworkX, Neo4j Graph Data Science (GDS), SciPy / NumPy |
| **Distributed Systems** | Vector indexing, HNSW tuning, BM25 text search, event streams, consumer groups, atomic transactions. | Redis Stack (RedisJSON, RediSearch), Redis Streams, Neo4j Cypher |
| **Context Engineering & LLMs** | Schema extraction, Pydantic validation, dynamic intent classification, prompt token knapsack packing. | Instructor, LiteLLM, Claude 3.5 Sonnet / Gemini API |
| **Empirical Benchmarking & Writing** | Multi-hop QA evaluation, long-context conversational testing, LaTeX typesetting, statistical hypothesis testing. | LongMemEval harness, HotpotQA scripts, Overleaf, Matplotlib |

*(See full details in `REQUIRED_SKILLS_AND_TECH_STACK.md`)*

---

## 4. Test Datasets & Validation Suite

Validation addresses both static retrieval accuracy and dynamic conversational usage:

### 4.1 Static Multi-Hop Verification
- **HotpotQA**: Validates 2-hop bridge entity discovery via U-PPR.
- **2WikiMultiHopQA**: Validates explicit reasoning path reconstruction.
- **MuSiQue**: Validates deep 3-hop / 4-hop relational traversal.

### 4.2 Dynamic Conversational & Usage Verification
- **LongMemEval (ICLR 2025)**: Evaluates the 5 essential abilities:
  1. *Information Extraction* (buried facts in 100k+ token histories)
  2. *Multi-Session Reasoning* (connecting facts across sessions)
  3. *Knowledge Updates* (testing the directed `SUPERSEDES` mechanism against obsolete facts)
  4. *Temporal Reasoning* (timestamped sequences)
  5. *Abstention* (resisting hallucinations)
- **Multi-Session Chat (MSC)**: Measures persona retention and consistency across 5+ human-agent sessions.
- **MemoryArena (2026)**: Evaluates memory as an active decision prior in closed-loop agent environments.
- **Simulated Continuous Deployment Protocol (SCDP)**: 100-session synthetic longitudinal stress test verifying God Node emergence, scaffolding retention, and zero memory leaks.

*(See full details in `EVALUATION_AND_BENCHMARKS.md`)*

---

## 5. End-to-End Execution Roadmap for arXiv Publication

```
+----------------------------------------------------------------------------+
|                          FOUR-PHASE PUBLICATION ROADMAP                    |
+----------------------------------------------------------------------------+

  Phase 1: Formalization & Reference Implementation (Weeks 1–2)
  ├── Lock mathematical definitions (U-PPR, CATD, Community Centroids).
  ├── Implement standalone Python prototype:
  │   ├── InMemory / Neo4j Graph with typed edges & dynamic weight tensor.
  │   ├── Redis HNSW + BM25 mock/live hybrid search.
  │   ├── U-PPR power iteration solver.
  │   └── CATD consolidation simulator with grace period.
  └── Build unit test suite verifying convergence and Scaffolding Preservation.

  Phase 2: Benchmark Integration & Empirical Experimentation (Weeks 3–4)
  ├── Run HotpotQA & MuSiQue baselines:
  │   └── Compare EpiGraph vs. Dense RAG vs. HippoRAG vs. GraphRAG.
  ├── Run LongMemEval benchmark suite:
  │   └── Measure Knowledge Update accuracy (SUPERSEDES validation).
  │   └── Measure Multi-Session Reasoning F1 score.
  ├── Run 100-Session Longitudinal Simulation (SCDP):
  │   └── Log God Node centrality emergence curves.
  │   └── Plot CATD retention rate vs. baseline exponential decay.
  └── Collect ablation data: U-PPR vs. static PPR, Grace Period variations.

  Phase 3: LaTeX Drafting & Visualization (Weeks 5–6)
  ├── Draft paper using NeurIPS/ICLR LaTeX template.
  ├── Render high-resolution TikZ / SVG architecture diagrams.
  ├── Generate empirical performance curves & ablation tables.
  └── Formalize mathematical theorems (convergence of U-PPR, CATD bound).

  Phase 4: Pre-Print Release & Community Dissemination (Week 7)
  ├── Package self-contained arXiv submission bundle (TeX + figures + BBL).
  ├── Upload to arXiv under cs.AI (primary), cs.CL, cs.IR (secondary).
  ├── Open-source GitHub repository with reproducibility scripts & benchmark data.
  └── Submit to target peer-reviewed venue (NeurIPS / ICLR).
+----------------------------------------------------------------------------+
```
