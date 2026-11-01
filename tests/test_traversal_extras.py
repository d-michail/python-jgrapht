import random

import pytest

import jgrapht as jg
from helpers import both, build, cycle, random_chordal, random_edges

K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# ------------------------------------------------------------ traversals


@both
def test_bfs_and_dfs_without_a_start_cover_every_component(sparse):
    g = build(6, [(0, 1), (1, 2), (3, 4)], sparse=sparse)  # vertex 5 is isolated
    assert sorted(jg.bfs(g)) == list(range(6)) and sorted(jg.dfs(g)) == list(range(6))
    assert sorted(jg.bfs(g, 0)) == [0, 1, 2] and sorted(jg.dfs(g, 3)) == [3, 4]
    assert jg.bfs(g)[0] == 0 and jg.dfs(g)[0] == 0
    with pytest.raises(jg.GraphError):
        jg.bfs(g, 99)


@both
def test_bfs_depths(sparse):
    g = build(5, [(0, 1), (1, 2), (0, 3), (3, 4)], sparse=sparse)
    assert jg.bfs_depths(g, 0) == {0: 0, 1: 1, 3: 1, 2: 2, 4: 2}
    assert jg.bfs_depths(build(3, [(0, 1)], directed=True, sparse=sparse), 1) == {1: 0}


@both
def test_dfs_postorder(sparse):
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5)]
    g = build(6, edges, directed=True, sparse=sparse)
    order = jg.dfs_postorder(g, 0)
    assert sorted(order) == list(range(6)) and order[-1] == 0
    position = {v: i for i, v in enumerate(order)}
    assert all(position[v] < position[u] for u, v in edges)  # every child before its parent
    assert sorted(jg.dfs_postorder(build(4, [(0, 1)], sparse=sparse))) == [0, 1, 2, 3]


@both
@pytest.mark.parametrize("seed", range(4))
@pytest.mark.parametrize("order_fn", [jg.lex_bfs_order, jg.maximum_cardinality_order])
def test_perfect_elimination_orders_of_chordal_graphs(sparse, seed, order_fn):
    g = build(10, random_chordal(10, seed), sparse=sparse)
    visit = order_fn(g)
    assert sorted(visit) == list(range(10))
    elimination = visit[::-1]  # the reverse of the search order is a perfect elimination order
    position = {v: i for i, v in enumerate(elimination)}
    for v in elimination:
        later = [u for u in g.neighbors_of(v) if position[u] > position[v]]
        assert all(b in g.neighbors_of(a) for a in later for b in later if a != b)


@both
@pytest.mark.parametrize(
    "n,edges,degeneracy",
    [(4, K4, 3), (5, [(i, i + 1) for i in range(4)], 1), (5, cycle(5), 2)],
    ids=["K4", "path", "cycle"],
)
def test_degeneracy_ordering(sparse, n, edges, degeneracy):
    g = build(n, edges, sparse=sparse)
    order, d = jg.degeneracy_ordering(g)
    assert d == degeneracy and sorted(order) == list(range(n))
    position = {v: i for i, v in enumerate(order)}
    for v in order:  # at most `degeneracy` neighbours come later in the ordering
        assert sum(1 for u in g.neighbors_of(v) if position[u] > position[v]) <= degeneracy


@both
def test_random_walk(sparse):
    g = build(5, cycle(5), directed=True, sparse=sparse)
    walk = jg.random_walk(g, 0, 12, seed=3)
    assert walk[0] == 0 and 1 <= len(walk) <= 13
    assert all((a + 1) % 5 == b for a, b in zip(walk, walk[1:]))  # follows the only out-edge
    assert jg.random_walk(g, 0, 12, seed=3) == walk  # reproducible
    sink = build(3, [(0, 1), (1, 2)], directed=True, sparse=sparse)
    assert jg.random_walk(sink, 0, 10, seed=1) == [0, 1, 2]  # stops at a vertex without out-edges
    assert jg.random_walk(g, 2, 0) == [2]


@both
def test_weighted_random_walk_never_takes_zero_weight_edges(sparse):
    g = build(3, [(0, 1), (0, 2)], [0.0, 1.0], directed=True, sparse=sparse)
    for seed in range(10):
        assert jg.random_walk(g, 0, 1, weighted=True, seed=seed) == [0, 2]
    with pytest.raises(jg.GraphError):
        jg.random_walk(g, 9, 3)


# ------------------------------------------------------------ strongly connected components


@both
@pytest.mark.parametrize("alg", ["tarjan", "kosaraju", "gabow", "kosaraju_inspector"])
@pytest.mark.parametrize("seed", range(3))
def test_scc_algorithms_agree(sparse, alg, seed):
    rng = random.Random(seed)
    edges = [tuple(rng.sample(range(10), 2)) for _ in range(16)]
    g = build(10, edges, directed=True, sparse=sparse)
    expected = sorted(sorted(c) for c in jg.strongly_connected_components(g))
    assert sorted(sorted(c) for c in jg.strongly_connected_components(g, alg)) == expected


@both
def test_scc_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.strongly_connected_components(build(2, [(0, 1)], directed=True, sparse=sparse), "nope")


@both
def test_connected_component_of_and_path_exists(sparse):
    g = build(6, [(0, 1), (1, 2), (3, 4)], directed=True, sparse=sparse)
    assert sorted(jg.connected_component_of(g, 2)) == [0, 1, 2]  # edge direction is ignored
    assert jg.connected_component_of(g, 5) == [5]
    assert jg.path_exists(g, 2, 0) and not jg.path_exists(g, 0, 3)
    with pytest.raises(jg.GraphError):
        jg.path_exists(g, 0, 99)


@both
def test_block_cutpoint_graph(sparse):
    bowtie = build(6, [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4), (4, 5)], sparse=sparse)
    tree, nodes, cutpoints = jg.block_cutpoint_graph(bowtie)
    assert sorted(cutpoints) == [2, 4]
    assert len(nodes) == 5 and len(tree) == 5 and tree.edge_count() == 4 and jg.is_tree(tree)
    blocks = sorted(sorted(n) for n in nodes if len(n) > 1)
    assert blocks == [[0, 1, 2], [2, 3, 4], [4, 5]]
    assert sorted(sorted(n) for n in nodes if len(n) == 1) == [[2], [4]]


# ------------------------------------------------------------ contract_edge, weighted line graph, cycle_to_path


def test_contract_edge_keeps_edge_objects_and_weights():
    g = jg.Graph(weighted=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", edge="ab", weight=1.0)
    g.add_edge("b", "c", edge="bc", weight=2.0)
    g.add_edge("c", "d", edge="cd", weight=3.0)
    contracted = jg.contract_edge(g, "bc")
    assert len(contracted) == 3 and contracted.edge_count() == 2
    assert set(contracted.edges()) == {"ab", "cd"}  # untouched edge objects survive
    assert contracted.edge_weight("cd") == 3.0 and contracted.edge_weight("ab") == 1.0
    assert len(g) == 4 and g.edge_count() == 3  # the original is unchanged
    ends = {frozenset((contracted.edge_source(e), contracted.edge_target(e))) for e in contracted.edges()}
    assert len(ends) == 2 and all(len(x) == 2 for x in ends)


def test_contract_edge_directed_and_errors():
    g = jg.Graph(directed=True)
    for v in range(3):
        g.add_vertex(v)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    c = jg.contract_edge(g, 0)
    assert c.directed and len(c) == 2 and c.edge_count() == 1
    with pytest.raises(jg.GraphError):
        jg.contract_edge(g, 99)
    with pytest.raises(jg.GraphError):
        jg.contract_edge(jg.SparseGraph(2, [(0, 1)]), 0)


@both
def test_weighted_line_graph(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse)
    lg = jg.line_graph(g, weight=lambda a, b: float(10 * a + b))
    assert lg.weighted and sorted(lg.vertices()) == [0, 1, 2]
    weights = sorted(lg.edge_weight(e) for e in lg.edges())
    assert weights in ([1.0, 12.0], [10.0, 21.0], [1.0, 21.0], [10.0, 12.0])  # one per ordered pair used
    assert lg.edge_count() == 2
    assert not jg.line_graph(g).weighted

    def boom(a, b):
        raise KeyError("no weight")

    with pytest.raises(KeyError):
        jg.line_graph(g, weight=boom)


@both
def test_cycle_to_path(sparse):
    g = build(4, cycle(4), [1.0, 2.0, 3.0, 4.0], sparse=sparse)
    p = jg.cycle_to_path(g, [2, 0, 3, 1])  # the edges in scrambled order
    assert p.vertices[0] == p.vertices[-1] and sorted(p.vertices[:-1]) == [0, 1, 2, 3]
    assert sorted(p.edges) == [0, 1, 2, 3] and p.weight == 10.0
    assert jg.cycle_to_path(g, []) is None
    with pytest.raises(jg.GraphError):
        jg.cycle_to_path(g, [0, 1])  # not a cycle
    with pytest.raises(jg.GraphError):
        jg.cycle_to_path(g, [0, 99])


# ------------------------------------------------------------ improve_tour


def line_metric_graph(n, sparse):
    edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
    return build(n, edges, [float(v - u) for u, v in edges], sparse=sparse)


@both
@pytest.mark.parametrize("seed", range(4))
def test_improve_tour_never_makes_it_worse(sparse, seed):
    g = line_metric_graph(9, sparse)
    rng = random.Random(seed)
    order = list(range(9))
    rng.shuffle(order)
    start = jg.hamiltonian_path  # keep the import used
    del start
    closed = order + [order[0]]
    before = sum(abs(a - b) for a, b in zip(closed, closed[1:]))
    improved = jg.improve_tour(g, order, passes=5, seed=seed)
    assert improved.vertices[0] == improved.vertices[-1] and sorted(improved.vertices[:-1]) == list(range(9))
    assert improved.weight <= before + 1e-9


@both
def test_improve_tour_accepts_paths_and_closed_lists(sparse):
    g = line_metric_graph(6, sparse)
    tour = jg.traveling_salesman_tour(g, "random", seed=2)
    by_path = jg.improve_tour(g, tour, seed=1)
    by_list = jg.improve_tour(g, tour.vertices, seed=1)  # already closed
    assert by_path.weight == by_list.weight <= tour.weight + 1e-9


@both
def test_improve_tour_errors(sparse):
    path = build(4, [(0, 1), (1, 2), (2, 3)], [1.0] * 3, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.improve_tour(path, [0, 1, 2, 3])  # 3 -> 0 is not an edge
    with pytest.raises(jg.GraphError):
        jg.improve_tour(build(3, [(0, 1)], directed=True, sparse=sparse), [0, 1, 2])


# ------------------------------------------------------------ TreeDynamicConnectivity


def test_tree_dynamic_connectivity_basics():
    t = jg.TreeDynamicConnectivity()
    assert t.add("a") and not t.add("a") and "a" in t and "z" not in t
    assert t.link("a", "b") and t.link("b", "c") and t.link(("d", 1), "e")
    assert t.connected("a", "c") and not t.connected("a", ("d", 1)) and not t.connected("a", "zzz")
    assert not t.link("a", "c") and not t.link("a", "a")  # would close a cycle / self link
    assert t.cut("b", "c") and not t.connected("a", "c") and t.connected("a", "b")
    assert t.link("c", ("d", 1)) and t.connected("c", "e")
    assert t.remove("b") and "b" not in t and not t.connected("a", "b")
    assert not t.remove("never-added")
    with pytest.raises(jg.GraphError):
        t.cut("a", "never-added")


@pytest.mark.parametrize("seed", range(5))
def test_tree_dynamic_connectivity_matches_a_reference(seed):
    rng = random.Random(seed)
    t, n = jg.TreeDynamicConnectivity(), 12
    for v in range(n):
        t.add(v)
    links = set()

    def component(start):
        seen, stack = {start}, [start]
        while stack:
            x = stack.pop()
            for a, b in links:
                for p, q in ((a, b), (b, a)):
                    if p == x and q not in seen:
                        seen.add(q)
                        stack.append(q)
        return seen

    for _ in range(200):
        u, v = rng.sample(range(n), 2)
        if rng.random() < 0.6:
            expected = v not in component(u)
            assert t.link(u, v) == expected
            if expected:
                links.add((u, v))
        elif links:
            a, b = rng.choice(sorted(links))
            assert t.cut(a, b)
            links.discard((a, b))
        x, y = rng.sample(range(n), 2)
        assert t.connected(x, y) == (y in component(x))
