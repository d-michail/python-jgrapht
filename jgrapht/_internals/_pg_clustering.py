from .. import backend

from ._clustering import _JGraphTClustering
from ._pg_wrappers import _PropertyGraphVertexIterator


class _PropertyGraphClustering(_JGraphTClustering):
    """A property graph vertex clustering."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def ith_cluster(self, i):
        res = backend.jgrapht_clustering_ith_cluster_vit(self._handle, i)
        return _PropertyGraphVertexIterator(res, self._graph)

    def __repr__(self):
        return "_PropertyGraphClustering(%r)" % self._handle
