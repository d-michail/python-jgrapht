from .. import backend

from ._int_graphs import _JGraphTIntegerGraph, _is_int_graph
from ._long_graphs import _JGraphTLongGraph, _is_long_graph
from ._ref_graphs import _JGraphTRefGraph, _is_ref_graph

import ctypes
from . import _callbacks
from . import _ref_hashequals, _ref_utils, _ref_results

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
    _JGraphTRefIterator,
    GraphBackend,
)
from ._collections_set import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerSetIterator,
    _JGraphTLongSet,
    _JGraphTLongMutableSet,
    _JGraphTLongSetIterator,
    _JGraphTRefSet,
    _JGraphTRefMutableSet,
    _JGraphTRefSetIterator,
)
from ._collections import (
    _JGraphTIntegerListIterator,
    _JGraphTLongListIterator,
    _JGraphTRefListIterator,
    _JGraphTIntegerIntegerMap,
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
    _JGraphTRefGomoryHuTree,
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
    """Given a heuristic callback method for astar in Python, create one for the JVM.
    We return a callback wrapper which contains the new callback together with a function pointer
    that can be passed directly to the JVM.
    """

    if graph._backend_type == GraphBackend.ANY_HASHABLE_GRAPH:
        # redefine in order to translate from integer to user vertices
        def actual_heuristic_cb(s, t):
            return heuristic_cb(
                _vertex_g_to_anyhashableg(graph, s), _vertex_g_to_anyhashableg(graph, t)
            )
        actual_heuristic_callback_type = ctypes.CFUNCTYPE(
            ctypes.c_double, ctypes.c_longlong, ctypes.c_longlong
        )

    elif graph._backend_type == GraphBackend.REF_GRAPH:
        actual_heuristic_cb = heuristic_cb
        actual_heuristic_callback_type = ctypes.CFUNCTYPE(
            ctypes.c_double, ctypes.py_object, ctypes.py_object
        )

    else:
        actual_heuristic_cb = heuristic_cb
        actual_heuristic_callback_type = ctypes.CFUNCTYPE(
            ctypes.c_double, ctypes.c_longlong, ctypes.c_longlong
        )

    callback_wrapper = _callbacks._CallbackWrapper(
        actual_heuristic_cb, actual_heuristic_callback_type
    )

    return callback_wrapper


def _wrap_vertex_set(graph, handle):
    """Given a vertex set in the JVM, build a vertex set in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (_AnyHashableGraphVertexSet, [handle, graph]),
        GraphBackend.LONG_GRAPH: (_JGraphTLongSet, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerSet, [handle]),
        GraphBackend.REF_GRAPH: (_ref_results._jgrapht_ref_set_to_python_set, [handle]),
    }
    alg = cases[graph._backend_type]
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
    hash_equals_resolver_handle = _ref_hashequals._get_hash_equals_wrapper().handle
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphVertexSetIterator,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTLongSetIterator, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerSetIterator, [handle]),
        GraphBackend.REF_GRAPH: (
            _JGraphTRefSetIterator,
            [handle, hash_equals_resolver_handle],
        ),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_vertex_iterator(graph, handle):
    """Given an vertex iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphVertexIterator,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTLongIterator, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerIterator, [handle]),
        GraphBackend.REF_GRAPH: (_JGraphTRefIterator, [handle]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_edge_iterator(graph, handle):
    """Given an edge iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphEdgeIterator,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTLongIterator, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerIterator, [handle]),
        GraphBackend.REF_GRAPH: (_JGraphTRefIterator, [handle]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_vertex_list_iterator(graph, handle):
    """Given an vertex list iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphVertexListIterator,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTLongListIterator, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerListIterator, [handle]),
        GraphBackend.REF_GRAPH: (_JGraphTRefListIterator, [handle]),
    }
    alg = cases[graph._backend_type]
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
        GraphBackend.ANY_HASHABLE_GRAPH: (_AnyHashableGraphGraphPath, [handle, graph]),
        GraphBackend.LONG_GRAPH: (_JGraphTGraphPath, [handle, graph]),
        GraphBackend.INT_GRAPH: (_JGraphTGraphPath, [handle, graph]),
        GraphBackend.REF_GRAPH: (_JGraphTGraphPath, [handle, graph]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_graphpath_iterator(graph, handle):
    """Given a graph path iterator in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphGraphPathIterator,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTGraphPathIterator, [handle, graph]),
        GraphBackend.INT_GRAPH: (_JGraphTGraphPathIterator, [handle, graph]),
        GraphBackend.REF_GRAPH: (_JGraphTGraphPathIterator, [handle, graph]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_single_source_paths(graph, handle, source_vertex):
    """Given a single source paths result in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.LONG_GRAPH: (
            _JGraphTSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.INT_GRAPH: (
            _JGraphTSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.REF_GRAPH: (
            _JGraphTSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_allpairs_paths(graph, handle):
    """Given an all pairs paths result in the JVM, build one in Python. The wrapper
    graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphAllPairsPaths,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTAllPairsPaths, [handle, graph]),
        GraphBackend.INT_GRAPH: (_JGraphTAllPairsPaths, [handle, graph]),
        GraphBackend.REF_GRAPH: (_JGraphTAllPairsPaths, [handle, graph]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_multi_objective_single_source_paths(graph, handle, source_vertex):
    """Given a multi objective single source paths result in the JVM, build one in Python.
    The wrapper graph takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.LONG_GRAPH: (
            _JGraphTMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.INT_GRAPH: (
            _JGraphTMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
        GraphBackend.REF_GRAPH: (
            _JGraphTMultiObjectiveSingleSourcePaths,
            [handle, graph, source_vertex],
        ),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_contraction_hierarchies(graph, handle):
    """Given contraction hierarchies in the JVM, build one in Python. The wrapper
    takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    return _JGraphTContractionHierarchies(handle, graph)


def _wrap_manytomany_contraction_hierarchies(graph, handle):
    """Given many-to-many contraction hierarchies in the JVM, build one in Python.
    The wrapper takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphContractionHierarchiesManyToMany,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (
            _JGraphTContractionHierarchiesManyToMany,
            [handle, graph],
        ),
        GraphBackend.INT_GRAPH: (
            _JGraphTContractionHierarchiesManyToMany,
            [handle, graph],
        ),
        GraphBackend.REF_GRAPH: (
            _JGraphTContractionHierarchiesManyToMany,
            [handle, graph],
        ),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_vertex_clustering(graph, handle):
    """Given a vertex clustering in the JVM, build one in Python. The wrapper
    takes ownership and will delete the JVM resource when Python deletes
    the instance."""
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (_AnyHashableGraphClustering, [handle, graph]),
        GraphBackend.LONG_GRAPH: (_JGraphTLongClustering, [handle]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerClustering, [handle]),
        GraphBackend.REF_GRAPH: (_JGraphTRefClustering, [handle]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_cut(graph, handle, weight):
    """Given a cut in the JVM, build one in Python. The wrapper takes ownership
    and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphCut,
            [graph, weight, handle],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTCut, [graph, weight, handle]),
        GraphBackend.INT_GRAPH: (_JGraphTCut, [graph, weight, handle]),
        GraphBackend.REF_GRAPH: (_JGraphTCut, [graph, weight, handle]),
    }
    alg = cases[graph._backend_type]
    return alg[0](*alg[1])


def _wrap_gomory_hu_tree(graph, handle):
    """Given a gomory hu tree in the JVM, build one in Python. The wrapper takes
    ownership and will delete the JVM resource when Python deletes the instance.
    """
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: (
            _AnyHashableGraphGomoryHuTree,
            [handle, graph],
        ),
        GraphBackend.LONG_GRAPH: (_JGraphTLongGomoryHuTree, [handle, graph]),
        GraphBackend.INT_GRAPH: (_JGraphTIntegerGomoryHuTree, [handle, graph]),
        GraphBackend.REF_GRAPH: (_JGraphTRefGomoryHuTree, [handle, graph]),
    }
    alg = cases[graph._backend_type]
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
            handle=backend.jgrapht_x_set_linked_create(), graph=graph
        )
    elif graph._backend_type == GraphBackend.LONG_GRAPH:
        if isinstance(vertex_set, _JGraphTLongSet):
            return vertex_set
        mutable_set = _JGraphTLongMutableSet(
            handle=backend.jgrapht_x_set_linked_create()
        )
    elif graph._backend_type == GraphBackend.INT_GRAPH:
        if isinstance(vertex_set, _JGraphTIntegerSet):
            return vertex_set
        mutable_set = _JGraphTIntegerMutableSet(
            handle=backend.jgrapht_x_set_linked_create()
        )
    elif graph._backend_type == GraphBackend.REF_GRAPH:
        mutable_set = _JGraphTRefMutableSet(
            handle=backend.jgrapht_x_set_linked_create(),
            hash_equals_resolver_handle=_ref_hashequals._get_hash_equals_wrapper().handle,
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
