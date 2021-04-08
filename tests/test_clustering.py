import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier

import jgrapht.algorithms.clustering as clustering


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_k_spanning_tree(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    repr(c)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0, 1, 2])
    assert set(c.ith_cluster(1)) == set([3, 4, 5])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_label_propagation(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.label_propagation(g, seed=17)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0, 1, 2])
    assert set(c.ith_cluster(1)) == set([3, 4, 5])

    # test with auto seed
    c = clustering.label_propagation(g)
    assert c.number_of_clusters() > 0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_k_spanning_tree(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    v = [g.add_vertex(str(i)) for i in range(0, 6)]

    g.add_edge(v[0], v[1])
    g.add_edge(v[1], v[2])
    g.add_edge(v[2], v[0])
    g.add_edge(v[3], v[4])
    g.add_edge(v[4], v[5])
    g.add_edge(v[5], v[3])
    g.add_edge(v[2], v[3], weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([v[0], v[1], v[2]])
    assert set(c.ith_cluster(1)) == set([v[3], v[4], v[5]])


def test_anyhashableg_label_propagation():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.label_propagation(g, seed=17)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0, 1, 2])
    assert set(c.ith_cluster(1)) == set([3, 4, 5])


def test_k_spanning_tree():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=GraphBackend.REF_GRAPH,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    repr(c)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0, 1, 2])
    assert set(c.ith_cluster(1)) == set([3, 4, 5])