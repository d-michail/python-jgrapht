from collections.abc import (
    Set,
)

from jgrapht import backend
from jgrapht.types import (
    Graph,
    GraphType,
    DirectedAcyclicGraph,
)
from jgrapht._internals._wrappers import _HandleWrapper
from ._refcount import _inc_ref, _inc_ref_by_id, _dec_ref, _dec_ref_by_id, _id_to_obj, _map_ids_to_objs
from jgrapht._internals._collections import (
    _JGraphTLongIterator,
    _JGraphTLongSet,
)


class _RefCountAnyHashableGraph(_HandleWrapper, Graph):
    """A graph which allows the use of any hashable as vertex and edges. 
    
    The actual implementation uses a long graph and maps python hashables using their ids.
    The reference count of each hashable is increased by one when it is inserted in the graph
    and decreased by one when it is removed from the graph. This means that all intermediate 
    results (e.g. such as a vertex set returns from a vertex cover algorithm) need to be 
    translated into Python collections (to keep a correct reference count).
    """

    def __init__(self, handle, vertex_supplier=None, edge_supplier=None, **kwargs):
        super().__init__(handle=handle, **kwargs)

        # read attributes from backend
        directed = backend.jgrapht_xx_graph_is_directed(self._handle)
        allowing_self_loops = backend.jgrapht_xx_graph_is_allowing_selfloops(
            self._handle
        )
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

        # initialize suppliers
        if vertex_supplier is None:
            vertex_supplier = lambda: object()
        self._vertex_supplier = vertex_supplier
        if edge_supplier is None:
            edge_supplier = lambda: object()
        self._edge_supplier = edge_supplier

    @property
    def type(self):
        return self._graph.type

    @property
    def vertex_supplier(self):
        """The vertex supplier."""
        return self._vertex_supplier

    @property
    def edge_supplier(self):
        """The edge supplier."""
        return self._edge_supplier

    def add_vertex(self, vertex=None):
        if vertex is not None:
            vid = id(vertex)
            if backend.jgrapht_ll_graph_contains_vertex(self._handle, vid):
                return vertex
        else:
            vertex = self._vertex_supplier()
            vid = id(vertex)
            if backend.jgrapht_ll_graph_contains_vertex(self._handle, vid):
                raise ValueError(
                    "Vertex supplier returns vertices already in the graph"
                )
        if backend.jgrapht_ll_graph_add_given_vertex(self._handle, vid):
            _inc_ref(vertex)
        return vertex

    def remove_vertex(self, v):
        if v is None:
            raise ValueError("Vertex cannot be None")
        vid = id(v)
        if backend.jgrapht_ll_graph_remove_vertex(self._handle, vid):
            _dec_ref(v)

    def contains_vertex(self, v):
        return backend.jgrapht_ll_graph_remove_vertex(self._handle, id(v))

    def add_edge(self, u, v, weight=None, edge=None):
        if edge is None:
            edge = self._edge_supplier()
        eid = id(edge)
        if backend.jgrapht_ll_graph_add_given_edge(self._handle, id(u), id(v), eid):
            _inc_ref(edge)
        if weight is not None:
            backend.jgrapht_ll_graph_set_edge_weight(self._handle, eid, weight)
        return edge

    def remove_edge(self, e):
        if e is None:
            raise ValueError("Edge cannot be None")
        eid = id(e)
        if backend.jgrapht_ll_graph_remove_edge(self._handle, eid):
            _dec_ref(e)
            return True
        else:
            return False

    def contains_edge(self, e):
        return backend.jgrapht_ll_graph_contains_edge(self._handle, id(e))

    def contains_edge_between(self, u, v):
        return backend.jgrapht_ll_graph_contains_edge_between(
            self._handle, id(u), id(v)
        )

    def degree_of(self, v):
        return backend.jgrapht_ll_graph_degree_of(self._handle, id(v))

    def indegree_of(self, v):
        return backend.jgrapht_ll_graph_indegree_of(self._handle, id(v))

    def outdegree_of(self, v):
        return backend.jgrapht_ll_graph_outdegree_of(self._handle, id(v))

    def edge_source(self, e):
        vid = backend.jgrapht_ll_graph_edge_source(self._handle, id(e))
        return _id_to_obj(vid)

    def edge_target(self, e):
        vid = backend.jgrapht_ll_graph_edge_target(self._handle, id(e))
        return _id_to_obj(vid)

    def get_edge_weight(self, e):
        return backend.jgrapht_ll_graph_get_edge_weight(self._handle, id(e))

    def set_edge_weight(self, e, weight):
        backend.jgrapht_ll_graph_set_edge_weight(self._handle, id(e), weight)

    @property
    def number_of_vertices(self):
        return backend.jgrapht_ll_graph_vertices_count(self._handle)

    @property
    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    @property
    def number_of_edges(self):
        return backend.jgrapht_ll_graph_edges_count(self._handle)

    @property
    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        it = backend.jgrapht_ll_graph_create_between_eit(self._handle, id(u), id(v))
        return _map_ids_to_objs(_JGraphTLongIterator(it))

    def edges_of(self, v):
        it = backend.jgrapht_ll_graph_vertex_create_eit(self._handle, id(v))
        return _map_ids_to_objs(_JGraphTLongIterator(it))

    def inedges_of(self, v):
        it = backend.jgrapht_ll_graph_vertex_create_in_eit(self._handle, id(v))
        return _map_ids_to_objs(_JGraphTLongIterator(it))

    def outedges_of(self, v):
        it = backend.jgrapht_ll_graph_vertex_create_out_eit(self._handle, id(v))
        return _map_ids_to_objs(_JGraphTLongIterator(it))

    def __repr__(self):
        return "_RefCountAnyHashableGraph(%r)" % self.handle

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_vit(self._handle)
            return _map_ids_to_objs(_JGraphTLongIterator(res))

        def __len__(self):
            return backend.jgrapht_ll_graph_vertices_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_ll_graph_contains_vertex(self._handle, id(v))

        def __repr__(self):
            return "_RefCountAnyHashableGraph-VertexSet(%r)" % self._handle

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
            return _map_ids_to_objs(_JGraphTLongIterator(res))

        def __len__(self):
            return backend.jgrapht_ll_graph_edges_count(self._handle)

        def __contains__(self, e):
            return backend.jgrapht_ll_graph_contains_edge(self._handle, id(e))

        def __repr__(self):
            return "_RefCountAnyHashableGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)


class _RefCountAnyHashableGraphDirectedAcyclicGraph(_RefCountAnyHashableGraph, DirectedAcyclicGraph):
    """The directed acyclic graph wrapper."""

    def __init__(self, handle, vertex_supplier=None, edge_supplier=None, **kwargs):
        """Initialize an any-hashable dag with refcounts.

        :param handle: the actual graph which we are wrapping. Must have long 
          vertices and edges.
        :param vertex_supplier: function which returns new vertices on each call. If
          None then object instances are used.
        :param edge_supplier: function which returns new edge on each call. If
          None then object instances are used.
        """
        super().__init__(
            handle=handle,
            vertex_supplier=vertex_supplier,
            edge_supplier=edge_supplier,
            **kwargs
        )

    def descendants(self, v):
        set_handle = backend.jgrapht_ll_graph_dag_vertex_descendants(self.handle, id(v))
        return _map_ids_to_objs(_JGraphTLongSet(handle=set_handle))
    
    def ancestors(self, v):
        set_handle = backend.jgrapht_ll_graph_dag_vertex_ancestors(self.handle, id(v))
        return _map_ids_to_objs(_JGraphTLongSet(handle=set_handle))

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_dag_topological_it(self.handle)
        return _map_ids_to_objs(_JGraphTLongIterator(handle=it_handle))

    def __repr__(self):
        return "_RefCountAnyHashableGraphDirectedAcyclicGraph(%r)" % self.handle


def _create_refcount_anyhashable_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a graph with any hashable as a vertex or edge using refcounts.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edges on each call. If
        None then object instances are used.    
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    handle = backend.jgrapht_ll_graph_create(
        directed, allowing_self_loops, allowing_multiple_edges, weighted
    )
    return _RefCountAnyHashableGraph(
        handle, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )


def _create_refcount_anyhashable_dag(
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a directed acyclic any-hashable graph and refcounts.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.        
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph` and :class:`~jgrapht.types.Graph`
    """
    handle = backend.jgrapht_ll_graph_dag_create(allowing_multiple_edges, weighted,)
    return _RefCountAnyHashableGraphDirectedAcyclicGraph(
        handle, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )


def _is_refcount_anyhashable_graph(graph):
    """Check if a graph instance is an any-hashable using refcounts and the
    long graph as a backend.

    :param graph: the graph
    :returns: True if the graph is an any-hashable graph using refcounts, False otherwise.
    """
    return isinstance(graph, (_RefCountAnyHashableGraph))
