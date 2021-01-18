from .. import backend
from ..types import PlanarEmbedding
from ._wrappers import (
    _HandleWrapper,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
)


class _JGraphTIntegerPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def edges_around(self, vertex):
        res = backend.jgrapht_ii_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_JGraphTIntegerIterator(res))

    def __repr__(self):
        return "_JGraphTIntegerPlanarEmbedding(%r)" % self._handle


class _JGraphTLongPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def edges_around(self, vertex):
        res = backend.jgrapht_ll_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_JGraphTLongIterator(res))

    def __repr__(self):
        return "_JGraphTLongPlanarEmbedding(%r)" % self._handle