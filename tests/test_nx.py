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
