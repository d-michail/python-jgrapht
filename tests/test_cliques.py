import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cliques as cliques

def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=False)

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

def test_bron_with_degeneracy():
    g = build_graph()

    clique_it = cliques.bron_kerbosch_with_degeneracy_ordering(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)

def test_bron_with_pivot():
    g = build_graph()

    clique_it = cliques.bron_kerbosch_with_pivot(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)

def test_bron():
    g = build_graph()

    clique_it = cliques.bron_kerbosch(g)

    assert set(next(clique_it)) == set([0, 1, 2])
    assert set(next(clique_it)) == set([2, 3])
    assert set(next(clique_it)) == set([3, 4, 5])

    with pytest.raises(StopIteration):
        next(clique_it)