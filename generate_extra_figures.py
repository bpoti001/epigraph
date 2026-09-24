import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_fig6_architecture():
    """Generates 300 DPI System Architecture Diagram for EpiGraph."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Title
    ax.text(50, 96, "EpiGraph Dual-Brain Architecture: Waking Reflex & Dreaming Consolidation", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1E293B")

    # Waking State Box (Top half)
    waking_rect = patches.FancyBboxPatch((3, 44), 94, 48, boxstyle="round,pad=1.5", 
                                        ec="#2563EB", fc="#EFF6FF", lw=2, linestyle="-")
    ax.add_patch(waking_rect)
    ax.text(6, 88, "WAKING STATE (Real-Time Read/Write Reflex — Sub-25ms Budget)", 
            fontsize=10.5, fontweight="bold", color="#1D4ED8")

    # Components inside Waking
    # Ingestion flow
    ax.add_patch(patches.FancyBboxPatch((6, 68), 16, 16, boxstyle="round,pad=0.8", ec="#3B82F6", fc="#FFFFFF", lw=1.5))
    ax.text(14, 78, "Dialogue Turn", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B")
    ax.text(14, 72, "Raw Utterances", ha="center", va="center", fontsize=8, color="#64748B")

    ax.annotate("", xy=(26, 76), xytext=(22, 76), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563EB"))

    ax.add_patch(patches.FancyBboxPatch((26, 68), 18, 16, boxstyle="round,pad=0.8", ec="#3B82F6", fc="#FFFFFF", lw=1.5))
    ax.text(35, 78, "Triage & Embed", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B")
    ax.text(35, 72, "MiniLM Encoder", ha="center", va="center", fontsize=8, color="#64748B")

    ax.annotate("", xy=(48, 76), xytext=(44, 76), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563EB"))

    ax.add_patch(patches.FancyBboxPatch((48, 68), 20, 16, boxstyle="round,pad=0.8", ec="#3B82F6", fc="#FFFFFF", lw=1.5))
    ax.text(58, 78, "Redis Streams", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B")
    ax.text(58, 72, "Async Queue + DLQ", ha="center", va="center", fontsize=8, color="#64748B")

    # Storage engines
    ax.add_patch(patches.FancyBboxPatch((72, 68), 22, 16, boxstyle="round,pad=0.8", ec="#059669", fc="#ECFDF5", lw=1.5))
    ax.text(83, 78, "Dual-Brain Stores", ha="center", va="center", fontsize=9, fontweight="bold", color="#065F46")
    ax.text(83, 72, "RedisJSON + Neo4j GDS", ha="center", va="center", fontsize=7.5, color="#047857")

    # Retrieval flow
    ax.add_patch(patches.FancyBboxPatch((6, 48), 16, 15, boxstyle="round,pad=0.8", ec="#8B5CF6", fc="#FFFFFF", lw=1.5))
    ax.text(14, 57, "User Query", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B")
    ax.text(14, 52, "Dynamic Intent", ha="center", va="center", fontsize=8, color="#64748B")

    ax.annotate("", xy=(26, 55.5), xytext=(22, 55.5), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7C3AED"))

    # Quad-Leg Retrieval Legs
    ax.add_patch(patches.FancyBboxPatch((26, 47), 18, 17, boxstyle="round,pad=0.8", ec="#8B5CF6", fc="#F5F3FF", lw=1.5))
    ax.text(35, 60, "Leg 1: Vector HNSW", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#6D28D9")
    ax.text(35, 55.5, "Leg 2: BM25 Lexical", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#6D28D9")
    ax.text(35, 51, "Leg 3: U-PPR Graph", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#6D28D9")

    ax.annotate("", xy=(48, 55.5), xytext=(44, 55.5), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7C3AED"))

    ax.add_patch(patches.FancyBboxPatch((48, 48), 20, 15, boxstyle="round,pad=0.8", ec="#8B5CF6", fc="#FFFFFF", lw=1.5))
    ax.text(58, 57, "Quad-Leg RRF", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E293B")
    ax.text(58, 52, "Rank Aggregation", ha="center", va="center", fontsize=8, color="#64748B")

    ax.annotate("", xy=(72, 55.5), xytext=(68, 55.5), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7C3AED"))

    ax.add_patch(patches.FancyBboxPatch((72, 48), 22, 15, boxstyle="round,pad=0.8", ec="#D97706", fc="#FFFBEB", lw=1.5))
    ax.text(83, 57, "Downstream Prompt", ha="center", va="center", fontsize=9, fontweight="bold", color="#92400E")
    ax.text(83, 52, "Local Open LLM", ha="center", va="center", fontsize=8, color="#B45309")

    # Dreaming State Box (Bottom half)
    dreaming_rect = patches.FancyBboxPatch((3, 4), 94, 34, boxstyle="round,pad=1.5", 
                                          ec="#7C3AED", fc="#FAF5FF", lw=2, linestyle="-")
    ax.add_patch(dreaming_rect)
    ax.text(6, 34, "DREAMING STATE (Offline Synaptic Consolidation Worker — Background Every 6h)", 
            fontsize=10.5, fontweight="bold", color="#6D28D9")

    # 4 Dreaming Pillars
    pillars = [
        ("1. HNSW-DBSCAN", "O(N log N) Entity Dedup\nNo pairwise O(N^2) memory", 7, "#EDE9FE", "#5B21B6"),
        ("2. Louvain Clustering", "Macro-thematic modules\nCommunity centroids", 30, "#EDE9FE", "#5B21B6"),
        ("3. God Node Centrality", "Global stationary PageRank\nEpistemic Macro-Hubs", 53, "#EDE9FE", "#5B21B6"),
        ("4. CATD Synaptic Pruning", "Load-bearing retention\nN_grace >= 4 grace period", 75, "#FEE2E2", "#991B1B"),
    ]

    for title, desc, x_pos, fc_col, text_col in pillars:
        ax.add_patch(patches.FancyBboxPatch((x_pos, 8), 19, 22, boxstyle="round,pad=0.8", ec=text_col, fc=fc_col, lw=1.5))
        ax.text(x_pos + 9.5, 25, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=text_col)
        ax.text(x_pos + 9.5, 16, desc, ha="center", va="center", fontsize=7.5, color="#374151")

    # Arrow connecting Waking and Dreaming
    ax.annotate("", xy=(50, 43), xytext=(50, 39), 
                arrowprops=dict(arrowstyle="<->", lw=2, color="#4F46E5", linestyle="--"))
    ax.text(52, 41, "Decoupled Asynchronous Consolidation", fontsize=8, color="#4338CA", fontstyle="italic")

    plt.tight_layout()
    plt.savefig("paper/figures/fig6_system_architecture.png", dpi=300, bbox_inches="tight")
    plt.savefig("results/figures/fig6_system_architecture.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Generated Figure 6: System Architecture Diagram")

def generate_fig7_knowledge_dag():
    """Generates 300 DPI Knowledge Mutation DAG vs Flat Vector diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)

    # Subplot 1: Flat Vector RAG (Split-Brain Hallucination Pathology)
    ax1.set_title("(a) Flat Vector RAG: Split-Brain Hallucination\n(70.0% Outdated Citation Rate)", fontsize=10, fontweight="bold", color="#991B1B")
    ax1.axis("off")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)

    # Query node
    ax1.add_patch(patches.Circle((5, 8.5), 1.0, color="#3B82F6", ec="#1D4ED8", lw=1.5))
    ax1.text(5, 8.5, "Query:\nUser Location", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    # Old and New Fact Nodes
    ax1.add_patch(patches.Circle((2.5, 3.5), 1.2, color="#FCA5A5", ec="#DC2626", lw=2))
    ax1.text(2.5, 3.5, "Old Fact (t=1)\n'Lives in Seattle'\n(OUTDATED)", ha="center", va="center", color="#7F1D1D", fontsize=7.5, fontweight="bold")

    ax1.add_patch(patches.Circle((7.5, 3.5), 1.2, color="#86EFAC", ec="#16A34A", lw=2))
    ax1.text(7.5, 3.5, "New Fact (t=2)\n'Lives in Zurich'\n(CURRENT)", ha="center", va="center", color="#14532D", fontsize=7.5, fontweight="bold")

    # Cosine Similarity Arrows
    ax1.annotate("", xy=(2.8, 4.6), xytext=(4.3, 7.8), arrowprops=dict(arrowstyle="->", lw=2, color="#DC2626", linestyle="--"))
    ax1.text(2.8, 6.4, "cos=0.88\n(Retrieved)", color="#DC2626", fontsize=8, fontweight="bold")

    ax1.annotate("", xy=(7.2, 4.6), xytext=(5.7, 7.8), arrowprops=dict(arrowstyle="->", lw=2, color="#16A34A", linestyle="-"))
    ax1.text(6.8, 6.4, "cos=0.89\n(Retrieved)", color="#16A34A", fontsize=8, fontweight="bold")

    ax1.text(5, 1.2, "FAILURE: Both facts retrieved together\ncausing LLM split-brain hallucination", ha="center", va="center", 
             fontsize=8.5, color="#B91C1C", fontweight="bold", bbox=dict(boxstyle="round,pad=0.5", fc="#FEE2E2", ec="#EF4444"))

    # Subplot 2: EpiGraph Directed SUPERSEDES DAG (0% Hallucination)
    ax2.set_title("(b) EpiGraph: Directed SUPERSEDES DAG\n(0.0% Hallucination, 100% Recall)", fontsize=10, fontweight="bold", color="#15803D")
    ax2.axis("off")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)

    # Query node
    ax2.add_patch(patches.Circle((5, 8.5), 1.0, color="#3B82F6", ec="#1D4ED8", lw=1.5))
    ax2.text(5, 8.5, "Query:\nUser Location", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    # Old and New Fact Nodes
    ax2.add_patch(patches.Circle((2.5, 3.5), 1.2, color="#E2E8F0", ec="#94A3B8", lw=1.5, linestyle="--"))
    ax2.text(2.5, 3.5, "Old Fact (t=1)\n'Lives in Seattle'\n[SUPPRESSED]", ha="center", va="center", color="#64748B", fontsize=7.5, fontstyle="italic")

    ax2.add_patch(patches.Circle((7.5, 3.5), 1.2, color="#86EFAC", ec="#16A34A", lw=2.5))
    ax2.text(7.5, 3.5, "New Fact (t=2)\n'Lives in Zurich'\n[SUPERSEDES]", ha="center", va="center", color="#14532D", fontsize=7.5, fontweight="bold")

    # Directed SUPERSEDES edge from New to Old
    ax2.annotate("", xy=(3.8, 3.5), xytext=(6.2, 3.5), arrowprops=dict(arrowstyle="->", lw=2.5, color="#DC2626"))
    ax2.text(5.0, 4.1, "[:SUPERSEDES]", ha="center", va="center", color="#DC2626", fontsize=8, fontweight="bold")

    # Activated path
    ax2.annotate("", xy=(7.2, 4.6), xytext=(5.7, 7.8), arrowprops=dict(arrowstyle="->", lw=2.5, color="#15803D"))
    ax2.text(6.8, 6.4, "U-PPR Prior\n(Active)", color="#15803D", fontsize=8, fontweight="bold")

    ax2.text(5, 1.2, "SUCCESS: SUPERSEDES edge blocks traversal\nto outdated node -> Zero hallucination", ha="center", va="center", 
             fontsize=8.5, color="#15803D", fontweight="bold", bbox=dict(boxstyle="round,pad=0.5", fc="#DCFCE7", ec="#22C55E"))

    plt.tight_layout()
    plt.savefig("paper/figures/fig7_knowledge_mutation_dag.png", dpi=300, bbox_inches="tight")
    plt.savefig("results/figures/fig7_knowledge_mutation_dag.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Generated Figure 7: Knowledge Mutation DAG Diagram")

def generate_fig8_spreading_activation():
    """Generates 300 DPI U-PPR Spreading Activation & God Node diagram."""
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.set_title("EpiGraph Usage-Modulated Spreading Activation (U-PPR) & Epistemic Hubs", 
                 fontsize=11, fontweight="bold", color="#1E293B", pad=12)

    # Epistemic Macro-Hub ("God Node") in the center
    ax.add_patch(patches.Circle((5, 5), 1.4, color="#FDE047", ec="#CA8A04", lw=3))
    ax.text(5, 5, "Epistemic Macro-Hub\n('God Node')\nUser Persona Anchor\npi*(v) = 0.264", 
            ha="center", va="center", color="#713F12", fontsize=8, fontweight="bold")

    # Seed Nodes (top-left)
    seeds = [(2, 8.5, "Query Seed 1\n(BM25 Hit)"), (4, 8.8, "Query Seed 2\n(Vector Hit)")]
    for sx, sy, lbl in seeds:
        ax.add_patch(patches.Circle((sx, sy), 0.9, color="#93C5FD", ec="#2563EB", lw=2))
        ax.text(sx, sy, lbl, ha="center", va="center", color="#1E3A8A", fontsize=7.5, fontweight="bold")
        # Edge to God Node
        ax.annotate("", xy=(4.3, 6.2), xytext=(sx + 0.3, sy - 0.8), 
                    arrowprops=dict(arrowstyle="->", lw=2, color="#2563EB"))

    # Multi-hop evidentiary turns (bottom-right and sides)
    nodes = [
        (8, 7.5, "Session 3 Fact\n(2-Hop Target)", "#BBF7D0", "#16A34A", 1.0),
        (8.5, 4.5, "Session 12 Constraint\n(3-Hop Reachable)", "#BBF7D0", "#16A34A", 1.0),
        (2, 2.5, "Hebbian Bridge Turn\n(Co-activated)", "#DDD6FE", "#7C3AED", 1.1),
        (7.5, 1.8, "Transient Chatter\n(Pruned by CATD)", "#F1F5F9", "#94A3B8", 0.9)
    ]

    for nx_pos, ny_pos, nlbl, nfc, nec, nrad in nodes:
        ls = "--" if "Pruned" in nlbl else "-"
        ax.add_patch(patches.Circle((nx_pos, ny_pos), nrad, color=nfc, ec=nec, lw=1.8, linestyle=ls))
        tc = "#64748B" if "Pruned" in nlbl else "#1E293B"
        ax.text(nx_pos, ny_pos, nlbl, ha="center", va="center", color=tc, fontsize=7.5, fontweight="bold")

    # Connect God Node to facts
    ax.annotate("", xy=(7.1, 7.0), xytext=(6.1, 5.8), arrowprops=dict(arrowstyle="->", lw=2.2, color="#CA8A04"))
    ax.annotate("", xy=(7.4, 4.6), xytext=(6.4, 5.0), arrowprops=dict(arrowstyle="->", lw=2.2, color="#CA8A04"))
    
    # Hebbian reinforced edge
    ax.annotate("", xy=(3.8, 4.4), xytext=(2.9, 3.2), arrowprops=dict(arrowstyle="<->", lw=2.5, color="#7C3AED"))
    ax.text(3.0, 4.0, "Hebbian W += 0.5", color="#6D28D9", fontsize=7.5, fontweight="bold", rotation=35)

    # Pruned edge (faded)
    ax.annotate("", xy=(6.8, 2.4), xytext=(5.8, 4.0), arrowprops=dict(arrowstyle="->", lw=1, color="#CBD5E1", linestyle=":"))

    # Legend / Annotation Box
    ax.text(5, 0.4, 
            "Legend: Gold = Epistemic Macro-Hub (Gravitational Anchor); Blue = Ingestion Seeds; Green = Retrieved Contexts; Purple = Hebbian Plasticity Bridge", 
            ha="center", va="center", fontsize=7.5, color="#475569", 
            bbox=dict(boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#E2E8F0"))

    plt.tight_layout()
    plt.savefig("paper/figures/fig8_uppr_spreading_activation.png", dpi=300, bbox_inches="tight")
    plt.savefig("results/figures/fig8_uppr_spreading_activation.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Generated Figure 8: Spreading Activation & God Node Diagram")

if __name__ == "__main__":
    import os
    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("paper/figures", exist_ok=True)
    generate_fig6_architecture()
    generate_fig7_knowledge_dag()
    generate_fig8_spreading_activation()
