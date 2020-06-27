from .. import backend

from ._drawing import _JGraphTLayoutModel2D
from ._anyhashableg import (
    _is_anyhashable_graph,
    _vertex_anyhashableg_to_g,
)


class _AnyHashableGraphLayoutModel2D(_JGraphTLayoutModel2D):
    """A 2D layout model."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_vertex_location(self, vertex):
        vertex = _vertex_anyhashableg_to_g(self._graph, vertex)
        return super().get_vertex_location(vertex)

    def set_vertex_location(self, vertex, point_2d):
        vertex = _vertex_anyhashableg_to_g(self._graph, vertex)
        super().set_vertex_location(vertex, point_2d)

    def is_fixed(self, vertex):
        vertex = _vertex_anyhashableg_to_g(self._graph, vertex)
        return super().is_fixed(vertex)

    def set_fixed(self, vertex, fixed):
        vertex = _vertex_anyhashableg_to_g(self._graph, vertex)
        super().set_fixed(vertex, fixed)

    def __repr__(self):
        return "_AnyHashableGraphLayoutModel2D(%r)" % self._handle


def _create_anyhashable_graph_layout_model_2d(graph, min_x, min_y, width, height):
    """Factory for a 2d layout model."""
    if not _is_anyhashable_graph(graph):
        raise ValueError("Graph must be an any-hashable graph")
    handle = backend.jgrapht_drawing_layout_model_2d_create(min_x, min_y, width, height)
    return _AnyHashableGraphLayoutModel2D(handle, graph)
