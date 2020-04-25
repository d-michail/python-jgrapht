import pytest

import jgrapht.graph as graph
import jgrapht.algorithms.coloring as coloring

def test_coloring():
    g = graph.Graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 10):
        g.add_vertex()

    vcount = len(g.vertices())
    assert vcount == 10

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

    assert len(g.edges()) == 18

    color_count, color_map = coloring.coloring_greedy(g)
    assert color_count == 4
    assert all([a == b for a,b in zip([color_map[v] for v in g.vertices()], [0, 1, 2, 1, 2, 1, 2, 1, 2, 3])]) 
    assert all([color_map[u]!=color_map[v] for u, v in zip([g.edge_source(e) for e in g.edges()], [g.edge_target(e) for e in g.edges()])])
    

    color_count, color_map = coloring.coloring_greedy_random(g, seed=17)
    assert color_count == 4
    assert all([a == b for a,b in zip([color_map[v] for v in g.vertices()], [1, 2, 0, 2, 0, 2, 3, 0, 2, 0])])
    assert all([color_map[u]!=color_map[v] for u, v in zip([g.edge_source(e) for e in g.edges()], [g.edge_target(e) for e in g.edges()])]) 

    color_count, color_map = coloring.coloring_greedy_dsatur(g)
    assert color_count == 4
    assert all([a == b for a,b in zip([color_map[v] for v in g.vertices()], [0, 1, 2, 1, 2, 1, 3, 2, 1, 2])])
    assert all([color_map[u]!=color_map[v] for u, v in zip([g.edge_source(e) for e in g.edges()], [g.edge_target(e) for e in g.edges()])])     

    color_count, color_map = coloring.coloring_backtracking_brown(g)
    assert color_count == 4
    assert all([a == b for a,b in zip([color_map[v] for v in g.vertices()], [1, 2, 3, 2, 3, 2, 3, 2, 3, 4])])    
    assert all([color_map[u]!=color_map[v] for u, v in zip([g.edge_source(e) for e in g.edges()], [g.edge_target(e) for e in g.edges()])])         

    color_count, color_map = coloring.coloring_color_refinement(g)
    assert color_count == 10
