from .. import backend as _backend
from .._internals._flows import (
    _JGraphTCut,
    _JGraphTGomoryHuTree,
)


def _cut_alg(name, graph, *args):

    alg_method_name = "jgrapht_cut_exec_" + name

    try:
        alg_method = getattr(_backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    cut_weight, cut_source_partition_handle = alg_method(graph.handle, *args)

    return _JGraphTCut(graph, cut_weight, cut_source_partition_handle)


def stoer_wagner(graph):
    r"""Compute a min-cut using the Stoer-Wagner algorithm.
        
    This implementation requires :math:`\mathcal{O}(m n \log m)` time where :math:`n` is the
    number of vertices and :math:`m` the number of edges of the graph.
    
    :param graph: the input graph. Must be undirected with non-negative edge weights 
    :returns: a min cut as an instance of :py:class:`.Cut`.
    """
    return _cut_alg("stoer_wagner", graph)


def gomory_hu_gusfield(graph):
    """Computes a Gomory-Hu Tree using Gusfield's algorithm.
    
    Gomory-Hu Trees can be used to calculate the maximum s-t flow value and the minimum
    s-t cut between all pairs of vertices. It does so by performing :math:`n-1` max flow
    computations. 

    For more details see: 

      * Gusfield, D, Very simple methods for all pairs network flow analysis. SIAM Journal
        on Computing, 19(1), p142-155, 1990

    This implementation uses the push-relabel algorithm for the minimum s-t cut which
    is :math:`\mathcal{O}(n^3)`. The total complexity is, therefore, :math:`\mathcal{O}(n^4)`.

    :param graph: an undirected network    
    :returns: a Gomory-Hu tree as an instance of :py:class:`jgrapht.types.GomoryHuTree`
    """
    handle = _backend.jgrapht_gomoryhu_exec_gusfield(graph.handle)
    return _JGraphTGomoryHuTree(handle, graph)
