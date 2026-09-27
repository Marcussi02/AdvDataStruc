import itertools
import random

from kruskal_mst import DisjointSet, kruskalMST, parse_graph


def brute_force_mst_weight(n, edges):
    """Minimum weight over all spanning trees (connected graphs only)."""
    best = None
    for subset in itertools.combinations(edges, n - 1):
        ds = DisjointSet(n)
        if all(ds.unionByHeight(u, v) for u, v, _ in subset):
            w = sum(e[2] for e in subset)
            best = w if best is None else min(best, w)
    return best


def random_connected_graph(rng, n, extra):
    edges = []
    for v in range(1, n):
        edges.append((rng.randrange(v), v, rng.randint(1, 20)))
    for _ in range(extra):
        u, v = rng.sample(range(n), 2)
        edges.append((u, v, rng.randint(1, 20)))
    rng.shuffle(edges)
    return edges


def test_small_known_graph():
    V, edges = parse_graph(["4 5", "0 1 1", "1 2 2", "2 3 3", "0 3 4", "0 2 5"])
    total, tree = kruskalMST(V, edges)
    assert total == 6
    assert tree == [(0, 1, 1), (1, 2, 2), (2, 3, 3)]


def test_weights_are_sorted_numerically_not_as_strings():
    # "10" < "9" as strings; Kruskal must pick 9 then 10 by value
    V, edges = parse_graph(["3 3", "0 1 10", "1 2 9", "0 2 100"])
    assert kruskalMST(V, edges)[0] == 19


def test_one_based_vertices():
    V, edges = parse_graph(["3 3", "1 2 4", "2 3 1", "1 3 2"])
    assert kruskalMST(V, edges)[0] == 3


def test_disconnected_graph_gives_forest():
    total, tree = kruskalMST(4, [(0, 1, 5), (2, 3, 7)])
    assert total == 12 and len(tree) == 2


def test_matches_brute_force():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(2, 6)
        edges = random_connected_graph(rng, n, rng.randint(0, 5))
        total, tree = kruskalMST(n, edges)
        assert len(tree) == n - 1
        assert total == brute_force_mst_weight(n, edges)


def test_union_find_path_compression():
    ds = DisjointSet(6)
    for a, b in [(0, 1), (1, 2), (3, 4), (2, 4)]:
        ds.unionByHeight(a, b)
    root = ds.findSmallest(0)
    assert all(ds.findSmallest(x) == root for x in range(5))
    assert ds.findSmallest(5) == 5
    assert ds.unionByHeight(0, 4) is False
