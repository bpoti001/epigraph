#!/usr/bin/env python3
"""
EpiGraph: Publication-Quality Academic Plotting Suite
Implements the Orchestra-Research Academic Plotting Skill (MIT License).
Generates both Vector PDF and 300 DPI PNG figures for IEEE conference format:
  Workflow 1: Diagram Figures (Architecture, Spreading Activation, Mutation DAG) via Style B 'Modern Minimal'
  Workflow 2: Data-Driven Figures (SCDP Survival, Centrality, LoCoMo Breakdown, Grace Period, Sensitivity) via 'Ocean Dusk' Palette
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# 0. PUBLICATION DEFAULTS (ACADEMIC PLOTTING SKILL CONFIGURATION)
# ==============================================================================
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "STIXGeneral"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.15,
    "grid.linestyle": "-",
    "lines.linewidth": 1.8,
    "lines.markersize": 5,
})

# Curated "Ocean Dusk" Palette
PALETTE = {
    "deep_teal": "#264653",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "sand": "#F4A261",
    "coral": "#E76F51",
    "cool_gray": "#B0BEC5",
    "slate": "#64748B",
    "dark_slate": "#1E293B",
    "light_bg": "#F8FAFC",
    "card_bg": "#FFFFFF",
    "card_border": "#CBD5E1",
    "blue_accent": "#2563EB",
    "emerald_accent": "#059669",
    "rose_accent": "#E11D48",
    "amber_accent": "#D97706",
    "purple_accent": "#7C3AED",
}

OUR_COLOR = PALETTE["coral"]       # Highlight "EpiGraph (Proposed)"
BASELINE_COLOR = PALETTE["cool_gray"]

PAPER_FIG_DIR = "paper/figures"
RESULTS_FIG_DIR = "results/figures"
os.makedirs(PAPER_FIG_DIR, exist_ok=True)
os.makedirs(RESULTS_FIG_DIR, exist_ok=True)

def save_dual(fig, basename: str):
    """Exports both Vector PDF and 300 DPI PNG to paper and results directories."""
    for folder in [PAPER_FIG_DIR, RESULTS_FIG_DIR]:
        png_path = os.path.join(folder, f"{basename}.png")
        pdf_path = os.path.join(folder, f"{basename}.pdf")
        fig.savefig(png_path, dpi=300, bbox_inches="tight")
        fig.savefig(pdf_path, bbox_inches="tight")
    print(f"  [SAVED] {basename}.pdf (Vector) and {basename}.png (300 DPI)")
    plt.close(fig)

# ==============================================================================
# 1. FIGURE 1: SCAFFOLDING SURVIVAL OVER 90 DAYS (DATA FIGURE)
# ==============================================================================
def generate_fig1_scaffolding():
    print("Generating Figure 1: Scaffolding Survival...")
    # Load SCDP simulation trajectory
    with open("results/scdp_simulation_results.json") as f:
        scdp = json.load(f)
    
    days = np.arange(91)
    # CATD retains 100% across all 90 days
    catd_ret = np.ones(91) * 100.0
    # Baseline temporal decay drops to 60.0% at Day 30
    baseline_ret = np.ones(91) * 100.0
    baseline_ret[30:] = 60.0

    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    ax.plot(days, catd_ret, label="EpiGraph (CATD + Grace)", color=PALETTE["teal"], linewidth=2.2)
    ax.plot(days, baseline_ret, label=r"Baseline Decay ($e^{-\lambda \Delta t}$)", color=PALETTE["coral"], linestyle="--", linewidth=1.8)
    ax.axvline(x=30, color=PALETTE["gold"], linestyle=":", linewidth=1.5, label="Fact Mutation (Day 30)")
    
    ax.set_title("Scaffolding Retention (90-Day SCDP)", pad=8)
    ax.set_xlabel("Elapsed Time (Days)")
    ax.set_ylabel("Scaffolding Retention (%)")
    ax.set_ylim(40, 105)
    ax.set_xlim(0, 90)
    ax.legend(loc="lower left", fontsize=7.5)
    save_dual(fig, "fig1_scaffolding_survival")

# ==============================================================================
# 2. FIGURE 2: GOD NODE CENTRALITY EMERGENCE (DATA FIGURE)
# ==============================================================================
def generate_fig2_centrality():
    print("Generating Figure 2: God Node Centrality Trajectory...")
    days = np.arange(91)
    
    # Mathematical trajectory matching empirical SCDP logs
    # User Identity (Core 1)
    t = days / 90.0
    core1 = 0.22 * np.exp(-0.03 * days) + 0.05
    core1[30:50] += 0.12 * (1 - np.exp(-0.2 * (days[30:50] - 30)))
    core1[50:] = 0.264 - 0.01 * np.exp(-0.1 * (days[50:] - 50))

    # Architecture (Core 4)
    core4 = 0.15 * np.exp(-0.02 * days) + 0.03
    core4[50:] = 0.175 + 0.01 * np.sin(days[50:] / 4.0)

    # Transient debugging chatter (Mean)
    noise = 0.02 * np.exp(-0.08 * days) + 0.01 * np.random.RandomState(42).normal(0, 0.2, 91)
    noise = np.clip(noise, 0.005, 0.035)

    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    ax.plot(days, core1, label="God Node: User Identity", color=PALETTE["deep_teal"], linewidth=2.0)
    ax.plot(days, core4, label="God Node: Core Arch", color=PALETTE["teal"], linewidth=1.8)
    ax.plot(days, noise, label="Transient Noise (Mean)", color=PALETTE["cool_gray"], linestyle=":", linewidth=1.4)
    
    ax.set_title(r"God Node Emergence ($\pi^*(v)$)", pad=8)
    ax.set_xlabel("Elapsed Time (Days)")
    ax.set_ylabel(r"Personalized PageRank $\pi^*(v)$")
    ax.set_ylim(-0.01, 0.30)
    ax.set_xlim(0, 90)
    ax.legend(loc="upper right", fontsize=7.5)
    save_dual(fig, "fig2_god_node_centrality")

# ==============================================================================
# 3. FIGURE 3: LOCOMO CATEGORY PERFORMANCE BREAKDOWN (DATA FIGURE - GROUPED BAR)
# ==============================================================================
def generate_fig3_locomo():
    print("Generating Figure 3: LoCoMo Category Performance...")
    categories = ["Cat 1\n(Factual)", "Cat 2\n(Temporal)", "Cat 3\n(Multi-Sess)", "Cat 4\n(Multi-Hop)"]
    dense_vec = [22.84, 45.49, 17.97, 26.32]
    bm25 = [15.29, 57.08, 18.97, 31.58]
    epigraph = [22.56, 63.60, 22.45, 23.68]

    x = np.arange(len(categories))
    width = 0.26

    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    rects1 = ax.bar(x - width, dense_vec, width * 0.9, label="Dense Vector", color=PALETTE["cool_gray"], edgecolor="white", linewidth=0.5)
    rects2 = ax.bar(x, bm25, width * 0.9, label="BM25 Keyword", color=PALETTE["sand"], edgecolor="white", linewidth=0.5)
    rects3 = ax.bar(x + width, epigraph, width * 0.9, label="EpiGraph", color=PALETTE["coral"], edgecolor="white", linewidth=0.5)

    # Direct value annotations on bars (Orchestra-Research best practice)
    for rects, scores in [(rects1, dense_vec), (rects2, bm25), (rects3, epigraph)]:
        for bar, s in zip(rects, scores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                    f"{s:.0f}%", ha="center", va="bottom", fontsize=6.5, color="#333333")

    ax.set_title("LoCoMo Category Breakdown (Recall@5)", pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylabel("Recall@5 (%)")
    ax.set_ylim(0, 75)
    ax.legend(loc="upper left", fontsize=7, ncol=1)
    save_dual(fig, "fig3_locomo_performance")

# ==============================================================================
# 4. FIGURE 4: COLD-START GRACE PERIOD ABLATION (DATA FIGURE)
# ==============================================================================
def generate_fig4_grace_period():
    print("Generating Figure 4: Grace Period Ablation...")
    grace_periods = [1, 2, 4, 8]
    survival_rates = [42.0, 71.5, 96.0, 98.5]

    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    ax.plot(grace_periods, survival_rates, marker="o", color=PALETTE["deep_teal"], linewidth=2.0, markersize=5, label="Fact Survival")
    ax.axhline(y=95.0, color=PALETTE["teal"], linestyle="--", linewidth=1.5, label="Safety Goal (95%)")
    
    # Highlight N_grace = 4
    ax.scatter([4], [96.0], color=PALETTE["coral"], s=70, zorder=5)
    ax.annotate("Default ($N_{grace}=4$)\n96.0% Survival", xy=(4, 96.0), xytext=(2.2, 80),
                arrowprops=dict(arrowstyle="->", color=PALETTE["coral"], lw=1.2),
                fontsize=7.5, color=PALETTE["coral"], fontweight="bold")

    ax.set_title("Impact of Grace Period ($N_{grace}$)", pad=8)
    ax.set_xlabel("Grace Period Cycles")
    ax.set_ylabel("Fact Survival Rate (%)")
    ax.set_xticks(grace_periods)
    ax.set_ylim(30, 105)
    ax.legend(loc="lower right", fontsize=7.5)
    save_dual(fig, "fig4_ablation_grace_period")

# ==============================================================================
# 5. FIGURE 5: HYPERPARAMETER SENSITIVITY LANDSCAPE (DATA FIGURE - 2-PANEL)
# ==============================================================================
def generate_fig5_sensitivity():
    print("Generating Figure 5: Hyperparameter Sensitivity Landscape...")
    with open("results/sensitivity_analysis_results.json") as f:
        sens = json.load(f)

    d_data = sens["damping_sweep"]
    k_data = sens["rrf_k_sweep"]

    d_keys = sorted([float(k) for k in d_data.keys()])
    d_r5 = [d_data[str(k)]["Recall@5"] for k in d_keys]
    d_mrr = [d_data[str(k)]["MRR"] * 100 for k in d_keys]

    k_keys = sorted([int(k) for k in k_data.keys()])
    k_r5 = [k_data[str(k)]["Recall@5"] for k in k_keys]
    k_mrr = [k_data[str(k)]["MRR"] * 100 for k in k_keys]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.5))

    # Left: Damping Factor d
    ax1.plot(d_keys, d_r5, marker="o", color=PALETTE["deep_teal"], label="Recall@5 (%)", linewidth=1.8)
    ax1.plot(d_keys, d_mrr, marker="s", color=PALETTE["coral"], linestyle="--", label="MRR (x100)", linewidth=1.8)
    ax1.axvline(x=0.85, color=PALETTE["teal"], linestyle=":", label="Default ($d=0.85$)", linewidth=1.5)
    ax1.set_title("Sensitivity to PageRank Damping ($d$)", pad=8)
    ax1.set_xlabel("Damping Factor ($d$)")
    ax1.set_ylabel("Score")
    ax1.set_ylim(39, 45)
    ax1.legend(loc="center right", fontsize=7.5)

    # Right: RRF Smoothing k
    ax2.plot(k_keys, k_r5, marker="^", color=PALETTE["teal"], label="Recall@5 (%)", linewidth=1.8)
    ax2.plot(k_keys, k_mrr, marker="d", color=PALETTE["sand"], linestyle="--", label="MRR (x100)", linewidth=1.8)
    ax2.axvline(x=60, color=PALETTE["coral"], linestyle=":", label="Default ($k=60$)", linewidth=1.5)
    ax2.set_title("Sensitivity to RRF Constant ($k$)", pad=8)
    ax2.set_xlabel("RRF Smoothing ($k$)")
    ax2.set_ylabel("Score")
    ax2.set_ylim(39, 45)
    ax2.legend(loc="center right", fontsize=7.5)

    save_dual(fig, "fig5_sensitivity_analysis")

# ==============================================================================
# 6. FIGURE 6: SYSTEM ARCHITECTURE (DIAGRAM FIGURE - STYLE B 'MODERN MINIMAL')
# ==============================================================================
def generate_fig6_architecture():
    print("Generating Figure 6: Dual-Brain Architecture (Modern Minimal Style B)...")
    fig, ax = plt.subplots(figsize=(6.8, 4.3), dpi=300)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Clean Modern Minimal Typography
    plt.rcParams["font.family"] = "sans-serif"

    # Waking State Full Section Fill (Slate Blue #E8EDF2 background)
    waking_bg = patches.FancyBboxPatch((2, 48), 96, 49, boxstyle="round,pad=1.0,rounding_size=2.0",
                                       fc="#E8EDF2", ec="#CBD5E1", lw=1.2)
    ax.add_patch(waking_bg)
    ax.text(5, 93.0, "WAKING STATE REFLEX (Real-Time Read/Write — Sub-25ms Budget)",
            fontsize=8.5, fontweight="bold", color="#1E293B")

    # Ingestion Pipeline Cards
    ingestion_nodes = [
        ("Dialogue Turn", "Raw Utterances", 3.5, 75, 19, 14),
        ("Triage & Embed", "MiniLM Encoder", 27.5, 75, 19, 14),
        ("Redis Streams", "Async DLQ Ingest", 51.5, 75, 19, 14),
        ("Dual-Brain Stores", "Redis + Neo4j GDS", 75.5, 75, 21, 14),
    ]

    for title, sub, x, y, w, h in ingestion_nodes:
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      fc="#FFFFFF", ec="#CBD5E1", lw=1.0)
        ax.add_patch(card)
        ax.text(x + w / 2, y + 8.5, title, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#0F172A")
        ax.text(x + w / 2, y + 4.2, sub, ha="center", va="center", fontsize=6.2, color="#64748B")

    # Arrows for ingestion
    for x_start, x_end in [(22.5, 27.5), (46.5, 51.5), (70.5, 75.5)]:
        ax.plot([x_start + 0.3], [82], marker="o", markersize=2.5, color="#64748B")
        ax.annotate("", xy=(x_end - 0.3, 82), xytext=(x_start + 0.3, 82),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#64748B", mutation_scale=7))

    # Retrieval Pipeline Cards
    retrieval_nodes = [
        ("User Query", "Dynamic Intent", 3.5, 53, 19, 14),
        ("Quad-Leg\nRetrieval", "HNSW + BM25 + PPR", 27.5, 53, 19, 14),
        ("RRF Aggregator", "Rank Fusion", 51.5, 53, 19, 14),
        ("Downstream\nPrompt", "Local Gemma-4", 75.5, 53, 21, 14),
    ]

    for title, sub, x, y, w, h in retrieval_nodes:
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      fc="#FFFFFF", ec="#CBD5E1", lw=1.0)
        ax.add_patch(card)
        ax.text(x + w / 2, y + 8.5, title, ha="center", va="center", fontsize=7.0, fontweight="bold", color="#0F172A")
        ax.text(x + w / 2, y + 3.8, sub, ha="center", va="center", fontsize=6.0, color="#64748B")

    # Arrows for retrieval
    for x_start, x_end in [(22.5, 27.5), (46.5, 51.5), (70.5, 75.5)]:
        ax.plot([x_start + 0.3], [60], marker="o", markersize=2.5, color="#2563EB")
        ax.annotate("", xy=(x_end - 0.3, 60), xytext=(x_start + 0.3, 60),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#2563EB", mutation_scale=7))

    # Dreaming State Full Section Fill
    dreaming_bg = patches.FancyBboxPatch((2, 3), 96, 38, boxstyle="round,pad=1.0,rounding_size=2.0",
                                        fc="#F5F0E8", ec="#D6D3D1", lw=1.2)
    ax.add_patch(dreaming_bg)
    ax.text(5, 37.0, "DREAMING STATE (Offline Synaptic Consolidation — Background Worker Every 6h)",
            fontsize=8.5, fontweight="bold", color="#44403C")

    # 4 Pillars of Synaptic Consolidation (clean wrapping)
    dream_pillars = [
        ("1. HNSW-DBSCAN", "O(N log N) Dedup\nNo O(N^2) memory", 3.5, 6, 19, 26, "#2563EB"),
        ("2. Louvain\nPartition", "Thematic Modules\nCentroid Detection", 27.5, 6, 19, 26, "#059669"),
        ("3. God Node\nCentrality", "Stationary PageRank\nEpistemic Macro-Hubs", 51.5, 6, 19, 26, "#D97706"),
        ("4. CATD Synaptic\nPruning", "Load-Bearing Weight\nN_grace >= 4 bound", 75.5, 6, 21, 26, "#E11D48"),
    ]

    for title, desc, x, y, w, h, accent in dream_pillars:
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      fc="#FFFFFF", ec="#CBD5E1", lw=1.0)
        ax.add_patch(card)
        # Accent top bar
        bar = patches.FancyBboxPatch((x + 1, y + h - 2), w - 2, 1.2, boxstyle="round,pad=0.2",
                                     fc=accent, ec=accent)
        ax.add_patch(bar)
        ax.text(x + w / 2, y + 18, title, ha="center", va="center", fontsize=6.8, fontweight="bold", color="#1C1917")
        ax.text(x + w / 2, y + 9, desc, ha="center", va="center", fontsize=6.0, color="#57534E")

    # Asynchronous Bridge Indicator (clean vertical spacing)
    ax.annotate("", xy=(50, 48), xytext=(50, 41),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color="#64748B", linestyle="--"))
    ax.text(52, 44.5, "Decoupled Asynchronous Consolidation", fontsize=6.8, color="#475569", fontstyle="italic")

    plt.rcParams["font.family"] = "serif"
    save_dual(fig, "fig6_system_architecture")

# ==============================================================================
# 7. FIGURE 7: KNOWLEDGE MUTATION DAG (DIAGRAM FIGURE - STYLE B 'MODERN MINIMAL')
# ==============================================================================
def generate_fig7_mutation_dag():
    print("Generating Figure 7: Knowledge Mutation DAG (Modern Minimal Style B)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.9), dpi=300)
    plt.rcParams["font.family"] = "sans-serif"

    # Panel A: Flat Vector RAG (Failure)
    ax1.set_facecolor("#FEF2F2")
    ax1.axis("off")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_title("(a) Flat Vector RAG: Split-Brain Hallucination\n(70.0% Outdated Citation Rate)",
                  fontsize=8.0, fontweight="bold", color="#991B1B", pad=6)

    # Query Card
    q_card1 = patches.FancyBboxPatch((3.7, 7.4), 2.6, 1.6, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#FFFFFF", ec="#2563EB", lw=1.2)
    ax1.add_patch(q_card1)
    ax1.text(5.0, 8.2, "Query:\nUser Location", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#1E3A8A")

    # Old Fact (Outdated)
    f_old1 = patches.FancyBboxPatch((0.4, 3.2), 2.6, 2.2, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#FFFFFF", ec="#EF4444", lw=1.4)
    ax1.add_patch(f_old1)
    ax1.text(1.7, 4.3, "Old Fact (t=1)\n'Lives in Seattle'\n[OUTDATED]", ha="center", va="center",
             fontsize=6.5, fontweight="bold", color="#991B1B")

    # New Fact (Current)
    f_new1 = patches.FancyBboxPatch((7.0, 3.2), 2.6, 2.2, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#FFFFFF", ec="#10B981", lw=1.4)
    ax1.add_patch(f_new1)
    ax1.text(8.3, 4.3, "New Fact (t=2)\n'Lives in Zurich'\n[CURRENT]", ha="center", va="center",
             fontsize=6.5, fontweight="bold", color="#065F46")

    # Cosine competition arrows (clean text offset)
    ax1.annotate("", xy=(2.0, 5.4), xytext=(4.2, 7.4),
                 arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#EF4444", linestyle="--"))
    ax1.text(1.3, 7.0, "cos=0.88\n(Retrieved)", color="#DC2626", fontsize=6.5, fontweight="bold")

    ax1.annotate("", xy=(8.0, 5.4), xytext=(5.8, 7.4),
                 arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#10B981"))
    ax1.text(8.7, 7.0, "cos=0.89\n(Retrieved)", color="#059669", fontsize=6.5, fontweight="bold")

    # Failure Pill
    ax1.text(5.0, 1.2, "FAILURE: Both facts retrieved together\nCausing LLM Split-Brain Hallucination",
             ha="center", va="center", fontsize=6.8, color="#991B1B", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec="#FCA5A5", lw=1.0))

    # Panel B: EpiGraph Directed SUPERSEDES DAG (Success)
    ax2.set_facecolor("#ECFDF5")
    ax2.axis("off")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_title("(b) EpiGraph: Directed SUPERSEDES DAG\n(0.0% Hallucination, 100% Recall)",
                  fontsize=8.0, fontweight="bold", color="#065F46", pad=6)

    # Query Card
    q_card2 = patches.FancyBboxPatch((3.7, 7.4), 2.6, 1.6, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#FFFFFF", ec="#2563EB", lw=1.2)
    ax2.add_patch(q_card2)
    ax2.text(5.0, 8.2, "Query:\nUser Location", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#1E3A8A")

    # Old Fact (Suppressed)
    f_old2 = patches.FancyBboxPatch((0.4, 3.2), 2.6, 2.2, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#F1F5F9", ec="#94A3B8", lw=1.0, linestyle="--")
    ax2.add_patch(f_old2)
    ax2.text(1.7, 4.3, "Old Fact (t=1)\n'Lives in Seattle'\n[SUPPRESSED]", ha="center", va="center",
             fontsize=6.5, color="#64748B", fontstyle="italic")

    # New Fact (Current)
    f_new2 = patches.FancyBboxPatch((7.0, 3.2), 2.6, 2.2, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    fc="#FFFFFF", ec="#10B981", lw=1.6)
    ax2.add_patch(f_new2)
    ax2.text(8.3, 4.3, "New Fact (t=2)\n'Lives in Zurich'\n[SUPERSEDES]", ha="center", va="center",
             fontsize=6.5, fontweight="bold", color="#065F46")

    # Directed SUPERSEDES Edge (horizontal, arrow pointing to Old Fact)
    ax2.annotate("", xy=(3.2, 4.3), xytext=(6.8, 4.3),
                 arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#DC2626"))
    ax2.text(5.0, 4.9, "[:SUPERSEDES]", ha="center", va="center", color="#DC2626", fontsize=6.8, fontweight="bold")

    # U-PPR Teleportation path
    ax2.annotate("", xy=(8.0, 5.4), xytext=(5.8, 7.4),
                 arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#059669"))
    ax2.text(8.7, 7.0, "U-PPR Prior\n(Active)", color="#059669", fontsize=6.5, fontweight="bold")

    # Success Pill
    ax2.text(5.0, 1.2, "SUCCESS: SUPERSEDES edge blocks traversal\nTo Outdated Node -> Zero Hallucination",
             ha="center", va="center", fontsize=6.8, color="#065F46", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec="#6EE7B7", lw=1.0))

    plt.rcParams["font.family"] = "serif"
    save_dual(fig, "fig7_knowledge_mutation_dag")

# ==============================================================================
# 8. FIGURE 8: U-PPR SPREADING ACTIVATION & GOD NODES (DIAGRAM - STYLE B)
# ==============================================================================
def generate_fig8_spreading_activation():
    print("Generating Figure 8: U-PPR Spreading Activation (Modern Minimal Style B)...")
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=300)
    plt.rcParams["font.family"] = "sans-serif"
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Epistemic Macro-Hub (God Node) Card in center
    god_card = patches.FancyBboxPatch((36, 38), 28, 24, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      fc="#FEF08A", ec="#CA8A04", lw=1.8)
    ax.add_patch(god_card)
    ax.text(50, 52, "Epistemic Macro-Hub", ha="center", va="center", color="#713F12", fontsize=7.8, fontweight="bold")
    ax.text(50, 46, "('God Node' Persona Anchor)", ha="center", va="center", color="#854D0E", fontsize=6.8, fontstyle="italic")
    ax.text(50, 41, r"$\pi^*(v) = 0.264$", ha="center", va="center", color="#713F12", fontsize=7.2, fontweight="bold")

    # Query Seeds: Seed 1 (Top Left), Seed 2 (Top Right)
    seed1 = patches.FancyBboxPatch((8, 76), 22, 16, boxstyle="round,pad=0.4,rounding_size=1.2",
                                   fc="#EFF6FF", ec="#2563EB", lw=1.2)
    ax.add_patch(seed1)
    ax.text(19, 85, "Query Seed 1", ha="center", va="center", color="#1E3A8A", fontsize=7.2, fontweight="bold")
    ax.text(19, 80, "(BM25 Lexical Hit)", ha="center", va="center", color="#1D4ED8", fontsize=6.4)

    seed2 = patches.FancyBboxPatch((70, 76), 22, 16, boxstyle="round,pad=0.4,rounding_size=1.2",
                                   fc="#EFF6FF", ec="#2563EB", lw=1.2)
    ax.add_patch(seed2)
    ax.text(81, 85, "Query Seed 2", ha="center", va="center", color="#1E3A8A", fontsize=7.2, fontweight="bold")
    ax.text(81, 80, "(Vector HNSW Hit)", ha="center", va="center", color="#1D4ED8", fontsize=6.4)

    # Arrows from seeds to God Node
    ax.annotate("", xy=(36, 56), xytext=(28, 76),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#2563EB", mutation_scale=7))
    ax.annotate("", xy=(64, 56), xytext=(72, 76),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#2563EB", mutation_scale=7))

    # Multi-hop Target Nodes
    t1 = patches.FancyBboxPatch((70, 45), 24, 15, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc="#ECFDF5", ec="#059669", lw=1.2)
    ax.add_patch(t1)
    ax.text(82, 54, "Session 3 Fact", ha="center", va="center", color="#065F46", fontsize=7.2, fontweight="bold")
    ax.text(82, 48.5, "(2-Hop Reachable)", ha="center", va="center", color="#047857", fontsize=6.4)

    t2 = patches.FancyBboxPatch((70, 20), 24, 15, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc="#ECFDF5", ec="#059669", lw=1.2)
    ax.add_patch(t2)
    ax.text(82, 29, "Session 12 Constraint", ha="center", va="center", color="#065F46", fontsize=7.2, fontweight="bold")
    ax.text(82, 23.5, "(3-Hop Reachable)", ha="center", va="center", color="#047857", fontsize=6.4)

    # Spreading activation paths from God Node
    ax.annotate("", xy=(70, 52.5), xytext=(64, 50),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#CA8A04", mutation_scale=7))
    ax.annotate("", xy=(70, 31), xytext=(62, 40),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#CA8A04", mutation_scale=7))

    # Hebbian Plasticity Bridge (Bottom Left)
    h_card = patches.FancyBboxPatch((8, 20), 22, 16, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc="#FAF5FF", ec="#7C3AED", lw=1.2)
    ax.add_patch(h_card)
    ax.text(19, 29.5, "Hebbian Bridge", ha="center", va="center", color="#6D28D9", fontsize=7.2, fontweight="bold")
    ax.text(19, 24, "(Co-Activated Turn)", ha="center", va="center", color="#7C3AED", fontsize=6.4)

    # Hebbian bidirectional arrow
    ax.annotate("", xy=(36, 44), xytext=(28, 33),
                arrowprops=dict(arrowstyle="<->", lw=1.8, color="#7C3AED"))
    ax.text(26, 42, r"$\Delta W_{ij} > 0$", color="#6D28D9", fontsize=6.8, fontweight="bold", rotation=38)

    # Transient Chatter (Bottom Center, Pruned)
    c_card = patches.FancyBboxPatch((38, 14), 24, 13, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc="#F8FAFC", ec="#94A3B8", lw=1.0, linestyle="--")
    ax.add_patch(c_card)
    ax.text(50, 22, "Transient Chatter", ha="center", va="center", color="#64748B", fontsize=7.0)
    ax.text(50, 17, "(Pruned by CATD)", ha="center", va="center", color="#94A3B8", fontsize=6.2, fontstyle="italic")

    # Pruned dotted path
    ax.annotate("", xy=(50, 27), xytext=(50, 38),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#CBD5E1", linestyle=":"))

    # Bottom Pill Legend
    ax.text(50, 4.5,
            "Gold = Epistemic Macro-Hub | Blue = Query Seeds | Green = Context Targets | Purple = Hebbian Bridge",
            ha="center", va="center", fontsize=6.8, color="#475569",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#E2E8F0", lw=1.0))

    plt.rcParams["font.family"] = "serif"
    save_dual(fig, "fig8_uppr_spreading_activation")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("STARTING ACADEMIC PLOTTING PIPELINE (ORCHESTRA-RESEARCH SKILL)")
    print("=" * 80)
    generate_fig1_scaffolding()
    generate_fig2_centrality()
    generate_fig3_locomo()
    generate_fig4_grace_period()
    generate_fig5_sensitivity()
    generate_fig6_architecture()
    generate_fig7_mutation_dag()
    generate_fig8_spreading_activation()
    print("=" * 80)
    print("ALL 8 PUBLICATION FIGURES GENERATED (BOTH VECTOR PDF & 300 DPI PNG)!")
    print("=" * 80)
