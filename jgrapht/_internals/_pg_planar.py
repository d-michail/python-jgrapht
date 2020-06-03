from .. import backend
from ..types import PlanarEmbedding

from ._wrappers import (
    _HandleWrapper,
)

from ._pg import vertex_pg_to_g as _vertex_pg_to_g
from ._pg_wrappers import _PropertyGraphEdgeIterator


class _PropertyGraphPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A property graph planar embedding."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def edges_around(self, vertex):
        vertex = _vertex_pg_to_g(self._graph, vertex)
        res = backend.jgrapht_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_PropertyGraphEdgeIterator(res, self._graph))

    def __repr__(self):
        return "_PropertyGraphPlanarEmbedding(%r)" % self._handle
