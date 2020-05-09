import pytest

from jgrapht import create_graph
import jgrapht.algorithms.scoring as scoring

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


def test_pagerank():
    g = build_graph()
    scores = scoring.pagerank(g)
    result = [scores[v] for v in g.vertices()]
    expected = [0.2324869499599194, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115]
    assert result == expected


def test_harmonic_centrality():
    g = build_graph()
    scores = scoring.harmonic_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [1.0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666]
    assert result == expected

def test_closeness_centrality():
    g = build_graph()
    scores = scoring.closeness_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [1.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    assert result == expected

def test_betweenness_centrality():
    g = build_graph()
    scores = scoring.betweenness_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [22.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert result == expected

def test_alpha_centrality():
    g = build_graph()
    scores = scoring.alpha_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [1.09284015241, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011]
    assert result == expected
