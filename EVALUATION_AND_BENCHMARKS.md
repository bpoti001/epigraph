# Empirical Evaluation Suite: Benchmarks, Datasets, and Validation Protocols

To rigorously validate **EpiGraph** for an arXiv submission, the evaluation suite must evaluate two complementary dimensions:
1. **Static Multi-Hop Retrieval & Reasoning**: Verifying structural graph traversal and association across disparate factual nodes.
2. **Dynamic Usage-Driven Multi-Session Evolution**: Verifying that dynamic usage plasticity, "God Node" hub formation, temporal contradiction handling, and Consolidation-Activated Topology Decay (CATD) maintain long-term coherence across repeated, evolving user interactions.

---

## 1. Static Multi-Hop Retrieval Benchmarks

These benchmarks establish that EpiGraph's topological graph traversal outperforms standard dense vector search and matches or exceeds static graph baselines (like HippoRAG and Microsoft GraphRAG) on multi-hop question answering.

| Benchmark | Characteristics & Scale | Metric | Primary Purpose in Paper |
| :--- | :--- | :--- | :--- |
| **HotpotQA** (Yang et al.) | 113k QA pairs requiring 2-hop reasoning over Wikipedia paragraphs (Distractor & Fullwiki splits). | Recall@K, Precision@K, F1, EM | Validates associative multi-hop leap between bridge entities without intermediate LLM queries. |
| **2WikiMultiHopQA** (Ho et al.) | 192k QA pairs with structured reasoning paths and explicit evidentiary triples. | Path Reconstruction Accuracy, Answer F1 | Validates that graph traversal faithfully follows true relational pathways rather than hallucinated semantic shortcuts. |
| **MuSiQue** (Trivedi et al.) | 25k 2-to-4 hop complex reasoning questions designed to minimize single-hop "cheating." | Multi-hop Exact Match, BLEU-4 | Stress-tests deep (3-hop, 4-hop) relational traversal through community clusters. |
| **MultiHop-RAG** (Tang et al., 2024) | Benchmark specifically evaluating RAG systems on multi-document cross-referencing. | NDCG@10, Hit Rate@5 | Tests Quad-Leg RRF fusion against raw dense vector baselines. |

---

## 2. Dynamic Multi-Session Conversational Benchmarks

These datasets validate the memory pipeline from the **usage and conversational life-cycle perspective** over long interaction histories.

| Benchmark | Source / Conference | Key Abilities Tested | Relevance to EpiGraph Architecture |
| :--- | :--- | :--- | :--- |
| **LongMemEval** | ICLR 2025 (Wu et al.) | 1. Information Extraction<br>2. Multi-Session Reasoning<br>3. Knowledge Updates<br>4. Temporal Reasoning<br>5. Abstention | Directly benchmarks EpiGraph's **Knowledge Update** via directed `SUPERSEDES` edges and **Multi-Session Reasoning** via community clustering. |
| **LongMemEval-V2** | ICML 2026 | Long-horizon agentic task memory in complex multi-modal environments. | Evaluates persistence of procedural skills and preferences across 50+ extended sessions. |
| **Multi-Session Chat (MSC)** | Meta AI (Xu et al.) | 5 conversational sessions with human annotators expanding personas over time. | Validates conversational persona retention and prevention of "context displacement." |
| **LoCoMo** | Mahbub et al. (2024) | Long-term conversational memory with explicit temporal event graphs. | Evaluates temporal event ordering and timestamped graph consolidation during the "Dreaming" cycle. |

---

## 3. Agentic & Dynamic Usage Evaluation ("The Usage Point of View")

Traditional static benchmarks cannot evaluate how an agent's memory actively adapts to **user feedback, retrieval frequency, and decision loops**. To validate this core novelty, we implement two dynamic frameworks:

### 3.1 MemoryArena (2026 Benchmark)
- **Concept**: Evaluates agentic memory as a *decision prior* in closed-loop multi-session environments.
- **Tasks**: Preference-constrained planning, sequential task execution, multi-day coding workflows.
- **Evaluation**: Compares task completion rate when the agent's memory graph is reinforced by usage plasticity ($U_{ij}(t)$) versus static memory baselines.

### 3.2 The Simulated Continuous Deployment Protocol (SCDP)
To simulate an enterprise agent deployment over an accelerated 90-day timeline:
- **Corpus Generation**: Synthesize 100 conversational sessions per simulated user persona across 4 distinct domains (Software Engineering, Financial Planning, Smart Home, Healthcare).
- **Session Types**:
  1. *Core Setup (Sessions 1–10)*: User establishes core identity, project repositories, constraints ("I am allergic to peanuts", "Always use strict TypeScript").
  2. *Transient Episodes (Sessions 11–70)*: Daily debugging logs, ephemeral error codes, temporary travel bookings.
  3. *Fact Mutations (Sessions 71–85)*: User updates previous state ("I changed my company from TechCorp to CloudScale AI", "Upgrade Python to 3.12").
  4. *Recall & Long-Horizon Multi-Hop Queries (Sessions 86–100)*: Queries requiring synthesis of Session 3 core identity + Session 75 mutation + Session 92 project status.

---

## 4. Targeted Probing & Ablation Experiments

To satisfy the rigorous peer-review standards of arXiv and top-tier AI venues (NeurIPS/ICLR/ACL), the paper must feature 4 targeted diagnostic experiments:

### Experiment 1: The "God Node" / Macro-Hub Emergence Test
- **Hypothesis**: Activity-dependent plasticity ($W_{ij}(t)$) and U-PPR will naturally promote foundational user preferences and core architectural entities into the macro-hub set $\mathcal{H}_{\text{macro}}$, while transient noise remains in the low-centrality periphery.
- **Metric**: Gini coefficient of graph centrality; Precision@K of $\mathcal{H}_{\text{macro}}$ matching the ground-truth core persona attributes.

### Experiment 2: Scaffolding Retention Test (CATD vs. Wall-Clock Decay)
- **Hypothesis**: In the presence of hundreds of transient intermediate interactions, baseline temporal exponential decay ($e^{-\lambda \Delta t}$) will erroneously prune foundational architectural facts. CATD, by measuring topological load-bearing weight ($0.4 \times \pi^* + 0.3 \times M + 0.3 \times D$), will preserve foundational scaffolding with zero amnesia.
- **Comparison**:
  - Baseline A: No Decay (Monotonic growth $\implies$ OOM & index latency degradation).
  - Baseline B: Access-only Decay ($e^{-\lambda \Delta t}$ with access count reset).
  - Baseline C: EpiGraph CATD with Grace Period ($N=4$ dreaming cycles).
- **Metric**: Foundational Recall Rate vs. Graph Node Count over 90 simulated days.

### Experiment 3: Dynamic Contradiction Resolution (`SUPERSEDES` Invalidation)
- **Hypothesis**: Traversal that filters nodes possessing active incoming `SUPERSEDES` edges will achieve near 100% precision on mutated state queries, completely eliminating the split-brain hallucination common to dense vector stores.
- **Metric**: Mutation Accuracy on LongMemEval Knowledge Update split.

### Experiment 4: Multi-Hop Traversal Efficiency & Latency Profiling
- **Comparison**:
  1. Flat Dense Vector Search (Redis HNSW alone)
  2. Unconstrained Multi-Hop Graph Traversal (breadth-first 3-hop)
  3. Static HippoRAG (Single-step PPR)
  4. EpiGraph Two-Tier Routing (Louvain Community Centroid $\to$ Seed Nodes $\to$ Local U-PPR $\to$ Quad-Leg RRF)
- **Metrics**: End-to-End Latency (ms), Token Budget Consumed, Answer Hit Rate@10, Hallucination Rate.
