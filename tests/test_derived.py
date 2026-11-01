import pytest

import jgrapht as jg

from helpers import build


def labelled(directed=False, weighted=False):
    g = jg.Graph(directed=directed, weighted=weighted, allow_multiple_edges=True)
    for v in "abcd":
        g.add_vertex(v)
    for name, u, v, w in [("e1", "a", "b", 1.0), ("e2", "b", "c", 2.0), ("e3", "c", "d", 3.0), ("e4", "a", "c", 4.0)]:
        g.add_edge(u, v, edge=name, weight=w if weighted else None)
    return g


@pytest.mark.parametrize("sparse", [False, True])
def test_copy_is_independent(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], weights=[1.0, 2.0, 3.0], sparse=sparse)
    c = jg.copy_graph(g)
    assert isinstance(c, jg.Graph) and c.weighted
    assert sorted(c.vertices()) == [0, 1, 2, 3]
    assert [c.edge_weight(e) for e in c.edges()] == [1.0, 2.0, 3.0]
    c.add_vertex(9)
    assert 9 not in g


def test_copy_keeps_flags_and_objects():
    g = jg.Graph(directed=True, weighted=True)
    g.add_vertex("x")
    g.add_vertex("y")
    g.add_edge("x", "y", edge=("my", "edge"), weight=5.0)
    c = jg.copy_graph(g)
    assert c.directed and c.weighted and not c.allow_self_loops and not c.allow_multiple_edges
    assert c.edges() == [("my", "edge")]
    assert c.edge_source(("my", "edge")) == "x" and c.edge_weight(("my", "edge")) == 5.0


def test_induced_subgraph():
    g = labelled(weighted=True)
    s = jg.induced_subgraph(g, ["a", "b", "c"])
    assert sorted(s.vertices()) == ["a", "b", "c"]
    assert sorted(s.edges()) == ["e1", "e2", "e4"]
    assert s.edge_weight("e4") == 4.0
    with pytest.raises(jg.GraphError):
        jg.induced_subgraph(g, ["a", "zzz"])
    sp = build(4, [(0, 1), (1, 2), (2, 3)], sparse=True)
    assert sorted(jg.induced_subgraph(sp, [1, 2, 3]).edges()) == [1, 2]


def test_edge_subgraph():
    g = labelled()
    s = jg.edge_subgraph(g, ["e3", "e1"])
    assert sorted(s.vertices()) == ["a", "b", "c", "d"]
    assert sorted(s.edges()) == ["e1", "e3"]
    s = jg.edge_subgraph(g, ["e1"])
    assert sorted(s.vertices()) == ["a", "b"]
    with pytest.raises(jg.GraphError):
        jg.edge_subgraph(g, ["nope"])


def test_union():
    g1, g2 = jg.Graph(weighted=True), jg.Graph(weighted=True, allow_multiple_edges=True)
    for v in "abc":
        g1.add_vertex(v)
    for v in "bcd":
        g2.add_vertex(v)
    g1.add_edge("a", "b", edge="x", weight=1.0)
    g1.add_edge("b", "c", edge="y", weight=2.0)
    g2.add_edge("b", "c", edge="y", weight=10.0)  # same edge
    g2.add_edge("c", "d", edge="z", weight=5.0)
    g2.add_edge("c", "b", edge="x", weight=7.0)  # same object, other endpoints: a new edge
    u = jg.graph_union(g1, g2)
    assert sorted(u.vertices()) == list("abcd")
    assert u.edge_count() == 4
    assert u.edge_weight("y") == 12.0 and u.edge_weight("x") == 1.0 and u.edge_weight("z") == 5.0
    assert sorted(u.edge_weight(e) for e in u.edges()) == [1.0, 5.0, 7.0, 12.0]
    for how, expected in [("first", 2.0), ("second", 10.0), ("min", 2.0), ("max", 10.0)]:
        assert jg.graph_union(g1, g2, weights=how).edge_weight("y") == expected
    with pytest.raises(jg.GraphError):
        jg.graph_union(g1, g2, weights="bogus")
    with pytest.raises(jg.GraphError):
        jg.graph_union(g1, jg.Graph(directed=True))


def test_union_unweighted_and_mixed():
    a = build(3, [(0, 1)])
    b = build(3, [(1, 2)], weights=[2.0])
    u = jg.graph_union(a, b)
    assert u.weighted and u.edge_count() == 2
    assert sorted(u.edge_weight(e) for e in u.edges()) == [1.0, 2.0]
    # edge 0 of both graphs is the same object but not the same edge
    assert len(set(u.edges())) == 2


def test_as_undirected_and_reverse():
    d = jg.Graph(directed=True)
    for v in range(3):
        d.add_vertex(v)
    d.add_edge(0, 1, edge="f")
    d.add_edge(1, 0, edge="g")
    d.add_edge(1, 2, edge="h")
    u = jg.as_undirected(d)
    assert not u.directed and u.allow_multiple_edges and u.edge_count() == 3
    r = jg.reverse_edges(d)
    assert r.directed
    assert (r.edge_source("h"), r.edge_target("h")) == (2, 1)
    assert (r.edge_source("f"), r.edge_target("f")) == (1, 0)
    assert jg.reverse_edges(u).directed is False
    s = jg.reverse_edges(build(3, [(0, 1), (1, 2)], directed=True, sparse=True))
    assert sorted((s.edge_source(e), s.edge_target(e)) for e in s.edges()) == [(1, 0), (2, 1)]


def test_weights_copies():
    g = labelled()
    w = jg.as_weighted(g, {"e1": 5.0, "e2": 6.0}, default=0.5)
    assert w.weighted
    assert [w.edge_weight(e) for e in ("e1", "e2", "e3", "e4")] == [5.0, 6.0, 0.5, 0.5]
    assert jg.as_weighted(g, lambda e: len(e) * 2.0).edge_weight("e1") == 4.0
    assert jg.as_weighted(g, 3).edge_weight("e3") == 3.0
    assert not jg.as_unweighted(w).weighted
    path = jg.shortest_path(jg.as_weighted(g, {"e1": 1, "e2": 1, "e4": 10, "e3": 1}), "a", "d")
    assert path.vertices == ["a", "b", "c", "d"] and path.weight == 3.0


def test_derived_graphs_feed_algorithms():
    g = jg.complete_graph(5)
    s = jg.induced_subgraph(g, [0, 1, 2])
    assert jg.number_of_triangles(s) == 1
    assert jg.diameter(jg.as_undirected(jg.path_graph(5, directed=True))) == 4


def test_unmodifiable_graph_reads_and_refuses_writes():
    g = jg.Graph()
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b", edge="e1", weight=None)
    u = jg.as_unmodifiable(g)
    assert u.edge_count() == 1 and len(u) == 3 and "a" in u and sorted(u) == ["a", "b", "c"]
    assert (u.edge_source("e1"), u.edge_target("e1")) == ("a", "b")
    assert u.degree_of("a") == 1 and u.edges_between("a", "b") == ["e1"]
    assert not u.directed and not u.weighted and u.graph is g
    for call in (
        lambda: u.add_vertex("z"),
        lambda: u.new_vertex(),
        lambda: u.remove_vertex("a"),
        lambda: u.add_edge("a", "c"),
        lambda: u.remove_edge("e1"),
        lambda: u.set_edge_weight("e1", 2.0),
    ):
        with pytest.raises(jg.GraphError):
            call()
    assert g.edge_count() == 1 and "z" not in g  # nothing changed


def test_unmodifiable_graph_is_live_and_feeds_algorithms():
    g = jg.Graph()
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b")
    u = jg.as_unmodifiable(g)
    assert len(jg.connected_components(u)) == 2
    g.add_edge("b", "c")  # the owner's change is visible
    assert u.edge_count() == 2 and len(jg.connected_components(u)) == 1
    assert jg.shortest_path(u, "a", "c").vertices == ["a", "b", "c"]
    s = jg.as_unmodifiable(jg.SparseGraph(3, [(0, 1), (1, 2)], directed=True))
    assert jg.shortest_path(s, 0, 2).vertices == [0, 1, 2]
    with pytest.raises(jg.GraphError):
        jg.stoer_wagner_minimum_cut(s)  # a directed graph, so undirected-only algorithms refuse
    assert jg.is_isomorphic(jg.as_unmodifiable(jg.path_graph(3)), jg.path_graph(3))


def test_unmodifiable_graph_rejects_other_objects():
    with pytest.raises(TypeError):
        jg.as_unmodifiable(jg.as_unmodifiable(jg.path_graph(2)))
    with pytest.raises(TypeError):
        jg.as_unmodifiable([1, 2])
