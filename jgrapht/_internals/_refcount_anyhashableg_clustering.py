
from .. import backend
from ..types import Clustering
from ._refcount import _map_ids_to_objs
from ._clustering import _JGraphTLongClustering


class _RefCountAnyHashableGraphClustering(Clustering):
    """A refcount any-hashable graph vertex clustering.
    
    Note: Initialized using a handle to a long clustering and takes ownership.
    """

    def __init__(self, handle, **kwargs):
        self._clusters = list()
        clustering = _JGraphTLongClustering(handle=handle)
        for i in range(clustering.number_of_clusters()): 
            cluster = set(_map_ids_to_objs(clustering.ith_cluster(i)))
            self._clusters.append(cluster)

    def number_of_clusters(self):
        return len(self._clusters)

    def ith_cluster(self, i):
        return self._clusters[i]

    def __repr__(self):
        return "_RefCountAnyHashableGraphClustering(%r)" % self._handle
