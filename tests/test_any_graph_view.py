import pytest

from jgrapht._internals._any_graph_view import _JGraphTAnyGraphView

from jgrapht import create_graph


def test_any_graph():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    g = _JGraphTAnyGraphView(g)

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    g.add_vertex("v1")
    g.add_vertex("v2")
    g.add_vertex("v3")
    g.add_vertex("v4")
    g.add_vertex("v5")
    g.add_vertex("v6")

    assert g.contains_vertex("v4")
    assert not g.contains_vertex("v7")

    assert g.vertices == {"v1", "v2", "v3", "v4", "v5", "v6"}
    assert len(g.vertices) == 6

    g.add_edge("v1", "v2", "e12")
    g.add_edge("v1", "v3", "e13")
    g.add_edge("v1", "v4", "e14")
    g.add_edge("v1", "v5", "e15")
    g.add_edge("v5", "v1", "e51_1")
    g.add_edge("v5", "v1", "e51_2")
    g.add_edge("v3", "v6", "e36")
    g.add_edge("v6", "v6", "e66")

    assert len(g.edges) == 8

    assert g.edge_source("e51_1") == "v5"
    assert g.edge_target("e51_1") == "v1"
    assert g.edge_source("e51_2") == "v5"
    assert g.edge_target("e51_2") == "v1"

    assert g.edge_target("e66") == "v6"
    assert g.edge_target("e66") == "v6"

    assert g.contains_edge("e13")
    assert not g.contains_edge("e31")

    assert g.get_edge_weight("e13") == 1.0
    g.set_edge_weight("e13", 50.0)
    assert g.get_edge_weight("e13") == 50.0

    g.set_edge_weight("e14", 14.0)
    assert g.edge_tuple("e14") == ("v1", "v4", 14.0)

    assert g.contains_edge_between("v1", "v4")
    assert not g.contains_edge_between("v5", "v3")

    assert set(g.edges_of("v5")) == {"e51_2", "e51_1", "e15"}
    assert set(g.inedges_of("v5")) == {"e15"}
    assert set(g.outedges_of("v5")) == {"e51_2", "e51_1"}

    assert g.degree_of("v5") == 3
    assert g.indegree_of("v5") == 1
    assert g.outdegree_of("v5") == 2

    assert set(g.edges_between("v5", "v1")) == {"e51_2", "e51_1"}

    assert len(g.edges) == 8
    assert g.remove_edge("e36")
    assert not g.contains_edge("e36")
    assert len(g.edges) == 7
    assert not g.remove_edge("e35")
    assert len(g.edges) == 7

    g.remove_vertex("v5")
    assert not g.contains_vertex("v5")
    assert len(g.vertices) == 5
    assert g.vertices == {"v1", "v2", "v3", "v4", "v6"}
    assert not g.contains_edge("e51_1")
    assert not g.contains_edge("e51_2")
    assert not g.contains_edge("e15")
    assert len(g.edges) == 4

    assert set(g.edges) == {"e12", "e13", "e14", "e66"}

    assert g.degree_of("v6") == 2
    assert g.outdegree_of("v6") == 1
    assert g.indegree_of("v6") == 1

    # now test the properties
    g.graph_props["name"] = "property graph"
    assert g.graph_props == {"name": "property graph"}

    g.vertex_props["v2"]["name"] = "vertex 2"
    g.vertex_props["v2"]["color"] = "red"
    assert g.vertex_props["v2"]["name"] == "vertex 2"
    assert g.vertex_props["v2"]["color"] == "red"
    assert g.vertex_props["v2"] == {"name": "vertex 2", "color": "red"}

    g.vertex_props["v3"]["name"] = "vertex 3"

    g.add_vertex("new vertex")
    g.vertex_props["new vertex"]["color"] = "white"
    g.remove_vertex("new vertex")
    assert dict(g.vertex_props) == {
        "v2": {"color": "red", "name": "vertex 2"},
        "v3": {"name": "vertex 3"},
    }

    with pytest.raises(ValueError):
        g.vertex_props["v20"]

    g.edge_props["e13"]["length"] = 100.0
    g.edge_props["e13"]["color"] = "white"
    g.edge_props["e14"]["length"] = 150.0
    g.edge_props["e14"]["color"] = "blue"

    assert dict(g.edge_props) == {
        "e13": {"color": "white", "length": 100.0},
        "e14": {"color": "blue", "length": 150.0},
    }

    with pytest.raises(ValueError):
        g.edge_props["e1345"]

    g.remove_edge("e13")

    assert dict(g.edge_props) == {
        "e14": {"color": "blue", "length": 150.0},
    }

    with pytest.raises(ValueError):
        g.edge_props["e13"]

