import itertools

import pytest

import jgrapht as jg
from helpers import build

# VF2 rejects multigraphs, and SparseGraph is a multigraph by type, so these use Graph only
simple = dict(multi=False, loops=False)

C4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
PATH4 = [(0, 1), (1, 2), (2, 3)]


def ug(n, edges, **kw):
    return build(n, edges, **simple, **kw)


def is_isomorphism(g1, g2, m):
    """``m`` maps the vertices of g1 bijectively onto g2 and preserves adjacency."""
    if sorted(m) != sorted(g1.vertices()) or sorted(m.values()) != sorted(g2.vertices()):
        return False
    return all(
        bool(g1.edges_between(u, v)) == bool(g2.edges_between(m[u], m[v]))
        for u, v in itertools.permutations(m, 2)
    )


def test_isomorphic_graphs():
    g1 = ug(4, C4)
    g2 = ug(4, [(0, 2), (2, 1), (1, 3), (3, 0)])  # a relabelled 4-cycle
    assert jg.is_isomorphic(g1, g2)
    maps = jg.isomorphisms(g1, g2)
    assert len(maps) == 8  # the dihedral group of the square
    assert all(is_isomorphism(g1, g2, m) for m in maps)
    assert len(jg.isomorphisms(g1, g2, limit=3)) == 3


def test_not_isomorphic():
    assert not jg.is_isomorphic(ug(4, C4), ug(4, PATH4))
    assert jg.isomorphisms(ug(4, C4), ug(4, PATH4)) == []
    assert not jg.is_isomorphic(ug(4, C4), ug(5, C4))


def test_directed_isomorphism():
    a = ug(3, [(0, 1), (1, 2)], directed=True)
    b = ug(3, [(2, 1), (1, 0)], directed=True)
    (m,) = jg.isomorphisms(a, b)
    assert m == {0: 2, 1: 1, 2: 0}
    assert not jg.is_isomorphic(a, ug(3, [(0, 1), (2, 1)], directed=True))


def test_vertex_and_edge_matchers_restrict_the_mappings():
    labels1 = {0: "a", 1: "b", 2: "a", 3: "b"}
    labels2 = {0: "a", 1: "a", 2: "b", 3: "b"}
    g1, g2 = ug(4, C4), ug(4, [(0, 2), (2, 1), (1, 3), (3, 0)])
    unrestricted = jg.isomorphisms(g1, g2)
    same_label = jg.isomorphisms(g1, g2, vertex_match=lambda u, v: labels1[u] == labels2[v])
    assert 0 < len(same_label) < len(unrestricted)
    assert all(labels1[u] == labels2[v] for m in same_label for u, v in m.items())
    # an edge matcher on weights
    w1 = build(3, [(0, 1), (1, 2)], [1.0, 2.0], multi=False, loops=False)
    w2 = build(3, [(0, 1), (1, 2)], [2.0, 1.0], multi=False, loops=False)
    assert jg.is_isomorphic(w1, w2)  # as plain graphs
    by_weight = lambda e1, e2: w1.edge_weight(e1) == w2.edge_weight(e2)
    maps = jg.isomorphisms(w1, w2, edge_match=by_weight)
    assert maps == [{0: 2, 1: 1, 2: 0}]


def test_matcher_errors_propagate():
    g = ug(3, [(0, 1), (1, 2)])

    def boom(u, v):
        raise KeyError("matcher failed")

    with pytest.raises(KeyError, match="matcher failed"):
        jg.isomorphisms(g, g, vertex_match=boom)
    with pytest.raises(KeyError):
        jg.is_isomorphic(g, g, edge_match=boom)


def test_subgraph_isomorphism():
    host = ug(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])  # a 5-cycle
    path3 = ug(3, [(0, 1), (1, 2)])
    maps = jg.subgraph_isomorphisms(host, path3)
    assert len(maps) == 10  # 5 centres x 2 orientations
    for m in maps:  # pattern vertex -> host vertex, and the pattern is induced
        assert sorted(m) == [0, 1, 2]
        assert host.edges_between(m[0], m[1]) and host.edges_between(m[1], m[2])
        assert not host.edges_between(m[0], m[2])
    assert jg.is_subgraph_isomorphic(host, path3)
    assert not jg.is_subgraph_isomorphic(host, ug(3, [(0, 1), (1, 2), (0, 2)]))  # no triangle
    assert len(jg.subgraph_isomorphisms(host, path3, limit=4)) == 4


def test_graphs_of_different_kinds_are_rejected():
    directed = ug(2, [(0, 1)], directed=True)
    undirected = ug(2, [(0, 1)])
    with pytest.raises(jg.GraphError):
        jg.is_isomorphic(directed, undirected)
    with pytest.raises(jg.GraphError):
        jg.is_isomorphic(undirected, jg.SparseGraph(2, [(0, 1)]))
    with pytest.raises(TypeError):
        jg.is_isomorphic("not a graph", undirected)


def test_sparse_graphs_are_multigraphs_so_vf2_rejects_them():
    with pytest.raises(jg.GraphError):
        jg.is_isomorphic(jg.SparseGraph(2, [(0, 1)]), jg.SparseGraph(2, [(0, 1)]))


# ------------------------------------------------------------ trees


@pytest.mark.parametrize("sparse", [False, True], ids=["Graph", "SparseGraph"])
def test_unrooted_tree_isomorphism(sparse):
    t1 = build(5, [(0, 1), (1, 2), (1, 3), (3, 4)], sparse=sparse)
    t2 = build(5, [(4, 3), (3, 2), (3, 1), (1, 0)], sparse=sparse)
    m = jg.tree_isomorphism(t1, t2)
    assert m is not None and sorted(m) == list(range(5)) and sorted(m.values()) == list(range(5))
    for e in t1.edges():
        u, v = t1.edge_source(e), t1.edge_target(e)
        assert t2.edges_between(m[u], m[v])
    star = build(5, [(0, 1), (0, 2), (0, 3), (0, 4)], sparse=sparse)
    assert jg.tree_isomorphism(t1, star) is None


@pytest.mark.parametrize("sparse", [False, True], ids=["Graph", "SparseGraph"])
def test_rooted_tree_isomorphism(sparse):
    t = build(4, [(0, 1), (0, 2), (2, 3)], sparse=sparse)  # root 0 has a leaf and a 2-path
    u = build(4, [(3, 2), (3, 0), (0, 1)], sparse=sparse)  # same shape rooted at 3
    assert jg.tree_isomorphism(t, u, 0, 3) == {0: 3, 1: 2, 2: 0, 3: 1}
    assert jg.tree_isomorphism(t, u, 0, 2) is None  # different shape from root 2
    with pytest.raises(jg.GraphError):
        jg.tree_isomorphism(t, u, 0)  # one root only
