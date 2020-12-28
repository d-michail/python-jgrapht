import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.spanning as spanning


def build_graph(backend):

    next_edge = 0

    def edge_supplier():
        nonlocal next_edge
        res = next_edge
        next_edge += 1
        return res

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=edge_supplier,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(0, 6)
    g.add_edge(0, 7)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.REFCOUNT_GRAPH,
        GraphBackend.ANY_HASHABLE_GRAPH,
    ],
)
def test_greedy_multiplicative(backend):
    g = build_graph(backend)
    weight, edges = spanning.multiplicative_greedy(g, 3)
    assert weight == 9.0
    expected = set([0, 1, 2, 3, 4, 5, 6, 7, 8])
    solution = set(edges)
    assert expected == solution
