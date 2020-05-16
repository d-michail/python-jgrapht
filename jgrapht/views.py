from . import backend
from ._internals._views import (
    _UnweightedGraphView,
    _UnmodifiableGraphView,
    _UndirectedGraphView,
    _EdgeReversedGraphView,
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
