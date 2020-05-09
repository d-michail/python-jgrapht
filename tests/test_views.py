import pytest

from jgrapht import create_graph
from jgrapht.exceptions import UnsupportedOperationError
from jgrapht.views import as_undirected, as_edgereversed, as_unmodifiable, as_unweighted


def test_as_unweighted():
    g = create_graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    v1 = 0
    g.add_vertex(1)
    v2 = 1
    g.add_vertex(2)
    v3 = 2
    g.add_vertex(3)
    v4 = 3
    g.add_vertex(4)
    v5 = 4
    g.create_edge(v1, v2)
    g.create_edge(v2, v3)
    g.create_edge(v1, v4)
    g.create_edge(v1, v1)
    e45 = g.create_edge(v4, v5)
    g.create_edge(v5, v1)

    g.set_edge_weight(e45, 100.0)

    g1 = as_unweighted(g)

    assert g.graph_type.directed == g1.graph_type.directed
    assert g.graph_type.allowing_self_loops == g1.graph_type.allowing_self_loops
    assert g.graph_type.allowing_multiple_edges == g1.graph_type.allowing_multiple_edges
    assert g.graph_type.weighted != g1.graph_type.weighted
    assert g.get_edge_weight(e45) == 100.0
    assert g1.get_edge_weight(e45) == 1.0


def test_as_undirected():
    g = create_graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    v1 = 0
    g.add_vertex(1)
    v2 = 1
    g.add_vertex(2)
    v3 = 2
    g.add_vertex(3)
    v4 = 3
    g.add_vertex(4)
    v5 = 4

    g.create_edge(v1, v2)
    g.create_edge(v2, v3)
    g.create_edge(v1, v4)
    g.create_edge(v1, v1)
    g.create_edge(v4, v5)
    g.create_edge(v5, v1)

    # undirected
    g2 = as_undirected(g)
    assert g2.graph_type.directed is False
    assert not g.contains_edge_between(2, 1)
    assert g2.contains_edge_between(2, 1)


def test_as_unmodifiable():

    g = create_graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    v1 = 0
    g.add_vertex(1)
    v2 = 1
    g.add_vertex(2)
    v3 = 2
    g.add_vertex(3)
    v4 = 3
    g.add_vertex(4)
    v5 = 4

    g.create_edge(v1, v2)
    g.create_edge(v2, v3)
    g.create_edge(v1, v4)
    g.create_edge(v1, v1)
    g.create_edge(v4, v5)
    g.create_edge(v5, v1)

    # unmodifiable
    g3 = as_unmodifiable(g)
    assert g3.graph_type.modifiable is False
    with pytest.raises(UnsupportedOperationError):
        g3.create_edge(v2, v2)


def test_as_edgereversed():
    g = create_graph(directed=True, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    v1 = 0
    g.add_vertex(1)
    v2 = 1
    g.add_vertex(2)
    v3 = 2
    g.add_vertex(3)
    v4 = 3
    g.add_vertex(4)
    v5 = 4
    
    g.create_edge(v1, v2)
    g.create_edge(v2, v3)
    g.create_edge(v1, v4)
    g.create_edge(v1, v1)
    e45 = g.create_edge(v4, v5)
    g.create_edge(v5, v1)

    # edge reversed
    g4 = as_edgereversed(g)
    assert g.edge_source(e45) == v4
    assert g.edge_target(e45) == v5
    assert g4.edge_source(e45) == v5
    assert g4.edge_target(e45) == v4

