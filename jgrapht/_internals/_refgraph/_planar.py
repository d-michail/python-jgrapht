from ... import backend
from ...types import PlanarEmbedding
from .._wrappers import _HandleWrapper
from .._collections import _JGraphTLongIterator
from .._refcount import _map_ids_to_objs


class _RefCountGraphPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A refcount graph planar embedding."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def edges_around(self, vertex):
        res = backend.jgrapht_ll_planarity_embedding_edges_around_vertex(
            self._handle, id(vertex)
        )
        return list(_map_ids_to_objs(_JGraphTLongIterator(res)))

    def __repr__(self):
        return "_RefCountGraphPlanarEmbedding(%r)" % self._handle
