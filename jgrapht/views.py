from . import backend
from ._errors import raise_status
from .graph import GraphType, JGraphTGraph
from copy import copy


class UnweightedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unweighted(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=False,
            modifiable=graph.graph_type.modifiable)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type

class UndirectedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_undirected(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=False,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=graph.graph_type.modifiable)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class UnmodifiableGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unmodifiable(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=False)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class EdgeReversedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_edgereversed(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)
        self._graph_type = copy(graph.graph_type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


def as_unweighted(graph):
    """Create an unweighted view of a graph"""
    return UnweightedGraphView(graph)


def as_undirected(graph):
    """Create an undirected view of a graph"""
    return UndirectedGraphView(graph)


def as_unmodifiable(graph):
    """Create an unmodifiable view of a graph"""
    return UnmodifiableGraphView(graph)


def as_edgereversed(graph):
    """Create an edge reversed view of a graph"""
    return EdgeReversedGraphView(graph)