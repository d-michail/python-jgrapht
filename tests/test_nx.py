import pytest

nx = pytest.importorskip("networkx")

from jgrapht import create_graph
from jgrapht.convert import to_nx, from_nx


def test_int_graph_to_nx():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    nxg = to_nx(g)

    assert len(nxg.nodes) == 6
    assert nxg.nodes == g.vertices
    assert len(nxg.edges) == 7

    for e in g.edges:
        u, v, _ = g.edge_tuple(e)
        assert nxg.has_edge(u, v)

    assert nxg.edges[2, 3]["weight"] == 100.0
    assert not nx.is_directed(nxg)


def test_any_hashable_graph_to_nx():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "0")

    e34 = g.add_edge("3", "4")
    g.add_edge("4", "5")
    g.add_edge("5", "3")

    g.add_edge("2", "3", edge="e23_1", weight=100.0)
    g.add_edge("2", "3", edge="e23_2", weight=50.0)

    g.vertex_attrs["5"]["name"] = "v5"
    g.vertex_attrs["4"]["name"] = "v4"

    g.edge_attrs[e34]["name"] = "e34"

    nxg = to_nx(g)

    assert len(nxg.nodes) == 6
    assert nxg.nodes == g.vertices
    assert len(nxg.edges) == 8

    for e in g.edges:
        u, v, _ = g.edge_tuple(e)
        assert nxg.has_edge(u, v)

    assert nxg.edges["2", "3", 0]["weight"] == 100.0
    assert nxg.edges["2", "3", 1]["weight"] == 50.0
    assert nxg.edges["3", "4", 0]["name"] == "e34"
    assert nxg.nodes["5"]["name"] == "v5"
    assert nxg.nodes["4"]["name"] == "v4"
    assert not nx.is_directed(nxg)


def test_any_hashable_no_multiple_edges_graph_to_nx():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "0")

    e34 = g.add_edge("3", "4")
    g.add_edge("4", "5")
    g.add_edge("5", "3")

    g.add_edge("2", "3", edge="e23")

    g.vertex_attrs["5"]["name"] = "v5"
    g.vertex_attrs["4"]["name"] = "v4"

    g.edge_attrs["e23"]["name"] = "e23"
    g.edge_attrs[e34]["name"] = "e34"

    nxg = to_nx(g)

    assert len(nxg.nodes) == 6
    assert nxg.nodes == g.vertices
    assert len(nxg.edges) == 7

    for e in g.edges:
        u, v, _ = g.edge_tuple(e)
        assert nxg.has_edge(u, v)

    assert nxg.edges["2", "3"]["name"] == "e23"
    assert nxg.edges["3", "4"]["name"] == "e34"
    assert nxg.nodes["5"]["name"] == "v5"
    assert nxg.nodes["4"]["name"] == "v4"
    assert not nx.is_directed(nxg)


def test_int_graph_from_nx():

    nxg = nx.DiGraph()
    nxg.add_node(5)
    nxg.add_node(6)
    nxg.add_node(7)

    nxg.add_edge(5, 6)
    nxg.add_edge(6, 7, weight=5.0)

    nxg.graph["name"] = "G"

    g = from_nx(nxg, any_hashable=False)

    assert g.type.directed
    assert g.type.weighted

    assert g.number_of_vertices == 3
    assert g.number_of_edges == 2
    assert g.vertices == {0, 1, 2}
    assert g.edges == {0, 1}

    assert g.edge_source(0) == 0
    assert g.edge_target(0) == 1
    assert g.get_edge_weight(0) == 1.0

    assert g.edge_source(1) == 1
    assert g.edge_target(1) == 2
    assert g.get_edge_weight(1) == 5.0


def test_int_graph_no_weights_from_nx():

    nxg = nx.DiGraph()
    nxg.add_node(5)
    nxg.add_node(6)
    nxg.add_node(7)

    nxg.add_edge(5, 6)
    nxg.add_edge(6, 7)

    nxg.graph["name"] = "G"

    g = from_nx(nxg, any_hashable=False)

    assert g.type.directed
    assert not g.type.weighted

    assert g.number_of_vertices == 3
    assert g.number_of_edges == 2
    assert g.vertices == {0, 1, 2}
    assert g.edges == {0, 1}

    assert g.edge_source(0) == 0
    assert g.edge_target(0) == 1
    assert g.get_edge_weight(0) == 1.0

    assert g.edge_source(1) == 1
    assert g.edge_target(1) == 2
    assert g.get_edge_weight(1) == 1.0


def test_any_hashable_graph_no_weights_from_nx():

    nxg = nx.MultiGraph()
    nxg.add_node("5")
    nxg.add_node("6")
    nxg.add_node("7")
    nxg.add_node("8")

    k67 = nxg.add_edge("6", "7")
    nxg.add_edge("7", "8")
    k56_1 = nxg.add_edge("5", "6")
    k56_2 = nxg.add_edge("5", "6")

    nxg.graph["name"] = "G"

    nxg.nodes["5"]["name"] = "name5"
    nxg.nodes["5"]["type"] = "any"
    nxg.nodes["6"]["name"] = "name6"
    nxg.nodes["6"]["type"] = "any"

    nxg.edges["6", "7", k67]["name"] = "e67"
    nxg.edges["5", "6", k56_1]["name"] = "e56_1"
    nxg.edges["5", "6", k56_2]["name"] = "e56_2"

    index = 0
    for u, v, k in nxg.edges: 
        nxg.edges[u,v,k]['index'] = index
        index += 1

    g = from_nx(nxg)

    assert not g.type.directed
    assert not g.type.weighted
    assert g.type.allowing_multiple_edges
    assert g.type.allowing_self_loops

    assert g.number_of_vertices == 4
    assert len(nxg.edges) == 4
    assert g.number_of_edges == 4
    assert g.vertices == {"5", "6", "7", "8"}

    assert g.degree_of("6") == 3

    assert g.graph_attrs["name"] == "G"
    assert g.vertex_attrs["5"]["name"] == "name5"
    assert g.vertex_attrs["6"]["name"] == "name6"

    index = 0
    for e in g.edges: 
        assert g.edge_attrs[e]['index'] == index
        index += 1


def test_any_hashable_graph_with_weights_from_nx():

    nxg = nx.MultiGraph()
    nxg.add_node("5")
    nxg.add_node("6")
    nxg.add_node("7")
    nxg.add_node("8")

    k67 = nxg.add_edge("6", "7", weight=10.0)
    nxg.add_edge("7", "8", weight=10.0)
    k56_1 = nxg.add_edge("5", "6", weight=10.0)
    k56_2 = nxg.add_edge("5", "6", weight=10.0)

    nxg.graph["name"] = "G"

    nxg.nodes["5"]["name"] = "name5"
    nxg.nodes["5"]["type"] = "any"
    nxg.nodes["6"]["name"] = "name6"
    nxg.nodes["6"]["type"] = "any"

    nxg.edges["6", "7", k67]["name"] = "e67"
    nxg.edges["5", "6", k56_1]["name"] = "e56_1"
    nxg.edges["5", "6", k56_2]["name"] = "e56_2"

    index = 0
    for u, v, k in nxg.edges: 
        nxg.edges[u,v,k]['index'] = index
        index += 1

    g = from_nx(nxg)

    assert not g.type.directed
    assert g.type.weighted
    assert g.type.allowing_multiple_edges
    assert g.type.allowing_self_loops

    assert g.number_of_vertices == 4
    assert len(nxg.edges) == 4
    assert g.number_of_edges == 4
    assert g.vertices == {"5", "6", "7", "8"}

    assert g.degree_of("6") == 3

    assert g.graph_attrs["name"] == "G"
    assert g.vertex_attrs["5"]["name"] == "name5"
    assert g.vertex_attrs["6"]["name"] == "name6"

    print(g.edge_attrs)

    index = 0
    for e in g.edges: 
        assert g.edge_attrs[e]['index'] == index
        assert g.edge_attrs[e]['weight'] == 10.0
        index += 1