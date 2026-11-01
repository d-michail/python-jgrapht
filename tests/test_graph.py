import pytest

import jgrapht as jg


def test_vertices_and_edges():
    g = jg.Graph()
    for v in ["a", "b", ("t", 1)]:
        assert g.add_vertex(v)
    assert not g.add_vertex("a")
    assert len(g) == 3 and "a" in g and "z" not in g
    e = g.add_edge("a", "b")
    assert g.edge_source(e) == "a" and g.edge_target(e) == "b"
    assert e == 0  # fresh integer edge object when none is given
    assert g.add_edge("b", "a") is None  # parallel edge forbidden
    assert g.edges() == [e] and g.edge_count() == 1
    assert g.degree_of("a") == 1
    assert g.neighbors_of("a") == ["b"]
    assert g.remove_vertex("a") and g.edge_count() == 0
    assert g.vertices() == ["b", ("t", 1)]


def test_hashable_edges():
    g = jg.Graph(allow_multiple_edges=True, weighted=True)
    for v in "ab":
        g.add_vertex(v)
    assert g.add_edge("a", "b", edge="road", weight=2.5) == "road"
    assert g.add_edge("a", "b", edge=("t", 7)) == ("t", 7)
    assert g.add_edge("a", "b", edge="road") is None  # same edge, same endpoints
    assert g.edges() == ["road", ("t", 7)]
    assert g.edge_weight("road") == 2.5 and g.edge_weight(("t", 7)) == 1.0
    g.set_edge_weight("road", 4.0)
    assert g.edge_weight("road") == 4.0
    assert set(g.edges_between("b", "a")) == {"road", ("t", 7)}
    assert g.contains_edge("road") and not g.contains_edge("rail")
    assert g.remove_edge("road") and not g.remove_edge("road")
    with pytest.raises(jg.GraphError):
        g.edge_source("road")
    g.add_vertex("c")
    g.add_edge("a", "c", edge="x")
    g.remove_vertex("a")
    assert g.edges() == [] and not g.contains_edge("x")
    p = jg.shortest_path(weighted_edges(), "a", "c")
    assert p.edges == ["ab", "bc"]


def weighted_edges():
    g = jg.Graph(weighted=True)
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b", "ab", 1.0)
    g.add_edge("b", "c", "bc", 1.0)
    g.add_edge("a", "c", "ac", 5.0)
    return g


def test_errors():
    g = jg.Graph()
    g.add_vertex(1)
    with pytest.raises(jg.GraphError):
        g.add_edge(1, 2)
    with pytest.raises(jg.GraphError):
        g.add_edge(1, 1)
    with pytest.raises(jg.GraphError):
        g.add_edge(1, 1, weight=2.0)
    assert issubclass(jg.GraphError, ValueError)


def test_multigraph_directed():
    g = jg.Graph(directed=True, allow_multiple_edges=True, allow_self_loops=True)
    g.add_vertex("x")
    g.add_vertex("y")
    e1, e2 = g.add_edge("x", "y"), g.add_edge("x", "y")
    assert e1 != e2 and len(g.edges_between("x", "y")) == 2
    assert g.edges_between("y", "x") == []
    assert g.add_edge("x", "x") is not None
    assert g.in_degree_of("y") == 2


def test_new_vertex():
    g = jg.Graph()
    assert [g.new_vertex(), g.new_vertex()] == [0, 1]


def weighted():
    g = jg.Graph(weighted=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=1.0)
    g.add_edge("b", "c", weight=2.0)
    g.add_edge("a", "c", weight=5.0)
    g.add_edge("c", "d", weight=1.0)
    return g


def test_shortest_path():
    g = weighted()
    p = jg.shortest_path(g, "a", "d")
    assert p.vertices == ["a", "b", "c", "d"] and p.weight == 4.0 and len(p) == 3
    assert jg.single_source_distances(g, "a") == {"a": 0.0, "b": 1.0, "c": 3.0, "d": 4.0}
    g.add_vertex("iso")
    assert jg.shortest_path(g, "a", "iso") is None


def test_traversal_and_components():
    g = weighted()
    g.add_vertex("iso")
    assert jg.bfs(g, "a")[0] == "a" and set(jg.bfs(g, "a")) == set("abcd")
    assert set(jg.dfs(g, "a")) == set("abcd")
    comps = [set(c) for c in jg.connected_components(g)]
    assert {"iso"} in comps and set("abcd") in comps


def test_scc():
    g = jg.Graph(directed=True)
    for v in range(4):
        g.add_vertex(v)
    for u, v in [(0, 1), (1, 0), (1, 2), (2, 3), (3, 2)]:
        g.add_edge(u, v)
    assert sorted(sorted(c) for c in jg.strongly_connected_components(g)) == [[0, 1], [2, 3]]
    with pytest.raises(jg.GraphError):
        jg.strongly_connected_components(jg.Graph())


@pytest.mark.parametrize("alg", ["kruskal", "prim", "boruvka"])
def test_mst(alg):
    w, edges = jg.minimum_spanning_tree(weighted(), alg)
    assert w == 4.0 and len(edges) == 3
