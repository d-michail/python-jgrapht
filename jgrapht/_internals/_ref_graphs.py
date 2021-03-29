from .. import backend
from ..types import (
    Graph,
    GraphType,
)

from ._wrappers import _HandleWrapper
import ctypes
from . import _refcount


#class _JGraphTRefGraph(_HandleWrapper, Graph):
class _JGraphTRefGraph(_HandleWrapper):
    """The ref graph implementation.
    """

    def __init__(self, handle, **kwargs):
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

    @property
    def type(self):
        return self._type

    def add_vertex(self, vertex=None):
        if vertex is not None:
            added = backend.jgrapht_rr_graph_add_given_vertex(self._handle, vertex)
            if added: 
                _refcount._inc_ref(vertex)
        else:
            vertex = backend.jgrapht_rr_graph_add_vertex(self._handle)
            _refcount._inc_ref(vertex)
        return vertex

    def remove_vertex(self, v):
        removed = backend.jgrapht_rr_graph_remove_vertex(self._handle, v)
        if removed: 
            _refcount._dec_ref(v)

    def contains_vertex(self, v):
        return backend.jgrapht_rr_graph_contains_vertex(self._handle, v)

    def __repr__(self):
        return "_JGraphTRefGraph(%r)" % self._handle


def _fallback_vertex_supplier():
    return object()


def _fallback_edge_supplier():
    return object()


def _hash_lookup(o):
    """TODO
    """
    return 0


def _equals_lookup(o):
    """TODO
    """
    return 0


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
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """

    if vertex_supplier is None:
        vertex_supplier = _fallback_vertex_supplier
    vertex_supplier_type = ctypes.CFUNCTYPE(ctypes.py_object)
    vertex_supplier_fptr_wrapper = _refcount._CallbackWrapper(
        vertex_supplier, vertex_supplier_type
    )

    if edge_supplier is None:
        edge_supplier = _fallback_edge_supplier
    edge_supplier_type = ctypes.CFUNCTYPE(ctypes.py_object)
    edge_supplier_fptr_wrapper = _refcount._CallbackWrapper(
        edge_supplier, edge_supplier_type
    )

    hash_lookup_fptr_wrapper = _refcount._CallbackWrapper(
        _hash_lookup, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    )

    equals_lookup_fptr_wrapper = _refcount._CallbackWrapper(
        _equals_lookup, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    )

    handle = backend.jgrapht_rr_graph_create(
        directed,
        allowing_self_loops,
        allowing_multiple_edges,
        weighted,
        vertex_supplier_fptr_wrapper.fptr,
        edge_supplier_fptr_wrapper.fptr,
        hash_lookup_fptr_wrapper.fptr,
        equals_lookup_fptr_wrapper.fptr,
    )

    return _JGraphTRefGraph(handle)
