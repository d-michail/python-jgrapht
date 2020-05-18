from . import backend
from ._internals._views import (
    _UnweightedGraphView,
    _UnmodifiableGraphView,
    _UndirectedGraphView,
    _EdgeReversedGraphView,
    _MaskedSubgraphView,
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


def as_edgereversed(graph):
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