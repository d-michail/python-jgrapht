from .. import backend
from ..types import PlanarEmbedding

from ._wrappers import (
    _HandleWrapper,
)

from ._attrsg import vertex_attrsg_to_g as _vertex_attrsg_to_g
from ._attrsg_wrappers import _AttributesGraphEdgeIterator


class _AttributesGraphPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """An attributes graph planar embedding."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def edges_around(self, vertex):
        vertex = _vertex_attrsg_to_g(self._graph, vertex)
        res = backend.jgrapht_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_AttributesGraphEdgeIterator(res, self._graph))

    def __repr__(self):
        return "_AttributesGraphPlanarEmbedding(%r)" % self._handle
