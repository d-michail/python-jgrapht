from .. import backend
from ..types import GraphType, GraphEvent
from ._graphs import _JGraphTGraph
from ._callbacks import _create_wrapped_callback

import ctypes


class _ListenableView(_JGraphTGraph):

    def __init__(self, graph):
        res = backend.jgrapht_listenable_as_listenable(graph.handle)
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

        cb_fptr, cb = _create_wrapped_callback(
            actual_cb, ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
        )

        listener_handle = backend.jgrapht_listenable_create_graph_listener(cb_fptr)
        backend.jgrapht_listenable_add_graph_listener(self.handle, listener_handle)

        # create listener identifier
        listener_id = self._next_id
        self._next_id += 1

        # register and make sure to keep the actual callback around to 
        # avoid garbage collection
        self._listeners[listener_id] = (listener_handle, cb)

        return listener_id

    def remove_listener(self, listener_id):
        listener_handle, cb = self._listeners.pop(listener_id)

        backend.jgrapht_listenable_remove_graph_listener(self.handle, listener_handle)
        backend.jgrapht_handles_destroy(listener_handle)
        

