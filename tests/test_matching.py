import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier

import jgrapht.algorithms.matching as matching
import jgrapht.algorithms.partition as partition
import jgrapht.generators as generators


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bipartite_max_cardinality(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    for i in range(0, 6):
        g.add_vertex(i)

    e03 = g.add_edge(0, 3)
    e13 = g.add_edge(1, 3)
    g.add_edge(2, 3)
    e14 = g.add_edge(1, 4)
    e25 = g.add_edge(2, 5)
    g.set_edge_weight(e13, 15.0)

    weight, m = matching.bipartite_max_cardinality(g)
    assert weight == 3.0
    assert set(m) == set([e03, e14, e25])

    weight, m = matching.bipartite_max_weight(g)
    assert weight == 16.0
    assert set(m) == set([e13, e25])


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bipartite_perfect_min_weight(backend):
    bg = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.complete_bipartite_graph(bg, 10, 10)
    _, part1, part2 = partition.bipartite_partitions(bg)
    weight, _ = matching.bipartite_perfect_min_weight(bg, part1, part2)

    assert weight == 10.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bipartite_perfect_min_weight_with_custom_partitions(backend):
    bg = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    bg.add_vertices_from([0, 1, 2, 3, 4, 5, 6, 7])

    part1 = set([0, 1, 2, 3])
    part2 = set([4, 5, 6, 7])

    for v in part1:
        for u in part2:
            bg.add_edge(v, u)

    weight, _ = matching.bipartite_perfect_min_weight(bg, part1, part2)

    assert weight == 4.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_bipartite_perfect_min_weight_with_custom_partitions(backend):
    bg = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    bg.add_vertices_from(["0", "1", "2", "3", "4", "5", "6", "7"])

    part1 = set(["0", "1", "2", "3"])
    part2 = set(["4", "5", "6", "7"])

    for v in part1:
        for u in part2:
            bg.add_edge(v, u)

    weight, _ = matching.bipartite_perfect_min_weight(bg, part1, part2)

    assert weight == 4.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_greedy_max_cardinality(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.greedy_max_cardinality(g)

    assert weight == 42.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_greedy_max_cardinality_with_sort(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.greedy_max_cardinality(g, sort=True)

    assert weight == 49.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_edmonds_max_cardinality(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.edmonds_max_cardinality(g)

    assert weight == 50.0

    weight, _ = matching.edmonds_max_cardinality(g, dense=True)

    assert weight == 50.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_greedy_max_weight(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.greedy_max_weight(g)

    assert weight == 41.0

    weight, _ = matching.greedy_max_weight(g, normalize_edge_costs=True)

    assert weight == 49.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_pathgrowing_max_weight(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.pathgrowing_max_weight(g)

    assert weight == 41.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_blossom5_max_weight(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.blossom5_max_weight(g)

    assert weight == 50.0

    weight, _ = matching.blossom5_max_weight(g, perfect=True)

    assert weight == 50.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_blossom5_min_weight(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.barabasi_albert(g, 5, 5, 100, seed=17)

    weight, _ = matching.blossom5_min_weight(g)

    assert weight == 0.0

    weight, _ = matching.blossom5_min_weight(g, perfect=True)

    assert weight == 50.0


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_bipartite_perfect_min_weight(backend):
    bg = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    generators.complete_bipartite_graph(bg, 10, 10)
    _, part1, part2 = partition.bipartite_partitions(bg)
    weight, _ = matching.bipartite_perfect_min_weight(bg, part1, part2)

    assert weight == 10.0