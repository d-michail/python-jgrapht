from .. import backend
from .._errors import raise_status, UnsupportedOperationError
from ..util import JGraphTLongSet

def _matching_alg(name, graph, *args, no_custom_prefix=False):

    alg_method_name = 'jgrapht_matching_exec_'
    if args and not no_custom_prefix:
        alg_method_name += 'custom_'
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")    

    err, weight, m_handle = alg_method(graph.handle, *args)
    if err: 
        raise_status()

    return weight, JGraphTLongSet(handle=m_handle)


def general_matching_greedy_max_cardinality(graph, sort=False):
    custom = [ sort ]
    return _matching_alg('greedy_general_max_card', graph, *custom)


def general_matching_edmonds_max_cardinality(graph, dense=False):
    if dense: 
        return _matching_alg('edmonds_general_max_card_dense', graph)
    else:
        return _matching_alg('edmonds_general_max_card_sparse', graph)


def general_matching_greedy_max_weight(graph, normalize_edge_costs=False, tolerance=1e-9):
    custom = [ normalize_edge_costs, tolerance ]
    return _matching_alg('greedy_general_max_weight', graph, *custom)


def general_matching_pathgrowing_max_weight(graph):
    return _matching_alg('pathgrowing_max_weight', graph)
    

def general_matching_blossom5_max_weight(graph, perfect=True):
    if perfect:
        return _matching_alg('blossom5_general_perfect_max_weight', graph)
    else:
        return _matching_alg('blossom5_general_max_weight', graph)


def general_matching_blossom5_min_weight(graph, perfect=True):
    if perfect:
        return _matching_alg('blossom5_general_perfect_min_weight', graph)
    else:
        return _matching_alg('blossom5_general_min_weight', graph)


def bipartite_matching_max_cardinality(graph):
    return _matching_alg('bipartite_max_card', graph)


def bipartite_matching_max_weight(graph):
    return _matching_alg('bipartite_max_weight', graph)


def bipartite_matching_perfect_min_weight(graph, partition_a, partition_b):
    custom = [ partition_a.handle, partition_b.handle ]
    return _matching_alg('bipartite_perfect_min_weight', graph, *custom, no_custom_prefix=True)

