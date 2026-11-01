import itertools
import math

import pytest

import jgrapht as jg
from helpers import both, build

# diamond network: 0 -> {1, 2} -> 3, capacities 3, 2 / 2, 3, so the maximum flow is 4
NET = [(0, 1), (1, 3), (0, 2), (2, 3)]
NET_W = [3.0, 2.0, 2.0, 3.0]

# two triangles (weight 2 edges) joined by a single weight 1 edge 2-3
TWO_TRIANGLES = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)]
TWO_TRIANGLES_W = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0]


def cut_weight(g, cut):
    return sum(g.edge_weight(e) for e in cut.cut_edges)


@both
@pytest.mark.parametrize("alg", ["dinic", "edmonds_karp", "push_relabel"])
def test_minimum_st_cut(sparse, alg):
    g = build(4, NET, NET_W, directed=True, sparse=sparse)
    cut = jg.minimum_st_cut(g, 0, 3, algorithm=alg)
    assert isinstance(cut, jg.MinimumCut)
    assert cut.capacity == 4.0 == cut_weight(g, cut)
    src, snk = set(cut.source_partition), set(cut.sink_partition)
    assert 0 in src and 3 in snk and not src & snk and src | snk == {0, 1, 2, 3}
    for e in cut.cut_edges:  # a directed cut edge goes from the source side to the sink side
        assert g.edge_source(e) in src and g.edge_target(e) in snk
    assert cut.capacity == jg.maximum_flow(g, 0, 3, algorithm=alg).value  # max-flow min-cut


@both
def test_minimum_st_cut_errors(sparse):
    g = build(4, NET, NET_W, directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.minimum_st_cut(g, 0, 0)
    with pytest.raises(jg.GraphError):
        jg.minimum_st_cut(g, 0, 3, algorithm="nope")


@both
def test_stoer_wagner(sparse):
    g = build(6, TWO_TRIANGLES, TWO_TRIANGLES_W, sparse=sparse)
    weight, side = jg.stoer_wagner_minimum_cut(g)
    assert weight == 1.0
    assert set(side) in ({0, 1, 2}, {3, 4, 5})


@both
def test_stoer_wagner_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.stoer_wagner_minimum_cut(build(1, [], [], sparse=sparse))  # needs two vertices
    with pytest.raises(jg.GraphError):
        jg.stoer_wagner_minimum_cut(build(3, [(0, 1)], [1.0], directed=True, sparse=sparse))


def tree_bottleneck(tree, u, v):
    """Smallest edge weight on the tree path from ``u`` to ``v``."""
    stack = [(u, None, math.inf)]
    while stack:
        x, parent, best = stack.pop()
        if x == v:
            return best
        for y in tree.neighbors_of(x):
            if y != parent:
                (e,) = tree.edges_between(x, y)
                stack.append((y, x, min(best, tree.edge_weight(e))))
    raise AssertionError("not connected")


@both
def test_gomory_hu_tree_gives_every_minimum_cut(sparse):
    g = build(6, TWO_TRIANGLES, TWO_TRIANGLES_W, sparse=sparse)
    tree = jg.gomory_hu_tree(g)
    assert isinstance(tree, jg.Graph) and tree.weighted and not tree.directed
    assert sorted(tree.vertices()) == list(range(6)) and tree.edge_count() == 5
    for u, v in itertools.combinations(range(6), 2):
        assert tree_bottleneck(tree, u, v) == jg.minimum_st_cut(g, u, v).capacity


@both
def test_equivalent_flow_tree_gives_every_maximum_flow(sparse):
    g = build(6, TWO_TRIANGLES, TWO_TRIANGLES_W, sparse=sparse)
    tree = jg.equivalent_flow_tree(g)
    assert tree.edge_count() == 5
    for u, v in itertools.combinations(range(6), 2):
        assert tree_bottleneck(tree, u, v) == jg.maximum_flow(g, u, v).value


@both
def test_minimum_odd_cut(sparse):
    g = build(6, TWO_TRIANGLES, TWO_TRIANGLES_W, sparse=sparse)
    cut = jg.minimum_odd_cut(g, [0, 3])
    assert cut.capacity == 1.0 == cut_weight(g, cut)
    assert jg.minimum_odd_cut(g, []) is None
    with pytest.raises(jg.GraphError):
        jg.minimum_odd_cut(g, [0, 1, 3])  # an odd number of odd vertices
    with pytest.raises(jg.GraphError):
        jg.minimum_odd_cut(g, [0, 9])


# ------------------------------------------------------------ arborescences


ARB = [(0, 1), (0, 2), (1, 2), (2, 3)]
ARB_W = [1.0, 5.0, 2.0, 1.0]


@both
def test_arborescences(sparse):
    g = build(4, ARB, ARB_W, directed=True, sparse=sparse)
    w, edges = jg.minimum_arborescence_tree(g, 0)
    assert w == 4.0 and sorted(edges) == [0, 2, 3]
    w, edges = jg.maximum_arborescence_tree(g, 0)
    assert w == 7.0 and sorted(edges) == [0, 1, 3]
    for w, edges in (jg.minimum_arborescence_tree(g, 0), jg.maximum_arborescence_tree(g, 0)):
        assert sorted(g.edge_target(e) for e in edges) == [1, 2, 3]  # one entering edge each


@both
def test_arborescence_errors(sparse):
    g = build(3, [(0, 1)], [1.0], directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.minimum_arborescence_tree(g, 0)  # vertex 2 is unreachable
    with pytest.raises(jg.GraphError):
        jg.minimum_arborescence_tree(build(2, [(0, 1)], [1.0], sparse=sparse), 0)


# ------------------------------------------------------------ Steiner trees


# centre 0 joined to leaves 1, 2, 3 by weight 1; the leaves are pairwise joined by weight 1.9
STAR = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
STAR_W = [1.0, 1.0, 1.0, 1.9, 1.9, 1.9]


@both
def test_steiner_tree(sparse):
    g = build(4, STAR, STAR_W, sparse=sparse)
    assert jg.steiner_tree_weight(g, [1, 2, 3]) == pytest.approx(3.0)  # via the centre
    w, edges = jg.steiner_tree(g, [1, 2, 3])
    assert 3.0 - 1e-9 <= w <= 2 * 3.0
    assert w == pytest.approx(sum(g.edge_weight(e) for e in edges))
    touched = {g.edge_source(e) for e in edges} | {g.edge_target(e) for e in edges}
    assert {1, 2, 3} <= touched and len(edges) == len(touched) - 1  # a tree covering the terminals


@both
def test_steiner_tree_on_a_path(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], [1.0, 2.0, 3.0], sparse=sparse)
    assert jg.steiner_tree_weight(g, [0, 3]) == 6.0
    assert jg.steiner_tree(g, [0, 3])[0] == 6.0
    assert jg.steiner_tree_weight(g, [1]) == 0.0


@both
def test_steiner_tree_errors(sparse):
    g = build(4, STAR, STAR_W, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.steiner_tree(g, [])
    with pytest.raises(jg.GraphError):
        jg.steiner_tree_weight(g, [1, 9])
    with pytest.raises(jg.GraphError):
        jg.steiner_tree(build(3, [(0, 1)], [1.0], directed=True, sparse=sparse), [0, 1])


# ------------------------------------------------------------ spanners


def distances(n, edges_with_ends):
    """All-pairs hop distances in the graph on ``0..n-1`` with the given ``(u, v)`` edges."""
    g = build(n, [(u, v) for u, v in edges_with_ends], sparse=False)
    return {u: jg.single_source_distances(g, u) for u in range(n)}


@both
@pytest.mark.parametrize("k", [1, 2, 3])
def test_greedy_spanner_stretch(sparse, k):
    n = 6
    edges = list(itertools.combinations(range(n), 2))  # K6
    g = build(n, edges, sparse=sparse)
    kept = jg.greedy_multiplicative_spanner(g, k)
    assert set(kept) <= set(g.edges())
    if k == 1:
        assert len(kept) == len(edges)  # stretch 1 keeps every edge
    else:
        assert len(kept) < len(edges)
    full = distances(n, edges)
    spanner = distances(n, [(g.edge_source(e), g.edge_target(e)) for e in kept])
    for u, v in itertools.combinations(range(n), 2):
        assert spanner[u][v] <= (2 * k - 1) * full[u][v]


@both
def test_greedy_spanner_errors(sparse):
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.greedy_multiplicative_spanner(g, 0)
    with pytest.raises(jg.GraphError):
        jg.greedy_multiplicative_spanner(build(3, [(0, 1)], directed=True, sparse=sparse), 2)
