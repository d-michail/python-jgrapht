import random

import pytest

import jgrapht as jg
from helpers import both, build

TRIANGLE_TAIL = [(0, 1), (1, 2), (0, 2), (2, 3)]  # perfect matching {01, 23}
PENTAGON = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]  # max matching 2, never perfect
PATH4_W = ([(0, 1), (1, 2), (2, 3)], [1.0, 5.0, 1.0])


def check_valid(g, m, cardinality=False):
    """The matched edges share no vertex, and the weight is the sum of their weights (or, for the
    cardinality algorithms, their number)."""
    seen = []
    for e in m:
        seen += [g.edge_source(e), g.edge_target(e)]
    assert len(seen) == len(set(seen))
    assert set(seen) == m.matched_vertices
    assert m.weight == pytest.approx(
        len(m) if cardinality else sum(g.edge_weight(e) for e in m)
    )
    assert len(m) == len(m.edges)
    assert list(m) == m.edges
    for v in range(len(g)):
        assert m.is_matched(v) == (v in seen)
    assert m.is_perfect() == (len(seen) == len(g))


# ------------------------------------------------------------ maximum cardinality


@both
@pytest.mark.parametrize("alg", ["sparse_edmonds", "dense_edmonds"])
def test_exact_maximum_matching(sparse, alg):
    g = build(4, TRIANGLE_TAIL, sparse=sparse)
    m = jg.maximum_matching(g, alg)
    assert isinstance(m, jg.Matching) and len(m) == 2 and m.is_perfect()
    check_valid(g, m)
    p = build(5, PENTAGON, sparse=sparse)
    m = jg.maximum_matching(p, alg)
    assert len(m) == 2 and not m.is_perfect()
    check_valid(p, m)


@both
def test_greedy_maximum_matching_is_maximal(sparse):
    g = build(5, PENTAGON, sparse=sparse)
    m = jg.maximum_matching(g, "greedy")
    check_valid(g, m)
    assert 1 <= len(m) <= 2
    # maximal: no edge has both endpoints unmatched
    for e in g.edges():
        assert m.is_matched(g.edge_source(e)) or m.is_matched(g.edge_target(e))


@both
def test_empty_graph_and_isolated_vertices(sparse):
    g = build(3, [], sparse=sparse)
    m = jg.maximum_matching(g)
    assert len(m) == 0 and m.weight == 0.0 and not m.is_perfect() and m.matched_vertices == set()


@both
@pytest.mark.parametrize("seed", range(6))
def test_edmonds_variants_agree_on_random_graphs(sparse, seed):
    rng = random.Random(seed)
    n = 14
    edges = list({tuple(sorted(rng.sample(range(n), 2))) for _ in range(24)})
    g = build(n, edges, sparse=sparse)
    sparse_m = jg.maximum_matching(g, "sparse_edmonds")
    dense_m = jg.maximum_matching(g, "dense_edmonds")
    greedy_m = jg.maximum_matching(g, "greedy")
    for m in (sparse_m, dense_m, greedy_m):
        check_valid(g, m)
    assert len(sparse_m) == len(dense_m)
    assert len(sparse_m) / 2 <= len(greedy_m) <= len(sparse_m)


# ------------------------------------------------------------ weighted matchings


@both
def test_weighted_matching_prefers_the_heavy_edge(sparse):
    edges, w = PATH4_W
    g = build(4, edges, w, sparse=sparse)
    for alg in ("greedy", "path_growing"):
        m = jg.weighted_matching(g, alg)
        check_valid(g, m)
        assert m.weight >= 5.0 / 2  # both are 1/2-approximations of the optimum 5.0
    assert jg.weighted_matching(g, "greedy").edges == [1]


@both
def test_perfect_matching_min_and_max(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3), (3, 0)], [1.0, 4.0, 1.0, 4.0], sparse=sparse)
    lo = jg.perfect_matching(g)
    hi = jg.perfect_matching(g, objective="maximize")
    check_valid(g, lo)
    check_valid(g, hi)
    assert lo.is_perfect() and hi.is_perfect()
    assert lo.weight == 2.0 and sorted(lo.edges) == [0, 2]
    assert hi.weight == 8.0 and sorted(hi.edges) == [1, 3]


@both
def test_perfect_matching_infeasible(sparse):
    with pytest.raises(jg.GraphError):  # odd number of vertices
        jg.perfect_matching(build(3, [(0, 1), (1, 2)], [1.0, 1.0], sparse=sparse))
    star = build(4, [(0, 1), (0, 2), (0, 3)], [1.0, 1.0, 1.0], sparse=sparse)
    with pytest.raises(jg.GraphError):  # even, but no perfect matching exists
        jg.perfect_matching(star)


# ------------------------------------------------------------ bipartite


K22 = [(0, 2), (0, 3), (1, 2), (1, 3)]
K22_W = [1.0, 3.0, 3.0, 1.0]


@both
def test_bipartite_maximum_matching(sparse):
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)
    m = jg.bipartite_maximum_matching(g, [0, 2], [1])
    check_valid(g, m)
    assert len(m) == 1
    assert len(jg.bipartite_maximum_matching(g)) == 1  # partitions computed
    k = build(4, K22, sparse=sparse)
    assert len(jg.bipartite_maximum_matching(k, [0, 1], [2, 3])) == 2
    assert len(jg.bipartite_maximum_matching(k, [2, 3], [0, 1])) == 2  # order does not matter


@both
def test_bipartite_maximum_weight_matching(sparse):
    g = build(4, K22, K22_W, sparse=sparse)
    m = jg.bipartite_maximum_weight_matching(g, [0, 1], [2, 3])
    check_valid(g, m)
    assert m.weight == 6.0 and sorted(m.edges) == [1, 2]
    assert jg.bipartite_maximum_weight_matching(g).weight == 6.0


@both
def test_bipartite_minimum_weight_perfect_matching(sparse):
    g = build(4, K22, K22_W, sparse=sparse)
    m = jg.bipartite_minimum_weight_perfect_matching(g, [0, 1], [2, 3])
    check_valid(g, m)
    assert m.is_perfect() and m.weight == 2.0 and sorted(m.edges) == [0, 3]


@both
def test_kuhn_munkres_needs_a_complete_balanced_graph(sparse):
    unbalanced = build(3, [(0, 1), (2, 1)], [1.0, 1.0], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.bipartite_minimum_weight_perfect_matching(unbalanced, [0, 2], [1])
    missing_edge = build(4, K22[:3], K22_W[:3], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.bipartite_minimum_weight_perfect_matching(missing_edge, [0, 1], [2, 3])


@both
def test_bipartite_argument_errors(sparse):
    triangle = build(3, [(0, 1), (1, 2), (0, 2)], sparse=sparse)
    with pytest.raises(jg.GraphError):  # not bipartite and no partitions given
        jg.bipartite_maximum_matching(triangle)
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)
    with pytest.raises(jg.GraphError):  # only one side given
        jg.bipartite_maximum_matching(g, [0, 2])
    with pytest.raises(jg.GraphError):  # unknown vertex
        jg.bipartite_maximum_matching(g, [0, 9], [1])


# ------------------------------------------------------------ errors and Graph specifics


@both
def test_directed_graphs_and_bad_arguments_are_rejected(sparse):
    d = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    for f in (jg.maximum_matching, jg.weighted_matching, jg.perfect_matching):
        with pytest.raises(jg.GraphError, match="undirected"):
            f(d)
    with pytest.raises(jg.GraphError, match="undirected"):
        jg.bipartite_maximum_matching(d)
    g = build(2, [(0, 1)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.maximum_matching(g, "nope")
    with pytest.raises(jg.GraphError):
        jg.weighted_matching(g, "nope")
    with pytest.raises(jg.GraphError):
        jg.perfect_matching(g, objective="nope")
    with pytest.raises(TypeError):
        jg.maximum_matching("not a graph")


def test_graph_with_hashable_vertices_and_edges():
    g = jg.Graph(weighted=True)
    for v in ("a", "b", "c", "d"):
        g.add_vertex(v)
    g.add_edge("a", "b", edge="ab", weight=1.0)
    g.add_edge("c", "d", edge=("cd", 1), weight=2.0)
    g.add_edge("b", "c", edge="bc", weight=1.0)
    m = jg.maximum_matching(g)
    assert set(m.edges) == {"ab", ("cd", 1)} and m.is_perfect()
    assert m.weight == 2.0  # cardinality algorithms count edges, not edge weights
    assert m.matched_vertices == {"a", "b", "c", "d"} and m.is_matched("a")
    assert not m.is_matched("zzz")
