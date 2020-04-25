import pytest

import jgrapht.graph as graph
import jgrapht.traversal as traversal


def test_traversals():
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

    bfs = list(traversal.bfs_traversal(g))
    assert bfs == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    bfs_from_5 = list(traversal.bfs_traversal(g, 5))
    assert bfs_from_5 == [5, 0, 4, 6, 1, 2, 3, 7, 8, 9]

    dfs = list(traversal.dfs_traversal(g))
    assert dfs == [0, 9, 1, 2, 3, 4, 5, 6, 7, 8]

    dfs_from_5 = list(traversal.dfs_traversal(g, 5))
    assert dfs_from_5 == [5, 6, 7, 8, 9, 1, 2, 3, 4, 0]

    lex_bfs = list(traversal.lexicographic_bfs_traversal(g))
    assert lex_bfs == [0, 1, 2, 9, 3, 8, 4, 7, 5, 6]

    max_card = list(traversal.max_cardinality_traversal(g))
    assert max_card == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    degeneracy_ordering = list(traversal.degeneracy_ordering_traversal(g))
    assert degeneracy_ordering == [1, 2, 3, 4, 5, 6, 0, 7, 8, 9]

    random_walk = list(traversal.random_walk_traversal(g, 0, False, 3, 17))
    assert random_walk == [7, 0, 2]

    closest_first = list(traversal.closest_first_traversal(g, 0))
    assert closest_first == [0, 1, 3, 5, 4, 9, 8, 2, 7, 6]


def test_dag():
    # Create a dag to test top
    g1 = graph.Graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    g1.add_vertex()
    g1.add_vertex()
    g1.add_vertex()
    g1.add_vertex()

    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(3, 2)

    topo = list(traversal.topological_order_traversal(g1))
    assert topo == [0, 3, 1, 2]

    

