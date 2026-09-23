# Mathematical Formulation: EpiGraph (Usage-Modulated Cognitive Memory Graph)

## 1. Graph Definition and State Space

Let the agentic memory system be represented as a time-evolving, directed, typed, attributed knowledge-and-episodic multigraph:

$$\mathcal{G}(t) = (\mathcal{V}(t), \mathcal{E}(t), \mathbf{W}(t), \mathbf{\Phi}, \mathbf{\mathcal{T}})$$

where:
- $\mathcal{V}(t) = \{v_1, v_2, \dots, v_{|\mathcal{V}|}\}$ is the set of memory nodes at discrete consolidation epoch or continuous time $t$. Nodes are partitioned into semantic types:
  $$\mathcal{V} = \mathcal{V}_{\text{entity}} \cup \mathcal{V}_{\text{fact}} \cup \mathcal{V}_{\text{preference}} \cup \mathcal{V}_{\text{goal}} \cup \mathcal{V}_{\text{skill}}$$
- $\mathcal{E}(t) \subseteq \mathcal{V}(t) \times \mathcal{V}(t) \times \mathcal{R}$ is the set of directed, typed relationships with relation types $\mathcal{R} = \{\text{RELATED\_TO}, \text{ABOUT}, \text{USES}, \text{SUPERSEDES}, \text{CORROBORATES}, \text{CAUSES}\}$.
- $\mathbf{W}(t): \mathcal{E}(t) \to \mathbb{R}^+$ is the dynamic edge weight function representing topological and usage-derived affinity.
- $\mathbf{\Phi}: \mathcal{V}(t) \to \mathbb{R}^d$ is the feature mapping associating each node with a normalized dense semantic embedding vector $\mathbf{x}_v \in \mathbb{R}^d$ ($d = 1024$, e.g., Amazon Titan v2 or text-embedding-3-large).
- $\mathbf{\mathcal{T}}: \mathcal{V}(t) \to \mathbb{R}^+$ associates each node with its temporal metadata: creation timestamp $t_{\text{create}}(v)$, last access timestamp $t_{\text{access}}(v)$, access count $n_{\text{access}}(v)$, and consolidation age $k_{\text{cycle}}(v)$.

---

## 2. Dynamic Usage Plasticity and Edge Weighting

Standard graph retrieval methods (e.g., HippoRAG) use static edge weights derived solely from extraction frequency or semantic co-occurrence. In **EpiGraph**, edge weights follow an activity-dependent plasticity rule inspired by neurobiological spike-timing and Hebbian learning: *"Nodes that are co-retrieved and co-utilized by the agent reinforce their relational synapse."*

For an edge $e_{ij} = (v_i, v_j, r) \in \mathcal{E}$, its weight $W_{ij}(t)$ is formulated as:

$$W_{ij}(t) = \alpha \cdot S_{\text{semantic}}(v_i, v_j) + \beta \cdot U_{ij}(t) + \gamma \cdot R_{\text{type}}(r)$$

where:
1. **Semantic Prior**: $S_{\text{semantic}}(v_i, v_j) = \max\left(0, \frac{\mathbf{x}_i \cdot \mathbf{x}_j}{\|\mathbf{x}_i\| \|\mathbf{x}_j\|}\right)$
2. **Relation Coefficient**: $R_{\text{type}}(r)$ assigns structural priors (e.g., $R_{\text{SUPERSEDES}} = 2.0$, $R_{\text{CORROBORATES}} = 1.5$, $R_{\text{RELATED\_TO}} = 1.0$).
3. **Dynamic Usage Affinity**:
   $$U_{ij}(t) = \sum_{k=1}^{M_{ij}(t)} \exp\left(-\lambda_{\text{access}} \cdot (t - t_k)\right)$$
   where $\{t_k\}_{k=1}^{M_{ij}(t)}$ are the timestamps of conversational episodes wherein both $v_i$ and $v_j$ were simultaneously retrieved, injected into the agent context, and yielded successful task execution.

---

## 3. Usage-Modulated Personalized PageRank (U-PPR) & "God Node" Centrality

To dynamically identify foundational nodes—the structural "God Nodes" or core identity hubs—and prevent context displacement, we define the **Usage-Modulated Personalized PageRank (U-PPR)**.

### 3.1 Transition Probability Matrix
Let $\mathbf{A}(t) \in \mathbb{R}^{|\mathcal{V}| \times |\mathcal{V}|}$ be the adjacency matrix with entries $A_{ij}(t) = W_{ij}(t)$. The row-normalized transition matrix $\mathbf{P}(t)$ is defined as:

$$P_{ij}(t) = \frac{A_{ij}(t)}{\sum_{k} A_{ik}(t)} \quad \text{if } \sum_{k} A_{ik}(t) > 0, \quad \text{else } \frac{1}{|\mathcal{V}|}$$

### 3.2 Dynamic Personalization Teleportation Vector
Unlike traditional PageRank which teleports uniformly ($\mathbf{p} = \frac{1}{N}\mathbf{1}$), or static query-based PPR which only teleports to query seed entities, EpiGraph's teleportation distribution $\mathbf{p}(q, t)$ fuses **query relevance** with **usage intensity**:

$$p_i(q, t) = \theta \cdot \frac{\text{sim}(\mathbf{x}_q, \mathbf{x}_i)}{\sum_{j} \text{sim}(\mathbf{x}_q, \mathbf{x}_j)} + (1 - \theta) \cdot \frac{\log(1 + n_{\text{access}}(v_i)) \cdot \exp(-\mu (t - t_{\text{access}}(v_i)))}{\sum_{j} \log(1 + n_{\text{access}}(v_j)) \cdot \exp(-\mu (t - t_{\text{access}}(v_j)))}$$

where:
- $\mathbf{x}_q \in \mathbb{R}^d$ is the embedding of the incoming user query.
- $\theta \in [0, 1]$ balances immediate query specificity with historical epistemic utility.

### 3.3 Convergence Equation
The stationary probability distribution vector $\mathbf{\pi}^*(q, t) \in \mathbb{R}^{|\mathcal{V}|}$ satisfies the fixed-point equation:

$$\mathbf{\pi}^*(q, t) = (1 - d) \cdot \mathbf{p}(q, t) + d \cdot \mathbf{P}(t)^\top \mathbf{\pi}^*(q, t)$$

where $d \in (0, 1)$ is the damping factor (empirically set to $d = 0.85$). 
The closed-form solution is:

$$\mathbf{\pi}^*(q, t) = (1 - d) \left( \mathbf{I} - d \mathbf{P}(t)^\top \right)^{-1} \mathbf{p}(q, t)$$

Solved iteratively via power iteration in $K \le 20$ steps:
$$\mathbf{\pi}^{(k+1)} = d \mathbf{P}^\top \mathbf{\pi}^{(k)} + (1 - d) \mathbf{p}$$

### 3.4 Definition of "God Nodes" (Epistemic Macro-Hubs)
A node $v_i \in \mathcal{V}$ is classified as an **Epistemic Macro-Hub ("God Node")** at time $t$ if:

$$\mathcal{H}_{\text{macro}}(t) = \left\{ v_i \in \mathcal{V} \;\middle|\; \pi_{\text{global}}^*(v_i, t) \ge \mu_{\pi} + 2\sigma_{\pi} \quad \text{and} \quad \text{deg}_{\text{out}}(v_i) \ge \tau_{\text{deg}} \right\}$$

where $\mathbf{\pi}_{\text{global}}^*(t)$ is computed with uniform personalization $\mathbf{p} = \frac{1}{|\mathcal{V}|} \mathbf{1}$. These hubs represent persistent invariants of the agent's environment (e.g., user identity, primary project repositories, permanent architectural constraints).

---

## 4. Multi-Level Community Navigation & Context Engineering

To perform scalable multi-hop search across millions of nodes without exponential expansion, EpiGraph employs a **Two-Tier Community-to-Node Routing** mechanism:

### 4.1 Community Partitioning
During the offline "Dreaming" consolidation cycle, the graph is partitioned into non-overlapping communities $\mathcal{C} = \{C_1, C_2, \dots, C_K\}$ by maximizing modularity $Q$ via the Louvain or Leiden algorithm:

$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

Each community $C_k$ is assigned an **abstract semantic centroid** $\mathbf{c}_k$ and a synthetic **Macro-Summary** $S_k$:
$$\mathbf{c}_k = \frac{1}{|C_k|} \sum_{v \in C_k} \mathbf{x}_v$$

### 4.2 Leg 2: Hierarchical Multi-Hop Traversal Algorithm
Given query $q$:
1. **Community Filtering**: Compute similarity between query vector $\mathbf{x}_q$ and community centroids:
   $$Sim(q, C_k) = \frac{\mathbf{x}_q \cdot \mathbf{c}_k}{\|\mathbf{x}_q\| \|\mathbf{c}_k\|}$$
   Select the top-$K_{\text{comm}}$ candidate communities ($\mathcal{C}_{\text{active}}$).
2. **Seed Injection**: Find the top-$M$ entry nodes inside $\mathcal{C}_{\text{active}}$ via cosine similarity and BM25 exact match.
3. **Constrained Spreading Activation**: Run local U-PPR restricted to the induced subgraph $G[\mathcal{C}_{\text{active}} \cup \mathcal{H}_{\text{macro}}]$.
4. **Temporal Contradiction Filtering**: Prune traversed nodes that possess an active incoming `SUPERSEDES` edge:
   $$\text{Valid}(v) = \begin{cases} \text{False}, & \exists u \in \mathcal{V} \text{ such that } (u, v, \text{SUPERSEDES}) \in \mathcal{E} \text{ and } t_{\text{create}}(u) > t_{\text{create}}(v) \\ \text{True}, & \text{otherwise} \end{cases}$$

---

## 5. Consolidation-Activated Topology Decay (CATD)

### 5.1 The Scaffolding Problem in Temporal Decay
Conventional agent memory applies exponential decay to all facts based on wall-clock time:
$$S_{\text{confidence}}(t) = S_0 \cdot \exp(-\lambda \Delta t)$$
**Failure Mode**: Foundational knowledge (e.g., architectural choices made 6 months ago, user allergies) that is rarely queried decays and gets evicted, destroying the agent's structural foundation ("amnesia").

### 5.2 The CATD Formulation
In **Consolidation-Activated Topology Decay (CATD)**, decay occurs **strictly during offline consolidation cycles (dreaming)** and is governed by the node's **topological load-bearing weight**:

$$\text{Score}_{\text{topology}}(v) = w_1 \cdot \tilde{\pi}_{\text{global}}^*(v) + w_2 \cdot M(v) + w_3 \cdot D_{\text{edge}}(v)$$

where:
- $\tilde{\pi}_{\text{global}}^*(v) \in [0, 1]$ is the min-max normalized global PageRank score.
- $M(v) = \frac{\sum_{u \in C(v)} W_{uv}}{\sum_{w \in \mathcal{V}} W_{vw}}$ measures intra-community cohesion.
- $D_{\text{edge}}(v) = -\sum_{r \in \mathcal{R}} p(r|v) \log_2 p(r|v)$ is the Shannon entropy of edge types incident to $v$ (edge diversity).
- Weights are set to $w_1 = 0.4, w_2 = 0.3, w_3 = 0.3$.

The effective retention half-life $\tau(v)$ is modulated by its topology score:

$$\tau(v) = \tau_{\text{base}}(\text{type}(v)) \cdot \exp\left(\kappa \cdot \text{Score}_{\text{topology}}(v)\right)$$

### 5.3 Active Forgetting & Pruning Condition with Grace Period
A node $v$ is physically pruned from the graph and vector index if and only if:

$$\begin{aligned}
&1. \quad k_{\text{cycle}}(v) > N_{\text{grace}} \quad \text{(Cold-start grace period, e.g., } N=4 \text{ cycles)} \\
&2. \quad \text{Score}_{\text{topology}}(v) < \theta_{\text{topology\_floor}} \\
&3. \quad n_{\text{access}}(v) = 0 \text{ within window } \Delta T_{\text{dormant}} \\
&4. \quad v \notin \mathcal{H}_{\text{macro}}
\end{aligned}$$

---

## 6. Quad-Leg Reciprocal Rank Fusion (RRF) with Dynamic Routing

Let the 4 retrieval legs return ordered candidate lists:
- $\mathcal{L}_1$: Dense Vector Retrieval via Redis HNSW ($\mathbf{r}_1$)
- $\mathcal{L}_2$: Topological U-PPR Multi-Hop Traversal via Neo4j ($\mathbf{r}_2$)
- $\mathcal{L}_3$: Sparse BM25 Keyword Matching via RediSearch ($\mathbf{r}_3$)
- $\mathcal{L}_4$: System-2 Agentic Multi-Hop Tool Fallback ($\mathbf{r}_4$, activated if $\max \text{score}(\mathcal{L}_1) < \delta_{\text{conf}}$)

For any memory candidate $d \in \bigcup_{i=1}^4 \mathcal{L}_i$:

$$\text{Score}_{\text{RRF}}(d) = \sum_{i=1}^4 \frac{w_i(q)}{k + r_i(d)}$$

where:
- Smoothing constant $k = 60$.
- Rank $r_i(d) \in \{1, 2, \dots, K\}$; if $d \notin \mathcal{L}_i$, $r_i(d) = \infty \implies \frac{w_i}{k + \infty} = 0$.
- **Dynamic Intent-Based Weight Vector** $\mathbf{w}(q) = [w_{\text{vec}}, w_{\text{graph}}, w_{\text{bm25}}, w_{\text{agentic}}]^\top$ is derived from query intent classification:
  $$\mathbf{w}(q) = \text{Softmax}\left(\mathbf{W}_{\text{intent}} \cdot \mathbf{x}_q + \mathbf{b}_{\text{intent}}\right)$$
  - Relational/Associative queries boost $w_{\text{graph}} \to 0.55$.
  - Factoid/Identifier queries boost $w_{\text{bm25}} \to 0.45$.
  - Conceptual queries boost $w_{\text{vec}} \to 0.55$.
