"""Tests for ``astar_shortest_path`` and its Python heuristic callback.

Every test runs on both graph classes: ``Graph`` (hashable vertex objects) and ``SparseGraph``
(integer vertices ``0..n``).
"""

import math
import random

import pytest

import jgrapht as jg

both = pytest.mark.parametrize("sparse", [False, True], ids=["Graph", "SparseGraph"])


def build(n, edges, weights=None, directed=False, sparse=False):
    """Graph on vertices ``0..n-1`` (``edges`` are index pairs)."""
    if sparse:
        return jg.SparseGraph(n, edges, directed=directed, weights=weights)
    g = jg.Graph(
        directed=directed, weighted=weights is not None, allow_multiple_edges=True
    )
    for v in range(n):
        g.add_vertex(v)
    for i, (u, v) in enumerate(edges):
        g.add_edge(u, v, weight=None if weights is None else weights[i])
    return g


def grid(n, sparse):
    """``n x n`` unit grid. Returns ``(graph, vertex_of(r, c), coords_of(vertex))``."""
    if sparse:
        edges = []
        for r in range(n):
            for c in range(n):
                if c + 1 < n:
                    edges.append((r * n + c, r * n + c + 1))
                if r + 1 < n:
                    edges.append((r * n + c, (r + 1) * n + c))
        return jg.SparseGraph(n * n, edges), (lambda r, c: r * n + c), (lambda v: divmod(v, n))
    g = jg.Graph()
    for r in range(n):
        for c in range(n):
            g.add_vertex((r, c))
    for r in range(n):
        for c in range(n):
            if c + 1 < n:
                g.add_edge((r, c), (r, c + 1))
            if r + 1 < n:
                g.add_edge((r, c), (r + 1, c))
    return g, (lambda r, c: (r, c)), (lambda v: v)


def manhattan(coords_of):
    def h(v, target):
        (r1, c1), (r2, c2) = coords_of(v), coords_of(target)
        return abs(r1 - r2) + abs(c1 - c2)

    return h


# ---------------------------------------------------------------- result correctness


@both
def test_grid_path_matches_dijkstra(sparse):
    g, at, coords = grid(6, sparse)
    s, t = at(0, 0), at(5, 5)
    p = jg.astar_shortest_path(g, s, t, manhattan(coords))
    d = jg.shortest_path(g, s, t)
    assert isinstance(p, jg.GraphPath)
    assert p.weight == d.weight == 10.0
    assert len(p) == 10 and len(p.vertices) == 11 and len(p.edges) == 10
    assert p.vertices[0] == s and p.vertices[-1] == t


@both
def test_path_is_a_real_path(sparse):
    g, at, coords = grid(5, sparse)
    p = jg.astar_shortest_path(g, at(0, 4), at(4, 0), manhattan(coords))
    for u, v, e in zip(p.vertices, p.vertices[1:], p.edges):
        assert e in g.edges_between(u, v)
        assert {g.edge_source(e), g.edge_target(e)} == {u, v}


@both
def test_weighted_detour_is_found(sparse):
    # direct 0-3 costs 10, the detour 0-1-2-3 costs 3
    g = build(4, [(0, 3), (0, 1), (1, 2), (2, 3)], [10.0, 1.0, 1.0, 1.0], sparse=sparse)
    p = jg.astar_shortest_path(g, 0, 3, lambda v, t: 0.0)
    assert p.vertices == [0, 1, 2, 3] and p.weight == 3.0


@both
def test_parallel_edges_pick_the_lighter(sparse):
    g = build(2, [(0, 1), (0, 1)], [5.0, 2.0], sparse=sparse)
    p = jg.astar_shortest_path(g, 0, 1, lambda v, t: 0.0)
    assert p.weight == 2.0 and len(p) == 1
    assert g.edge_weight(p.edges[0]) == 2.0


@both
def test_directed_respects_direction(sparse):
    g = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    assert jg.astar_shortest_path(g, 0, 2, lambda v, t: 0.0).vertices == [0, 1, 2]
    assert jg.astar_shortest_path(g, 2, 0, lambda v, t: 0.0) is None


@both
def test_source_equals_target(sparse):
    g, at, coords = grid(3, sparse)
    p = jg.astar_shortest_path(g, at(1, 1), at(1, 1), manhattan(coords))
    assert p.weight == 0.0 and len(p) == 0 and p.vertices == [at(1, 1)] and p.edges == []


@both
def test_unreachable_returns_none(sparse):
    g = build(4, [(0, 1), (2, 3)], sparse=sparse)
    assert jg.astar_shortest_path(g, 0, 3, lambda v, t: 0.0) is None
    assert jg.astar_shortest_path(g, 0, 3) is None


@both
def test_without_heuristic_equals_dijkstra(sparse):
    g, at, _ = grid(5, sparse)
    p = jg.astar_shortest_path(g, at(0, 0), at(4, 4))
    assert p.weight == jg.shortest_path(g, at(0, 0), at(4, 4)).weight
    assert jg.astar_shortest_path(g, at(0, 0), at(4, 4), heuristic=None).weight == 8.0


@both
def test_custom_edge_objects_are_returned(sparse):
    if sparse:
        pytest.skip("SparseGraph edges are always integers")
    g = jg.Graph(weighted=True)
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b", edge="ab", weight=1.0)
    g.add_edge("b", "c", edge=("bc", 1), weight=1.0)
    p = jg.astar_shortest_path(g, "a", "c", lambda v, t: 0.0)
    assert p.vertices == ["a", "b", "c"] and p.edges == ["ab", ("bc", 1)]


# ---------------------------------------------------------------- randomized comparison


def random_weighted(n, m, seed, sparse, directed):
    rng = random.Random(seed)
    edges, weights = [], []
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            edges.append((u, v))
            weights.append(float(rng.randint(1, 9)))
    return build(n, edges, weights, directed=directed, sparse=sparse)


@both
@pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
@pytest.mark.parametrize("seed", range(5))
def test_random_graphs_agree_with_dijkstra(sparse, directed, seed):
    n = 30
    g = random_weighted(n, 90, seed, sparse, directed)
    rng = random.Random(1000 + seed)
    for _ in range(10):
        s, t = rng.randrange(n), rng.randrange(n)
        expected = jg.shortest_path(g, s, t)
        zero = jg.astar_shortest_path(g, s, t, lambda v, tt: 0.0)
        assert (zero is None) == (expected is None)
        if expected is None:
            continue
        assert math.isclose(zero.weight, expected.weight)
        # a perfect (and therefore admissible and consistent) heuristic: the exact distance
        # to the target, computed on the reversed problem
        if not directed:
            exact = jg.single_source_distances(g, t)
            perfect = jg.astar_shortest_path(g, s, t, lambda v, tt: exact.get(v, 0.0))
            assert math.isclose(perfect.weight, expected.weight)


# ---------------------------------------------------------------- the callback


@both
def test_callback_receives_vertex_and_target(sparse):
    g, at, coords = grid(4, sparse)
    s, t = at(0, 0), at(3, 3)
    seen = []

    def h(v, target):
        seen.append((v, target))
        return manhattan(coords)(v, target)

    jg.astar_shortest_path(g, s, t, h)
    assert seen
    assert all(target == t for _, target in seen)  # always the search target
    assert all(v in g for v, _ in seen)  # always a vertex of the graph
    assert all(type(v) is type(s) for v, _ in seen)  # the caller's own vertex objects


def test_callback_gets_the_original_vertex_objects():
    g = jg.Graph()
    a, b, c = ("a", 1), "b", frozenset({3})
    for v in (a, b, c):
        g.add_vertex(v)
    g.add_edge(a, b)
    g.add_edge(b, c)
    received = []
    p = jg.astar_shortest_path(g, a, c, lambda v, t: received.append(v) or 0.0)
    assert p.vertices == [a, b, c]
    assert received and all(v in (a, b, c) for v in received)


@both
def test_good_heuristic_looks_at_fewer_vertices_than_a_zero_heuristic(sparse):
    g, at, coords = grid(15, sparse)
    s, t = at(0, 0), at(14, 14)
    informed, blind = [], []
    h = manhattan(coords)
    jg.astar_shortest_path(g, s, t, lambda v, tt: informed.append(v) or h(v, tt))
    jg.astar_shortest_path(g, s, t, lambda v, tt: blind.append(v) or 0.0)
    assert informed and blind
    assert len(set(informed)) < len(set(blind))


@both
def test_callback_may_return_ints_and_floats(sparse):
    g, at, coords = grid(4, sparse)
    h = manhattan(coords)
    s, t = at(0, 0), at(3, 3)
    assert jg.astar_shortest_path(g, s, t, h).weight == 6.0  # ints
    assert jg.astar_shortest_path(g, s, t, lambda v, tt: float(h(v, tt))).weight == 6.0
    assert jg.astar_shortest_path(g, s, t, lambda v, tt: h(v, tt) * 0.5).weight == 6.0


@both
def test_inconsistent_but_admissible_heuristic_is_still_optimal(sparse):
    g, at, coords = grid(6, sparse)
    h = manhattan(coords)

    def jumpy(v, target):
        # admissible (never above the true distance) but not consistent: alternates 0 / exact
        r, c = coords(v)
        return h(v, target) if (r + c) % 2 else 0.0

    s, t = at(0, 0), at(5, 5)
    assert jg.astar_shortest_path(g, s, t, jumpy).weight == 10.0


@both
def test_callable_objects_and_builtin_callables_work(sparse):
    g, at, coords = grid(4, sparse)

    class Heuristic:
        calls = 0

        def __call__(self, v, target):
            Heuristic.calls += 1
            return manhattan(coords)(v, target)

    s, t = at(0, 0), at(3, 3)
    assert jg.astar_shortest_path(g, s, t, Heuristic()).weight == 6.0
    assert Heuristic.calls > 0
    assert jg.astar_shortest_path(g, s, t, lambda *args: 0).weight == 6.0


# ---------------------------------------------------------------- callback failures


class HeuristicError(Exception):
    pass


@both
def test_exception_in_callback_is_reraised_unchanged(sparse):
    g, at, _ = grid(4, sparse)
    boom = HeuristicError("no estimate")

    def h(v, target):
        raise boom

    with pytest.raises(HeuristicError) as info:
        jg.astar_shortest_path(g, at(0, 0), at(3, 3), h)
    assert info.value is boom


@both
def test_search_stops_calling_the_callback_after_it_fails(sparse):
    g, at, _ = grid(5, sparse)
    calls = []

    def h(v, target):
        calls.append(v)
        raise ValueError("fail")

    with pytest.raises(ValueError):
        jg.astar_shortest_path(g, at(0, 0), at(4, 4), h)
    assert len(calls) == 1


@both
def test_only_the_first_error_is_reported(sparse):
    g, at, coords = grid(4, sparse)
    n = []

    def h(v, target):
        n.append(1)
        if len(n) == 3:
            raise KeyError("third")
        if len(n) > 3:
            raise RuntimeError("must not be reached")
        return manhattan(coords)(v, target)

    with pytest.raises(KeyError):
        jg.astar_shortest_path(g, at(0, 0), at(3, 3), h)
    assert len(n) == 3


@both
@pytest.mark.parametrize("bad", ["far", None, [1.0], object()], ids=["str", "None", "list", "object"])
def test_non_numeric_return_value_raises_type_error(sparse, bad):
    g, at, _ = grid(3, sparse)
    with pytest.raises(TypeError):
        jg.astar_shortest_path(g, at(0, 0), at(2, 2), lambda v, t: bad)


@both
def test_not_callable_heuristic_raises_type_error(sparse):
    g, at, _ = grid(3, sparse)
    with pytest.raises(TypeError):
        jg.astar_shortest_path(g, at(0, 0), at(2, 2), 3.0)


@both
def test_callback_error_does_not_leave_the_graph_unusable(sparse):
    g, at, coords = grid(4, sparse)
    with pytest.raises(ZeroDivisionError):
        jg.astar_shortest_path(g, at(0, 0), at(3, 3), lambda v, t: 1 / 0)
    assert jg.astar_shortest_path(g, at(0, 0), at(3, 3), manhattan(coords)).weight == 6.0


@both
def test_callback_may_query_the_graph(sparse):
    g, at, coords = grid(4, sparse)
    h = manhattan(coords)

    def reads_graph(v, target):
        assert v in g and g.degree_of(v) >= 2  # read-only access from inside the callback
        return h(v, target)

    assert jg.astar_shortest_path(g, at(0, 0), at(3, 3), reads_graph).weight == 6.0


# ---------------------------------------------------------------- argument errors


@both
def test_unknown_vertices_raise_graph_error(sparse):
    g, at, _ = grid(3, sparse)
    missing = 99 if sparse else (9, 9)
    with pytest.raises(jg.GraphError):
        jg.astar_shortest_path(g, missing, at(0, 0))
    with pytest.raises(jg.GraphError):
        jg.astar_shortest_path(g, at(0, 0), missing)


def test_wrong_graph_type_raises_type_error():
    with pytest.raises(TypeError):
        jg.astar_shortest_path("not a graph", 0, 1)
