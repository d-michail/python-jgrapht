from .. import backend as _backend

from .._internals._flows import (
    _JGraphTCut,
    _JGraphTGomoryHuTree,
)
from .._internals._collections import _JGraphTIntegerMutableSet

from .._internals._anyhashableg import (
    _is_anyhashable_graph,
    _vertex_anyhashableg_to_g as _vertex_anyhashableg_to_g,
)
from .._internals._anyhashableg_flows import (
    _AnyHashableGraphCut,
    _AnyHashableGraphGomoryHuTree,
    _AnyHashableGraphEquivalentFlowTree,
)

from .flow import push_relabel


def mincut_stoer_wagner(graph):
    r"""Compute a min-cut using the Stoer-Wagner algorithm.
        
    This implementation requires :math:`\mathcal{O}(m n \log m)` time where :math:`n` is the
    number of vertices and :math:`m` the number of edges of the graph.
    
    :param graph: the input graph. Must be undirected with non-negative edge weights 
    :returns: a min cut as an instance of :py:class:`.Cut`.
    """
    (
        cut_weight,
        cut_source_partition_handle,
    ) = _backend.jgrapht_cut_mincut_exec_stoer_wagner(graph.handle)

    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphCut(graph, cut_weight, cut_source_partition_handle)
    else:
        return _JGraphTCut(graph, cut_weight, cut_source_partition_handle)


def min_st_cut(graph, source, sink):
    r"""Compute a minimum s-t cut using the Push-relabel algorithm.
    
    This is a :math:`\mathcal{O}(n^3)` algorithm where :math:`n` is the number of vertices 
    of the graph. For more details on the algorithm see:

      * Andrew V. Goldberg and Robert Tarjan. A new approach to the maximum flow problem.
        Proceedings of STOC '86.

    The algorithm uses the graph edge weights as the network edge capacities.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A min s-t cut.
    """
    _, cut = push_relabel(graph, source, sink)
    return cut


def gomory_hu_gusfield(graph):
    r"""Computes a Gomory-Hu Tree using Gusfield's algorithm.
    
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
    handle = _backend.jgrapht_cut_gomoryhu_exec_gusfield(graph.handle)

    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphGomoryHuTree(handle, graph)
    else:
        return _JGraphTGomoryHuTree(handle, graph)


def oddmincutset_padberg_rao(graph, odd_vertices, use_tree_compression=False):
    r"""Compute Odd Minimum Cut-Sets using the Pardberg and Rao algorithm.

    See the following papers:

      * Padberg, M. Rao, M. Odd Minimum Cut-Sets and b-Matchings. Mathematics of Operations
        Research, 7(1), p67-80, 1982.
      * Letchford, A. Reinelt, G. Theis, D. Odd minimum cut-sets and b-matchings revisited.
        SIAM Journal of Discrete Mathematics, 22(4), p1480-1487, 2008.

    Running time :math:`\mathcal{O}(n^4)`.
    
    :param graph: an undirected network. Must be simple and all edge weights must be positive.
    :param odd_vertices: set of vertices labelled "odd". It must have even cardinality.
    :param use_tree_compression: whether to use the tree compression technique    
    :returns: a cut as an instance of :py:class:`.Cut`.
    """
    odd_set = _JGraphTIntegerMutableSet()
    if _is_anyhashable_graph(graph):
        for x in odd_vertices:
            odd_set.add(_vertex_anyhashableg_to_g(graph, x))
    else:
        for x in odd_vertices:
            odd_set.add(x)

    (
        cut_weight,
        cut_source_partition_handle,
    ) = _backend.jgrapht_cut_oddmincutset_exec_padberg_rao(
        graph.handle, odd_set.handle, use_tree_compression
    )

    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphCut(graph, cut_weight, cut_source_partition_handle)
    else:
        return _JGraphTCut(graph, cut_weight, cut_source_partition_handle)
