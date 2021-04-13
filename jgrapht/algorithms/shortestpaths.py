from .. import backend as _backend

from .._internals._wrappers import GraphBackend, _JGraphTThreadPool
from .._internals._results import (
    _build_vertex_set,
    _unwrap_vertex,
    _unwrap_astar_heuristic_cb,
    _wrap_graphpath,
    _wrap_graphpath_iterator,
    _wrap_single_source_paths,
    _wrap_allpairs_paths,
    _wrap_multi_objective_single_source_paths,
    _wrap_contraction_hierarchies,
    _wrap_manytomany_contraction_hierarchies,
)
from .._internals._callbacks import _create_wrapped_callback

import ctypes
import multiprocessing
import time


def _sp_singlesource_alg(name, graph, source_vertex, *args):
    cases = {
        GraphBackend.LONG_GRAPH: "jgrapht_lx_sp_exec_",
        GraphBackend.INT_GRAPH: "jgrapht_ix_sp_exec_",
        GraphBackend.REF_GRAPH: "jgrapht_rx_sp_exec_",
    }
    alg_method_name = cases[graph._backend_type] + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(graph.handle, _unwrap_vertex(graph, source_vertex), *args)
    return _wrap_single_source_paths(graph, handle, source_vertex)


def _sp_between_alg(name, graph, source_vertex, target_vertex, *args):
    cases = {
        GraphBackend.LONG_GRAPH: "jgrapht_lx_sp_exec_",
        GraphBackend.INT_GRAPH: "jgrapht_ix_sp_exec_",
        GraphBackend.REF_GRAPH: "jgrapht_rx_sp_exec_",
    }
    alg_method_name = cases[graph._backend_type] + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(
        graph.handle,
        _unwrap_vertex(graph, source_vertex),
        _unwrap_vertex(graph, target_vertex),
        *args
    )
    if handle is None:
        return None
    return _wrap_graphpath(graph, handle)


def _sp_allpairs_alg(name, graph):
    alg_method_name = "jgrapht_xx_sp_exec_" + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(graph.handle)
    return _wrap_allpairs_paths(graph, handle)


def _sp_k_between_alg(name, graph, source_vertex, target_vertex, k, *args):
    cases = {
        GraphBackend.LONG_GRAPH: "jgrapht_lx_sp_exec_",
        GraphBackend.INT_GRAPH: "jgrapht_ix_sp_exec_",
        GraphBackend.REF_GRAPH: "jgrapht_rx_sp_exec_",
    }
    alg_method_name = cases[graph._backend_type] + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(
        graph.handle,
        _unwrap_vertex(graph, source_vertex),
        _unwrap_vertex(graph, target_vertex),
        k,
        *args
    )
    return _wrap_graphpath_iterator(graph, handle)


def _multisp_singlesource_alg(name, graph, source_vertex, *args):
    cases = {
        GraphBackend.LONG_GRAPH: "jgrapht_ll_multisp_exec_",
        GraphBackend.INT_GRAPH: "jgrapht_ii_multisp_exec_",
        GraphBackend.REF_GRAPH: "jgrapht_rr_multisp_exec_",
    }
    alg_method_name = cases[graph._backend_type] + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(graph.handle, _unwrap_vertex(graph, source_vertex), *args)
    return _wrap_multi_objective_single_source_paths(graph, handle, source_vertex)


def _multisp_between_alg(name, graph, source_vertex, target_vertex, *args):
    cases = {
        GraphBackend.LONG_GRAPH: "jgrapht_ll_multisp_exec_",
        GraphBackend.INT_GRAPH: "jgrapht_ii_multisp_exec_",
        GraphBackend.REF_GRAPH: "jgrapht_rr_multisp_exec_",
    }
    alg_method_name = cases[graph._backend_type] + name
    alg_method = getattr(_backend, alg_method_name)

    handle = alg_method(
        graph.handle,
        _unwrap_vertex(graph, source_vertex),
        _unwrap_vertex(graph, target_vertex),
        *args
    )
    return _wrap_graphpath_iterator(graph, handle)


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
    :param heuristic_cb: the heuristic callback. Must be a function which accepts two vertex parameters
      (source and target) and returns a double
    :param use_bidirectional: use a bidirectional search
    :returns: a :py:class:`.GraphPath`
    """

    actual_heuristic_cb_wrapper = _unwrap_astar_heuristic_cb(graph, heuristic_cb)
    custom = [actual_heuristic_cb_wrapper.fptr]

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

    landmarks_set = _build_vertex_set(graph, landmarks)
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
        k,
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
        "eppstein_get_k_paths_between_vertices", graph, source_vertex, target_vertex, k
    )


def delta_stepping(
    graph, source_vertex, target_vertex=None, delta=None, parallelism=None
):
    """Delta stepping algorithm to compute single-source shortest paths.

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex. If None then shortest paths to all vertices are computed
           and returned as an instance of :py:class:`.SingleSourcePaths`
    :param delta: the delta parameter. If None then it is automatically calculated, by traversing
      the graph at least once.
    :param parallelism: amount of parallelism to use. If None the cpu cores are used
    :returns: either a :py:class:`.GraphPath` or :py:class:`.SingleSourcePaths` depending on whether a
              target vertex is provided
    """
    if graph._backend_type == GraphBackend.REF_GRAPH:
        raise ValueError("Delta stepping not supported with ref-graph backend")

    if parallelism is None:
        parallelism = multiprocessing.cpu_count()
    thread_pool = _JGraphTThreadPool(
        handle=_backend.jgrapht_executor_thread_pool_create(parallelism)
    )

    if delta is None:
        delta = 0.0

    custom = [delta, thread_pool.handle]

    if target_vertex is None:
        res = _sp_singlesource_alg(
            "delta_stepping_get_singlesource_from_vertex", graph, source_vertex, *custom
        )

    else:
        res = _sp_between_alg(
            "delta_stepping_get_path_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )
    thread_pool.shutdown()
    return res


def martin_multiobjective(
    graph, edge_weight_cb, edge_weight_dimension, source_vertex, target_vertex=None
):
    """Martin's algorithm for the multi-objective shortest paths problem.

    Martin's label setting algorithm is a multiple objective extension of Dijkstra's algorithm, where
    the minimum operator is replaced by a dominance test. It computes a maximal complete set of efficient
    paths when all the weight values are non-negative.

    .. note :: Note that the multi-objective shortest path problem is a well-known NP-hard problem.

    :param graph: the graph
    :param edge_weight_cb: edge weight callback. It should accept an edge as a parameter and return a list of
      weights.
    :param edge_weight_dimension: dimension of the edge weight function
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex. If None the paths to all vertices are computed
           and returned as an instance of :py:class:`.MultiObjectiveSingleSourcePaths`
    :returns: either an iterator of :py:class:`.GraphPath` or :py:class:`.MultiObjectiveSingleSourcePaths`
       depending on whether a target vertex is provided
    """
    if edge_weight_dimension < 1:
        raise ValueError("Cost function needs to have a positive dimension")

    if graph._backend_type == GraphBackend.LONG_GRAPH:

        def inner_edge_weight_cb(edge):
            weights = edge_weight_cb(edge)[:edge_weight_dimension]
            array = (ctypes.c_double * len(weights))(*weights)
            array_ptr = ctypes.cast(array, ctypes.c_void_p)
            return array_ptr.value

        cb_fptr, cb = _create_wrapped_callback(
            inner_edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_longlong)
        )

    elif graph._backend_type == GraphBackend.REF_GRAPH:

        def inner_edge_weight_cb(edge):
            weights = edge_weight_cb(edge)[:edge_weight_dimension]
            array = (ctypes.c_double * len(weights))(*weights)
            array_ptr = ctypes.cast(array, ctypes.c_void_p)
            return array_ptr.value

        cb_fptr, cb = _create_wrapped_callback(
            inner_edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.py_object)
        )

    else:

        def inner_edge_weight_cb(edge):
            weights = edge_weight_cb(edge)[:edge_weight_dimension]
            array = (ctypes.c_double * len(weights))(*weights)
            array_ptr = ctypes.cast(array, ctypes.c_void_p)
            return array_ptr.value

        cb_fptr, cb = _create_wrapped_callback(
            inner_edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int)
        )

    custom = [cb_fptr, edge_weight_dimension]

    if target_vertex is None:
        return _multisp_singlesource_alg(
            "martin_get_multiobjectivesinglesource_from_vertex",
            graph,
            source_vertex,
            *custom
        )
    else:
        return _multisp_between_alg(
            "martin_get_paths_between_vertices",
            graph,
            source_vertex,
            target_vertex,
            *custom
        )


def precompute_contraction_hierarchies(graph, parallelism=None, seed=None):
    r"""Precompute contraction hierarchies.

    This is a preprocessing technique which speeds up shortest path queries. See
    :py:meth:`contraction_hierarchies_many_to_many` and
    :py:meth:`contraction_hierarchies_dijkstra` on how to use this object.

    :param graph: the graph
    :param parallelism: how many thread to use
    :param seed: seed for the random number generator.
    :returns: the contraction hierarchies
    """
    if parallelism is None:
        parallelism = multiprocessing.cpu_count()
    thread_pool = _JGraphTThreadPool(
        handle=_backend.jgrapht_executor_thread_pool_create(parallelism)
    )

    if seed is None:
        seed = int(time.time())

    res = _backend.jgrapht_xx_sp_exec_contraction_hierarchy(
        graph.handle, thread_pool.handle, seed
    )
    thread_pool.shutdown()
    return _wrap_contraction_hierarchies(graph, res)


def contraction_hierarchies_many_to_many(graph, sources, targets, ch=None):
    r"""Compute shortest paths between two set of vertices using contraction hierarchies.

    :param graph: the graph
    :param sources: source vertices
    :param targets: target vertices
    :param ch: the contraction hierarchy to use. If None it is computed from scratch.
    :returns: a set of shortest paths
    :rtype: :py:class:`.ManyToManyPaths`
    """
    jgrapht_sources = _build_vertex_set(graph, sources)
    jgrapht_targets = _build_vertex_set(graph, targets)

    if ch is None:
        ch = precompute_contraction_hierarchies(graph)

    handle = _backend.jgrapht_xx_sp_exec_contraction_hierarchy_get_manytomany(
        ch.handle, jgrapht_sources.handle, jgrapht_targets.handle
    )
    return _wrap_manytomany_contraction_hierarchies(graph, handle)


def contraction_hierarchies_dijkstra(
    graph, source_vertex, target_vertex, ch=None, radius=None
):
    r"""Compute a shortest path using bidirectional dijkstra and contraction
    hierarchies.

    :param graph: the graph
    :param source_vertex: the source vertex
    :param target_vertex: the target vertex
    :param ch: the contraction hierarchy to use. If None it is computed from scratch.
    :param radius: compute shortest paths of at most this length
    :returns: a shortest path
    :rtype: :py:class:`.GraphPath`
    """
    if radius is None:
        radius = float.fromhex("0x1.fffffffffffffP+1023")

    if ch is None:
        ch = precompute_contraction_hierarchies(graph)

    handle = _backend.jgrapht_ix_sp_exec_contraction_hierarchy_bidirectional_dijkstra_get_path_between_vertices(
        ch.handle,
        _unwrap_vertex(graph, source_vertex),
        _unwrap_vertex(graph, target_vertex),
        radius,
    )

    if handle is None:
        return None
    return _wrap_graphpath(graph, handle)
