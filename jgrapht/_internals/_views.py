from .. import backend
from ..types import GraphType
from ._graphs import _JGraphTGraph

import copy


class _UnweightedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        res = backend.jgrapht_graph_as_unweighted(graph.handle)

        super().__init__(res, True)

        self._type = GraphType(
            directed=graph.type.directed,
            allowing_self_loops=graph.type.allowing_self_loops,
            allowing_multiple_edges=graph.type.allowing_multiple_edges,
            weighted=False,
            modifiable=graph.type.modifiable,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type


class _UndirectedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        res = backend.jgrapht_graph_as_undirected(graph.handle)

        super().__init__(res, True)

        self._type = GraphType(
            directed=False,
            allowing_self_loops=graph.type.allowing_self_loops,
            allowing_multiple_edges=graph.type.allowing_multiple_edges,
            weighted=graph.type.weighted,
            modifiable=graph.type.modifiable,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type


class _UnmodifiableGraphView(_JGraphTGraph):
    def __init__(self, graph):
        res = backend.jgrapht_graph_as_unmodifiable(graph.handle)

        super().__init__(res, True)

        self._type = GraphType(
            directed=graph.type.directed,
            allowing_self_loops=graph.type.allowing_self_loops,
            allowing_multiple_edges=graph.type.allowing_multiple_edges,
            weighted=graph.type.weighted,
            modifiable=False,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type


class _EdgeReversedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        res = backend.jgrapht_graph_as_edgereversed(graph.handle)

        super().__init__(res, True)
        self._type = copy.copy(graph.type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type
