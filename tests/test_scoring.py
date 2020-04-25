import pytest

import jgrapht.graph as graph
import jgrapht.algorithms.scoring as scoring

def build_graph():

    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 10):
        g.add_vertex()

    e01 = g.add_edge(0, 1)
    e02 = g.add_edge(0, 2)
    e03 = g.add_edge(0, 3)
    e04 = g.add_edge(0, 4)
    e05 = g.add_edge(0, 5)
    e06 = g.add_edge(0, 6)
    e07 = g.add_edge(0, 7)
    e08 = g.add_edge(0, 8)
    e09 = g.add_edge(0, 9)

    e12 = g.add_edge(1, 2)
    e23 = g.add_edge(2, 3)
    e34 = g.add_edge(3, 4)
    e45 = g.add_edge(4, 5)
    e56 = g.add_edge(5, 6)
    e67 = g.add_edge(6, 7)
    e78 = g.add_edge(7, 8)
    e89 = g.add_edge(8, 9)
    e91 = g.add_edge(9, 1)

    return g


def test_pagerank():
    g = build_graph()
    scores = scoring.scoring_pagerank(g)
    result = [scores[v] for v in g.vertices()]
    expected = [0.2324869499599194, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115, 0.08527922778223115]
    assert all([a == b for a,b in zip(result, expected)]) 


def test_harmonic_centrality():
    g = build_graph()
    scores = scoring.scoring_harmonic_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [1.0, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666, 0.6666666666666666]
    assert all([a == b for a,b in zip(result, expected)]) 
    #print (result)
    #assert False

def test_closeness_centrality():
    g = build_graph()
    scores = scoring.scoring_closeness_centrality(g)
    result = [scores[v] for v in g.vertices()]
    print (result)
    expected = [1.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    assert all([a == b for a,b in zip(result, expected)]) 
    #assert False    

def test_betweenness_centrality():
    g = build_graph()
    scores = scoring.scoring_betweenness_centrality(g)
    result = [scores[v] for v in g.vertices()]
    print (result)
    expected = [22.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert all([a == b for a,b in zip(result, expected)]) 

def test_alpha_centrality():
    g = build_graph()
    scores = scoring.scoring_alpha_centrality(g)
    result = [scores[v] for v in g.vertices()]
    expected = [1.09284015241, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011, 1.03155950011]
    assert all([a == b for a,b in zip(result, expected)]) 
