import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cuts as cuts

def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 10):
        g.add_vertex(i)

    g.create_edge(0, 1, weight=3)
    g.create_edge(0, 2)
    g.create_edge(0, 3, weight=2)
    g.create_edge(0, 4)
    g.create_edge(0, 5, weight=3)
    g.create_edge(0, 6)
    g.create_edge(0, 7, weight=100)
    g.create_edge(0, 8)
    g.create_edge(0, 9)

    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 6, weight=2)
    g.create_edge(6, 7)
    g.create_edge(7, 8)
    g.create_edge(8, 9)
    g.create_edge(9, 1)

    return g

def test_stoer_wagner():
    g = build_graph()
    cut = cuts.stoer_wagner(g)
    assert cut.weight == 3.0
    assert cut.edges == set([8, 16, 17])
    assert cut.source_partition == set([9])
