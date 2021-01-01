from ._int_graphs import _JGraphTIntegerGraph, _is_int_graph
from ._long_graphs import _JGraphTLongGraph, _is_long_graph
from ._anyhashableg import _AnyHashableGraph, _is_anyhashable_graph

from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerSetIterator,
    _JGraphTIntegerListIterator,
    _JGraphTIntegerIntegerMap,
    _JGraphTLongSet,
    _JGraphTLongMutableSet,
    _JGraphTLongSetIterator,
    _JGraphTLongListIterator,
    _JGraphTLongIntegerMap,
    _JGraphTIntegerDoubleMap,
    _JGraphTLongDoubleMap,
)
from ._paths import (
    _JGraphTGraphPath,
    _JGraphTGraphPathIterator,
)
from ._clustering import (
    _JGraphTIntegerClustering,
    _JGraphTLongClustering,
)
from ._flows import (
    _JGraphTCut,
    _JGraphTIntegerGomoryHuTree,
    _JGraphTLongGomoryHuTree,
    _JGraphTIntegerEquivalentFlowTree,
    _JGraphTLongEquivalentFlowTree,
    _JGraphTIntegerFlow,
    _JGraphTLongFlow,
)
from ._anyhashableg_collections import (
    _AnyHashableGraphVertexSet,
    _AnyHashableGraphMutableVertexSet,
    _AnyHashableGraphVertexSetIterator,
    _AnyHashableGraphVertexListIterator,
    _AnyHashableGraphVertexIntegerMap,
    _AnyHashableGraphVertexDoubleMap,        
    _AnyHashableGraphEdgeSet,
)
from ._anyhashableg_paths import (
    _AnyHashableGraphGraphPath,
    _AnyHashableGraphGraphPathIterator,
)
from ._anyhashableg_clustering import (
    _AnyHashableGraphClustering,
)
from ._anyhashableg_flows import (
    _AnyHashableGraphCut,
    _AnyHashableGraphFlow,
    _AnyHashableGraphGomoryHuTree,
    _AnyHashableGraphEquivalentFlowTree,
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


def _wrap_vertex_list_iterator(graph, handle):
    """Given an vertex list iterator in the JVM, build one in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexListIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongListIterator, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerListIterator, [handle]),
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


def _wrap_graphpath(graph, handle):
    """Given a graph path in the JVM, build one in Python. The wrapper
       graph takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphGraphPath, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTGraphPath, [handle, graph]),
        _JGraphTIntegerGraph: (_JGraphTGraphPath, [handle, graph]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_graphpath_iterator(graph, handle):
    """Given a graph path iterator in the JVM, build one in Python. The wrapper
           graph takes ownership and will delete the JVM resource when Python deletes
           the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphGraphPathIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTGraphPathIterator, [handle, graph]),
        _JGraphTIntegerGraph: (_JGraphTGraphPathIterator, [handle, graph]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_clustering(graph, handle):
    """Given a vertex clustering in the JVM, build one in Python. The wrapper
       takes ownership and will delete the JVM resource when Python deletes
       the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphClustering, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongClustering, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerClustering, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_cut(graph, handle, weight):
    """Given a cut in the JVM, build one in Python. The wrapper takes ownership
       and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphCut, [graph, weight, handle]),
        _JGraphTLongGraph: (_JGraphTCut, [graph, weight, handle]),
        _JGraphTIntegerGraph: (_JGraphTCut, [graph, weight, handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_gomory_hu_tree(graph, handle):
    """Given a gomory hu tree in the JVM, build one in Python. The wrapper takes
       ownership and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphGomoryHuTree, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongGomoryHuTree, [handle, graph]),
        _JGraphTIntegerGraph: (_JGraphTIntegerGomoryHuTree, [handle, graph]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_equivalent_flow_tree(graph, handle):
    """Given an equivalent flow tree in the JVM, build one in Python. The wrapper takes
       ownership and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphEquivalentFlowTree, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongEquivalentFlowTree, [handle, graph]),
        _JGraphTIntegerGraph: (_JGraphTIntegerEquivalentFlowTree, [handle, graph]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_flow(graph, handle, source, sink, value):
    """Given a flow in the JVM, build one in Python. The wrapper takes ownership
    and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphFlow, [graph, handle, source, sink, value]),
        _JGraphTLongGraph: (_JGraphTLongFlow, [handle, source, sink, value]),
        _JGraphTIntegerGraph: (_JGraphTIntegerFlow, [handle, source, sink, value]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_integer_map(graph, handle):
    """Given a vertex integer map in the JVM, build one in Python. The wrapper takes ownership
    and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexIntegerMap, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongIntegerMap, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerIntegerMap, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_vertex_double_map(graph, handle):
    """Given a vertex double map in the JVM, build one in Python. The wrapper takes ownership
    and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexDoubleMap, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongDoubleMap, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerDoubleMap, [handle]),
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