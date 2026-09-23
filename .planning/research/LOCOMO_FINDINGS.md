# Research Notes: LoCoMo Benchmark Findings

## 1. Experimental Overview

The **LoCoMo** (Long-term Conversational Memory) benchmark (Mahbub et al., SNAP Research) evaluates conversational memory across very long, multi-session human-curated dialogues. Each conversation spans up to 35 independent sessions, containing ~300 dialogue turns and averaging 9,000 tokens.

We evaluated 4 memory architectures across all 10 multi-session conversations, testing 496 question-answering evaluation pairs:
- **Baseline 1: Dense Vector RAG** (`sentence-transformers/all-MiniLM-L6-v2`)
- **Baseline 2: BM25 Keyword Search** (Okapi BM25, $k_1=1.5, b=0.75$)
- **Baseline 3: Static Graph RAG** (HippoRAG-style static Knowledge Graph + static Personalized PageRank)
- **Proposed: EpiGraph** (Dynamic Cognitive Graph + U-PPR + Epistemic Macro-Hubs + 2-Hop Spreading Activation + Dynamic Intent RRF)

---

## 2. Key Empirical Findings

### 2.1 Why EpiGraph Wins on Temporal Reasoning (+18.11% over Vector RAG)
In Category 2 (Temporal Reasoning), queries ask about dates, chronological sequences, and relative timing:
- *Query Example*: *"When did Caroline go to the LGBTQ support group?"*
- *Ground Truth Evidence (`D1:3`)*: *"I went to a LGBTQ support group yesterday and it was so powerful."*
- *Session Context*: Session 1 occurred on `8 May, 2023`.
- *Answer*: `7 May 2023`.

**Failure Mode of Vector RAG**: Dense vector models match on semantic similarity. The sentence contains *"yesterday"*, but does not contain *"May"*, *"2023"*, or *"8th"*. Vector search fails to link the relative utterance to the session timestamp.

**EpiGraph Solution**: EpiGraph anchors every turn node to its session node (`SESSION_PRECEDES`, `CONTAINS_TURN`) with timestamp metadata. During retrieval, U-PPR spreads activation from the query entities to the timestamped session anchor and the adjacent turns, yielding a **63.60% Recall@5** (compared to 45.49% for Vector RAG).

### 2.2 Why EpiGraph Wins on Multi-Session Reasoning (Category 3)
In Category 3, evidence turns are separated across distinct sessions:
- *Query Example*: *"Would Caroline still want to pursue counseling as a career if she hadn't received support growing up?"*
- *Evidence*: `['D4:15', 'D3:5']` (Turn 15 in Session 4, and Turn 5 in Session 3).

**Failure Mode of Vector RAG**: Vector search returns one isolated turn that matches the query terms, but misses the cross-session bridge turn.

**EpiGraph Solution**: In EpiGraph, entities (`counseling`, `support`, `transition`) act as bridges connecting turns across sessions. When `D4:15` is activated, U-PPR traverses the shared entity node and pulls `D3:5` into the candidate context, yielding a **22.45% Recall@5** (compared to 17.97% for Vector RAG and 7.81% for Static Graph RAG).

### 2.3 Why Static Graph RAG Fails in Conversational Memory (3.48% Recall@1, 7.56% Recall@5)
Static Graph RAG (like HippoRAG) was designed for static Wikipedia paragraphs where OpenIE extracts clean subject-predicate-object triples. In natural conversations:
1. Dialogues are full of conversational chatter, pronouns (*"I"*, *"you"*, *"we"*), and ellipses.
2. Static OpenIE triples miss the rich contextual subtleties of conversational utterances.
3. Without dense vector fallback or BM25 keyword fusion, static PPR on conversational entities suffers from massive noise dilution.

EpiGraph solves this by maintaining a **hybrid multi-leg fusion**: BM25 grounds exact entity mentions, dense vectors capture semantic intent, and U-PPR traverses the structural graph topology.
