import math

import pytest

import jgrapht as jg
from helpers import both, build

# 0 -> 1 -> 3, 0 -> 2 -> 3, 0 -> 3, plus 1 -> 2
DIAMOND = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 3), (1, 2)]
DIAMOND_W = [1.0, 1.0, 2.0, 2.0, 5.0, 1.0]


# ------------------------------------------------------------ extra single-source algorithms


@both
@pytest.mark.parametrize("alg", ["dijkstra", "bidirectional_dijkstra", "delta_stepping"])
@pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
def test_nonnegative_algorithms_agree(sparse, alg, directed):
    g = build(4, DIAMOND, DIAMOND_W, directed=directed, sparse=sparse)
    p = jg.shortest_path(g, 0, 3, algorithm=alg)
    assert p.vertices == [0, 1, 3] and p.weight == 2.0
    d = jg.single_source_distances(g, 0, algorithm=alg)
    assert d[0] == 0.0 and d[3] == 2.0 and math.isclose(d[2], 2.0 if directed else 2.0)


@both
def test_bfs_ignores_weights(sparse):
    g = build(4, DIAMOND, DIAMOND_W, directed=True, sparse=sparse)
    p = jg.shortest_path(g, 0, 3, algorithm="bfs")
    assert p.vertices == [0, 3] and p.weight == 1.0 and p.edges == [4]


@both
def test_unreachable_in_new_algorithms(sparse):
    g = build(3, [(0, 1)], [1.0], directed=True, sparse=sparse)
    for alg in ("bidirectional_dijkstra", "bfs", "delta_stepping"):
        assert jg.shortest_path(g, 0, 2, algorithm=alg) is None


# ------------------------------------------------------------ k shortest paths


def k_shortest_cases():
    # Eppstein needs a simple directed graph, which SparseGraph (a multigraph by type) is not
    return [
        pytest.param("yen", False, id="yen-Graph"),
        pytest.param("yen", True, id="yen-SparseGraph"),
        pytest.param("eppstein", False, id="eppstein-Graph"),
    ]


@pytest.mark.parametrize("alg,sparse", k_shortest_cases())
def test_k_shortest_paths(sparse, alg):
    g = build(4, DIAMOND, DIAMOND_W, directed=True, sparse=sparse, multi=False, loops=False)
    paths = jg.k_shortest_paths(g, 0, 3, 5, algorithm=alg)
    assert [p.weight for p in paths] == [2.0, 4.0, 4.0, 5.0]
    assert paths[0].vertices == [0, 1, 3]
    assert {tuple(p.vertices) for p in paths[1:3]} == {(0, 2, 3), (0, 1, 2, 3)}
    assert paths[3].vertices == [0, 3]
    assert [p.weight for p in jg.k_shortest_paths(g, 0, 3, 2, algorithm=alg)] == [2.0, 4.0]
    assert jg.k_shortest_paths(g, 0, 3, 0, algorithm=alg) == []


@both
def test_eppstein_requires_a_simple_directed_graph(sparse):
    g = build(4, DIAMOND, DIAMOND_W, directed=True, sparse=sparse)  # allows multi-edges, loops
    if not sparse:
        g_simple = build(4, DIAMOND, DIAMOND_W, directed=True, multi=False, loops=False)
        assert len(jg.k_shortest_paths(g_simple, 0, 3, 2, algorithm="eppstein")) == 2
    with pytest.raises(jg.GraphError):
        jg.k_shortest_paths(g, 0, 3, 2, algorithm="eppstein")


@both
def test_k_shortest_paths_edges_are_consistent(sparse):
    g = build(4, DIAMOND, DIAMOND_W, directed=True, sparse=sparse)
    for p in jg.k_shortest_paths(g, 0, 3, 4):
        assert math.isclose(sum(g.edge_weight(e) for e in p.edges), p.weight)
        assert [g.edge_source(e) for e in p.edges] == p.vertices[:-1]


@both
def test_k_shortest_paths_errors(sparse):
    g = build(4, DIAMOND, DIAMOND_W, directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.k_shortest_paths(g, 0, 3, 2, algorithm="nope")
    with pytest.raises(jg.GraphError):
        jg.k_shortest_paths(g, 0, 9, 2)


# ------------------------------------------------------------ disjoint paths


@both
@pytest.mark.parametrize("alg", ["suurballe", "bhandari"])
def test_k_disjoint_shortest_paths(sparse, alg):
    g = build(4, [(0, 1), (1, 3), (0, 2), (2, 3)], [1.0, 1.0, 2.0, 2.0], directed=True, sparse=sparse)
    paths = jg.k_disjoint_shortest_paths(g, 0, 3, 2, algorithm=alg)
    assert sorted(p.weight for p in paths) == [2.0, 4.0]
    used = [e for p in paths for e in p.edges]
    assert len(used) == len(set(used)) == 4  # edge-disjoint
    assert len(jg.k_disjoint_shortest_paths(g, 0, 3, 5, algorithm=alg)) <= 2


@both
def test_disjoint_paths_need_a_directed_graph(sparse):
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.k_disjoint_shortest_paths(g, 0, 2, 1)


def test_bhandari_allows_negative_weights():
    g = build(4, [(0, 1), (1, 3), (0, 2), (2, 3)], [1.0, -1.0, 2.0, 2.0], directed=True)
    paths = jg.k_disjoint_shortest_paths(g, 0, 3, 2, algorithm="bhandari")
    assert sorted(p.weight for p in paths) == [0.0, 4.0]


# ------------------------------------------------------------ all paths / counting


@both
def test_all_directed_paths(sparse):
    g = build(4, DIAMOND, directed=True, sparse=sparse)
    paths = jg.all_directed_paths(g, 0, 3)
    assert sorted(tuple(p.vertices) for p in paths) == [
        (0, 1, 2, 3),
        (0, 1, 3),
        (0, 2, 3),
        (0, 3),
    ]
    assert all(p.weight == len(p) for p in paths)
    short = jg.all_directed_paths(g, 0, 3, True, 2)
    assert sorted(tuple(p.vertices) for p in short) == [(0, 1, 3), (0, 2, 3), (0, 3)]


@both
def test_all_directed_paths_with_cycle_needs_a_bound(sparse):
    g = build(3, [(0, 1), (1, 0), (1, 2)], directed=True, sparse=sparse)
    simple = jg.all_directed_paths(g, 0, 2)
    assert [p.vertices for p in simple] == [[0, 1, 2]]
    walks = jg.all_directed_paths(g, 0, 2, simple_only=False, max_length=4)
    assert sorted(len(p) for p in walks) == [2, 4]


@both
def test_count_dag_paths(sparse):
    g = build(4, DIAMOND, directed=True, sparse=sparse)
    assert jg.count_dag_paths(g, 0, 3) == 4
    assert jg.count_dag_paths(g, 3, 0) == 0
    assert jg.count_dag_paths(g, 2, 2) == 1


@both
def test_count_dag_paths_big_and_errors(sparse):
    # a chain of 70 "diamonds" has 2**70 paths: needs more than 64 bits
    n = 3 * 70 + 1
    edges = []
    for i in range(70):
        a, b, c, d = 3 * i, 3 * i + 1, 3 * i + 2, 3 * i + 3
        edges += [(a, b), (a, c), (b, d), (c, d)]
    g = build(n, edges, directed=True, sparse=sparse)
    count = jg.count_dag_paths(g, 0, n - 1)
    assert isinstance(count, int) and count == 2**70
    cyc = build(2, [(0, 1), (1, 0)], directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.count_dag_paths(cyc, 0, 1)
    with pytest.raises(jg.GraphError):
        jg.count_dag_paths(build(2, [(0, 1)], sparse=sparse), 0, 1)


# ------------------------------------------------------------ metrics


PATH4 = [(0, 1), (1, 2), (2, 3)]


@both
def test_distance_metrics(sparse):
    g = build(4, PATH4, [1.0, 1.0, 1.0], sparse=sparse)
    assert jg.diameter(g) == 3.0 and jg.radius(g) == 2.0
    assert jg.eccentricities(g) == {0: 3.0, 1: 2.0, 2: 2.0, 3: 3.0}
    assert sorted(jg.graph_center(g)) == [1, 2]
    assert sorted(jg.graph_periphery(g)) == [0, 3]
    assert sorted(jg.graph_pseudo_periphery(g)) == [0, 3]


@both
def test_weights_are_distances(sparse):
    g = build(3, [(0, 1), (1, 2)], [2.0, 5.0], sparse=sparse)
    assert jg.diameter(g) == 7.0 and jg.radius(g) == 5.0
    assert jg.graph_center(g) == [1]


@both
def test_disconnected_has_no_diameter_or_radius(sparse):
    g = build(3, [(0, 1)], [1.0], sparse=sparse)
    assert jg.diameter(g) is None and jg.radius(g) is None


@both
def test_girth(sparse):
    assert jg.girth(build(4, PATH4, sparse=sparse)) is None
    tri = build(4, [(0, 1), (1, 2), (0, 2), (2, 3)], sparse=sparse)
    assert jg.girth(tri) == 3
    square = build(4, [(0, 1), (1, 2), (2, 3), (3, 0)], sparse=sparse)
    assert jg.girth(square) == 4
    assert jg.girth(build(2, [(0, 1), (0, 1)], sparse=sparse)) == 2  # parallel edges
    assert jg.girth(build(2, [(0, 0)], sparse=sparse)) == 1  # self-loop
