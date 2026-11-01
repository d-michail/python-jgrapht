import pytest

import jgrapht as jg

SPARSE = pytest.mark.parametrize("sparse", [False, True], ids=["graph", "sparse"])


def kind(sparse):
    return jg.SparseGraph if sparse else jg.Graph


def nv(g):
    return len(list(g.vertices()))


def ne(g):
    return g.edge_count()


def pairs(g):
    return sorted(
        tuple(sorted((g.edge_source(e), g.edge_target(e)))) if not g.directed else (g.edge_source(e), g.edge_target(e))
        for e in g.edges()
    )


def degrees(g):
    return sorted(g.degree_of(v) for v in g.vertices())


@SPARSE
def test_basic_families(sparse):
    g = jg.empty_graph(5, sparse=sparse)
    assert isinstance(g, kind(sparse)) and (nv(g), ne(g)) == (5, 0)
    g = jg.path_graph(6, sparse=sparse)
    assert (nv(g), ne(g)) == (6, 5) and degrees(g) == [1, 1, 2, 2, 2, 2]
    g = jg.ring_graph(6, sparse=sparse)
    assert (nv(g), ne(g)) == (6, 6) and set(degrees(g)) == {2}
    g = jg.star_graph(6, sparse=sparse)
    assert (nv(g), ne(g)) == (6, 5) and degrees(g) == [1] * 5 + [5]
    g = jg.wheel_graph(6, sparse=sparse)
    assert (nv(g), ne(g)) == (6, 10)
    g = jg.complete_graph(6, sparse=sparse)
    assert (nv(g), ne(g)) == (6, 15) and set(degrees(g)) == {5}
    g = jg.complete_bipartite_graph(3, 4, sparse=sparse)
    assert (nv(g), ne(g)) == (7, 12)
    g = jg.grid_graph(3, 4, sparse=sparse)
    assert (nv(g), ne(g)) == (12, 17)
    g = jg.hypercube_graph(4, sparse=sparse)
    assert (nv(g), ne(g)) == (16, 32) and set(degrees(g)) == {4}
    g = jg.generalized_petersen_graph(5, 2, sparse=sparse)
    assert (nv(g), ne(g)) == (10, 15) and set(degrees(g)) == {3}
    g = jg.windmill_graph(3, 4, sparse=sparse)
    assert nv(g) == 1 + 3 * 3


@SPARSE
def test_directed_variants(sparse):
    g = jg.complete_graph(4, directed=True, sparse=sparse)
    assert g.directed and ne(g) == 12
    g = jg.path_graph(4, directed=True, sparse=sparse)
    assert pairs(g) == [(0, 1), (1, 2), (2, 3)]
    g = jg.ring_graph(4, directed=True, sparse=sparse)
    assert ne(g) == 4 and g.directed


@SPARSE
def test_weight_matrices(sparse):
    g = jg.graph_from_weight_matrix([[0, 2, 0], [2, 0, 3], [0, 3, 0]], sparse=sparse)
    assert ne(g) >= 2
    assert sorted(g.edge_weight(e) for e in g.edges())[-1] == 3
    g = jg.bipartite_graph_from_weight_matrix([[1, 2], [3, 4]], sparse=sparse)
    assert nv(g) == 4 and ne(g) == 4


@SPARSE
def test_random_graphs_are_deterministic(sparse):
    for make in (
        lambda s: jg.gnp_random_graph(30, 0.2, seed=s, sparse=sparse),
        lambda s: jg.gnm_random_graph(30, 50, seed=s, sparse=sparse),
        lambda s: jg.barabasi_albert_graph(3, 2, 30, seed=s, sparse=sparse),
        lambda s: jg.watts_strogatz_graph(30, 4, 0.3, seed=s, sparse=sparse),
        lambda s: jg.random_regular_graph(20, 4, seed=s, sparse=sparse),
        lambda s: jg.planted_partition_graph(3, 5, 0.9, 0.1, seed=s, sparse=sparse),
        lambda s: jg.gnm_random_bipartite_graph(5, 6, 10, seed=s, sparse=sparse),
        lambda s: jg.gnp_random_bipartite_graph(5, 6, 0.5, seed=s, sparse=sparse),
        lambda s: jg.linearized_chord_diagram_graph(20, 2, seed=s, sparse=sparse),
        lambda s: jg.scale_free_graph(25, seed=s, sparse=sparse),
        lambda s: jg.kleinberg_small_world_graph(5, 1, 1, 2, seed=s, sparse=sparse),
        lambda s: jg.barabasi_albert_forest(3, 20, seed=s, sparse=sparse),
        lambda s: jg.prufer_tree(15, seed=s, sparse=sparse),
    ):
        a, b = make(7), make(7)
        assert isinstance(a, kind(sparse))
        assert pairs(a) == pairs(b)


@SPARSE
def test_random_sizes(sparse):
    g = jg.gnm_random_graph(20, 30, seed=1, sparse=sparse)
    assert (nv(g), ne(g)) == (20, 30)
    g = jg.gnm_random_graph(20, 30, directed=True, seed=1, sparse=sparse)
    assert g.directed and ne(g) == 30
    g = jg.gnp_random_graph(10, 1.0, seed=1, sparse=sparse)
    assert ne(g) == 45
    g = jg.gnp_random_graph(10, 0.0, seed=1, sparse=sparse)
    assert ne(g) == 0
    g = jg.random_regular_graph(20, 3, seed=2, sparse=sparse)
    assert set(degrees(g)) == {3}
    g = jg.prufer_tree(12, seed=3, sparse=sparse)
    assert (nv(g), ne(g)) == (12, 11)
    g = jg.prufer_tree(5, sequence=[0, 0, 0], sparse=sparse)
    assert degrees(g) == [1, 1, 1, 1, 4]
    g = jg.gnm_random_bipartite_graph(4, 5, 7, seed=1, sparse=sparse)
    assert (nv(g), ne(g)) == (9, 7)


def test_different_seeds_differ():
    a = jg.gnm_random_graph(40, 80, seed=1)
    b = jg.gnm_random_graph(40, 80, seed=2)
    assert pairs(a) != pairs(b)
    c = jg.gnm_random_graph(40, 80)
    assert ne(c) == 80


def test_graph_flags_match_edges():
    g = jg.gnm_random_graph(5, 12, loops=True, multiple_edges=True, seed=1)
    assert ne(g) == 12


def test_generated_graph_is_usable():
    g = jg.grid_graph(4, 4)
    assert jg.diameter(g) == 6
    s = jg.grid_graph(4, 4, sparse=True)
    assert jg.diameter(s) == 6


def test_invalid_parameters():
    with pytest.raises(jg.GraphError):
        jg.gnm_random_graph(3, 100, seed=1)
    with pytest.raises(jg.GraphError):
        jg.random_regular_graph(5, 3, seed=1)
    with pytest.raises(jg.GraphError):
        jg.named_graph("no_such_graph")


@SPARSE
def test_named_graphs(sparse):
    names = jg.named_graph_names()
    assert len(names) == len(set(names)) == 44 and "petersen" in names
    for name in names:
        g = jg.named_graph(name, sparse=sparse)
        assert isinstance(g, kind(sparse))
        assert nv(g) > 0 and ne(g) > 0
    g = jg.named_graph("petersen", sparse=sparse)
    assert (nv(g), ne(g)) == (10, 15) and set(degrees(g)) == {3}
    assert jg.girth(g) == 5
    g = jg.named_graph("zachary_karate_club", sparse=sparse)
    assert (nv(g), ne(g)) == (34, 78)
    g = jg.named_graph("heawood", sparse=sparse)
    assert (nv(g), ne(g)) == (14, 21) and jg.girth(g) == 6
    g = jg.named_graph("frucht", sparse=sparse)
    assert (nv(g), ne(g)) == (12, 18)
    g = jg.named_graph("bull", sparse=sparse)
    assert (nv(g), ne(g)) == (5, 5)


@SPARSE
def test_maximum_flow_network(sparse):
    g, sources, sinks = jg.maximum_flow_network(
        20, 60, 50, min_capacity=1, max_capacity=10, sources=2, sinks=2, seed=5, sparse=sparse
    )
    assert isinstance(g, kind(sparse)) and g.directed and g.weighted
    assert nv(g) == 20 and ne(g) == 60
    assert len(sources) == 2 and len(sinks) == 2
    assert all(g.edge_weight(e) >= 1 for e in g.edges())
    g1, s1, t1 = jg.maximum_flow_network(10, 30, 20, 1, 5, seed=9, sparse=sparse)
    assert (len(s1), len(t1)) == (1, 1)
    flow = jg.maximum_flow(g1, s1[0], t1[0])
    assert flow.value >= 0
    g2, s2, t2 = jg.maximum_flow_network(10, 30, 20, 1, 5, seed=9, sparse=sparse)
    assert pairs(g1) == pairs(g2) and (s1, t1) == (s2, t2)
    assert flow.value == jg.maximum_flow(g1, s1[0], t1[0], algorithm="edmonds_karp").value


@SPARSE
def test_bipartite_matching_network(sparse):
    g, left, right = jg.bipartite_matching_network(10, 20, min_cost=1, max_cost=9, seed=3, sparse=sparse)
    assert isinstance(g, kind(sparse)) and g.directed and g.weighted
    assert nv(g) == 10 and ne(g) == 20
    assert len(left) == 5 and len(right) == 5 and not set(left) & set(right)
    for e in g.edges():
        assert g.edge_source(e) in left and g.edge_target(e) in right


@SPARSE
def test_minimum_cost_flow_network(sparse):
    g, supply, capacity, cost = jg.minimum_cost_flow_network(
        10, 30, 2, 2, 20, 0, 0, 5, 20, 1, 10, 100, 0, seed=4, sparse=sparse
    )
    assert isinstance(g, kind(sparse)) and g.directed
    assert nv(g) == 10 and ne(g) == 30
    assert sum(supply.values()) == 0 and sum(v for v in supply.values() if v > 0) == 20
    assert len(capacity) == 30 and len(cost) == 30
    assert all(5 <= c <= 20 for c in capacity.values())
    result = jg.minimum_cost_flow(g, supply, capacity, cost)
    assert result.cost >= 0
