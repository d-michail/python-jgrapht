import pytest

import jgrapht.graph as graph
import jgrapht.generators as generators


def test_barabasi_albert():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_barabasi_albert(g, 10, 5, 100)
    assert len(g.vertices()) == 100

def test_barabasi_albert_forest():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_barabasi_albert_forest(g, 10, 100)
    assert len(g.vertices()) == 100

def test_complete():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_complete(g, 10)
    assert len(g.vertices()) == 10

def test_complete_bipartite():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_complete_bipartite(g, 10, 10)
    assert len(g.vertices()) == 20

def test_empty():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_empty(g, 10)
    assert len(g.vertices()) == 10

def test_gnm_random():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_gnm_random(g, 10, 30)
    assert len(g.vertices()) == 10

def test_gnp_random():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_gnp_random(g, 10, 0.2)
    assert len(g.vertices()) == 10

def test_ring():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_ring(g, 10)
    assert len(g.vertices()) == 10

def test_scalefree():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_scalefree(g, 10)
    assert len(g.vertices()) == 10

def test_watts_strogatz():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_watts_strogatz(g, 10, 2, 0.1)
    assert len(g.vertices()) == 10

def test_kleinberg_smallworld():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    generators.generate_kleinberg_smallworld(g, 10, 2, 2, 1)
    assert len(g.vertices()) == 100
