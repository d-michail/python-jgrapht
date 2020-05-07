from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTGraphPath, JGraphTSingleSourcePaths, JGraphTAllPairsPaths
import ctypes


def _sp_singlesource_alg(name, graph, source_vertex):
    alg_method_name = "jgrapht_sp_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err, handle = alg_method(graph.handle, source_vertex)
    if err:
        raise_status()

    return JGraphTSingleSourcePaths(handle, source_vertex)


def _sp_between_alg(name, graph, source_vertex, target_vertex, *args):
    alg_method_name = "jgrapht_sp_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err, handle = alg_method(graph.handle, source_vertex, target_vertex, *args)
    if err:
        raise_status()

    return JGraphTGraphPath(handle) if handle is not None else None


def _sp_allpairs_alg(name, graph):
    alg_method_name = "jgrapht_sp_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err, handle = alg_method(graph.handle)
    if err:
        raise_status()

    return JGraphTAllPairsPaths(handle)


def dijkstra(graph, source_vertex, target_vertex=None, use_bidirectional=True):
    """Dijkstra's algorithm to compute single-source shortest paths. 

    This implementation uses a pairing heap.

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex. If None then shortest paths to all vertices are computed 
           and returned as an instance of :py:class:`.SingleSourcePaths`
    :param use_bidirectional: only valid if a target vertex is supplied. In this case the search is 
           bidirectional
    :returns: either a :py:class:`.GraphPath` or :py:class:`.SingleSourcePaths` depending on whether a
              target vertex is provided
    """
    if target_vertex is None:
        return _sp_singlesource_alg(
            "dijkstra_get_singlesource_from_vertex", graph, source_vertex
        )
    else:
        if use_bidirectional:
            return _sp_between_alg(
                "bidirectional_dijkstra_get_path_between_vertices",
                graph,
                source_vertex,
                target_vertex,
            )
        else:
            return _sp_between_alg(
                "dijkstra_get_path_between_vertices",
                graph,
                source_vertex,
                target_vertex,
            )


def bellman_ford(graph, source_vertex):
    """Bellman-Ford algorithm to compute single-source shortest paths.

    Computes shortest paths from a single source vertex to all other vertices in a weighted graph.
    The Bellman-Ford algorithm supports negative edge weights.

    Negative weight cycles are not allowed and will be reported by the algorithm by raising an error.
    This implies that negative edge weights are not allowed in undirected graphs.
    Note that the algorithm will not find negative weight cycles which are not reachable from the
    source vertex.

    Running time :math:`\mathcal{O}(m n)`.

    :param graph: the graph
    :param source_vertex: the source vertex
    :returns: a shortest path tree as an instance of :py:class:`.SingleSourcePaths`
    """
    return _sp_singlesource_alg(
        "bellmanford_get_singlesource_from_vertex", graph, source_vertex
    )


def bfs(graph, source_vertex):
    """The BFS as a shortest path algorithm. Even if the graph has weights, 
    this algorithms treats the graph as unweighted.

    Running time :math:`\mathcal{O}(n+m)`.

    :param graph: the graph
    :param source_vertex: the source vertex
    :returns: a shortest path tree as an instance of :py:class:`.SingleSourcePaths`
    """
    return _sp_singlesource_alg(
        "bfs_get_singlesource_from_vertex", graph, source_vertex
    )


def johnson_allpairs(graph):
    """Johnson's all-pairs shortest-paths algorithm.

    Finds the shortest paths between all pairs of vertices in a sparse graph. Edge weights
    can be negative, but no negative-weight cycles may exist. It first executes the
    Bellman-Ford algorithm to compute a transformation of the input graph that removes all
    negative weights, allowing Dijkstra's algorithm to be used on the transformed graph.

    Running time :math:`\mathcal{O}(n m + n^2 \log n)`.

    :param graph: the input graph
    :returns: all-pairs shortest paths as an instance of :py:class:`.AllPairsPaths`
    """
    return _sp_allpairs_alg("johnson_get_allpairs", graph)


def floyd_warshall_allpairs(graph):
    """The Floyd-Warshall algorithm for all-pairs shortest-paths.

    Find all :math:`n^2` shortest paths in time :math:`\mathcal{O}(n^3)`.
    Also requires :math:`\mathcal{O}(n^2)` space.

    :param graph: the input graph
    :returns: all-pairs shortest paths as an instance of :py:class:`.AllPairsPaths`
    """
    return _sp_allpairs_alg("floydwarshall_get_allpairs", graph)


def a_star(graph, source_vertex, target_vertex, heuristic_cb, use_bidirectional=False):
    """The A-star algorithm.

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex.
    :param heuristic_cb: the heuristic callback. Must be a function which accepts two long parameters
      (source and target) and returns a double
    :param use_bidirectional: use a bidirectional search
    :returns: a :py:class:`.GraphPath`
    """
    heuristic_f_type = ctypes.CFUNCTYPE(
        ctypes.c_double, ctypes.c_longlong, ctypes.c_longlong
    )
    heuristic_f = heuristic_f_type(heuristic_cb)
    heuristic_f_ptr = ctypes.cast(heuristic_f, ctypes.c_void_p).value

    custom = [heuristic_f_ptr]

    if use_bidirectional:
        return _sp_between_alg(
            "bidirectional_astar_get_path_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )
    else:
        return _sp_between_alg(
            "astar_get_path_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )
