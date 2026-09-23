# Required Skills, Competencies, and Technology Stack for EpiGraph

Executing the research, implementation, empirical validation, and publication of the **EpiGraph** paper on arXiv requires a multidisciplinary skill set spanning network science, distributed systems, modern LLM context engineering, and academic publication.

---

## 1. Mathematical & Theoretical Competencies

### 1.1 Network Science & Graph Theory
- **Random Walks & Markov Chains**: Mastery of stationary probability distributions, transition probability matrices, power iteration convergence criteria, and Personalized PageRank (PPR) formulation.
- **Community Detection & Modularity**: Understanding greedy modularity optimization (Louvain algorithm), resolution parameters, and the newer Leiden algorithm (resolving Louvain's disconnected community defect).
- **Network Centrality & Topology**: Degree centrality, eigenvector centrality, PageRank, betweenness centrality, and topological entropy (Shannon diversity of typed edges).

### 1.2 Information Retrieval & Rank Aggregation
- **Reciprocal Rank Fusion (RRF)**: Theoretical rationale for ordinal rank combination over score normalization (handling scale incomparability between vector distances and BM25 scores).
- **Approximate Nearest Neighbor (ANN) Search**: HNSW graph theory (multi-layer skip-list graph traversal, parameter trade-offs between $M$, $efConstruction$, and $efSearch$).
- **Information Retrieval Metrics**: Precision@K, Recall@K, Mean Reciprocal Rank (MRR), Normalized Discounted Cumulative Gain (NDCG@K), and multi-hop path reconstruction accuracy.

### 1.3 Neurobiological Learning Metaphors
- **Synaptic Plasticity & Hebbian Learning**: Formulating usage-dependent edge reinforcement rules ($\Delta W_{ij} \propto \text{co-activation}$).
- **Synaptic Homeostasis & Forgetting Curves**: Ebbinghaus decay, consolidation-activated pruning, and balancing stability vs. plasticity (resolving the plastic-stability dilemma).

---

## 2. Systems, Databases & Engineering Competencies

| Layer | Technology | Key Competencies Required |
| :--- | :--- | :--- |
| **Fast Document & Index Store** | **Redis Stack (RedisJSON + RediSearch)** | - Writing JSON documents (`JSON.SET`)<br>- Configuring HNSW vector indexes with `VECTOR_RANGE` and `KNN`<br>- Tuning BM25 schema weights on text fields<br>- Redis Sorted Sets (`ZADD`, `ZRANGEBYSCORE`) for the DedupRegistry |
| **Relational & Topological Store** | **Neo4j / Memgraph** | - Complex Cypher query optimization (`MERGE`, `DETACH DELETE`)<br>- Neo4j Graph Data Science (GDS) library: executing native in-memory PageRank and Louvain algorithms<br>- Directed temporal relationships (`-[:SUPERSEDES {timestamp}]->`) |
| **Distributed Messaging & Decoupling** | **Redis Streams** | - Consumer groups (`XGROUP CREATE`, `XREADGROUP`)<br>- Fault-tolerant processing with `XPENDING` and `XCLAIM`<br>- Dead Letter Queue (DLQ) pattern for dual-write failure isolation |
| **Data Processing & Clustering** | **Python, NumPy, Scikit-learn, NetworkX** | - High-performance vectorized cosine distance matrices via BLAS/LAPACK<br>- DBSCAN / HDBSCAN clustering for fuzzy entity resolution<br>- In-memory graph manipulation and topology profiling |

---

## 3. LLM Orchestration & Context Engineering Competencies

### 3.1 Strict Schema Extraction
- **Instructor + Pydantic v2**: Defining robust schemas for typed knowledge extraction:
  - `EntityNode(name, type, aliases)`
  - `FactNode(subject, predicate, object, confidence, decay_class, timestamp)`
  - `RelationshipEdge(source, target, relation_type, confidence)`
- **Prompt Engineering**: Designing the high-signal "Golden Prompt" (*"Would a DIFFERENT agent in a FUTURE conversation benefit from knowing this?"*) to prevent episodic noise pollution.
- **Lightweight Triage Routing**: Constructing fast-path binary filters (e.g., Claude 3 Haiku / Gemini 1.5/2.0 Flash) to drop uninformative turns before triggering costly schema extraction.

### 3.2 Dynamic Context Compilation
- **Dynamic Intent Routing**: Implementing embedding prototype classifiers to dynamically adjust RRF leg weights ($w_{\text{vec}}, w_{\text{graph}}, w_{\text{bm25}}$) based on query semantics.
- **Context Window Packing (Knapsack Optimization)**: Assembling multi-hop community summaries, top-ranked facts, and foundational "God Nodes" into an LLM context prompt within strict token budgets ($B \le 4000$ tokens).
- **Active Temporal Invalidation**: Ensuring nodes with active incoming `SUPERSEDES` links are pruned during prompt compilation to prevent agent hallucinations.

---

## 4. Empirical Evaluation & Research Competencies

### 4.1 Benchmark Integration & Harnessing
- Scripting automated evaluation harnesses for:
  - **HotpotQA & 2WikiMultiHopQA**: Evaluating multi-hop graph retrieval accuracy.
  - **LongMemEval (ICLR 2025)**: Running the 500-question multi-session test suite (Information Extraction, Knowledge Updates, Multi-Session Reasoning).
  - **MemoryArena**: Hooking up the agent memory pipeline to the interactive decision-making environment.

### 4.2 Statistical Significance & Ablation Profiling
- Conducting paired $t$-tests and McNemar's tests to establish $p < 0.01$ statistical significance over baseline architectures.
- Designing component ablations: evaluating the marginal contribution of U-PPR, CATD, Grace Period, and Quad-Leg RRF.

---

## 5. Academic Writing & arXiv Publishing Competencies

- **LaTeX & Overleaf**: Writing clean, publication-grade LaTeX using official standard templates (`neurips_2026.sty` or `iclr2026.sty`).
- **Figure Generation**: Creating professional vector diagrams (TikZ, draw.io SVG, or matplotlib) illustrating the Dual-Brain architecture, the Waking/Dreaming cycles, and the U-PPR spreading activation.
- **arXiv Submission Workflow**: Compiling self-contained `.tex` bundles with `.bbl` bibliographies, choosing the optimal primary category (`cs.AI` - Artificial Intelligence) and secondary categories (`cs.CL` - Computation and Language, `cs.IR` - Information Retrieval).
