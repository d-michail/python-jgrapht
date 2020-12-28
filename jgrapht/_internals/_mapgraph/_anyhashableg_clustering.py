from jgrapht import backend

from jgrapht._internals._intgraph._clustering import _JGraphTIntegerClustering
from ._anyhashableg_wrappers import _AnyHashableGraphVertexIterator


class _AnyHashableGraphClustering(_JGraphTIntegerClustering):
    """An any-hashable graph vertex clustering."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def ith_cluster(self, i):
        res = backend.jgrapht_xx_clustering_ith_cluster_vit(self._handle, i)
        return _AnyHashableGraphVertexIterator(res, self._graph)

    def __repr__(self):
        return "_AnyHashableGraphClustering(%r)" % self._handle
