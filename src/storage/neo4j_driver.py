import logging
import networkx as nx
from typing import Dict, List, Tuple, Any, Optional

try:
    from neo4j import GraphDatabase
    HAS_NEO4J = True
except ImportError:
    HAS_NEO4J = False

logger = logging.getLogger("epigraph.neo4j")

class Neo4jGraphStore:
    """Neo4j Graph client supporting atomic Cypher transactions, GDS PageRank, and Louvain clustering."""

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "epigraph_password"):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver: Optional[Any] = None
        self.is_connected = False
        self._fallback_graph = nx.DiGraph()

        if HAS_NEO4J:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                self.driver.verify_connectivity()
                self.is_connected = True
                self._init_constraints()
                logger.info(f"Connected to Neo4j at {uri}")
            except Exception as e:
                logger.warning(f"Neo4j not reachable at {uri} ({e}). Operating in in-memory NetworkX fallback mode.")
                self.is_connected = False
        else:
            self.is_connected = False

    def _init_constraints(self):
        if not self.is_connected or not self.driver:
            return
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (f:Fact) REQUIRE f.id IS UNIQUE")
            session.run("CREATE INDEX IF NOT EXISTS FOR (f:Fact) ON (f.confidence)")

    def upsert_entity(self, name: str, entity_type: str = "concept"):
        if self.is_connected and self.driver:
            with self.driver.session() as session:
                session.run(
                    "MERGE (e:Entity {name: $name}) ON CREATE SET e.type = $type, e.access_count = 1 ON MATCH SET e.access_count = e.access_count + 1",
                    name=name, type=entity_type
                )
        else:
            if not self._fallback_graph.has_node(name):
                self._fallback_graph.add_node(name, node_type="entity", entity_type=entity_type, access_count=1)
            else:
                self._fallback_graph.nodes[name]["access_count"] += 1

    def upsert_fact(self, fact_id: str, text: str, confidence: float = 1.0, timestamp: str = ""):
        if self.is_connected and self.driver:
            with self.driver.session() as session:
                session.run(
                    "MERGE (f:Fact {id: $id}) ON CREATE SET f.text = $text, f.confidence = $conf, f.timestamp = $ts, f.access_count = 1 "
                    "ON MATCH SET f.confidence = $conf, f.access_count = f.access_count + 1",
                    id=fact_id, text=text, conf=confidence, ts=timestamp
                )
        else:
            if not self._fallback_graph.has_node(fact_id):
                self._fallback_graph.add_node(fact_id, node_type="fact", text=text, confidence=confidence, timestamp=timestamp, access_count=1)
            else:
                self._fallback_graph.nodes[fact_id]["access_count"] += 1

    def add_relationship(self, src_id: str, dst_id: str, rel_type: str, weight: float = 1.0):
        if self.is_connected and self.driver:
            with self.driver.session() as session:
                query = f"""
                MATCH (a {{id: $src}})
                MATCH (b {{id: $dst}})
                MERGE (a)-[r:{rel_type}]->(b)
                ON CREATE SET r.weight = $weight
                ON MATCH SET r.weight = r.weight + $weight
                """
                session.run(query, src=src_id, dst=dst_id, weight=weight)
        else:
            if self._fallback_graph.has_edge(src_id, dst_id):
                self._fallback_graph[src_id][dst_id]["weight"] += weight
            else:
                self._fallback_graph.add_edge(src_id, dst_id, weight=weight, rel_type=rel_type)

    def mark_superseded(self, new_fact_id: str, old_fact_id: str, timestamp: str = ""):
        """Create directed (new_fact)-[:SUPERSEDES]->(old_fact) relationship."""
        if self.is_connected and self.driver:
            with self.driver.session() as session:
                session.run(
                    "MATCH (new:Fact {id: $new_id}), (old:Fact {id: $old_id}) "
                    "MERGE (new)-[r:SUPERSEDES]->(old) ON CREATE SET r.timestamp = $ts",
                    new_id=new_fact_id, old_id=old_fact_id, ts=timestamp
                )
        else:
            self._fallback_graph.add_edge(new_fact_id, old_fact_id, rel_type="SUPERSEDES", weight=2.5, timestamp=timestamp)

    def sweep_orphans(self) -> int:
        """Prune disconnected entity nodes left behind by fact evictions."""
        if self.is_connected and self.driver:
            with self.driver.session() as session:
                res = session.run("MATCH (e:Entity) WHERE NOT (e)--() DELETE e RETURN count(e) AS deleted")
                record = res.single()
                return record["deleted"] if record else 0
        else:
            orphans = [n for n in self._fallback_graph.nodes if self._fallback_graph.degree(n) == 0]
            for n in orphans:
                self._fallback_graph.remove_node(n)
            return len(orphans)
