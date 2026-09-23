# Research Notes: EpiGraph Architecture & Theoretical Synthesis

## 1. The Dual-Brain Architectural Paradigm

EpiGraph divides agent memory processing into two distinct operational regimes:

```
           [STREAMING CHAT TRANSCRIPT]
                       │
                       ▼
       ┌───────────────────────────────┐
       │   WAKING INGESTION (Fast)     │
       │ • Triage binary filter        │
       │ • Pydantic schema extraction  │
       │ • L0 Ingestion KNN dedup      │
       └───────────────┬───────────────┘
                       │ Redis Streams (XREADGROUP / DLQ)
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────────┐          ┌──────────────────┐
│  Redis LTM Store │          │   Neo4j Graph    │
│ • RedisJSON docs │          │ • Entities/Turns │
│ • HNSW (1024d)   │          │ • Typed Edges    │
│ • BM25 Index     │          │ • SUPERSEDES DAG │
└──────────────────┘          └──────────────────┘
        ▲                             ▲
        └──────────────┬──────────────┘
                       │
       ┌───────────────┴───────────────┐
       │   DREAMING CONSOLIDATION      │
       │ • Louvain community detection │
       │ • U-PPR centrality & Hubs     │
       │ • CATD Synaptic Pruning       │
       │ • Incremental HNSW+DBSCAN     │
       └───────────────────────────────┘
```

---

## 2. Core Mathematical Formulations

### 2.1 Dynamic Hebbian Edge Plasticity
For any directed edge $e_{ij} = (v_i, v_j, r) \in \mathcal{E}$, its edge weight evolves dynamically based on agent usage:
$$W_{ij}(t) = \alpha \cdot \cos(\mathbf{x}_i, \mathbf{x}_j) + \beta \sum_{k=1}^{M_{ij}(t)} \exp\left(-\lambda_{\text{access}}(t - t_k)\right) + \gamma \cdot R_{\text{type}}(r)$$

### 2.2 Usage-Modulated Personalized PageRank (U-PPR)
The transition matrix $\mathbf{P}(t)$ is formed by row-normalizing $W_{ij}(t)$. The personalization vector $\mathbf{p}(q, t)$ blends semantic query relevance with historical access intensity:
$$p_i(q, t) = \theta \cdot \frac{\text{sim}(\mathbf{x}_q, \mathbf{x}_i)}{\sum_j \text{sim}(\mathbf{x}_q, \mathbf{x}_j)} + (1 - \theta) \cdot \frac{\log(1 + n_{\text{access}}(v_i)) \cdot \exp(-\mu(t - t_{\text{access}}(v_i)))}{\sum_j \log(1 + n_{\text{access}}(v_j)) \cdot \exp(-\mu(t - t_{\text{access}}(v_j)))}$$

Stationary distribution converges via:
$$\mathbf{\pi}^*(q, t) = (1 - d)\left(\mathbf{I} - d \mathbf{P}(t)^\top\right)^{-1} \mathbf{p}(q, t)$$

### 2.3 Epistemic Macro-Hubs ("God Nodes")
Nodes satisfying:
$$\mathcal{H}_{\text{macro}}(t) = \left\{ v_i \in \mathcal{V} \;\middle|\; \pi_{\text{global}}^*(v_i, t) \ge \mu_\pi + 1.2\sigma_\pi \quad \text{and} \quad \text{deg}(v_i) \ge 3 \right\}$$
These nodes represent cognitive invariants (user identity, core preferences, overarching system constraints) that act as gravitational anchors during multi-hop retrieval.

### 2.4 Consolidation-Activated Topology Decay (CATD)
Decay occurs **strictly during offline consolidation cycles (dreaming)** based on topological load-bearing weight:
$$\text{Score}_{\text{topology}}(v) = 0.4 \cdot \tilde{\pi}_{\text{global}}^*(v) + 0.3 \cdot M(v) + 0.3 \cdot D_{\text{edge}}(v)$$
- Protected by a cold-start grace period ($N_{\text{grace}} \ge 4$ cycles).
- Physical eviction occurs only if $\text{Score}_{\text{topology}}(v) < \theta_{\text{floor}}$, $n_{\text{access}} = 0$, and $v \notin \mathcal{H}_{\text{macro}}$.

### 2.5 Intent-Routed Quad-Leg Reciprocal Rank Fusion
$$\text{RRF}(d) = \sum_{i=1}^4 \frac{w_i(q)}{60 + r_i(d)}$$
where $\mathbf{w}(q) = [w_{\text{vec}}, w_{\text{graph}}, w_{\text{bm25}}, w_{\text{agentic}}]^\top$ is dynamically adjusted based on query intent classification.
