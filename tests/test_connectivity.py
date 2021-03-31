import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.connectivity as connectivity


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_weakly(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    g.add_vertices_from([0, 1, 2, 3])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert is_connected
    component1 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3])

    g.add_vertices_from([4, 5])
    g.add_edge(4, 5)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert not is_connected
    component1 = next(components)
    component2 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3])
    assert component2 == set([4, 5])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_weakly_directed(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
    )

    g.add_vertices_from([0, 1, 2, 3])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert is_connected
    component1 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3])

    g.add_vertices_from([4, 5])
    g.add_edge(4, 5)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert not is_connected
    component1 = next(components)
    component2 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3])
    assert component2 == set([4, 5])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_strongly_kosaraju(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(2, 3)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    is_connected, components = connectivity.is_strongly_connected_kosaraju(g)
    assert not is_connected
    component1 = next(components)
    component2 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2])
    assert component2 == set([3, 4, 5])

    g.add_edge(3, 2)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert is_connected
    component1 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3, 4, 5])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_strongly_gabow(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(2, 3)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    is_connected, components = connectivity.is_strongly_connected_gabow(g)
    assert not is_connected
    component1 = next(components)
    component2 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([3, 4, 5])
    assert component2 == set([0, 1, 2])

    g.add_edge(3, 2)

    is_connected, components = connectivity.is_weakly_connected(g)
    assert is_connected
    component1 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set([0, 1, 2, 3, 4, 5])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_is_connected(backend):
    # directed
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    g.add_vertices_from([0, 1])
    g.add_edge(0, 1)

    is_connected, components = connectivity.is_connected(g)
    assert not is_connected

    g.add_edge(1, 0)
    is_connected, components = connectivity.is_connected(g)
    assert is_connected

    # undirected
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g.add_vertices_from([0, 1])
    g.add_edge(0, 1)
    is_connected, components = connectivity.is_connected(g)
    assert is_connected


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_strongly_gabow(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    g.add_vertices_from(["0", "1", "2", "3", "4", "5"])
    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "0")
    g.add_edge("2", "3")
    g.add_edge("3", "4")
    g.add_edge("4", "5")
    g.add_edge("5", "3")

    is_connected, components = connectivity.is_strongly_connected_gabow(g)
    assert not is_connected
    component1 = next(components)
    component2 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set(["3", "4", "5"])
    assert component2 == set(["0", "1", "2"])

    g.add_edge("3", "2")

    is_connected, components = connectivity.is_weakly_connected(g)
    assert is_connected
    component1 = next(components)
    with pytest.raises(StopIteration):
        next(components)

    assert component1 == set(["0", "1", "2", "3", "4", "5"])

