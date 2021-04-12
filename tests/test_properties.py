import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier, create_edge_supplier, create_vertex_supplier
import jgrapht.properties as properties


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_empty_graph(backend):
    g = create_graph(
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )
    assert properties.is_empty_graph(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_simple(backend):
    g = create_graph(
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_simple(g)

    g.add_edge(1, 1)

    assert not properties.is_simple(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_has_self_loops(backend):
    g = create_graph(
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.has_selfloops(g)

    g.add_edge(1, 1)

    assert properties.has_selfloops(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_has_multiple_edges(backend):
    g = create_graph(
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.has_multipleedges(g)

    g.add_edge(1, 1)

    assert not properties.has_multipleedges(g)

    g.add_edge(1, 2)

    assert properties.has_multipleedges(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_complete(backend):
    g = create_graph(
        directed=True,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)
    g.add_edge(2, 1)

    assert properties.is_complete(g)

    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_complete(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_weakly_connected(backend):
    g = create_graph(
        directed=True,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_weakly_connected(g)

    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_weakly_connected(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_strongly_connected(backend):
    g = create_graph(
        directed=True,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.is_strongly_connected(g)

    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_strongly_connected(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_tree(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_tree(g)

    g.add_edge(3, 1)

    assert not properties.is_tree(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_forest(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_forest(g)

    g.add_edge(3, 1)

    assert not properties.is_forest(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_overfull(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert not properties.is_overfull(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_split(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_split(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_bipartite(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)

    assert properties.is_bipartite(g)

    g.add_edge(3, 1)

    assert not properties.is_bipartite(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_cubic(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_cubic(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_eulerian(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_eulerian(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_chordal(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_chordal(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_weakly_chordal(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_weakly_chordal(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_triangle_free(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_trianglefree(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_perfect(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_perfect(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_planar(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_planar(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_has_ore(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.has_ore(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_kuratowski_subdivision(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_kuratowski_subdivision(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_k33_subdivision(backend):
    g = create_graph(
        directed=False,
        allowing_multiple_edges=True,
        allowing_self_loops=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_k33_subdivision(g)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_k5_subdivision(backend):
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True,         backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_k5_subdivision(g)
