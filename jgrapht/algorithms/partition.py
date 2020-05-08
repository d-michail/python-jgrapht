from .. import backend
from .._internals._errors import _raise_status
from .._internals._wrappers import _JGraphTLongSet


def bipartite_partitions(graph):
    """Check whether a graph is bipartite and compute the partitions.
    
    The algorithm runs in linear time in the number of vertices and edges.

    :param graph: The input graph
    :returns: A tuple (result, partition1, partition2)
    """
    err, res, part1, part2 = backend.jgrapht_partition_exec_bipartite(graph.handle)
    if err:
        _raise_status()
    return res, _JGraphTLongSet(part1), _JGraphTLongSet(part2)
