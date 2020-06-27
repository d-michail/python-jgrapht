import pytest

from jgrapht import create_graph, copy_to_sparse_graph
from jgrapht.types import GraphEvent
from jgrapht.utils import create_edge_supplier, create_vertex_supplier
from jgrapht.generators import complete_graph

from jgrapht._internals._anyhashableg import _create_sparse_anyhashable_graph

def test_any_graph():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
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
    assert dict(g.vertex_attrs) == {
        "v2": {"color": "red", "name": "vertex 2"},
        "v3": {"name": "vertex 3"},
    }

    with pytest.raises(ValueError):
        g.vertex_attrs["v20"]

    with pytest.raises(ValueError):
        g.vertex_attrs["v30"]["color"] = "blue"

    with pytest.raises(ValueError):
        g.vertex_attrs["v30"] = {}

    with pytest.raises(ValueError):
        del g.vertex_attrs["v30"]

    del g.vertex_attrs["v3"]
    assert len(g.vertex_attrs) == 1
    g.vertex_attrs["v3"]["name"] = "vertex 3"
    assert len(g.vertex_attrs) == 2

    repr(g.vertex_attrs)

    g.edge_attrs["e13"]["length"] = 100.0
    g.edge_attrs["e13"]["color"] = "white"
    g.edge_attrs["e14"]["length"] = 150.0
    g.edge_attrs["e14"]["color"] = "blue"

    assert dict(g.edge_attrs) == {
        "e13": {"color": "white", "length": 100.0},
        "e14": {"color": "blue", "length": 150.0},
    }

    with pytest.raises(ValueError):
        g.edge_attrs["e1345"]

    g.remove_edge("e13")

    assert dict(g.edge_attrs) == {
        "e14": {"color": "blue", "length": 150.0},
    }

    with pytest.raises(ValueError):
        g.edge_attrs["e13"]

    repr(g.edge_attrs)

    with pytest.raises(ValueError):
        g.edge_attrs["e53"] = {}
    del g.edge_attrs["e14"]
    with pytest.raises(ValueError):
        del g.edge_attrs["e35"]
    assert len(g.edge_attrs) == 0
    g.edge_attrs["e14"]["color"] = "blue"
    assert len(g.edge_attrs) == 1

    with pytest.raises(TypeError):
        g.edge_attrs["e14"]["weight"] = "5.0"

    g.edge_attrs["e14"]["weight"] = 33.3
    del g.edge_attrs["e14"]["weight"]
    assert g.edge_attrs["e14"]["weight"] == 1.0

    g.edge_attrs["e14"]["color"] = "blue"
    del g.edge_attrs["e14"]["color"]

    g.edge_attrs["e14"]["color"] = "blue"
    repr(g.edge_attrs["e14"])

    assert len(g.edge_attrs["e14"]) == 1

    assert str(g.edge_attrs["e14"]) == "{'color': 'blue'}"


def test_any_graph_of_graphs():

    g1 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )
    g1.add_vertex(0)
    g1.add_vertex(1)
    g1.add_edge(0, 1)

    g2 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )
    g2.add_vertex(2)
    g2.add_vertex(3)
    g2.add_edge(2, 3)

    g3 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )
    g3.add_vertex(4)
    g3.add_vertex(5)
    g3.add_edge(4, 5)

    # create the graph of graphs
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(g1)
    g.add_vertex(g2)

    g.add_edge(g1, g2, edge=g3)

    assert (
        str(g)
        == "({({0, 1}, {0=(0,1)}), ({2, 3}, {0=(2,3)})}, {({4, 5}, {0=(4,5)})=(({0, 1}, {0=(0,1)}),({2, 3}, {0=(2,3)}))})"
    )

    assert g.contains_vertex(g1)
    assert g.contains_vertex(g2)
    assert g.contains_edge(g3)

    assert len(g.vertices) == 2
    assert len(g.edges) == 1

    assert g.edge_source(g3) == g1
    assert g.edge_target(g3) == g2


def test_suppliers_graph():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    v0 = g.add_vertex()
    g.add_vertex("v1")
    v2 = g.add_vertex()

    assert g.contains_vertex(v0)
    assert g.contains_vertex("v1")
    assert g.contains_vertex(v2)
    assert not g.contains_vertex("v7")

    assert g.vertices == {v0, "v1", v2}
    assert len(g.vertices) == 3

    e02 = g.add_edge(v0, v2)

    assert g.edge_source(e02) == v0
    assert g.edge_target(e02) == v2

    assert len(g.edges) == 1

    assert g.edges == {e02}


def test_with_string_suppliers_graph():
    class StringSupplier:
        def __init__(self):
            self._count = 0

        def __call__(self):
            ret = str(self._count)
            self._count += 1
            return ret

    supplier = StringSupplier()

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=supplier,
        edge_supplier=supplier,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    g.add_vertex()
    g.add_vertex("v1")
    g.add_vertex()

    assert g.contains_vertex("0")
    assert g.contains_vertex("v1")
    assert g.contains_vertex("1")

    assert g.vertices == {"0", "v1", "1"}
    assert len(g.vertices) == 3

    g.add_edge("0", "1")

    assert g.edge_source("2") == "0"
    assert g.edge_target("2") == "1"

    assert len(g.edges) == 1

    assert g.edges == {"2"}


def test_on_already_initialized_graph():
    class StringSupplier:
        def __init__(self, prefix):
            self._count = 0
            self._prefix = prefix

        def __call__(self):
            ret = "{}{}".format(self._prefix, self._count)
            self._count += 1
            return ret

    pg = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=StringSupplier("v"),
        edge_supplier=StringSupplier("e"),
    )

    pg.add_vertex(0)
    pg.add_vertex(1)
    pg.add_edge(0, 1)
    pg.add_edge(1, 0)

    pg.add_vertex(vertex="new2")

    assert len(pg.vertices) == 3

    assert pg.vertices == {0, 1, "new2"}
    assert pg.edges == {"e0", "e1"}


def test_bad_vertex_supplier_property_graph():
    def vertex_supplier():
        return "v0"

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=vertex_supplier,
    )

    g.add_vertex()
    with pytest.raises(ValueError):
        g.add_vertex()


def test_bad_edge_supplier_property_graph():
    def edge_supplier():
        return "e0"

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        edge_supplier=edge_supplier,
    )

    v0 = g.add_vertex()
    v1 = g.add_vertex()
    v2 = g.add_vertex()

    g.add_edge(v0, v1)

    with pytest.raises(ValueError):
        g.add_edge(v1, v2)


def test_listenable_property_graph():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    vertices = []

    def listener(element, event):
        if event == GraphEvent.VERTEX_ADDED:
            vertices.append(element)

    g.add_listener(listener)

    complete_graph(g, 5)

    assert vertices == ["v0", "v1", "v2", "v3", "v4"]


def test_anyhashable_graph_sparse_weighted():

    edgelist = [
        ('v0', 'v1', 5),
        ('v0', 'v2', 2),
        ('v0', 'v3', 3),
        ('v1', 'v3', 1),
        ('v2', 'v3', 7.7),
        ('v2', 'v4', 3.3),
        ('v2', 'v5', 13.0),
        ('v0', 'v4', 9.999),
        ('v2', 'v6', 3.0),
    ]
    g = _create_sparse_anyhashable_graph(edgelist, directed=False)

    assert not g.type.directed
    assert g.type.weighted

    assert g.vertices == set(['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6'])

    edgelist2 = []
    for e in g.edges:
        edgelist2.append(g.edge_tuple(e))
    assert edgelist2 == edgelist

    # sparse graphs cannot be modified
    with pytest.raises(ValueError):
        g.add_edge('0', '5')

    # But can modify the weights
    for e in g.edges: 
        g.edge_attrs[e]['weight'] += 1.0

    weighted = [g.edge_attrs[e]['weight'] for e in g.edges]
    assert weighted == [6.0, 3.0, 4.0, 2.0, 8.7, 4.3, 14.0, 10.999, 4.0]



def test_graph_copy_to_sparse():

    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    assert not g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    assert g.add_vertex(0) == 0
    v1 = 0
    assert g.add_vertex(1) == 1
    v2 = 1
    assert g.add_vertex(2) == 2
    v3 = 2
    assert g.add_vertex(3) == 3
    v4 = 3
    assert g.add_vertex(4) == 4
    v5 = 4

    assert g.vertices, set([0, 1, 2, 3, 4])

    e12 = g.add_edge(v1, v2)
    e23 = g.add_edge(v2, v3)
    e14 = g.add_edge(v1, v4)
    e11 = g.add_edge(v1, v1)
    e45 = g.add_edge(v4, v5)
    e51_1 = g.add_edge(v5, v1)
    e51_2 = g.add_edge(v5, v1)

    assert len(g.edges) == 7

    gs = copy_to_sparse_graph(g)

    assert gs.vertices == set([0, 1, 2, 3, 4])
    assert len(gs.edges) == 7


def test_graph_copy_to_sparse1():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    assert g.add_vertex(0) == 0
    assert g.add_vertex(5) == 5
    assert g.add_vertex(10) == 10

    g.add_edge(0, 10)
    g.add_edge(0, 5)
    g.add_edge(10, 5)

    assert len(g.edges) == 3

    gs = copy_to_sparse_graph(g)

    assert gs.vertices == {0, 10, 5}
    assert len(gs.edges) == 3
    assert gs.type.weighted
    assert gs.type.directed


def test_graph_copy_to_sparse_with_attrs():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted

    assert g.add_vertex('0') == '0'
    assert g.add_vertex('5') == '5'
    assert g.add_vertex('10') == '10'

    g.add_edge('0', '10', edge='e0')
    g.add_edge('0', '5', edge='e1')
    g.add_edge('10', '5', edge='e2')

    g.edge_attrs['e0']['color'] = 'red'
    g.edge_attrs['e1']['color'] = 'blue'
    g.edge_attrs['e2']['color'] = 'black'

    g.vertex_attrs['0']['color'] = 'black'
    g.vertex_attrs['5']['color'] = 'red'
    g.vertex_attrs['10']['color'] = 'unknown'

    g.graph_attrs['type'] = 'directed'

    assert len(g.edges) == 3

    gs = copy_to_sparse_graph(g)

    assert gs.vertices == { '0', '5', '10' }
    assert len(gs.edges) == 3
    assert gs.type.weighted
    assert gs.type.directed

    assert gs.edge_attrs['e0']['color'] == 'red'
    assert gs.edge_attrs['e1']['color'] == 'blue'
    assert gs.edge_attrs['e2']['color'] == 'black'

    assert gs.vertex_attrs['0']['color'] == 'black'
    assert gs.vertex_attrs['5']['color'] == 'red'
    assert gs.vertex_attrs['10']['color'] == 'unknown'

    gs.graph_attrs['type'] == 'directed'
    