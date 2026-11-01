import decimal
import itertools
import random

import pytest

import jgrapht as jg
from helpers import both, build


def complete(n, weight=lambda u, v: float(abs(u - v)), sparse=False):
    edges = list(itertools.combinations(range(n), 2))
    return build(n, edges, [weight(u, v) for u, v in edges], sparse=sparse), edges


# ------------------------------------------------------------ capacitated spanning trees


def check_capacitated(g, tree, root, capacity, demand=lambda v: 1):
    n = len(g)
    assert len(tree.edges) == n - 1
    assert tree.weight == pytest.approx(sum(g.edge_weight(e) for e in tree.edges))
    groups = [set(vs) for vs, _ in tree.partition]
    assert sorted(v for grp in groups for v in grp) == sorted(set(range(n)) - {root})
    for (vs, total), index in zip(tree.partition, range(len(tree.partition))):
        assert total == pytest.approx(sum(demand(v) for v in vs)) and total <= capacity
        assert all(tree.labels[v] == index for v in vs)
    # removing the root from the tree leaves exactly the partition's subtrees as components
    adjacency = {v: set() for v in range(n)}
    for e in tree.edges:
        u, v = g.edge_source(e), g.edge_target(e)
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen, components = {root}, []
    for start in range(n):
        if start in seen:
            continue
        comp, stack = set(), [start]
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack += [y for y in adjacency[x] if y != root and y not in comp]
        seen |= comp
        components.append(comp)
    assert sorted(map(sorted, components)) == sorted(map(sorted, groups))


@both
@pytest.mark.parametrize("alg", ["esau_williams", "ahuja_orlin_sharma"])
def test_capacitated_minimum_spanning_tree(sparse, alg):
    g, _ = complete(8, sparse=sparse)
    tree = jg.capacitated_minimum_spanning_tree(g, 0, 3.0, 1, alg, number_of_operations=3, seed=1)
    assert isinstance(tree, jg.CapacitatedSpanningTree)
    check_capacitated(g, tree, 0, 3.0)
    assert len(tree.partition) >= 3  # 7 unit-demand customers, capacity 3


@both
def test_capacitated_demands_and_reproducibility(sparse):
    g, _ = complete(7, sparse=sparse)
    demand = lambda v: float(v % 3 + 1)
    for spec in (demand, {v: demand(v) for v in range(7)}):
        tree = jg.capacitated_minimum_spanning_tree(g, 0, 4.0, spec, seed=2, number_of_operations=2)
        check_capacitated(g, tree, 0, 4.0, demand)
    a = jg.capacitated_minimum_spanning_tree(g, 0, 4.0, demand, seed=9, number_of_operations=2)
    b = jg.capacitated_minimum_spanning_tree(g, 0, 4.0, demand, seed=9, number_of_operations=2)
    assert a.edges == b.edges and a.weight == b.weight


@both
def test_capacitated_options_and_errors(sparse):
    g, _ = complete(6, sparse=sparse)
    for kwargs in (
        dict(use_tabu_search=False),
        dict(best_improvement=True, length_bound=2),
        dict(use_vertex_operation=False, use_subtree_operation=True),
    ):
        tree = jg.capacitated_minimum_spanning_tree(g, 0, 2.0, 1, "ahuja_orlin_sharma", **kwargs)
        check_capacitated(g, tree, 0, 2.0)
    with pytest.raises(jg.GraphError):  # a vertex demands more than the capacity
        jg.capacitated_minimum_spanning_tree(g, 0, 0.5, 1)
    with pytest.raises(jg.GraphError):
        jg.capacitated_minimum_spanning_tree(g, 0, 3.0, 1, "nope")
    with pytest.raises(jg.GraphError):
        jg.capacitated_minimum_spanning_tree(g, 99, 3.0, 1)
    with pytest.raises(jg.GraphError):
        jg.capacitated_minimum_spanning_tree(
            g, 0, 3.0, 1, "ahuja_orlin_sharma", use_vertex_operation=False, use_subtree_operation=False
        )


@both
def test_cyclic_exchange_augmentation(sparse):
    g = build(3, [(0, 1), (1, 2), (2, 0)], [1.0, 1.0, -5.0], directed=True, sparse=sparse)
    cycle = jg.cyclic_exchange_augmentation(g, {0: 0, 1: 1, 2: 2}, 3)
    assert cycle.vertices[0] == cycle.vertices[-1] and sorted(cycle.vertices[:-1]) == [0, 1, 2]
    assert cycle.weight == -3.0
    assert jg.cyclic_exchange_augmentation(g, {0: 0, 1: 1, 2: 2}, 3, best_improvement=True).weight == -3.0
    assert jg.cyclic_exchange_augmentation(g, {0: 0, 1: 0, 2: 0}, 3) is None  # labels must differ
    nonneg = build(3, [(0, 1), (1, 2), (2, 0)], [1.0, 1.0, 1.0], directed=True, sparse=sparse)
    assert jg.cyclic_exchange_augmentation(nonneg, {0: 0, 1: 1, 2: 2}, 3) is None
    with pytest.raises(jg.GraphError):
        jg.cyclic_exchange_augmentation(g, {0: 0, 1: 1}, 3)  # a label is missing


# ------------------------------------------------------------ Goldberg and Gon


def brute_force_density(n, edges):
    best = 0.0
    for r in range(1, n + 1):
        for subset in itertools.combinations(range(n), r):
            inside = set(subset)
            count = sum(1 for u, v in edges if u in inside and v in inside)
            best = max(best, count / r)
    return best


@both
def test_goldberg_densest_subgraph(sparse):
    k4 = list(itertools.combinations(range(4), 2))
    g = build(7, k4 + [(3, 4), (4, 5), (5, 6)], sparse=sparse)
    vertices, density = jg.densest_subgraph(g, "goldberg")
    assert sorted(vertices) == [0, 1, 2, 3] and density == pytest.approx(1.5)
    assert jg.densest_subgraph(g)[1] == pytest.approx(1.5)  # greedy finds it too


@both
@pytest.mark.parametrize("seed", range(4))
def test_goldberg_matches_brute_force(sparse, seed):
    rng = random.Random(seed)
    edges = sorted({tuple(sorted(rng.sample(range(8), 2))) for _ in range(14)})
    g = build(8, edges, sparse=sparse)
    vertices, density = jg.densest_subgraph(g, "goldberg", epsilon=1e-9)
    assert density == pytest.approx(brute_force_density(8, edges), abs=1e-6)
    inside = set(vertices)
    assert sum(1 for u, v in edges if u in inside and v in inside) / len(inside) == pytest.approx(density, abs=1e-6)
    greedy = jg.densest_subgraph(g)[1]
    assert greedy <= density + 1e-9 and greedy >= density / 2 - 1e-9  # a 1/2-approximation


@both
def test_goldberg_node_weights_and_errors(sparse):
    k4 = list(itertools.combinations(range(4), 2))
    g = build(7, k4 + [(3, 4), (4, 5), (5, 6)], sparse=sparse)
    assert jg.densest_subgraph(g, "goldberg", node_weights=2.0)[1] == pytest.approx(3.5)
    assert jg.densest_subgraph(g, "goldberg", node_weights={0: 2.0}, per_edge_weight=True)[0]
    assert jg.densest_subgraph(g, "goldberg", node_weights=lambda v: 2.0, per_edge_weight=True)[1] == pytest.approx(0.75)
    with pytest.raises(jg.GraphError):
        jg.densest_subgraph(g, "nope")


@both
def test_gon_k_center(sparse):
    g, _ = complete(8, sparse=sparse)
    centers, assignment, radius = jg.gon_k_center(g, 3, seed=1)
    assert len(set(centers)) == 3 and radius <= 2 * 1.0  # optimum on a line of 8 points is 1
    assert set(assignment) == set(range(8)) - set(centers) and set(assignment.values()) <= set(centers)
    assert all(abs(v - c) <= radius for v, c in assignment.items())
    assert jg.gon_k_center(g, 3, seed=1) == (centers, assignment, radius)  # reproducible
    seeded = jg.gon_k_center(g, 3, initial_centers=[0])
    assert 0 in seeded[0]
    assert jg.gon_k_center(g, 8)[2] == 0.0
    with pytest.raises(jg.GraphError):
        jg.gon_k_center(g, 0)
    with pytest.raises(jg.GraphError):  # not complete
        jg.gon_k_center(build(4, [(0, 1), (1, 2), (2, 3)], [1.0] * 3, sparse=sparse), 2)


# ------------------------------------------------------------ Boykov-Kolmogorov


@both
@pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
@pytest.mark.parametrize("seed", range(3))
def test_boykov_kolmogorov_agrees_with_dinic(sparse, directed, seed):
    rng = random.Random(seed)
    n = 9
    edges = [tuple(rng.sample(range(n), 2)) for _ in range(24)]
    weights = [float(rng.randint(1, 9)) for _ in edges]
    g = build(n, edges, weights, directed=directed, sparse=sparse)
    for s, t in [(0, n - 1), (2, 5)]:
        bk = jg.maximum_flow(g, s, t, "boykov_kolmogorov")
        assert bk.value == pytest.approx(jg.maximum_flow(g, s, t).value)
        cut = jg.minimum_st_cut(g, s, t, "boykov_kolmogorov")
        assert cut.capacity == pytest.approx(bk.value)
        assert s in cut.source_partition and t in cut.sink_partition


# ------------------------------------------------------------ lowest common ancestors


def tree_edges(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(i), i) for i in range(1, n)]  # parent of i is a smaller index


def true_lca(parent, a, b):
    ancestors = set()
    while a is not None:
        ancestors.add(a)
        a = parent.get(a)
    while b not in ancestors:
        b = parent.get(b)
    return b


@both
@pytest.mark.parametrize("alg", ["binary_lifting", "euler_tour", "heavy_path", "tarjan"])
@pytest.mark.parametrize("seed", range(3))
def test_lca_algorithms_agree_with_brute_force(sparse, alg, seed):
    n = 20
    edges = tree_edges(n, seed)
    parent = {v: p for p, v in edges}
    g = build(n, edges, directed=True, sparse=sparse)
    rng = random.Random(seed + 100)
    pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(30)]
    expected = [true_lca(parent, a, b) for a, b in pairs]
    assert jg.lowest_common_ancestors(g, 0, pairs, alg) == expected


@both
@pytest.mark.parametrize("alg", ["binary_lifting", "euler_tour", "heavy_path", "tarjan"])
def test_lca_in_a_forest_and_errors(sparse, alg):
    g = build(6, [(0, 1), (0, 2), (3, 4), (3, 5)], directed=True, sparse=sparse)
    result = jg.lowest_common_ancestors(g, [0, 3], [(1, 2), (4, 5), (1, 4)], alg)
    assert result[:2] == [0, 3] and result[2] is None  # different trees have no common ancestor
    with pytest.raises(jg.GraphError):
        jg.lowest_common_ancestors(g, 99, [(1, 2)], alg)


@both
def test_naive_lca_and_all_lcas_in_a_dag(sparse):
    # a and b are both parents of c and d
    g = build(4, [(0, 2), (0, 3), (1, 2), (1, 3)], directed=True, sparse=sparse)
    assert sorted(jg.all_lowest_common_ancestors(g, 2, 3)) == [0, 1]
    assert jg.lowest_common_ancestors(g, 0, [(2, 3), (2, 2)], "naive")[1] == 2
    assert jg.lowest_common_ancestors(g, 0, [(2, 3)], "naive")[0] in (0, 1)
    assert jg.all_lowest_common_ancestors(g, 0, 1) == []
    with pytest.raises(jg.GraphError):
        jg.lowest_common_ancestors(g, 0, [(2, 3)], "nope")


# ------------------------------------------------------------ more isomorphism


def test_forest_isomorphism():
    f1 = build(5, [(0, 1), (0, 2), (3, 4)], multi=False, loops=False)
    f2 = build(5, [(4, 3), (4, 2), (1, 0)], multi=False, loops=False)
    m = jg.forest_isomorphism(f1, f2, [0, 3], [4, 1])
    assert m is not None and sorted(m) == list(range(5)) and sorted(m.values()) == list(range(5))
    assert m[0] == 4 and m[3] == 1
    assert jg.forest_isomorphism(f1, f2, [0, 3], [1, 4]) is not None  # root order does not matter
    other = build(5, [(0, 1), (1, 2), (3, 4)], multi=False, loops=False)
    assert jg.forest_isomorphism(f1, other, [0, 3], [1, 3]) is not None  # a path rooted at its middle
    assert jg.forest_isomorphism(f1, other, [0, 3], [0, 3]) is None  # rooted at an end it is not


def test_color_refinement_isomorphism():
    p4 = build(4, [(0, 1), (1, 2), (2, 3)], multi=False, loops=False)
    p4b = build(4, [(2, 0), (0, 3), (3, 1)], multi=False, loops=False)
    decided, mapping = jg.color_refinement_isomorphism(p4, p4b)
    assert decided is True and sorted(mapping.values()) == [0, 1, 2, 3]
    star = build(4, [(0, 1), (0, 2), (0, 3)], multi=False, loops=False)
    assert jg.color_refinement_isomorphism(p4, star) == (False, None)
    assert jg.color_refinement_isomorphism(p4, build(3, [(0, 1), (1, 2)], multi=False, loops=False)) == (False, None)
    c6 = build(6, [(i, (i + 1) % 6) for i in range(6)], multi=False, loops=False)
    two_triangles = build(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)], multi=False, loops=False)
    assert jg.color_refinement_isomorphism(c6, two_triangles) == (None, None)  # refinement cannot decide


# ------------------------------------------------------------ Blossom V options, weighted matching


def brute_force_matching_weight(n, edges, weights):
    best = 0.0
    for r in range(len(edges) + 1):
        for chosen in itertools.combinations(range(len(edges)), r):
            used = [x for i in chosen for x in edges[i]]
            if len(used) == len(set(used)):
                best = max(best, sum(weights[i] for i in chosen))
    return best


@both
@pytest.mark.parametrize("seed", range(4))
def test_blossom_weighted_matching_is_optimal(sparse, seed):
    rng = random.Random(seed)
    edges = sorted({tuple(sorted(rng.sample(range(7), 2))) for _ in range(11)})
    weights = [float(rng.randint(1, 9)) for _ in edges]
    g = build(7, edges, weights, sparse=sparse)
    best = brute_force_matching_weight(7, edges, weights)
    assert jg.weighted_matching(g, "blossom").weight == pytest.approx(best)
    assert jg.weighted_matching(g, "path_growing").weight >= best / 2 - 1e-9
    assert jg.weighted_matching(g, "greedy").weight >= best / 2 - 1e-9


@both
@pytest.mark.parametrize("initialization", ["greedy", "none", "fractional"])
@pytest.mark.parametrize("dual_update", ["fixed_delta", "connected_components"])
def test_blossom_options_do_not_change_the_optimum(sparse, initialization, dual_update):
    g = build(4, [(0, 1), (1, 2), (2, 3), (3, 0)], [1.0, 4.0, 1.0, 4.0], sparse=sparse)
    kw = dict(initialization=initialization, dual_update=dual_update, update_duals_before=False, update_duals_after=True)
    assert jg.perfect_matching(g, "minimize", **kw).weight == 2.0
    assert jg.perfect_matching(g, "maximize", **kw).weight == 8.0
    assert jg.weighted_matching(g, "blossom", "maximize", **kw).weight == 8.0


@both
def test_blossom_option_errors(sparse):
    g = build(4, [(0, 1), (2, 3)], [1.0, 1.0], sparse=sparse)
    for bad in (dict(initialization="nope"), dict(dual_update="nope")):
        with pytest.raises(jg.GraphError):
            jg.perfect_matching(g, **bad)
    with pytest.raises(jg.GraphError):
        jg.weighted_matching(g, "blossom", "nope")


# ------------------------------------------------------------ exact betweenness


@both
@pytest.mark.parametrize("seed", range(3))
def test_exact_betweenness_matches_the_float_version(sparse, seed):
    rng = random.Random(seed)
    edges = sorted({tuple(sorted(rng.sample(range(8), 2))) for _ in range(13)})
    g = build(8, edges, sparse=sparse)
    exact = jg.exact_betweenness_centrality(g, precision=40)
    floats = jg.betweenness_centrality(g, normalize=False)
    assert set(exact) == set(floats)
    for v, score in exact.items():
        assert isinstance(score, decimal.Decimal)
        assert float(score) == pytest.approx(floats[v])


@both
@pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
def test_exact_betweenness_normalisation_convention(sparse, directed):
    # The exact variant divides by (n-1)(n-2) in both cases; betweenness_centrality divides an
    # undirected graph's scores by half of that, so its normalised scores are twice as large.
    g = build(5, [(0, 1), (1, 2), (2, 3), (3, 4)], directed=directed, sparse=sparse)
    exact = jg.exact_betweenness_centrality(g, normalize=True, precision=30)
    floats = jg.betweenness_centrality(g, normalize=True)
    factor = 1.0 if directed else 2.0
    for v, score in exact.items():
        assert float(score) * factor == pytest.approx(floats[v])


@both
def test_exact_betweenness_details(sparse):
    path = build(3, [(0, 1), (1, 2)], sparse=sparse)
    assert jg.exact_betweenness_centrality(path) == {0: 0, 1: 1, 2: 0}
    # normalising by (n-1)(n-2) = 12 gives a non-terminating decimal that unlimited precision rejects
    square_tail = build(5, [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4)], sparse=sparse)
    with pytest.raises(jg.GraphError, match="terminate"):
        jg.exact_betweenness_centrality(square_tail, normalize=True)
    assert jg.exact_betweenness_centrality(square_tail, precision=20)[3] == decimal.Decimal("3.5")
    with pytest.raises(jg.GraphError):
        jg.exact_betweenness_centrality(path, precision=0)


def test_betweenness_conventions_are_documented_and_different():
    # The two functions deliberately normalise undirected graphs differently: the middle vertex of
    # a path lies on every shortest path, which is 1.0 for the float version and 0.5 for the exact one.
    g = jg.path_graph(5)
    assert jg.betweenness_centrality(g, normalize=True)[2] == pytest.approx(2 / 3)
    assert float(jg.exact_betweenness_centrality(g, normalize=True, precision=20)[2]) == pytest.approx(1 / 3)
    star = jg.star_graph(5)
    assert jg.betweenness_centrality(star, normalize=True)[0] == pytest.approx(1.0)
    assert float(jg.exact_betweenness_centrality(star, normalize=True, precision=20)[0]) == pytest.approx(0.5)
    assert "half" in jg.exact_betweenness_centrality.__doc__


def test_edge_betweenness_ignores_normalize():
    g = jg.path_graph(5)
    assert jg.edge_betweenness_centrality(g, normalize=True) == jg.edge_betweenness_centrality(g, normalize=False)
    assert "no effect" in jg.edge_betweenness_centrality.__doc__
