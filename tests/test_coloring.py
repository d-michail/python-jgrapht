import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht.algorithms.coloring as coloring


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH])
def test_coloring(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    for i in range(0, 10):
        g.add_vertex(i)

    vcount = len(g.vertices)
    assert vcount == 10

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

    assert len(g.edges) == 18

    color_count, color_map = coloring.greedy_smallestnotusedcolor(g)
    assert color_count == 4
    assert all(
        [
            a == b
            for a, b in zip(
                [color_map[v] for v in g.vertices], [0, 1, 2, 1, 2, 1, 2, 1, 2, 3]
            )
        ]
    )
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.greedy_random(g, seed=17)
    assert color_count == 4
    assert all(
        [
            a == b
            for a, b in zip(
                [color_map[v] for v in g.vertices], [1, 2, 0, 2, 0, 2, 3, 0, 2, 0]
            )
        ]
    )
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.greedy_random(g)
    assert color_count > 0
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.greedy_dsatur(g)
    assert color_count == 4
    assert all(
        [
            a == b
            for a, b in zip(
                [color_map[v] for v in g.vertices], [0, 1, 2, 1, 2, 1, 3, 2, 1, 2]
            )
        ]
    )
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.backtracking_brown(g)
    assert color_count == 4
    assert all(
        [
            a == b
            for a, b in zip(
                [color_map[v] for v in g.vertices], [1, 2, 3, 2, 3, 2, 3, 2, 3, 4]
            )
        ]
    )
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.color_refinement(g)
    assert color_count == 10


    color_count, color_map = coloring.greedy_smallestdegreelast(g)
    assert color_count == 4
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )

    color_count, color_map = coloring.greedy_largestdegreefirst(g)
    assert color_count == 4
    assert all(
        [
            color_map[u] != color_map[v]
            for u, v in zip(
                [g.edge_source(e) for e in g.edges], [g.edge_target(e) for e in g.edges]
            )
        ]
    )


@pytest.mark.parametrize("backend", [GraphBackend.INT_GRAPH, GraphBackend.LONG_GRAPH, GraphBackend.REFCOUNT_GRAPH])
def test_chordal(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 0)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 5)
    g.add_edge(1, 3)

    color_count, color_map = coloring.chordal_min_coloring(g)

    assert color_count == 3
    assert color_map == {0: 0, 1: 1, 2: 0, 3: 2, 4: 1, 5: 2}


@pytest.mark.parametrize("backend", [GraphBackend.ANY_HASHABLE_GRAPH, GraphBackend.REFCOUNT_GRAPH])
def test_any_chordal(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend
    )

    v0 = g.add_vertex(str(0))
    v1 = g.add_vertex(str(1))
    v2 = g.add_vertex(str(2))
    v3 = g.add_vertex(str(3))
    v4 = g.add_vertex(str(4))
    v5 = g.add_vertex(str(5))

    g.add_edge(v0, v1)
    g.add_edge(v1, v2)
    g.add_edge(v2, v3)
    g.add_edge(v4, v5)
    g.add_edge(v5, v0)
    g.add_edge(v0, v3)
    g.add_edge(v0, v4)
    g.add_edge(v1, v5)
    g.add_edge(v1, v3)

    color_count, color_map = coloring.chordal_min_coloring(g)

    assert color_count == 3
    assert color_map == {"0": 0, "1": 1, "2": 0, "3": 2, "4": 1, "5": 2}


    color_count, color_map = coloring.backtracking_brown(g)
    assert color_count == 3
    assert color_map == {"0": 1, "1": 2, "2": 1, "3": 3, "4": 2, "5": 3}

