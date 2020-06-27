import pytest

from jgrapht import create_graph
import jgrapht.algorithms.clustering as clustering


def test_k_spanning_tree():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
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


def test_label_propagation():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
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


def test_anyhashableg_k_spanning_tree():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge(str(0), str(1))
    g.add_edge(str(1), str(2))
    g.add_edge(str(2), str(0))
    g.add_edge(str(3), str(4))
    g.add_edge(str(4), str(5))
    g.add_edge(str(5), str(3))
    g.add_edge(str(2), str(3), weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set(["0", "1", "2"])
    assert set(c.ith_cluster(1)) == set(["3", "4", "5"])


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

