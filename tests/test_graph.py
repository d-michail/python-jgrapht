import pytest

import jgrapht.graph as graph
from jgrapht._errors import IllegalArgumentError, UnsupportedOperationError

def assert_same_set(set1, set2):
    assert set1 <= set2 and set2 <= set1


def test_graph_directed_inoutedges():

    g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True)

    assert g.graph_type.directed
    assert g.graph_type.allowing_self_loops
    assert g.graph_type.allowing_multiple_edges
    assert g.graph_type.weighted

    v1 = g.add_vertex()
    assert v1 == 0
    v2 = g.add_vertex()
    assert v2 == 1
    v3 = g.add_vertex()
    assert v3 == 2
    v4 = g.add_vertex()
    assert v4 == 3
    v5 = g.add_vertex()
    assert v5 == 4

    vcount = len(g.vertices())
    assert vcount == 5

    assert g.number_of_vertices() == 5

    assert_same_set(set(g.vertices()), set([0, 1, 2, 3, 4]))

    e12 = g.add_edge(v1, v2)
    assert e12 == 0
    assert g.edge_source(e12) == v1
    assert g.edge_target(e12) == v2
    assert g.edge_endpoints(e12) == (v1, v2)
    e23 = g.add_edge(v2, v3)
    assert g.edge_source(e23) == v2
    assert g.edge_target(e23) == v3
    assert g.edge_endpoints(e23) == (v2, v3)
    assert e23 == 1
    e14 = g.add_edge(v1, v4)
    assert e14 == 2
    e11 = g.add_edge(v1, v1)
    assert e11 == 3
    e45 = g.add_edge(v4, v5)
    assert e45 == 4
    e51_1 = g.add_edge(v5, v1)
    assert e51_1 == 5
    e51_2 = g.add_edge(v5, v1)
    assert e51_2 == 6

    assert len(g.edges()) == 7

    assert g.contains_edge_between(v1, v4)
    assert not g.contains_edge_between(v1, v5)

    assert_same_set(set(g.edges_of(v1)), set([e12, e14, e11, e51_1, e51_2]))
    assert_same_set(set(g.outedges_of(v1)), set([e12, e14, e11]))
    assert_same_set(set(g.inedges_of(v1)), set([e51_1, e51_2, e11]))
    assert g.degree_of(v1) == 6 # self-loops count twice!
    assert g.outdegree_of(v1) == 3
    assert g.indegree_of(v1) == 3

    assert_same_set(set(g.edges_of(v2)), set([e12, e23]))
    assert_same_set(set(g.outedges_of(v2)), set([e23]))
    assert_same_set(set(g.inedges_of(v2)), set([e12]))
    assert g.degree_of(v2) == 2
    assert g.outdegree_of(v2) == 1
    assert g.indegree_of(v2) == 1

    assert_same_set(set(g.edges_of(v3)), set([e23]))
    assert_same_set(set(g.outedges_of(v3)), set())
    assert_same_set(set(g.inedges_of(v3)), set([e23]))
    assert g.degree_of(v3) == 1
    assert g.outdegree_of(v3) == 0
    assert g.indegree_of(v3) == 1

    assert_same_set(set(g.edges_of(v4)), set([e45, e14]))
    assert_same_set(set(g.outedges_of(v4)), set([e45]))
    assert_same_set(set(g.inedges_of(v4)), set([e14]))
    assert g.degree_of(v4) == 2
    assert g.outdegree_of(v4) == 1
    assert g.indegree_of(v4) == 1

    assert_same_set(set(g.edges_of(v5)), set([e45, e51_1, e51_2]))
    assert_same_set(set(g.outedges_of(v5)), set([e51_1, e51_2]))
    assert_same_set(set(g.inedges_of(v5)), set([e45]))
    assert g.degree_of(v5) == 3
    assert g.outdegree_of(v5) == 2
    assert g.indegree_of(v5) == 1    

    assert_same_set(set(g.edges()), set([0, 1, 2, 3, 4, 5, 6]))


def test_graph_undirected_inoutedges():

    g = graph.Graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True)

    assert not g.graph_type.directed
    assert g.graph_type.allowing_self_loops
    assert g.graph_type.allowing_multiple_edges
    assert g.graph_type.weighted

    v1 = g.add_vertex()
    assert v1 == 0
    v2 = g.add_vertex()
    assert v2 == 1
    v3 = g.add_vertex()
    assert v3 == 2
    v4 = g.add_vertex()
    assert v4 == 3
    v5 = g.add_vertex()
    assert v5 == 4

    vcount = len(g.vertices())
    assert vcount == 5

    assert_same_set(set(g.vertices()), set([0, 1, 2, 3, 4]))

    e12 = g.add_edge(v1, v2)
    assert e12 == 0
    assert g.edge_source(e12) == v1
    assert g.edge_target(e12) == v2
    assert g.edge_endpoints(e12) == (v1, v2)
    e23 = g.add_edge(v2, v3)
    assert g.edge_source(e23) == v2
    assert g.edge_target(e23) == v3
    assert g.edge_endpoints(e23) == (v2, v3)
    assert e23 == 1
    e14 = g.add_edge(v1, v4)
    assert e14 == 2
    e11 = g.add_edge(v1, v1)
    assert e11 == 3
    e45 = g.add_edge(v4, v5)
    assert e45 == 4
    e51_1 = g.add_edge(v5, v1)
    assert e51_1 == 5
    e51_2 = g.add_edge(v5, v1)
    assert e51_2 == 6

    assert len(g.edges()) == 7

    assert g.contains_edge_between(v1, v4)
    assert g.contains_edge_between(v1, v5)

    assert_same_set(set(g.edges_between(v1, v5)), set([e51_1, e51_2]))

    assert_same_set(set(g.edges_of(v1)), set([e12, e14, e11, e51_1, e51_2]))
    assert_same_set(set(g.outedges_of(v1)), set([e12, e14, e11, e51_1, e51_2]))
    assert_same_set(set(g.inedges_of(v1)), set([e12, e14, e11, e51_1, e51_2]))
    assert g.degree_of(v1) == 6 # self-loops count twice!
    assert g.outdegree_of(v1) == 6
    assert g.indegree_of(v1) == 6

    assert_same_set(set(g.edges_of(v2)), set([e12, e23]))
    assert_same_set(set(g.outedges_of(v2)), set([e12, e23]))
    assert_same_set(set(g.inedges_of(v2)), set([e12, e23]))
    assert g.degree_of(v2) == 2
    assert g.outdegree_of(v2) == 2
    assert g.indegree_of(v2) == 2

    assert_same_set(set(g.edges_of(v3)), set([e23]))
    assert_same_set(set(g.outedges_of(v3)), set([e23]))
    assert_same_set(set(g.inedges_of(v3)), set([e23]))
    assert g.degree_of(v3) == 1
    assert g.outdegree_of(v3) == 1
    assert g.indegree_of(v3) == 1

    assert_same_set(set(g.edges_of(v4)), set([e45, e14]))
    assert_same_set(set(g.outedges_of(v4)), set([e45, e14]))
    assert_same_set(set(g.inedges_of(v4)), set([e45, e14]))
    assert g.degree_of(v4) == 2
    assert g.outdegree_of(v4) == 2
    assert g.indegree_of(v4) == 2

    assert_same_set(set(g.edges_of(v5)), set([e45, e51_1, e51_2]))
    assert_same_set(set(g.outedges_of(v5)), set([e45, e51_1, e51_2]))
    assert_same_set(set(g.inedges_of(v5)), set([e45, e51_1, e51_2]))
    assert g.degree_of(v5) == 3
    assert g.outdegree_of(v5) == 3
    assert g.indegree_of(v5) == 3  

    assert_same_set(set(g.edges()), set([0, 1, 2, 3, 4, 5, 6]))


def test_graph_no_allow_self_loops():

    g = graph.Graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    assert g.graph_type.directed
    assert not g.graph_type.allowing_self_loops
    assert g.graph_type.allowing_multiple_edges
    assert g.graph_type.weighted

    v1 = g.add_vertex()
    assert v1 == 0

    with pytest.raises(IllegalArgumentError):
        g.add_edge(v1, v1)


def test_graph_no_allow_multiple_edges():

    g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    assert g.graph_type.directed
    assert g.graph_type.allowing_self_loops
    assert not g.graph_type.allowing_multiple_edges
    assert g.graph_type.weighted

    v1 = g.add_vertex()
    assert v1 == 0
    v2 = g.add_vertex()
    assert v2 == 1

    g.add_edge(v1, v2)
    with pytest.raises(IllegalArgumentError):
        g.add_edge(v1, v2)


def test_graph_no_weights():

    g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=False)

    assert g.graph_type.directed
    assert g.graph_type.allowing_self_loops
    assert not g.graph_type.allowing_multiple_edges
    assert not g.graph_type.weighted

    v1 = g.add_vertex()
    assert v1 == 0
    v2 = g.add_vertex()
    assert v2 == 1

    e12 = g.add_edge(v1, v2)

    assert g.get_edge_weight(e12) == 1.0

    with pytest.raises(UnsupportedOperationError):
        g.set_edge_weight(e12, 10.0)


def test_graph_add_edge_with_weight():

    g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    v1 = g.add_vertex()
    v2 = g.add_vertex()
    e12 = g.add_edge(v1, v2, weight=55.0)
    assert g.get_edge_weight(e12) == 55.0

