import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.generators as generators
from jgrapht.utils import create_vertex_supplier, create_edge_supplier


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_barabasi_albert(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.barabasi_albert(g, 10, 5, 100)
    assert len(g.vertices) == 100


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_barabasi_albert_forest(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.barabasi_albert_forest(g, 10, 100)
    assert len(g.vertices) == 100


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_complete(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.complete_graph(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_complete_bipartite(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.complete_bipartite_graph(g, 10, 10)
    assert len(g.vertices) == 20


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_empty(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.empty_graph(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_gnm_random(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.gnm_random_graph(g, 10, 30)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_gnp_random(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.gnp_random_graph(g, 10, 0.2)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_ring(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.ring_graph(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_scalefree(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.scalefree_graph(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_watts_strogatz(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.watts_strogatz_graph(g, 10, 2, 0.1)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_kleinberg_smallworld(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.kleinberg_smallworld_graph(g, 10, 2, 2, 1)
    assert len(g.vertices) == 100


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_complement(backend):
    g_source = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    g_source.add_vertex(0)
    g_source.add_vertex(1)
    g_source.add_vertex(2)
    g_source.add_edge(0, 1, edge=0)
    g_source.add_edge(0, 2, edge=1)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        vertex_supplier=create_vertex_supplier(type="int"),
        edge_supplier=create_edge_supplier(type="int"),
        backend=backend,
    )

    generators.complement_graph(g, g_source)

    assert g.vertices == {0, 1, 2}
    assert g.edges == {0}
    assert g.edge_tuple(0) == (1, 2, 1.0)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_generalized_petersen(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.generalized_petersen(g, 10, 4)
    assert len(g.vertices) == 20


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_grid(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.grid(g, 10, 4)
    assert len(g.vertices) == 40


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_hypercube(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.hypercube(g, 4)
    assert len(g.vertices) == 16


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_linear(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.linear(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_random_regular(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.random_regular(g, 10, 3, 17)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_random_regular_no_seed(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.random_regular(g, 10, 3)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_star(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.star(g, 10)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_wheel(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.wheel(g, 10, False)
    assert len(g.vertices) == 10


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_windmill(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    generators.windmill(g, 3, 3, dutch=False)
    assert len(g.vertices) == 7


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_linearized_chord_diagram(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        backend=backend,
    )
    generators.linearized_chord_diagram(g, 100, 3, 17)
    assert len(g.vertices) == 100

    # test that error is raised if the graph does not support self loops and multiple edges
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )
    with pytest.raises(ValueError):
        generators.linearized_chord_diagram(g, 100, 3, 17)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
        GraphBackend.LONG_REF_GRAPH,
    ],
)
def test_linearized_chord_diagram_no_seed(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        backend=backend,
    )
    generators.linearized_chord_diagram(g, 100, 3)
    assert len(g.vertices) == 100
