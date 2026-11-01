import itertools

import pytest

import jgrapht as jg
from helpers import both, build

N = 6
K6 = list(itertools.combinations(range(N), 2))


def dist(u, v):
    """Distances of points on a line: a metric, so the metric TSP heuristics apply."""
    return float(abs(u - v))


K6_W = [dist(u, v) for u, v in K6]
ALL_UNDIRECTED = [
    "nearest_neighbor",
    "nearest_insertion",
    "farthest_insertion",
    "random",
    "greedy",
    "two_approx",
    "christofides",
    "two_opt",
]


def check_tour(g, tour, n=N):
    assert tour.vertices[0] == tour.vertices[-1]
    assert sorted(tour.vertices[:-1]) == list(range(n))  # every vertex exactly once
    assert len(tour) == n
    assert tour.weight == pytest.approx(sum(g.edge_weight(e) for e in tour.edges))
    for e, u, v in zip(tour.edges, tour.vertices, tour.vertices[1:]):
        assert {g.edge_source(e), g.edge_target(e)} == {u, v}


@both
def test_held_karp_is_optimal(sparse):
    g = build(N, K6, K6_W, sparse=sparse)
    tour = jg.traveling_salesman_tour(g, "held_karp")
    check_tour(g, tour)
    assert tour.weight == 10.0  # out and back along the line: 2 * (N - 1)


@both
@pytest.mark.parametrize("alg", ALL_UNDIRECTED)
def test_heuristics_produce_valid_tours(sparse, alg):
    g = build(N, K6, K6_W, sparse=sparse)
    tour = jg.traveling_salesman_tour(g, alg, seed=3)
    check_tour(g, tour)
    assert tour.weight >= 10.0  # never better than the optimum
    if alg in ("two_approx", "christofides"):
        assert tour.weight <= 2 * 10.0  # metric approximation guarantees
    if alg == "christofides":
        assert tour.weight <= 1.5 * 10.0


@both
@pytest.mark.parametrize("alg", ["nearest_neighbor", "random", "two_opt"])
def test_seed_makes_randomized_tours_reproducible(sparse, alg):
    g = build(N, K6, K6_W, sparse=sparse)
    a = jg.traveling_salesman_tour(g, alg, seed=11)
    b = jg.traveling_salesman_tour(g, alg, seed=11)
    assert a.vertices == b.vertices and a.edges == b.edges


@both
def test_held_karp_on_a_directed_graph(sparse):
    edges = [(u, v) for u in range(4) for v in range(4) if u != v]
    weights = [1.0 if v == (u + 1) % 4 else 10.0 for u, v in edges]
    g = build(4, edges, weights, directed=True, sparse=sparse)
    tour = jg.traveling_salesman_tour(g, "held_karp")
    assert tour.weight == 4.0 and tour.vertices[:-1] in ([0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2])


@both
def test_tour_algorithm_errors(sparse):
    g = build(N, K6, K6_W, sparse=sparse)
    with pytest.raises(jg.GraphError):
        jg.traveling_salesman_tour(g, "nope")
    d = build(3, [(0, 1), (1, 2), (2, 0)], [1.0] * 3, directed=True, sparse=sparse)
    with pytest.raises(jg.GraphError, match="undirected"):
        jg.traveling_salesman_tour(d, "nearest_neighbor")


@both
def test_graph_without_a_tour(sparse):
    path = build(3, [(0, 1), (1, 2)], [1.0, 1.0], sparse=sparse)
    assert jg.traveling_salesman_tour(path, "held_karp") is None


# ------------------------------------------------------------ Hamiltonian cycles and paths


def test_hamiltonian_cycle():
    # Palmer's algorithm needs a simple graph with Ore's property (here: the complete graph K5)
    edges = list(itertools.combinations(range(5), 2))
    g = build(5, edges, multi=False, loops=False)
    cycle = jg.hamiltonian_cycle(g)
    check_tour(g, cycle, 5)


def test_hamiltonian_cycle_preconditions():
    edges = list(itertools.combinations(range(5), 2))
    # not declared simple (Graph allowing parallel edges / loops) and SparseGraph: rejected
    for g in (build(5, edges), build(5, edges, sparse=True)):
        with pytest.raises(jg.GraphError):
            jg.hamiltonian_cycle(g)
    # simple but without Ore's property
    path = build(5, [(0, 1), (1, 2), (2, 3), (3, 4)], multi=False, loops=False)
    with pytest.raises(jg.GraphError, match="Ore"):
        jg.hamiltonian_cycle(path)


@both
@pytest.mark.parametrize("alg", ["held_karp", "backtracking"])
def test_hamiltonian_path(sparse, alg):
    g = build(5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2)], sparse=sparse)
    p = jg.hamiltonian_path(g, alg)
    assert sorted(p.vertices) == [0, 1, 2, 3, 4] and len(p) == 4
    star = build(4, [(0, 1), (0, 2), (0, 3)], sparse=sparse)
    assert jg.hamiltonian_path(star, alg) is None


@both
def test_hamiltonian_path_in_a_dag(sparse):
    g = build(4, [(0, 1), (1, 2), (2, 3), (0, 2)], directed=True, sparse=sparse)
    assert jg.hamiltonian_path(g, "dag").vertices == [0, 1, 2, 3]
    assert jg.hamiltonian_path(build(3, [(0, 1), (0, 2)], directed=True, sparse=sparse), "dag") is None
    with pytest.raises(jg.GraphError):
        jg.hamiltonian_path(g, "nope")
