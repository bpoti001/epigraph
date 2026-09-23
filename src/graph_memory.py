import math
import re
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Set, Optional
from networkx.algorithms.community import louvain_communities

class GraphNode:
    def __init__(self, node_id: str, label: str, node_type: str, session_id: Optional[str] = None, timestamp: Optional[str] = None):
        self.node_id = node_id
        self.label = label
        self.node_type = node_type  # 'turn', 'entity', 'session_anchor', 'topic'
        self.session_id = session_id
        self.timestamp = timestamp
        self.access_count = 0
        self.last_access_cycle = 0
        self.created_cycle = 0
        self.pagerank = 0.0
        self.community_id = 0
        self.confidence = 1.0
        self.embedding: Optional[np.ndarray] = None
        self.is_god_node = False

class DynamicCognitiveGraph:
    def __init__(self, damping: float = 0.85):
        self.damping = damping
        self.nodes: Dict[str, GraphNode] = {}
        self.graph = nx.DiGraph()
        self.current_cycle = 0
        self.communities: List[Set[str]] = []
        self.god_nodes: Set[str] = set()

    def add_node(self, node_id: str, label: str, node_type: str, session_id: Optional[str] = None, timestamp: Optional[str] = None, embedding: Optional[np.ndarray] = None) -> GraphNode:
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.label = label
            if embedding is not None:
                node.embedding = embedding
            return node

        node = GraphNode(node_id, label, node_type, session_id, timestamp)
        node.created_cycle = self.current_cycle
        node.embedding = embedding
        self.nodes[node_id] = node
        self.graph.add_node(node_id, node_type=node_type, label=label)
        return node

    def add_edge(self, src: str, dst: str, rel_type: str, weight: float = 1.0):
        if src not in self.nodes or dst not in self.nodes:
            return
        if self.graph.has_edge(src, dst):
            self.graph[src][dst]["weight"] += weight
            self.graph[src][dst]["rel_type"] = rel_type
        else:
            self.graph.add_edge(src, dst, weight=weight, rel_type=rel_type)

    def record_usage(self, accessed_node_ids: List[str]):
        """Hebbian plasticity: reinforce co-activated nodes and edges."""
        valid_ids = [nid for nid in accessed_node_ids if nid in self.nodes]
        for nid in valid_ids:
            self.nodes[nid].access_count += 1
            self.nodes[nid].last_access_cycle = self.current_cycle

        # Hebbian edge reinforcement for co-activated pairs
        for i in range(len(valid_ids)):
            for j in range(i + 1, len(valid_ids)):
                u, v = valid_ids[i], valid_ids[j]
                # Reinforce both directions
                if self.graph.has_edge(u, v):
                    self.graph[u][v]["weight"] += 0.5
                else:
                    self.graph.add_edge(u, v, weight=1.0, rel_type="HEBBIAN_REINFORCED")

                if self.graph.has_edge(v, u):
                    self.graph[v][u]["weight"] += 0.5
                else:
                    self.graph.add_edge(v, u, weight=1.0, rel_type="HEBBIAN_REINFORCED")

    def partition_communities(self):
        """Partition memory into Louvain communities using undirected projection."""
        if self.graph.number_of_nodes() < 2:
            return

        undirected = self.graph.to_undirected()
        try:
            self.communities = louvain_communities(undirected, weight="weight", seed=42)
            for comm_idx, comm_set in enumerate(self.communities):
                for nid in comm_set:
                    if nid in self.nodes:
                        self.nodes[nid].community_id = comm_idx
        except Exception:
            pass

    def identify_god_nodes(self, std_mult: float = 1.5):
        """Identify Epistemic Macro-Hubs ('God Nodes') using global centrality and degree."""
        if self.graph.number_of_nodes() == 0:
            return

        # Compute unpersonalized PageRank for structural centrality
        try:
            raw_pr = nx.pagerank(self.graph, alpha=self.damping, weight="weight", max_iter=100)
            for nid, score in raw_pr.items():
                if nid in self.nodes:
                    self.nodes[nid].pagerank = score
        except Exception:
            for nid in self.nodes:
                self.nodes[nid].pagerank = 1.0 / len(self.nodes)

        scores = np.array([self.nodes[nid].pagerank for nid in self.nodes])
        mu, sigma = float(scores.mean()), float(scores.std())
        threshold = mu + std_mult * sigma

        self.god_nodes = set()
        for nid, node in self.nodes.items():
            deg = self.graph.degree(nid)
            # Must have high PageRank and at least 3 connections
            if node.pagerank >= threshold and deg >= 3:
                node.is_god_node = True
                self.god_nodes.add(nid)
            else:
                node.is_god_node = False

    def compute_uppr(self, seed_node_ids: List[str], seed_weights: Optional[List[float]] = None) -> Dict[str, float]:
        """Usage-Modulated Personalized PageRank (U-PPR)."""
        N = self.graph.number_of_nodes()
        if N == 0:
            return {}

        personalization = {}
        total_p = 0.0

        # 1. Teleportation to query seeds
        seed_dict = {}
        if seed_node_ids:
            if seed_weights is None:
                seed_weights = [1.0] * len(seed_node_ids)
            for nid, sw in zip(seed_node_ids, seed_weights):
                if nid in self.nodes:
                    seed_dict[nid] = sw

        # 2. Add usage intensity & God Node anchor teleportation
        usage_mass = 0.35  # fraction allocated to epistemic usage & god nodes
        seed_mass = 0.65 if seed_dict else 0.0
        if not seed_dict:
            usage_mass = 1.0

        # Seed component
        if seed_dict:
            sum_sw = sum(seed_dict.values())
            for nid, sw in seed_dict.items():
                personalization[nid] = personalization.get(nid, 0.0) + seed_mass * (sw / sum_sw)

        # Usage & God Node component
        usage_weights = {}
        for nid, node in self.nodes.items():
            base_usage = math.log1p(node.access_count) * math.exp(-0.05 * (self.current_cycle - node.last_access_cycle))
            if node.is_god_node:
                base_usage += 1.5  # God node gravitational anchor
            if base_usage > 0:
                usage_weights[nid] = base_usage

        sum_uw = sum(usage_weights.values())
        if sum_uw > 0:
            for nid, uw in usage_weights.items():
                personalization[nid] = personalization.get(nid, 0.0) + usage_mass * (uw / sum_uw)
        else:
            # Fallback uniform
            for nid in self.nodes:
                personalization[nid] = personalization.get(nid, 0.0) + usage_mass * (1.0 / N)

        # Normalize
        norm_sum = sum(personalization.values())
        if norm_sum > 0:
            personalization = {k: v / norm_sum for k, v in personalization.items()}
        else:
            personalization = {k: 1.0 / N for k in self.nodes}

        # Run NetworkX PPR
        try:
            uppr_scores = nx.pagerank(
                self.graph,
                alpha=self.damping,
                personalization=personalization,
                weight="weight",
                max_iter=80,
                tol=1e-5
            )
        except Exception:
            uppr_scores = {nid: 1.0 / N for nid in self.nodes}

        return uppr_scores

    def apply_catd(self, grace_cycles: int = 3) -> List[str]:
        """Consolidation-Activated Topology Decay (CATD)."""
        self.current_cycle += 1
        self.partition_communities()
        self.identify_god_nodes()

        evicted = []
        for nid, node in list(self.nodes.items()):
            age = self.current_cycle - node.created_cycle
            if age <= grace_cycles:
                continue

            # Fact-type parameterization
            if node.node_type == "identity":
                base_lambda = 0.0001
            elif node.node_type == "preference":
                base_lambda = 0.0008
            elif node.node_type in ["entity", "session_anchor"]:
                base_lambda = 0.015
            else:
                base_lambda = 0.08

            deg = self.graph.degree(nid) if self.graph.has_node(nid) else 0
            pr = node.pagerank
            topo_score = 0.4 * (pr * 10.0) + 0.3 * min(2.0, deg / 3.0) + 0.3 * (1.5 if node.is_god_node else 0.2)

            # CATD retention half-life modulated by topology score
            cycles_dormant = max(0, self.current_cycle - node.last_access_cycle)
            lambda_eff = base_lambda * math.exp(-2.0 * topo_score)
            node.confidence = max(0.05, math.exp(-lambda_eff * cycles_dormant))

            # Eviction criteria: low confidence, stagnant access, low degree, not a God Node, and not a core identity/preference
            if node.confidence <= 0.10 and cycles_dormant > 4 and deg <= 1 and not node.is_god_node and node.node_type not in ["identity", "preference"]:
                evicted.append(nid)

        for nid in evicted:
            if self.graph.has_node(nid):
                self.graph.remove_node(nid)
            if nid in self.nodes:
                del self.nodes[nid]

        return evicted
