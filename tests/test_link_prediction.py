import pytest

from jgrapht import create_graph, GraphBackend

from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.linkprediction as linkprediction
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

    g.add_edge(1, 6)

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_adamic_adar(backend):
    g = build_graph(backend)

    scores = [linkprediction.adamic_adar_index(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([1.1764671337579005, 0.45511961331341866])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_common_neighbors(backend):
    g = build_graph(backend)

    scores = [linkprediction.common_neighbors(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([2.0, 1.0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_hub_depressed_index(backend):
    g = build_graph(backend)

    scores = [linkprediction.hub_depressed_index(g, u, v) for u, v in [(1, 7), (1, 6)]]
    print(scores)
    assert scores == pytest.approx([0.5, 0.25])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_hub_promoted_index(backend):
    g = build_graph(backend)

    scores = [linkprediction.hub_promoted_index(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([0.6666666666666666, 0.25])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_jaccard_coefficient(backend):
    g = build_graph(backend)

    scores = [linkprediction.jaccard_coefficient(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([0.4, 0.14285714285714285])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_leicht_holme_newman_index(backend):
    g = build_graph(backend)

    scores = [
        linkprediction.leicht_holme_newman_index(g, u, v) for u, v in [(1, 7), (1, 6)]
    ]
    assert scores == pytest.approx([1.5, 1.0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_preferential_attachment(backend):
    g = build_graph(backend)

    scores = [
        linkprediction.preferential_attachment(g, u, v) for u, v in [(1, 7), (1, 6)]
    ]
    assert scores == pytest.approx([12.0, 16.0])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_resource_allocation_index(backend):
    g = build_graph(backend)

    scores = [
        linkprediction.resource_allocation_index(g, u, v) for u, v in [(1, 7), (1, 6)]
    ]
    assert scores == pytest.approx([0.3611111111111111, 0.1111111111111111])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_salton_index(backend):
    g = build_graph(backend)

    scores = [linkprediction.salton_index(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([0.5773502691896258, 0.25])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_sorensen_index(backend):
    g = build_graph(backend)

    scores = [linkprediction.sorensen_index(g, u, v) for u, v in [(1, 7), (1, 6)]]
    assert scores == pytest.approx([0.5714285714285714, 0.25])
