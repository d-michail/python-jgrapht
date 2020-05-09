import pytest

from jgrapht import create_graph
import jgrapht.algorithms.spanning as spanning

def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 10):
        g.add_vertex(i)

    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(0, 4)
    g.create_edge(0, 5)
    g.create_edge(0, 6)
    g.create_edge(0, 7)
    g.create_edge(0, 8)
    g.create_edge(0, 9)

    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 6)
    g.create_edge(6, 7)
    g.create_edge(7, 8)
    g.create_edge(8, 9)
    g.create_edge(9, 1)

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
