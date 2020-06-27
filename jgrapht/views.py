from .types import ListenableGraph

from ._internals._views import (
    _UnweightedGraphView,
    _UnmodifiableGraphView,
    _UndirectedGraphView,
    _EdgeReversedGraphView,
    _MaskedSubgraphView,
    _WeightedView,
    _GraphUnion,
    _ListenableView,
)

from ._internals._anyhashableg import (
    _is_anyhashable_graph,
    _as_unweighted_anyhashable_graph as _as_unweighted_anyhashable_graph,
    _as_undirected_anyhashable_graph as _as_undirected_anyhashable_graph,
    _as_unmodifiable_anyhashable_graph as _as_unmodifiable_anyhashable_graph,
    _as_edgereversed_anyhashable_graph as _as_edgereversed_anyhashable_graph,
    _as_weighted_anyhashable_graph as _as_weighted_anyhashable_graph,
    _as_masked_subgraph_anyhashable_graph as _as_masked_subgraph_anyhashable_graph,
)


def as_unweighted(graph):
    """Create an unweighted view of a graph. Any updates in the original graph are reflected
    in the view.
    
    :param graph: the original graph
    :returns: an unweighted graph
    """
    if _is_anyhashable_graph(graph):
        return _as_unweighted_anyhashable_graph(graph)
    else:
        return _UnweightedGraphView(graph)


def as_undirected(graph):
    """Create an undirected view of a graph. Any updates in the original graph are reflected
    in the view.
    
    :param graph: the original graph
    :returns: an undirected graph
    """
    if _is_anyhashable_graph(graph):
        return _as_undirected_anyhashable_graph(graph)
    else:
        return _UndirectedGraphView(graph)


def as_unmodifiable(graph):
    """Create an unmodifiable view of a graph. Any updates in the original graph are reflected
    in the view.

    :param graph: the original graph
    :returns: an unmodifiable graph
    """
    if _is_anyhashable_graph(graph):
        return _as_unmodifiable_anyhashable_graph(graph)
    else:
        return _UnmodifiableGraphView(graph)


def as_edge_reversed(graph):
    """Create an edge reversed view of a graph. Any updates in the original graph are reflected
    in the view.

    :param graph: the original graph
    :returns: a graph with reversed edges
    """
    if _is_anyhashable_graph(graph):
        return _as_edgereversed_anyhashable_graph(graph)
    else:
        return _EdgeReversedGraphView(graph)


def as_masked_subgraph(graph, vertex_mask_cb, edge_mask_cb=None):
    """Create a masked subgraph view. 

    This is an unmodifiable subgraph induced by the vertex/edge masking callbacks. The subgraph
    will keep track of edges being added to its vertex subset as well as deletion of edges and
    vertices (from the original graph). When iterating over the vertices/edges, it will iterate
    over the vertices/edges of the base graph and discard vertices/edges that are masked (an
    edge with a masked endpoint vertex is discarded as well).

    .. note :: Callback functions accept the vertex or edge as a parameter and they must return 
      true or false indicating whether the vertex or edge should be masked.

    :param graph: the original graph
    :param vertex_mask_cb: a vertex mask callback
    :param edge_mask_cb: an edge mask callback
    :returns: a masked subgraph 
    """
    if _is_anyhashable_graph(graph):
        return _as_masked_subgraph_anyhashable_graph(
            graph, vertex_mask_cb, edge_mask_cb
        )
    else:
        return _MaskedSubgraphView(graph, vertex_mask_cb, edge_mask_cb)


def as_weighted(graph, edge_weight_cb, cache_weights=True, write_weights_through=False):
    """Create a weighted view of a graph.

    This function can be used to make an unweighted graph weighted, to override the weights
    of a weighted graph, or to provide different weighted views of the same underlying graph.

    The weights are calculated using the user provided edge_weight_cb callback function.
    This function should take as argument the edge identifier and return its weight. If the 
    edge weight callback is None, then a default function which always returns 1.0 is 
    used. 

    If parameter cache_weights is True, then the edge weight function is only called once
    to initialize the weight. Other calls will return the cached weight without calling the 
    provided function. Moreover, the returned value can be adjusted. Note that calling 
    :py:meth:`~jgrapht.types.Graph.set_edge_weight` with caching disabled will raise an error.

    If parameter write_weights_through is True, the weight set by calling method 
    :py:meth:`~jgrapht.types.Graph.set_edge_weight` will be propagated to the backing graph.
    In this case the backing graph must be weighted, otherwise an error will be raised.

    :param graph: the original graph
    :param edge_weight_cb: edge weight function
    :param cache_weights: if true weights are cached once computed by the weight function
    :param write_weights_through: if true, any weight adjustment by method 
      :py:meth:`~jgrapht.types.Graph.set_edge_weight` will be propagated to the backing graph
    :returns: a weighted view
    """
    if _is_anyhashable_graph(graph):
        return _as_weighted_anyhashable_graph(
            graph, edge_weight_cb, cache_weights, write_weights_through
        )
    else:
        return _WeightedView(
            graph, edge_weight_cb, cache_weights, write_weights_through
        )


def as_listenable(graph):
    """Create a listenable view of a graph. This is a graph view which supports listeners
    on structural change events.

    :param graph: the original graph
    :returns: a listenable graph which is an instance of type :py:class:`~jgrapht.types.ListenableGraph`.
    """
    if isinstance(graph, ListenableGraph) or _is_anyhashable_graph(graph):
        return graph
    return _ListenableView(graph)


def as_graph_union(graph1, graph2, edge_weight_combiner_cb=None):
    """Create a graph union view of two graphs. Any updates in the original graphs are reflected
    in the view.

    The resulting graph is unmodifiable and may contain multiple-edges even if the input graphs did
    not contain multiple edges. If both graphs contain an edge with the same identifier, but the 
    edge endpoints are different in the two graphs, then the graph union contains the edge with the
    endpoints from the first graph. The weight of edge is computed using the combiner provided as 
    parameter.

    .. note:: Graph types must be the same. You cannot union a directed with an undirected graph.

    :param graph1: the first graph
    :param graph2: the second graph
    :param edge_weight_combiner_cb: function responsible for combining weights in edges which belong
       to both graphs. If None then the default combiner is addition. The callback must accept two 
       double parameters and return one.
    :returns: a graph which is the union of the two graphs
    """
    if _is_anyhashable_graph(graph1) or _is_anyhashable_graph(graph2):
        raise ValueError("View not supported for any-hashable graphs")
    return _GraphUnion(graph1, graph2, edge_weight_combiner_cb)
