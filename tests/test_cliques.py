import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier

import jgrapht.algorithms.cliques as cliques


def build_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bron_with_degeneracy(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch_with_degeneracy_ordering(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bron_with_pivot(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch_with_pivot(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bron(backend):
    g = build_graph(backend)

    clique_it = cliques.bron_kerbosch(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_chordal(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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

