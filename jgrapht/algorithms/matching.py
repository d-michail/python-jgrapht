from .. import backend as _backend
from .._internals._results import _wrap_edge_set, _build_vertex_set


def greedy_max_cardinality(graph, sort=False):
    custom = [sort]
    weight, m_handle = _backend.jgrapht_xx_matching_exec_custom_greedy_general_max_card(
        graph.handle, *custom
    )
    return weight, _wrap_edge_set(graph, m_handle)


def edmonds_max_cardinality(graph, dense=False):
    if dense:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_edmonds_general_max_card_dense(graph.handle)
    else:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_edmonds_general_max_card_sparse(graph.handle)
    return weight, _wrap_edge_set(graph, m_handle)


def greedy_max_weight(graph, normalize_edge_costs=False, tolerance=1e-9):
    custom = [normalize_edge_costs, tolerance]
    weight, m_handle = _backend.jgrapht_xx_matching_exec_custom_greedy_general_max_weight(
        graph.handle, *custom
    )
    return weight, _wrap_edge_set(graph, m_handle)


def pathgrowing_max_weight(graph):
    weight, m_handle = _backend.jgrapht_xx_matching_exec_pathgrowing_max_weight(
        graph.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)


def blossom5_max_weight(graph, perfect=False):
    if perfect:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_blossom5_general_perfect_max_weight(
            graph.handle
        )
    else:
        weight, m_handle = _backend.jgrapht_xx_matching_exec_blossom5_general_max_weight(
            graph.handle
        )
    return weight, _wrap_edge_set(graph, m_handle)


def blossom5_min_weight(graph, perfect=False):
    if perfect:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_blossom5_general_perfect_min_weight(
            graph.handle
        )
    else:
        weight, m_handle = _backend.jgrapht_xx_matching_exec_blossom5_general_min_weight(
            graph.handle
        )
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_max_cardinality(graph):
    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_max_card(graph.handle)
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_max_weight(graph):
    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_max_weight(graph.handle)
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_perfect_min_weight(graph, partition_a, partition_b):
    partition_a = _build_vertex_set(graph, partition_a)
    partition_b = _build_vertex_set(graph, partition_b)

    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_perfect_min_weight(
        graph.handle, partition_a.handle, partition_b.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)
