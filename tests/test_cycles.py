import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cycles as cycles


def test_hierholzer():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    
    g.add_vertices_from([0,1,2,3])
    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)

    cycle = cycles.eulerian_cycle(g)

    assert cycle is not None
    assert cycle.edges == [3, 0, 1, 2]


def test_chinese_postman():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    
    g.add_vertices_from([0,1,2,3,4])
    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)
    g.create_edge(3, 4)

    closed_walk = cycles.chinese_postman(g)

    assert closed_walk is not None
    assert closed_walk.edges == [4, 3, 0, 1, 2, 4]
