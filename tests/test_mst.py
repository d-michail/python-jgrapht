import pytest

import jgrapht.graph as graph
import jgrapht.algorithms.spanners as spanners

def build_graph():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for _ in range(0, 10):
        g.add_vertex()

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
    mst_w, mst_edges = spanners.kruskal(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution


def test_prim():
    g = build_graph()
    mst_w, mst_edges = spanners.prim(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution


def test_boruvka():
    g = build_graph()
    mst_w, mst_edges = spanners.boruvka(g)
    assert mst_w == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(mst_edges)
    assert expected == solution
