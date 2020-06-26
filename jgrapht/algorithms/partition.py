from .. import backend as _backend

from .._internals._collections import _JGraphTIntegerSet

from .._internals._attrsg import is_attrs_graph
from .._internals._attrsg_collections import _AttributesGraphVertexSet


def bipartite_partitions(graph):
    """Check whether a graph is bipartite and compute the partitions.
    
    The algorithm runs in linear time in the number of vertices and edges.

    :param graph: The input graph
    :returns: A tuple (result, partition1, partition2)
    """
    res, part1, part2 = _backend.jgrapht_partition_exec_bipartite(graph.handle)

    if is_attrs_graph(graph):
        return res, _AttributesGraphVertexSet(part1, graph), _AttributesGraphVertexSet(part2, graph)
    else:
        return res, _JGraphTIntegerSet(part1), _JGraphTIntegerSet(part2)
