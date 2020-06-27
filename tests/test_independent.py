import pytest

from jgrapht import create_graph

import jgrapht.algorithms.independent as independent


def test_chordal():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 0)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 5)
    g.add_edge(1, 3)

    ind = independent.chordal_max_independent_set(g)

    assert ind == {2, 4}


def test_anyhashableg_chordal():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 0)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 5)
    g.add_edge(1, 3)

    ind = independent.chordal_max_independent_set(g)

    assert ind == {2, 4}