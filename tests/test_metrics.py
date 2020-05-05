import pytest

from jgrapht import create_graph
from jgrapht.metrics import diameter, radius, girth, count_triangles

def create_test_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

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


def test_diameter():
    g = create_test_graph()
    assert diameter(g) == 2.0

def test_radius():
    g = create_test_graph()
    assert radius(g) == 1.0

def test_girth():
    g = create_test_graph()
    assert girth(g) == 3.0

def test_count_triangles():
    g = create_test_graph()
    assert count_triangles(g) == 9

