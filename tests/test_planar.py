import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier, create_edge_supplier, create_vertex_supplier

import jgrapht.algorithms.planar as planar
import jgrapht.generators as generators


def build_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 0)
    g.add_edge(2, 0)

    return g


def build_anyhashableg_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex("2")
    g.add_vertex(3)
    g.add_vertex(4)

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, "2", edge=1)
    g.add_edge("2", 3, edge=2)
    g.add_edge(3, 4, edge="3")
    g.add_edge(4, 0, edge=4)
    g.add_edge("2", 0, edge="5")

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_planar(backend):
    g = build_graph(backend)

    res, aux = planar.is_planar(g)

    assert res == True
    assert aux.edges_around(0) == list([5, 0, 4])


def test_anyhashableg_planar():
    g = build_anyhashableg_graph()

    res, aux = planar.is_planar(g)

    assert res == True
    assert aux.edges_around(0) == list(["5", 0, 4])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_non_planar(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),        
    )
    generators.complete_graph(g, 5)

    res, aux = planar.is_planar(g)

    assert res == False
    assert aux.vertices == set([0, 1, 2, 3, 4])


def test_anyhashableg_non_planar():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )
    generators.complete_graph(g, 5)

    g.add_vertex("extra")

    res, kuratowski = planar.is_planar(g)

    assert res == False
    assert kuratowski.vertices == set(g.vertices).difference({"extra"})
