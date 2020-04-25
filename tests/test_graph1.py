import pytest

import jgrapht.graph as graph


def assert_same_set(set1, set2):
    assert set1 <= set2 and set2 <= set1


def test_graph1():

    g = graph.Graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    assert g.graph_type.directed
    assert g.graph_type.allowing_self_loops
    assert not g.graph_type.allowing_multiple_edges
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
    e51 = g.add_edge(v5, v1)
    assert e51 == 5

    assert len(g.edges()) == 6

    assert_same_set(set(g.edges_of(v1)), set([e12, e14, e11, e51]))
    assert_same_set(set(g.outedges_of(v1)), set([e12, e14, e11]))
    assert_same_set(set(g.inedges_of(v1)), set([e51, e11]))

    assert_same_set(set(g.edges()), set([0, 1, 2, 3, 4, 5]))

