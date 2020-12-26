from .. import backend
from ..types import Clustering
from ._wrappers import (
    _HandleWrapper,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
)


class _JGraphTIntegerClustering(_HandleWrapper, Clustering):
    """A vertex clustering."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def number_of_clusters(self):
        return backend.jgrapht_xx_clustering_get_number_clusters(self._handle)

    def ith_cluster(self, i):
        res = backend.jgrapht_xx_clustering_ith_cluster_vit(self._handle, i)
        return _JGraphTIntegerIterator(res)

    def __repr__(self):
        return "_JGraphTIntegerClustering(%r)" % self._handle


class _JGraphTLongClustering(_HandleWrapper, Clustering):
    """A vertex clustering."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def number_of_clusters(self):
        return backend.jgrapht_xx_clustering_get_number_clusters(self._handle)

    def ith_cluster(self, i):
        res = backend.jgrapht_xx_clustering_ith_cluster_vit(self._handle, i)
        return _JGraphTLongIterator(res)

    def __repr__(self):
        return "_JGraphTLongClustering(%r)" % self._handle