import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cuts as cuts



def test_gomory_hu_tree():
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

    e01 = g.add_edge(0, 1, weight=20)
    e02 = g.add_edge(0, 2, weight=10)
    g.add_edge(1, 2, weight=30)
    g.add_edge(1, 3, weight=10)
    g.add_edge(2, 3, weight=20)

    ght = cuts.gomory_hu_gusfield(g)

    mincut = ght.min_cut()
    assert mincut.capacity == 30.0
    assert mincut.edges == {0, 1}

    cut_1_3 = ght.min_st_cut(1, 3)
    assert cut_1_3.capacity == 30.0
    assert cut_1_3.edges == {3, 4}

    cut_1_2 = ght.min_st_cut(1, 2)
    assert cut_1_2.capacity == 50.0
    assert cut_1_2.edges == {1, 2, 3}

    tree = ght.as_graph()
    edge_tuples = [tree.edge_tuple(e) for e in tree.edges]
    assert edge_tuples == [(1,0,30.0), (2,1,50.0), (3,2,30.0)]


def test_anyhashableg_gomory_hu_tree():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex("1")
    g.add_vertex(2)
    g.add_vertex(3)

    e0 = g.add_edge(0, "1", weight=20)
    e1 = g.add_edge(0, 2, weight=10)
    e2 = g.add_edge("1", 2, weight=30)
    e3 = g.add_edge("1", 3, weight=10)
    e4 = g.add_edge(2, 3, weight=20)

    ght = cuts.gomory_hu_gusfield(g)

    mincut = ght.min_cut()
    assert mincut.capacity == 30.0
    assert mincut.edges == {e0, e1}

    cut_1_3 = ght.min_st_cut("1", 3)
    assert cut_1_3.capacity == 30.0
    assert cut_1_3.edges == {e3, e4}

    cut_1_2 = ght.min_st_cut("1", 2)
    assert cut_1_2.capacity == 50.0
    assert cut_1_2.edges == {e1, e2, e3}

    tree = ght.as_graph()
    edge_tuples = [tree.edge_tuple(e) for e in tree.edges]
    assert edge_tuples == [("1",0,30.0), (2,"1",50.0), (3,2,30.0)]