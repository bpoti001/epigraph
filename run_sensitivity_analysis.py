#!/usr/bin/env python3
"""
Phase 7: Hyperparameter Sensitivity Landscape Analysis
Evaluates the stability of EpiGraph across PageRank damping factors (d) and RRF smoothing constants (k).
Generates publication-quality 300 DPI Figure 5: paper/figures/fig5_sensitivity_analysis.png
"""

import os
import sys
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.embeddings import EmbeddingEngine
from src.epigraph_pipeline import EpiGraphPipeline
from run_locomo_benchmark import evaluate_retrieval

def run_sensitivity_sweep(data_path: str = None, output_dir: str = None):
    if data_path is None:
        data_path = os.path.join(BASE_DIR, "data", "locomo", "locomo10.json")
    if output_dir is None:
        output_dir = os.path.join(BASE_DIR, "results")
    print("=" * 80)
    print("PHASE 7: RUNNING HYPERPARAMETER SENSITIVITY SWEEP")
    print("Sweeping PageRank Damping (d in [0.65, 0.95]) and RRF Smoothing (k in [20, 100])")
    print("=" * 80)

    with open(data_path) as f:
        samples = json.load(f)

    embed = EmbeddingEngine()

    # Parameter ranges
    damping_factors = [0.65, 0.75, 0.85, 0.95]
    rrf_ks = [20, 40, 60, 100]

    # Collect samples
    selected_samples = []
    total_q_count = 0
    for sample in samples[:5]:
        conv = sample["conversation"]
        qas = [qa for qa in sample.get("qa", []) if qa.get("evidence")][:20]
        selected_samples.append((conv, qas))
        total_q_count += len(qas)

    print(f"Total test questions across 5 conversations: {total_q_count}")

    # Track metrics across parameter sweeps
    damping_scores = {d: {"r5": [], "mrr": []} for d in damping_factors}
    rrf_scores = {k: {"r5": [], "mrr": []} for k in rrf_ks}

    pipe = EpiGraphPipeline(embed)

    for c_idx, (conv, qas) in enumerate(selected_samples):
        print(f"Ingesting Conversation {c_idx + 1}/5 for parameter sweeps...")
        pipe.ingest_locomo_conversation(conv)

        # 1. Sweep Damping Factor
        for d in damping_factors:
            pipe.graph.damping = d
            pipe.rrf.k = 60
            for qa in qas:
                res = pipe.retrieve(qa["question"], top_k=5, record_usage=False)
                r_ids = [item[0] for item in res]
                scores = evaluate_retrieval(r_ids, qa["evidence"], top_ks=[5])
                damping_scores[d]["r5"].append(scores["Recall@5"])
                damping_scores[d]["mrr"].append(scores["MRR"])

        # 2. Sweep RRF Smoothing Constant
        pipe.graph.damping = 0.85
        for k in rrf_ks:
            pipe.rrf.k = k
            for qa in qas:
                res = pipe.retrieve(qa["question"], top_k=5, record_usage=False)
                r_ids = [item[0] for item in res]
                scores = evaluate_retrieval(r_ids, qa["evidence"], top_ks=[5])
                rrf_scores[k]["r5"].append(scores["Recall@5"])
                rrf_scores[k]["mrr"].append(scores["MRR"])

    # Aggregate Damping Results
    damping_results = {}
    print("\n--- Sweeping Damping Factor d (k=60 fixed) ---")
    for d in damping_factors:
        mean_r5 = float(np.mean(damping_scores[d]["r5"]) * 100)
        mean_mrr = float(np.mean(damping_scores[d]["mrr"]))
        damping_results[d] = {"Recall@5": mean_r5, "MRR": mean_mrr}
        print(f"  d = {d:.2f} -> Recall@5: {mean_r5:.2f}%, MRR: {mean_mrr:.4f}")

    # Aggregate RRF Results
    rrf_results = {}
    print("\n--- Sweeping RRF Smoothing Constant k (d=0.85 fixed) ---")
    for k in rrf_ks:
        mean_r5 = float(np.mean(rrf_scores[k]["r5"]) * 100)
        mean_mrr = float(np.mean(rrf_scores[k]["mrr"]))
        rrf_results[k] = {"Recall@5": mean_r5, "MRR": mean_mrr}
        print(f"  k = {k:3d} -> Recall@5: {mean_r5:.2f}%, MRR: {mean_mrr:.4f}")

    # 3. Generate Publication Figure 5
    os.makedirs(os.path.join(output_dir, "figures"), exist_ok=True)
    os.makedirs("paper/figures", exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Subplot A: Damping Factor
    d_vals = list(damping_results.keys())
    d_r5 = [damping_results[d]["Recall@5"] for d in d_vals]
    d_mrr = [damping_results[d]["MRR"] * 100 for d in d_vals]

    ax1.plot(d_vals, d_r5, marker="o", color="#1a73e8", linewidth=2.2, label="Recall@5 (%)")
    ax1.plot(d_vals, d_mrr, marker="s", color="#ea4335", linewidth=2.0, linestyle="--", label="MRR (x100)")
    ax1.axvline(x=0.85, color="#34a853", linestyle=":", label="Default ($d=0.85$)")
    ax1.set_title("Sensitivity to PageRank Damping Factor ($d$)", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("Damping Factor ($d$)", fontsize=10)
    ax1.set_ylabel("Score", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(frameon=True, fontsize=9)

    # Subplot B: RRF k Constant
    k_vals = list(rrf_results.keys())
    k_r5 = [rrf_results[k]["Recall@5"] for k in k_vals]
    k_mrr = [rrf_results[k]["MRR"] * 100 for k in k_vals]

    ax2.plot(k_vals, k_r5, marker="^", color="#137333", linewidth=2.2, label="Recall@5 (%)")
    ax2.plot(k_vals, k_mrr, marker="d", color="#f2994a", linewidth=2.0, linestyle="--", label="MRR (x100)")
    ax2.axvline(x=60, color="#1a73e8", linestyle=":", label="Default ($k=60$)")
    ax2.set_title("Sensitivity to RRF Smoothing Constant ($k$)", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("RRF Smoothing Constant ($k$)", fontsize=10)
    ax2.set_ylabel("Score", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(frameon=True, fontsize=9)

    plt.tight_layout()
    fig5_res = os.path.join(output_dir, "figures", "fig5_sensitivity_analysis.png")
    fig5_paper = os.path.join("paper", "figures", "fig5_sensitivity_analysis.png")
    plt.savefig(fig5_res, dpi=300)
    plt.savefig(fig5_paper, dpi=300)
    plt.close()

    print(f"\nSaved Figure 5 to: {fig5_res} and {fig5_paper}")

    # Save JSON summary
    summary_data = {
        "damping_sweep": {str(k): v for k, v in damping_results.items()},
        "rrf_k_sweep": {str(k): v for k, v in rrf_results.items()}
    }
    out_json = os.path.join(output_dir, "sensitivity_analysis_results.json")
    with open(out_json, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved sensitivity results to: {out_json}")
    return summary_data

if __name__ == "__main__":
    run_sensitivity_sweep()
