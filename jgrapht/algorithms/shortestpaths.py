from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import (
    JGraphTGraphPath,
    JGraphTGraphPathIterator,
    JGraphTSingleSourcePaths,
    JGraphTAllPairsPaths,
    JGraphTLongSet,
)
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

def _sp_k_between_alg(name, graph, source_vertex, target_vertex, k, *args):
    alg_method_name = "jgrapht_sp_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm {} not supported.".format(name))

    err, handle = alg_method(graph.handle, source_vertex, target_vertex, k, *args)
    if err:
        raise_status()

    return JGraphTGraphPathIterator(handle)


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
    r"""Bellman-Ford algorithm to compute single-source shortest paths.

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
    r"""The BFS as a shortest path algorithm. Even if the graph has weights, 
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
    r"""Johnson's all-pairs shortest-paths algorithm.

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
    r"""The Floyd-Warshall algorithm for all-pairs shortest-paths.

    Find all :math:`n^2` shortest paths in time :math:`\mathcal{O}(n^3)`.
    Also requires :math:`\mathcal{O}(n^2)` space.

    :param graph: the input graph
    :returns: all-pairs shortest paths as an instance of :py:class:`.AllPairsPaths`
    """
    return _sp_allpairs_alg("floydwarshall_get_allpairs", graph)


def a_star(graph, source_vertex, target_vertex, heuristic_cb, use_bidirectional=False):
    """The A* algorithm.

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


def a_star_with_alt_heuristic(
    graph, source_vertex, target_vertex, landmarks, use_bidirectional=False
):
    r"""The A* algorithm with the ALT admissible heuristic.

    The ALT admissible heuristic for the A* algorithm using a set of landmarks and the triangle inequality.
    Assumes that the graph contains non-negative edge weights. The heuristic requires a set of input nodes
    from the graph, which are used as landmarks. During a pre-processing phase, which requires two shortest
    path computations per landmark using Dijkstra's algorithm, all distances to and from these landmark nodes
    are computed and stored. Afterwards the heuristic estimates the distance from a vertex to another vertex
    using the already computed distances to and from the landmarks and the fact that shortest path distances
    obey the triangle-inequality. The heuristic's space requirement is :math:`\mathcal{O}(n)` per landmark
    where :math:`n` is the number of vertices of the graph. In case of undirected graphs only one Dijkstra's
    algorithm execution is performed per landmark.

    The method generally abbreviated as ALT (from A*, Landmarks and Triangle inequality) is described
    in detail in the following 
    `paper <https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory>`_
    which also contains a discussion on landmark selection strategies.
    
      * Andrew Goldberg and Chris Harrelson. Computing the shortest path: A* Search Meets Graph Theory.
        In Proceedings of the sixteenth annual ACM-SIAM symposium on Discrete algorithms (SODA' 05),
        156--165, 2005.
 
    Note that using this heuristic does not require the edge weights to satisfy the triangle-inequality. The
    method depends on the triangle inequality with respect to the shortest path distances in the graph, not
    an embedding in Euclidean space or some other metric, which need not be present.

    In general more landmarks will speed up A* but will need more space. Given an A* query with
    vertices source and target, a good landmark appears "before" source or "after" target where
    before and after are relative to the "direction" from source to target.    

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex.
    :param landmarks: set of graph vertices to use for landmarks
    :param use_bidirectional: use a bidirectional search
    :returns: a :py:class:`.GraphPath`
    """

    landmarks_set = JGraphTLongSet(linked=True)
    for landmark in landmarks:
        landmarks_set.add(landmark)

    custom = [landmarks_set.handle]

    if use_bidirectional:
        return _sp_between_alg(
            "bidirectional_astar_alt_heuristic_get_path_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )
    else:
        return _sp_between_alg(
            "astar_alt_heuristic_get_path_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )

def yen_k_loopless(graph, source_vertex, target_vertex, k):
    r"""Yen's algorithm for k loopless shortest paths. 

    Running time :math:`\mathcal{O}(k n (m + n \log n))`. 

    The implementation follows: 
    
      * Q. V. Martins, Ernesto and M. B. Pascoal, Marta. (2003). A new implementation
        of Yen’s ranking loopless paths algorithm. Quarterly Journal of the Belgian,
        French and Italian Operations Research Societies. 1. 121-133.

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex.
    :param k: how many paths to return
    :returns: a iterator of :py:class:`.GraphPath`
    """
    return _sp_k_between_alg(
                "yen_get_k_loopless_paths_between_vertices",
                graph,
                source_vertex,
                target_vertex,
                k
            )

def eppstein_k(graph, source_vertex, target_vertex, k):
    r"""Eppstein's algorithm for k shortest paths (may contain loops). 

    Running time :math:`\mathcal{O}(m + n \log n + k \log k)`. Paths are 
    produced in sorted order by weight.

    .. note:: Paths are not guaranteed to be simple, i.e. many contains loops.

    :param graph: the graph. Must be simple
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex
    :param k: how many paths to return
    :returns: a iterator of :py:class:`.GraphPath`
    """
    return _sp_k_between_alg(
                "eppstein_get_k_paths_between_vertices",
                graph,
                source_vertex,
                target_vertex,
                k
            )