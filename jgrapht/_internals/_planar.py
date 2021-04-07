from .. import backend
from ..types import PlanarEmbedding
from ._wrappers import (
    _HandleWrapper,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
    _JGraphTRefIterator,
)


class _JGraphTIntegerPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def edges_around(self, vertex):
        res = backend.jgrapht_ix_planarity_embedding_edges_around_vertex(
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
        res = backend.jgrapht_lx_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_JGraphTLongIterator(res))

    def __repr__(self):
        return "_JGraphTLongPlanarEmbedding(%r)" % self._handle


class _JGraphTRefPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def edges_around(self, vertex):
        res = backend.jgrapht_rx_planarity_embedding_edges_around_vertex(
            self._handle, id(vertex), self._hash_equals_resolver_handle
        )
        return list(_JGraphTRefIterator(res))

    def __repr__(self):
        return "_JGraphTRefPlanarEmbedding(%r)" % self._handle
