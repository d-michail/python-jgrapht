from ._int_graphs import _JGraphTIntegerGraph
from ._long_graphs import _JGraphTLongGraph
from ._anyhashableg import _AnyHashableGraph

from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerSetIterator,
    _JGraphTLongSet,
    _JGraphTLongSetIterator,
)
from ._anyhashableg_collections import (
    _AnyHashableGraphVertexSet,
    _AnyHashableGraphVertexSetIterator,
)


def _wrap_vertex_set(graph, handle):
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexSet, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSet, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSet, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_set_iterator(graph, handle):
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexSetIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSetIterator, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSetIterator, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])

