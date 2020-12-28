from collections.abc import (
    Set,
)

from ... import backend
from ...types import (
    Graph,
    GraphType,
    DirectedAcyclicGraph,
)
from .._wrappers import _HandleWrapper
from .._callbacks import _create_wrapped_long_supplier_callback
from ._refcount import _inc_ref, _dec_ref, _id_to_obj, _map_ids_to_objs
from .._collections import (
    _JGraphTLongIterator,
    _JGraphTLongSet,
)


class _RefCountGraph(_HandleWrapper, Graph):
    """A graph which allows the use of any hashable as vertex and edges.

    The actual implementation uses a long graph and maps python hashables using their ids.
    The reference count of each hashable is increased by one when it is inserted in the graph
    and decreased by one when it is removed from the graph. This means that all intermediate
    results (e.g. such as a vertex set returns from a vertex cover algorithm) need to be
    translated into Python collections, to keep a positive reference count even on vertices or
    edges removed from the graph.

    Additionally, user vertex and edge suppliers are called directly from the JVM in order 
    to construct new vertices and edges when needed.

    Do not construct this instance directly, look at the corresponding factory method for the 
    right way to initialize this object.
    """

    def __init__(self, handle, vertex_supplier_cb, edge_supplier_cb, **kwargs):
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
        self._vertex_supplier_cb = vertex_supplier_cb
        self._edge_supplier_cb = edge_supplier_cb

    @property
    def type(self):
        return self._type

    def add_vertex(self, vertex=None):
        if vertex is not None:
            vid = id(vertex)
            if backend.jgrapht_ll_graph_add_given_vertex(self._handle, vid):
                _inc_ref(vertex)
        else:
            # no refcount increment as the  edge supplier increments the refcount 
            vid = backend.jgrapht_ll_graph_add_vertex(self._handle)
            vertex = _id_to_obj(vid)
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
        if edge is not None:
            eid = id(edge)
            if backend.jgrapht_ll_graph_add_given_edge(self._handle, id(u), id(v), eid):
                _inc_ref(edge)
                if weight is not None:
                    backend.jgrapht_ll_graph_set_edge_weight(self._handle, eid, weight)
        else:
            # no refcount increment as the  edge supplier increments the refcount 
            eid = backend.jgrapht_ll_graph_add_edge(self._handle, id(u), id(v))    
            edge = _id_to_obj(eid)
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
        return "_RefCountGraph(%r)" % self.handle

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
            return "_RefCountGraph-VertexSet(%r)" % self._handle

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
            return "_RefCountGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)


class _RefCountDirectedAcyclicGraph(_RefCountGraph, DirectedAcyclicGraph):
    """The directed acyclic refcount graph wrapper."""

    def __init__(self, handle, vertex_supplier_cb, edge_supplier_cb, **kwargs):
        """Initialize a refcount dag.

        :param handle: the actual graph which we are wrapping. Must have long
          vertices and edges.
        """
        super().__init__(
            handle=handle,
            vertex_supplier_cb=vertex_supplier_cb,
            edge_supplier_cb=edge_supplier_cb,
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
        return "_RefCountDirectedAcyclicGraph(%r)" % self.handle


def _default_supplier():
    return object()


def _create_refcount_graph(
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

    if vertex_supplier is None:
        vertex_supplier = _default_supplier
    if edge_supplier is None:
        edge_supplier = _default_supplier

    def actual_vertex_supplier():
        v = vertex_supplier()
        _inc_ref(v)
        return id(v)

    def actual_edge_supplier():
        e = edge_supplier()
        _inc_ref(e)
        return id(e)

    vf_ptr, vf = _create_wrapped_long_supplier_callback(actual_vertex_supplier)
    ef_ptr, ef = _create_wrapped_long_supplier_callback(actual_edge_supplier)

    handle = backend.jgrapht_ll_graph_create_with_suppliers(
        directed, allowing_self_loops, allowing_multiple_edges, weighted, vf_ptr, ef_ptr
    )
    return _RefCountGraph(
        handle, vertex_supplier_cb=vf, edge_supplier_cb=ef
    )


def _create_refcount_dag(
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a directed acyclic refcount graph.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph` and :class:`~jgrapht.types.Graph`
    """
    if vertex_supplier is None:
        vertex_supplier = _default_supplier
    if edge_supplier is None:
        edge_supplier = _default_supplier

    def actual_vertex_supplier(): 
        v = vertex_supplier()
        _inc_ref(v)
        return id(v)

    def actual_edge_supplier():
        e = edge_supplier()
        _inc_ref(e)
        return id(e)

    vf_ptr, vf = _create_wrapped_long_supplier_callback(actual_vertex_supplier)
    ef_ptr, ef = _create_wrapped_long_supplier_callback(actual_edge_supplier)

    handle = backend.jgrapht_ll_graph_dag_create_with_suppliers(
        allowing_multiple_edges,
        weighted,
        vf_ptr,
        ef_ptr
    )
    return _RefCountDirectedAcyclicGraph(
        handle, vertex_supplier_cb=vf, edge_supplier_cb=ef
    )


def _is_refcount_graph(graph):
    """Check if a graph instance is a refcount graph.

    :param graph: the graph
    :returns: True if the graph is a refcount graph, False otherwise.
    """
    return isinstance(graph, (_RefCountGraph))
