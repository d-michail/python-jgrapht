from .. import backend
from .._internals._errors import _raise_status, UnsupportedOperationError
from .._internals._wrappers import _JGraphTCut, _JGraphTFlow


def _maxflow_alg(name, graph, source, sink, *args):

    alg_method_name = "jgrapht_maxflow_exec_" + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")

    err, flow_value, flow_handle, cut_source_partition_handle = alg_method(
        graph.handle, source, sink, *args
    )
    if err:
        _raise_status()

    flow = _JGraphTFlow(flow_handle, source, sink, flow_value)
    cut = _JGraphTCut(graph, flow_value, cut_source_partition_handle)

    return flow, cut


def dinic(graph, source, sink):
    r"""Compute a maximum flow using Dinic's algorithm with scaling.
    
    This is a :math:`\mathcal{O}(n^2 m)` algorithm where :math:`n` is the number of vertices 
    and :math:`m` the number of edges of the graph.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.
    
    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights. 
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("dinic", graph, source, sink)


def push_relabel(graph, source, sink):
    r"""Compute a maximum flow using the Push-relabel algorithm.
    
    This is a :math:`\mathcal{O}(n^3)` algorithm where :math:`n` is the number of vertices 
    of the graph. For more details on the algorithm see:

      * Andrew V. Goldberg and Robert Tarjan. A new approach to the maximum flow problem.
        Proceedings of STOC '86.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("push_relabel", graph, source, sink)


def edmonds_karp(graph, source, sink):
    r"""Compute a maximum flow using the Edmonds-Karp variant of the Ford-Fulkerson algorithm.
    
    This is a :math:`\mathcal{O}(n m^2)` algorithm where :math:`n` is the number of vertices 
    and :math:`m` the number of edges of the graph.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.

    .. note:: This implementation assumes that the graph does not contain self-loops or multiple-edges.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights. 
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("edmonds_karp", graph, source, sink)


def max_st_flow(graph, source, sink):
    r"""Compute a maximum flow using the Push-relabel algorithm.
    
    This is a :math:`\mathcal{O}(n^3)` algorithm where :math:`n` is the number of vertices 
    of the graph. For more details on the algorithm see:

      * Andrew V. Goldberg and Robert Tarjan. A new approach to the maximum flow problem.
        Proceedings of STOC '86.

    The algorithm uses the graph edge weights as the network edge capacities.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: The max s-t flow.
    """
    flow, _ = push_relabel(graph, source, sink)
    return flow


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
