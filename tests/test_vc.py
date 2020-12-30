import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.vertexcover as vc


def build_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
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


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_greedy(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.greedy(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_greedy_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.greedy(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_clarkson(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.clarkson(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_clarkson_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.clarkson(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_edgebased(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.edgebased(g)
    assert vc_weight == 2.0
    assert set(vc_vertices) == set([0, 1])


def build_property_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_vertex("2")
    g.add_vertex("3")
    g.add_vertex("4")
    g.add_vertex("5")
    g.add_vertex("6")
    g.add_vertex("7")
    g.add_vertex("8")
    g.add_vertex("9")

    g.add_edge("0", "1")
    g.add_edge("0", "2")
    g.add_edge("0", "3")        
    g.add_edge("0", "4")
    g.add_edge("0", "5")
    g.add_edge("0", "6")
    g.add_edge("0", "7")
    g.add_edge("0", "8")
    g.add_edge("0", "9")

    vertex_weights = dict()
    vertex_weights["0"] = 1000.0
    
    vertex_weights["1"] = 1.0
    vertex_weights["2"] = 1.0
    vertex_weights["3"] = 1.0
    vertex_weights["4"] = 1.0
    vertex_weights["5"] = 1.0
    vertex_weights["6"] = 1.0
    vertex_weights["7"] = 1.0
    vertex_weights["8"] = 1.0
    vertex_weights["9"] = 1.0

    return g, vertex_weights


@pytest.mark.parametrize("backend", [GraphBackend.LONG_REF_GRAPH])
def test_anyhashableg_greedy_with_weights(backend):
    g, vertex_weights = build_property_graph(backend)
    vc_weight, vc_vertices = vc.greedy(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_baryehuda_even(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.baryehuda_even(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_baryehuda_even_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.baryehuda_even(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_exact(backend):
    g, _ = build_graph(backend)
    vc_weight, vc_vertices = vc.exact(g)
    assert vc_weight == 1.0
    assert set(vc_vertices) == set([0])


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.LONG_REF_GRAPH])
def test_exact_with_weights(backend):
    g, vertex_weights = build_graph(backend)
    vc_weight, vc_vertices = vc.exact(g, vertex_weights=vertex_weights)
    assert vc_weight == 9.0
    assert set(vc_vertices) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])
