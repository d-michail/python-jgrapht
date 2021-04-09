import pytest
import math

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.cycles as cycles


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_hierholzer(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_chinese_postman(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_chinese_postman(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_fundamental_cycle_basis_paton(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
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



@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_fundamental_cycle_basis_queuebfs(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),                
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_fundamental_cycle_basis_stackbfs(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(), 
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_simple_cycles_tiernan(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_simple_cycles_johnson(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_simple_cycles_tarjan(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_simple_cycles_szwarcfiter_lauer(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_simple_cycles_hawick_james(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
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



@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_howard(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5, 6])
    g.add_edge(0, 1)
    e12 = g.add_edge(1, 2)
    g.set_edge_weight(e12, 100.0)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    e63 = g.add_edge(6, 3)
    g.set_edge_weight(e63, 2.0)

    mean, cycle = cycles.howard_minimum_cycle_mean(g)

    assert mean == pytest.approx(1.25)
    assert cycle is not None
    assert cycle.edges == [4, 5, 6, 7]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_howard_on_dag(backend):
    # test with no cycle 
    g1 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend, 
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    g1.add_vertices_from([0, 1, 2])
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(0, 2)

    mean, cycle = cycles.howard_minimum_cycle_mean(g1)
    assert mean == math.inf
    assert cycle is None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_howard_any_hashable(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )

    g.add_vertices_from(["0", "1", "2", "3", "4", "5", "6"])
    g.add_edge("0", "1")
    e12 = g.add_edge("1", "2")
    g.set_edge_weight(e12, 100.0)
    g.add_edge("2", "3", edge="2")
    g.add_edge("3", "0", edge="3")
    g.add_edge("3", "4", edge="4")
    g.add_edge("4", "5", edge="5")
    g.add_edge("5", "6", edge="6")
    e63 = g.add_edge("6", "3", edge="7")
    g.set_edge_weight(e63, 2.0)

    mean, cycle = cycles.howard_minimum_cycle_mean(g)

    assert mean == pytest.approx(1.25)
    assert cycle is not None
