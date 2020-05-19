import pytest

from jgrapht import create_graph
import jgrapht.generators as generators


def test_barabasi_albert():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.barabasi_albert_graph(g, 10, 5, 100)
    assert len(g.vertices) == 100

def test_barabasi_albert_forest():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.barabasi_albert_forest(g, 10, 100)
    assert len(g.vertices) == 100

def test_complete():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.complete_graph(g, 10)
    assert len(g.vertices) == 10

def test_complete_bipartite():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.complete_bipartite_graph(g, 10, 10)
    assert len(g.vertices) == 20

def test_empty():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.empty_graph(g, 10)
    assert len(g.vertices) == 10

def test_gnm_random():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.gnm_random_graph(g, 10, 30)
    assert len(g.vertices) == 10

def test_gnp_random():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.gnp_random_graph(g, 10, 0.2)
    assert len(g.vertices) == 10

def test_ring():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.ring_graph(g, 10)
    assert len(g.vertices) == 10

def test_scalefree():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.scalefree_graph(g, 10)
    assert len(g.vertices) == 10

def test_watts_strogatz():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.watts_strogatz_graph(g, 10, 2, 0.1)
    assert len(g.vertices) == 10

def test_kleinberg_smallworld():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.kleinberg_smallworld_graph(g, 10, 2, 2, 1)
    assert len(g.vertices) == 100
