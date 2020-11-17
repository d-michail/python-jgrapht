import time

from .. import backend as _backend

from .._internals._paths import _JGraphTGraphPath

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_paths import _AnyHashableGraphGraphPath


def _wrap_result(graph, graph_path_handle):
    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphGraphPath(graph_path_handle, graph)
    else:
        return _JGraphTGraphPath(graph_path_handle, graph)


def tsp_random(graph, seed=None):
    """Compute a random Hamiltonian cycle. This is a simple unoptimized solution to the 
    Travelling Salesman Problem, suitable for a starting point in optimizing using the 
    two-opt heuristic.

    :param graph: the input graph. Must be undirected and complete
    :param seed: seed for the random number generator. If None then the seed is chosen based
                 on the current time
    :returns: A random tour
    :rtype: :py:class:`.GraphPath`
    """
    if seed is None:
        seed = int(time.time())
    graph_path_handle = _backend.jgrapht_tour_tsp_random(graph.handle, seed)
    return _wrap_result(graph, graph_path_handle)


def tsp_greedy_heuristic(graph):
    r""" Construct a tour greedily. The algorithm repeatedly selects the shortest edge
    and adds it to the tour as long as it doesn’t create a cycle with less than :math:`n`
    edges, or increases the degree of any node to more that two. 
 
    The runtime complexity is :math:`\mathcal{O}(n^2 \log n)`.
 
    :param graph: the input graph. Must be undirected and complete
    :returns: a greedy tour
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_tsp_greedy_heuristic(graph.handle)
    return _wrap_result(graph, graph_path_handle)


def tsp_nearest_insertion_heuristic(graph):
    r"""The nearest insertion heuristic algorithm for the TSP problem.

    The runtime complexity is :math:`\mathcal{O}(n^2)`.

    :param graph: the input graph. Must be undirected and complete
    :returns: a tour
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_tsp_nearest_insertion_heuristic(
        graph.handle
    )
    return _wrap_result(graph, graph_path_handle)


def tsp_nearest_neighbor_heuristic(graph, seed=None):
    r"""The nearest neighbour heuristic algorithm for the TSP problem.

    The runtime complexity is :math:`\mathcal{O}(n^2)`.

    :param graph: the input graph. Must be undirected and complete
    :param seed: seed for the random number generator, use system time if None
    :returns: a tour
    :rtype: :py:class:`.GraphPath`
    """
    if seed is None:
        seed = int(time.time())
    graph_path_handle = _backend.jgrapht_tour_tsp_nearest_neighbor_heuristic(
        graph.handle, seed
    )
    return _wrap_result(graph, graph_path_handle)


def metric_tsp_christofides(graph):
    r"""The Christofides 3/2-approximation algorithm for the metric TSP.

    For details see:

      * Christofides, N.: Worst-case analysis of a new heuristic for the travelling
        salesman problem. Graduate School of Industrial Administration, Carnegie Mellon
        University (1976).

    Running time :math:`\mathcal{O}(n^3 m)`.

    :param graph: The input graph. Must be undirected, complete and satisfy the
      triangle inequality.
    :returns: a tour which is a 3/2 approximation
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_metric_tsp_christofides(graph.handle)
    return _wrap_result(graph, graph_path_handle)


def metric_tsp_two_approx(graph):
    r"""A 2-approximation algorithm for the metric TSP.

    This is an implementation of the folklore algorithm which returns a depth-first ordering
    of the minimum spanning tree. The algorithm is a 2-approximation assuming that the instance
    satisfies the triangle inequality. The implementation requires the input graph to be
    undirected and complete. The running time is :math:`\mathcal{O}(n^2 \log n)`.

    :param graph: the input graph. Must be undirected, complete and satisfy the
      triangle inequality
    :returns: a tour which is a 2-approximation
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_metric_tsp_two_approx(graph.handle)
    return _wrap_result(graph, graph_path_handle)


def tsp_held_karp(graph):
    r"""A dynamic programming algorithm for the TSP.

    Finds an optimal, minimum-cost Hamiltonian tour. Running time is 
    :math:`\mathcal{O}(2^n \times n^2)` and space :math:`\mathcal{O}(2^n \times n)`.

    :param graph: the input graph. Must be undirected and complete
    :returns: an optimal tour
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_tsp_held_karp(graph.handle)
    return _wrap_result(graph, graph_path_handle)


def hamiltonian_palmer(graph):
    r"""Palmer's algorithm for computing Hamiltonian cycles in graphs that meet Ore's condition.

    Running time :math:`\mathcal{O}(n^2)`.

    :param graph: the input graph. Must be simple and meet Ore's condition.
    :returns: a hamiltonian cycle
    :rtype: :py:class:`.GraphPath`
    """
    graph_path_handle = _backend.jgrapht_tour_hamiltonian_palmer(graph.handle)
    return _wrap_result(graph, graph_path_handle)


def tsp_two_opt_heuristic(graph, k=1, min_cost_improvement=0.0001, seed=None):
    """The 2-opt heuristic algorithm for the TSP problem.

    This is an implementation of the 2-opt improvement heuristic algorithm. The algorithm
    generates k initial tours and then iteratively improves the tours until a local minimum
    is reached. In each iteration it applies the best possible 2-opt move which means to find
    the best pair of edges (i,i+1) and (j,j+1) such that replacing them with (i,j) and
    (i+1,j+1) minimizes the tour length. The default initial tours are constructed randomly.

    :param graph: the input graph. Must be undirected and complete
    :param k: how many initial tours to generate
    :param min_cost_improvement: minimum cost improvement per iteration
    :param seed: seed for the random number generator, use system time if None
    :returns: a tour
    :rtype: :py:class:`.GraphPath`
    """
    if seed is None:
        seed = int(time.time())
    custom = [k, min_cost_improvement, seed]
    graph_path_handle = _backend.jgrapht_tour_tsp_two_opt_heuristic(
        graph.handle, *custom
    )
    return _wrap_result(graph, graph_path_handle)


def tsp_two_opt_heuristic_improve(graph_path, min_cost_improvement=0.0001, seed=None):
    """Improve a tour using the 2-opt heuristic for the TSP problem.

    This is an implementation of the 2-opt improvement heuristic algorithm. The algorithm
    takes as input a tour and then iteratively improves the tour until a local minimum
    is reached. In each iteration it applies the best possible 2-opt move which means to find
    the best pair of edges (i,i+1) and (j,j+1) such that replacing them with (i,j) and
    (i+1,j+1) minimizes the tour length.

    :param graph: the input tour, instance of :py:class:`.GraphPath`
    :param min_cost_improvement: minimum cost improvement per iteration
    :param seed: seed for the random number generator, use system time if None
    :returns: a tour
    :rtype: :py:class:`.GraphPath`
    """
    if seed is None:
        seed = int(time.time())

    new_graph_path_handle = _backend.jgrapht_tour_tsp_two_opt_heuristic_improve(
        graph_path.handle, min_cost_improvement, seed
    )

    graph = graph_path.graph
    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphGraphPath(new_graph_path_handle, graph)
    else:
        return _JGraphTGraphPath(new_graph_path_handle, graph)
