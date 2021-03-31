from .. import backend

from ._int_graphs import _JGraphTIntegerGraph, _is_int_graph
from ._long_graphs import _JGraphTLongGraph, _is_long_graph
from ._ref_graphs import _JGraphTRefGraph, _is_ref_graph

from . import _ref_hashequals, _ref_results

from ._anyhashableg import (
    _AnyHashableGraph,
    _is_anyhashable_graph,
    _vertex_anyhashableg_to_g,
    _vertex_g_to_anyhashableg,
    _create_anyhashable_graph_subgraph,
)

from ._wrappers import (
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
    GraphBackend,
)
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
    _JGraphTRefSet,
    _JGraphTRefMutableSet,
    _JGraphTLongIntegerMap,
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerDoubleMutableMap,
    _JGraphTLongDoubleMap,
    _JGraphTLongDoubleMutableMap,
)
from ._paths import (
    _JGraphTGraphPath,
    _JGraphTGraphPathIterator,
    _JGraphTSingleSourcePaths,
    _JGraphTAllPairsPaths,
    _JGraphTMultiObjectiveSingleSourcePaths,
    _JGraphTContractionHierarchies,
    _JGraphTContractionHierarchiesManyToMany,
)
from ._clustering import (
    _JGraphTIntegerClustering,
    _JGraphTLongClustering,
    _JGraphTRefClustering,
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
from ._planar import (
    _JGraphTIntegerPlanarEmbedding,
    _JGraphTLongPlanarEmbedding,
)
from ._anyhashableg_wrappers import (
    _AnyHashableGraphVertexIterator,
    _AnyHashableGraphEdgeIterator,
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
    _AnyHashableGraphSingleSourcePaths,
    _AnyHashableGraphAllPairsPaths,
    _AnyHashableGraphMultiObjectiveSingleSourcePaths,
    _AnyHashableGraphContractionHierarchiesManyToMany,
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
from ._anyhashableg_planar import _AnyHashableGraphPlanarEmbedding


def _unwrap_vertex(graph, vertex):
    """Given a vertex in Python, return the corresponding vertex in the JVM
    (if different)."""
    if vertex is None:
        return None
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            lambda graph, v: _vertex_anyhashableg_to_g(graph, v),
            [graph, vertex],
        ),
        GraphBackend.LONG_GRAPH: (lambda v: v, [vertex]),
        GraphBackend.INT_GRAPH: (lambda v: v, [vertex]),
        GraphBackend.REF_GRAPH: (lambda v: id(v), [vertex]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _unwrap_astar_heuristic_cb(graph, heuristic_cb):
    """Given a heuristic callback method for astar in Python, create one for the JVM."""
    if _is_anyhashable_graph(graph):
        # redefine in order to translate from integer to user vertices
        def actual_heuristic_cb(s, t):
            return heuristic_cb(
                _vertex_g_to_anyhashableg(graph, s), _vertex_g_to_anyhashableg(graph, t)
            )

    else:
        actual_heuristic_cb = heuristic_cb

    return actual_heuristic_cb


def _wrap_vertex_set(graph, handle):
    """Given a vertex set in the JVM, build a vertex set in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexSet, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongSet, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerSet, [handle]),
        _JGraphTRefGraph: (_ref_results._jgrapht_ref_set_to_python_set, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_edge_set(graph, handle):
    """Given an edge set in the JVM, build an edge set in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (_AnyHashableGraphEdgeSet, [handle, graph]),
        GraphBackend.LONG_GRAPH: (_JGraphTLongSet, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerSet, [handle]),
        GraphBackend.REF_GRAPH: (_ref_results._jgrapht_ref_set_to_python_set, [handle]),
    }
    alg = cases[graph._backend_type]
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


def _wrap_vertex_iterator(graph, handle):
    """Given an vertex iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphVertexIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongIterator, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerIterator, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_edge_iterator(graph, handle):
    """Given an edge iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphEdgeIterator, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongIterator, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerIterator, [handle]),
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
        _JGraphTRefGraph: (_JGraphTGraphPath, [handle, graph]),
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


def _wrap_single_source_paths(graph, handle, source_vertex):
    """Given a single source paths result in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (
            _AnyHashableGraphSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        _JGraphTLongGraph: (_JGraphTSingleSourcePaths, [handle, graph, source_vertex]),
        _JGraphTIntegerGraph: (
            _JGraphTSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_allpairs_paths(graph, handle):
    """Given an all pairs paths result in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphAllPairsPaths, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTAllPairsPaths, [handle, graph]),
        _JGraphTIntegerGraph: (_JGraphTAllPairsPaths, [handle, graph]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_multi_objective_single_source_paths(graph, handle, source_vertex):
    """Given a multi objective single source paths result in the JVM, build one in Python.
    The wrapper graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (
            _AnyHashableGraphMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        _JGraphTLongGraph: (
            _JGraphTMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        _JGraphTIntegerGraph: (
            _JGraphTMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_contraction_hierarchies(graph, handle):
    """Given contraction hierarchies in the JVM, build one in Python. The wrapper
    takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (
            _JGraphTContractionHierarchies,
            [handle, graph],
        ),
        _JGraphTLongGraph: (
            _JGraphTContractionHierarchies,
            [handle, graph],
        ),
        _JGraphTIntegerGraph: (
            _JGraphTContractionHierarchies,
            [handle, graph],
        ),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_manytomany_contraction_hierarchies(graph, handle):
    """Given many-to-many contraction hierarchies in the JVM, build one in Python.
    The wrapper takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        _AnyHashableGraph: (
            _AnyHashableGraphContractionHierarchiesManyToMany,
            [handle, graph],
        ),
        _JGraphTLongGraph: (
            _JGraphTContractionHierarchiesManyToMany,
            [handle, graph],
        ),
        _JGraphTIntegerGraph: (
            _JGraphTContractionHierarchiesManyToMany,
            [handle, graph],
        ),
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
        _JGraphTRefGraph: (_JGraphTRefClustering, [handle]),
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
        _JGraphTRefGraph: (_JGraphTCut, [graph, weight, handle]),
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
        _AnyHashableGraph: (
            _AnyHashableGraphFlow,
            [graph, handle, source, sink, value],
        ),
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


def _wrap_planar_embedding(graph, handle):
    """Given a planar embedding in the JVM, build one in Python. The wrapper takes
    ownership and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        _AnyHashableGraph: (_AnyHashableGraphPlanarEmbedding, [handle, graph]),
        _JGraphTLongGraph: (_JGraphTLongPlanarEmbedding, [handle]),
        _JGraphTIntegerGraph: (_JGraphTIntegerPlanarEmbedding, [handle]),
    }
    alg = cases[type(graph)]
    return alg[0](*alg[1])


def _wrap_subgraph(graph, handle):
    """Given a subgraph in the JVM, build one in Python. The wrapper takes
    ownership and will delete the JVM resource when Python deletes the instance.
    """
    if _is_anyhashable_graph(graph):
        sub = _JGraphTIntegerGraph(handle=handle)
        return _create_anyhashable_graph_subgraph(graph, sub)
    else:
        cases = {
            _JGraphTLongGraph: (_JGraphTLongGraph, [handle]),
            _JGraphTIntegerGraph: (_JGraphTIntegerGraph, [handle]),
        }
        alg = cases[type(graph)]
        return alg[0](*alg[1])


def _build_vertex_set(graph, vertex_set):
    """Given a vertex set in Python, build a vertex set inside the JVM."""

    if graph._backend_type == GraphBackend.ANY_HASHABLE_GRAPH:
        if isinstance(vertex_set, _AnyHashableGraphVertexSet):
            return vertex_set
        mutable_set = _AnyHashableGraphMutableVertexSet(
            handle=backend.jgrapht_set_linked_create(), graph=graph
        )
    elif graph._backend_type == GraphBackend.LONG_GRAPH:
        if isinstance(vertex_set, _JGraphTLongSet):
            return vertex_set
        mutable_set = _JGraphTLongMutableSet(handle=backend.jgrapht_set_linked_create())
    elif graph._backend_type == GraphBackend.INT_GRAPH:
        if isinstance(vertex_set, _JGraphTIntegerSet):
            return vertex_set
        mutable_set = _JGraphTIntegerMutableSet(
            handle=backend.jgrapht_set_linked_create()
        )
    elif graph._backend_type == GraphBackend.REF_GRAPH:
        mutable_set = _JGraphTRefMutableSet(
            handle=backend.jgrapht_set_linked_create(),
            hash_equals_resolver_handle=_ref_hashequals._get_equals_hash_wrapper().handle,
        )
    else:
        raise ValueError("Not supported graph backend")

    for v in vertex_set:
        mutable_set.add(v)

    return mutable_set


def _build_vertex_weights(graph, vertex_weights):
    """Given a vertex weights dictionary in Python, build one inside the JVM."""
    if _is_anyhashable_graph(graph):
        jgrapht_vertex_weights = _JGraphTIntegerDoubleMutableMap()
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[graph._vertex_hash_to_id[key]] = val
    elif _is_long_graph(graph):
        jgrapht_vertex_weights = _JGraphTLongDoubleMutableMap()
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[key] = val
    else:
        jgrapht_vertex_weights = _JGraphTIntegerDoubleMutableMap()
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[key] = val
    return jgrapht_vertex_weights
