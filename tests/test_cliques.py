import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.cliques as cliques


def build_graph(backend=GraphBackend.INT_GRAPH):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)

    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    g.add_edge(2, 3)

    return g


def build_anyhashableg_graph(backend=GraphBackend.ANY_HASHABLE_GRAPH):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
    )

    v0 = g.add_vertex(str(0))
    v1 = g.add_vertex(str(1))
    v2 = g.add_vertex(str(2))
    v3 = g.add_vertex(str(3))
    v4 = g.add_vertex(str(4))
    v5 = g.add_vertex(str(5))

    g.add_edge(v0, v1)
    g.add_edge(v0, v2)
    g.add_edge(v1, v2)

    g.add_edge(v3, v4)
    g.add_edge(v3, v5)
    g.add_edge(v4, v5)

    g.add_edge(v2, v3)

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_bron_with_degeneracy(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch_with_degeneracy_ordering(g)

    result = set([frozenset(c) for c in clique_it])

    assert result == {frozenset({3, 4, 5}), frozenset({2, 3}), frozenset({0, 1, 2})}


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_bron_with_pivot(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch_with_pivot(g)

    result = set([frozenset(c) for c in clique_it])
    assert result == {frozenset({3, 4, 5}), frozenset({2, 3}), frozenset({0, 1, 2})}


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
    ],
)
def test_bron(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch(g)

    result = set([frozenset(c) for c in clique_it])
    assert result == {frozenset({3, 4, 5}), frozenset({2, 3}), frozenset({0, 1, 2})}


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REFCOUNT_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
    ],
)
def test_anyhashableg_bron(backend):
    g = build_anyhashableg_graph(backend)

    clique_it = cliques.bron_kerbosch(g)

    result = set([frozenset(c) for c in clique_it])
    assert result == {
        frozenset({str(3), str(4), str(5)}),
        frozenset({str(2), str(3)}),
        frozenset({str(0), str(1), str(2)}),
    }


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REFCOUNT_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
    ],
)
def test_anyhashableg_bron_with_pivot(backend):
    g = build_anyhashableg_graph(backend)

    clique_it = cliques.bron_kerbosch_with_pivot(g)

    result = set([frozenset(c) for c in clique_it])
    assert result == {
        frozenset({str(3), str(4), str(5)}),
        frozenset({str(2), str(3)}),
        frozenset({str(0), str(1), str(2)}),
    }


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REFCOUNT_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
    ],
)
def test_anyhashableg_bron_with_degeneracy(backend):
    g = build_anyhashableg_graph(backend)

    clique_it = cliques.bron_kerbosch_with_degeneracy_ordering(g)

    result = set([frozenset(c) for c in clique_it])
    assert result == {
        frozenset({str(3), str(4), str(5)}),
        frozenset({str(2), str(3)}),
        frozenset({str(0), str(1), str(2)}),
    }


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

    clique = cliques.chordal_max_clique(g)

    assert clique == {0, 1, 3}



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

    clique = cliques.chordal_max_clique(g)

    assert clique == {0, 1, 3}
