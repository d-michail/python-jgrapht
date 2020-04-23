from .. import jgrapht as backend
from ..errors import raise_status
from ..util import JGraphTLongSet


def partition_bipartite(graph):
    """Check whether a graph is bipartite and compute the partitions.
    
    The algorithm runs in linear time in the number of vertices and edges.

    :param graph: The input graph
    :returns: A tuple (result, partition1, partition2)
    """
    err, res, part1, part2 = backend.jgrapht_partition_exec_bipartite(graph.handle)
    if err: 
        raise_status()
    return res, JGraphTLongSet(part1), JGraphTLongSet(part2)


