import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.isomorphism as iso


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_iso(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, 6, 7, 8])

    g2.add_edge(5, 6, edge=0)
    g2.add_edge(6, 7, edge=1)
    g2.add_edge(7, 8, edge=2)
    g2.add_edge(8, 5, edge=3)

    it = iso.vf2(g1, g2)

    repr(it)

    assert it is not None

    gm = next(it)
    repr(gm)
    assert gm.vertices_correspondence() == {0: 5, 1: 6, 2: 7, 3: 8}
    assert gm.vertices_correspondence(forward=False) == {5: 0, 6: 1, 7: 2, 8: 3}
    assert gm.edges_correspondence() == {0: 0, 1: 1, 2: 2, 3: 3}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: 8, 2: 7, 3: 6}
    assert gm.edges_correspondence() == {0: 3, 1: 2, 2: 1, 3: 0}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 5, 2: 8, 3: 7}
    assert gm.edges_correspondence() == {0: 0, 1: 3, 2: 2, 3: 1}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 8, 1: 5, 2: 6, 3: 7}
    assert gm.edges_correspondence() == {0: 3, 1: 0, 2: 1, 3: 2}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: 6, 2: 5, 3: 8}
    assert gm.edges_correspondence() == {0: 1, 1: 0, 2: 3, 3: 2}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: 8, 2: 5, 3: 6}
    assert gm.edges_correspondence() == {0: 2, 1: 3, 2: 0, 3: 1}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 7, 2: 8, 3: 5}
    assert gm.edges_correspondence() == {0: 1, 1: 2, 2: 3, 3: 0}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 8, 1: 7, 2: 6, 3: 5}
    assert gm.edges_correspondence() == {0: 2, 1: 1, 2: 0, 3: 3}


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_iso_no(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, 6, 7])

    g2.add_edge(5, 6, edge=0)
    g2.add_edge(6, 7, edge=1)
    g2.add_edge(7, 5, edge=2)

    it = iso.vf2(g1, g2)

    assert it is None


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_iso_induced_subgraph(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, 6, 7])

    g2.add_edge(5, 6, edge=0)
    g2.add_edge(6, 7, edge=1)

    it = iso.vf2_subgraph(g1, g2)

    assert it is not None

    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: 6, 2: 7, 3: None}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: None, 2: 7, 3: 6}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 5, 2: None, 3: 7}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: None, 1: 5, 2: 6, 3: 7}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: 6, 2: 5, 3: None}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: None, 2: 5, 3: 6}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 7, 2: None, 3: 5}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: None, 1: 7, 2: 6, 3: 5}


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_iso_not_induced_subgraph(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 0)
    g1.add_edge(0, 2)
    g1.add_edge(1, 3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, 6, 7])

    g2.add_edge(5, 6)
    g2.add_edge(6, 7)

    it = iso.vf2_subgraph(g1, g2)

    assert it is None


@pytest.mark.parametrize("backend", [GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_anyhashableg_iso(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, "6", 7, 8])

    g2.add_edge(5, "6", edge=0)
    g2.add_edge("6", 7, edge=1)
    g2.add_edge(7, 8, edge="e2")
    g2.add_edge(8, 5, edge=3)

    it = iso.vf2(g1, g2)

    assert it is not None

    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: "6", 2: 7, 3: 8}
    assert gm.vertices_correspondence(forward=False) == {5: 0, "6": 1, 7: 2, 8: 3}
    assert gm.edges_correspondence() == {0: 0, 1: 1, 2: "e2", 3: 3}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: 8, 2: 7, 3: "6"}
    assert gm.edges_correspondence() == {0: 3, 1: "e2", 2: 1, 3: 0}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: "6", 1: 5, 2: 8, 3: 7}
    assert gm.edges_correspondence() == {0: 0, 1: 3, 2: "e2", 3: 1}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 8, 1: 5, 2: "6", 3: 7}
    assert gm.edges_correspondence() == {0: 3, 1: 0, 2: 1, 3: "e2"}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: "6", 2: 5, 3: 8}
    assert gm.edges_correspondence() == {0: 1, 1: 0, 2: 3, 3: "e2"}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: 8, 2: 5, 3: "6"}
    assert gm.edges_correspondence() == {0: "e2", 1: 3, 2: 0, 3: 1}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: "6", 1: 7, 2: 8, 3: 5}
    assert gm.edges_correspondence() == {0: 1, 1: "e2", 2: 3, 3: 0}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 8, 1: 7, 2: "6", 3: 5}
    assert gm.edges_correspondence() == {0: "e2", 1: 1, 2: 0, 3: 3}


@pytest.mark.parametrize("backend", [GraphBackend.REFCOUNT_GRAPH, GraphBackend.ANY_HASHABLE_GRAPH])
def test_anyhashableg_iso_induced_subgraph(backend):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    g2.add_vertices_from([5, 6, 7])

    g2.add_edge(5, 6, edge=0)
    g2.add_edge(6, 7, edge=1)

    it = iso.vf2_subgraph(g1, g2)

    assert it is not None

    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: 6, 2: 7, 3: None}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 5, 1: None, 2: 7, 3: 6}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 5, 2: None, 3: 7}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: None, 1: 5, 2: 6, 3: 7}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: 6, 2: 5, 3: None}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 7, 1: None, 2: 5, 3: 6}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: 6, 1: 7, 2: None, 3: 5}
    gm = next(it)
    assert gm.vertices_correspondence() == {0: None, 1: 7, 2: 6, 3: 5}


@pytest.mark.parametrize("backend1", [GraphBackend.REFCOUNT_GRAPH])
@pytest.mark.parametrize("backend2", [GraphBackend.ANY_HASHABLE_GRAPH])
def test_different_backends_error(backend1, backend2):
    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend1
    )

    g1.add_vertices_from([0, 1, 2, 3])

    g1.add_edge(0, 1, edge=0)
    g1.add_edge(1, 2, edge=1)
    g1.add_edge(2, 3, edge=2)
    g1.add_edge(3, 0, edge=3)

    g2 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend2
    )

    g2.add_vertices_from([5, "6", 7, 8])

    g2.add_edge(5, "6", edge=0)
    g2.add_edge("6", 7, edge=1)
    g2.add_edge(7, 8, edge="e2")
    g2.add_edge(8, 5, edge=3)

    with pytest.raises(TypeError):
        it = iso.vf2(g1, g2)
