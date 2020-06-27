from .. import backend as _backend

from .._internals._collections import _JGraphTIntegerSet, _JGraphTIntegerMutableSet

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_collections import (
    _AnyHashableGraphVertexSet,
    _AnyHashableGraphEdgeSet,
    _AnyHashableGraphMutableVertexSet,
)


def _wrap_result(graph, weight, matching_handle):
    if _is_anyhashable_graph(graph):
        return weight, _AnyHashableGraphEdgeSet(matching_handle, graph)
    else:
        return weight, _JGraphTIntegerSet(matching_handle)


def _to_wrapped_vertex_set(graph, vertex_set):
    if _is_anyhashable_graph(graph):
        if isinstance(vertex_set, _AnyHashableGraphVertexSet):
            return vertex_set
        mutable_set = _AnyHashableGraphMutableVertexSet(handle=None, graph=graph)
    else:
        if isinstance(vertex_set, _JGraphTIntegerSet):
            return vertex_set
        mutable_set = _JGraphTIntegerMutableSet()

    for v in vertex_set:
        mutable_set.add(v)
    return mutable_set


def greedy_max_cardinality(graph, sort=False):
    custom = [sort]
    weight, m_handle = _backend.jgrapht_matching_exec_custom_greedy_general_max_card(
        graph.handle, *custom
    )
    return _wrap_result(graph, weight, m_handle)


def edmonds_max_cardinality(graph, dense=False):
    if dense:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_matching_exec_edmonds_general_max_card_dense(graph.handle)
    else:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_matching_exec_edmonds_general_max_card_sparse(graph.handle)
    return _wrap_result(graph, weight, m_handle)


def greedy_max_weight(graph, normalize_edge_costs=False, tolerance=1e-9):
    custom = [normalize_edge_costs, tolerance]
    weight, m_handle = _backend.jgrapht_matching_exec_custom_greedy_general_max_weight(
        graph.handle, *custom
    )
    return _wrap_result(graph, weight, m_handle)


def pathgrowing_max_weight(graph):
    weight, m_handle = _backend.jgrapht_matching_exec_pathgrowing_max_weight(
        graph.handle
    )
    return _wrap_result(graph, weight, m_handle)


def blossom5_max_weight(graph, perfect=False):
    if perfect:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_matching_exec_blossom5_general_perfect_max_weight(
            graph.handle
        )
    else:
        weight, m_handle = _backend.jgrapht_matching_exec_blossom5_general_max_weight(
            graph.handle
        )
    return _wrap_result(graph, weight, m_handle)


def blossom5_min_weight(graph, perfect=False):
    if perfect:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_matching_exec_blossom5_general_perfect_min_weight(
            graph.handle
        )
    else:
        weight, m_handle = _backend.jgrapht_matching_exec_blossom5_general_min_weight(
            graph.handle
        )
    return _wrap_result(graph, weight, m_handle)


def bipartite_max_cardinality(graph):
    weight, m_handle = _backend.jgrapht_matching_exec_bipartite_max_card(graph.handle)
    return _wrap_result(graph, weight, m_handle)


def bipartite_max_weight(graph):
    weight, m_handle = _backend.jgrapht_matching_exec_bipartite_max_weight(graph.handle)
    return _wrap_result(graph, weight, m_handle)


def bipartite_perfect_min_weight(graph, partition_a, partition_b):
    partition_a = _to_wrapped_vertex_set(graph, partition_a)
    partition_b = _to_wrapped_vertex_set(graph, partition_b)

    weight, m_handle = _backend.jgrapht_matching_exec_bipartite_perfect_min_weight(
        graph.handle, partition_a.handle, partition_b.handle
    )

    return _wrap_result(graph, weight, m_handle)
