from .. import backend as _backend
from .._internals._results import _wrap_edge_set, _build_vertex_set


def greedy_max_cardinality(graph, sort=False):
    """The greedy algorithm for maximum cardinality matching in arbitrary graphs. 

    The algorithm can run in two modes: sorted or unsorted. When unsorted, the matching
    is obtained by iterating through the edges and adding an edge if it doesn't conflict
    with the edges already in the matching. When sorted, the edges are first sorted by
    the sum of degrees of their endpoints. After that, the algorithm proceeds in the same
    manner. Running this algorithm in sorted mode can sometimes produce better results,
    albeit at the cost of some additional computational overhead.

    Independent of the mode, the resulting matching is maximal, and is therefore guaranteed
    to contain at least half of the edges that a maximum cardinality matching has
    (1/2 approximation). The algorithm runs in :math:`\mathcal{O}(m)` time when the edges 
    are not sorted and in :math:`\mathcal{O}(m + m \log n)` time when sorted where
    :math:`n` is the number of vertices and :math:`m` the number of edges of the graph.

    :param graph: the graph
    :param sort: whether to sort edges by sum of vertex degrees
    :returns: an edge set corresponding to the matching
    """
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
        ) = _backend.jgrapht_xx_matching_exec_edmonds_general_max_card_dense(
            graph.handle
        )
    else:
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_edmonds_general_max_card_sparse(
            graph.handle
        )
    return weight, _wrap_edge_set(graph, m_handle)


def greedy_max_weight(graph, normalize_edge_costs=False, tolerance=1e-9):
    custom = [normalize_edge_costs, tolerance]
    (
        weight,
        m_handle,
    ) = _backend.jgrapht_xx_matching_exec_custom_greedy_general_max_weight(
        graph.handle, *custom
    )
    return weight, _wrap_edge_set(graph, m_handle)


def pathgrowing_max_weight(graph):
    """The pathgrowing approximation matching algorithm. 
    
    A linear time 1/2 approximation algorithm for finding a maximum weight matching in an
    arbitrary graph. Linear time here means :math:`\mathcal{O}(m)` where :math:`m` is the
    cardinality of the edge set, even if the graph contains isolated vertices. 1/2-approximation
    means that for any graph instance, the algorithm computes a matching whose weight is at least
    half of the weight of a maximum weight matching. The implementation accepts directed and
    undirected graphs which may contain self-loops and multiple edges. There is no assumption on
    the edge weights, i.e. they can also be negative or zero.

    The algorithm is due to Drake and Hougardy, described in detail in the following paper:
    D.E. Drake, S. Hougardy, A Simple Approximation Algorithm for the Weighted Matching Problem, 
    Information Processing Letters 85, 211-213, 2003.

    This particular implementation uses by two additional heuristics discussed by the authors
    which also take linear time but improve the quality of the matchings. For a discussion on
    engineering approximate weighted matching algorithms see the following paper: Jens Maue and
    Peter Sanders. Engineering algorithms for approximate weighted matching. International Workshop
    on Experimental and Efficient Algorithms, Springer, 2007.

    :param graph: the graph
    :returns: an edge set corresponding to the matching
    """
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
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_blossom5_general_max_weight(graph.handle)
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
        (
            weight,
            m_handle,
        ) = _backend.jgrapht_xx_matching_exec_blossom5_general_min_weight(graph.handle)
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_max_cardinality(graph):
    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_max_card(
        graph.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_max_weight(graph):
    """Maximum weight matching in bipartite graphs.

    Running time is :math:`\mathcal{O}(n(m+n \log n))` where :math:`n` is the number of
    vertices and :math:`m` the number of edges of the input graph. Uses exact arithmetic
    and produces a certificate of optimality in the form of a tight vertex potential
    function.

    This is the algorithm and implementation described in the LEDA book. See the LEDA
    Platform of Combinatorial and Geometric Computing, Cambridge University Press, 1999.

    :param graph: the graph (must be bipartite)
    :returns: an edge set corresponding to the matching
    """
    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_max_weight(
        graph.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)


def bipartite_perfect_min_weight(graph, partition_a, partition_b):
    partition_a = _build_vertex_set(graph, partition_a)
    partition_b = _build_vertex_set(graph, partition_b)

    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_perfect_min_weight(
        graph.handle, partition_a.handle, partition_b.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)
