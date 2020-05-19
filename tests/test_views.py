import pytest

from jgrapht import create_graph
from jgrapht.types import GraphEvent
from jgrapht.views import (
    as_undirected,
    as_edge_reversed,
    as_unmodifiable,
    as_unweighted,
    as_masked_subgraph,
    as_weighted,
    as_listenable,
)

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

    assert g.type.directed == g1.type.directed
    assert g.type.allowing_self_loops == g1.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == g1.type.allowing_multiple_edges
    assert g.type.weighted != g1.type.weighted
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
    assert g2.type.directed is False
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
    assert g3.type.modifiable is False
    with pytest.raises(ValueError):
        g3.create_edge(v2, v2)


def test_as_edge_reversed():
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
    g4 = as_edge_reversed(g)
    assert g.edge_source(e45) == v4
    assert g.edge_target(e45) == v5
    assert g4.edge_source(e45) == v5
    assert g4.edge_target(e45) == v4


def test_as_masked_subgraph():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    
    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(2, 3)
    g.create_edge(1, 3)
    g.create_edge(2, 4)

    def vertex_mask(v): 
        if v == 3: 
            return True
        return False

    def edge_mask(e): 
        if e == 5: 
            return True
        return False
    
    masked_graph = as_masked_subgraph(g, vertex_mask_cb=vertex_mask, edge_mask_cb=edge_mask)

    assert masked_graph.vertices == {0,1,2,4}
    assert masked_graph.edges == {0,1}
    assert not masked_graph.type.modifiable

    # test that we see changed in the original graph
    g.add_vertex(5)

    assert masked_graph.vertices == {0, 1, 2, 4, 5}

    # test that we are unmodifiable
    with pytest.raises(ValueError):
        masked_graph.add_vertex(6)


def test_as_weighted():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=False)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e): 
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=False, write_weights_through=False)

    assert wg.get_edge_weight(0) == 100.5

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)


def test_as_weighted_with_None_function():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=False)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e): 
        return 100.5

    wg = as_weighted(g, edge_weight_cb=None, cache_weights=False, write_weights_through=False)

    assert wg.get_edge_weight(0) == 1.0

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)


def test_as_weighted_with_caching():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=False)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e): 
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=False)

    assert wg.get_edge_weight(0) == 100.5

    wg.set_edge_weight(0, 5.0)

    assert wg.get_edge_weight(0) == 5.0


def test_as_weighted_with_caching_and_write_throught_with_unweighted():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=False)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e): 
        return 100.5

    with pytest.raises(ValueError):
        wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=True)


def test_as_weighted_with_caching_and_write_throught():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    g.set_edge_weight(0, 200.0)
    assert g.get_edge_weight(0) == 200.0

    def edge_weight(e): 
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=True)

    assert wg.get_edge_weight(0) == 100.5

    wg.set_edge_weight(0, 5.0)

    assert wg.get_edge_weight(0) == 5.0

    assert g.get_edge_weight(0) == 5.0


def test_as_weighted_with_no_caching_and_write_through():
    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    g.add_vertex(0)
    g.add_vertex(1)
    g.create_edge(0, 1)

    g.set_edge_weight(0, 5.0)
    assert g.get_edge_weight(0) == 5.0

    def edge_weight(e): 
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=False, write_weights_through=True)

    assert wg.get_edge_weight(0) == 100.5

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)

    assert wg.get_edge_weight(0) == 100.5    


listener1_expected = """element 0, event GraphEvent.VERTEX_ADDED
element 1, event GraphEvent.VERTEX_ADDED
element 2, event GraphEvent.VERTEX_ADDED
element 0, event GraphEvent.EDGE_ADDED
element 1, event GraphEvent.EDGE_ADDED
element 1, event GraphEvent.EDGE_REMOVED
element 2, event GraphEvent.VERTEX_REMOVED
element 0, event GraphEvent.EDGE_WEIGHT_UPDATED"""

listener2_expected = """element 1, event GraphEvent.EDGE_REMOVED
element 2, event GraphEvent.VERTEX_REMOVED
element 0, event GraphEvent.EDGE_WEIGHT_UPDATED"""


def test_listenable(): 

    g = create_graph(directed=False, allowing_self_loops=True, allowing_multiple_edges=False, weighted=True)

    lg = as_listenable(g)


    listener1_results = []
    def listener1(vertex, event):
        listener1_results.append('element {}, event {}'.format(vertex, event))

    listener2_results = []
    def listener2(vertex, event):
        listener2_results.append('element {}, event {}'.format(vertex, event))

    listener_id_1 = lg.add_listener(listener1)

    lg.add_vertex(0)
    lg.add_vertex(1)
    lg.add_vertex(2)
    lg.create_edge(0, 1)
    lg.create_edge(1, 2)

    listener_id_2 = lg.add_listener(listener2)

    lg.remove_edge(1)
    lg.remove_vertex(2)
    lg.set_edge_weight(0, 5.0)

    lg.remove_listener(listener_id_1)
    lg.remove_listener(listener_id_2)

    assert listener1_results == listener1_expected.splitlines()
    assert listener2_results == listener2_expected.splitlines()
