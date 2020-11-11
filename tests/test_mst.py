import pytest

from jgrapht import create_graph

import jgrapht.algorithms.spanning as spanning
import jgrapht.generators as generators


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(0, 6)
    g.add_edge(0, 7)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


def test_kruskal():
    g = build_graph()
    mst_w, mst_edges = spanning.kruskal(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution


def test_prim():
    g = build_graph()
    mst_w, mst_edges = spanning.prim(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution


def test_boruvka():
    g = build_graph()
    mst_w, mst_edges = spanning.boruvka(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution


def test_small_graph_prim():
    g = create_graph(directed=False)

    generators.gnp_random_graph(g, n=500, p=0.1, seed=17)

    mst_w, mst_edges = spanning.prim(g)
    assert mst_w == 499.0


def test_anyhashableg_prim():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_vertex("2")

    e1 = g.add_edge("0", "1")
    g.set_edge_weight(e1, 1.0)
    e2 = g.add_edge("1", "2")
    g.set_edge_weight(e2, 2.0)
    e3 = g.add_edge("2", "0")
    g.set_edge_weight(e3, 3.0)

    mst_w, mst_edges = spanning.prim(g)
    assert mst_w == 3.0
    assert set(mst_edges) == {e1, e2}
    
def test_result_with_difference(): 
    g = build_graph()
    mst_weight, mst_tree = spanning.prim(g)

    non_mst_edges = g.edges - set(mst_tree)

    # test that our intermediate set results, property implement
    # method _from_iterable

    assert non_mst_edges == { 9, 10, 11, 12, 13, 14, 15, 16, 17 }

def test_result_with_difference_symmetric(): 
    g = build_graph()
    mst_weight, mst_tree = spanning.prim(g)

    non_mst_edges = g.edges - set(mst_tree)

    # test that our intermediate set results, property implement
    # method _from_iterable

    assert non_mst_edges == { 9, 10, 11, 12, 13, 14, 15, 16, 17 }
