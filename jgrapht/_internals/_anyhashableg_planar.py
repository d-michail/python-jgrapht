from .. import backend
from ..types import PlanarEmbedding

from ._wrappers import _HandleWrapper

from ._anyhashableg import _vertex_anyhashableg_to_g
from ._anyhashableg_wrappers import _AnyHashableGraphEdgeIterator


class _AnyHashableGraphPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """An any-hashable graph planar embedding."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def edges_around(self, vertex):
        vertex = _vertex_anyhashableg_to_g(self._graph, vertex)
        res = backend.jgrapht_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_AnyHashableGraphEdgeIterator(res, self._graph))

    def __repr__(self):
        return "_AnyHashableGraphPlanarEmbedding(%r)" % self._handle
