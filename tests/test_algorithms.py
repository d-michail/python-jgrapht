import math

import pytest

import jgrapht as jg


def make(edges, directed=False, weights=None, sparse=False, n=None):
    if sparse:
        return jg.SparseGraph(n, edges, directed=directed, weights=weights)
    g = jg.Graph(directed=directed, weighted=weights is not None)
    for v in range(n):
        g.add_vertex(v)
    for i, (u, v) in enumerate(edges):
        g.add_edge(u, v, weight=None if weights is None else weights[i])
    return g


both = pytest.mark.parametrize("sparse", [False, True])


@both
@pytest.mark.parametrize("alg", ["bellman_ford", "floyd_warshall", "johnson"])
def test_negative_weights(sparse, alg):
    g = make([(0, 1), (1, 2), (0, 2)], directed=True, weights=[4.0, -2.0, 3.0], sparse=sparse, n=3)
    p = jg.shortest_path(g, 0, 2, algorithm=alg)
    assert p.vertices == [0, 1, 2] and p.weight == 2.0
    assert jg.single_source_distances(g, 0, algorithm=alg) == {0: 0.0, 1: 4.0, 2: 2.0}


@both
def test_negative_cycle(sparse):
    g = make([(0, 1), (1, 0)], directed=True, weights=[1.0, -3.0], sparse=sparse, n=2)
    with pytest.raises(jg.GraphError):
        jg.shortest_path(g, 0, 1, algorithm="bellman_ford")


def test_unknown_algorithm_and_missing_vertex():
    g = make([(0, 1)], sparse=False, n=2)
    with pytest.raises(jg.GraphError):
        jg.shortest_path(g, 0, 1, algorithm="nope")
    with pytest.raises(jg.GraphError):
        jg.coloring(g, "nope")


@both
@pytest.mark.parametrize("alg", ["floyd_warshall", "johnson"])
def test_all_pairs(sparse, alg):
    g = make([(0, 1), (1, 2)], directed=True, weights=[1.0, 2.0], sparse=sparse, n=3)
    d = jg.all_pairs_distances(g, alg)
    assert d == {0: {0: 0.0, 1: 1.0, 2: 3.0}, 1: {1: 0.0, 2: 2.0}, 2: {2: 0.0}}


TRIANGLE_TAIL = [(0, 1), (1, 2), (0, 2), (2, 3)]


@both
def test_centrality(sparse):
    g = make(TRIANGLE_TAIL, sparse=sparse, n=4)
    assert jg.degree_centrality(g) == {0: 2, 1: 2, 2: 3, 3: 1}
    bc = jg.betweenness_centrality(g, normalize=False)
    assert bc[2] == 2.0 and bc[0] == 0.0
    ebc = jg.edge_betweenness_centrality(g, normalize=False)
    assert set(ebc) == set(g.edges()) and max(ebc.values()) == ebc[3]
    cl = jg.closeness_centrality(g)
    assert cl[2] == max(cl.values())
    assert jg.harmonic_centrality(g)[2] == max(jg.harmonic_centrality(g).values())
    pr = jg.pagerank(g)
    assert math.isclose(sum(pr.values()), 1.0, rel_tol=1e-6) and pr[2] == max(pr.values())
    assert jg.eigenvector_centrality(g)[2] == max(jg.eigenvector_centrality(g).values())
    assert jg.katz_centrality(g)[2] == max(jg.katz_centrality(g).values())
    assert jg.coreness(g) == {0: 2, 1: 2, 2: 2, 3: 1}


@both
def test_clustering(sparse):
    g = make(TRIANGLE_TAIL, sparse=sparse, n=4)
    assert jg.count_triangles(g) == 1
    lc = jg.local_clustering_coefficients(g)
    assert lc[0] == 1.0 and math.isclose(lc[2], 1 / 3) and lc[3] == 0.0
    assert math.isclose(jg.global_clustering_coefficient(g), 3 / 5)
    assert math.isclose(jg.average_clustering_coefficient(g), (1 + 1 + 1 / 3) / 4)


@both
@pytest.mark.parametrize(
    "alg", ["greedy", "largest_degree_first", "smallest_degree_last", "saturation_degree"]
)
def test_coloring(sparse, alg):
    g = make(TRIANGLE_TAIL, sparse=sparse, n=4)
    k, colors = jg.coloring(g, alg)
    assert k == 3 and set(colors) == {0, 1, 2, 3}
    assert all(colors[u] != colors[v] for u, v in TRIANGLE_TAIL)


@both
def test_cliques_independent_cover(sparse):
    g = make(TRIANGLE_TAIL, sparse=sparse, n=4)
    assert sorted(sorted(c) for c in jg.maximal_cliques(g)) == [[0, 1, 2], [2, 3]]
    assert sorted(jg.maximum_clique(g)) == [0, 1, 2]
    ind = jg.maximum_independent_set(g)
    assert len(ind) == 2 and not (ind[0] in (0, 1, 2) and ind[1] in (0, 1, 2))
    assert len(jg.greedy_independent_set(g)) >= 2
    for alg in ["greedy", "two_approximation"]:
        size, cover = jg.vertex_cover(g, alg)
        assert size == len(cover)
        assert all(u in cover or v in cover for u, v in TRIANGLE_TAIL)


@both
def test_bipartite_dag(sparse):
    path = make([(0, 1), (1, 2), (2, 3)], sparse=sparse, n=4)
    assert jg.is_bipartite(path)
    left, right = jg.bipartite_partition(path)
    assert sorted(left + right) == [0, 1, 2, 3] and len(left) == 2
    assert not jg.is_bipartite(make(TRIANGLE_TAIL, sparse=sparse, n=4))
    assert jg.bipartite_partition(make(TRIANGLE_TAIL, sparse=sparse, n=4)) is None

    dag = make([(0, 1), (1, 2), (0, 2)], directed=True, sparse=sparse, n=3)
    assert jg.is_dag(dag) and jg.topological_sort(dag) == [0, 1, 2]
    cyc = make([(0, 1), (1, 0)], directed=True, sparse=sparse, n=2)
    assert not jg.is_dag(cyc) and jg.topological_sort(cyc) is None
    with pytest.raises(jg.GraphError):
        jg.is_dag(path)


@both
@pytest.mark.parametrize("alg", ["dinic", "edmonds_karp", "push_relabel"])
def test_maximum_flow(sparse, alg):
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]
    g = make(edges, directed=True, weights=[3.0, 2.0, 2.0, 3.0, 1.0], sparse=sparse, n=4)
    f = jg.maximum_flow(g, 0, 3, algorithm=alg)
    assert f.value == 5.0
    assert set(f.flow) == set(g.edges())
    assert 0 in f.source_partition and 3 not in f.source_partition
    out = sum(f.flow[e] for e in g.out_edges_of(0))
    assert out == 5.0
    with pytest.raises(jg.GraphError):
        jg.maximum_flow(g, 0, 0)

