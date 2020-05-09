from .. import backend
from .._internals._wrappers import _JGraphTLongIterator, _JGraphTLongDoubleMap


def _scoring_alg(name, graph, *args):

    alg_method_name = "jgrapht_scoring_exec_"
    if args:
        alg_method_name += "custom_"
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    _, scores_handle = alg_method(graph.handle, *args)

    return _JGraphTLongDoubleMap(handle=scores_handle)


def alpha_centrality(
    graph,
    damping_factor=0.01,
    exogenous_factor=1.0,
    max_iterations=100,
    tolerance=0.0001,
):
    custom = [damping_factor, exogenous_factor, max_iterations, tolerance]
    return _scoring_alg("alpha_centrality", graph, *custom)


def betweenness_centrality(graph, incoming=False, normalize=False):
    custom = [normalize]
    return _scoring_alg("betweenness_centrality", graph, *custom)


def closeness_centrality(graph, incoming=False, normalize=True):
    custom = [incoming, normalize]
    return _scoring_alg("closeness_centrality", graph, *custom)


def harmonic_centrality(graph, incoming=False, normalize=True):
    custom = [incoming, normalize]
    return _scoring_alg("harmonic_centrality", graph, *custom)


def pagerank(graph, damping_factor=0.85, max_iterations=100, tolerance=0.0001):
    custom = [damping_factor, max_iterations, tolerance]
    return _scoring_alg("pagerank", graph, *custom)
