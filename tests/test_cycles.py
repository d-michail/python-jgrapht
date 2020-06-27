import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cycles as cycles


def test_hierholzer():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)

    cycle = cycles.eulerian_cycle(g)

    assert cycle is not None
    assert cycle.edges == [3, 0, 1, 2]

    g.add_edge(0, 2)
    cycle = cycles.eulerian_cycle(g)
    assert cycle is None



def test_anyhashableg_hierholzer():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3])
    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)

    cycle = cycles.eulerian_cycle(g)

    assert cycle is not None
    assert cycle.edges == [3, 0, 1, 2]


def test_chinese_postman():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(3, 4)

    closed_walk = cycles.chinese_postman(g)

    assert closed_walk is not None
    assert closed_walk.edges == [4, 3, 0, 1, 2, 4]


def test_anyhashableg_chinese_postman():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4])
    g.add_edge(0, 1, edge='0')
    g.add_edge(1, 2, edge='1')
    g.add_edge(2, 3, edge='2')
    g.add_edge(3, 0, edge='3')
    g.add_edge(3, 4, edge='4')

    closed_walk = cycles.chinese_postman(g)

    assert closed_walk is not None
    assert closed_walk.edges == ['4', '3', '0', '1', '2', '4']


def test_fundamental_cycle_basis_paton():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_paton(g)

    assert fcb_weight == 8.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [1, 2, 3, 0]
    assert cycle2.edges == [4, 5, 6, 1]


def test_anyhashableg_fundamental_cycle_basis_paton():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_paton(g)

    assert fcb_weight == 8.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [1, 2, 3, 0]
    assert cycle2.edges == [4, 5, 6, 1]


def test_fundamental_cycle_basis_queuebfs():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_bfs_with_queue(g)

    assert fcb_weight == 8.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [0, 1, 2, 3]
    assert cycle2.edges == [4, 5, 6, 1]


def test_fundamental_cycle_basis_stackbfs():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_bfs_with_stack(g)

    assert fcb_weight == 10.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [0, 1, 2, 3]
    assert cycle2.edges == [0, 4, 5, 6, 2, 3]


def test_simple_cycles_tiernan():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    it = cycles.enumerate_simple_cycles_tiernan(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_anyhashableg_simple_cycles_tiernan():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    it = cycles.enumerate_simple_cycles_tiernan(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_simple_cycles_johnson():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    it = cycles.enumerate_simple_cycles_johnson(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_simple_cycles_tarjan():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    it = cycles.enumerate_simple_cycles_tarjan(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_simple_cycles_szwarcfiter_lauer():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    it = cycles.enumerate_simple_cycles_szwarcfiter_lauer(g)

    cycle1 = next(it)
    assert list(cycle1) == [2, 3, 0, 1]
    cycle2 = next(it)
    assert list(cycle2) == [2, 3, 0, 1, 4, 5]

    with pytest.raises(StopIteration):
        next(it)


def test_simple_cycles_hawick_james():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(1, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    it = cycles.enumerate_simple_cycles_hawick_james(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_anyhashableg_fundamental_cycle_basis_queuebfs():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_bfs_with_queue(g)

    assert fcb_weight == 8.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [0, 1, 2, 3]
    assert cycle2.edges == [4, 5, 6, 1]


def test_anyhashableg_fundamental_cycle_basis_stackbfs():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])
    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    fcb_weight, fcb_it = cycles.fundamental_cycle_basis_bfs_with_stack(g)

    assert fcb_weight == 10.0
    cycle1 = next(fcb_it)
    cycle2 = next(fcb_it)
    with pytest.raises(StopIteration):
        next(fcb_it)

    assert cycle1.edges == [0, 1, 2, 3]
    assert cycle2.edges == [0, 4, 5, 6, 2, 3]



def test_anyhashableg_simple_cycles_johnson():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    it = cycles.enumerate_simple_cycles_johnson(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_anyhashableg_simple_cycles_tarjan():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    it = cycles.enumerate_simple_cycles_tarjan(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)


def test_anyhashableg_simple_cycles_szwarcfiter_lauer():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    it = cycles.enumerate_simple_cycles_szwarcfiter_lauer(g)

    cycle1 = next(it)
    assert list(cycle1) == [2, 3, 0, 1]
    cycle2 = next(it)
    assert list(cycle2) == [2, 3, 0, 1, 4, 5]

    with pytest.raises(StopIteration):
        next(it)


def test_anyhashableg_simple_cycles_hawick_james():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5])

    g.add_edge(0, 1, edge=0)
    g.add_edge(1, 2, edge=1)
    g.add_edge(2, 3, edge=2)
    g.add_edge(3, 0, edge=3)
    g.add_edge(1, 4, edge=4)
    g.add_edge(4, 5, edge=5)
    g.add_edge(5, 2, edge=6)

    it = cycles.enumerate_simple_cycles_hawick_james(g)

    cycle1 = next(it)
    assert list(cycle1) == [0, 1, 2, 3]
    cycle2 = next(it)
    assert list(cycle2) == [0, 1, 4, 5, 2, 3]

    with pytest.raises(StopIteration):
        next(it)
