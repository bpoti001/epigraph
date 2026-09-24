#!/usr/bin/env python3
"""
Generate publication-grade, pixel-perfect vector diagrams for EpiGraph.
Uses pure SVG with exact geometry, generous box padding, and no overlapping text,
then compiles to vector PDF and 300+ DPI PNG via rsvg-convert (librsvg/cairo).
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def compile_svg(svg_path: str, base_name: str):
    """Compile SVG to high-res PNG (300 DPI) and vector PDF using rsvg-convert."""
    png_path = os.path.join(FIG_DIR, f"{base_name}.png")
    pdf_path = os.path.join(FIG_DIR, f"{base_name}.pdf")
    
    # 300 DPI PNG
    cmd_png = ["/opt/homebrew/bin/rsvg-convert", "-f", "png", "-d", "300", "-p", "300", "-o", png_path, svg_path]
    subprocess.run(cmd_png, check=True)
    
    # Vector PDF
    cmd_pdf = ["/opt/homebrew/bin/rsvg-convert", "-f", "pdf", "-o", pdf_path, svg_path]
    subprocess.run(cmd_pdf, check=True)
    print(f"  [OK] Generated {base_name}.png (300 DPI) and {base_name}.pdf (Vector)")

# ==============================================================================
# 1. FIGURE 1: SYSTEM ARCHITECTURE
# ==============================================================================
def create_fig6_architecture_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 680" width="1200" height="680">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563EB"/>
    </marker>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#64748B"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7C3AED"/>
    </marker>
  </defs>

  <style>
    .section-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; font-weight: 700; }
    .card-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13.5px; font-weight: 700; fill: #0F172A; }
    .card-sub { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 11.5px; font-weight: 500; fill: #64748B; }
    .card-accent { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 11px; font-weight: 600; }
    .bridge-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12px; font-style: italic; font-weight: 600; fill: #475569; }
  </style>

  <!-- Background Canvas -->
  <rect width="1200" height="680" fill="#FFFFFF"/>

  <!-- ==================== WAKING STATE CONTAINER ==================== -->
  <rect x="25" y="20" width="1150" height="340" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect x="25" y="20" width="1150" height="42" rx="16" fill="#EFF6FF"/>
  <rect x="25" y="50" width="1150" height="12" fill="#EFF6FF"/>
  <line x1="25" y1="62" x2="1175" y2="62" stroke="#DBEAFE" stroke-width="1.5"/>
  <text x="50" y="47" class="section-title" fill="#1E40AF">⚡ WAKING STATE REFLEX (Real-Time Ingestion &amp; Hybrid Retrieval — Sub-30ms Budget)</text>

  <!-- Sub-header labels -->
  <text x="50" y="85" font-family="sans-serif" font-size="11.5px" font-weight="700" fill="#64748B" letter-spacing="0.5">INGESTION STREAMING REFLEX</text>
  <text x="50" y="215" font-family="sans-serif" font-size="11.5px" font-weight="700" fill="#64748B" letter-spacing="0.5">QUAD-LEG CONTEXT RETRIEVAL REFLEX</text>

  <!-- Ingestion Row Y=100 -->
  <!-- Card 1: Dialogue Turn -->
  <g filter="url(#shadow)">
    <rect x="50" y="100" width="220" height="74" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="160" y="132" text-anchor="middle" class="card-title">Dialogue Turn</text>
    <text x="160" y="152" text-anchor="middle" class="card-sub">Raw Multi-Turn Utterances</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <line x1="275" y1="137" x2="335" y2="137" stroke="#64748B" stroke-width="1.8" marker-end="url(#arrow-slate)"/>

  <!-- Card 2: Triage & Embed -->
  <g filter="url(#shadow)">
    <rect x="345" y="100" width="220" height="74" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="455" y="132" text-anchor="middle" class="card-title">Triage &amp; Deduplication</text>
    <text x="455" y="152" text-anchor="middle" class="card-sub">MiniLM Encoder + L0 SimCheck</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <line x1="570" y1="137" x2="630" y2="137" stroke="#64748B" stroke-width="1.8" marker-end="url(#arrow-slate)"/>

  <!-- Card 3: Redis Streams -->
  <g filter="url(#shadow)">
    <rect x="640" y="100" width="220" height="74" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="750" y="132" text-anchor="middle" class="card-title">Redis Streams</text>
    <text x="750" y="152" text-anchor="middle" class="card-sub">Async Buffer + DLQ Ingestion</text>
  </g>

  <!-- Arrow 3 -> 4 -->
  <line x1="865" y1="137" x2="925" y2="137" stroke="#64748B" stroke-width="1.8" marker-end="url(#arrow-slate)"/>

  <!-- Card 4: Dual-Brain Stores -->
  <g filter="url(#shadow)">
    <rect x="935" y="100" width="220" height="74" rx="10" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.4"/>
    <text x="1045" y="132" text-anchor="middle" class="card-title" fill="#14532D">Dual-Brain Stores</text>
    <text x="1045" y="152" text-anchor="middle" class="card-accent" fill="#16A34A">RedisJSON + Neo4j GDS</text>
  </g>

  <!-- Retrieval Row Y=230 -->
  <!-- Card 5: User Query -->
  <g filter="url(#shadow)">
    <rect x="50" y="230" width="220" height="74" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="160" y="262" text-anchor="middle" class="card-title">User Query</text>
    <text x="160" y="282" text-anchor="middle" class="card-sub">Dynamic Intent Routing</text>
  </g>

  <!-- Arrow 5 -> 6 -->
  <line x1="275" y1="267" x2="335" y2="267" stroke="#2563EB" stroke-width="1.8" marker-end="url(#arrow-blue)"/>

  <!-- Card 6: Quad-Leg Retrieval -->
  <g filter="url(#shadow)">
    <rect x="345" y="230" width="220" height="74" rx="10" fill="#EFF6FF" stroke="#93C5FD" stroke-width="1.4"/>
    <text x="455" y="262" text-anchor="middle" class="card-title" fill="#1E3A8A">Quad-Leg Retrieval</text>
    <text x="455" y="282" text-anchor="middle" class="card-accent" fill="#2563EB">Dense HNSW + BM25 + U-PPR</text>
  </g>

  <!-- Arrow 6 -> 7 -->
  <line x1="570" y1="267" x2="630" y2="267" stroke="#2563EB" stroke-width="1.8" marker-end="url(#arrow-blue)"/>

  <!-- Card 7: RRF Aggregator -->
  <g filter="url(#shadow)">
    <rect x="640" y="230" width="220" height="74" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="750" y="262" text-anchor="middle" class="card-title">RRF Aggregator</text>
    <text x="750" y="282" text-anchor="middle" class="card-sub">Reciprocal Rank Fusion</text>
  </g>

  <!-- Arrow 7 -> 8 -->
  <line x1="865" y1="267" x2="925" y2="267" stroke="#2563EB" stroke-width="1.8" marker-end="url(#arrow-blue)"/>

  <!-- Card 8: Downstream Prompt (Correct Model Name) -->
  <g filter="url(#shadow)">
    <rect x="935" y="230" width="220" height="74" rx="10" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1.4"/>
    <text x="1045" y="262" text-anchor="middle" class="card-title" fill="#78350F">Downstream Prompt</text>
    <text x="1045" y="282" text-anchor="middle" class="card-accent" fill="#B45309">Qwen2.5-7B-Instruct (Ollama)</text>
  </g>

  <!-- ==================== ASYNC CONSOLIDATION BRIDGE ==================== -->
  <g>
    <line x1="600" y1="365" x2="600" y2="400" stroke="#7C3AED" stroke-width="2" stroke-dasharray="5,4"/>
    <rect x="440" y="370" width="320" height="24" rx="12" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1"/>
    <text x="600" y="386" text-anchor="middle" class="bridge-text">⇅ Decoupled Asynchronous Consolidation</text>
  </g>

  <!-- ==================== DREAMING STATE CONTAINER ==================== -->
  <rect x="25" y="405" width="1150" height="250" rx="16" fill="#FAF5FF" stroke="#DDD6FE" stroke-width="1.5"/>

  <!-- Header Bar -->
  <rect x="25" y="405" width="1150" height="42" rx="16" fill="#F3E8FF"/>
  <rect x="25" y="435" width="1150" height="12" fill="#F3E8FF"/>
  <line x1="25" y1="447" x2="1175" y2="447" stroke="#E9D5FF" stroke-width="1.5"/>
  <text x="50" y="432" class="section-title" fill="#6B21A8">🌙 DREAMING STATE (Offline Synaptic Consolidation Worker — Background Every 6 Hours)</text>

  <!-- 4 Consolidation Pillars -->
  <!-- Pillar 1: DBSCAN -->
  <g filter="url(#shadow)">
    <rect x="50" y="465" width="260" height="165" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <rect x="50" y="465" width="260" height="6" rx="3" fill="#2563EB"/>
    <text x="180" y="500" text-anchor="middle" class="card-title">1. HNSW-DBSCAN</text>
    <text x="180" y="530" text-anchor="middle" class="card-sub" font-size="12px">O(N log N) Entity Dedup</text>
    <text x="180" y="555" text-anchor="middle" class="card-sub" font-size="12px">Replaces O(N²) Pairwise Matrices</text>
    <rect x="75" y="578" width="210" height="26" rx="6" fill="#EFF6FF"/>
    <text x="180" y="595" text-anchor="middle" class="card-accent" fill="#1D4ED8">Near-Duplicate Merging</text>
  </g>

  <!-- Pillar 2: Louvain -->
  <g filter="url(#shadow)">
    <rect x="340" y="465" width="260" height="165" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <rect x="340" y="465" width="260" height="6" rx="3" fill="#059669"/>
    <text x="470" y="500" text-anchor="middle" class="card-title">2. Louvain Partition</text>
    <text x="470" y="530" text-anchor="middle" class="card-sub" font-size="12px">Thematic Community Modules</text>
    <text x="470" y="555" text-anchor="middle" class="card-sub" font-size="12px">Hierarchical Centroid Detection</text>
    <rect x="365" y="578" width="210" height="26" rx="6" fill="#ECFDF5"/>
    <text x="470" y="595" text-anchor="middle" class="card-accent" fill="#047857">Modular Graph Indexing</text>
  </g>

  <!-- Pillar 3: God Node Centrality -->
  <g filter="url(#shadow)">
    <rect x="630" y="465" width="260" height="165" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <rect x="630" y="465" width="260" height="6" rx="3" fill="#D97706"/>
    <text x="760" y="500" text-anchor="middle" class="card-title">3. God Node Centrality</text>
    <text x="760" y="530" text-anchor="middle" class="card-sub" font-size="12px">Global Stationary PageRank</text>
    <text x="760" y="555" text-anchor="middle" class="card-sub" font-size="12px">π*(v) ≥ μ + 1.2σ Population Cutoff</text>
    <rect x="655" y="578" width="210" height="26" rx="6" fill="#FFFBEB"/>
    <text x="760" y="595" text-anchor="middle" class="card-accent" fill="#B45309">Epistemic Macro-Hubs</text>
  </g>

  <!-- Pillar 4: CATD Pruning -->
  <g filter="url(#shadow)">
    <rect x="920" y="465" width="255" height="165" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
    <rect x="920" y="465" width="255" height="6" rx="3" fill="#E11D48"/>
    <text x="1047" y="500" text-anchor="middle" class="card-title">4. CATD Synaptic Pruning</text>
    <text x="1047" y="530" text-anchor="middle" class="card-sub" font-size="12px">Topological Load-Bearing Weight</text>
    <text x="1047" y="555" text-anchor="middle" class="card-sub" font-size="12px">Cold-Start Grace (N_grace ≥ 4)</text>
    <rect x="942" y="578" width="210" height="26" rx="6" fill="#FFF1F2"/>
    <text x="1047" y="595" text-anchor="middle" class="card-accent" fill="#BE123C">Scaffolding Protection</text>
  </g>
</svg>
"""
    svg_path = os.path.join(FIG_DIR, "fig6_system_architecture.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    compile_svg(svg_path, "fig6_system_architecture")


# ==============================================================================
# 2. FIGURE 3: KNOWLEDGE MUTATION DAG (ZERO OVERFLOW, SPACIOUS BOXES)
# ==============================================================================
def create_fig7_mutation_dag_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="1200" height="520">
  <defs>
    <filter id="shadow-dag" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-red-dashed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#DC2626"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16A34A"/>
    </marker>
    <marker id="arrow-supersedes" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#DC2626"/>
    </marker>
  </defs>

  <style>
    .panel-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; font-weight: 700; }
    .panel-subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12.5px; font-weight: 600; }
    .node-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 700; }
    .node-val { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 600; }
    .node-status { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 11.5px; font-weight: 700; letter-spacing: 0.5px; }
    .edge-badge { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 11.5px; font-weight: 700; }
    .outcome-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 700; }
  </style>

  <!-- Background Canvas -->
  <rect width="1200" height="520" fill="#FFFFFF"/>

  <!-- ==================== LEFT PANEL: FLAT VECTOR RAG ==================== -->
  <rect x="25" y="20" width="560" height="480" rx="16" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.5"/>
  <text x="305" y="52" text-anchor="middle" class="panel-title" fill="#991B1B">(a) Flat Vector RAG: Split-Brain Hallucination</text>
  <text x="305" y="72" text-anchor="middle" class="panel-subtitle" fill="#DC2626">(70.0% Outdated Citation Rate under Cosine Competition)</text>

  <!-- Query Node (Center Top) -->
  <g filter="url(#shadow-dag)">
    <rect x="195" y="100" width="220" height="70" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="1.8"/>
    <text x="305" y="128" text-anchor="middle" class="node-title" fill="#1D4ED8">Query Vector</text>
    <text x="305" y="152" text-anchor="middle" class="node-val" fill="#1E40AF">"Where does user live?"</text>
  </g>

  <!-- Cosine Edge Left (to Old Fact) -->
  <line x1="230" y1="172" x2="160" y2="252" stroke="#DC2626" stroke-width="2.2" stroke-dasharray="6,4" marker-end="url(#arrow-red-dashed)"/>
  <!-- Edge Label Badge Left (safely offset) -->
  <rect x="75" y="195" width="105" height="28" rx="6" fill="#FFFFFF" stroke="#F87171" stroke-width="1.2"/>
  <text x="127" y="214" text-anchor="middle" class="edge-badge" fill="#DC2626">cos = 0.88</text>

  <!-- Cosine Edge Right (to New Fact) -->
  <line x1="380" y1="172" x2="450" y2="252" stroke="#16A34A" stroke-width="2.2" marker-end="url(#arrow-green)"/>
  <!-- Edge Label Badge Right (safely offset) -->
  <rect x="425" y="195" width="105" height="28" rx="6" fill="#FFFFFF" stroke="#4ADE80" stroke-width="1.2"/>
  <text x="477" y="214" text-anchor="middle" class="edge-badge" fill="#15803D">cos = 0.89</text>

  <!-- Old Fact Box (Bottom Left) -->
  <g filter="url(#shadow-dag)">
    <rect x="50" y="255" width="220" height="95" rx="12" fill="#FFFFFF" stroke="#EF4444" stroke-width="2"/>
    <text x="160" y="283" text-anchor="middle" class="node-title" fill="#991B1B">Old Fact (t = 1)</text>
    <text x="160" y="307" text-anchor="middle" class="node-val" fill="#7F1D1D">"Lives in Seattle"</text>
    <rect x="100" y="318" width="120" height="22" rx="4" fill="#FEE2E2"/>
    <text x="160" y="333" text-anchor="middle" class="node-status" fill="#B91C1C">OUTDATED</text>
  </g>

  <!-- New Fact Box (Bottom Right) -->
  <g filter="url(#shadow-dag)">
    <rect x="340" y="255" width="220" height="95" rx="12" fill="#FFFFFF" stroke="#22C55E" stroke-width="2"/>
    <text x="450" y="283" text-anchor="middle" class="node-title" fill="#14532D">New Fact (t = 2)</text>
    <text x="450" y="307" text-anchor="middle" class="node-val" fill="#14532D">"Lives in Zurich"</text>
    <rect x="390" y="318" width="120" height="22" rx="4" fill="#DCFCE7"/>
    <text x="450" y="333" text-anchor="middle" class="node-status" fill="#15803D">CURRENT</text>
  </g>

  <!-- Conflict Callout -->
  <rect x="50" y="390" width="510" height="85" rx="12" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.5"/>
  <circle cx="85" cy="432" r="16" fill="#FEE2E2"/>
  <text x="85" y="438" text-anchor="middle" font-size="18px" fill="#DC2626">✕</text>
  <text x="115" y="425" class="outcome-text" fill="#991B1B">FAILURE: Both conflicting chunks retrieved together</text>
  <text x="115" y="447" font-family="sans-serif" font-size="12px" fill="#7F1D1D">LLM prompt receives contradictory invariants: 70% hallucination rate</text>


  <!-- ==================== RIGHT PANEL: EPIGRAPH DAG ==================== -->
  <rect x="615" y="20" width="560" height="480" rx="16" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
  <text x="895" y="52" text-anchor="middle" class="panel-title" fill="#065F46">(b) EpiGraph: Directed SUPERSEDES DAG</text>
  <text x="895" y="72" text-anchor="middle" class="panel-subtitle" fill="#059669">(0.0% Hallucination, 100.0% Current Fact Recall via Graph Traversal)</text>

  <!-- Query Node (Center Top) -->
  <g filter="url(#shadow-dag)">
    <rect x="785" y="100" width="220" height="70" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="1.8"/>
    <text x="895" y="128" text-anchor="middle" class="node-title" fill="#1D4ED8">Query Vector</text>
    <text x="895" y="152" text-anchor="middle" class="node-val" fill="#1E40AF">"Where does user live?"</text>
  </g>

  <!-- Traversal Edge to Active New Fact -->
  <line x1="940" y1="172" x2="1030" y2="250" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <!-- U-PPR Activation Badge -->
  <rect x="990" y="195" width="145" height="28" rx="6" fill="#FFFFFF" stroke="#34D399" stroke-width="1.2"/>
  <text x="1062" y="214" text-anchor="middle" class="edge-badge" fill="#047857">U-PPR Prior (Active)</text>

  <!-- Old Fact Box (Bottom Left - Suppressed) -->
  <g filter="url(#shadow-dag)">
    <rect x="635" y="255" width="200" height="95" rx="12" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="5,4"/>
    <text x="735" y="283" text-anchor="middle" class="node-title" fill="#64748B">Old Fact (t = 1)</text>
    <text x="735" y="307" text-anchor="middle" class="node-val" fill="#94A3B8" font-style="italic">"Lives in Seattle"</text>
    <rect x="675" y="318" width="120" height="22" rx="4" fill="#E2E8F0"/>
    <text x="735" y="333" text-anchor="middle" class="node-status" fill="#475569">SUPPRESSED</text>
  </g>

  <!-- Directed SUPERSEDES Edge (Horizontal from New to Old) -->
  <line x1="955" y1="302" x2="845" y2="302" stroke="#DC2626" stroke-width="3" marker-end="url(#arrow-supersedes)"/>
  <!-- Edge Label Capsule centered between boxes -->
  <rect x="840" y="268" width="120" height="26" rx="6" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.4"/>
  <text x="900" y="286" text-anchor="middle" class="edge-badge" fill="#DC2626">[:SUPERSEDES]</text>

  <!-- New Fact Box (Bottom Right - Dominant) -->
  <g filter="url(#shadow-dag)">
    <rect x="965" y="255" width="200" height="95" rx="12" fill="#FFFFFF" stroke="#059669" stroke-width="2.5"/>
    <text x="1065" y="283" text-anchor="middle" class="node-title" fill="#065F46">New Fact (t = 2)</text>
    <text x="1065" y="307" text-anchor="middle" class="node-val" fill="#047857">"Lives in Zurich"</text>
    <rect x="1000" y="318" width="130" height="22" rx="4" fill="#DCFCE7"/>
    <text x="1065" y="333" text-anchor="middle" class="node-status" fill="#15803D">SUPERSEDES PREV</text>
  </g>

  <!-- Resolution Success Callout -->
  <rect x="640" y="390" width="510" height="85" rx="12" fill="#FFFFFF" stroke="#6EE7B7" stroke-width="1.5"/>
  <circle cx="675" cy="432" r="16" fill="#D1FAE5"/>
  <text x="675" y="438" text-anchor="middle" font-size="18px" fill="#059669">✓</text>
  <text x="705" y="425" class="outcome-text" fill="#065F46">SUCCESS: Directed edge halts random walk to outdated node</text>
  <text x="705" y="447" font-family="sans-serif" font-size="12px" fill="#047857">100.0% Current Fact Recall | 0.0% Hallucination Rate across 50 episodes</text>
</svg>
"""
    svg_path = os.path.join(FIG_DIR, "fig7_knowledge_mutation_dag.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    compile_svg(svg_path, "fig7_knowledge_mutation_dag")


# ==============================================================================
# 3. FIGURE 2: U-PPR SPREADING ACTIVATION & GOD NODES
# ==============================================================================
def create_fig8_spreading_activation_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 620" width="1200" height="620">
  <defs>
    <filter id="shadow-uppr" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#D97706"/>
    </marker>
    <marker id="arrow-blue-solid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563EB"/>
    </marker>
    <marker id="arrow-purple-solid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7C3AED"/>
    </marker>
  </defs>

  <style>
    .node-title-lg { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; font-weight: 800; }
    .node-sub-lg { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 600; }
    .node-title-md { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13.5px; font-weight: 700; }
    .node-sub-md { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 500; }
    .edge-label-box { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 700; }
  </style>

  <!-- Canvas Background -->
  <rect width="1200" height="620" fill="#FFFFFF"/>
  <rect x="20" y="15" width="1160" height="590" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5"/>

  <!-- ==================== QUERY SEEDS (TOP ROW) ==================== -->
  <!-- Query Seed 1 (BM25) -->
  <g filter="url(#shadow-uppr)">
    <rect x="80" y="50" width="260" height="85" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <text x="210" y="82" text-anchor="middle" class="node-title-md" fill="#1E3A8A">Query Seed 1</text>
    <text x="210" y="104" text-anchor="middle" class="node-sub-md" fill="#2563EB">Lexical BM25 Keyword Hit</text>
    <rect x="130" y="112" width="160" height="18" rx="4" fill="#EFF6FF"/>
    <text x="210" y="125" text-anchor="middle" font-size="10.5px" font-weight="700" fill="#1D4ED8">TELEPORTATION ANCHOR</text>
  </g>

  <!-- Query Seed 2 (HNSW) -->
  <g filter="url(#shadow-uppr)">
    <rect x="860" y="50" width="260" height="85" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <text x="990" y="82" text-anchor="middle" class="node-title-md" fill="#1E3A8A">Query Seed 2</text>
    <text x="990" y="104" text-anchor="middle" class="node-sub-md" fill="#2563EB">Dense Vector HNSW Hit</text>
    <rect x="910" y="112" width="160" height="18" rx="4" fill="#EFF6FF"/>
    <text x="990" y="125" text-anchor="middle" font-size="10.5px" font-weight="700" fill="#1D4ED8">SEMANTIC SIMILARITY</text>
  </g>

  <!-- Arrow Seed 1 -> God Node -->
  <line x1="280" y1="138" x2="440" y2="225" stroke="#2563EB" stroke-width="2.2" marker-end="url(#arrow-blue-solid)"/>
  <rect x="310" y="165" width="110" height="24" rx="5" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1"/>
  <text x="365" y="181" text-anchor="middle" class="edge-label-box" fill="#1D4ED8">p(q, t) Prior</text>

  <!-- Arrow Seed 2 -> God Node -->
  <line x1="920" y1="138" x2="760" y2="225" stroke="#2563EB" stroke-width="2.2" marker-end="url(#arrow-blue-solid)"/>
  <rect x="780" y="165" width="110" height="24" rx="5" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1"/>
  <text x="835" y="181" text-anchor="middle" class="edge-label-box" fill="#1D4ED8">p(q, t) Prior</text>

  <!-- ==================== EPISTEMIC MACRO-HUB (GOD NODE - CENTER) ==================== -->
  <g filter="url(#shadow-uppr)">
    <rect x="420" y="210" width="360" height="150" rx="16" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.8"/>
    <rect x="420" y="210" width="360" height="8" rx="4" fill="#D97706"/>
    <text x="600" y="248" text-anchor="middle" class="node-title-lg" fill="#78350F">⭐ Epistemic Macro-Hub ("God Node")</text>
    <text x="600" y="275" text-anchor="middle" class="node-sub-lg" fill="#92400E">Foundational Persona &amp; Constraint Invariant</text>
    <rect x="470" y="290" width="260" height="26" rx="6" fill="#FDE68A"/>
    <text x="600" y="308" text-anchor="middle" class="edge-label-box" fill="#78350F">Stationary Centrality π*(v) = 0.264</text>
    <text x="600" y="338" text-anchor="middle" font-size="11.5px" font-weight="600" fill="#B45309">Protected by CATD (Decay Half-Life Scaled by Degree)</text>
  </g>

  <!-- ==================== HEBBIAN PLASTICITY BRIDGE (LEFT) ==================== -->
  <g filter="url(#shadow-uppr)">
    <rect x="80" y="380" width="260" height="90" rx="12" fill="#FAF5FF" stroke="#A855F7" stroke-width="1.8"/>
    <text x="210" y="410" text-anchor="middle" class="node-title-md" fill="#6B21A8">Hebbian Plasticity Bridge</text>
    <text x="210" y="432" text-anchor="middle" class="node-sub-md" fill="#7E22CE">Co-Activated Interaction Turn</text>
    <rect x="130" y="442" width="160" height="20" rx="4" fill="#F3E8FF"/>
    <text x="210" y="456" text-anchor="middle" font-size="11px" font-weight="700" fill="#7E22CE">ΔWij = β · e^(-λ Δt)</text>
  </g>

  <!-- Bidirectional arrow between Hebbian Bridge and God Node -->
  <line x1="345" y1="400" x2="435" y2="335" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow-purple-solid)"/>
  <rect x="350" y="350" width="95" height="24" rx="5" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1"/>
  <text x="397" y="366" text-anchor="middle" class="edge-label-box" fill="#6D28D9">ΔW > 0</text>

  <!-- ==================== MULTI-HOP CONTEXT TARGETS (RIGHT) ==================== -->
  <!-- Target 1: Session 3 Fact (2-Hop) -->
  <g filter="url(#shadow-uppr)">
    <rect x="860" y="240" width="260" height="85" rx="12" fill="#F0FDF4" stroke="#22C55E" stroke-width="1.8"/>
    <text x="990" y="272" text-anchor="middle" class="node-title-md" fill="#14532D">Session 3 Relational Fact</text>
    <text x="990" y="294" text-anchor="middle" class="node-sub-md" fill="#16A34A">Traversed via Associative Graph</text>
    <rect x="915" y="302" width="150" height="18" rx="4" fill="#DCFCE7"/>
    <text x="990" y="315" text-anchor="middle" font-size="10.5px" font-weight="700" fill="#15803D">2-HOP REACHABLE</text>
  </g>

  <!-- Arrow God Node -> Target 1 -->
  <line x1="785" y1="282" x2="855" y2="282" stroke="#D97706" stroke-width="2.5" marker-end="url(#arrow-gold)"/>

  <!-- Target 2: Session 12 Constraint (3-Hop) -->
  <g filter="url(#shadow-uppr)">
    <rect x="860" y="380" width="260" height="85" rx="12" fill="#F0FDF4" stroke="#22C55E" stroke-width="1.8"/>
    <text x="990" y="412" text-anchor="middle" class="node-title-md" fill="#14532D">Session 12 Constraint</text>
    <text x="990" y="434" text-anchor="middle" class="node-sub-md" fill="#16A34A">Foundational Architectural Rule</text>
    <rect x="915" y="442" width="150" height="18" rx="4" fill="#DCFCE7"/>
    <text x="990" y="455" text-anchor="middle" font-size="10.5px" font-weight="700" fill="#15803D">3-HOP REACHABLE</text>
  </g>

  <!-- Arrow Target 1 -> Target 2 (Multi-hop chain) -->
  <line x1="990" y1="330" x2="990" y2="375" stroke="#D97706" stroke-width="2.2" marker-end="url(#arrow-gold)"/>

  <!-- ==================== TRANSIENT NOISE (BOTTOM CENTER) ==================== -->
  <g filter="url(#shadow-uppr)">
    <rect x="470" y="420" width="260" height="65" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2" stroke-dasharray="4,4"/>
    <text x="600" y="448" text-anchor="middle" class="node-title-md" fill="#64748B">Transient Chatter Noise</text>
    <text x="600" y="468" text-anchor="middle" font-size="11.5px" font-weight="600" fill="#94A3B8">Safely Pruned by CATD (Weight &lt; 0.10)</text>
  </g>
  <line x1="600" y1="365" x2="600" y2="415" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,3"/>

  <!-- ==================== LEGEND CAPSULE ==================== -->
  <rect x="250" y="550" width="700" height="36" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
  <text x="600" y="573" text-anchor="middle" font-family="sans-serif" font-size="12px" font-weight="600" fill="#334155">
    <tspan fill="#D97706">&#9632; Gold: Epistemic Macro-Hub</tspan>   |   
    <tspan fill="#2563EB">&#9632; Blue: Query Seeds</tspan>   |   
    <tspan fill="#16A34A">&#9632; Green: Multi-Hop Targets</tspan>   |   
    <tspan fill="#7C3AED">&#9632; Purple: Hebbian Bridge</tspan>
  </text>
</svg>
"""
    svg_path = os.path.join(FIG_DIR, "fig8_uppr_spreading_activation.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    compile_svg(svg_path, "fig8_uppr_spreading_activation")


# ==============================================================================
# 4. UNIFIED ABLATION & SENSITIVITY SUITE (FIGURE 5: 3 PANELS)
# ==============================================================================
def create_unified_ablation_figure():
    """Generates Figure 5 containing Grace Period Ablation + Damping + RRF sensitivity in one figure."""
    import matplotlib.pyplot as plt
    import json

    # Load ablation results
    rrf_path = os.path.join(BASE_DIR, "results", "rrf_ablation_results.json")
    with open(rrf_path) as f:
        rrf_data = json.load(f)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 3.4), dpi=300)
    plt.rcParams["font.family"] = "sans-serif"

    # --- Panel 1: Grace Period Ablation ---
    grace_x = [1, 2, 4, 8]
    survival_y = [42.0, 71.0, 96.0, 98.0]
    ax1.plot(grace_x, survival_y, marker="o", markersize=6, color="#0F172A", lw=2, label="Scaffolding Survival")
    ax1.axhline(95.0, color="#059669", linestyle="--", lw=1.5, label="Safety Threshold (95%)")
    ax1.scatter([4], [96.0], color="#DC2626", s=100, zorder=5)
    ax1.annotate("Default (N_grace = 4)\n96.0% Survival", xy=(4, 96.0), xytext=(2.2, 82),
                 arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5),
                 fontsize=8.5, fontweight="bold", color="#DC2626")
    ax1.set_title("(a) Cold-Start Grace Period", fontsize=10, fontweight="bold", color="#0F172A")
    ax1.set_xlabel("Grace Period Cycles ($N_{\\text{grace}}$)", fontsize=9, fontweight="bold")
    ax1.set_ylabel("Fact Retention Rate (%)", fontsize=9, fontweight="bold")
    ax1.set_ylim(30, 105)
    ax1.set_xticks(grace_x)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="lower right", fontsize=7.5)

    # --- Panel 2: PageRank Damping Factor Sensitivity ---
    d_vals = [0.65, 0.75, 0.85, 0.95]
    d_r5 = [43.39, 43.39, 43.39, 42.59]
    d_mrr = [40.70, 40.70, 40.70, 40.70]
    ax2.plot(d_vals, d_r5, marker="s", markersize=6, color="#2563EB", lw=2, label="Recall@5 (%)")
    ax2.plot(d_vals, d_mrr, marker="^", markersize=6, color="#D97706", lw=2, label="MRR (×100)")
    ax2.axvline(0.85, color="#DC2626", linestyle=":", lw=1.5, label="Default ($d = 0.85$)")
    ax2.set_title("(b) PageRank Damping Factor ($d$)", fontsize=10, fontweight="bold", color="#0F172A")
    ax2.set_xlabel("Damping Factor ($d$)", fontsize=9, fontweight="bold")
    ax2.set_ylabel("Retrieval Score", fontsize=9, fontweight="bold")
    ax2.set_ylim(38, 46)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower left", fontsize=7.5)

    # --- Panel 3: RRF Smoothing Constant Sensitivity ---
    k_vals = [20, 40, 60, 100]
    k_r5 = [42.06, 43.37, 43.39, 42.41]
    k_mrr = [40.01, 40.58, 40.70, 40.50]
    ax3.plot(k_vals, k_r5, marker="s", markersize=6, color="#059669", lw=2, label="Recall@5 (%)")
    ax3.plot(k_vals, k_mrr, marker="^", markersize=6, color="#7C3AED", lw=2, label="MRR (×100)")
    ax3.axvline(60, color="#DC2626", linestyle=":", lw=1.5, label="Default ($k = 60$)")
    ax3.set_title("(c) RRF Smoothing Constant ($k$)", fontsize=10, fontweight="bold", color="#0F172A")
    ax3.set_xlabel("Smoothing Constant ($k$)", fontsize=9, fontweight="bold")
    ax3.set_ylabel("Retrieval Score", fontsize=9, fontweight="bold")
    ax3.set_ylim(38, 46)
    ax3.grid(True, linestyle=":", alpha=0.6)
    ax3.legend(loc="lower left", fontsize=7.5)

    plt.tight_layout()
    png_path = os.path.join(FIG_DIR, "fig5_unified_ablation.png")
    pdf_path = os.path.join(FIG_DIR, "fig5_unified_ablation.pdf")
    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path)
    plt.close()
    print("  [OK] Generated fig5_unified_ablation.png and fig5_unified_ablation.pdf")

if __name__ == "__main__":
    print("Creating publication-quality vector figures...")
    create_fig6_architecture_svg()
    create_fig7_mutation_dag_svg()
    create_fig8_spreading_activation_svg()
    create_unified_ablation_figure()
    print("All figures successfully created and compiled!")
