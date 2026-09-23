# Literature Review: State-of-the-Art in Agentic Memory Systems (2024–2026)

## 1. Introduction & Taxonomy of Agentic Memory

The rapid scaling of Large Language Models (LLMs) has revealed fundamental limitations in handling long-horizon, multi-session agentic workflows. While context windows have expanded (e.g., 1M+ tokens in Gemini 1.5/2.0), models suffer from quadratic attention compute costs, the **"Lost-in-the-Middle" phenomenon**, attention dilution, and the inability to maintain persistent identity and factual consistency across independent execution sessions.

To address these challenges, the academic and industrial landscape has transitioned through four distinct evolutionary paradigms:

```
Era 1: Flat Vector RAG (2022-2023)
[Dense Vector Embeddings] --> [Cosine Similarity Top-K] --> [Context Injection]
   Problems: Semantic noise, no multi-hop reasoning, no structural hierarchy, flat amnesia.

Era 2: OS-Style Virtual Memory (2023-2024)
[MemGPT / Letta] --> [Main Context (RAM) vs. Archival (Disk)] --> [Explicit Tool Calls / Paging]
   Problems: Rigid paging boundaries, lack of associative graph navigation, high tool-calling overhead.

Era 3: Static Graph-Augmented RAG (2024-2025)
[HippoRAG, Microsoft GraphRAG] --> [Static KG Extraction] --> [Leiden Summaries / Static PPR]
   Problems: Built for static document corpora; cannot adapt to dynamic, conversational usage feedback; no forgetting/pruning.

Era 4: Dynamic Usage-Plasticity & Consolidation (2025-2026 - EpiGraph)
[Hierarchical Hybrid Graph] --> [Dynamic Usage-Modulated PPR] --> [Consolidation-Activated Topology Decay (CATD)]
   Advantages: Self-tuning centrality ("God Nodes"), Hebbian reinforcement, load-bearing forgetting, multi-hop context engineering.
```

---

## 2. In-Depth Comparative Analysis of Leading Paradigms

### 2.1 OS-Inspired Memory: MemGPT & Letta (Packer et al., 2023/2024)
- **Core Mechanism**: Conceptualizes LLMs as an Operating System CPU. Manages memory via a strict hierarchy:
  - *Working Context (RAM)*: System instructions, core user persona, and immediate scratchpad.
  - *Recall Storage (FIFO)*: Recent conversational logs.
  - *Archival Storage (Disk)*: Vector database containing past interactions and unconstrained knowledge.
- **Strengths**: Enables unbounded conversational length through explicit paging tools (`core_memory_append`, `archival_memory_insert`, `archival_memory_search`).
- **Deficiencies & Failure Modes**:
  1. **High Tool Overhead**: Forces the LLM to actively decide when and how to page data, consuming substantial reasoning tokens and introducing failure states when the LLM forgets to call memory tools.
  2. **No Associative Multi-Hop Reasoning**: Retrieval from archival storage relies on flat vector similarity, missing cross-document relational leaps ($A \to B \to C$).
  3. **Absence of Topological Structure**: Facts have no structural relationships, making contradiction detection (`SUPERSEDES`) and identity hierarchy impossible.

### 2.2 Neurobiological Static Indexing: HippoRAG (Bernal et al., 2024)
- **Core Mechanism**: Draws direct analogy to the *Complementary Learning Systems (CLS)* neurobiological framework:
  - LLM = Neocortex (extracting structured entities and triples).
  - OpenIE Knowledge Graph + Personalized PageRank (PPR) = Hippocampus (associative indexing and rapid pattern completion).
  - Query entities serve as seed nodes; PPR spreads activation across the graph to retrieve multi-hop context in a single matrix iteration.
- **Strengths**: Outperforms iterative multi-hop RAG (like DSPy or self-ask) on complex QA (HotpotQA, 2WikiMultiHopQA) with zero intermediate LLM calls.
- **Deficiencies & Failure Modes**:
  1. **Static Corpus Assumption**: HippoRAG is designed as an offline indexer for fixed text collections. It provides no mechanism for continuous streaming dialogue ingestion.
  2. **Zero Usage Plasticity**: Edge weights are static. The graph never learns from which reasoning paths the agent actually took or which facts proved useful.
  3. **No Synaptic Forgetting**: Lacks any temporal decay or active pruning. In long-running agent deployments, the graph suffers unbounded topological bloat and noise accumulation.

### 2.3 Hierarchical Global Summarization: Microsoft GraphRAG (Edge et al., 2024)
- **Core Mechanism**: Uses LLMs to extract entities, relationships, and claims from documents, followed by **Leiden community detection** to build a multi-level semantic hierarchy. High-level communities are pre-summarized by LLMs to answer global corpus-wide questions ("What are the overarching themes in this dataset?").
- **Strengths**: Resolves the "global question" failure mode of standard RAG; provides panoramic context.
- **Deficiencies & Failure Modes**:
  1. **Massive Indexing Latency & Cost**: Requires hundreds of LLM calls to generate community reports, making real-time conversational updates prohibitively expensive ($O(N)$ re-indexing).
  2. **Inflexible to Dynamic Identity**: Conversational agent memory requires granular, rapid episodic updates rather than batch-processed static macro-summaries.

### 2.4 Biological Sleep Consolidation: SCM & HiMem (2025–2026)
- **Core Mechanism**: Divides agent operation into two distinct metabolic regimes:
  - *Waking State*: Low-latency ingestion and responsive retrieval.
  - *Dreaming / NREM Sleep State*: Offline background worker that clusters memories, resolves semantic drift, and consolidates episodic episodes into semantic rules.
- **Strengths**: Eliminates heavy computation from the user-facing latency budget.
- **Deficiencies**: Most existing implementations still rely on ad-hoc LLM reflection prompts rather than formal network science metrics (e.g., modularity optimization, PageRank convergence, or formal decay theorems).

### 2.5 Practical Production Frameworks: Zep, Mem0, Cognee, A-Mem
- **Zep**: Implements a temporal knowledge graph with automated entity extraction, edge invalidation, and hybrid vector+graph search. However, ranking algorithms remain proprietary and lack formal mathematical plasticity rules.
- **Mem0 (Embedchain Memory)**: Focuses on lightweight CRUD memory for personalized chatbots. Lacks deep multi-hop graph traversal and structural community abstraction.
- **Cognee**: Implements modular deterministic pipelines converting text to Neo4j graphs with vector embeddings, but relies on static Cypher patterns rather than dynamic random walks.

---

## 3. Systematic Feature Comparison Matrix

| Dimension / Capability | MemGPT / Letta (2024) | HippoRAG (2024) | Microsoft GraphRAG (2024) | SCM / HiMem (2026) | **EpiGraph (This Work)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Data Structure** | Key-Value / Flat Vectors | OpenIE Static KG | Hierarchical Leiden KG | Clustered Vector Store | **Typed Dynamic Multi-Graph + Dual Redis/Neo4j** |
| **Multi-Hop Traversal** | ❌ None (Flat Cosine) | ✅ Static PPR (Single-Step) | ⚠️ Local Traversal Only | ❌ Multi-turn LLM chains | ✅ **Usage-Modulated PPR (U-PPR)** |
| **Dynamic Usage Plasticity** | ❌ None | ❌ None (Static weights) | ❌ None | ⚠️ Simple access counter | ✅ **Hebbian Edge/Node Plasticity ($W_{ij}(t)$)** |
| **Macro-Hub Detection** | ❌ None | ⚠️ Static Degree/PageRank | ⚠️ Leiden Communities | ❌ None | ✅ **"God Node" Centrality $\mathcal{H}_{\text{macro}}$** |
| **Contradiction Management** | ⚠️ LLM Manual Edit | ❌ None (Preserves all) | ❌ None | ⚠️ Textual Overwrite | ✅ **Directed `SUPERSEDES` Temporal DAG** |
| **Forgetting & Decay** | ⚠️ LRU / FIFO Paging | ❌ Monotonic Growth | ❌ Monotonic Growth | ⚠️ Temporal Half-Life | ✅ **Consolidation-Activated Topology Decay (CATD)** |
| **Scaffolding Protection** | ❌ Core Memory Limited | ❌ No Decay Mechanism | ❌ No Decay Mechanism | ❌ Wall-clock decays roots | ✅ **Load-Bearing Topology Weighting** |
| **Retrieval Fusion** | ❌ Single Leg | ❌ Graph PPR Only | ❌ Map-Reduce LLM | ⚠️ Vector + Recency | ✅ **Quad-Leg RRF with Intent Routing** |
| **Ingestion Complexity** | $O(1)$ write, $O(K)$ search | $O(N)$ batch indexing | $O(N^2)$ LLM summarization | $O(1)$ stream, offline dream | ✅ **$O(1)$ Stream + $O(k \log n)$ Dreaming KNN** |

---

## 4. The Scientific Gap Addressed by This Research

The comparative analysis reveals a glaring void at the intersection of **network topology**, **dynamic agent usage**, and **synaptic consolidation**:

1. **The Static Topology Fallacy**: Graph-based memory systems (HippoRAG, GraphRAG) treat graph structure as fixed. In reality, an agent's memory is a living ecosystem where the significance of a concept is a function of both its semantic connections and its **operational utility** across multi-session tasks.
2. **The Scaffolding Amnesia Problem**: Temporal decay models (exponential half-life based on wall-clock time) catastrophically erode foundational facts (user identity, core preferences, overarching system constraints) simply because they are not mentioned every day.
3. **The Multi-Hop Context Engineering Bottleneck**: Blind vector retrieval returns fragmented context chunks, while brute-force graph expansion floods the LLM context window with irrelevant neighbors. A disciplined, two-tier navigation protocol—routing through **Louvain/Leiden communities** and anchored by **Usage-Modulated "God Nodes"**—is urgently required to compile coherent, token-efficient context.
