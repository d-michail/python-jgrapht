from . import backend
from ._internals._views import (
    _UnweightedGraphView,
    _UnmodifiableGraphView,
    _UndirectedGraphView,
    _EdgeReversedGraphView,
    _MaskedSubgraphView,
    _WeightedView,
)


def as_unweighted(graph):
    """Create an unweighted view of a graph. Any updates in the original graph are reflected
    in the view.
    
    :param graph: the original graph
    :returns: an unweighted graph
    """
    return _UnweightedGraphView(graph)


def as_undirected(graph):
    """Create an undirected view of a graph. Any updates in the original graph are reflected
    in the view.
    
    :param graph: the original graph
    :returns: an undirected graph
    """
    return _UndirectedGraphView(graph)


def as_unmodifiable(graph):
    """Create an unmodifiable view of a graph. Any updates in the original graph are reflected
    in the view.

    :param graph: the original graph
    :returns: an unmodifiable graph
    """
    return _UnmodifiableGraphView(graph)


def as_edge_reversed(graph):
    """Create an edge reversed view of a graph. Any updates in the original graph are reflected
    in the view.

    :param graph: the original graph
    :returns: a graph with reversed edges
    """
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
    return _WeightedView(graph, edge_weight_cb, cache_weights, write_weights_through)
