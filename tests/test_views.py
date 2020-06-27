import pytest

from jgrapht import create_graph
from jgrapht.utils import create_vertex_supplier, create_edge_supplier

from jgrapht.types import GraphEvent
from jgrapht.views import (
    as_undirected,
    as_edge_reversed,
    as_unmodifiable,
    as_unweighted,
    as_masked_subgraph,
    as_weighted,
    as_listenable,
    as_graph_union,
)


def test_as_unweighted():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

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
    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v1, v4)
    g.add_edge(v1, v1)
    e45 = g.add_edge(v4, v5)
    g.add_edge(v5, v1)

    g.set_edge_weight(e45, 100.0)

    g1 = as_unweighted(g)

    assert g.type.directed == g1.type.directed
    assert g.type.allowing_self_loops == g1.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == g1.type.allowing_multiple_edges
    assert g.type.weighted != g1.type.weighted
    assert g.get_edge_weight(e45) == 100.0
    assert g1.get_edge_weight(e45) == 1.0


def test_as_undirected():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

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

    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v1, v4)
    g.add_edge(v1, v1)
    g.add_edge(v4, v5)
    g.add_edge(v5, v1)

    # undirected
    g2 = as_undirected(g)
    assert g2.type.directed is False
    assert not g.contains_edge_between(2, 1)
    assert g2.contains_edge_between(2, 1)


def test_as_unmodifiable():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

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

    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v1, v4)
    g.add_edge(v1, v1)
    g.add_edge(v4, v5)
    g.add_edge(v5, v1)

    # unmodifiable
    g3 = as_unmodifiable(g)
    assert g3.type.modifiable is False
    with pytest.raises(ValueError):
        g3.add_edge(v2, v2)


def test_as_edge_reversed():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

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

    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v1, v4)
    g.add_edge(v1, v1)
    e45 = g.add_edge(v4, v5)
    g.add_edge(v5, v1)

    # edge reversed
    g4 = as_edge_reversed(g)
    assert g.edge_source(e45) == v4
    assert g.edge_target(e45) == v5
    assert g4.edge_source(e45) == v5
    assert g4.edge_target(e45) == v4


def test_as_masked_subgraph():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(2, 3)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    def vertex_mask(v):
        if v == 3:
            return True
        return False

    def edge_mask(e):
        if e == 5:
            return True
        return False

    masked_graph = as_masked_subgraph(
        g, vertex_mask_cb=vertex_mask, edge_mask_cb=edge_mask
    )

    assert masked_graph.vertices == {0, 1, 2, 4}
    assert masked_graph.edges == {0, 1}
    assert not masked_graph.type.modifiable

    # test that we see changes in the original graph
    g.add_vertex(5)

    assert masked_graph.vertices == {0, 1, 2, 4, 5}

    # test that we are unmodifiable
    with pytest.raises(ValueError):
        masked_graph.add_vertex(6)


def test_anyhashableg_as_masked_subgraph():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex('v0')
    g.add_vertex('v1')
    g.add_vertex('v2')
    g.add_vertex('v3')
    g.add_vertex('v4')

    g.add_edge('v0', 'v1', edge='e1')
    g.add_edge('v0', 'v2', edge='e2')
    g.add_edge('v0', 'v3', edge='e3')
    g.add_edge('v2', 'v3', edge='e4')
    g.add_edge('v1', 'v3', edge='e5')
    g.add_edge('v2', 'v4', edge='e6')

    g.vertex_attrs['v0']['label'] = 'label0'
    g.vertex_attrs['v1']['label'] = 'label1'
    g.vertex_attrs['v2']['label'] = 'label2'
    g.vertex_attrs['v3']['label'] = 'label3'
    g.vertex_attrs['v4']['label'] = 'label4'

    assert g.vertex_attrs['v0']['label'] == 'label0'
    assert g.vertex_attrs['v1']['label'] == 'label1'
    assert g.vertex_attrs['v2']['label'] == 'label2'
    assert g.vertex_attrs['v3']['label'] == 'label3'
    assert g.vertex_attrs['v4']['label'] == 'label4'

    def vertex_mask(v):
        if v == 'v3':
            return True
        return False

    def edge_mask(e):
        if e == 'e5':
            return True
        return False

    masked_graph = as_masked_subgraph(
        g, vertex_mask_cb=vertex_mask, edge_mask_cb=edge_mask
    )


    assert masked_graph.vertices == {'v0', 'v1', 'v2', 'v4'}
    assert masked_graph.edges == {'e1', 'e2', 'e6'}
    assert not masked_graph.type.modifiable

    # test that while the sets are shared, our view is masked
    assert masked_graph._vertex_hash_to_id.__contains__('v3') == True
    assert masked_graph.vertices.__contains__('v3') == False
    assert masked_graph._edge_hash_to_id.__contains__('e5') == True
    assert masked_graph.edges.__contains__('e5') == False

    # test that we see changes in the original graph
    g.add_vertex('v5')

    assert masked_graph.vertices == {'v0', 'v1', 'v2', 'v4', 'v5'}

    g.add_edge('v5', 'v4', edge='e7')
    g.edge_attrs['e7']['capacity'] = 9.0

    assert masked_graph.edges == {'e1', 'e2', 'e6', 'e7'}

    # test that we are unmodifiable
    with pytest.raises(ValueError):
        masked_graph.add_vertex('v6')

    # test properties
    assert masked_graph.vertex_attrs['v0']['label'] == 'label0'
    assert masked_graph.vertex_attrs['v1']['label'] == 'label1'
    assert masked_graph.vertex_attrs['v2']['label'] == 'label2'
    assert masked_graph.vertex_attrs['v4']['label'] == 'label4'

    with pytest.raises(ValueError):
        assert masked_graph.vertex_attrs['v3']['label'] == 'label3'

    assert masked_graph.edge_attrs['e7']['capacity'] == 9.0

    with pytest.raises(ValueError):
        masked_graph.add_vertex()

    with pytest.raises(ValueError):
        masked_graph.remove_vertex('v2')

    with pytest.raises(ValueError):
        masked_graph.add_edge('v0', 'v1')

    with pytest.raises(ValueError):
        masked_graph.remove_edge('e1')    

    assert masked_graph.contains_vertex('v2')
    assert masked_graph.contains_edge('e1')

    repr(masked_graph)

def test_as_weighted():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

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
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(
        g, edge_weight_cb=None, cache_weights=False, write_weights_through=False
    )

    assert wg.get_edge_weight(0) == 1.0

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)


def test_as_weighted_with_caching():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

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
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e):
        return 100.5

    with pytest.raises(ValueError):
        wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=True)


def test_as_weighted_with_caching_and_write_throught():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

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
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1)

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

    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    lg = as_listenable(g)

    listener1_results = []

    def listener1(vertex, event):
        listener1_results.append("element {}, event {}".format(vertex, event))

    listener2_results = []

    def listener2(vertex, event):
        listener2_results.append("element {}, event {}".format(vertex, event))

    listener_id_1 = lg.add_listener(listener1)

    lg.add_vertex(0)
    lg.add_vertex(1)
    lg.add_vertex(2)
    lg.add_edge(0, 1)
    lg.add_edge(1, 2)

    listener_id_2 = lg.add_listener(listener2)

    lg.remove_edge(1)
    lg.remove_vertex(2)
    lg.set_edge_weight(0, 5.0)

    lg.remove_listener(listener_id_1)
    lg.remove_listener(listener_id_2)

    assert listener1_results == listener1_expected.splitlines()
    assert listener2_results == listener2_expected.splitlines()


def test_union():

    g1 = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g2 = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g = as_graph_union(g1, g2)

    assert not g.type.directed
    assert g.type.allowing_multiple_edges
    assert not g.type.modifiable

    g1.add_vertex(0)
    g1.add_vertex(1)
    g1.add_vertex(2)
    g1.add_vertex(3)

    g1.add_edge(2, 3, weight=7.0, edge=0)
    g1.add_edge(0, 1, weight=5.0, edge=1)
    g1.add_edge(1, 2, weight=6.0, edge=2)

    g2.add_vertex(2)
    g2.add_vertex(3)
    g2.add_vertex(4)
    g2.add_vertex(5)
    g2.add_vertex(6)

    g2.add_edge(2, 3, weight=8.0, edge=0)
    g2.add_edge(3, 4, weight=9.0, edge=1)
    g2.add_edge(4, 5, weight=9.0, edge=2)
    g2.add_edge(5, 6, weight=10.0, edge=3)

    assert g.vertices == {0, 1, 2, 3, 4, 5, 6}
    assert g.edges == {0, 1, 2, 3}

    assert g.edge_tuple(0) == (2, 3, 15.0)
    assert g.edge_tuple(1) == (0, 1, 14.0)
    assert g.edge_tuple(2) == (1, 2, 15.0)
    assert g.edge_tuple(3) == (5, 6, 10.0)


def test_union_with_combiner():

    g1 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g2 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def max_weight_combiner(x, y):
        return max(x, y)

    g = as_graph_union(g1, g2, edge_weight_combiner_cb=max_weight_combiner)

    assert g.type.directed
    assert g.type.allowing_multiple_edges
    assert not g.type.modifiable

    g1.add_vertex(0)
    g1.add_vertex(1)
    g1.add_vertex(2)
    g1.add_vertex(3)

    g1.add_edge(2, 3, weight=7.0, edge=0)
    g1.add_edge(0, 1, weight=5.0, edge=1)
    g1.add_edge(1, 2, weight=6.0, edge=2)

    g2.add_vertex(2)
    g2.add_vertex(3)
    g2.add_vertex(4)
    g2.add_vertex(5)
    g2.add_vertex(6)

    g2.add_edge(3, 2, weight=8.0, edge=0)
    g2.add_edge(3, 4, weight=9.0, edge=1)
    g2.add_edge(4, 5, weight=3.0, edge=2)
    g2.add_edge(5, 6, weight=10.0, edge=3)

    assert g.vertices == {0, 1, 2, 3, 4, 5, 6}
    assert g.edges == {0, 1, 2, 3}

    assert g.edge_tuple(0) == (2, 3, 8.0)
    assert g.edge_tuple(1) == (0, 1, 9.0)
    assert g.edge_tuple(2) == (1, 2, 6.0)
    assert g.edge_tuple(3) == (5, 6, 10.0)


def test_bad_union():

    g1 = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g2 = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    with pytest.raises(ValueError):
        g = as_graph_union(g1, g2)

    with pytest.raises(ValueError):
        g = as_graph_union(g2, g1)


def test_anyhashableg_bad_union():

    g1 = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )
    g2 = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
    )

    with pytest.raises(ValueError):
        g = as_graph_union(g1, g2)



def test_anyhashableg_as_unweighted():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_edge("0", "1", edge="e1")
    g.set_edge_weight("e1", 100.0)

    assert g.get_edge_weight("e1") == 100.0

    ug = as_unweighted(g)

    assert g.type.directed == ug.type.directed
    assert g.type.allowing_self_loops == ug.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == ug.type.allowing_multiple_edges
    assert g.type.weighted != ug.type.weighted

    assert g.get_edge_weight("e1") == 100.0
    assert ug.get_edge_weight("e1") == 1.0


def test_anyhashableg_as_undirected():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_vertex("2")
    g.add_edge("0", "1", edge="e1")
    g.add_edge("1", "2", edge="e2")

    g.edge_attrs['e1']['capacity'] = 5.0
    g.edge_attrs['e2']['capacity'] = 15.0

    assert not g.contains_edge_between("1", "0")

    ug = as_undirected(g)

    assert g.type.directed != ug.type.directed
    assert g.type.allowing_self_loops == ug.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == ug.type.allowing_multiple_edges
    assert g.type.weighted == ug.type.weighted

    assert ug.contains_edge_between("1", "0")

    assert ug.edge_attrs['e1']['capacity'] == 5.0
    assert ug.edge_attrs['e2']['capacity'] == 15.0

    # test that properties are shared
    ug.edge_attrs['e1']['capacity'] = 105.0
    assert g.edge_attrs['e1']['capacity'] == 105.0


def test_anyhashableg_as_unmodifiable():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_edge("0", "1", edge="e1")

    ug = as_unmodifiable(g)

    assert g.type.directed == ug.type.directed
    assert g.type.allowing_self_loops == ug.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == ug.type.allowing_multiple_edges
    assert g.type.weighted == ug.type.weighted

    with pytest.raises(ValueError):
        ug.add_vertex("2")

    
def test_anyhashableg_two_wrappers():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_edge("0", "1", edge="e1")

    ug = as_undirected(g)
    ug = as_unmodifiable(ug)

    assert g.type.directed != ug.type.directed
    assert g.type.allowing_self_loops == ug.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == ug.type.allowing_multiple_edges
    assert g.type.weighted == ug.type.weighted
    assert g.type.modifiable != ug.type.modifiable

    with pytest.raises(ValueError):
        ug.add_vertex("2")

    assert ug.contains_edge_between("1", "0")


def test_as_unweighted_on_property_graphs():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    g.add_vertex()
    g.add_vertex()
    g.add_vertex()
    g.add_vertex()
    g.add_edge('v0', 'v1')
    g.add_edge('v1', 'v2')
    g.add_edge('v2', 'v3')

    g.set_edge_weight('e0', 100.0)
    g.set_edge_weight('e1', 50.0)
    g.set_edge_weight('e2', 25.0)

    g.vertex_attrs['v0']['before'] = 'v0'
    g.vertex_attrs['v1']['before'] = 'v1'
    g.edge_attrs['e0']['before'] = 'e0'
    g.edge_attrs['e1']['before'] = 'e1'

    g1 = as_unweighted(g)

    assert g.type.directed == g1.type.directed
    assert g.type.allowing_self_loops == g1.type.allowing_self_loops
    assert g.type.allowing_multiple_edges == g1.type.allowing_multiple_edges
    assert g.type.weighted != g1.type.weighted

    assert g1.get_edge_weight('e0') == 1.0
    assert g1.get_edge_weight('e1') == 1.0
    assert g1.get_edge_weight('e2') == 1.0

    # test that properties still exist
    assert g.vertex_attrs['v0']['before'] == 'v0'
    assert g.vertex_attrs['v1']['before'] == 'v1'
    assert g.edge_attrs['e0']['before'] == 'e0'
    assert g.edge_attrs['e1']['before'] == 'e1'

    assert g1.vertex_attrs['v0']['before'] == 'v0'
    assert g1.vertex_attrs['v1']['before'] == 'v1'
    assert g1.edge_attrs['e0']['before'] == 'e0'
    assert g1.edge_attrs['e1']['before'] == 'e1'

    # test adding a property in g
    g.vertex_attrs['v0']['after'] = 'v0'
    assert g1.vertex_attrs['v0']['after'] == 'v0'

    # test adding a property in g1
    g1.edge_attrs['e0']['after'] = 'e0'
    assert g.edge_attrs['e0']['after'] == 'e0'

    # test deleting a property from g 
    del g.vertex_attrs['v1']['before']
    with pytest.raises(KeyError):
        g1.vertex_attrs['v1']['before']

    with pytest.raises(ValueError):
        g1.edge_attrs['e0']['weight'] = 200.0

    g.edge_attrs['e0']['weight'] = 200.0
    assert g.edge_attrs['e0']['weight'] == 200.0
    assert g1.edge_attrs['e0']['weight'] == 1.0


def test_anyhashableg_as_weighted():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex('0')
    g.add_vertex('1')
    g.add_edge('0', '1', edge='0')

    with pytest.raises(ValueError):
        g.set_edge_weight('0', 5.0)

    assert g.get_edge_weight('0') == 1.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=False, write_weights_through=False)

    assert wg.get_edge_weight('0') == 100.5

    print(g)
    print(wg)

    with pytest.raises(ValueError):
        wg.set_edge_weight('0', 5.0)



def test_anyhashableg_as_weighted_with_None_function():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1, edge=0)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(
        g, edge_weight_cb=None, cache_weights=False, write_weights_through=False
    )

    assert wg.get_edge_weight(0) == 1.0

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)


def test_anyhashableg_as_weighted_with_caching():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1, edge=0)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    with pytest.raises(ValueError):
        g.edge_attrs[0]['weight'] = 5.0

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=False)

    assert wg.get_edge_weight(0) == 100.5

    assert wg.edge_attrs[0]['weight'] == 100.5

    wg.set_edge_weight(0, 5.0)

    assert wg.get_edge_weight(0) == 5.0
    assert wg.edge_attrs[0]['weight'] == 5.0


def test_anyhashableg_as_weighted_with_caching_and_write_throught_with_unweighted():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1, edge=0)

    with pytest.raises(ValueError):
        g.set_edge_weight(0, 5.0)

    with pytest.raises(ValueError):
        g.edge_attrs[0]['weight'] = 5.0

    assert g.get_edge_weight(0) == 1.0

    def edge_weight(e):
        return 100.5

    with pytest.raises(ValueError):
        wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=True)


def test_anyhashableg_as_weighted_with_caching_and_write_throught():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1, edge=0)

    g.set_edge_weight(0, 200.0)
    assert g.get_edge_weight(0) == 200.0

    assert g.edge_attrs[0]['weight'] == 200.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=True, write_weights_through=True)

    assert wg.get_edge_weight(0) == 100.5

    wg.set_edge_weight(0, 5.0)

    assert wg.get_edge_weight(0) == 5.0

    assert wg.edge_attrs[0]['weight'] == 5.0

    assert g.get_edge_weight(0) == 5.0

    assert g.edge_attrs[0]['weight'] == 5.0


def test_anyhashableg_as_weighted_with_no_caching_and_write_through():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_edge(0, 1, edge=0)

    g.set_edge_weight(0, 5.0)
    assert g.get_edge_weight(0) == 5.0
    assert g.edge_attrs[0]['weight'] == 5.0

    def edge_weight(e):
        return 100.5

    wg = as_weighted(g, edge_weight, cache_weights=False, write_weights_through=True)

    assert wg.get_edge_weight(0) == 100.5

    with pytest.raises(ValueError):
        wg.set_edge_weight(0, 5.0)

    with pytest.raises(ValueError):
        wg.edge_attrs[0]['weight'] = 5.0

    assert wg.get_edge_weight(0) == 100.5

    assert wg.edge_attrs[0]['weight'] == 100.5


pg_listener1_expected = """element v0, event GraphEvent.VERTEX_ADDED
element v1, event GraphEvent.VERTEX_ADDED
element v2, event GraphEvent.VERTEX_ADDED
element e0, event GraphEvent.EDGE_ADDED
element e1, event GraphEvent.EDGE_ADDED
element e1, event GraphEvent.EDGE_REMOVED
element v2, event GraphEvent.VERTEX_REMOVED
element e0, event GraphEvent.EDGE_WEIGHT_UPDATED"""

pg_listener2_expected = """element e1, event GraphEvent.EDGE_REMOVED
element v2, event GraphEvent.VERTEX_REMOVED
element e0, event GraphEvent.EDGE_WEIGHT_UPDATED"""


def test_anyhashableg_listenable():

    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    lg = as_listenable(g)

    listener1_results = []

    def listener1(vertex, event):
        listener1_results.append("element {}, event {}".format(vertex, event))

    listener2_results = []

    def listener2(vertex, event):
        listener2_results.append("element {}, event {}".format(vertex, event))

    listener_id_1 = lg.add_listener(listener1)

    lg.add_vertex('v0')
    lg.add_vertex('v1')
    lg.add_vertex('v2')
    lg.add_edge('v0', 'v1', edge='e0')
    lg.add_edge('v1', 'v2', edge='e1')

    listener_id_2 = lg.add_listener(listener2)

    lg.remove_edge('e1')
    lg.remove_vertex('v2')
    lg.set_edge_weight('e0', 5.0)

    lg.remove_listener(listener_id_1)
    lg.remove_listener(listener_id_2)

    assert listener1_results == pg_listener1_expected.splitlines()
    assert listener2_results == pg_listener2_expected.splitlines()



def test_anyhashableg_as_edge_reversed():
    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

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

    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v1, v4)
    g.add_edge(v1, v1)
    e45 = g.add_edge(v4, v5)
    g.add_edge(v5, v1)

    # edge reversed
    g4 = as_edge_reversed(g)
    assert g.edge_source(e45) == v4
    assert g.edge_target(e45) == v5
    assert g4.edge_source(e45) == v5
    assert g4.edge_target(e45) == v4
