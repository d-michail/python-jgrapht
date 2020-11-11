from .. import backend
from ..types import (
    Graph,
    GraphType,
    DirectedAcyclicGraph,
)

from collections.abc import Set

from ._wrappers import _HandleWrapper
from ._collections import (
    _JGraphTIntegerIterator,
    _JGraphTIntegerSet,
    _JGraphTEdgeTripleList,
)


class _JGraphTGraph(_HandleWrapper, Graph):
    """The actual graph implementation. This implementation always uses integers
    for the vertices and the edges of the graph. All operations are delegated to
    the backend.
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

        # read attributes from backend
        directed = backend.jgrapht_graph_is_directed(self._handle)
        allowing_self_loops = backend.jgrapht_graph_is_allowing_selfloops(self._handle)
        allowing_multiple_edges = backend.jgrapht_graph_is_allowing_multipleedges(
            self._handle
        )
        allowing_cycles = backend.jgrapht_graph_is_allowing_cycles(self._handle)
        weighted = backend.jgrapht_graph_is_weighted(self._handle)
        modifiable = backend.jgrapht_graph_is_modifiable(self._handle)

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
            backend.jgrapht_graph_add_given_vertex(self._handle, vertex)
        else:
            vertex = backend.jgrapht_graph_add_vertex(self._handle)
        return vertex

    def remove_vertex(self, v):
        backend.jgrapht_graph_remove_vertex(self._handle, v)

    def contains_vertex(self, v):
        return backend.jgrapht_graph_contains_vertex(self._handle, v)

    def add_edge(self, u, v, weight=None, edge=None):
        added = True
        if edge is not None:
            added = backend.jgrapht_graph_add_given_edge(self._handle, u, v, edge)
        else:
            edge = backend.jgrapht_graph_add_edge(self._handle, u, v)

        if added and weight is not None:
            self.set_edge_weight(edge, weight)
        return edge

    def remove_edge(self, e):
        return backend.jgrapht_graph_remove_edge(self._handle, e)

    def contains_edge(self, e):
        return backend.jgrapht_graph_contains_edge(self._handle, e)

    def contains_edge_between(self, u, v):
        return backend.jgrapht_graph_contains_edge_between(self._handle, u, v)

    def degree_of(self, v):
        return backend.jgrapht_graph_degree_of(self._handle, v)

    def indegree_of(self, v):
        return backend.jgrapht_graph_indegree_of(self._handle, v)

    def outdegree_of(self, v):
        return backend.jgrapht_graph_outdegree_of(self._handle, v)

    def edge_source(self, e):
        return backend.jgrapht_graph_edge_source(self._handle, e)

    def edge_target(self, e):
        return backend.jgrapht_graph_edge_target(self._handle, e)

    def get_edge_weight(self, e):
        return backend.jgrapht_graph_get_edge_weight(self._handle, e)

    def set_edge_weight(self, e, weight):
        backend.jgrapht_graph_set_edge_weight(self._handle, e, weight)

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
        res = backend.jgrapht_graph_create_between_eit(self._handle, u, v)
        return _JGraphTIntegerIterator(res)

    def edges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_eit(self._handle, v)
        return _JGraphTIntegerIterator(res)

    def inedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        return _JGraphTIntegerIterator(res)

    def outedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        return _JGraphTIntegerIterator(res)

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_vit(self._handle)
            return _JGraphTIntegerIterator(res)

        def __len__(self):
            return backend.jgrapht_graph_vertices_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_graph_contains_vertex(self._handle, v)

        def __repr__(self):
            return "_JGraphTGraph-VertexSet(%r)" % self._handle

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
            res = backend.jgrapht_graph_create_all_eit(self._handle)
            return _JGraphTIntegerIterator(res)

        def __len__(self):
            return backend.jgrapht_graph_edges_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_graph_contains_edge(self._handle, v)

        def __repr__(self):
            return "_JGraphTGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)

    def __repr__(self):
        return "_JGraphTGraph(%r)" % self._handle


class _JGraphTDirectedAcyclicGraph(_JGraphTGraph, DirectedAcyclicGraph):
    """The directed acyclic graph wrapper."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def descendants(self, vertex):
        set_handle = backend.jgrapht_graph_dag_vertex_descendants(self.handle, vertex)
        return _JGraphTIntegerSet(handle=set_handle)

    def ancestors(self, vertex):
        set_handle = backend.jgrapht_graph_dag_vertex_ancestors(self.handle, vertex)
        return _JGraphTIntegerSet(handle=set_handle)

    def __iter__(self):
        it_handle = backend.jgrapht_graph_dag_topological_it(self.handle)
        return _JGraphTIntegerIterator(handle=it_handle)


def _create_int_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
):
    """Create a graph with integer vertices/edges.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`    
    """
    handle = backend.jgrapht_graph_create(
        directed, allowing_self_loops, allowing_multiple_edges, weighted
    )
    return _JGraphTGraph(handle)


def _create_sparse_int_graph(edgelist, num_of_vertices=None, directed=True, weighted=True):
    """Create a sparse graph with integer vertices/edges. 

    A sparse graph uses a CSR (compressed-sparse-rows) representation. The result is 
    lower memory consumption and very efficient and cache-friendly representation on
    recent machines. Their drawback is that they assume a continuous range of vertices
    and edges and that they are not modifiable after construction.

    .. note :: Sparse graphs cannot be modified after construction. They are best suited 
       for executing algorithms which do not need to modify the graph after loading.
       
    .. note :: While the graph structure is unmodifiable, the edge weights can be
      adjusted.
    
    Sparse graphs can always support self-loops and multiple-edges.

    :param edgelist: list of tuple (u,v) or (u,v,weight) for weighted graphs
    :param num_of_vertices: number of vertices in the graph. Vertices always start from 0 
      and increase continuously. If not explicitly given the edgelist will be traversed in
      order to find out the number of vertices
    :param directed: whether the graph will be directed or undirected
    :param weighted: whether the graph will be weighted or not
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    track_num_vertices = num_of_vertices is None

    if weighted and isinstance(edgelist, _JGraphTEdgeTripleList):
        # Special case for internal edge list, created using the edgelist
        # importers. This avoids copying.
        e_list_owner = False
        e_list = edgelist.handle

        if track_num_vertices: 
            num_of_vertices = 0
            for u, v, *w in edgelist:
                num_of_vertices = max(u, v, num_of_vertices)
            num_of_vertices += 1
    else:
        e_list_owner = True
        e_list = backend.jgrapht_list_create()

        if track_num_vertices: 
            num_of_vertices = 0

        if weighted:
            for u, v, w in edgelist:
                backend.jgrapht_list_edge_triple_add(e_list, u, v, w)
                if track_num_vertices:
                     num_of_vertices = max(u, v, num_of_vertices)
        else:
            for u, v, *w in edgelist:
                backend.jgrapht_list_edge_pair_add(e_list, u, v)
                if track_num_vertices:
                    num_of_vertices = max(u, v, num_of_vertices)

        if track_num_vertices: 
            num_of_vertices += 1

    handle = backend.jgrapht_graph_sparse_create(
        directed, weighted, num_of_vertices, e_list
    )

    if e_list_owner:
        backend.jgrapht_handles_destroy(e_list)

    return _JGraphTGraph(handle)


def _copy_to_sparse_int_graph(graph):
    """Copy a graph to a sparse graph.

    .. note :: The resulting graph might have more vertices that the source graph. The reason is 
      that sparse graphs have a continuous range of vertices. Thus, if your input graph contains 
      three vertices 0, 5, and 10 the resulting sparse graph will contain all vertices from 0 up to
      10 (inclusive). The extra vertices will be isolated, meaning that they will not have any incident
      edges.

    .. note :: Sparse graphs are unmodifiable. Attempting to alter one will result in an error 
      being raised.

    :param graph: the input graph
    :returns: a sparse graph 
    :rtype: :class:`jgrapht.types.Graph`
    """
    if len(graph.vertices) == 0:
        raise ValueError("Graph with no vertices")

    max_vertex = max(graph.vertices)
    edgelist = [graph.edge_tuple(e) for e in graph.edges]

    return _create_sparse_int_graph(
        edgelist, max_vertex + 1, graph.type.directed, graph.type.weighted
    )


def _create_int_dag(
    allowing_multiple_edges=False, weighted=True,
):
    """Create a directed acyclic graph.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph`    
    """
    handle = backend.jgrapht_graph_dag_create(allowing_multiple_edges, weighted,)
    return _JGraphTDirectedAcyclicGraph(handle)
