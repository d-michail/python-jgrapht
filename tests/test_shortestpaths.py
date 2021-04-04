import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.shortestpaths as sp
import math


class CustomVertex:
    def __init__(self, id):
        self._id = id

    def __repr__(self):
        return "CustomVertex(%r)" % self._id


class CustomEdge:
    def __init__(self, id):
        self._id = id

    def __repr__(self):
        return "CustomEdge(%r)" % self._id


class CustomVertexSupplier:
    def __init__(self):
        self._next = 0

    def __call__(self):
        ret = self._next
        self._next += 1
        return CustomVertex(ret)


class CustomEdgeSupplier:
    def __init__(self):
        self._next = 0

    def __call__(self):
        ret = self._next
        self._next += 1
        return CustomEdge(ret)


def get_graph(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1, weight=3.0)
    g.add_edge(1, 3, weight=100.0)
    g.add_edge(0, 2, weight=40.0)
    g.add_edge(2, 4, weight=20.0)
    g.add_edge(3, 5, weight=2.0)
    g.add_edge(4, 5, weight=2.0)
    g.add_edge(5, 0, weight=13.0)
    g.add_edge(0, 5, weight=1000.0)

    return g


def get_anyhashableg_graph(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    for i in range(0, 6):
        g.add_vertex()

    g.add_edge(0, 1, weight=3.0, edge=0)
    g.add_edge(1, 3, weight=100.0, edge=1)
    g.add_edge(0, 2, weight=40.0, edge="2")
    g.add_edge(2, 4, weight=20.0, edge=3)
    g.add_edge(3, 5, weight=2.0, edge=4)
    g.add_edge(4, 5, weight=2.0, edge=5)
    g.add_edge(5, 0, weight=13.0, edge=6)
    g.add_edge(0, 5, weight=1000.0, edge=7)

    return g


def get_graph_with_negative_edges(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    assert g.type.directed

    for i in range(0, 7):
        assert g.add_vertex() == i

    g.add_edge(0, 1, weight=3.0)
    g.add_edge(1, 3, weight=100.0)
    g.add_edge(0, 2, weight=40.0)
    g.add_edge(2, 4, weight=20.0)
    g.add_edge(3, 5, weight=2.0)
    g.add_edge(4, 5, weight=2.0)
    g.add_edge(5, 0, weight=13.0)
    g.add_edge(0, 6, weight=1000.0)
    g.add_edge(6, 3, weight=-900.0)

    assert len(g.vertices) == 7
    assert len(g.edges) == 9

    assert g.edges == {0, 1, 2, 3, 4, 5, 6, 7, 8}
    return g


def get_graph_custom_vertices_with_negative_edges(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=CustomVertexSupplier(),
        edge_supplier=CustomEdgeSupplier(),
    )

    assert g.type.directed

    v = [g.add_vertex() for i in range(0,7)]

    g.add_edge(v[0], v[1], weight=3.0)
    g.add_edge(v[1], v[3], weight=100.0)
    g.add_edge(v[0], v[2], weight=40.0)
    g.add_edge(v[2], v[4], weight=20.0)
    g.add_edge(v[3], v[5], weight=2.0)
    g.add_edge(v[4], v[5], weight=2.0)
    g.add_edge(v[5], v[0], weight=13.0)
    g.add_edge(v[0], v[6], weight=1000.0)
    g.add_edge(v[6], v[3], weight=-900.0)

    assert len(g.vertices) == 7
    assert len(g.edges) == 9

    return g


def get_anyhashableg_graph_with_negative_edges(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    assert g.type.directed

    for i in range(0, 7):
        assert g.add_vertex(i) == i

    g.add_edge(0, 1, weight=3.0, edge=0)
    g.add_edge(1, 3, weight=100.0, edge=1)
    g.add_edge(0, 2, weight=40.0, edge="2")
    g.add_edge(2, 4, weight=20.0, edge=3)
    g.add_edge(3, 5, weight=2.0, edge=4)
    g.add_edge(4, 5, weight=2.0, edge=5)
    g.add_edge(5, 0, weight=13.0, edge=6)
    g.add_edge(0, 6, weight=1000.0, edge=7)
    g.add_edge(6, 3, weight=-900.0, edge=8)

    assert len(g.vertices) == 7
    assert len(g.edges) == 9

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_dijkstra(backend):
    g = get_graph(backend)

    single_path = sp.dijkstra(g, 0, 5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]
    assert [e for e in single_path] == [2, 3, 5]

    single_path = sp.dijkstra(g, 0, 5, use_bidirectional=False)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    from_paths = sp.dijkstra(g, 0)
    repr(from_paths)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    single_path = from_paths.get_path(3)
    repr(single_path)
    assert single_path.weight == 103.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 3
    assert list(single_path.edges) == [0, 1]

    # test no path
    g.add_vertex(100)
    nopath = sp.dijkstra(g, 0, 100)
    assert nopath is None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_dijkstra(backend):
    g = get_anyhashableg_graph(backend)

    single_path = sp.dijkstra(g, 0, 5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    single_path = sp.dijkstra(g, 0, 5, use_bidirectional=False)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    from_paths = sp.dijkstra(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    single_path = from_paths.get_path(3)
    assert single_path.weight == 103.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 3
    assert list(single_path.edges) == [0, 1]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bfs(backend):
    g = get_graph(backend)

    from_paths = sp.bfs(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 1000.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [7]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_bfs(backend):
    g = get_anyhashableg_graph(backend)

    from_paths = sp.bfs(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 1000.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [7]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_bellman(backend):
    g = get_graph_with_negative_edges(backend)

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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_bellman(backend):
    g = get_anyhashableg_graph_with_negative_edges(backend)

    from_paths = sp.bellman_ford(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    from1 = sp.bellman_ford(g, 1)
    assert from1.source_vertex == 1
    path15 = from1.get_path(5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_johnsons(backend):
    g = get_graph_with_negative_edges(backend)

    allpairs = sp.johnson_allpairs(g)
    repr(allpairs)
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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_johnsons_refgraph_custom(backend):
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=CustomVertexSupplier(),
        edge_supplier=CustomEdgeSupplier(),
    )

    assert g.type.directed

    v = [g.add_vertex() for i in range(0,7)]

    e0 = g.add_edge(v[0], v[1], weight=3.0)
    e1 = g.add_edge(v[1], v[3], weight=100.0)
    e2 = g.add_edge(v[0], v[2], weight=40.0)
    e3 = g.add_edge(v[2], v[4], weight=20.0)
    e4 = g.add_edge(v[3], v[5], weight=2.0)
    e5 = g.add_edge(v[4], v[5], weight=2.0)
    e6 = g.add_edge(v[5], v[0], weight=13.0)
    e7 = g.add_edge(v[0], v[6], weight=1000.0)
    e8 = g.add_edge(v[6], v[3], weight=-900.0)

    assert len(g.vertices) == 7
    assert len(g.edges) == 9

    allpairs = sp.johnson_allpairs(g)
    repr(allpairs)

    path05 = allpairs.get_path(v[0], v[5])
    assert path05.weight == 62.0
    assert path05.start_vertex == v[0]
    assert path05.end_vertex == v[5]
    print(path05.edges)
    assert list(path05.edges) == [e2, e3, e5]

    path15 = allpairs.get_path(v[1], v[5])
    assert path15.weight == 102.0
    assert path15.start_vertex == v[1]
    assert path15.end_vertex == v[5]
    assert list(path15.edges) == [e1, e4]

    path05 = allpairs.get_paths_from(v[0]).get_path(v[5])
    assert path05.weight == 62.0
    assert path05.start_vertex == v[0]
    assert path05.end_vertex == v[5]
    assert list(path05.edges) == [e2, e3, e5]    


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_johnsons(backend):
    g = get_anyhashableg_graph_with_negative_edges(backend)

    allpairs = sp.johnson_allpairs(g)
    path05 = allpairs.get_path(0, 5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == ["2", 3, 5]

    path15 = allpairs.get_path(1, 5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]

    path05 = allpairs.get_paths_from(0).get_path(5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == ["2", 3, 5]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_floyd_warshall(backend):
    g = get_graph_with_negative_edges(backend)

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


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_floyd_warshall(backend):
    g = get_anyhashableg_graph_with_negative_edges(backend)

    allpairs = sp.floyd_warshall_allpairs(g)
    repr(allpairs)

    path05 = allpairs.get_path(0, 5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == ["2", 3, 5]

    path15 = allpairs.get_path(1, 5)
    assert path15.weight == 102.0
    assert path15.start_vertex == 1
    assert path15.end_vertex == 5
    assert list(path15.edges) == [1, 4]

    path05 = allpairs.get_paths_from(0).get_path(5)
    assert path05.weight == 62.0
    assert path05.start_vertex == 0
    assert path05.end_vertex == 5
    assert list(path05.edges) == ["2", 3, 5]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_a_star(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5, 6, 7, 8])

    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(1, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(3, 6)
    g.add_edge(4, 5)
    g.add_edge(4, 7)
    g.add_edge(5, 8)

    def heuristic(source, target):
        coordinates = {
            0: (2, 0),
            1: (2, 1),
            2: (2, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (0, 0),
            7: (0, 1),
            8: (0, 2),
        }
        sx = coordinates[source][0]
        sy = coordinates[source][1]

        tx = coordinates[target][0]
        ty = coordinates[target][1]

        dx = sx - tx
        dy = sy - ty
        d = math.sqrt(dx * dx + dy * dy)

        return d

    path = sp.a_star(g, 0, 8, heuristic_cb=heuristic)

    assert path.edges == [0, 3, 7, 9]
    assert path.start_vertex == 0
    assert path.end_vertex == 8

    path1 = sp.a_star(g, 0, 8, heuristic_cb=heuristic, use_bidirectional=True)

    assert path1.edges == [0, 3, 7, 9]
    assert path1.start_vertex == 0
    assert path1.end_vertex == 8


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_a_star(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend
    )

    g.add_vertices_from([0, 1, 2, "3", 4, "5", 6, 7, "8"])

    g.add_edge(0, 1, edge=0)
    g.add_edge(0, "3", edge=1)
    g.add_edge(1, 2, edge=2)
    g.add_edge(1, 4, edge=3)
    g.add_edge(2, "5", edge=4)
    g.add_edge("3", 4, edge=5)
    g.add_edge("3", 6, edge=6)
    g.add_edge(4, "5", edge=7)
    g.add_edge(4, 7, edge=8)
    g.add_edge("5", "8", edge=9)

    def heuristic(source, target):
        coordinates = {
            0: (2, 0),
            1: (2, 1),
            2: (2, 2),
            "3": (1, 0),
            4: (1, 1),
            "5": (1, 2),
            6: (0, 0),
            7: (0, 1),
            "8": (0, 2),
        }
        sx = coordinates[source][0]
        sy = coordinates[source][1]

        tx = coordinates[target][0]
        ty = coordinates[target][1]

        dx = sx - tx
        dy = sy - ty
        d = math.sqrt(dx * dx + dy * dy)

        return d

    path = sp.a_star(g, 0, "8", heuristic_cb=heuristic)

    assert path.edges == [0, 3, 7, 9]
    assert path.start_vertex == 0
    assert path.end_vertex == "8"

    path1 = sp.a_star(g, 0, "8", heuristic_cb=heuristic, use_bidirectional=True)

    assert path1.edges == [0, 3, 7, 9]
    assert path1.start_vertex == 0
    assert path1.end_vertex == "8"


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_a_star_with_alt_heuristic(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=IntegerSupplier(),
        edge_supplier=IntegerSupplier(),        
    )

    g.add_vertices_from([0, 1, 2, 3, 4, 5, 6, 7, 8])

    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(1, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(3, 6)
    g.add_edge(4, 5)
    g.add_edge(4, 7)
    g.add_edge(5, 8)

    path = sp.a_star_with_alt_heuristic(g, 0, 8, landmarks=set([3, 6]))

    assert path.edges == [0, 2, 4, 9]
    assert path.start_vertex == 0
    assert path.end_vertex == 8

    path1 = sp.a_star_with_alt_heuristic(
        g, 0, 8, landmarks=set([2, 7]), use_bidirectional=True
    )

    assert path1.edges == [0, 2, 4, 9]
    assert path1.start_vertex == 0
    assert path1.end_vertex == 8


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_a_star_with_alt_heuristic(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
    )

    g.add_vertices_from([0, 1, 2, "3", 4, 5, 6, 7, 8])

    g.add_edge(0, 1, edge=0)
    g.add_edge(0, "3", edge=1)
    g.add_edge(1, 2, edge=2)
    g.add_edge(1, 4, edge=3)
    g.add_edge(2, 5, edge=4)
    g.add_edge("3", 4, edge=5)
    g.add_edge("3", 6, edge=6)
    g.add_edge(4, 5, edge=7)
    g.add_edge(4, 7, edge=8)
    g.add_edge(5, 8, edge=9)

    path = sp.a_star_with_alt_heuristic(g, 0, 8, landmarks=set(["3", 6]))

    assert path.edges == [0, 2, 4, 9]
    assert path.start_vertex == 0
    assert path.end_vertex == 8

    path1 = sp.a_star_with_alt_heuristic(
        g, 0, 8, landmarks=set([2, 7]), use_bidirectional=True
    )

    assert path1.edges == [0, 2, 4, 9]
    assert path1.start_vertex == 0
    assert path1.end_vertex == 8


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_yen_k(backend):

    g = get_graph(backend)

    it = sp.yen_k_loopless(g, 0, 5, 2)

    p1 = next(it)
    assert p1.edges == [2, 3, 5]
    assert p1.weight == 62.0
    assert p1.vertices == [0, 2, 4, 5]
    p2 = next(it)
    assert p2.edges == [0, 1, 4]
    assert p2.weight == 105.0
    assert next(it, None) == None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_yen_k(backend):

    g = get_anyhashableg_graph(backend)

    it = sp.yen_k_loopless(g, 0, 5, 2)

    p1 = next(it)
    assert p1.edges == ["2", 3, 5]
    assert p1.weight == 62.0
    assert p1.vertices == [0, 2, 4, 5]
    p2 = next(it)
    assert p2.edges == [0, 1, 4]
    assert p2.weight == 105.0
    assert next(it, None) == None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_eppstein_k(backend):

    g = get_graph(backend)

    it = sp.eppstein_k(g, 0, 5, 2)

    p1 = next(it)
    assert p1.edges == [2, 3, 5]
    assert p1.weight == 62.0
    p2 = next(it)
    assert p2.edges == [0, 1, 4]
    assert p2.weight == 105.0
    assert next(it, None) == None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_eppstein_k(backend):

    g = get_anyhashableg_graph(backend)

    it = sp.eppstein_k(g, 0, 5, 2)

    p1 = next(it)
    assert p1.edges == ["2", 3, 5]
    assert p1.weight == 62.0
    p2 = next(it)
    assert p2.edges == [0, 1, 4]
    assert p2.weight == 105.0
    assert next(it, None) == None


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_delta_stepping(backend):
    g = get_graph(backend)

    single_path = sp.delta_stepping(g, 0, 5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    single_path = sp.delta_stepping(g, 0, 5, delta=20.0)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    from_paths = sp.delta_stepping(g, 0)
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

    single_path = sp.delta_stepping(g, 0, 5, delta=10.0, parallelism=2)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]

    single_path = sp.delta_stepping(g, 0, 5, delta=10.0, parallelism=16)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == [2, 3, 5]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
    ],
)
def test_anyhashableg_delta_stepping(backend):
    g = get_anyhashableg_graph(backend)

    single_path = sp.delta_stepping(g, 0, 5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    single_path = sp.delta_stepping(g, 0, 5, delta=20.0)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    from_paths = sp.delta_stepping(g, 0)
    assert from_paths.source_vertex == 0
    single_path = from_paths.get_path(5)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    single_path = from_paths.get_path(3)
    assert single_path.weight == 103.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 3
    assert list(single_path.edges) == [0, 1]

    single_path = sp.delta_stepping(g, 0, 5, delta=10.0, parallelism=2)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]

    single_path = sp.delta_stepping(g, 0, 5, delta=10.0, parallelism=16)
    assert single_path.weight == 62.0
    assert single_path.start_vertex == 0
    assert single_path.end_vertex == 5
    assert list(single_path.edges) == ["2", 3, 5]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_martin(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    g.add_vertices_from(range(1, 6))

    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(2, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    costs = {
        0: [1.0, 5.0],
        1: [4.0, 2.0],
        2: [4.0, 4.0],
        3: [1.0, 2.0],
        4: [2.0, 5.0],
        5: [2.0, 3.0],
        6: [6.0, 1.0],
        7: [3.0, 3.0],
    }

    def cost_function(e):
        return costs[e]

    multi_paths = sp.martin_multiobjective(g, cost_function, 2, 1)
    repr(multi_paths)

    assert multi_paths.source_vertex == 1
    it = multi_paths.get_paths(5)
    repr(it)
    p1 = next(it)
    assert p1.edges == [0, 4]
    p2 = next(it)
    assert p2.edges == [1, 6]
    p3 = next(it)
    assert p3.edges == [2, 7]
    assert next(it, "Exhausted") == "Exhausted"

    it = sp.martin_multiobjective(g, cost_function, 2, 1, 5)
    p1 = next(it)
    assert p1.edges == [0, 4]
    p2 = next(it)
    assert p2.edges == [1, 6]
    p3 = next(it)
    assert p3.edges == [2, 7]
    assert next(it, "Exhausted") == "Exhausted"


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.ANY_HASHABLE_GRAPH,
        GraphBackend.REF_GRAPH,
    ],
)
def test_anyhashableg_martin(backend):

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=False,
        backend=backend
    )

    g.add_vertices_from(range(1, 6))

    g.add_edge(1, 2, edge=0)
    g.add_edge(1, 3, edge=1)
    g.add_edge(1, 4, edge="e2")
    g.add_edge(2, 4, edge="edge3")
    g.add_edge(2, 5, edge=4)
    g.add_edge(3, 4, edge=5)
    g.add_edge(3, 5, edge=6)
    g.add_edge(4, 5, edge=7)

    costs = {
        0: [1.0, 5.0],
        1: [4.0, 2.0],
        "e2": [4.0, 4.0],
        "edge3": [1.0, 2.0],
        4: [2.0, 5.0],
        5: [2.0, 3.0],
        6: [6.0, 1.0],
        7: [3.0, 3.0],
    }

    def cost_function(e):
        return costs[e]

    multi_paths = sp.martin_multiobjective(g, cost_function, 2, 1)
    repr(multi_paths)
    
    assert multi_paths.source_vertex == 1
    it = multi_paths.get_paths(5)
    p1 = next(it)
    assert p1.edges == [0, 4]
    p2 = next(it)
    assert p2.edges == [1, 6]
    p3 = next(it)
    assert p3.edges == ["e2", 7]
    assert next(it, "Exhausted") == "Exhausted"

    it = sp.martin_multiobjective(g, cost_function, 2, 1, 5)
    repr(it)
    p1 = next(it)
    assert p1.edges == [0, 4]
    p2 = next(it)
    assert p2.edges == [1, 6]
    p3 = next(it)
    assert p3.edges == ["e2", 7]
    assert next(it, "Exhausted") == "Exhausted"


def test_martin_bad_cost_function():

    g = create_graph(
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=False,
    )

    assert g.type.allowing_cycles

    g.add_vertices_from(range(1, 6))

    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(2, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    costs = {
        0: [1.0, 5.0],
        1: [4.0, 2.0],
        2: [4.0, 4.0],
        3: [1.0, 2.0],
        4: [2.0, 5.0],
        5: [2.0, 3.0],
        6: [6.0, 1.0],
        7: [3.0, 3.0],
    }

    def cost_function(e):
        return costs[e]

    bad_dimension = 0
    with pytest.raises(ValueError):
        multi_paths = sp.martin_multiobjective(g, cost_function, bad_dimension, 1)

