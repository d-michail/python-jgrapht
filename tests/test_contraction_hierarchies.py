import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.shortestpaths as sp
import math


def get_graph(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )

    for i in range(0, 8):
        g.add_vertex(i)

    g.add_edge(0, 1, edge=0, weight=3.0)
    g.add_edge(1, 3, edge=1, weight=100.0)
    g.add_edge(0, 2, edge=2, weight=40.0)
    g.add_edge(2, 4, edge=3, weight=20.0)
    g.add_edge(3, 5, edge=4, weight=2.0)
    g.add_edge(4, 5, edge=5, weight=2.0)
    g.add_edge(5, 0, edge=6, weight=13.0)
    g.add_edge(0, 5, edge=7, weight=1000.0)
    g.add_edge(5, 6, edge=8, weight=12.0)
    g.add_edge(5, 7, edge=9, weight=20.0)
    g.add_edge(6, 7, edge=10, weight=3.0)
    g.add_edge(4, 7, edge=11, weight=200.0)

    return g


def get_anyhashableg_graph(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )

    for i in range(0, 8):
        g.add_vertex(i)

    g.add_edge(0, 1, weight=3.0, edge=0)
    g.add_edge(1, 3, weight=100.0, edge=1)
    g.add_edge(0, 2, weight=40.0, edge="2")
    g.add_edge(2, 4, weight=20.0, edge=3)
    g.add_edge(3, 5, weight=2.0, edge=4)
    g.add_edge(4, 5, weight=2.0, edge=5)
    g.add_edge(5, 0, weight=13.0, edge=6)
    g.add_edge(0, 5, weight=1000.0, edge=7)
    g.add_edge(5, 6, weight=12.0, edge=8)
    g.add_edge(5, 7, weight=20.0, edge=9)
    g.add_edge(6, 7, weight=3.0, edge=10)
    g.add_edge(4, 7, weight=200.0, edge=11)

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_ch_dijkstra(backend):
    g = get_graph(backend)

    ch = sp.precompute_contraction_hierarchies(g, parallelism=1, seed=31)

    p1 = sp.contraction_hierarchies_dijkstra(g, 0, 7, ch=ch)

    assert 77 == p1.weight
    assert [2, 3, 5, 8, 10] == p1.edges
    assert 0 == p1.start_vertex
    assert 7 == p1.end_vertex

    p2 = sp.contraction_hierarchies_dijkstra(g, 1, 6, ch=ch)

    assert 114 == p2.weight
    assert [1, 4, 8] == p2.edges
    assert 1 == p2.start_vertex
    assert 6 == p2.end_vertex


@pytest.mark.parametrize(
    "backend", [GraphBackend.ANY_HASHABLE_GRAPH, GraphBackend.REFCOUNT_GRAPH]
)
def test_ch_dijkstra_anyhashable(backend):
    g = get_anyhashableg_graph(backend)

    ch = sp.precompute_contraction_hierarchies(g, parallelism=1, seed=31)

    p1 = sp.contraction_hierarchies_dijkstra(g, 0, 7, ch=ch)

    assert 77 == p1.weight
    assert ["2", 3, 5, 8, 10] == p1.edges
    assert 0 == p1.start_vertex
    assert 7 == p1.end_vertex

    p2 = sp.contraction_hierarchies_dijkstra(g, 1, 6, ch=ch)

    assert 114 == p2.weight
    assert [1, 4, 8] == p2.edges
    assert 1 == p2.start_vertex
    assert 6 == p2.end_vertex


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_ch_many_to_many(backend):
    g = get_graph(backend)

    ch = sp.precompute_contraction_hierarchies(g, parallelism=1, seed=31)

    mm = sp.contraction_hierarchies_many_to_many(g, {0, 1}, {6, 7}, ch=ch)

    p1 = mm.get_path(0, 7)

    assert 77 == p1.weight
    assert [2, 3, 5, 8, 10] == p1.edges
    assert 0 == p1.start_vertex
    assert 7 == p1.end_vertex

    p2 = mm.get_path(1, 6)

    assert 114 == p2.weight
    assert [1, 4, 8] == p2.edges
    assert 1 == p2.start_vertex
    assert 6 == p2.end_vertex

    with pytest.raises(ValueError):
        mm.get_path(2, 6)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_anyhashable_ch_many_to_many(backend):
    g = get_anyhashableg_graph(backend)

    ch = sp.precompute_contraction_hierarchies(g, parallelism=1, seed=31)

    mm = sp.contraction_hierarchies_many_to_many(g, {0, 1}, {6, 7}, ch=ch)

    p1 = mm.get_path(0, 7)

    assert 77 == p1.weight
    assert ["2", 3, 5, 8, 10] == p1.edges
    assert 0 == p1.start_vertex
    assert 7 == p1.end_vertex

    p2 = mm.get_path(1, 6)

    assert 114 == p2.weight
    assert [1, 4, 8] == p2.edges
    assert 1 == p2.start_vertex
    assert 6 == p2.end_vertex

    with pytest.raises(ValueError):
        mm.get_path(2, 6)
