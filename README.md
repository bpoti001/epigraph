# EpiGraph: Dynamic Usage-Weighted Topology and Synaptic Consolidation for Multi-Hop Agentic Memory

[![Verification](https://img.shields.io/badge/Verification-67%2F67%20Checks%20Passed-brightgreen.svg)](#empirical-verification)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Benchmark](https://img.shields.io/badge/Benchmark-LoCoMo%20%7C%20LongMemEval-orange.svg)](#empirical-evaluation)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Official implementation and evaluation suite for the research paper:  
**"EpiGraph: Dynamic Usage-Weighted Topology and Synaptic Consolidation for Multi-Hop Agentic Memory"** (arXiv pre-print, `cs.AI` / `cs.CL`).

---

## 🚀 Key Theoretical Contributions

EpiGraph solves three fundamental failure modes in persistent LLM agent memory:
1. **Associative Blindness** $\rightarrow$ Solved via **Usage-Modulated Personalized PageRank (U-PPR)** and Hebbian plasticity, dynamically surfacing multi-session connections.
2. **Scaffolding Amnesia** $\rightarrow$ Solved via **Consolidation-Activated Topology Decay (CATD)**, shielding foundational persona facts and architectural invariants ($100\%$ survival over 90 days).
3. **Split-Brain Hallucination** $\rightarrow$ Solved via directed `SUPERSEDES` and `CORROBORATES` graph filtering, eliminating outdated fact citations ($0.0\%$ hallucination vs. $70.0\%$ for flat dense vector search).

---

## 🏛 Architecture: Waking vs. Dreaming Dual-Brain

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      WAKING STATE (Read/Write Reflex)                 │
 │                                                                        │
 │  User Utterance ──► Ingestion Filter ──► MiniLM Embedder ──► Streams   │
 │                                                                 │      │
 │  Query ───────────► Intent Router ────┬─► Dense Vector (HNSW)   ▼      │
 │                                        ├─► BM25 Keyword       Redis /  │
 │                                        └─► U-PPR Subgraph     Neo4j    │
 │                                                  │                     │
 │  Downstream Context ◄── Quad-Leg RRF Fusion ─────┘                     │
 └────────────────────────────────────────────────────────────────────────┘
                                      ▲
                                      │ Synchronized every 6h
                                      ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                 DREAMING STATE (Offline Synaptic Consolidation)        │
 │                                                                        │
 │  • Incremental HNSW + DBSCAN Deduplication (O(N log N))                │
 │  • Louvain Community Detection & Macro-Hub Clustering                  │
 │  • Global PageRank & Epistemic Macro-Hub ("God Node") Detection        │
 │  • CATD Topological Synaptic Pruning (with N_grace >= 4 grace period)  │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Empirical Evaluation Summary

### 1. LoCoMo Retrieval Benchmark (496 Questions, 10 Multi-Session Conversations)

| Architecture / Model | Recall@1 | Recall@3 | Recall@5 | HitRate@5 | MRR | Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Static Graph RAG** (HippoRAG-style) | 3.48% | 6.52% | 7.56% | 9.68% | 0.0649 | 5.91 ms |
| **Dense Vector RAG** (`all-MiniLM-L6-v2`) | 14.19% | 25.29% | 32.39% | 42.74% | 0.2906 | 12.85 ms |
| **BM25 Keyword** (Okapi) | 17.98% | 29.24% | 34.92% | 45.77% | 0.3274 | **0.51 ms** |
| **EpiGraph (Proposed)** | **22.47%** | **34.85%** | **40.79%** | **52.62%** | **0.3991** | 21.75 ms |
| *Relative Gain vs. Dense Vector* | **+58.3%** | **+37.8%** | **+25.9%** | **+23.1%** | **+37.3%** | *Real-time budget met* |

**LoCoMo Category Highlights**:
- **Temporal Reasoning (Cat 2)**: **63.60%** Recall@5 vs. 45.49% for Dense Vector (**+18.11 point gain**).
- **Multi-Session Reasoning (Cat 3)**: **22.45%** Recall@5 vs. 17.97% for Dense Vector (**+4.48 point gain**).

### 2. Knowledge Update & Contradiction Resolution (50 Mutation Episodes)

| Memory Architecture | Current Fact Recall | Outdated Fact Citation (Split-Brain Hallucination) |
| :--- | :---: | :---: |
| **BM25 Keyword** | 86.0% | 80.0% |
| **Dense Vector RAG** | 100.0% | 70.0% |
| **EpiGraph (`SUPERSEDES` DAG)** | **100.0%** | **0.0%** |

### 3. Asymptotic Scaling & Graph Stress Test

| Graph Size ($|V|$) | Number of Edges ($|E|$) | U-PPR Latency (ms) | Throughput (QPS) |
| :---: | :---: | :---: | :---: |
| 100 | 582 | 0.58 ms | 1,713.9 |
| 500 | 2,980 | 2.14 ms | 467.4 |
| 1,000 | 5,980 | 5.16 ms | 193.7 |
| 2,500 | 14,980 | 8.46 ms | 118.2 |
| 5,000 | 29,980 | 18.89 ms | 53.0 |
| 10,000 | 59,980 | 51.72 ms | 19.3 |

---

## 🛠 Quickstart & Reproduction

### Prerequisites
- Python 3.10+
- PyTorch with MPS / CUDA / CPU support

### Setup
```bash
git clone https://github.com/example/epigraph.git
cd epigraph
pip install -r requirements.txt
```

### Reproducing Benchmark Experiments
```bash
# 1. Run full LoCoMo benchmark (496 QA pairs across 10 conversations)
python run_locomo_benchmark.py

# 2. Run 90-day SCDP longitudinal simulation & generate publication figures
python run_longitudinal_simulation.py

# 3. Run Knowledge Update & Contradiction Resolution benchmark
python run_knowledge_update_eval.py

# 4. Run Closed-Loop Downstream LLM QA evaluation (requires Ollama running qwen2.5vl:7b)
python run_closed_loop_qa.py

# 5. Run Hyperparameter Sensitivity Grid Sweep
python run_sensitivity_analysis.py

# 6. Run Graph Scaling Stress Test
python run_scaling_benchmark.py
```

### Automated Hallucination Verification
To mathematically verify that every metric in `paper/main.tex` strictly matches the raw JSON logs:
```bash
python verify_hallucinations.py
```

---

## 📦 Distributed Infrastructure (Redis Stack + Neo4j GDS)

Launch the dual-store background services via Docker Compose:
```bash
docker compose up -d
```
- **Redis Stack**: Port `6379` (RedisJSON documents, RediSearch HNSW vector indices, Redis Streams).
- **Neo4j Enterprise**: Port `7474` (HTTP) / `7687` (Bolt) with Graph Data Science (GDS) library enabled for native Cypher PageRank and Louvain queries.

---

## 📄 Citation

```bibtex
@article{epigraph2026,
  title   = {EpiGraph: Dynamic Usage-Weighted Topology and Synaptic Consolidation for Multi-Hop Agentic Memory},
  author  = {Potineni, Bhavyateja and Giri, Lohit and Kutsyy, Vadim and Pentakota, Rajasekhar},
  journal = {arXiv preprint arXiv:2609.xxxxx},
  year    = {2026}
}
```
