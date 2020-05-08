from .. import backend
from ..types import GraphType
import copy

from ._errors import _raise_status
from ._wrappers import _JGraphTGraph


class _UnweightedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unweighted(graph.handle)
        if err:
            _raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(
            directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=False,
            modifiable=graph.graph_type.modifiable,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class _UndirectedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_undirected(graph.handle)
        if err:
            _raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(
            directed=False,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=graph.graph_type.modifiable,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class _UnmodifiableGraphView(_JGraphTGraph):
    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unmodifiable(graph.handle)
        if err:
            _raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(
            directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=False,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class _EdgeReversedGraphView(_JGraphTGraph):
    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_edgereversed(graph.handle)
        if err:
            _raise_status()

        super().__init__(res, True)
        self._graph_type = copy.copy(graph.graph_type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type