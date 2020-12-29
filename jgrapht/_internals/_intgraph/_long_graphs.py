from ... import backend
from ...types import (
    Graph,
    GraphType,
    DirectedAcyclicGraph,
)

from collections.abc import Set

from .._wrappers import _HandleWrapper
from .._collections import (
    _JGraphTLongIterator,
    _JGraphTLongSet,
)


class _JGraphTLongGraph(_HandleWrapper, Graph):
    """The actual graph implementation. This implementation always uses longs
    for the vertices and the edges of the graph. All operations are delegated to
    the backend.
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

        # read attributes from backend
        directed = backend.jgrapht_xx_graph_is_directed(self._handle)
        allowing_self_loops = backend.jgrapht_xx_graph_is_allowing_selfloops(self._handle)
        allowing_multiple_edges = backend.jgrapht_xx_graph_is_allowing_multipleedges(
            self._handle
        )
        allowing_cycles = backend.jgrapht_xx_graph_is_allowing_cycles(self._handle)
        weighted = backend.jgrapht_xx_graph_is_weighted(self._handle)
        modifiable = backend.jgrapht_xx_graph_is_modifiable(self._handle)

        self._type = GraphType(
            directed=directed,
            allowing_self_loops=allowing_self_loops,
            allowing_multiple_edges=allowing_multiple_edges,
            allowing_cycles=allowing_cycles,
            weighted=weighted,
            modifiable=modifiable,
        )
        self._vertex_set = None
        self._edge_set = None

    @property
    def type(self):
        return self._type

    def add_vertex(self, vertex=None):
        if vertex is not None:
            backend.jgrapht_ll_graph_add_given_vertex(self._handle, vertex)
        else:
            vertex = backend.jgrapht_ll_graph_add_vertex(self._handle)
        return vertex

    def remove_vertex(self, v):
        backend.jgrapht_ll_graph_remove_vertex(self._handle, v)

    def contains_vertex(self, v):
        return backend.jgrapht_ll_graph_contains_vertex(self._handle, v)

    def add_edge(self, u, v, weight=None, edge=None):
        added = True
        if edge is not None:
            added = backend.jgrapht_ll_graph_add_given_edge(self._handle, u, v, edge)
        else:
            edge = backend.jgrapht_ll_graph_add_edge(self._handle, u, v)

        if added and weight is not None:
            self.set_edge_weight(edge, weight)
        return edge

    def remove_edge(self, e):
        return backend.jgrapht_ll_graph_remove_edge(self._handle, e)

    def contains_edge(self, e):
        return backend.jgrapht_ll_graph_contains_edge(self._handle, e)

    def contains_edge_between(self, u, v):
        return backend.jgrapht_ll_graph_contains_edge_between(self._handle, u, v)

    def degree_of(self, v):
        return backend.jgrapht_ll_graph_degree_of(self._handle, v)

    def indegree_of(self, v):
        return backend.jgrapht_ll_graph_indegree_of(self._handle, v)

    def outdegree_of(self, v):
        return backend.jgrapht_ll_graph_outdegree_of(self._handle, v)

    def edge_source(self, e):
        return backend.jgrapht_ll_graph_edge_source(self._handle, e)

    def edge_target(self, e):
        return backend.jgrapht_ll_graph_edge_target(self._handle, e)

    def get_edge_weight(self, e):
        return backend.jgrapht_ll_graph_get_edge_weight(self._handle, e)

    def set_edge_weight(self, e, weight):
        backend.jgrapht_ll_graph_set_edge_weight(self._handle, e, weight)

    @property
    def number_of_vertices(self):
        return len(self.vertices)

    @property
    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    @property
    def number_of_edges(self):
        return len(self.edges)

    @property
    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        res = backend.jgrapht_ll_graph_create_between_eit(self._handle, u, v)
        return _JGraphTLongIterator(res)

    def edges_of(self, v):
        res = backend.jgrapht_ll_graph_vertex_create_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def inedges_of(self, v):
        res = backend.jgrapht_ll_graph_vertex_create_in_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def outedges_of(self, v):
        res = backend.jgrapht_ll_graph_vertex_create_out_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_vit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            return backend.jgrapht_ll_graph_vertices_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_ll_graph_contains_vertex(self._handle, v)

        def __repr__(self):
            return "_JGraphLongTGraph-VertexSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)    

    class _EdgeSet(Set):
        """Wrapper around the edges of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_eit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            return backend.jgrapht_ll_graph_edges_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_ll_graph_contains_edge(self._handle, v)

        def __repr__(self):
            return "_JGraphTLongGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)

    def __repr__(self):
        return "_JGraphTLongGraph(%r)" % self._handle


class _JGraphTLongDirectedAcyclicGraph(_JGraphTLongGraph, DirectedAcyclicGraph):
    """The directed acyclic graph wrapper."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def descendants(self, vertex):
        set_handle = backend.jgrapht_ll_graph_dag_vertex_descendants(self.handle, vertex)
        return _JGraphTLongSet(handle=set_handle)

    def ancestors(self, vertex):
        set_handle = backend.jgrapht_ll_graph_dag_vertex_ancestors(self.handle, vertex)
        return _JGraphTLongSet(handle=set_handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_dag_topological_it(self.handle)
        return _JGraphTLongIterator(handle=it_handle)


def _create_long_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
):
    """Create a graph with long vertices/edges.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`    
    """
    handle = backend.jgrapht_ll_graph_create(
        directed, allowing_self_loops, allowing_multiple_edges, weighted, False, 0, 0
    )
    return _JGraphTLongGraph(handle)


def _create_long_dag(
    allowing_multiple_edges=False, weighted=True,
):
    """Create a directed acyclic graph.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph`    
    """
    handle = backend.jgrapht_ll_graph_dag_create(allowing_multiple_edges, weighted)
    return _JGraphTLongDirectedAcyclicGraph(handle)


def _is_long_graph(graph):
    """Check if a graph instance is a graph using longs for vertices and edges.
    
    :param graph: the graph
    :returns: True if the graph is a long graph, False otherwise.
    """
    return isinstance(graph, (_JGraphTLongGraph))
