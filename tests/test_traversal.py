import pytest

from jgrapht import create_graph

import jgrapht.traversal as traversal


def test_traversals():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

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

    random_walk_it = traversal.random_walk_traversal(g, 0, False)
    for i in range(0,100):
        v = next(random_walk_it)
        assert v is not None

    closest_first = list(traversal.closest_first_traversal(g, 0))
    assert closest_first == [0, 1, 3, 5, 4, 9, 8, 2, 7, 6]

    closest_first = list(traversal.closest_first_traversal(g, 0, radius=10))
    assert closest_first == [0, 1, 3, 5, 4, 9, 8, 2, 7, 6]


def test_dag():
    # Create a dag to test top
    g1 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g1.add_vertex(0)
    g1.add_vertex(1)
    g1.add_vertex(2)
    g1.add_vertex(3)

    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(3, 2)

    topo = list(traversal.topological_order_traversal(g1))
    assert topo == [0, 3, 1, 2]


def test_property_graph_traversals():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    for i in range(0, 9):
        g.add_vertex(str(i))
        
    g.add_vertex("node9")

    g.add_edge("0", "1", edge="e01")
    g.add_edge("0", "2", edge="e02")
    g.add_edge("0", "3", edge="e03")
    g.add_edge("0", "4", edge="e04")
    g.add_edge("0", "5", edge="e05")
    g.add_edge("0", "6", edge="e06")
    g.add_edge("0", "7", edge="e07")
    g.add_edge("0", "8", edge="e08")
    g.add_edge("0", "node9", edge="e09")

    g.add_edge("1", "2", edge="e12")
    g.add_edge("2", "3", edge="e23")
    g.add_edge("3", "4", edge="e34")
    g.add_edge("4", "5", edge="e45")
    g.add_edge("5", "6", edge="e56")
    g.add_edge("6", "7", edge="e67")
    g.add_edge("7", "8", edge="e78")
    g.add_edge("8", "node9", edge="e79")
    g.add_edge("node9", "1", edge="e91")


    bfs_it = traversal.bfs_traversal(g)
    repr(bfs_it)
    bfs = list(bfs_it)

    assert bfs == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "node9"]

    bfs_from_5 = list(traversal.bfs_traversal(g, "5"))
    assert bfs_from_5 == ["5", "0", "4", "6", "1", "2", "3", "7", "8", "node9"]

    dfs = list(traversal.dfs_traversal(g))
    assert dfs == ["0", "node9", "1", "2", "3", "4", "5", "6", "7", "8"]

    dfs_from_5 = list(traversal.dfs_traversal(g, "5"))
    assert dfs_from_5 == ["5", "6", "7", "8", "node9", "1", "2", "3", "4", "0"]

    lex_bfs = list(traversal.lexicographic_bfs_traversal(g))
    assert lex_bfs == ["0", "1", "2", "node9", "3", "8", "4", "7", "5", "6"]

    max_card = list(traversal.max_cardinality_traversal(g))
    assert max_card == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "node9"]

    degeneracy_ordering = list(traversal.degeneracy_ordering_traversal(g))
    assert degeneracy_ordering == ["1", "2", "3", "4", "5", "6", "0", "7", "8", "node9"]

    random_walk = list(traversal.random_walk_traversal(g, "0", False, 3, 17))
    assert random_walk == ["7", "0", "2"]

    closest_first = list(traversal.closest_first_traversal(g, "0"))
    assert closest_first == ["0", "1", "3", "5", "4", "node9", "8", "2", "7", "6"]


def test_anyhashableg_dag():
    # Create a dag to test top
    g1 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )
    g1.add_vertex(0)
    g1.add_vertex(1)
    g1.add_vertex(2)
    g1.add_vertex(3)

    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(3, 2)

    topo = list(traversal.topological_order_traversal(g1))
    assert topo == [0, 3, 1, 2]
