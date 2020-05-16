from .. import backend
from ..types import Clustering
from ._wrappers import (
    _HandleWrapper,
    _JGraphTIntegerIterator,
)


class _JGraphTClustering(_HandleWrapper, Clustering):
    """A vertex clustering."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def number_of_clusters(self):
        return backend.jgrapht_clustering_get_number_clusters(self._handle)

    def ith_cluster(self, i):
        res = backend.jgrapht_clustering_ith_cluster_vit(self._handle, i)
        return _JGraphTIntegerIterator(res)

    def __repr__(self):
        return "_JGraphTClustering(%r)" % self._handle
