"""Unit tests for associative-concept-mesh."""
import unittest
from associative_concept_mesh.mesh import AssociativeConceptMesh


class TestAssociativeConceptMesh(unittest.TestCase):
    def test_add_and_link_concepts(self):
        mesh = AssociativeConceptMesh(min_similarity=0.3)
        mesh.add_concept("c1", ["ai", "agents", "python"])
        mesh.add_concept("c2", ["ai", "agents", "crdt"])
        self.assertIn("c2", mesh.links["c1"])
        self.assertGreater(mesh.links["c1"]["c2"], 0.3)

    def test_expand_query(self):
        mesh = AssociativeConceptMesh(min_similarity=0.2)
        mesh.add_concept("testing", ["code", "qa", "unit"])
        mesh.add_concept("pytest", ["code", "qa", "fixtures"])
        exp = mesh.expand_query("testing")
        names = [x[0] for x in exp]
        self.assertIn("testing", names)
        self.assertIn("pytest", names)
