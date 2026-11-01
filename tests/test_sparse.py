import pytest

import jgrapht as jg

EDGES = [(0, 1), (1, 2), (0, 2), (2, 3)]
WEIGHTS = [1.0, 2.0, 5.0, 1.0]


def test_basic_queries():
    g = jg.SparseGraph(4, EDGES)
    assert len(g) == 4 and g.edge_count() == 4
    assert g.vertices() == [0, 1, 2, 3] and g.edges() == [0, 1, 2, 3]
    assert (g.edge_source(3), g.edge_target(3)) == (2, 3)
    assert g.degree_of(2) == 3 and sorted(g.neighbors_of(2)) == [0, 1, 3]
    assert g.edges_between(2, 0) == [2]
    assert 3 in g and 4 not in g and "a" not in g
    assert g.edge_weight(0) == 1.0
    with pytest.raises(jg.GraphError):
        g.degree_of(9)
    with pytest.raises(jg.GraphError):
        g.edge_source(9)
    with pytest.raises(jg.GraphError):
        jg.SparseGraph(2, [(0, 5)])
    with pytest.raises(jg.GraphError):
        g.set_edge_weight(0, 2.0)


def test_directed():
    g = jg.SparseGraph(3, [(0, 1), (1, 2), (2, 1)], directed=True)
    assert g.directed and g.out_degree_of(1) == 1 and g.in_degree_of(1) == 2
    assert g.out_edges_of(0) == [0] and g.in_edges_of(1) == [0, 2]
    assert sorted(sorted(c) for c in jg.strongly_connected_components(g)) == [[0], [1, 2]]
    with pytest.raises(jg.GraphError):
        jg.strongly_connected_components(jg.SparseGraph(2, [(0, 1)]))


@pytest.mark.parametrize("directed", [False, True])
def test_algorithms_weighted(directed):
    g = jg.SparseGraph(4, EDGES, directed=directed, weights=WEIGHTS)
    p = jg.shortest_path(g, 0, 3)
    assert p.vertices == [0, 1, 2, 3] and p.edges == [0, 1, 3] and p.weight == 4.0
    assert jg.single_source_distances(g, 0) == {0: 0.0, 1: 1.0, 2: 3.0, 3: 4.0}
    assert jg.bfs(g, 0)[0] == 0 and set(jg.dfs(g, 0)) == {0, 1, 2, 3}
    assert len(jg.connected_components(g)) == 1
    g.set_edge_weight(2, 0.5)
    assert jg.shortest_path(g, 0, 3).weight == 1.5
    if not directed:
        w, edges = jg.minimum_spanning_tree(g, "kruskal")
        assert w == 2.5 and sorted(edges) == [0, 2, 3]


def test_weights_length_mismatch():
    with pytest.raises(jg.GraphError):
        jg.SparseGraph(4, EDGES, weights=[1.0])


def test_algorithm_rejects_other_types():
    with pytest.raises(TypeError):
        jg.bfs("not a graph", 0)
