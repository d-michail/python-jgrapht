import itertools

import pytest

import jgrapht as jg
from helpers import both, build

K4 = list(itertools.combinations(range(4), 2))
K5 = list(itertools.combinations(range(5), 2))
K33 = [(u, v) for u in range(3) for v in range(3, 6)]
C5 = [(i, (i + 1) % 5) for i in range(5)]


# ------------------------------------------------------------ planarity


@both
def test_planarity(sparse):
    assert jg.is_planar(build(4, K4, sparse=sparse))
    assert jg.is_planar(build(5, C5, sparse=sparse))
    assert not jg.is_planar(build(5, K5, sparse=sparse))
    assert not jg.is_planar(build(6, K33, sparse=sparse))


@both
def test_planar_embedding(sparse):
    g = build(4, K4, sparse=sparse)
    emb = jg.planar_embedding(g)
    assert sorted(emb) == [0, 1, 2, 3]
    for v, around in emb.items():
        assert sorted(around) == sorted(g.edges_of(v))  # each vertex lists exactly its edges
    assert jg.planar_embedding(build(5, K5, sparse=sparse)) is None


@both
def test_euler_formula_for_the_embedding(sparse):
    # V - E + F = 2 for a connected planar graph; count faces by tracing the rotation system
    g = build(4, K4, sparse=sparse)
    emb = jg.planar_embedding(g)
    nxt = {}
    for v, around in emb.items():
        for i, e in enumerate(around):
            nxt[(v, e)] = around[(i + 1) % len(around)]

    def other(e, v):
        return g.edge_target(e) if g.edge_source(e) == v else g.edge_source(e)

    seen, faces = set(), 0
    for v in emb:
        for e in emb[v]:
            if (v, e) in seen:
                continue
            faces += 1
            d = (v, e)
            while d not in seen:
                seen.add(d)
                u, edge = d
                w = other(edge, u)
                d = (w, nxt[(w, edge)])
    assert 4 - 6 + faces == 2


@both
@pytest.mark.parametrize("n,edges", [(5, K5), (6, K33)], ids=["K5", "K33"])
def test_kuratowski_subdivision(sparse, n, edges):
    g = build(n, edges, sparse=sparse)
    vertices, sub_edges = jg.kuratowski_subdivision(g)
    assert set(sub_edges) <= set(g.edges()) and set(vertices) <= set(range(n))
    assert len(vertices) >= 5 and len(sub_edges) >= 9
    assert jg.kuratowski_subdivision(build(4, K4, sparse=sparse)) is None


# ------------------------------------------------------------ lowest common ancestors


@both
def test_lowest_common_ancestors(sparse):
    #        0
    #      /   \
    #     1     2
    #    / \     \
    #   3   4     5
    g = build(6, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)], directed=True, sparse=sparse)
    pairs = [(3, 4), (3, 5), (4, 4), (1, 3), (0, 5)]
    assert jg.lowest_common_ancestors(g, 0, pairs) == [1, 0, 4, 1, 0]
    assert jg.lowest_common_ancestors(g, 0, []) == []


@both
def test_lca_errors(sparse):
    g = build(3, [(0, 1), (0, 2)], directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.lowest_common_ancestors(g, 9, [(1, 2)])
    with pytest.raises(jg.GraphError):
        jg.lowest_common_ancestors(g, 0, [(1, 9)])


# ------------------------------------------------------------ transforms


def edge_set(g, directed):
    pairs = [(g.edge_source(e), g.edge_target(e)) for e in g.edges()]
    return set(pairs) if directed else {frozenset(p) for p in pairs}


@both
def test_complement_undirected(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse)
    c = jg.complement(g)
    assert isinstance(c, jg.Graph) and not c.directed
    assert sorted(c.vertices()) == [0, 1, 2, 3]
    assert edge_set(c, False) == {frozenset(p) for p in [(0, 2), (0, 3), (1, 3)]}
    assert edge_set(jg.complement(c), False) == edge_set(g, False)  # complement twice
    assert edge_set(jg.complement(g, loops=True), False) == edge_set(c, False) | {frozenset([v]) for v in range(4)}


@both
def test_complement_directed(sparse):
    g = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    c = jg.complement(g)
    assert c.directed
    assert edge_set(c, True) == {(1, 0), (2, 1), (0, 2), (2, 0)}


@both
def test_line_graph_undirected(sparse):
    g = build(4, [(0, 1), (1, 2), (1, 3)], sparse=sparse)  # a star centred at 1
    lg = jg.line_graph(g)
    assert sorted(lg.vertices()) == [0, 1, 2]  # one vertex per original edge
    assert lg.edge_count() == 3 and not lg.directed  # the three edges pairwise share vertex 1
    path = jg.line_graph(build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse))
    assert edge_set(path, False) == {frozenset([0, 1]), frozenset([1, 2])}


@both
def test_line_graph_directed(sparse):
    g = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    lg = jg.line_graph(g)
    assert lg.directed and edge_set(lg, True) == {(0, 1)}  # edge 0 ends where edge 1 starts


@both
def test_transitive_closure(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], directed=True, sparse=sparse)
    c = jg.transitive_closure(g)
    assert c.directed
    assert edge_set(c, True) == {(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)}
    assert edge_set(jg.transitive_closure(c), True) == edge_set(c, True)  # idempotent


@both
def test_transitive_reduction(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)], directed=True, sparse=sparse)
    r = jg.transitive_reduction(g)
    assert edge_set(r, True) == {(0, 1), (1, 2), (2, 3)}


@both
def test_closure_of_a_cycle_and_loops_are_ignored(sparse):
    g = build(3, [(0, 1), (1, 2), (2, 0), (1, 1)], directed=True, sparse=sparse)
    c = jg.transitive_closure(g)
    assert len(edge_set(c, True)) == 6  # every ordered pair of distinct vertices, no loops


@both
def test_transforms_require_directed_graphs_where_needed(sparse):
    u = build(3, [(0, 1)], sparse=sparse)
    for f in (jg.transitive_closure, jg.transitive_reduction):
        with pytest.raises(jg.GraphError):
            f(u)
