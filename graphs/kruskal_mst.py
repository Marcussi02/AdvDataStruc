"""Kruskal's minimum spanning tree (forest) on a disjoint-set structure.

Input file format::

    V E
    u v w      (E lines, one undirected weighted edge each)

Vertex ids may be 0-based or 1-based; ids up to V are accepted.

Usage::

    python kruskal_mst.py graph.txt
"""

import sys


class DisjointSet:
    """Union-find with union by height and path compression.

    parent[x] >= 0 is x's parent; parent[x] < 0 marks a root, and its
    magnitude is the (upper bound on the) height of that tree.
    """

    def __init__(self, n):
        self.parent = [-1] * n

    def findSmallest(self, a):
        """Return the root of a's set, compressing the path on the way."""
        root = a
        while self.parent[root] >= 0:
            root = self.parent[root]
        while self.parent[a] >= 0:
            nxt = self.parent[a]
            self.parent[a] = root
            a = nxt
        return root

    def unionByHeight(self, a, b):
        """Merge the sets holding a and b. Return False if already merged."""
        rootA = self.findSmallest(a)
        rootB = self.findSmallest(b)
        if rootA == rootB:
            return False
        heightA = -self.parent[rootA]
        heightB = -self.parent[rootB]
        if heightA > heightB:
            self.parent[rootB] = rootA
        elif heightB > heightA:
            self.parent[rootA] = rootB
        else:
            self.parent[rootA] = rootB
            self.parent[rootB] = -(heightB + 1)
        return True


def kruskalMST(num_vertices, edges):
    """Return (total_weight, tree_edges) for a minimum spanning forest.

    edges is an iterable of (u, v, w). tree_edges are (u, v, w) in the
    order they were accepted, which is non-decreasing weight.
    """
    edges = list(edges)
    size = num_vertices
    for u, v, _ in edges:
        size = max(size, u + 1, v + 1)
    ds = DisjointSet(size)

    total = 0
    tree = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if ds.unionByHeight(u, v):
            tree.append((u, v, w))
            total += w
            if len(tree) == num_vertices - 1:
                break
    return total, tree


def parse_graph(lines):
    """Parse 'V E' then E lines of 'u v w' into (V, [(u, v, w), ...])."""
    rows = [line.split() for line in lines if line.strip()]
    if not rows:
        raise ValueError("empty graph file")
    V, E = int(rows[0][0]), int(rows[0][1])
    if len(rows) - 1 < E:
        raise ValueError(f"expected {E} edges, found {len(rows) - 1}")
    edges = []
    for row in rows[1:E + 1]:
        u, v, w = int(row[0]), int(row[1]), int(row[2])
        edges.append((u, v, w))
    return V, edges


def readFile(fileName):
    with open(fileName, "r") as f:
        return f.read().splitlines()


def main(argv):
    if len(argv) != 2:
        print("usage: python kruskal_mst.py <graph file>", file=sys.stderr)
        return 1
    V, edges = parse_graph(readFile(argv[1]))
    total, tree = kruskalMST(V, edges)
    lines = [str(total)] + [f"{u} {v} {w}" for u, v, w in tree]
    with open("output_kruskal.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
