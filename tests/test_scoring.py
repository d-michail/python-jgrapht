import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.scoring as scoring


def build_graph(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
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


def build_anyhashableg_graph(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )

    g.add_vertex("0")
    for i in range(1, 10):
        g.add_vertex(i)

    g.add_edge("0", 1)
    g.add_edge("0", 2)
    g.add_edge("0", 3)
    g.add_edge("0", 4)
    g.add_edge("0", 5)
    g.add_edge("0", 6)
    g.add_edge("0", 7)
    g.add_edge("0", 8)
    g.add_edge("0", 9)

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
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_pagerank(backend):
    g = build_graph(backend)
    scores = scoring.pagerank(g)
    result = [scores[v] for v in g.vertices]
    expected = [
        0.2324869499599194,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
    ]
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_harmonic_centrality(backend):
    g = build_graph(backend)
    scores = scoring.harmonic_centrality(g)
    result = [scores[v] for v in g.vertices]
    expected = [
        1.0,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
    ]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_closeness_centrality(backend):
    g = build_graph(backend)
    scores = scoring.closeness_centrality(g)
    result = [scores[v] for v in g.vertices]
    expected = [1.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_betweenness_centrality(backend):
    g = build_graph(backend)
    scores = scoring.betweenness_centrality(g)
    result = [scores[v] for v in g.vertices]
    expected = [22.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_alpha_centrality(backend):
    g = build_graph(backend)
    scores = scoring.alpha_centrality(g)
    result = [scores[v] for v in g.vertices]
    expected = [
        1.09284015241,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
        1.03155950011,
    ]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_coreness(backend):
    g = build_graph(backend)
    degeneracy, scores = scoring.coreness(g)
    assert degeneracy == 3
    result = [scores[v] for v in g.vertices]
    expected = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_clustering_coefficient(backend):
    g = build_graph(backend)
    global_cc, avg_cc, local_cc = scoring.clustering_coefficient(g)
    assert global_cc == 0.42857142857142855
    assert avg_cc == 0.6250000000000001
    result = [local_cc[v] for v in g.vertices]
    expected = [
        0.25,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
    ]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_anyhashableg_pagerank(backend):
    g = build_anyhashableg_graph(backend)
    scores = scoring.pagerank(g)
    result = [scores[v] for v in g.vertices]
    expected = [
        0.2324869499599194,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
        0.08527922778223115,
    ]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_anyhashableg_clustering_coefficient(backend):
    g = build_anyhashableg_graph(backend)
    global_cc, avg_cc, local_cc = scoring.clustering_coefficient(g)
    assert global_cc == 0.42857142857142855
    assert avg_cc == pytest.approx(0.6250000000000001)
    result = [local_cc[v] for v in g.vertices]
    expected = [
        0.25,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666,
    ]
    assert result == expected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_anyhashableg_coreness(backend):
    g = build_anyhashableg_graph(backend)
    degeneracy, scores = scoring.coreness(g)
    assert degeneracy == 3
    result = [scores[v] for v in g.vertices]
    expected = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    assert result == expected