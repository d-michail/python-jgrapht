import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cuts as cuts


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1, weight=3)
    g.add_edge(0, 2)
    g.add_edge(0, 3, weight=2)
    g.add_edge(0, 4)
    g.add_edge(0, 5, weight=3)
    g.add_edge(0, 6)
    g.add_edge(0, 7, weight=100)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6, weight=2)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


def build_anyhashableg_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1, weight=3, edge=0)
    g.add_edge(0, 2, edge=1)
    g.add_edge(0, 3, weight=2, edge=2)
    g.add_edge(0, 4, edge=3)
    g.add_edge(0, 5, weight=3, edge=4)
    g.add_edge(0, 6, edge=5)
    g.add_edge(0, 7, weight=100, edge=6)
    g.add_edge(0, 8, edge=7)
    g.add_edge(0, 9, edge=8)

    g.add_edge(1, 2, edge=9)
    g.add_edge(2, 3, edge=10)
    g.add_edge(3, 4, edge=11)
    g.add_edge(4, 5, edge=12)
    g.add_edge(5, 6, weight=2, edge=13)
    g.add_edge(6, 7, edge=14)
    g.add_edge(7, 8, edge=15)
    g.add_edge(8, 9, edge=16)
    g.add_edge(9, 1, edge=17)

    return g


def test_mincut_stoer_wagner():
    g = build_graph()
    cut = cuts.mincut_stoer_wagner(g)
    assert cut.weight == 3.0
    assert cut.edges == set([8, 16, 17])
    assert cut.source_partition == set([9])


def test_anyhashableg_mincut_stoer_wagner():
    g = build_anyhashableg_graph()
    cut = cuts.mincut_stoer_wagner(g)
    assert cut.weight == 3.0
    assert cut.edges == set([8, 16, 17])
    assert cut.source_partition == set([9])


def test_oddmincutset_padberg_rao():
    g = build_graph()

    cut = cuts.oddmincutset_padberg_rao(g, {1, 3, 4, 6})

    assert cut.weight == 3.0
    assert cut.edges == set([3, 11, 12])
    assert cut.source_partition == set([4])

    cut = cuts.oddmincutset_padberg_rao(g, {1, 3, 4, 6}, use_tree_compression=True)

    assert cut.weight == 3.0
    assert cut.edges == set([3, 11, 12])
    assert cut.target_partition == set([4])

    with pytest.raises(ValueError):
        cuts.oddmincutset_padberg_rao(g, {1, 3, 4})


def test_anyhashableg_oddmincutset_padberg_rao():
    g = build_anyhashableg_graph()

    cut = cuts.oddmincutset_padberg_rao(g, {1, 3, 4, 6})

    assert cut.weight == 3.0
    assert cut.edges == set([3, 11, 12])
    assert cut.source_partition == set([4])

    cut = cuts.oddmincutset_padberg_rao(g, {1, 3, 4, 6}, use_tree_compression=True)

    assert cut.weight == 3.0
    assert cut.edges == set([3, 11, 12])
    assert cut.target_partition == set([4])

    with pytest.raises(ValueError):
        cuts.oddmincutset_padberg_rao(g, {1, 3, 4})


def test_min_st_cut():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)

    e01 = g.add_edge(0, 1, weight=20)
    e02 = g.add_edge(0, 2, weight=10)
    g.add_edge(1, 2, weight=30)
    g.add_edge(1, 3, weight=10)
    g.add_edge(2, 3, weight=20)

    cut = cuts.min_st_cut(g, 0, 3)

    assert cut.capacity == 30.0
    assert cut.edges == set([e01, e02])
    assert cut.source_partition == set([0])
    assert cut.target_partition == set([1, 2, 3])


def test_anyhashableg_min_st_cut():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)

    e01 = g.add_edge(0, 1, weight=20)
    e02 = g.add_edge(0, 2, weight=10)
    g.add_edge(1, 2, weight=30)
    g.add_edge(1, 3, weight=10)
    g.add_edge(2, 3, weight=20)

    cut = cuts.min_st_cut(g, 0, 3)

    assert cut.capacity == 30.0
    assert cut.edges == set([e01, e02])
    assert cut.source_partition == set([0])
    assert cut.target_partition == set([1, 2, 3])