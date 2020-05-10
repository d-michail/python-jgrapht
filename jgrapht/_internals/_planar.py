from .. import backend
from ..types import (
    PlanarEmbedding, 
)
from ._wrappers import (
    _HandleWrapper,
    _JGraphTLongIterator,
)


class _JGraphTPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def edges_around(self, vertex):
        res = backend.jgrapht_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_JGraphTLongIterator(res))

    def __repr__(self):
        return "_JGraphTPlanarEmbedding(%r)" % self._handle

