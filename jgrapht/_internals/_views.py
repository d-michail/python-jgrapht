from .. import backend
from .. import GraphBackend
from ..types import GraphType, GraphEvent, ListenableGraph
from ._int_graphs import _JGraphTIntegerGraph
from ._long_graphs import _JGraphTLongGraph
from ._ref_graphs import _JGraphTRefGraph
from ._callbacks import _create_wrapped_callback
from ._callbacks_graph import _create_vertex_or_edge_mask_wrapper
from ._attributes import _VertexAttributes, _EdgeAttributes

import ctypes
import copy


class _UnweightedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unweighted(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnweightedIntegerGraphView(%r)" % self._handle


class _UnweightedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unweighted(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnweightedLongGraphView(%r)" % self._handle


class _UnweightedRefGraphView(_JGraphTRefGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unweighted(graph.handle)
        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnweightedRefGraphView(%r)" % self._handle


class _UndirectedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_undirected(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UndirectedIntegerGraphView(%r)" % self._handle


class _UndirectedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_undirected(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UndirectedLongGraphView(%r)" % self._handle


class _UndirectedRefGraphView(_JGraphTRefGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_undirected(graph.handle)
        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UndirectedRefGraphView(%r)" % self._handle


class _UnmodifiableIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unmodifiable(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnmodifiableIntegerGraphView(%r)" % self._handle


class _UnmodifiableLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unmodifiable(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnmodifiableLongGraphView(%r)" % self._handle


class _UnmodifiableRefGraphView(_JGraphTRefGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_unmodifiable(graph.handle)
        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_UnmodifiableRefGraphView(%r)" % self._handle


class _EdgeReversedIntegerGraphView(_JGraphTIntegerGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_edgereversed(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_EdgeReversedIntegerGraphView(%r)" % self._handle


class _EdgeReversedLongGraphView(_JGraphTLongGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_edgereversed(graph.handle)
        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_EdgeReversedLongGraphView(%r)" % self._handle


class _EdgeReversedRefGraphView(_JGraphTRefGraph):
    def __init__(self, graph):
        handle = backend.jgrapht_xx_graph_as_edgereversed(graph.handle)
        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    def __repr__(self):
        return "_EdgeReversedRefGraphView(%r)" % self._handle


class _MaskedIntegerSubgraphView(_JGraphTIntegerGraph):
    def __init__(self, graph, vertex_mask_cb, edge_mask_cb):

        self._vertex_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, vertex_mask_cb
        )
        self._edge_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, edge_mask_cb
        )

        res = backend.jgrapht_ii_graph_as_masked_subgraph(
            graph.handle,
            self._vertex_mask_wrapper.fptr,
            self._edge_mask_wrapper.fptr,
        )

        super().__init__(res)
        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)

    def __repr__(self):
        return "_MaskedIntegerSubgraphView(%r)" % self._handle


class _MaskedLongSubgraphView(_JGraphTLongGraph):
    def __init__(self, graph, vertex_mask_cb, edge_mask_cb):

        self._vertex_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, vertex_mask_cb
        )
        self._edge_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, edge_mask_cb
        )

        res = backend.jgrapht_ll_graph_as_masked_subgraph(
            graph.handle,
            self._vertex_mask_wrapper.fptr,
            self._edge_mask_wrapper.fptr,
        )

        super().__init__(res)
        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)

    def __repr__(self):
        return "_MaskedLongSubgraphView(%r)" % self._handle


class _MaskedRefSubgraphView(_JGraphTRefGraph):
    def __init__(self, graph, vertex_mask_cb, edge_mask_cb):

        self._vertex_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, vertex_mask_cb
        )
        self._edge_mask_wrapper = _create_vertex_or_edge_mask_wrapper(
            graph, edge_mask_cb
        )

        handle = backend.jgrapht_rr_graph_as_masked_subgraph(
            graph.handle,
            self._vertex_mask_wrapper.fptr,
            self._edge_mask_wrapper.fptr,
        )

        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )
        self._type = graph.type.as_unmodifiable()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)

    def __repr__(self):
        return "_MaskedRefSubgraphView(%r)" % self._handle


class _IntegerWeightedView(_JGraphTIntegerGraph):
    def __init__(self, graph, edge_weight_cb, cache_weights, write_weights_through):

        # Create callbacks and keep a reference
        self._edge_weight_cb_fptr, self._edge_weight_cb = _create_wrapped_callback(
            edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_int)
        )
        handle = backend.jgrapht_xi_graph_as_weighted(
            graph.handle,
            self._edge_weight_cb_fptr,
            cache_weights,
            write_weights_through,
        )

        super().__init__(handle=handle)

        self._type = graph.type.as_weighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_IntegerWeightedView(%r)" % self._handle


class _LongWeightedView(_JGraphTLongGraph):
    def __init__(self, graph, edge_weight_cb, cache_weights, write_weights_through):

        # Create callbacks and keep a reference
        self._edge_weight_cb_fptr, self._edge_weight_cb = _create_wrapped_callback(
            edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_longlong)
        )
        handle = backend.jgrapht_xl_graph_as_weighted(
            graph.handle,
            self._edge_weight_cb_fptr,
            cache_weights,
            write_weights_through,
        )

        super().__init__(handle=handle)

        self._type = graph.type.as_weighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_LongWeightedView(%r)" % self._handle


class _RefWeightedView(_JGraphTRefGraph):
    def __init__(self, graph, edge_weight_cb, cache_weights, write_weights_through):

        # Create callbacks and keep a reference
        self._edge_weight_cb_fptr, self._edge_weight_cb = _create_wrapped_callback(
            edge_weight_cb, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.py_object)
        )
        handle = backend.jgrapht_xr_graph_as_weighted(
            graph.handle,
            self._edge_weight_cb_fptr,
            cache_weights,
            write_weights_through,
        )

        super().__init__(
            handle=handle,
            vertex_supplier_fptr_wrapper=graph._vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=graph._edge_supplier_fptr_wrapper,
            hash_equals_wrapper=graph._hash_equals_wrapper,
        )

        self._type = graph.type.as_weighted()

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # support for graph attributes
        self._graph_attrs = self._graph._graph_attrs
        self._vertex_attrs = _VertexAttributes(self, self._graph._vertex_to_attrs)
        self._edge_attrs = _EdgeAttributes(self, self._graph._edge_to_attrs)        

    @property
    def type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._type

    def __repr__(self):
        return "_RefWeightedView(%r)" % self._handle



class _IntegerGraphUnion(_JGraphTIntegerGraph):
    def __init__(self, graph1, graph2, edge_weight_combiner_cb=None):

        # Create callbacks and keep a reference
        (
            self._edge_weight_combiner_cb_fptr,
            self._edge_weight_combiner_cb,
        ) = _create_wrapped_callback(
            edge_weight_combiner_cb,
            ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double),
        )

        # create graph union at the backend
        handle = backend.jgrapht_xx_graph_as_graph_union(
            graph1.handle, graph2.handle, self._edge_weight_combiner_cb_fptr
        )

        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph1 = graph1
        self._graph2 = graph2


class _LongGraphUnion(_JGraphTLongGraph):
    def __init__(self, graph1, graph2, edge_weight_combiner_cb=None):

        # Create callbacks and keep a reference
        (
            self._edge_weight_combiner_cb_fptr,
            self._edge_weight_combiner_cb,
        ) = _create_wrapped_callback(
            edge_weight_combiner_cb,
            ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double),
        )

        # create graph union at the backend
        handle = backend.jgrapht_xx_graph_as_graph_union(
            graph1.handle, graph2.handle, self._edge_weight_combiner_cb_fptr
        )

        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph1 = graph1
        self._graph2 = graph2


class _RefGraphUnion(_JGraphTRefGraph):
    def __init__(self, graph1, graph2, edge_weight_combiner_cb=None):

        # Create callbacks and keep a reference
        (
            self._edge_weight_combiner_cb_fptr,
            self._edge_weight_combiner_cb,
        ) = _create_wrapped_callback(
            edge_weight_combiner_cb,
            ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double),
        )

        # create graph union at the backend
        handle = backend.jgrapht_xx_graph_as_graph_union(
            graph1.handle, graph2.handle, self._edge_weight_combiner_cb_fptr
        )

        super().__init__(handle=handle)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph1 = graph1
        self._graph2 = graph2


class _ListenableView(_JGraphTIntegerGraph, ListenableGraph):
    def __init__(self, graph):
        res = backend.jgrapht_xx_listenable_as_listenable(graph.handle)
        super().__init__(res)

        # Keep a reference to avoid gargage collection. This is important since the
        # same references are maintained inside the JVM. If the graph gets garbaged
        # collected here, the same will happen inside the JVM.
        self._graph = graph

        # list of user-added listeners
        self._listeners = {}
        self._next_id = 0

    def add_listener(self, listener_cb):
        def actual_cb(element, event_type):
            # convert integer event type to enum
            listener_cb(element, GraphEvent(event_type))

        if self._graph._backend_type == GraphBackend.INT_GRAPH:
            cb_fptr, cb = _create_wrapped_callback(
                actual_cb, ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
            )
            listener_handle = backend.jgrapht_ii_listenable_create_graph_listener(
                cb_fptr
            )
        elif self._graph._backend_type == GraphBackend.LONG_GRAPH:
            cb_fptr, cb = _create_wrapped_callback(
                actual_cb, ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_longlong)
            )
            listener_handle = backend.jgrapht_ll_listenable_create_graph_listener(
                cb_fptr
            )
        else:
            raise ValueError("TODO: write rr graph")

        backend.jgrapht_xx_listenable_add_graph_listener(self.handle, listener_handle)

        # create listener identifier
        listener_id = self._next_id
        self._next_id += 1

        # register and make sure to keep the actual callback around to
        # avoid garbage collection
        self._listeners[listener_id] = (listener_handle, cb)

        return listener_id

    def remove_listener(self, listener_id):
        listener_handle, cb = self._listeners.pop(listener_id)

        backend.jgrapht_xx_listenable_remove_graph_listener(
            self.handle, listener_handle
        )
        backend.jgrapht_handles_destroy(listener_handle)

    def __repr__(self):
        return "_ListenableView(%r)" % self._handle
