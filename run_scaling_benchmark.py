import os
import time
import json
import numpy as np
import networkx as nx
from src.graph_memory import DynamicCognitiveGraph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def benchmark_graph_scaling():
    print("=== Running EpiGraph U-PPR Graph Scaling Stress Test ===")
    sizes = [100, 500, 1000, 2500, 5000, 10000]
    results = []

    for n in sizes:
        # Generate scale-free / small-world graph (representative of conversational cognitive topology)
        # Power-law degree distribution with clustering (Holme and Kim model)
        m = 3  # edges to attach
        p = 0.1  # probability of adding a triangle
        base_g = nx.powerlaw_cluster_graph(n, m, p, seed=42)

        dcg = DynamicCognitiveGraph(damping=0.85)
        for u in base_g.nodes():
            dcg.add_node(f"node_{u}", f"Turn {u} concept", "entity")
        
        for u, v in base_g.edges():
            dcg.add_edge(f"node_{u}", f"node_{v}", "RELATES_TO", weight=1.0)
            dcg.add_edge(f"node_{v}", f"node_{u}", "RELATES_TO", weight=1.0)

        # Pick 5 seed nodes
        seeds = [f"node_{i}" for i in range(5)]
        
        # Warmup
        _ = dcg.compute_uppr(seeds)

        # Benchmark 20 iterations
        trials = 20
        start = time.perf_counter()
        for _ in range(trials):
            _ = dcg.compute_uppr(seeds)
        elapsed = (time.perf_counter() - start) / trials * 1000.0  # ms
        qps = 1000.0 / elapsed if elapsed > 0 else 0

        num_edges = dcg.graph.number_of_edges()
        entry = {
            "num_nodes": n,
            "num_edges": num_edges,
            "latency_ms": round(elapsed, 2),
            "qps": round(qps, 1)
        }
        results.append(entry)
        print(f"|V| = {n:5d} nodes, |E| = {num_edges:6d} edges -> Latency: {elapsed:6.2f} ms ({qps:5.1f} queries/sec)")

    out_file = os.path.join(BASE_DIR, "results", "graph_scaling_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {out_file}")

if __name__ == "__main__":
    benchmark_graph_scaling()
