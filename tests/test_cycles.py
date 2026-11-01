import pytest

import jgrapht as jg
from helpers import both, build

SQUARE = [(0, 1), (1, 2), (2, 3), (3, 0)]
SQUARE_DIAGONAL = SQUARE + [(0, 2)]
SIMPLE_CYCLE_ALGS = ["johnson", "tarjan", "tiernan", "szwarcfiter_lauer", "hawick_james"]


def canon(cycle):
    """A cycle (vertex list) rotated to start at its smallest vertex."""
    i = cycle.index(min(cycle))
    return tuple(cycle[i:] + cycle[:i])


def is_closed_walk(g, path):
    return (
        path.vertices[0] == path.vertices[-1]
        and len(path.edges) == len(path.vertices) - 1
        and all(
            {g.edge_source(e), g.edge_target(e)} == {u, v}
            for e, u, v in zip(path.edges, path.vertices, path.vertices[1:])
        )
    )


# ------------------------------------------------------------ detection


@both
def test_has_cycle_directed(sparse):
    assert not jg.has_cycle(build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse))
    assert jg.has_cycle(build(3, [(0, 1), (1, 2), (2, 0)], directed=True, sparse=sparse))
    assert jg.has_cycle(build(2, [(0, 0)], directed=True, sparse=sparse))  # self-loop
    # an undirected-looking pair of arcs 0->1, 1->0 is a directed 2-cycle
    assert jg.has_cycle(build(2, [(0, 1), (1, 0)], directed=True, sparse=sparse))
    assert not jg.has_cycle(build(3, [(0, 1), (0, 2), (1, 2)], directed=True, sparse=sparse))


@both
def test_has_cycle_undirected(sparse):
    assert not jg.has_cycle(build(5, [(0, 1), (1, 2), (3, 4)], sparse=sparse))  # forest
    assert not jg.has_cycle(build(3, [], sparse=sparse))
    assert jg.has_cycle(build(3, [(0, 1), (1, 2), (2, 0)], sparse=sparse))
    assert jg.has_cycle(build(5, [(0, 1), (1, 2), (3, 4), (4, 3)], sparse=sparse))  # parallel
    assert jg.has_cycle(build(2, [(0, 1), (1, 1)], sparse=sparse))  # self-loop


@both
def test_vertices_on_cycles(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 0), (2, 3)], directed=True, sparse=sparse)
    assert sorted(jg.vertices_on_cycles(g)) == [0, 1, 2]
    assert jg.vertices_on_cycles(build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)) == []
    with pytest.raises(jg.GraphError):
        jg.vertices_on_cycles(build(3, [(0, 1)], sparse=sparse))


# ------------------------------------------------------------ simple cycles


@both
@pytest.mark.parametrize("alg", SIMPLE_CYCLE_ALGS)
def test_simple_cycles(sparse, alg):
    g = build(3, [(0, 1), (1, 2), (2, 0), (1, 0)], directed=True, sparse=sparse)
    assert sorted(canon(c) for c in jg.simple_cycles(g, alg)) == [(0, 1), (0, 1, 2)]


@both
@pytest.mark.parametrize("alg", SIMPLE_CYCLE_ALGS)
def test_simple_cycles_complete_digraph(sparse, alg):
    edges = [(u, v) for u in range(3) for v in range(3) if u != v]
    g = build(3, edges, directed=True, sparse=sparse)
    cycles = {canon(c) for c in jg.simple_cycles(g, alg)}
    assert cycles == {(0, 1), (0, 2), (1, 2), (0, 1, 2), (0, 2, 1)}


@both
@pytest.mark.parametrize("alg", SIMPLE_CYCLE_ALGS)
def test_simple_cycles_acyclic(sparse, alg):
    assert jg.simple_cycles(build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse), alg) == []


@both
def test_simple_cycles_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.simple_cycles(build(3, [(0, 1), (1, 2), (2, 0)], sparse=sparse))
    with pytest.raises(jg.GraphError):
        jg.simple_cycles(build(2, [(0, 1)], directed=True, sparse=sparse), "nope")


# ------------------------------------------------------------ cycle basis


@both
@pytest.mark.parametrize("alg", ["paton", "queue_bfs", "stack_bfs"])
def test_cycle_basis(sparse, alg):
    g = build(4, SQUARE_DIAGONAL, sparse=sparse)
    basis = jg.cycle_basis(g, alg)
    assert len(basis) == 2  # m - n + components = 5 - 4 + 1
    for cycle in basis:
        degree = {}
        for e in cycle:
            for v in (g.edge_source(e), g.edge_target(e)):
                degree[v] = degree.get(v, 0) + 1
        assert set(degree.values()) == {2}  # every vertex of a cycle has degree 2
    assert len({frozenset(c) for c in basis}) == 2


@both
@pytest.mark.parametrize("alg", ["paton", "queue_bfs", "stack_bfs"])
def test_cycle_basis_of_a_forest_is_empty(sparse, alg):
    assert jg.cycle_basis(build(4, [(0, 1), (1, 2)], sparse=sparse), alg) == []


@both
def test_paton_rejects_parallel_edges(sparse):
    g = build(2, [(0, 1), (0, 1)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.cycle_basis(g, "paton")
    assert len(jg.cycle_basis(g, "queue_bfs")) == 1


@both
def test_cycle_basis_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.cycle_basis(build(3, [(0, 1)], directed=True, sparse=sparse))
    with pytest.raises(jg.GraphError):
        jg.cycle_basis(build(3, [(0, 1)], sparse=sparse), "nope")


# ------------------------------------------------------------ Eulerian cycle, Chinese postman


@both
@pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
def test_eulerian_cycle(sparse, directed):
    g = build(4, SQUARE, directed=directed, sparse=sparse)
    assert jg.is_eulerian(g)
    p = jg.eulerian_cycle(g)
    assert is_closed_walk(g, p) if not directed else p.vertices[0] == p.vertices[-1]
    assert sorted(p.edges) == [0, 1, 2, 3]  # every edge exactly once


@both
def test_not_eulerian(sparse):
    path = build(3, [(0, 1), (1, 2)], sparse=sparse)
    assert not jg.is_eulerian(path)
    with pytest.raises(jg.GraphError):
        jg.eulerian_cycle(path)
    two_triangles = build(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)], sparse=sparse)
    assert not jg.is_eulerian(two_triangles)  # all degrees even, but disconnected


@both
def test_chinese_postman_undirected(sparse):
    g = build(3, [(0, 1), (1, 2)], [1.0, 2.0], sparse=sparse)
    p = jg.chinese_postman(g)
    assert is_closed_walk(g, p) and p.weight == 6.0
    assert set(p.edges) == {0, 1}


@both
def test_chinese_postman_directed(sparse):
    g = build(3, [(0, 1), (1, 2), (2, 0), (1, 0)], [1.0] * 4, directed=True, sparse=sparse)
    p = jg.chinese_postman(g)
    assert p.vertices[0] == p.vertices[-1] and set(p.edges) == {0, 1, 2, 3}
    assert p.weight == 5.0  # edge 0->1 is repeated once


@both
def test_chinese_postman_eulerian_graph_needs_no_repeats(sparse):
    g = build(4, SQUARE, [1.0, 2.0, 3.0, 4.0], sparse=sparse)
    assert jg.chinese_postman(g).weight == 10.0


@both
def test_chinese_postman_needs_a_connected_graph(sparse):
    g = build(4, [(0, 1), (2, 3)], [1.0, 1.0], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.chinese_postman(g)


# ------------------------------------------------------------ minimum mean cycle


@both
def test_minimum_mean_cycle(sparse):
    g = build(
        4, [(0, 1), (1, 0), (2, 3), (3, 2), (1, 2)], [1.0, 3.0, 1.0, 1.0, 0.5], directed=True, sparse=sparse
    )
    mean, cycle = jg.minimum_mean_cycle(g)
    assert mean == pytest.approx(1.0)
    assert sorted(set(cycle.vertices)) == [2, 3]
    assert cycle.weight / len(cycle) == pytest.approx(mean)


@both
def test_minimum_mean_cycle_of_a_dag_is_none(sparse):
    g = build(3, [(0, 1), (1, 2)], [1.0, 1.0], directed=True, sparse=sparse)
    assert jg.minimum_mean_cycle(g) is None


@both
def test_minimum_mean_cycle_needs_a_directed_graph(sparse):
    with pytest.raises(jg.GraphError):
        jg.minimum_mean_cycle(build(3, [(0, 1)], [1.0], sparse=sparse))


# ------------------------------------------------------------ chordality


@both
@pytest.mark.parametrize("order", ["mcs", "lex_bfs"])
def test_chordal_graph(sparse, order):
    g = build(4, [(0, 1), (1, 2), (0, 2), (2, 3)], sparse=sparse)
    assert jg.is_chordal(g, order)
    peo = jg.perfect_elimination_order(g, order)
    assert sorted(peo) == [0, 1, 2, 3]
    assert jg.chordal_hole(g, order) is None
    # in a perfect elimination order each vertex's later neighbours form a clique
    pos = {v: i for i, v in enumerate(peo)}
    for v in peo:
        later = [u for u in g.neighbors_of(v) if pos[u] > pos[v]]
        for a in later:
            for b in later:
                assert a == b or b in g.neighbors_of(a)


@both
@pytest.mark.parametrize("order", ["mcs", "lex_bfs"])
def test_non_chordal_graph_has_a_hole(sparse, order):
    g = build(4, SQUARE, sparse=sparse)
    assert not jg.is_chordal(g, order)
    assert jg.perfect_elimination_order(g, order) is None
    hole = jg.chordal_hole(g, order)
    assert len(hole) == 4 and is_closed_walk(g, hole)
    assert jg.is_chordal(build(4, SQUARE_DIAGONAL, sparse=sparse), order)  # a chord fixes it


@both
def test_chordality_errors(sparse):
    g = build(3, [(0, 1)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.is_chordal(g, "nope")
    with pytest.raises(jg.GraphError):
        jg.is_chordal(build(3, [(0, 1)], directed=True, sparse=sparse))
