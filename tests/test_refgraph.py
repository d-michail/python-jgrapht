import pytest

from jgrapht._internals._ref_graphs import _create_ref_graph


class CustomVertex:
    def __init__(self, id): 
        self._id = id

    def __repr__(self):
        return "CustomVertex(%r)" % self._id


def test_ref_graph_directed_inoutedges():

    g = _create_ref_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )

    assert g.type.directed
    assert g.type.allowing_self_loops
    assert g.type.allowing_multiple_edges
    assert g.type.weighted
    assert g.type.allowing_cycles

    v1 = CustomVertex(1)
    assert g.add_vertex(v1) is v1
    v2 = CustomVertex(2)
    assert g.add_vertex(v2) is v2
    v3 = CustomVertex(3)
    assert g.add_vertex(v3) is v3
    v4 = CustomVertex(4)
    assert g.add_vertex(v4) is v4
    v5 = CustomVertex(5)
    assert g.add_vertex(v5) is v5

    vcount = len(g.vertices)
    assert vcount == 5

    assert g.number_of_vertices == 5

    assert set(g.vertices) == set([v1, v2, v3, v4, v5])

    e12 = g.add_edge(v1, v2)
    assert g.edge_source(e12) == v1
    assert g.edge_target(e12) == v2
    assert g.edge_tuple(e12) == (v1, v2, 1.0)
    e23 = g.add_edge(v2, v3)
    assert g.edge_source(e23) == v2
    assert g.edge_target(e23) == v3
    assert g.edge_tuple(e23) == (v2, v3, 1.0)
    e14 = g.add_edge(v1, v4)
    e11 = g.add_edge(v1, v1)
    e45 = g.add_edge(v4, v5)
    e51_1 = g.add_edge(v5, v1)
    e51_2 = g.add_edge(v5, v1)

    assert len(g.edges) == 7

    assert g.contains_edge_between(v1, v4)
    assert not g.contains_edge_between(v1, v5)

    assert set(g.edges_of(v1)) == set([e12, e14, e11, e51_1, e51_2])
    assert set(g.outedges_of(v1)) == set([e12, e14, e11])
    assert set(g.inedges_of(v1)) == set([e51_1, e51_2, e11])
    assert g.degree_of(v1) == 6  # self-loops count twice!
    assert g.outdegree_of(v1) == 3
    assert g.indegree_of(v1) == 3

    assert set(g.edges_of(v2)) == set([e12, e23])
    assert set(g.outedges_of(v2)) == set([e23])
    assert set(g.inedges_of(v2)) == set([e12])
    assert g.degree_of(v2) == 2
    assert g.outdegree_of(v2) == 1
    assert g.indegree_of(v2) == 1

    assert set(g.edges_of(v3)) == set([e23])
    assert set(g.outedges_of(v3)) == set()
    assert set(g.inedges_of(v3)) == set([e23])
    assert g.degree_of(v3) == 1
    assert g.outdegree_of(v3) == 0
    assert g.indegree_of(v3) == 1

    assert set(g.edges_of(v4)) == set([e45, e14])
    assert set(g.outedges_of(v4)) == set([e45])
    assert set(g.inedges_of(v4)) == set([e14])
    assert g.degree_of(v4) == 2
    assert g.outdegree_of(v4) == 1
    assert g.indegree_of(v4) == 1

    assert set(g.edges_of(v5)) == set([e45, e51_1, e51_2])
    assert set(g.outedges_of(v5)) == set([e51_1, e51_2])
    assert set(g.inedges_of(v5)) == set([e45])
    assert g.degree_of(v5) == 3
    assert g.outdegree_of(v5) == 2
    assert g.indegree_of(v5) == 1

    assert set(g.edges) == set([e12, e23, e14, e11, e45, e51_1, e51_2])
