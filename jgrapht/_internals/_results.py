from ._int_graphs import _JGraphTIntegerGraph, _is_int_graph
from ._long_graphs import _JGraphTLongGraph, _is_long_graph
from ._anyhashableg import _AnyHashableGraph, _is_anyhashable_graph

from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerSetIterator,
    _JGraphTIntegerIntegerMap,
    _JGraphTLongSet,
    _JGraphTLongMutableSet,
    _JGraphTLongSetIterator,
    _JGraphTLongIntegerMap,
)
from ._anyhashableg_collections import (
    _AnyHashableGraphVertexSet,
    _AnyHashableGraphMutableVertexSet,
    _AnyHashableGraphVertexSetIterator,
    _AnyHashableGraphVertexIntegerMap,
    _AnyHashableGraphEdgeSet,
)


def _wrap_vertex_set(graph, handle):
    """Given a vertex set in the JVM, build a vertex set in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexSet, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSet, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSet, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_edge_set(graph, handle):
    """Given an edge set in the JVM, build an edge set in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphEdgeSet, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSet, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSet, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_set_iterator(graph, handle):
    """Given an vertex set iterator in the JVM, build one in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexSetIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSetIterator, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSetIterator, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_coloring(graph, handle):
    """Given a vertex coloring in the JVM, build one in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexIntegerMap, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongIntegerMap, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerIntegerMap, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _build_vertex_set(graph, vertex_set):
    """Given a vertex set in Python, build a vertex set inside the JVM."""
    if _is_anyhashable_graph(graph):
        if isinstance(vertex_set, _AnyHashableGraphVertexSet):
            return vertex_set
        mutable_set = _AnyHashableGraphMutableVertexSet(handle=None, graph=graph)
    elif _is_long_graph(graph):
        if isinstance(vertex_set, _JGraphTLongSet):
            return vertex_set
        mutable_set = _JGraphTLongMutableSet()
    else:
        if isinstance(vertex_set, _JGraphTIntegerSet):
            return vertex_set
        mutable_set = _JGraphTIntegerMutableSet()

    for v in vertex_set:
        mutable_set.add(v)

    return mutable_set