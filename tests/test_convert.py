import pytest

nx = pytest.importorskip("networkx")

import jgrapht as jg  # noqa: E402
from jgrapht.convert import from_nx, to_nx  # noqa: E402


def test_to_nx_undirected_weighted():
    g = jg.Graph(weighted=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=2.0)
    g.add_edge("b", "c", weight=3.5)
    n = to_nx(g)
    assert type(n) is nx.Graph
    assert set(n.nodes) == set("abcd")  # isolated vertices are kept
    assert n["a"]["b"]["weight"] == 2.0 and n["c"]["b"]["weight"] == 3.5
    assert to_nx(g, weight="cost")["a"]["b"]["cost"] == 2.0


def test_to_nx_kinds():
    assert type(to_nx(jg.path_graph(3, directed=True))) is nx.DiGraph
    d = to_nx(jg.path_graph(3, directed=True))
    assert sorted(d.edges) == [(0, 1), (1, 2)] and "weight" not in d[0][1]
    g = jg.Graph(allow_multiple_edges=True)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)
    g.add_edge(1, 2)
    assert type(to_nx(g)) is nx.MultiGraph and to_nx(g).number_of_edges() == 2
    m = jg.Graph(directed=True, allow_multiple_edges=True)
    assert type(to_nx(m)) is nx.MultiDiGraph


def test_to_nx_sparse_and_wrapper():
    s = jg.SparseGraph(3, [(0, 1), (1, 2)], directed=True, weights=[4.0, 5.0])
    n = to_nx(s)
    assert type(n) is nx.DiGraph and n[1][2]["weight"] == 5.0
    assert type(to_nx(jg.SparseGraph(3, [(0, 1), (0, 1)]))) is nx.MultiGraph
    assert sorted(to_nx(jg.as_unmodifiable(jg.path_graph(3))).edges) == [(0, 1), (1, 2)]


def test_from_nx_unweighted_keeps_objects():
    n = nx.DiGraph()
    n.add_edge("a", "b")
    n.add_edge("b", "c")
    n.add_node("z")
    g = from_nx(n)
    assert g.directed and not g.weighted and g.allow_self_loops
    assert g.vertices() == ["a", "b", "c", "z"] and g.edge_count() == 2
    e = jg.shortest_path(g, "a", "c")
    assert e.vertices == ["a", "b", "c"]


def test_from_nx_weights_and_multigraph():
    n = nx.MultiGraph()
    n.add_edge(1, 2, weight=2.5)
    n.add_edge(1, 2)  # no weight attribute: weight 1.0
    n.add_edge(2, 2, weight=4)
    g = from_nx(n)
    assert g.weighted and g.allow_multiple_edges and not g.directed
    assert sorted(g.edge_weight(e) for e in g.edges()) == [1.0, 2.5, 4.0]
    assert from_nx(n, weight="cost").weighted is False


def test_from_nx_sparse():
    n = nx.Graph()
    n.add_edge("x", "y", weight=3)
    n.add_edge("y", "z", weight=4)
    s = from_nx(n, sparse=True)
    assert isinstance(s, jg.SparseGraph) and s.weighted
    assert [(s.edge_source(e), s.edge_target(e), s.edge_weight(e)) for e in s.edges()] == [
        (0, 1, 3.0),
        (1, 2, 4.0),
    ]
    assert not from_nx(nx.path_graph(3), sparse=True).weighted


def test_round_trip():
    g = jg.Graph(directed=True, weighted=True)
    for v in range(4):
        g.add_vertex(v)
    g.add_edge(0, 1, weight=1.0)
    g.add_edge(1, 2, weight=2.0)
    g.add_edge(2, 0, weight=3.0)
    back = from_nx(to_nx(g))
    assert back.directed and back.weighted
    assert sorted(back.vertices()) == [0, 1, 2, 3]
    assert sorted(
        (back.edge_source(e), back.edge_target(e), back.edge_weight(e)) for e in back.edges()
    ) == [(0, 1, 1.0), (1, 2, 2.0), (2, 0, 3.0)]
    assert jg.shortest_path(back, 0, 2).weight == 3.0


def test_algorithms_agree_with_networkx():
    n = nx.gnp_random_graph(30, 0.15, seed=3)
    g = from_nx(n)
    assert len(jg.connected_components(g)) == nx.number_connected_components(n)


# ---- pydot ----

pydot = pytest.importorskip("pydot")

from jgrapht.convert import from_pydot, to_pydot  # noqa: E402


def dot(text):
    return pydot.graph_from_dot_data(text)[0]


def test_to_pydot_undirected_and_directed():
    g = jg.path_graph(3)
    d = to_pydot(g)
    assert d.get_type() == "graph"
    text = d.to_string()
    assert "0 -- 1" in text and "1 -- 2" in text
    assert "digraph" in to_pydot(jg.path_graph(3, directed=True), name="X").to_string()


def test_to_pydot_weights_and_multiple_edges():
    g = jg.Graph(weighted=True, allow_multiple_edges=True)
    for v in "ab":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=1.5)
    g.add_edge("a", "b", weight=2.5)
    text = to_pydot(g, weight="w").to_string()
    assert text.count("a -- b") == 2 and "w=1.5" in text and "w=2.5" in text
    assert not to_pydot(g).get_strict()
    assert to_pydot(jg.SparseGraph(2, [(0, 1)], weights=[3.0])).to_string().count("weight=3.0") == 1


def test_from_pydot_basic():
    g = from_pydot(dot("digraph { a -> b; b -> c [weight=2.5]; d; }"))
    assert g.directed and g.weighted
    assert sorted(g.vertices()) == ["a", "b", "c", "d"]  # declared nodes first, then the others
    assert sorted(g.edge_weight(e) for e in g.edges()) == [1.0, 2.5]


def test_from_pydot_unweighted_quoted_and_groups():
    g = from_pydot(dot('graph { "node one" -- "node two"; {x y} -- z; node [shape=box]; }'))
    assert not g.directed and not g.weighted
    assert set(g.vertices()) == {"node one", "node two", "x", "y", "z"}
    assert g.edge_count() == 3  # the group {x y} -- z is two edges


def test_from_pydot_strict_and_parallel_edges():
    assert from_pydot(dot("graph { a -- b; a -- b; }")).allow_multiple_edges
    assert not from_pydot(dot("strict graph { a -- b; }")).allow_multiple_edges
    ignored = from_pydot(dot("graph { a -- b [weight=heavy]; }"))
    assert not ignored.weighted  # a non-numeric weight is ignored


def test_from_pydot_sparse_and_round_trip():
    s = from_pydot(dot("digraph { a -> b; b -> c; }"), sparse=True)
    assert isinstance(s, jg.SparseGraph) and s.directed and s.edge_count() == 2
    g = jg.Graph(directed=True, weighted=True)
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=4.0)
    g.add_edge("b", "c", weight=5.0)
    back = from_pydot(dot(to_pydot(g).to_string()))
    assert back.directed and back.weighted
    assert sorted((back.edge_source(e), back.edge_target(e), back.edge_weight(e)) for e in back.edges()) == [
        ("a", "b", 4.0),
        ("b", "c", 5.0),
    ]


# ---- attributes ----


def test_to_nx_copies_attributes():
    g = jg.Graph(directed=True, weighted=True, allow_multiple_edges=True)
    for v in "ab":
        g.add_vertex(v)
    e1 = g.add_edge("a", "b", weight=1.5)
    e2 = g.add_edge("a", "b", weight=2.5)
    g.vertex_attrs["a"]["color"] = "red"
    g.edge_attrs[e1]["kind"] = "road"
    g.edge_attrs[e2]["weight"] = "ignored"  # the real weight wins over an attribute of that name
    g.graph_attrs["name"] = "demo"
    n = to_nx(g)
    assert n.graph == {"name": "demo"} and n.nodes["a"] == {"color": "red"} and n.nodes["b"] == {}
    assert n["a"]["b"][0] == {"kind": "road", "weight": 1.5}
    assert n["a"]["b"][1]["weight"] == 2.5
    n.nodes["a"]["color"] = "blue"  # the dicts are copies
    assert g.vertex_attrs["a"]["color"] == "red"
    assert to_nx(g, weight="cost")["a"]["b"][0]["cost"] == 1.5


def test_to_nx_attributes_of_sparse_and_simple_graphs():
    s = jg.SparseGraph(3, [(0, 1), (1, 2)])
    s.vertex_attrs[2]["x"] = 1
    s.edge_attrs[1]["y"] = 2
    n = to_nx(s)
    assert n.nodes[2] == {"x": 1} and n[1][2] == {"y": 2} and n[0][1] == {}
    plain = jg.path_graph(3)
    plain.edge_attrs[0]["z"] = 3
    assert to_nx(plain)[0][1] == {"z": 3}


def test_from_nx_copies_attributes():
    n = nx.MultiDiGraph(name="demo")
    n.add_node("a", color="red")
    n.add_node("b")
    n.add_edge("a", "b", weight=2.0, kind="road")
    n.add_edge("a", "b", kind="rail")
    g = from_nx(n)
    assert g.graph_attrs == {"name": "demo"}
    assert g.vertex_attrs.items() == [("a", {"color": "red"})]
    assert [g.edge_attrs.get(e) for e in g.edges()] == [{"kind": "road"}, {"kind": "rail"}]
    assert [g.edge_weight(e) for e in g.edges()] == [2.0, 1.0]  # the weight is not an attribute
    g.vertex_attrs["a"]["color"] = "blue"
    assert n.nodes["a"]["color"] == "red"


def test_from_nx_sparse_attributes():
    n = nx.Graph(title="t")
    n.add_node("x", k=1)
    n.add_edge("x", "y", w=5.0, tag="a")
    s = from_nx(n, sparse=True)
    assert s.graph_attrs == {"title": "t"}
    assert s.vertex_attrs.items() == [(0, {"k": 1})]
    assert s.edge_attrs.items() == [(0, {"w": 5.0, "tag": "a"})] and not s.weighted
    weighted = from_nx(n, weight="w", sparse=True)  # now "w" is the weight, not an attribute
    assert weighted.edge_weight(0) == 5.0 and weighted.edge_attrs.items() == [(0, {"tag": "a"})]


def test_nx_round_trip_keeps_attributes():
    n = nx.DiGraph(name="g")
    n.add_node(1, label="one")
    n.add_edge(1, 2, weight=3.0, color="red")
    back = to_nx(from_nx(n))
    assert back.graph == {"name": "g"} and back.nodes[1] == {"label": "one"}
    assert back[1][2] == {"weight": 3.0, "color": "red"}


def test_pydot_attributes():
    g = jg.Graph(directed=True, weighted=True)
    for v in "ab":
        g.add_vertex(v)
    e = g.add_edge("a", "b", weight=4.0)
    g.vertex_attrs["a"].update(color="red", size=3)
    g.edge_attrs[e]["label"] = "road"
    g.graph_attrs.update(name="net", rankdir="LR")
    d = to_pydot(g)
    text = d.to_string()
    assert d.get_name() == "net" and "rankdir=LR" in text and "color=red" in text and "size=3" in text
    back = from_pydot(dot(text))
    assert back.graph_attrs == {"rankdir": "LR", "name": "net"}
    assert back.vertex_attrs["a"] == {"color": "red", "size": "3"}  # DOT values are strings
    assert back.edge_attrs.items()[0][1] == {"label": "road"} and back.edge_weight(0) == 4.0
    assert to_pydot(g, name="other").get_name() == "other"
    s = from_pydot(dot('digraph { a [color=red]; a -> b [label="x y"]; }'), sparse=True)
    assert s.vertex_attrs.items() == [(0, {"color": "red"})] and s.edge_attrs[0] == {"label": "x y"}
