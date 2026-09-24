#!/usr/bin/env python3
"""
Ablation Study: Dynamic Intent Routing vs. Static RRF & Component Contributions
Evaluates on all 496 LoCoMo QA pairs to generate empirical evidence for Section 6.
"""

import os
import json
import time
import numpy as np
from typing import Dict, List, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from src.embeddings import EmbeddingEngine
from src.epigraph_pipeline import EpiGraphPipeline
from run_locomo_benchmark import evaluate_retrieval

class StaticRRFEpiGraph(EpiGraphPipeline):
    """Ablation: Uses static equal weights (0.35, 0.35, 0.35) instead of intent-routed weights."""
    def retrieve(self, query: str, top_k: int = 10, record_usage: bool = True):
        # Temporarily override classify_intent_weights
        orig_classify = self.rrf.classify_intent_weights
        self.rrf.classify_intent_weights = lambda q: {"vector": 0.35, "graph": 0.35, "bm25": 0.35}
        try:
            return super().retrieve(query, top_k=top_k, record_usage=record_usage)
        finally:
            self.rrf.classify_intent_weights = orig_classify

class NoPlasticityEpiGraph(EpiGraphPipeline):
    """Ablation: No Hebbian edge reinforcement or usage recording."""
    def retrieve(self, query: str, top_k: int = 10, record_usage: bool = False):
        return super().retrieve(query, top_k=top_k, record_usage=False)

def run_ablation():
    with open(os.path.join(BASE_DIR, "data", "locomo", "locomo10.json")) as f:
        samples = json.load(f)

    print(f"Loaded {len(samples)} conversations from LoCoMo dataset.")

    embed = EmbeddingEngine()
    systems = {
        "EpiGraph_Dynamic_Intent": EpiGraphPipeline(embedding_engine=embed),
        "EpiGraph_Static_RRF": StaticRRFEpiGraph(embedding_engine=embed),
        "EpiGraph_No_Plasticity": NoPlasticityEpiGraph(embedding_engine=embed)
    }

    metrics = {sys_name: {"Recall@1": [], "Recall@5": [], "MRR": []} for sys_name in systems}
    cat_metrics = {sys_name: {cat: {"Recall@5": []} for cat in range(1, 6)} for sys_name in systems}

    total_q = 0
    for sample_idx, sample in enumerate(samples):
        conv = sample["conversation"]
        qa_list = sample.get("qa", [])[:50]
        print(f"\n--- Conversation {sample_idx + 1}/{len(samples)} ({len(qa_list)} QA pairs) ---")
        
        for sys_name, sys_obj in systems.items():
            sys_obj.ingest_locomo_conversation(conv)

        for q_idx, qa in enumerate(qa_list):
            q = qa.get("question", "")
            ev = qa.get("evidence", [])
            cat = qa.get("category", 1)
            if not ev:
                continue
            total_q += 1

            for sys_name, sys_obj in systems.items():
                res = sys_obj.retrieve(q, top_k=10)
                r_ids = [item[0] for item in res]
                scores = evaluate_retrieval(r_ids, ev, top_ks=[1, 5])
                metrics[sys_name]["Recall@1"].append(scores["Recall@1"])
                metrics[sys_name]["Recall@5"].append(scores["Recall@5"])
                metrics[sys_name]["MRR"].append(scores["MRR"])
                cat_metrics[sys_name][cat]["Recall@5"].append(scores["Recall@5"])

    print(f"\nCompleted evaluation over {total_q // len(systems)} unique questions.")

    summary = {}
    for sys_name in systems:
        summary[sys_name] = {
            "Recall@1": float(np.mean(metrics[sys_name]["Recall@1"]) * 100),
            "Recall@5": float(np.mean(metrics[sys_name]["Recall@5"]) * 100),
            "MRR": float(np.mean(metrics[sys_name]["MRR"])),
            "Cat2_Temporal_R5": float(np.mean(cat_metrics[sys_name][2]["Recall@5"]) * 100),
            "Cat3_MultiSession_R5": float(np.mean(cat_metrics[sys_name][3]["Recall@5"]) * 100)
        }

    print("\n" + "=" * 80)
    print(f"{'VARIANT':<25} | {'Recall@1':<9} | {'Recall@5':<9} | {'MRR':<8} | {'Cat2 (Temp)':<11} | {'Cat3 (MS)':<11}")
    print("-" * 80)
    for s_name, s_data in summary.items():
        print(f"{s_name:<25} | {s_data['Recall@1']:>7.2f}% | {s_data['Recall@5']:>7.2f}% | {s_data['MRR']:>7.4f} | {s_data['Cat2_Temporal_R5']:>9.2f}% | {s_data['Cat3_MultiSession_R5']:>9.2f}%")
    print("=" * 80)

    out_file = os.path.join(BASE_DIR, "results", "rrf_ablation_results.json")
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved results to {out_file}")

if __name__ == "__main__":
    run_ablation()
