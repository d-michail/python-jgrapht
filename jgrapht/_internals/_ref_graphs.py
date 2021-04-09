from collections import defaultdict
from collections.abc import Set

from .. import backend
from ..types import (
    Graph,
    GraphType,
    DirectedAcyclicGraph,
    AttributesGraph,
)

from ._collections_set import (
    _JGraphTRefSet,
)

import ctypes
from . import _callbacks, _ref_utils, _ref_hashequals
from ._wrappers import _HandleWrapper, _JGraphTRefIterator, GraphBackend
from ._attributes import _VertexAttributes, _EdgeAttributes


class _JGraphTRefGraph(_HandleWrapper, Graph, AttributesGraph):
    """The ref graph implementation. A graph which allows the use of any hashable as vertex
    and edges.

    The actual implementation uses maps python hashables using their ids. The reference count
    of each hashable is increased by one when it is inserted in the graph and decreased by one
    when it is removed from the graph. This means that all intermediate results (e.g. such as
    a vertex set returns from a vertex cover algorithm) need to be translated into Python
    collections, to keep a positive reference count even when vertices or edges removed from
    the graph.

    Additionally, user vertex and edge suppliers are called directly from the JVM in order
    to construct new vertices and edges when needed.

    The implementation delegates the hashCode and equals methods in the JVM to the hash and __eq__
    methods in Python.

    Do not construct this instance directly, look at the corresponding factory method for the
    right way to initialize this object.
    """

    def __init__(
        self,
        handle,
        vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper,
        hash_equals_wrapper,
        **kwargs
    ):
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

        self._vertex_ref_count = _ref_utils._SingleRefCount()
        self._edge_ref_count = _ref_utils._SingleRefCount()

        # support for graph attributes
        self._graph_attrs = dict()
        self._vertex_to_attrs = defaultdict(lambda: {})
        self._vertex_attrs = _VertexAttributes(self, self._vertex_to_attrs)
        self._edge_to_attrs = defaultdict(lambda: {})
        self._edge_attrs = _EdgeAttributes(self, self._edge_to_attrs)

        # keep ctypes callbacks from being garbage collected
        self._vertex_supplier_fptr_wrapper = vertex_supplier_fptr_wrapper
        self._edge_supplier_fptr_wrapper = edge_supplier_fptr_wrapper
        self._hash_equals_wrapper = hash_equals_wrapper

    @property
    def type(self):
        return self._type

    @property
    def _backend_type(self):
        return GraphBackend.REF_GRAPH

    def add_vertex(self, vertex=None):
        if vertex is not None:
            if backend.jgrapht_rx_graph_add_given_vertex(self._handle, id(vertex)):
                self._vertex_ref_count.inc(vertex)
        else:
            v_ptr = backend.jgrapht_rx_graph_add_vertex(self._handle)
            vertex = _ref_utils._swig_ptr_to_obj(v_ptr)
            self._vertex_ref_count.inc(vertex)
        return vertex

    def remove_vertex(self, v):
        if v is None:
            raise ValueError("Vertex cannot be None")
        removed = backend.jgrapht_rx_graph_remove_vertex(self._handle, id(v))
        if removed:
            self._vertex_ref_count.dec(v)
            self._vertex_attrs._unsafe_delitem(v)

    def contains_vertex(self, v):
        return backend.jgrapht_rx_graph_contains_vertex(self._handle, id(v))

    def add_edge(self, u, v, weight=None, edge=None):
        if edge is not None:
            e_ptr = id(edge)
            if backend.jgrapht_rr_graph_add_given_edge(
                self._handle, id(u), id(v), e_ptr
            ):
                self._edge_ref_count.inc(edge)
                if weight is not None:
                    backend.jgrapht_xr_graph_set_edge_weight(
                        self._handle, e_ptr, weight
                    )
        else:
            e_ptr = backend.jgrapht_rr_graph_add_edge(self._handle, id(u), id(v))
            edge = _ref_utils._swig_ptr_to_obj(e_ptr)
            self._edge_ref_count.inc(edge)
            if weight is not None:
                backend.jgrapht_xr_graph_set_edge_weight(self._handle, id(edge), weight)
        return edge

    def remove_edge(self, e):
        if e is None:
            raise ValueError("Edge cannot be None")
        if backend.jgrapht_xr_graph_remove_edge(self._handle, id(e)):
            self._edge_ref_count.dec(e)
            self._edge_attrs._unsafe_delitem(e)
            return True
        else:
            return False

    def contains_edge(self, e):
        return backend.jgrapht_xr_graph_contains_edge(self._handle, id(e))

    def contains_edge_between(self, u, v):
        return backend.jgrapht_rx_graph_contains_edge_between(
            self._handle, id(u), id(v)
        )

    def degree_of(self, v):
        return backend.jgrapht_rx_graph_degree_of(self._handle, id(v))

    def indegree_of(self, v):
        return backend.jgrapht_rx_graph_indegree_of(self._handle, id(v))

    def outdegree_of(self, v):
        return backend.jgrapht_rx_graph_outdegree_of(self._handle, id(v))

    def edge_source(self, e):
        v_ptr = backend.jgrapht_rr_graph_edge_source(self._handle, id(e))
        return _ref_utils._swig_ptr_to_obj(v_ptr)

    def edge_target(self, e):
        v_ptr = backend.jgrapht_rr_graph_edge_target(self._handle, id(e))
        return _ref_utils._swig_ptr_to_obj(v_ptr)

    def get_edge_weight(self, e):
        return backend.jgrapht_xr_graph_get_edge_weight(self._handle, id(e))

    def set_edge_weight(self, e, weight):
        backend.jgrapht_xr_graph_set_edge_weight(self._handle, id(e), weight)

    @property
    def number_of_vertices(self):
        return backend.jgrapht_xx_graph_vertices_count(self._handle)

    @property
    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    @property
    def number_of_edges(self):
        return backend.jgrapht_xx_graph_edges_count(self._handle)

    @property
    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        it = backend.jgrapht_rx_graph_create_between_eit(self._handle, id(u), id(v))
        return _JGraphTRefIterator(it)

    def edges_of(self, v):
        it = backend.jgrapht_rx_graph_vertex_create_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def inedges_of(self, v):
        it = backend.jgrapht_rx_graph_vertex_create_in_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def outedges_of(self, v):
        it = backend.jgrapht_rx_graph_vertex_create_out_eit(self._handle, id(v))
        return _JGraphTRefIterator(it)

    def __repr__(self):
        return "_JGraphTRefGraph(%r)" % self._handle

    @property
    def graph_attrs(self):
        return self._graph_attrs

    @property
    def vertex_attrs(self):
        return self._vertex_attrs

    @property
    def edge_attrs(self):
        return self._edge_attrs

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_xx_graph_create_all_vit(self._handle)
            return _JGraphTRefIterator(res)

        def __len__(self):
            return backend.jgrapht_xx_graph_vertices_count(self._handle)

        def __contains__(self, v):
            return backend.jgrapht_rx_graph_contains_vertex(self._handle, id(v))

        def __repr__(self):
            return "_JGraphTRefGraph-VertexSet(%r)" % self._handle

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
            return _JGraphTRefIterator(res)

        def __len__(self):
            return backend.jgrapht_xx_graph_edges_count(self._handle)

        def __contains__(self, e):
            return backend.jgrapht_xr_graph_contains_edge(self._handle, id(e))

        def __repr__(self):
            return "_JGraphTRefGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)

    def __del__(self):
        self._vertex_ref_count.dec_all()
        self._edge_ref_count.dec_all()
        super().__del__()


class _JGraphTRefDirectedAcyclicGraph(_JGraphTRefGraph, DirectedAcyclicGraph):
    """The directed acyclic graph wrapper."""

    def __init__(
        self,
        handle,
        vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper,
        hash_equals_wrapper,
        **kwargs
    ):
        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
            hash_equals_wrapper=hash_equals_wrapper,
            **kwargs
        )

    def descendants(self, vertex):
        set_handle = backend.jgrapht_rx_graph_dag_vertex_descendants(
            self.handle, id(vertex)
        )
        return _JGraphTRefSet(
            handle=set_handle,
            hash_equals_resolver_handle=self._hash_equals_wrapper.handle,
        )

    def ancestors(self, vertex):
        set_handle = backend.jgrapht_rx_graph_dag_vertex_ancestors(
            self.handle, id(vertex)
        )
        return _JGraphTRefSet(
            handle=set_handle,
            hash_equals_resolver_handle=self._hash_equals_wrapper.handle,
        )

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_dag_topological_it(self.handle)
        return _JGraphTRefIterator(handle=it_handle)


def _create_ref_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a graph with any reference as vertices/edges.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    # create vertex supplier
    vertex_supplier_fptr_wrapper = _callbacks._create_py_object_supplier(
        supplier=vertex_supplier
    )
    # create edge supplier
    edge_supplier_fptr_wrapper = _callbacks._create_py_object_supplier(
        supplier=edge_supplier
    )

    # create python hash-equals ctypes wrappers and setup JVM object
    hash_equals_wrapper = _ref_hashequals._get_hash_equals_wrapper()

    handle = backend.jgrapht_rr_graph_create(
        directed,
        allowing_self_loops,
        allowing_multiple_edges,
        weighted,
        vertex_supplier_fptr_wrapper.fptr,
        edge_supplier_fptr_wrapper.fptr,
        hash_equals_wrapper.handle,
    )

    return _JGraphTRefGraph(
        handle,
        vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
        hash_equals_wrapper=hash_equals_wrapper,
    )


def _create_ref_dag(
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a directed acyclic graph.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph`
    """
    # create vertex supplier
    vertex_supplier_fptr_wrapper = _callbacks._create_py_object_supplier(
        supplier=vertex_supplier
    )
    # create edge supplier
    edge_supplier_fptr_wrapper = _callbacks._create_py_object_supplier(
        supplier=edge_supplier
    )

    # create python hash-equals ctypes wrappers and setup JVM object
    hash_equals_wrapper = _ref_hashequals._get_hash_equals_wrapper()

    handle = backend.jgrapht_rr_graph_dag_create(
        allowing_multiple_edges,
        weighted,
        vertex_supplier_fptr_wrapper.fptr,
        edge_supplier_fptr_wrapper.fptr,
        hash_equals_wrapper.handle,
    )

    return _JGraphTRefDirectedAcyclicGraph(
        handle,
        vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
        edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
        hash_equals_wrapper=hash_equals_wrapper,
    )


def _is_ref_graph(graph):
    """Check if a graph instance is a ref graph.

    :param graph: the graph
    :returns: True if the graph is a ref graph, False otherwise.
    """
    return isinstance(graph, (_JGraphTRefGraph))
