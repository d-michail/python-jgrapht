import itertools
import math

import pytest

import jgrapht as jg
from helpers import both, build

# two K4's {0..3} and {4..7} joined by the bridge 3-4
K4A = list(itertools.combinations(range(4), 2))
K4B = [(u + 4, v + 4) for u, v in K4A]
TWO_CLIQUES = K4A + K4B + [(3, 4)]
TWO_CLIQUES_W = [1.0] * 12 + [9.0]
CLIQUES = [{0, 1, 2, 3}, {4, 5, 6, 7}]


def as_sets(clusters):
    return sorted((frozenset(c) for c in clusters), key=min)


# ------------------------------------------------------------ clustering


@both
def test_modularity(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    good = jg.modularity(g, [sorted(c) for c in CLIQUES])
    assert good == pytest.approx(2 * (6 / 13 - 0.25))
    assert jg.modularity(g, [list(range(8))]) == pytest.approx(0.0)
    assert jg.modularity(g, [[0, 4, 1, 5], [2, 6, 3, 7]]) < good
    with pytest.raises(jg.GraphError):
        jg.modularity(build(3, [(0, 1)], directed=True, sparse=sparse), [[0, 1, 2]])


@both
def test_girvan_newman_and_greedy_modularity_find_the_cliques(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    assert as_sets(jg.girvan_newman_clustering(g, 2)) == [frozenset(c) for c in CLIQUES]
    assert as_sets(jg.greedy_modularity_clustering(g)) == [frozenset(c) for c in CLIQUES]


@both
def test_k_spanning_tree_clustering_cuts_the_heavy_edge(sparse):
    g = build(8, TWO_CLIQUES, TWO_CLIQUES_W, sparse=sparse)
    assert as_sets(jg.k_spanning_tree_clustering(g, 2)) == [frozenset(c) for c in CLIQUES]
    assert len(jg.k_spanning_tree_clustering(g, 1)) == 1
    assert len(jg.k_spanning_tree_clustering(g, 8)) == 8
    for bad in (0, 9):
        with pytest.raises(jg.GraphError):
            jg.k_spanning_tree_clustering(g, bad)


@both
def test_label_propagation(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    clusters = jg.label_propagation_clustering(g, seed=1)
    assert sorted(v for c in clusters for v in c) == list(range(8))  # a partition
    assert 1 <= len(clusters) <= 2
    again = jg.label_propagation_clustering(g, seed=1)
    assert as_sets(clusters) == as_sets(again)  # reproducible
    isolated = build(3, [], sparse=sparse)
    assert len(jg.label_propagation_clustering(isolated, seed=0)) == 3


# ------------------------------------------------------------ link prediction, SimRank


@both
def test_link_scores(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse)
    assert jg.link_score(g, 0, 2) == 1.0  # one common neighbour (1)
    assert jg.link_score(g, 0, 3) == 0.0
    assert jg.link_score(g, 0, 2, "jaccard") == pytest.approx(0.5)  # {1} / {1, 3}
    assert jg.link_score(g, 0, 2, "preferential_attachment") == 2.0
    assert jg.link_score(g, 0, 2, "resource_allocation") == pytest.approx(0.5)
    for name in (
        "common_neighbors total_neighbors jaccard sorensen salton hub_promoted hub_depressed "
        "leicht_holme_newman preferential_attachment adamic_adar resource_allocation"
    ).split():
        assert math.isfinite(jg.link_score(g, 0, 2, name))
    with pytest.raises(jg.GraphError):
        jg.link_score(g, 0, 2, "nope")
    with pytest.raises(jg.GraphError):
        jg.link_score(g, 0, 9)


@both
def test_predict_links(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse)
    ranked = jg.predict_links(g, 0)
    assert [v for v, _ in ranked] == [2, 3]  # non-neighbours of 0, best first
    assert ranked[0][1] > ranked[1][1]
    assert all(v not in g.neighbors_of(0) for v, _ in ranked)


@both
def test_simrank(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3)], sparse=sparse)
    s = jg.simrank(g)
    for v in range(4):
        assert s[(v, v)] == pytest.approx(1.0)
    for u, v in itertools.product(range(4), repeat=2):
        assert 0.0 <= s[(u, v)] <= 1.0 and s[(u, v)] == pytest.approx(s[(v, u)])
    assert s[(0, 2)] > s[(0, 1)]  # same parity vertices are more similar on a path


# ------------------------------------------------------------ tree edit distance


def labelled_tree(labels, edges):
    g = jg.Graph()
    for x in labels:
        g.add_vertex(x)
    for u, v in edges:
        g.add_edge(u, v)
    return g


def test_tree_edit_distance():
    t1 = labelled_tree("rxy", [("r", "x"), ("r", "y")])
    same = labelled_tree("rxy", [("r", "x"), ("r", "y")])
    renamed = labelled_tree("rxz", [("r", "x"), ("r", "z")])
    bigger = labelled_tree("rxyw", [("r", "x"), ("r", "y"), ("y", "w")])
    assert jg.tree_edit_distance(t1, same, "r", "r") == 0.0
    assert jg.tree_edit_distance(t1, renamed, "r", "r") == 1.0  # relabel y -> z
    assert jg.tree_edit_distance(t1, bigger, "r", "r") == 1.0  # insert w


def test_tree_edit_distance_custom_costs_and_direction():
    t1 = labelled_tree("rx", [("r", "x")])
    t2 = labelled_tree("ry", [("r", "y")])
    assert jg.tree_edit_distance(t1, t2, "r", "r") == 1.0
    assert jg.tree_edit_distance(t1, t2, "r", "r", change_cost=lambda a, b: 0 if a == b else 10) == 2.0  # remove+insert
    seen = {"remove": [], "insert": [], "change": []}

    def remove(v):
        seen["remove"].append(v)
        return 0.5

    def insert(v):
        seen["insert"].append(v)
        return 0.5

    def change(a, b):
        seen["change"].append((a, b))
        return 0.0 if a == b else 10.0

    # remove x (0.5) + insert y (0.5); the root is kept
    assert jg.tree_edit_distance(t1, t2, "r", "r", change, insert, remove) == pytest.approx(1.0)
    assert all(v in "rx" for v in seen["remove"] + [a for a, _ in seen["change"]])  # tree1 vertices
    assert all(v in "ry" for v in seen["insert"] + [b for _, b in seen["change"]])  # tree2 vertices
    assert seen["change"] and seen["remove"] and seen["insert"]


def test_tree_edit_distance_errors():
    t = labelled_tree("rx", [("r", "x")])
    with pytest.raises(jg.GraphError):
        jg.tree_edit_distance(t, labelled_tree("ab", []), "r", "a")  # not a tree

    def boom(*args):
        raise KeyError("cost failed")

    with pytest.raises(KeyError, match="cost failed"):
        jg.tree_edit_distance(t, t, "r", "r", change_cost=boom)


@pytest.mark.parametrize("sparse", [False, True], ids=["Graph", "SparseGraph"])
def test_tree_edit_distance_on_both_graph_classes(sparse):
    path3 = build(3, [(0, 1), (1, 2)], sparse=sparse)
    star = build(3, [(0, 1), (0, 2)], sparse=sparse)
    assert jg.tree_edit_distance(path3, path3, 0, 0) == 0.0
    assert jg.tree_edit_distance(path3, star, 0, 0) >= 0.0


# ------------------------------------------------------------ k-center, densest subgraph


@both
def test_k_center(sparse):
    g = build(5, [(i, i + 1) for i in range(4)], sparse=sparse)  # a path: optimal radius 1
    centers, radius = jg.k_center(g, 2)
    assert len(set(centers)) == 2
    d = {c: jg.single_source_distances(g, c, "bfs") for c in centers}
    assert radius == max(min(d[c][v] for c in centers) for v in range(5))
    assert radius <= 2 * 1  # a 2-approximation of the optimum
    assert jg.k_center(g, 5)[1] == 0.0  # every vertex its own center
    for bad in (0, 6):
        with pytest.raises(jg.GraphError):
            jg.k_center(g, bad)


@both
def test_densest_subgraph(sparse):
    g = build(7, K4A + [(3, 4), (4, 5), (5, 6)], sparse=sparse)  # K4 with a tail
    vertices, density = jg.densest_subgraph(g)
    assert set(vertices) == {0, 1, 2, 3} and density == pytest.approx(1.5)


# ------------------------------------------------------------ perfect / weakly chordal graphs


def cycle(n):
    return [(i, (i + 1) % n) for i in range(n)]


@both
def test_perfect_and_weakly_chordal(sparse):
    c4, c5, c6, k4 = (build(n, e, sparse=sparse) for n, e in ((4, cycle(4)), (5, cycle(5)), (6, cycle(6)), (4, K4A)))
    assert jg.is_perfect(c4) and jg.is_perfect(k4) and jg.is_perfect(c6)
    assert not jg.is_perfect(c5)
    assert sorted(jg.odd_hole_or_antihole(c5)) == [0, 1, 2, 3, 4]
    assert jg.odd_hole_or_antihole(c4) is None
    assert jg.is_weakly_chordal(c4) and jg.is_weakly_chordal(k4)
    assert not jg.is_weakly_chordal(c5) and not jg.is_weakly_chordal(c6)
    assert sorted(jg.weak_chordality_certificate(c6)) == list(range(6))
    assert jg.weak_chordality_certificate(k4) is None


# ------------------------------------------------------------ tree decomposition


def check_decomposition(g, bags, tree_edges):
    n = len(g)
    assert set(v for b in bags for v in b) == set(g.vertices())  # every vertex is in some bag
    for e in g.edges():  # every edge lies inside a bag
        u, v = g.edge_source(e), g.edge_target(e)
        assert any(u in b and v in b for b in bags)
    assert len(tree_edges) == len(bags) - 1  # the bags form a tree...
    t = build(len(bags), tree_edges, sparse=False)
    assert jg.is_tree(t)
    for v in g.vertices():  # ...and the bags containing a vertex are connected in it
        holding = [i for i, b in enumerate(bags) if v in b]
        sub = [(a, b) for a, b in tree_edges if a in holding and b in holding]
        assert len(sub) == len(holding) - 1


@both
@pytest.mark.parametrize("heuristic", ["min_fill", "min_degree"])
@pytest.mark.parametrize(
    "n,edges,width",
    [(4, cycle(4), 2), (5, [(i, i + 1) for i in range(4)], 1), (4, K4A, 3)],
    ids=["cycle", "path", "K4"],
)
def test_tree_decomposition(sparse, heuristic, n, edges, width):
    g = build(n, edges, sparse=sparse)
    bags, tree_edges = jg.tree_decomposition(g, heuristic)
    check_decomposition(g, bags, tree_edges)
    assert max(len(b) for b in bags) - 1 == width
    assert jg.treewidth(g) == width


@both
def test_tree_decomposition_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.tree_decomposition(build(3, [(0, 1)], sparse=sparse), "nope")


# ------------------------------------------------------------ layouts


@both
def test_circular_layout(sparse):
    g = build(6, cycle(6), sparse=sparse)
    pos = jg.circular_layout(g, radius=2.0)
    assert sorted(pos) == list(range(6))
    for x, y in pos.values():
        assert math.hypot(x, y) == pytest.approx(2.0)
    assert len(set(pos.values())) == 6  # distinct points


@both
def test_random_and_force_directed_layouts(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    for layout in (jg.random_layout, jg.fruchterman_reingold_layout):
        pos = layout(g, width=4.0, height=2.0, seed=5)
        assert sorted(pos) == list(range(8))
        assert all(0.0 <= x <= 4.0 and 0.0 <= y <= 2.0 for x, y in pos.values())
        assert pos == layout(g, width=4.0, height=2.0, seed=5)  # reproducible
        assert pos != layout(g, width=4.0, height=2.0, seed=6)
    pos = jg.fruchterman_reingold_layout(g, iterations=200, seed=2)
    near = [math.dist(pos[u], pos[v]) for u, v in K4A]
    far = [math.dist(pos[u], pos[v]) for u, v in itertools.product(range(4), range(4, 8))]
    assert sum(near) / len(near) < sum(far) / len(far)  # clusters pull together
    assert jg.circular_layout(build(0, [], sparse=sparse)) == {}


# ------------------------------------------------------------ minimum cost flow


MCF_EDGES = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]  # edge ids 0..4
MCF_CAP = {0: 3, 1: 3, 2: 2, 3: 4, 4: 2}
MCF_COST = {0: 1, 1: 2, 2: 1, 3: 1, 4: 1}


def check_flow(g, f, supply):
    for v in g.vertices():  # conservation: out - in == supply
        out = sum(f.flow[e] for e in g.out_edges_of(v))
        inn = sum(f.flow[e] for e in g.in_edges_of(v))
        assert out - inn == pytest.approx(supply.get(v, 0))
    for e, x in f.flow.items():
        assert -1e-9 <= x <= MCF_CAP[e] + 1e-9


@both
def test_minimum_cost_flow(sparse):
    g = build(4, MCF_EDGES, directed=True, sparse=sparse)
    supply = {0: 4, 3: -4}
    f = jg.minimum_cost_flow(g, supply, MCF_CAP, MCF_COST)
    assert isinstance(f, jg.MinimumCostFlow)
    assert f.cost == pytest.approx(10.0)
    assert f.cost == pytest.approx(sum(f.flow[e] * MCF_COST[e] for e in f.flow))
    assert set(f.flow) == set(range(5)) and set(f.dual) == set(range(4))
    check_flow(g, f, supply)


@both
def test_minimum_cost_flow_accepts_callables_constants_and_weights(sparse):
    g = build(4, MCF_EDGES, [float(MCF_COST[e]) for e in range(5)], directed=True, sparse=sparse)
    supply = lambda v: {0: 4, 3: -4}.get(v, 0)
    by_weight = jg.minimum_cost_flow(g, supply, lambda e: MCF_CAP[e])  # cost = edge weights
    explicit = jg.minimum_cost_flow(g, {0: 4, 3: -4}, MCF_CAP, MCF_COST)
    assert by_weight.cost == pytest.approx(explicit.cost) == pytest.approx(10.0)
    assert jg.minimum_cost_flow(g, {0: 1, 3: -1}, 10, 1).cost == pytest.approx(2.0)  # constants
    lo = jg.minimum_cost_flow(g, {0: 4, 3: -4}, MCF_CAP, MCF_COST, lower_bound={4: 1})
    assert lo.flow[4] >= 1 and lo.cost >= explicit.cost - 1e-9


@both
def test_minimum_cost_flow_errors(sparse):
    g = build(4, MCF_EDGES, directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError):  # supplies do not balance
        jg.minimum_cost_flow(g, {0: 4, 3: -3}, MCF_CAP, MCF_COST)
    with pytest.raises(jg.GraphError):  # more supply than the network can carry
        jg.minimum_cost_flow(g, {0: 20, 3: -20}, MCF_CAP, MCF_COST)
    with pytest.raises(jg.GraphError, match="integer"):
        jg.minimum_cost_flow(g, {0: 1, 3: -1}, {e: 1.5 for e in range(5)}, MCF_COST)
    with pytest.raises(jg.GraphError):  # undirected
        jg.minimum_cost_flow(build(2, [(0, 1)], sparse=sparse), {0: 1, 1: -1}, 5, 1)


# ------------------------------------------------------------ layout_2d and rescale_layout


@both
def test_layout_2d_circular_random_and_force_directed(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    for alg in ("circular", "random", "fruchterman_reingold"):
        pos = jg.layout_2d(g, alg, area=(0, 0, 4, 2), seed=3)
        assert sorted(pos) == list(range(8))
        assert all(isinstance(x, float) and isinstance(y, float) for x, y in pos.values())
    for alg in ("random", "fruchterman_reingold"):
        a = jg.layout_2d(g, alg, seed=5)
        assert a == jg.layout_2d(g, alg, seed=5) and a != jg.layout_2d(g, alg, seed=6)
    ring = jg.layout_2d(g, "circular", area=(0, 0, 10, 10), radius=2.0)
    centre = (sum(x for x, _ in ring.values()) / 8, sum(y for _, y in ring.values()) / 8)
    assert all(math.dist(p, centre) == pytest.approx(2.0) for p in ring.values())
    with pytest.raises(jg.GraphError, match="radius"):
        jg.layout_2d(g, "circular", radius=2.0)  # does not fit the default unit square


@both
def test_layout_2d_barnes_hut_and_initial_positions(sparse):
    g = build(8, TWO_CLIQUES, sparse=sparse)
    fast = jg.layout_2d(g, "fruchterman_reingold", theta=0.5, seed=1, iterations=60)
    assert sorted(fast) == list(range(8))
    start = {v: (float(v), 0.0) for v in range(8)}
    placed = jg.layout_2d(g, "fruchterman_reingold", seed=1, iterations=0, initial_positions=start)
    assert placed == start  # zero iterations keep the initial positions
    with pytest.raises(jg.GraphError):
        jg.layout_2d(g, "fruchterman_reingold", theta=2.0)


@both
@pytest.mark.parametrize("order", ["plain", "median", "barycenter"])
def test_layout_2d_bipartite(sparse, order):
    g = build(5, [(0, 3), (0, 4), (1, 3), (2, 4)], sparse=sparse)
    pos = jg.layout_2d(g, "bipartite", area=(0, 0, 10, 10), order=order)
    layer = {v: pos[v][0] for v in pos}  # vertical layout: a layer shares an x coordinate
    assert len({layer[0], layer[1], layer[2]}) == 1 and len({layer[3], layer[4]}) == 1
    assert layer[0] != layer[3]
    flat = jg.layout_2d(g, "bipartite", vertical=False, first_partition=[3, 4])
    assert len({flat[3][1], flat[4][1]}) == 1 and flat[3][1] != flat[0][1]
    with pytest.raises(jg.GraphError):
        jg.layout_2d(g, "bipartite", order="nope")
    triangle = build(3, [(0, 1), (1, 2), (0, 2)], sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.layout_2d(triangle, "bipartite")


@both
def test_layout_2d_errors(sparse):
    with pytest.raises(jg.GraphError):
        jg.layout_2d(build(3, [(0, 1)], sparse=sparse), "nope")


@both
def test_rescale_layout(sparse):
    g = build(4, cycle(4), sparse=sparse)
    pos = {0: (10.0, 10.0), 1: (30.0, 10.0), 2: (30.0, 20.0), 3: (10.0, 20.0)}
    out = jg.rescale_layout(g, pos, scale=2.0, area=(0, 0, 4, 4))
    xs = [x for x, _ in out.values()]
    ys = [y for _, y in out.values()]
    assert (min(xs) + max(xs)) / 2 == pytest.approx(2.0) and (min(ys) + max(ys)) / 2 == pytest.approx(2.0)
    assert max(max(abs(x - 2.0) for x in xs), max(abs(y - 2.0) for y in ys)) == pytest.approx(2.0)
    with pytest.raises(jg.GraphError):
        jg.rescale_layout(g, pos, scale=0.0)
