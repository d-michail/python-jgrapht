import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.clustering as clustering


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH])
def test_k_spanning_tree(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
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


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH])
def test_label_propagation(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
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
        GraphBackend.ANY_HASHABLE_REFCOUNT_LONG_GRAPH,
        GraphBackend.ANY_HASHABLE_WRAPPER_INT_GRAPH,
    ],
)
def test_anyhashableg_k_spanning_tree(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    v0 = g.add_vertex(str(0))
    v1 = g.add_vertex(str(1))
    v2 = g.add_vertex(str(2))
    v3 = g.add_vertex(str(3))
    v4 = g.add_vertex(str(4))
    v5 = g.add_vertex(str(5))

    g.add_edge(v0, v1)
    g.add_edge(v1, v2)
    g.add_edge(v2, v0)
    g.add_edge(v3, v4)
    g.add_edge(v4, v5)
    g.add_edge(v5, v3)
    g.add_edge(v2, v3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set(["0", "1", "2"])
    assert set(c.ith_cluster(1)) == set(["3", "4", "5"])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_REFCOUNT_LONG_GRAPH,
        GraphBackend.ANY_HASHABLE_WRAPPER_INT_GRAPH,
    ],
)
def test_anyhashableg_label_propagation(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    v0 = g.add_vertex(str(0))
    v1 = g.add_vertex(str(1))
    v2 = g.add_vertex(str(2))
    v3 = g.add_vertex(str(3))
    v4 = g.add_vertex(str(4))
    v5 = g.add_vertex(str(5))

    g.add_edge(v0, v1)
    g.add_edge(v1, v2)
    g.add_edge(v2, v0)
    g.add_edge(v3, v4)
    g.add_edge(v4, v5)
    g.add_edge(v5, v3)
    g.add_edge(v2, v3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.label_propagation(g, seed=17)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set(["0", "1", "2"])
    assert set(c.ith_cluster(1)) == set(["3", "4", "5"])
