import pytest

from jgrapht import create_graph
import jgrapht.metrics as metrics

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
    assert metrics.diameter(g) == 2.0

def test_radius():
    g = create_test_graph()
    assert metrics.radius(g) == 1.0

def test_girth():
    g = create_test_graph()
    assert metrics.girth(g) == 3.0

def test_count_triangles():
    g = create_test_graph()
    assert metrics.count_triangles(g) == 9

def test_measure():
    g = create_test_graph()

    d, r, center, periphery, pseudo_periphery, eccentricity_map = metrics.measure(g)

    assert d == 2.0
    assert r == 1.0
    assert center == set([0])
    assert periphery == set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert pseudo_periphery == set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    assert eccentricity_map[0] == 1.0
    for i in range(1,10): 
        assert eccentricity_map[i] == 2.0

