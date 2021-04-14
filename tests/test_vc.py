import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.vertexcover as vc


def build_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    for i in range(0, 10):
        g.add_vertex(i)
    for i in range(1, 10):
        g.add_edge(0, i)

    vertex_weights = dict()
    vertex_weights[0] = 1000.0
    for i in range(1, 10):
        vertex_weights[i] = 1.0

    return g, vertex_weights


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_greedy(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.greedy(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_greedy_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.greedy(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_clarkson(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.clarkson(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_clarkson_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.clarkson(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_edgebased(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.edgebased(g)
    assert vc_weight == 2.0
    assert set(vc_vertices) == set([0, 1])



def build_property_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        edge_supplier=IntegerSupplier()
    )

    for i in range(0, 10):
        g.add_vertex(str(i))
    for i in range(1, 10):
        g.add_edge(str(0), str(i))

    vertex_weights = dict()
    vertex_weights["0"] = 1000.0
    for i in range(1, 10):
        vertex_weights[str(i)] = 1.0

    print(g)
    print(vertex_weights)

    return g, vertex_weights



def test_anyhashableg_greedy_with_weights():
    g, vertex_weights = build_property_graph()
    vc_weight, vc_vertices = vc.greedy(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_baryehuda_even(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.baryehuda_even(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_baryehuda_even_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.baryehuda_even(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_exact(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.exact(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_exact_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.exact(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])
