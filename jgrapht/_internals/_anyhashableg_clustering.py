from .. import backend

from ._clustering import _JGraphTClustering
from ._anyhashableg_wrappers import _AnyHashableGraphVertexIterator


class _AnyHashableGraphClustering(_JGraphTClustering):
    """An any-hashable graph vertex clustering."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def ith_cluster(self, i):
        res = backend.jgrapht_clustering_ith_cluster_vit(self._handle, i)
        return _AnyHashableGraphVertexIterator(res, self._graph)

    def __repr__(self):
        return "_AnyHashableGraphClustering(%r)" % self._handle
