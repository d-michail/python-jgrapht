from .. import backend
from .._internals._errors import _raise_status, UnsupportedOperationError
from .._internals._wrappers import _JGraphTClustering

import time


def _clustering_alg(name, graph, *args):
    alg_method_name = "jgrapht_clustering_exec_"
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")

    err, handle = alg_method(graph.handle, *args)
    if err:
        _raise_status()

    return _JGraphTClustering(handle)


def k_spanning_tree(graph, k):
    args = [k]
    return _clustering_alg("k_spanning_tree", graph, *args)


def label_propagation(graph, max_iterations=None, seed=None):
    if seed is None:
        seed = time.time()
    if max_iterations is None:
        max_iterations = 0
    args = [max_iterations, seed]
    return _clustering_alg("label_propagation", graph, *args)
