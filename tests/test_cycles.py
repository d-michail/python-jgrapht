import pytest

from jgrapht import create_graph
import jgrapht.algorithms.cycles as cycles


def test_hierholzer():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    
    g.add_vertices_from([0,1,2,3])
    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)

    cycle = cycles.eulerian_cycle(g)

    assert cycle is not None
    assert cycle.edges == [3, 0, 1, 2]


def test_chinese_postman():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    
    g.add_vertices_from([0,1,2,3,4])
    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)
    g.create_edge(3, 4)

    closed_walk = cycles.chinese_postman(g)

    assert closed_walk is not None
    assert closed_walk.edges == [4, 3, 0, 1, 2, 4]


def test_simple_cycles_tarjan(): 

    for variant in ['Tarjan', 'Tiernan', 'Johnson']: 
        g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

        g.add_vertices_from([0,1,2,3,4,5])

        g.create_edge(0, 1)
        g.create_edge(1, 2)
        g.create_edge(2, 3)
        g.create_edge(3, 0)
        g.create_edge(1, 4)
        g.create_edge(4, 5)
        g.create_edge(5, 2)

        it = cycles.enumerate_simple_cycles(g, variant=variant)    

        cycle1 = next(it)
        assert list(cycle1) == [0, 1, 2, 3]
        cycle2 = next(it)
        assert list(cycle2) == [0, 1, 4, 5, 2, 3]

        with pytest.raises(StopIteration):
            next(it)



def test_simple_cycles_szwarcfiter_lauer(): 

    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    g.add_vertices_from([0,1,2,3,4,5])

    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)
    g.create_edge(1, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 2)

    it = cycles.enumerate_simple_cycles(g, variant='Szwarcfiter-Lauer')    

    cycle1 = next(it)
    assert list(cycle1) == [2, 3, 0, 1]
    cycle2 = next(it)
    assert list(cycle2) == [2, 3, 0, 1, 4, 5]

    with pytest.raises(StopIteration):
        next(it)


def test_simple_cycles_hawick_james(): 

    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    g.add_vertices_from([0,1,2,3,4,5])

    g.create_edge(0, 1)
    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 0)
    g.create_edge(1, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 2)

    it = cycles.enumerate_simple_cycles(g, variant='Hawick-James')    

    cycle1 = next(it)
    assert list(cycle1) == [3, 2, 1, 0]
    cycle2 = next(it)
    assert list(cycle2) == [3, 2, 5, 4, 1, 0]

    with pytest.raises(StopIteration):
        next(it)


