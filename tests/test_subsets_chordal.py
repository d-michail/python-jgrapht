import itertools
import random

import pytest

import jgrapht as jg
from helpers import both, build, cycle, random_chordal, random_edges

K4 = list(itertools.combinations(range(4), 2))
TRIANGLE_TAIL = [(0, 1), (1, 2), (0, 2), (2, 3)]
C4 = [(0, 1), (1, 2), (2, 3), (3, 0)]


# ------------------------------------------------------------ cliques and independent sets


@both
@pytest.mark.parametrize("seed", range(4))
def test_clique_algorithms_agree(sparse, seed):
    g = build(10, random_edges(10, 22, seed), sparse=sparse)
    expected = {frozenset(c) for c in jg.maximal_cliques(g)}
    for alg in ("bron_kerbosch", "pivot", "degeneracy"):
        assert {frozenset(c) for c in jg.maximal_cliques(g, alg)} == expected, alg
    with pytest.raises(jg.GraphError):
        jg.maximal_cliques(g, "nope")


@both
def test_is_clique_and_independent_set(sparse):
    g = build(4, TRIANGLE_TAIL, sparse=sparse)
    assert jg.is_clique(g, [0, 1, 2]) and not jg.is_clique(g, [0, 1, 3])
    assert jg.is_independent_set(g, [0, 3]) and not jg.is_independent_set(g, [0, 1])
    assert jg.is_clique(g, []) and jg.is_independent_set(g, [])
    with pytest.raises(jg.GraphError):
        jg.is_clique(g, [0, 9])


@both
@pytest.mark.parametrize("seed", range(4))
def test_chordal_clique_and_independent_set_are_optimal(sparse, seed):
    g = build(9, random_chordal(9, seed), sparse=sparse)
    clique = jg.chordal_maximum_clique(g)
    assert jg.is_clique(g, clique) and len(clique) == len(jg.maximum_clique(g))
    indep = jg.chordal_maximum_independent_set(g)
    assert jg.is_independent_set(g, indep) and len(indep) == len(jg.maximum_independent_set(g))


@both
def test_chordal_algorithms_reject_non_chordal_graphs(sparse):
    g = build(4, C4, sparse=sparse)
    assert jg.chordal_maximum_clique(g) is None
    assert jg.chordal_maximum_independent_set(g) is None
    assert jg.chordal_minimal_separators(g) is None
    with pytest.raises(jg.GraphError):
        jg.chordal_maximum_clique(build(3, [(0, 1)], directed=True, sparse=sparse))


@both
def test_chordal_minimal_separators(sparse):
    assert jg.chordal_minimal_separators(build(3, [(0, 1), (1, 2)], sparse=sparse)) == {(1,): 1}
    assert jg.chordal_minimal_separators(build(4, TRIANGLE_TAIL, sparse=sparse)) == {(2,): 1}
    assert jg.chordal_minimal_separators(build(4, K4, sparse=sparse)) == {}


@both
def test_clique_minimal_separator_decomposition(sparse):
    bowtie = build(5, [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)], sparse=sparse)
    d = jg.clique_minimal_separator_decomposition(bowtie)
    assert sorted(sorted(a) for a in d.atoms) == [[0, 1, 2], [2, 3, 4]]
    assert [sorted(s) for s in d.separators] == [[2]]
    assert d.is_chordal and d.fill_edges == []
    assert isinstance(d.minimal_triangulation, jg.Graph) and d.minimal_triangulation.edge_count() == 6
    assert sorted(d.minimal_elimination_ordering) == list(range(5))
    c4 = jg.clique_minimal_separator_decomposition(build(4, C4, sparse=sparse))
    assert not c4.is_chordal and len(c4.fill_edges) == 1  # one chord triangulates the square
    assert c4.minimal_triangulation.edge_count() == 5
    assert [sorted(a) for a in c4.atoms] == [[0, 1, 2, 3]]


@both
def test_berge_certificate(sparse):
    assert jg.berge_certificate(build(4, C4, sparse=sparse)) is None
    kind, vs = jg.berge_certificate(build(5, cycle(5), sparse=sparse))
    assert kind == "odd_hole" and vs[0] == vs[-1] and sorted(vs[:-1]) == list(range(5))
    kind, vs = jg.berge_certificate(build(7, cycle(7), sparse=sparse))
    assert kind == "odd_hole" and vs[0] == vs[-1] and len(vs) == 8  # closed walk
    co7 = jg.complement(build(7, cycle(7), sparse=sparse))  # complement of an odd hole
    kind, vs = jg.berge_certificate(co7)
    assert kind == "odd_antihole" and vs[0] == vs[-1] and sorted(vs[:-1]) == list(range(7))
    with pytest.raises(jg.GraphError):
        jg.berge_certificate(build(3, [(0, 1)], directed=True, sparse=sparse))


@both
def test_triangle_counts(sparse):
    g = build(4, K4, sparse=sparse)
    assert jg.number_of_triangles(g) == 4
    assert jg.count_triangles_among(g, [0, 1, 2]) == 1
    assert jg.count_triangles_among(g, [0, 1]) == 0
    assert jg.number_of_triangles(build(4, C4, sparse=sparse)) == 0


# ------------------------------------------------------------ vertex covers


COVER_ALGS = ["greedy", "two_approximation", "bar_yehuda_even", "clarkson", "edge_based_two_approximation"]


@both
@pytest.mark.parametrize("alg", COVER_ALGS)
def test_vertex_cover_algorithms_produce_covers(sparse, alg):
    edges = random_edges(10, 18, 3)
    g = build(10, edges, sparse=sparse)
    weight, cover = jg.vertex_cover(g, alg)
    assert jg.is_vertex_cover(g, cover)
    assert weight == len(cover)
    optimum = min(
        len(c)
        for r in range(11)
        for c in itertools.combinations(range(10), r)
        if jg.is_vertex_cover(g, c)
    )
    if alg != "greedy":
        assert len(cover) <= 2 * optimum  # 2-approximations


@both
@pytest.mark.parametrize("alg", ["bar_yehuda_even", "clarkson"])
def test_weighted_vertex_cover_avoids_heavy_vertices(sparse, alg):
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)  # a path whose middle vertex is expensive
    weight, cover = jg.vertex_cover(g, alg, weights={1: 10.0})
    assert sorted(cover) == [0, 2] and weight == 2.0
    assert jg.vertex_cover(g, alg, weights=lambda v: 10.0 if v == 1 else 1.0)[0] == 2.0
    assert jg.vertex_cover(g, alg, weights=3.0)[0] >= 3.0  # constant weights


@both
def test_bipartite_vertex_cover_is_exact(sparse):
    k23 = build(5, [(u, v) for u in range(2) for v in range(2, 5)], sparse=sparse)
    weight, cover = jg.vertex_cover(k23, "bipartite")
    assert weight == 2 and sorted(cover) == [0, 1]
    with pytest.raises(jg.GraphError):
        jg.vertex_cover(build(3, [(0, 1), (1, 2), (0, 2)], sparse=sparse), "bipartite")


@both
def test_vertex_cover_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.vertex_cover(build(2, [(0, 1)], sparse=sparse), "nope")
    with pytest.raises(jg.GraphError, match="undirected"):
        jg.vertex_cover(build(2, [(0, 1)], directed=True, sparse=sparse), "bipartite")


# ------------------------------------------------------------ colorings


@both
@pytest.mark.parametrize(
    "alg", ["greedy", "largest_degree_first", "smallest_degree_last", "saturation_degree", "random_greedy", "brown_backtrack"]
)
def test_proper_colorings(sparse, alg):
    g = build(10, random_edges(10, 20, 5), sparse=sparse)
    k, colors = jg.coloring(g, alg, seed=1)
    assert jg.is_proper_coloring(g, colors) and k == len(set(colors.values()))


@both
def test_random_greedy_is_reproducible(sparse):
    g = build(12, random_edges(12, 25, 2), sparse=sparse)
    assert jg.coloring(g, "random_greedy", seed=7) == jg.coloring(g, "random_greedy", seed=7)


@both
@pytest.mark.parametrize("n,edges,chromatic", [(5, cycle(5), 3), (4, K4, 4), (6, cycle(6), 2), (3, [], 1)])
def test_brown_backtrack_finds_the_chromatic_number(sparse, n, edges, chromatic):
    g = build(n, edges, sparse=sparse)
    assert jg.coloring(g, "brown_backtrack")[0] == chromatic


@both
@pytest.mark.parametrize("seed", range(4))
def test_chordal_coloring_is_optimal(sparse, seed):
    g = build(9, random_chordal(9, seed), sparse=sparse)
    k, colors = jg.coloring(g, "chordal")
    assert jg.is_proper_coloring(g, colors) and k == len(jg.maximum_clique(g))
    with pytest.raises(jg.GraphError, match="chordal"):
        jg.coloring(build(4, C4, sparse=sparse), "chordal")


@both
def test_color_refinement(sparse):
    k, colors = jg.coloring(build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse), "color_refinement")
    assert k == 2 and colors[0] == colors[3] and colors[1] == colors[2] and colors[0] != colors[1]
    assert jg.coloring(build(5, cycle(5), sparse=sparse), "color_refinement")[0] == 1


@both
def test_is_proper_coloring(sparse):
    g = build(3, [(0, 1), (1, 2)], sparse=sparse)
    assert jg.is_proper_coloring(g, {0: 0, 1: 1, 2: 0})
    assert not jg.is_proper_coloring(g, {0: 0, 1: 0, 2: 1})


@both
def test_coloring_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.coloring(build(3, [(0, 1)], sparse=sparse), "nope")


# ------------------------------------------------------------ decompositions


TREE = [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5)]


@both
def test_heavy_path_decomposition(sparse):
    g = build(6, TREE, sparse=sparse)
    d = jg.heavy_path_decomposition(g, 0)
    assert d.subtree_size == {0: 6, 1: 4, 2: 1, 3: 1, 4: 2, 5: 1}
    assert d.depth == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}
    assert d.parent == {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 4}
    assert sorted(d.paths) == [[0, 1, 4, 5], [2], [3]]
    heavy = {frozenset((g.edge_source(e), g.edge_target(e))) for e in d.heavy_edges}
    light = {frozenset((g.edge_source(e), g.edge_target(e))) for e in d.light_edges}
    # an edge is heavy when its child holds more than half of the parent's subtree
    assert heavy == {frozenset((0, 1))}
    assert heavy | light == {frozenset(p) for p in TREE} and not heavy & light


@both
def test_heavy_path_decomposition_of_a_forest(sparse):
    g = build(5, [(0, 1), (1, 2), (3, 4)], sparse=sparse)
    d = jg.heavy_path_decomposition(g, [0, 3])
    assert sorted(d.paths) == [[0, 1, 2], [3, 4]]
    assert d.component[0] == d.component[2] != d.component[3]
    with pytest.raises(jg.GraphError):
        jg.heavy_path_decomposition(g, 9)


def test_heavy_path_decomposition_with_tuple_vertices():
    g = jg.Graph()
    for v in [(0, 0), (0, 1), (1, 0)]:
        g.add_vertex(v)
    g.add_edge((0, 0), (0, 1))
    g.add_edge((0, 1), (1, 0))
    d = jg.heavy_path_decomposition(g, (0, 0))  # one tuple root, not a list of two roots
    assert d.paths == [[(0, 0), (0, 1), (1, 0)]]


@both
def test_dulmage_mendelsohn(sparse):
    g = build(5, [(0, 3), (1, 3), (2, 4)], sparse=sparse)
    left_dom, right_dom, matched = jg.dulmage_mendelsohn_decomposition(g, [0, 1, 2], [3, 4])
    assert left_dom == [0, 1, 3] and right_dom == [] and matched == [[2, 4]]
    parts = left_dom + right_dom + [v for s in matched for v in s]
    assert sorted(parts) == list(range(5))  # a partition of all vertices
    fine = jg.dulmage_mendelsohn_decomposition(g, [0, 1, 2], [3, 4], fine=True)
    assert sorted(v for s in fine[2] for v in s) == [2, 4]
    with pytest.raises(jg.GraphError):
        jg.dulmage_mendelsohn_decomposition(build(3, [(0, 1)], directed=True, sparse=sparse), [0], [1])
