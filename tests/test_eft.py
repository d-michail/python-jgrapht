import pytest

from jgrapht import create_graph
import jgrapht.algorithms.flow as flow



def test_eft():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)

    e01 = g.add_edge(0, 1, weight=20)
    e02 = g.add_edge(0, 2, weight=10)
    g.add_edge(1, 2, weight=30)
    g.add_edge(1, 3, weight=10)
    g.add_edge(2, 3, weight=20)
    g.add_edge(3, 4, weight=10)

    eft = flow.equivalent_flow_tree_gusfield(g)

    assert eft.max_st_flow_value(2,3) == 30.0
    assert eft.max_st_flow_value(1,3) == 30.0
    assert eft.max_st_flow_value(0,1) == 30.0
    assert eft.max_st_flow_value(0,2) == 30.0
    assert eft.max_st_flow_value(0,3) == 30.0
    assert eft.max_st_flow_value(0,4) == 10.0

    tree = eft.as_graph()
    edge_tuples = [tree.edge_tuple(e) for e in tree.edges]
    assert edge_tuples == [(1,0,30.0), (2,1,50.0), (3,2,30.0), (4,3,10.0)]


def test_anyhashableg_eft():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)

    e01 = g.add_edge(0, 1, weight=20, edge='e01')
    e02 = g.add_edge(0, 2, weight=10, edge='e02')
    g.add_edge(1, 2, weight=30)
    g.add_edge(1, 3, weight=10)
    g.add_edge(2, 3, weight=20)
    g.add_edge(3, 4, weight=10)

    eft = flow.equivalent_flow_tree_gusfield(g)

    assert eft.max_st_flow_value(2,3) == 30.0
    assert eft.max_st_flow_value(1,3) == 30.0
    assert eft.max_st_flow_value(0,1) == 30.0
    assert eft.max_st_flow_value(0,2) == 30.0
    assert eft.max_st_flow_value(0,3) == 30.0
    assert eft.max_st_flow_value(0,4) == 10.0

    tree = eft.as_graph()
    edge_tuples = [tree.edge_tuple(e) for e in tree.edges]
    assert edge_tuples == [(1,0,30.0), (2,1,50.0), (3,2,30.0), (4,3,10.0)]
