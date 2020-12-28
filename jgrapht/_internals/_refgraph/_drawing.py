from ... import backend

from .._intgraph._drawing import _JGraphTLongLayoutModel2D
from ._graphs import (
    _is_refcount_graph, 
)


class _RefCountGraphLayoutModel2D(_JGraphTLongLayoutModel2D):
    """A 2D layout model."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_vertex_location(self, vertex):
        return super().get_vertex_location(id(vertex))

    def set_vertex_location(self, vertex, point_2d):
        super().set_vertex_location(id(vertex), point_2d)

    def is_fixed(self, vertex):
        return super().is_fixed(id(vertex))

    def set_fixed(self, vertex, fixed):
        super().set_fixed(id(vertex), fixed)

    def __repr__(self):
        return "_RefCountGraphLayoutModel2D(%r)" % self._handle


def _create_refcount_graph_layout_model_2d(graph, min_x, min_y, width, height):
    """Factory for a 2d layout model."""
    if not _is_refcount_graph(graph):
        raise ValueError("Graph must be a refcount graph")
    handle = backend.jgrapht_xx_drawing_layout_model_2d_create(min_x, min_y, width, height)
    return _RefCountGraphLayoutModel2D(handle, graph)
