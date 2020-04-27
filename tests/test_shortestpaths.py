import pytest

from jgrapht import create_graph
import jgrapht.algorithms.shortestpaths as sp

def get_graph():
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for _ in range(0, 6):
        g.add_vertex()

    g.add_edge(0, 1, weight=3.0)
    g.add_edge(1, 3, weight=100.0)
    g.add_edge(0, 2, weight=40.0)
    g.add_edge(2, 4, weight=20.0)
    g.add_edge(3, 5, weight=2.0)
    g.add_edge(4, 5, weight=2.0)
    g.add_edge(5, 0, weight=13.0)
    g.add_edge(0, 5, weight=1000.0)

    return g

def get_graph_with_negative_edges():
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for _ in range(0, 7):
        g.add_vertex()

    g.add_edge(0, 1, weight=3.0)
    g.add_edge(1, 3, weight=100.0)
    g.add_edge(0, 2, weight=40.0)
    g.add_edge(2, 4, weight=20.0)
    g.add_edge(3, 5, weight=2.0)
    g.add_edge(4, 5, weight=2.0)
    g.add_edge(5, 0, weight=13.0)
    g.add_edge(0, 6, weight=1000.0)
    g.add_edge(6, 3, weight=-900.0)

    return g    

def test_dijkstra():
    g = get_graph()

    single_path = sp.dijkstra(g, 0, 5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    single_path = sp.dijkstra(g, 0, 5, use_bidirectional=False)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    from_paths = sp.dijkstra(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    single_path = from_paths.get_path(3)
    assert single_path.weight == 103.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 3
    assert list(single_path.edges) == [0, 1]


def test_bfs():
    g = get_graph()

    from_paths = sp.bfs(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 1000.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [7]


def test_bellman():
    g = get_graph_with_negative_edges()

    from_paths = sp.bellman_ford(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    from1 = sp.bellman_ford(g, 1)
    assert from1.source_vertex == 1
    path15 = from1.get_path(5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]


def test_johnsons():
    g = get_graph_with_negative_edges()

    allpairs = sp.johnson_allpairs(g)
    path05 = allpairs.get_path(0, 5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == [2, 3, 5]

    path15 = allpairs.get_path(1, 5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]

    path05 = allpairs.get_paths_from(0).get_path(5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == [2, 3, 5]



def test_floyd_warshall():
    g = get_graph_with_negative_edges()

    allpairs = sp.floyd_warshall_allpairs(g)
    path05 = allpairs.get_path(0, 5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == [2, 3, 5]

    path15 = allpairs.get_path(1, 5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]

    path05 = allpairs.get_paths_from(0).get_path(5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == [2, 3, 5]