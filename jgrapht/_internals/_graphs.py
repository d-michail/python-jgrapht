from .. import backend
from ..types import (
    Graph,
    GraphType,
)
from collections.abc import (
    Set,
)
from ._wrappers import _HandleWrapper
from ._collections import _JGraphTLongIterator


class _JGraphTGraph(_HandleWrapper, Graph):
    """The actual graph implementation."""

    def __init__(
        self,
        handle=None,
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        **kwargs
    ):
        creating_graph = handle is None
        if creating_graph:
            handle = backend.jgrapht_graph_create(
                directed, allowing_self_loops, allowing_multiple_edges, weighted
            )
        super().__init__(handle=handle, **kwargs)

        self._vertex_set = None
        self._edge_set = None

        if not creating_graph:
            # read attributes from backend
            directed = backend.jgrapht_graph_is_directed(self._handle)
            allowing_self_loops = backend.jgrapht_graph_is_allowing_selfloops(
                self._handle
            )
            allowing_multiple_edges = backend.jgrapht_graph_is_allowing_multipleedges(self._handle)
            weighted = backend.jgrapht_graph_is_weighted(self._handle)

        self._graph_type = GraphType(
            directed, allowing_self_loops, allowing_multiple_edges, weighted
        )

    @property
    def graph_type(self):
        return self._graph_type

    def add_vertex(self, vertex):
        res = backend.jgrapht_graph_add_given_vertex(self._handle, vertex)
        return res

    def remove_vertex(self, v):
        backend.jgrapht_graph_remove_vertex(self._handle, v)

    def contains_vertex(self, v):
        res = backend.jgrapht_graph_contains_vertex(self._handle, v)
        return res

    def create_edge(self, u, v, weight=None):
        res = backend.jgrapht_graph_add_edge(self._handle, u, v)
        if weight is not None:
            self.set_edge_weight(res, weight)
        return res

    def add_edge(self, u, v, edge, weight=None):
        added = backend.jgrapht_graph_add_given_edge(self._handle, u, v, edge)
        if added and weight is not None: 
            self.set_edge_weight(edge, weight)
        return added

    def remove_edge(self, e):
        res = backend.jgrapht_graph_remove_edge(self._handle, e)
        return res

    def contains_edge(self, e):
        res = backend.jgrapht_graph_contains_edge(self._handle, e)
        return res

    def contains_edge_between(self, u, v):
        res = backend.jgrapht_graph_contains_edge_between(self._handle, u, v)
        return res

    def degree_of(self, v):
        res = backend.jgrapht_graph_degree_of(self._handle, v)
        return res

    def indegree_of(self, v):
        res = backend.jgrapht_graph_indegree_of(self._handle, v)
        return res

    def outdegree_of(self, v):
        res = backend.jgrapht_graph_outdegree_of(self._handle, v)
        return res

    def edge_source(self, e):
        res = backend.jgrapht_graph_edge_source(self._handle, e)
        return res

    def edge_target(self, e):
        res = backend.jgrapht_graph_edge_target(self._handle, e)
        return res

    def get_edge_weight(self, e):
        res = backend.jgrapht_graph_get_edge_weight(self._handle, e)
        return res

    def set_edge_weight(self, e, weight):
        backend.jgrapht_graph_set_edge_weight(self._handle, e, weight)

    def number_of_vertices(self):
        return len(self.vertices())

    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    def number_of_edges(self):
        return len(self.edges())

    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        res = backend.jgrapht_graph_create_between_eit(self._handle, u, v)
        return _JGraphTLongIterator(res)

    def edges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def inedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def outedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_vit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            res = backend.jgrapht_graph_vertices_count(self._handle)
            return res

        def __contains__(self, v):
            res = backend.jgrapht_graph_contains_vertex(self._handle, v)
            return res

        def __repr__(self):
            return "_JGraphTGraph-VertexSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

    class _EdgeSet(Set):
        """Wrapper around the edges of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_eit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            res = backend.jgrapht_graph_edges_count(self._handle)
            return res

        def __contains__(self, v):
            res = backend.jgrapht_graph_contains_edge(self._handle, v)
            return res

        def __repr__(self):
            return "_JGraphTGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

    def __repr__(self):
        return "_JGraphTGraph(%r)" % self._handle


def create_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
):
    """Create a graph.

    :param directed: If True the graph will be directed, otherwise undirected.
    :param allowing_self_loops: If True the graph will allow the addition of self-loops.
    :param allowing_multiple_edges: If True the graph will allow multiple-edges.
    :param weighted: If True the graph will be weighted, otherwise unweighted.
    :returns: A graph
    :rtype: :class:`type <.types.Graph>`
    """
    return _JGraphTGraph(
        directed=directed,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
    )