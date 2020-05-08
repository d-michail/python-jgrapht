from .. import backend
from .._internals._errors import _raise_status, UnsupportedOperationError
from .._internals._wrappers import _JGraphTCut


def _cut_alg(name, graph, *args):

    alg_method_name = "jgrapht_cut_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")

    err, cut_weight, cut_source_partition_handle = alg_method(
        graph.handle, *args
    )
    if err:
        _raise_status()

    return _JGraphTCut(graph, cut_weight, cut_source_partition_handle)


def stoer_wagner(graph):
    r"""Compute a min-cut using the Stoer-Wagner algorithm.
        
    This implementation requires :math:`\mathcal{O}(m n \log m)` time where :math:`n` is the
    number of vertices and :math:`m` the number of edges of the graph.
    
    :param graph: the input graph. Must be undirected with non-negative edge weights 
    :returns: a min cut as an instance of :py:class:`.Cut`.
    """
    return _cut_alg("stoer_wagner", graph)

