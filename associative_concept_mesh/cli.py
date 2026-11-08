"""CLI for associative-concept-mesh."""
import sys
import argparse
from .mesh import AssociativeConceptMesh


def main():
    parser = argparse.ArgumentParser(description="Associative Concept Mesh CLI")
    parser.add_argument("--demo", action="store_true", help="Run associative concept expansion demo")
    args = parser.parse_args()

    if args.demo:
        mesh = AssociativeConceptMesh(min_similarity=0.2)
        mesh.add_concept("auth", ["security", "tokens", "identity", "login"])
        mesh.add_concept("oauth2", ["security", "tokens", "identity", "pkce"])
        mesh.add_concept("database", ["storage", "sql", "tables"])

        expanded = mesh.expand_query("auth", max_expansions=2)
        print("Associative Query Expansion for 'auth':")
        for concept, score in expanded:
            print(f"  - {concept} (similarity: {score:.2f})")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
