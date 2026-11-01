import pytest

import jgrapht as jg
from helpers import both, build

# two triangles sharing vertex 2, and a pendant edge 4-5
BOWTIE = [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4), (4, 5)]
K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
C5 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
PATH4 = [(0, 1), (1, 2), (2, 3)]


@both
def test_is_connected(sparse):
    assert jg.is_connected(build(6, BOWTIE, sparse=sparse))
    assert not jg.is_connected(build(4, [(0, 1), (2, 3)], sparse=sparse))
    assert jg.is_connected(build(1, [], sparse=sparse))


@both
def test_directed_connectivity(sparse):
    cycle = build(3, [(0, 1), (1, 2), (2, 0)], directed=True, sparse=sparse)
    path = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    assert jg.is_strongly_connected(cycle) and jg.is_weakly_connected(cycle)
    assert not jg.is_strongly_connected(path) and jg.is_weakly_connected(path)
    split = build(4, [(0, 1), (2, 3)], directed=True, sparse=sparse)
    assert not jg.is_weakly_connected(split)
    for f in (jg.is_strongly_connected, jg.is_weakly_connected):
        with pytest.raises(jg.GraphError):
            f(build(3, [(0, 1)], sparse=sparse))


@both
def test_articulation_points_bridges_blocks(sparse):
    g = build(6, BOWTIE, sparse=sparse)
    assert sorted(jg.articulation_points(g)) == [2, 4]
    assert jg.bridges(g) == [6]  # the pendant edge 4-5
    blocks = sorted(sorted(b) for b in jg.biconnected_components(g))
    assert blocks == [[0, 1, 2], [2, 3, 4], [4, 5]]
    assert not jg.is_biconnected(g)
    assert jg.is_biconnected(build(4, K4, sparse=sparse))
    assert jg.articulation_points(build(4, K4, sparse=sparse)) == []
    assert jg.bridges(build(4, K4, sparse=sparse)) == []


@both
def test_every_edge_of_a_path_is_a_bridge(sparse):
    g = build(4, PATH4, sparse=sparse)
    assert sorted(jg.bridges(g)) == [0, 1, 2]
    assert sorted(jg.articulation_points(g)) == [1, 2]


@both
def test_block_cut_tree(sparse):
    g = build(6, BOWTIE, sparse=sparse)
    blocks, cuts, edges = jg.block_cut_tree(g)
    assert sorted(sorted(b) for b in blocks) == [[0, 1, 2], [2, 3, 4], [4, 5]]
    assert sorted(cuts) == [2, 4]
    assert len(edges) == 4  # cut vertex 2 is in two blocks, cut vertex 4 in two blocks
    for b, c in edges:
        assert cuts[c] in blocks[b]  # an edge joins a block to a cut vertex it contains


@both
def test_condensation(sparse):
    g = build(4, [(0, 1), (1, 0), (1, 2), (2, 3), (3, 2)], directed=True, sparse=sparse)
    dag, comps = jg.condensation(g)
    assert isinstance(dag, jg.Graph) and dag.directed
    assert sorted(sorted(c) for c in comps) == [[0, 1], [2, 3]]
    assert sorted(dag.vertices()) == [0, 1] and dag.edge_count() == 1
    (e,) = dag.edges()
    assert set(comps[dag.edge_source(e)]) == {0, 1} and set(comps[dag.edge_target(e)]) == {2, 3}
    with pytest.raises(jg.GraphError):
        jg.condensation(build(2, [(0, 1)], sparse=sparse))


@both
@pytest.mark.parametrize(
    "n,edges,expected",
    [(5, C5, 2), (4, K4, 3), (4, PATH4, 1), (4, [(0, 1), (2, 3)], 0)],
    ids=["cycle", "K4", "path", "disconnected"],
)
def test_connectivity_numbers(sparse, n, edges, expected):
    g = build(n, edges, sparse=sparse)
    assert jg.edge_connectivity(g) == expected
    assert jg.vertex_connectivity(g) == expected
    assert jg.is_k_edge_connected(g, expected) and not jg.is_k_edge_connected(g, expected + 1)
    assert jg.is_k_vertex_connected(g, expected) and not jg.is_k_vertex_connected(g, expected + 1)


# ------------------------------------------------------------ simple properties


@both
def test_structure_properties(sparse):
    path = build(4, PATH4, sparse=sparse)
    k4 = build(4, K4, sparse=sparse)
    forest = build(4, [(0, 1), (2, 3)], sparse=sparse)
    assert jg.is_tree(path) and jg.is_forest(path)
    assert jg.is_forest(forest) and not jg.is_tree(forest)
    assert not jg.is_forest(k4) and not jg.is_tree(k4)
    assert jg.is_complete(k4) and not jg.is_complete(path)
    assert jg.is_cubic(k4) and not jg.is_cubic(path)
    assert not jg.is_triangle_free(k4) and jg.is_triangle_free(build(5, C5, sparse=sparse))


@both
def test_loops_and_parallel_edges(sparse):
    plain = build(3, [(0, 1), (1, 2)], sparse=sparse)
    loop = build(3, [(0, 1), (2, 2)], sparse=sparse)
    parallel = build(3, [(0, 1), (0, 1)], sparse=sparse)
    assert not jg.has_self_loops(plain) and jg.has_self_loops(loop)
    assert not jg.has_multiple_edges(plain) and jg.has_multiple_edges(parallel)
    assert jg.is_simple(plain) and not jg.is_simple(loop) and not jg.is_simple(parallel)


@both
def test_split_graph(sparse):
    triangle_pendant = build(4, [(0, 1), (1, 2), (0, 2), (2, 3)], sparse=sparse)
    assert jg.is_split(triangle_pendant)
    assert not jg.is_split(build(5, C5, sparse=sparse))
