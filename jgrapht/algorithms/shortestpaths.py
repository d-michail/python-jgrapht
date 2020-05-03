from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTGraphPath, JGraphTSingleSourcePaths, JGraphTAllPairsPaths


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


def _sp_between_alg(name, graph, source_vertex, target_vertex):
    alg_method_name = "jgrapht_sp_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err, handle = alg_method(graph.handle, source_vertex, target_vertex)
    if err:
        raise_status()

    return JGraphTGraphPath(handle)


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

    This implementation uses a pairing heap in order to order the edge relaxations.

    :param source_vertex: The source vertex.
    :param target_vertex: The target vertex. If None then shortest paths to all vertices are computed 
           and returns as an instance of `:py:class:.SingleSourcePaths`.
    :param use_bidirectional: Only valid if a target vertex is supplied. In this case the search is 
           bidirectional.
    :returns: Either a `:py:class:jgrapht.types.AbstractGraphPath` or `:py:class:.SingleSourcePaths`.
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
    return _sp_singlesource_alg(
        "bellmanford_get_singlesource_from_vertex", graph, source_vertex
    )


def bfs(graph, source_vertex):
    return _sp_singlesource_alg(
        "bfs_get_singlesource_from_vertex", graph, source_vertex
    )


def johnson_allpairs(graph):
    return _sp_allpairs_alg("johnson_get_allpairs", graph)


def floyd_warshall_allpairs(graph):
    return _sp_allpairs_alg("floydwarshall_get_allpairs", graph)
