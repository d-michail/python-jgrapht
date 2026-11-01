import itertools
import math
import random

import pytest

import jgrapht as jg
from helpers import both, build


def random_graph(n, extra, seed, directed=False, sparse=False, no_parallel=False):
    """A strongly connected random weighted graph: a ring plus ``extra`` random chords."""
    rng = random.Random(seed)
    edges = [(i, (i + 1) % n) for i in range(n)]
    key = (lambda e: e) if directed else (lambda e: tuple(sorted(e)))
    seen = {key(e) for e in edges}
    for _ in range(extra):
        e = tuple(rng.sample(range(n), 2))
        if no_parallel and key(e) in seen:
            continue
        seen.add(key(e))
        edges.append(e)
    weights = [float(rng.randint(1, 9)) for _ in edges]
    return build(n, edges, weights, directed=directed, sparse=sparse)


def path_weight(g, p):
    return sum(g.edge_weight(e) for e in p.edges)


def check_path(g, p, s, t):
    assert p.vertices[0] == s and p.vertices[-1] == t
    assert p.weight == pytest.approx(path_weight(g, p))
    for e, u, v in zip(p.edges, p.vertices, p.vertices[1:]):
        assert (g.edge_source(e), g.edge_target(e)) in ({(u, v)} if g.directed else {(u, v), (v, u)})


DIRECTED = pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])


# ------------------------------------------------------------ batch queries, many-to-many


@both
@DIRECTED
@pytest.mark.parametrize("alg", ["contraction_hierarchy", "transit_node_routing", "dijkstra"])
def test_batch_shortest_paths_match_dijkstra(sparse, directed, alg):
    g = random_graph(30, 45, 7, directed, sparse)
    rng = random.Random(1)
    pairs = [(rng.randrange(30), rng.randrange(30)) for _ in range(25)]
    results = jg.batch_shortest_paths(g, pairs, alg)
    assert len(results) == len(pairs)
    for (s, t), p in zip(pairs, results):
        expected = jg.shortest_path(g, s, t)
        assert p.weight == pytest.approx(expected.weight)
        check_path(g, p, s, t)


@both
def test_batch_shortest_paths_details(sparse):
    g = build(4, [(0, 1), (1, 2)], [1.0, 2.0], directed=True, sparse=sparse)
    for alg in ("contraction_hierarchy", "dijkstra"):
        paths = jg.batch_shortest_paths(g, [(0, 2), (2, 0), (1, 1)], alg)
        assert paths[0].weight == 3.0 and paths[1] is None and paths[2].vertices == [1]
    assert jg.batch_shortest_paths(g, [], "contraction_hierarchy") == []
    big = random_graph(40, 60, 3, False, sparse)
    assert jg.batch_shortest_paths(big, [(0, 20)], "transit_node_routing", transit_vertex_count=6)[0] is not None
    assert jg.batch_shortest_paths(big, [(0, 20)], "contraction_hierarchy", parallelism=2)[0] is not None
    with pytest.raises(jg.GraphError):
        jg.batch_shortest_paths(g, [(0, 2)], "nope")
    with pytest.raises(jg.GraphError):
        jg.batch_shortest_paths(g, [(0, 9)], "dijkstra")
    negative = build(2, [(0, 1)], [-1.0], directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.batch_shortest_paths(negative, [(0, 1)], "contraction_hierarchy")


@both
@DIRECTED
@pytest.mark.parametrize("alg", ["contraction_hierarchy", "dijkstra", "default"])
def test_many_to_many(sparse, directed, alg):
    g = random_graph(25, 30, 11, directed, sparse)
    sources, targets = [0, 3, 7], [2, 9, 14, 20]
    result = jg.many_to_many_shortest_paths(g, sources, targets, alg)
    assert set(result) == set(itertools.product(sources, targets))
    for (s, t), p in result.items():
        assert p.weight == pytest.approx(jg.shortest_path(g, s, t).weight)
        check_path(g, p, s, t)


@both
def test_many_to_many_with_more_sources_than_targets_and_unreachable_pairs(sparse):
    g = build(4, [(0, 1), (2, 1)], [1.0, 1.0], directed=True, sparse=sparse)
    for alg in ("contraction_hierarchy", "dijkstra", "default"):
        r = jg.many_to_many_shortest_paths(g, [0, 2, 3], [1], alg)
        assert set(r) == {(0, 1), (2, 1)}  # 3 cannot reach 1
        assert jg.many_to_many_shortest_paths(g, [1], [0, 2], alg) == {}
    with pytest.raises(jg.GraphError):
        jg.many_to_many_shortest_paths(g, [0], [1], "nope")


# ------------------------------------------------------------ ALT, bidirectional A*, closest first


@both
@DIRECTED
@pytest.mark.parametrize("bidirectional", [False, True])
def test_alt_matches_dijkstra(sparse, directed, bidirectional):
    g = random_graph(30, 40, 5, directed, sparse)
    for s, t in [(0, 17), (5, 29), (12, 12)]:
        p = jg.alt_shortest_path(g, s, t, [0, 10, 20], bidirectional=bidirectional)
        assert p.weight == pytest.approx(jg.shortest_path(g, s, t).weight)
        check_path(g, p, s, t)


@both
def test_alt_unreachable_and_errors(sparse):
    g = build(3, [(0, 1)], [1.0], directed=True, sparse=sparse)
    assert jg.alt_shortest_path(g, 0, 2, [0]) is None
    with pytest.raises(jg.GraphError):
        jg.alt_shortest_path(g, 0, 1, [9])


def grid(n, sparse):
    edges = [(r * n + c, r * n + c + 1) for r in range(n) for c in range(n - 1)]
    edges += [(r * n + c, (r + 1) * n + c) for r in range(n - 1) for c in range(n)]
    return build(n * n, edges, [1.0] * len(edges), sparse=sparse)


@both
def test_bidirectional_astar(sparse):
    n = 6
    g = grid(n, sparse)

    def manhattan(v, t):
        return abs(v // n - t // n) + abs(v % n - t % n)

    p = jg.bidirectional_astar_shortest_path(g, 0, n * n - 1, manhattan)
    assert p.weight == 2 * (n - 1)
    check_path(g, p, 0, n * n - 1)
    assert jg.bidirectional_astar_shortest_path(g, 0, 0, lambda v, t: 0).vertices == [0]
    disconnected = build(3, [(0, 1)], [1.0], sparse=sparse)
    assert jg.bidirectional_astar_shortest_path(disconnected, 0, 2, lambda v, t: 0) is None


@both
def test_bidirectional_astar_callback_errors(sparse):
    g = grid(3, sparse)

    def boom(v, t):
        raise ValueError("no estimate")

    with pytest.raises(ValueError, match="no estimate"):
        jg.bidirectional_astar_shortest_path(g, 0, 8, boom)
    with pytest.raises(TypeError):
        jg.bidirectional_astar_shortest_path(g, 0, 8, lambda v, t: "far")


@both
@DIRECTED
def test_closest_first(sparse, directed):
    g = random_graph(20, 25, 2, directed, sparse)
    order = jg.closest_first(g, 0)
    distances = [d for _, d in order]
    assert distances == sorted(distances) and order[0] == (0, 0.0)
    assert {v: d for v, d in order} == jg.single_source_distances(g, 0)
    within = jg.closest_first(g, 0, radius=5.0)
    assert within == [(v, d) for v, d in order if d <= 5.0]
    with pytest.raises(jg.GraphError):
        jg.closest_first(g, 0, radius=-1.0)


@both
def test_tree_center(sparse):
    assert jg.tree_center(build(5, [(i, i + 1) for i in range(4)], sparse=sparse)) == [2]
    assert sorted(jg.tree_center(build(4, [(i, i + 1) for i in range(3)], sparse=sparse))) == [1, 2]


# ------------------------------------------------------------ single-source paths, negative cycles


@both
@pytest.mark.parametrize(
    "alg", ["dijkstra", "bidirectional_dijkstra", "delta_stepping", "delta_stepping_parallel", "bellman_ford"]
)
def test_single_source_paths_and_parallel_delta_stepping(sparse, alg):
    g = random_graph(25, 30, 4, True, sparse)
    paths = jg.single_source_paths(g, 0, alg)
    dist = jg.single_source_distances(g, 0)
    assert set(paths) == set(dist)
    for v, p in paths.items():
        assert p.vertices[0] == 0 and p.vertices[-1] == v
        assert p.weight == pytest.approx(dist[v])
    assert jg.single_source_distances(g, 0, alg) == pytest.approx(dist)


@both
def test_negative_cycle(sparse):
    g = build(3, [(0, 1), (1, 2), (2, 1)], [1.0, 1.0, -3.0], directed=True, sparse=sparse)
    cycle = jg.negative_cycle(g, 0)
    assert cycle.vertices[0] == cycle.vertices[-1] and cycle.weight < 0
    assert sum(g.edge_weight(e) for e in cycle.edges) == pytest.approx(cycle.weight)
    ok = build(3, [(0, 1), (1, 2)], [1.0, -1.0], directed=True, sparse=sparse)
    assert jg.negative_cycle(ok, 0) is None
    with pytest.raises(jg.GraphError):
        jg.negative_cycle(ok, 9)


# ------------------------------------------------------------ multi-objective


# a -> b -> d is cheap and slow, a -> c -> d is dear and fast, a -> d is dominated by both
MO_EDGES = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 3)]
MO_WEIGHTS = {0: (1, 5), 1: (1, 5), 2: (5, 1), 3: (5, 1), 4: (12, 12)}


@both
@pytest.mark.parametrize("alg", ["martin", "label_correcting"])
def test_multi_objective_pareto_paths(sparse, alg):
    g = build(4, MO_EDGES, directed=True, sparse=sparse)

    def vector(p):
        return tuple(sum(MO_WEIGHTS[e][i] for e in p.edges) for i in range(2))

    by_target = jg.multi_objective_shortest_paths(g, 0, MO_WEIGHTS, algorithm=alg)
    assert set(by_target) == {0, 1, 2, 3}
    assert sorted(vector(p) for p in by_target[3]) == [(2, 10), (10, 2)]  # the direct edge is dominated
    only = jg.multi_objective_shortest_paths(g, 0, lambda e: MO_WEIGHTS[e], target=3, algorithm=alg)
    assert isinstance(only, list) and sorted(vector(p) for p in only) == [(2, 10), (10, 2)]
    assert len(jg.multi_objective_shortest_paths(g, 0, MO_WEIGHTS, target=1, algorithm=alg)) == 1


@both
def test_multi_objective_errors(sparse):
    g = build(4, MO_EDGES, directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.multi_objective_shortest_paths(g, 0, MO_WEIGHTS, algorithm="nope")
    with pytest.raises(jg.GraphError):  # a weight vector is missing
        jg.multi_objective_shortest_paths(g, 0, {0: (1, 1)})
    with pytest.raises(TypeError):
        jg.multi_objective_shortest_paths(g, 0, 5)

    def boom(e):
        raise KeyError("no weights")

    with pytest.raises(KeyError):
        jg.multi_objective_shortest_paths(g, 0, boom)


# ------------------------------------------------------------ path validators


DIAMOND = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 3)]


@both
def test_yen_path_validator(sparse):
    g = build(4, DIAMOND, [1.0, 1.0, 2.0, 2.0, 5.0], directed=True, sparse=sparse)
    assert len(jg.k_shortest_paths(g, 0, 3, 5)) == 3
    seen = []

    def no_edge_1(partial, edge):
        seen.append((partial, edge))
        return edge != 1  # forbid the edge 1 -> 3

    paths = jg.k_shortest_paths(g, 0, 3, 5, path_validator=no_edge_1)
    assert all(1 not in p.edges for p in paths) and len(paths) == 2
    assert seen and all(isinstance(p, jg.GraphPath) for p, _ in seen)
    assert len(jg.k_shortest_paths(g, 0, 3, 5, path_validator=lambda p, e: True)) == 3


@both
def test_bounded_pruned_yen_matches_yen(sparse):
    # the bounded variant works on vertex sequences, so compare on a graph without parallel edges
    g = random_graph(15, 25, 8, True, sparse, no_parallel=True)
    yen = jg.k_shortest_paths(g, 0, 9, 6)
    bounded = jg.k_shortest_paths(g, 0, 9, 6, "bounded_pruned_yen")
    assert [p.weight for p in bounded] == pytest.approx([p.weight for p in yen])


@both
def test_all_directed_paths_validator(sparse):
    g = build(4, DIAMOND, directed=True, sparse=sparse)
    only_first_edge = jg.all_directed_paths(g, 0, 3, path_validator=lambda partial, edge: len(partial) < 1)
    assert [p.edges for p in only_first_edge] == [[4]]  # only the direct edge is one edge long
    everything = jg.all_directed_paths(g, 0, 3, path_validator=lambda partial, edge: True)
    assert sorted(len(p) for p in everything) == [1, 2, 2]
    avoid = jg.all_directed_paths(g, 0, 3, path_validator=lambda partial, edge: edge != 4)
    assert all(4 not in p.edges for p in avoid) and len(avoid) == 2


@both
def test_validator_errors(sparse):
    g = build(4, DIAMOND, directed=True, sparse=sparse)

    def boom(partial, edge):
        raise RuntimeError("validator failed")

    with pytest.raises(RuntimeError, match="validator failed"):
        jg.k_shortest_paths(g, 0, 3, 3, path_validator=boom)
    with pytest.raises(RuntimeError, match="validator failed"):
        jg.all_directed_paths(g, 0, 3, path_validator=boom)
    with pytest.raises(jg.GraphError):  # only Yen supports validators
        jg.k_shortest_paths(g, 0, 3, 3, "bounded_pruned_yen", path_validator=lambda p, e: True)
