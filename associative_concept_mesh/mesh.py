"""Core Associative Concept Mesh implementation."""
import re
from typing import Dict, List, Set, Tuple, Optional, Any


class ConceptNode:
    def __init__(self, name: str, tags: Set[str]):
        self.name = name.lower()
        self.tags = set(t.lower() for t in tags)


class AssociativeConceptMesh:
    def __init__(self, min_similarity: float = 0.25):
        self.min_similarity = min_similarity
        self.nodes: Dict[str, ConceptNode] = {}
        self.links: Dict[str, Dict[str, float]] = {}

    def add_concept(self, name: str, tags: List[str]):
        norm_name = name.lower()
        node = ConceptNode(norm_name, set(tags))
        self.nodes[norm_name] = node
        if norm_name not in self.links:
            self.links[norm_name] = {}

        # Recompute similarities with all existing concepts
        for existing_name, existing_node in self.nodes.items():
            if existing_name == norm_name:
                continue
            sim = self._jaccard_similarity(node.tags, existing_node.tags)
            if sim >= self.min_similarity:
                self.links[norm_name][existing_name] = sim
                if existing_name not in self.links:
                    self.links[existing_name] = {}
                self.links[existing_name][norm_name] = sim

    def _jaccard_similarity(self, s1: Set[str], s2: Set[str]) -> float:
        if not s1 or not s2:
            return 0.0
        intersection = len(s1.intersection(s2))
        union = len(s1.union(s2))
        return intersection / float(union) if union > 0 else 0.0

    def expand_query(self, term: str, max_expansions: int = 3) -> List[Tuple[str, float]]:
        norm_term = term.lower()
        if norm_term not in self.links:
            return [(norm_term, 1.0)]

        ranked = sorted(self.links[norm_term].items(), key=lambda x: x[1], reverse=True)
        expansions = [(norm_term, 1.0)] + ranked[:max_expansions]
        return expansions
