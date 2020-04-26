import time

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from ..util import JGraphTLongIterator, JGraphTGraphPath

def _tour_tsp_alg(name, graph_or_graph_path, *args):
    alg_method_name = 'jgrapht_tour_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, graph_path = alg_method(graph_or_graph_path.handle, *args)
    if err:
        raise_status()

    return JGraphTGraphPath(graph_path)


def tour_tsp_random(graph, seed=None):
    if seed is None:
        seed = time.time()
    return _tour_tsp_alg('tsp_random', graph, seed)
    

def tour_tsp_greedy_heuristic(graph):
    return _tour_tsp_alg('tsp_greedy_heuristic', graph)    


def tour_tsp_nearest_insertion_heuristic(graph):
    return _tour_tsp_alg('tsp_nearest_insertion_heuristic', graph)    


def tour_tsp_nearest_neighbor_heuristic(graph, seed=None):
    if seed is None:
        seed = time.time()
    custom = [ seed ]
    return _tour_tsp_alg('tsp_nearest_neighbor_heuristic', graph, *custom)    


def tour_metric_tsp_christofides(graph):
    return _tour_tsp_alg('metric_tsp_christofides', graph)    


def tour_metric_tsp_two_approx(graph):
    return _tour_tsp_alg('metric_tsp_christofides', graph)


def tour_tsp_held_karp(graph):
    return _tour_tsp_alg('tsp_held_karp', graph)    


def tour_hamiltonian_palmer(graph):
    return _tour_tsp_alg('hamiltonian_palmer', graph)


def tour_tsp_two_opt_heuristic(graph, k=1, min_cost_improvement=0.0001, seed=None):
    if seed is None:
        seed = time.time()
    custom = [ k, min_cost_improvement, seed ]
    return _tour_tsp_alg('tsp_two_opt_heuristic', graph, *custom)


def tour_tsp_two_opt_heuristic_improve(graph_path, min_cost_improvement=0.0001, seed=None):
    if seed is None:
        seed = time.time()
    custom = [  min_cost_improvement, seed ]
    return _tour_tsp_alg('tsp_two_opt_heuristic_improve', graph_path, *custom)

