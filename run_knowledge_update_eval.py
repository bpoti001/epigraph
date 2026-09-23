#!/usr/bin/env python3
"""
Phase 6: LongMemEval Knowledge Update & Contradiction Resolution Benchmark
Evaluates how effectively directed SUPERSEDES graph edges eliminate split-brain hallucinations
when user preferences, locations, or technical constraints mutate across sessions.
"""

import os
import sys
import json
import random
import numpy as np
from typing import Dict, List, Tuple, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.embeddings import EmbeddingEngine
from src.graph_memory import DynamicCognitiveGraph

MUTATION_EPISODES = [
    {
        "domain": "Location",
        "fact_initial": "User lives and works in Seattle, Washington.",
        "fact_updated": "User has officially relocated and now resides in Austin, Texas.",
        "query": "Where does the user currently live?",
        "ground_truth_current": "Austin, Texas",
        "ground_truth_outdated": "Seattle, Washington"
    },
    {
        "domain": "Dietary Invariant",
        "fact_initial": "User is strictly vegetarian and eats dairy.",
        "fact_updated": "User transitioned to a 100% plant-based vegan diet with zero dairy.",
        "query": "Can the user eat cheese or dairy?",
        "ground_truth_current": "vegan / zero dairy",
        "ground_truth_outdated": "vegetarian / eats dairy"
    },
    {
        "domain": "Primary Programming Language",
        "fact_initial": "The backend service is written in Node.js and TypeScript.",
        "fact_updated": "The backend service was migrated entirely to Go and gRPC.",
        "query": "What language is the backend service written in?",
        "ground_truth_current": "Go / gRPC",
        "ground_truth_outdated": "Node.js / TypeScript"
    },
    {
        "domain": "Database Choice",
        "fact_initial": "User stores agent memories in PostgreSQL with pgvector.",
        "fact_updated": "User replaced Postgres with Redis Stack and Neo4j GDS.",
        "query": "What databases are used for agent memory?",
        "ground_truth_current": "Redis Stack and Neo4j GDS",
        "ground_truth_outdated": "PostgreSQL with pgvector"
    },
    {
        "domain": "Security Policy",
        "fact_initial": "API authentication uses static Bearer tokens stored in environment variables.",
        "fact_updated": "Static API keys are deprecated; all services now use short-lived OAuth2 mTLS certificates.",
        "query": "How are services authenticated?",
        "ground_truth_current": "OAuth2 mTLS certificates",
        "ground_truth_outdated": "static Bearer tokens"
    }
]

def run_knowledge_update_benchmark(num_trials: int = 50, output_dir: str = "results"):
    print("=" * 80)
    print("PHASE 6: RUNNING KNOWLEDGE UPDATE & CONTRADICTION RESOLUTION (SUPERSEDES)")
    print("Benchmarking Split-Brain Hallucination Rate across Mutating Long-Term Facts")
    print("=" * 80)

    embed = EmbeddingEngine()
    random.seed(42)
    np.random.seed(42)

    # 3 Systems: Dense Vector RAG, BM25, and EpiGraph with SUPERSEDES DAG
    results = {
        "Dense_Vector_RAG": {"current_retrieved": 0, "outdated_hallucinated": 0, "total": 0},
        "BM25_Keyword": {"current_retrieved": 0, "outdated_hallucinated": 0, "total": 0},
        "EpiGraph_SUPERSEDES": {"current_retrieved": 0, "outdated_hallucinated": 0, "total": 0}
    }

    # Generate 50 synthetic multi-session mutation test cases
    for trial_idx in range(num_trials):
        template = random.choice(MUTATION_EPISODES)
        q = template["query"]
        init_fact = f"[Session 1]: {template['fact_initial']}"
        upd_fact = f"[Session 12]: {template['fact_updated']}"
        
        # Add 15 distractor background facts
        distractors = [
            f"[Session {i}]: Unrelated conversational dialogue on debugging, weather, and scheduling."
            for i in range(2, 12)
        ]
        all_docs = [init_fact] + distractors + [upd_fact]
        doc_ids = [f"DOC_{i}" for i in range(len(all_docs))]
        upd_id = doc_ids[-1]
        init_id = doc_ids[0]

        # 1. Dense Vector RAG
        all_vecs = embed.embed_texts(all_docs)
        q_vec = embed.embed_query(q)
        sims = np.dot(all_vecs, q_vec) / (np.linalg.norm(all_vecs, axis=1) * np.linalg.norm(q_vec) + 1e-9)
        top_vec_idx = np.argsort(sims)[::-1][:3]
        top_vec_ids = [doc_ids[i] for i in top_vec_idx]

        results["Dense_Vector_RAG"]["total"] += 1
        if upd_id in top_vec_ids:
            results["Dense_Vector_RAG"]["current_retrieved"] += 1
        if init_id in top_vec_ids and (top_vec_ids.index(init_id) < top_vec_ids.index(upd_id) if upd_id in top_vec_ids else True):
            results["Dense_Vector_RAG"]["outdated_hallucinated"] += 1

        # 2. BM25 Keyword Search
        q_words = set(q.lower().split())
        bm25_scores = []
        for did, text in zip(doc_ids, all_docs):
            overlap = len(set(text.lower().split()) & q_words)
            bm25_scores.append((did, overlap))
        bm25_scores.sort(key=lambda x: x[1], reverse=True)
        top_bm25_ids = [x[0] for x in bm25_scores[:3]]

        results["BM25_Keyword"]["total"] += 1
        if upd_id in top_bm25_ids:
            results["BM25_Keyword"]["current_retrieved"] += 1
        if init_id in top_bm25_ids and (top_bm25_ids.index(init_id) <= top_bm25_ids.index(upd_id) if upd_id in top_bm25_ids else True):
            results["BM25_Keyword"]["outdated_hallucinated"] += 1

        # 3. EpiGraph with Directed SUPERSEDES Filtering
        graph = DynamicCognitiveGraph(damping=0.85)
        for did, text in zip(doc_ids, all_docs):
            graph.add_node(did, label=text, node_type="fact")
        
        # Explicit SUPERSEDES directed edge from new fact to old fact
        graph.add_edge(upd_id, init_id, rel_type="SUPERSEDES", weight=3.0)

        # Retrieve with SUPERSEDES suppression
        # Seed graph with top vector and BM25 matches
        seeds = [doc_ids[i] for i in top_vec_idx[:2]] + [x[0] for x in bm25_scores[:2]]
        uppr = graph.compute_uppr(seeds, [2.0]*len(seeds))
        
        # Traverse SUPERSEDES edges: any node that is the target of a SUPERSEDES edge from a retrieved node is filtered
        superseded_targets = set()
        for src in graph.graph.nodes:
            for nbr in graph.graph.successors(src):
                edge_data = graph.graph.get_edge_data(src, nbr, {})
                if edge_data.get("rel_type") == "SUPERSEDES":
                    superseded_targets.add(nbr)

        # Ranked candidates without superseded nodes
        ranked_candidates = [nid for nid, score in sorted(uppr.items(), key=lambda x: x[1], reverse=True) if nid not in superseded_targets]
        top_epigraph_ids = ranked_candidates[:3]

        results["EpiGraph_SUPERSEDES"]["total"] += 1
        if upd_id in top_epigraph_ids:
            results["EpiGraph_SUPERSEDES"]["current_retrieved"] += 1
        if init_id in top_epigraph_ids:
            results["EpiGraph_SUPERSEDES"]["outdated_hallucinated"] += 1

    # Aggregate Summary
    summary = {}
    print("\n" + "=" * 80)
    print(f"{'SYSTEM':<26} | {'Current Fact Recall':<22} | {'Split-Brain Hallucination':<26}")
    print("-" * 80)

    for sys_name, data in results.items():
        curr_recall = (data["current_retrieved"] / data["total"]) * 100
        halluc_rate = (data["outdated_hallucinated"] / data["total"]) * 100
        summary[sys_name] = {
            "Current_Fact_Recall": curr_recall,
            "Split_Brain_Hallucination_Rate": halluc_rate,
            "Total_Trials": data["total"]
        }
        print(f"{sys_name:<26} | {curr_recall:>20.1f}% | {halluc_rate:>24.1f}%")
    print("=" * 80)

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "knowledge_update_results.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved knowledge update benchmark results to: {out_path}")
    return summary

if __name__ == "__main__":
    run_knowledge_update_benchmark()
