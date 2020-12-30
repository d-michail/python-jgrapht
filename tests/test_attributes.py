import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.types import GraphEvent
from jgrapht.utils import create_edge_supplier, create_vertex_supplier
from jgrapht.generators import complete_graph


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_any_graph_long_ref(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        with_attributes=True,
        backend=backend,
    )

    assert repr(g) is not None

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

    assert g.add_vertex("v1") == "v1"
    assert len(g.vertices) == 6

    repr(g.vertices)
    repr(g.edges)

    g.add_edge("v1", "v2", edge="e12")
    g.add_edge("v1", "v3", edge="e13")
    g.add_edge("v1", "v4", edge="e14")
    g.add_edge("v1", "v5", edge="e15")
    g.add_edge("v5", "v1", edge="e51_1")
    g.add_edge("v5", "v1", edge="e51_2")
    g.add_edge("v3", "v6", edge="e36")
    g.add_edge("v6", "v6", edge="e66")

    assert len(g.edges) == 8

    with pytest.raises(ValueError):
        g.add_edge("v1", "v18", edge="e118")

    assert g.edge_source("e51_1") == "v5"
    assert g.edge_target("e51_1") == "v1"
    assert g.edge_source("e51_2") == "v5"
    assert g.edge_target("e51_2") == "v1"

    assert g.edge_target("e66") == "v6"
    assert g.edge_target("e66") == "v6"

    with pytest.raises(ValueError):
        g.edge_source("e123")

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
    assert g.number_of_vertices == 5
    assert g.vertices == {"v1", "v2", "v3", "v4", "v6"}
    assert not g.contains_edge("e51_1")
    assert not g.contains_edge("e51_2")
    assert not g.contains_edge("e15")
    assert len(g.edges) == 4
    assert g.number_of_edges == 4

    with pytest.raises(ValueError):
        g.remove_vertex(None)

    assert not g.remove_vertex("v5")

    with pytest.raises(ValueError):
        g.remove_edge(None)

    assert set(g.edges) == {"e12", "e13", "e14", "e66"}

    assert g.degree_of("v6") == 2
    assert g.outdegree_of("v6") == 1
    assert g.indegree_of("v6") == 1

    # now test the properties
    g.graph_attrs["name"] = "property graph"
    assert g.graph_attrs == {"name": "property graph"}

    g.vertex_attrs["v2"]["name"] = "vertex 2"
    g.vertex_attrs["v2"]["color"] = "red"
    assert g.vertex_attrs["v2"]["name"] == "vertex 2"
    assert g.vertex_attrs["v2"]["color"] == "red"
    assert g.vertex_attrs["v2"] == {"name": "vertex 2", "color": "red"}

    g.vertex_attrs["v3"]["name"] = "vertex 3"

    g.add_vertex("new vertex")
    g.vertex_attrs["new vertex"]["color"] = "white"
    g.remove_vertex("new vertex")

    assert dict(g.vertex_attrs["v2"]) == {"color": "red", "name": "vertex 2"}
    assert dict(g.vertex_attrs["v3"]) == {"name": "vertex 3"}

    with pytest.raises(KeyError):
        g.vertex_attrs["v20"]

    with pytest.raises(KeyError):
        g.vertex_attrs["v30"]["color"] = "blue"

    with pytest.raises(TypeError):
        g.vertex_attrs["v30"] = {}

    with pytest.raises(TypeError):
        del g.vertex_attrs["v30"]

    with pytest.raises(TypeError):
        del g.vertex_attrs["v3"]

    assert len(g.vertex_attrs) == len(g.vertices)
    g.vertex_attrs["v3"]["name"] = "vertex 3"
    assert len(g.vertex_attrs) == len(g.vertices)

    repr(g.vertex_attrs)

    g.edge_attrs["e13"]["length"] = 100.0
    g.edge_attrs["e13"]["color"] = "white"
    g.edge_attrs["e14"]["length"] = 150.0
    g.edge_attrs["e14"]["color"] = "blue"

    assert dict(g.edge_attrs["e13"]) ==  {"color": "white", "length": 100.0}
    assert dict(g.edge_attrs["e14"]) ==  {"color": "blue", "length": 150.0}

    with pytest.raises(KeyError):
        g.edge_attrs["e1345"]

    g.remove_edge("e13")

    assert dict(g.edge_attrs["e14"]) == {"color": "blue", "length": 150.0}

    with pytest.raises(KeyError):
        g.edge_attrs["e13"]

    repr(g.edge_attrs)

    with pytest.raises(TypeError):
        g.edge_attrs["e53"] = {}
    with pytest.raises(TypeError):    
        del g.edge_attrs["e14"]
    with pytest.raises(TypeError):
        del g.edge_attrs["e35"]
    assert len(g.edge_attrs) == len(g.edges)
    g.edge_attrs["e14"]["color"] = "blue"
    assert len(g.edge_attrs) == len(g.edges)


@pytest.mark.parametrize(
    "backend",
    [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH],
)
def test_any_graph(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        with_attributes=True,
        backend=backend,
    )

    print(repr(g))

    assert repr(g) is not None

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_vertex(5)
    g.add_vertex(6)

    assert g.contains_vertex(4)
    assert not g.contains_vertex(7)

    assert g.vertices == {1, 2, 3, 4, 5, 6}
    assert len(g.vertices) == 6

    assert g.add_vertex(1) == 1
    assert len(g.vertices) == 6

    repr(g.vertices)
    repr(g.edges)

    emap = {
        "e12": 1,
        "e13": 2,
        "e14": 3,
        "e15": 4,
        "e51_1": 5,
        "e51_2": 6,
        "e36": 7,
        "e66": 8,
        "e35": 800,
    }

    g.add_edge(1, 2, edge=emap["e12"])
    g.add_edge(1, 3, edge=emap["e13"])
    g.add_edge(1, 4, edge=emap["e14"])
    g.add_edge(1, 5, edge=emap["e15"])
    g.add_edge(5, 1, edge=emap["e51_1"])
    g.add_edge(5, 1, edge=emap["e51_2"])
    g.add_edge(3, 6, edge=emap["e36"])
    g.add_edge(6, 6, edge=emap["e66"])

    assert len(g.edges) == 8

    with pytest.raises(ValueError):
        g.add_edge(1, 18, edge=118)

    assert g.edge_source(emap["e51_1"]) == 5
    assert g.edge_target(emap["e51_1"]) == 1
    assert g.edge_source(emap["e51_2"]) == 5
    assert g.edge_target(emap["e51_2"]) == 1
    assert g.edge_target(emap["e66"]) == 6
    assert g.edge_target(emap["e66"]) == 6

    assert g.contains_edge(emap["e13"])
    assert not g.contains_edge(500)

    assert g.get_edge_weight(emap["e13"]) == 1.0
    g.set_edge_weight(emap["e13"], 50.0)
    assert g.get_edge_weight(emap["e13"]) == 50.0

    g.set_edge_weight(emap["e14"], 14.0)
    assert g.edge_tuple(emap["e14"]) == (1, 4, 14.0)

    assert g.contains_edge_between(1, 4)
    assert not g.contains_edge_between(5, 3)

    assert set(g.edges_of(5)) == {emap["e51_2"], emap["e51_1"], emap["e15"]}
    assert set(g.inedges_of(5)) == {emap["e15"]}
    assert set(g.outedges_of(5)) == {emap["e51_2"], emap["e51_1"]}

    assert g.degree_of(5) == 3
    assert g.indegree_of(5) == 1
    assert g.outdegree_of(5) == 2

    assert set(g.edges_between(5, 1)) == {emap["e51_2"], emap["e51_1"]}

    assert len(g.edges) == 8
    assert g.remove_edge(emap["e36"])
    assert not g.contains_edge(emap["e36"])
    assert len(g.edges) == 7
    assert not g.remove_edge(emap["e35"])
    assert len(g.edges) == 7

    g.remove_vertex(5)
    assert not g.contains_vertex(5)
    assert len(g.vertices) == 5
    assert g.number_of_vertices == 5
    assert g.vertices == {1, 2, 3, 4, 6}
    assert not g.contains_edge(emap["e51_1"])
    assert not g.contains_edge(emap["e51_2"])
    assert not g.contains_edge(emap["e15"])
    assert len(g.edges) == 4
    assert g.number_of_edges == 4

    with pytest.raises(ValueError):
        g.remove_vertex(None)

    assert not g.remove_vertex(5)

    with pytest.raises(ValueError):
        g.remove_edge(None)

    assert set(g.edges) == {emap["e12"], emap["e13"], emap["e14"], emap["e66"]}

    assert g.degree_of(6) == 2
    assert g.outdegree_of(6) == 1
    assert g.indegree_of(6) == 1

    # now test the properties
    g.graph_attrs["name"] = "property graph"

    assert g.graph_attrs == {"name": "property graph"}

    g.vertex_attrs[2]["name"] = "vertex 2"
    g.vertex_attrs[2]["color"] = "red"
    assert g.vertex_attrs[2]["name"] == "vertex 2"
    assert g.vertex_attrs[2]["color"] == "red"
    assert g.vertex_attrs[2] == {"name": "vertex 2", "color": "red"}

    g.vertex_attrs[3]["name"] = "vertex 3"

    g.add_vertex(100)
    g.vertex_attrs[100]["color"] = "white"
    g.remove_vertex(100)

    assert dict(g.vertex_attrs[2]) == {"color": "red", "name": "vertex 2"}
    assert dict(g.vertex_attrs[3]) == {"name": "vertex 3"}

    with pytest.raises(KeyError):
        g.vertex_attrs[20]

    with pytest.raises(KeyError):
        g.vertex_attrs[30]["color"] = "blue"

    with pytest.raises(TypeError):
        g.vertex_attrs[30] = {}

    with pytest.raises(TypeError):
        del g.vertex_attrs[30]

    with pytest.raises(TypeError):
        del g.vertex_attrs[3]

    assert len(g.vertex_attrs) == len(g.vertices)
    g.vertex_attrs[3]["name"] = "vertex 3"
    g.vertex_attrs[3]["name1"] = "another name 3"
    assert len(g.vertex_attrs[3]) == 2

    repr(g.vertex_attrs)

    g.edge_attrs[emap["e13"]]["length"] = 100.0
    g.edge_attrs[emap["e13"]]["color"] = "white"
    g.edge_attrs[emap["e14"]]["length"] = 150.0
    g.edge_attrs[emap["e14"]]["color"] = "blue"

    assert dict(g.edge_attrs[2]) == {'length': 100.0, 'color': 'white'}
    assert dict(g.edge_attrs[3]) == {'length': 150.0, 'color': 'blue'}

    g.remove_edge(emap["e13"])

    assert dict(g.edge_attrs[3]) == {'length': 150.0, 'color': 'blue'}
