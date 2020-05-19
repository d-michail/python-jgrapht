import pytest

from jgrapht import create_graph
import jgrapht.algorithms.clustering as clustering

def test_k_spanning_tree():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 6):
        g.add_vertex(i)

    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 0)

    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 3)

    g.create_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.k_spanning_tree(g, k=2)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0,1,2])
    assert set(c.ith_cluster(1)) == set([3,4,5])

def test_label_propagation():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for i in range(0, 6):
        g.add_vertex(i)

    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 0)

    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 3)

    g.create_edge(2, 3, weight=100.0)

    assert len(g.edges) == 7

    c = clustering.label_propagation(g, seed=17)

    assert c.number_of_clusters() == 2
    assert set(c.ith_cluster(0)) == set([0,1,2])
    assert set(c.ith_cluster(1)) == set([3,4,5])
