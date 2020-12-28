from .. import backend as _backend

from .._internals._collections import _JGraphTIntegerSet, _JGraphTLongSet
from jgrapht._internals._intgraph._long_graphs import _is_long_graph
from jgrapht._internals._mapgraph._graphs import _is_anyhashable_graph
from jgrapht._internals._mapgraph._collections import _AnyHashableGraphVertexSet


def bipartite_partitions(graph):
    """Check whether a graph is bipartite and compute the partitions.
    
    The algorithm runs in linear time in the number of vertices and edges.

    :param graph: The input graph
    :returns: A tuple (result, partition1, partition2)
    """
    res, part1, part2 = _backend.jgrapht_xx_partition_exec_bipartite(graph.handle)

    if _is_anyhashable_graph(graph):
        return (
            res,
            _AnyHashableGraphVertexSet(part1, graph),
            _AnyHashableGraphVertexSet(part2, graph),
        )
    elif _is_long_graph(graph):
        return res, _JGraphTLongSet(part1), _JGraphTLongSet(part2)
    else:
        return res, _JGraphTIntegerSet(part1), _JGraphTIntegerSet(part2)
