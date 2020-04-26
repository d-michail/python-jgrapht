import time

from .. import backend
from ..graph import GraphPath
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator

def _tour_tsp_alg(name, graph_or_graph_path, *args):
    alg_method_name = 'jgrapht_tour_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, graph_path = alg_method(graph_or_graph_path.handle, *args)
    if err:
        raise_status()

    return GraphPath(graph_path)


def tsp_random(graph, seed=None):
    """Compute a random Hamiltonian cycle. This is a simple unoptimized solution to the 
    Travelling Salesman Problem, suitable for a starting point in optimizing using the 
    two-opt heuristic.

    :param graph: The input graph. Must be undirected and complete.
    :param seed: Seed for the random number generator. If None then the seed is chosen based
                 on the current time.
    :returns: A graph path
    :rtype: :py:class:`jgrapht.graph.GraphPath`
    """
    if seed is None:
        seed = time.time()
    return _tour_tsp_alg('tsp_random', graph, seed)
    

def tsp_greedy_heuristic(graph):
    """ Construct a tour greedily. The algorithm repeatedly selects the shortest edge
    and adds it to the tour as long as it doesn’t create a cycle with less than :math:`n`
    edges, or increases the degree of any node to more that two. 
 
    The runtime complexity is :math:`\mathcal{O}(n^2 \log n)`.
 
    :param graph: The input graph. Must be undirected and complete.
    :returns: A graph path
    :rtype: :py:class:`jgrapht.graph.GraphPath`
    """
    return _tour_tsp_alg('tsp_greedy_heuristic', graph)    


def tsp_nearest_insertion_heuristic(graph):
    return _tour_tsp_alg('tsp_nearest_insertion_heuristic', graph)    


def tsp_nearest_neighbor_heuristic(graph, seed=None):
    if seed is None:
        seed = time.time()
    custom = [ seed ]
    return _tour_tsp_alg('tsp_nearest_neighbor_heuristic', graph, *custom)    


def metric_tsp_christofides(graph):
    return _tour_tsp_alg('metric_tsp_christofides', graph)    


def metric_tsp_two_approx(graph):
    return _tour_tsp_alg('metric_tsp_christofides', graph)


def tsp_held_karp(graph):
    return _tour_tsp_alg('tsp_held_karp', graph)    


def hamiltonian_palmer(graph):
    return _tour_tsp_alg('hamiltonian_palmer', graph)


def tsp_two_opt_heuristic(graph, k=1, min_cost_improvement=0.0001, seed=None):
    if seed is None:
        seed = time.time()
    custom = [ k, min_cost_improvement, seed ]
    return _tour_tsp_alg('tsp_two_opt_heuristic', graph, *custom)


def tsp_two_opt_heuristic_improve(graph_path, min_cost_improvement=0.0001, seed=None):
    if seed is None:
        seed = time.time()
    custom = [  min_cost_improvement, seed ]
    return _tour_tsp_alg('tsp_two_opt_heuristic_improve', graph_path, *custom)

