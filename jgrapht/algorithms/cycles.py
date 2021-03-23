from .. import backend as _backend
from .._internals._results import (
    _wrap_graphpath,
    _wrap_graphpath_iterator,
    _wrap_vertex_list_iterator,
)


def eulerian_cycle(graph):
    r"""Run Hierholzer's algorithm to check if a graph is Eulerian and if yes
    construst an Eulerian cycle.

    The algorithm works with directed and undirected graphs which may contain loops and/or
    multiple edges. The running time is linear, i.e. :math:`\mathcal{O}(m)` where :math:`m`
    is the cardinality of the edge set of the graph.

    See the `wikipedia article <https://en.wikipedia.org/wiki/Eulerian_path>`_ for details
    and references about Eulerian cycles and a short description of Hierholzer's algorithm
    for the construction of an Eulerian cycle. The original presentation of the algorithm
    dates back to 1873 and the following paper:

      * Carl Hierholzer: Über die Möglichkeit, einen Linienzug ohne Wiederholung und ohne
        Unterbrechung zu umfahren. Mathematische Annalen 6(1), 30–32, 1873.

    :param graph: The input graph
    :returns: An Eulerian cycle as a :py:class:`.GraphPath` or None if the graph is not Eulerian
    """
    is_eulerian, gp = _backend.jgrapht_xx_cycles_eulerian_exec_hierholzer(graph.handle)
    return _wrap_graphpath(graph, gp) if is_eulerian else None


def chinese_postman(graph):
    r"""Run Edmonds-Johnson algorithm to solve the chinese postman problem (CPP).

    The CPP problem asks for the minimum length (weight) closed-walk that visits every
    edge of the graph at least once.

    .. note:: This implementation assumes that the graph is strongly connected, otherwise
      the behavior is undefined.

    Running time :math:`\mathcal{O}(n^3)` where :math:`n` is the number of vertices.

    See the following paper:

     * Edmonds, J., Johnson, E.L. Matching, Euler tours and the Chinese postman,
       Mathematical Programming (1973) 5: 88. doi:10.1007/BF01580113

    :param graph: the input graph. It must be strongly connected
    :returns: a closed-walk of minimum weight which visits every edge at least once
    """
    gp = _backend.jgrapht_xx_cycles_chinese_postman_exec_edmonds_johnson(graph.handle)
    return _wrap_graphpath(graph, gp)


def fundamental_cycle_basis_paton(graph):
    r"""Compute a fundamental cycle basis.

    This is a variant of Paton's algorithm, performing a BFS using a stack which
    returns a weakly fundamental cycle basis. It supports graphs with self-loops
    but not multiple edges.

    Running time :math:`\mathcal{O}(n^3)`.

    See:
      * K. Paton, An algorithm for finding a fundamental set of cycles for an
        undirected linear graph, Comm. ACM 12 (1969), pp. 514-518.

    :param graph: the graph. It must be undirected
    :returns: a tuple (weight, cycle iterator). Each cycle is returned as a
      :py:class:`.GraphPath` instance
    """
    weight, cycles_it = _backend.jgrapht_xx_cycles_fundamental_basis_exec_paton(
        graph.handle
    )
    return weight, _wrap_graphpath_iterator(graph, cycles_it)


def fundamental_cycle_basis_bfs_with_stack(graph):
    r"""Compute a fundamental cycle basis.

    Generate a set of fundamental cycles by building a spanning tree (forest) using an
    implementation of BFS using a LIFO Stack. The implementation first constructs the
    spanning forest and then builds the fundamental-cycles set. It supports graphs with
    self-loops and/or graphs with multiple edges.

    The algorithm constructs the same fundamental cycle basis as the algorithm in the
    following paper:

     * K. Paton, An algorithm for finding a fundamental set of cycles for an undirected
       linear graph, Comm. ACM 12 (1969), pp. 514-518.

    Running time :math:`\mathcal{O}(n^3)`.

    :param graph: the graph. It must be undirected
    :returns: a tuple (weight, cycle iterator). Each cycle is returned as a
      :py:class:`.GraphPath` instance
    """
    weight, cycles_it = _backend.jgrapht_xx_cycles_fundamental_basis_exec_stack_bfs(
        graph.handle
    )
    return weight, _wrap_graphpath_iterator(graph, cycles_it)


def fundamental_cycle_basis_bfs_with_queue(graph):
    r"""Compute a fundamental cycle basis.

    Generate a set of fundamental cycles by building a spanning tree (forest) using a
    straightforward implementation of BFS using a FIFO queue. The implementation first
    constructs the spanning forest and then builds the fundamental-cycles set. It supports
    graphs with self-loops and/or graphs with multiple edges.

    For information on algorithms computing fundamental cycle bases see the following paper:

     * Narsingh Deo, G. Prabhu, and M. S. Krishnamoorthy. Algorithms for Generating
       Fundamental Cycles in a Graph. ACM Trans. Math. Softw. 8, 1, 26-42, 1982.

    Running time :math:`\mathcal{O}(n^3)`.

    :param graph: the graph. It must be undirected
    :returns: a tuple (weight, cycle iterator). Each cycle is returned as a
      :py:class:`.GraphPath` instance
    """
    weight, cycles_it = _backend.jgrapht_xx_cycles_fundamental_basis_exec_queue_bfs(
        graph.handle
    )
    return weight, _wrap_graphpath_iterator(graph, cycles_it)


def enumerate_simple_cycles_tarjan(graph):
    r"""Enumerate all simple cycles in a directed graph.

    Running time :math:`\mathcal{O}(n m C)` where :math:`n` is the number of vertices,
    :math:`m` the number of edges and :math:`C` the number of simple cycles in the graph.

    .. note:: The algorithm supports self-loops but not multiple edges.

    .. note:: The algorithm returns cycles as sets of vertices.

    See the paper:

     * R. Tarjan, Enumeration of the elementary circuits of a directed graph, SIAM J.
       Comput., 2 (1973), pp. 211-216.

    :param graph: the graph. Must be directed and without multiple edges
    :returns: an iterator over the cycles. Cycles are returned as vertex sets.
    """
    cycles_it = _backend.jgrapht_xx_cycles_simple_enumeration_exec_tarjan(graph.handle)
    return _wrap_vertex_list_iterator(graph, cycles_it)


def enumerate_simple_cycles_johnson(graph):
    r"""Enumerate all simple cycles in a directed graph.

    Running time :math:`\mathcal{O}((n + m)C)` where :math:`n` is the number of vertices,
    :math:`m` the number of edges and :math:`C` the number of simple cycles in the graph.

    .. note:: The algorithm supports self-loops but not multiple edges.

    .. note:: The algorithm returns cycles as sets of vertices.

    See the paper:

     * D. B. Johnson, Finding all the elementary circuits of a directed graph,
       SIAM J. Comput., 4 (1975), pp. 77-84.

    :param graph: the graph. Must be directed and without multiple edges
    :returns: an iterator over the cycles. Cycles are returned as vertex sets.
    """
    cycles_it = _backend.jgrapht_xx_cycles_simple_enumeration_exec_johnson(graph.handle)
    return _wrap_vertex_list_iterator(graph, cycles_it)


def enumerate_simple_cycles_tiernan(graph):
    r"""Enumerate all simple cycles in a directed graph.

    Running time :math:`\mathcal{O}(n d^n)` where :math:`n` is the number of vertices,
    :math:`m` the number of edges and :math:`d` is a constant.

    .. note:: The algorithm supports self-loops but not multiple edges.

    .. note:: The algorithm returns cycles as sets of vertices.

    See the paper:

     * J.C.Tiernan An Efficient Search Algorithm Find the Elementary Circuits of a Graph.,
       Communications of the ACM, V13, 12, (1970), pp. 722 - 726.

    :param graph: the graph. Must be directed and without multiple edges
    :returns: an iterator over the cycles. Cycles are returned as vertex sets.
    """
    cycles_it = _backend.jgrapht_xx_cycles_simple_enumeration_exec_tiernan(graph.handle)
    return _wrap_vertex_list_iterator(graph, cycles_it)


def enumerate_simple_cycles_szwarcfiter_lauer(graph):
    r"""Enumerate all simple cycles in a directed graph.

    Running time :math:`\mathcal{O}((n+m)C)` where :math:`n` is the number of vertices,
    :math:`m` the number of edges and :math:`C` the number of simple cycles in the graph.

    .. note:: The algorithm supports self-loops but not multiple edges.

    .. note:: The algorithm returns cycles as sets of vertices.

    See the paper:

     * J. L. Szwarcfiter and P. E. Lauer, Finding the elementary cycles of a directed
       graph in O(n + m) per cycle, Technical Report Series, #60, May 1974, Univ. of
       Newcastle upon Tyne, Newcastle upon Tyne, England.

    :param graph: the graph. Must be directed and without multiple edges
    :returns: an iterator over the cycles. Cycles are returned as vertex sets.
    """
    cycles_it = _backend.jgrapht_xx_cycles_simple_enumeration_exec_szwarcfiter_lauer(
        graph.handle
    )
    return _wrap_vertex_list_iterator(graph, cycles_it)


def enumerate_simple_cycles_hawick_james(graph):
    r"""Enumerate all simple cycles in a directed graph.

    Running time :math:`\mathcal{O}((n+m)C)` where :math:`n` is the number of vertices,
    :math:`m` the number of edges and :math:`C` the number of simple cycles in the graph.
    This algorithm is a variant of Johnson' algorithm.

    .. note:: The algorithm supports self-loops but not multiple edges.

    .. note:: The algorithm returns cycles as sets of vertices.

    See the paper:

     * Hawick, Kenneth A., and Heath A. James. "Enumerating Circuits and Loops in Graphs
       with Self-Arcs and Multiple-Arcs." FCS. 2008.

    :param graph: the graph. Must be directed and without multiple edges
    :returns: an iterator over the cycles. Cycles are returned as vertex sets.
    """
    cycles_it = _backend.jgrapht_xx_cycles_simple_enumeration_exec_hawick_james(
        graph.handle
    )
    return _wrap_vertex_list_iterator(graph, cycles_it)


def howard_minimum_cycle_mean(graph, iterations=2147483647, tolerance=1e-9):
    r"""Howard`s algorithm for finding the minimum cycle mean in a graph.

    The algorithm is described in the article: Ali Dasdan, Sandy S. Irani, and Rajesh K. Gupta. 1999.
    Efficient algorithms for optimum cycle mean and optimum cost to time ratio problems. In
    Proceedings of the 36th annual ACM/IEEE Design Automation Conference (DAC ’99). Association for
    Computing Machinery, New York, NY, USA, 37–42. DOI:https://doi.org/10.1145/309847.309862

    Initially, the graph is divided into strongly connected components. The minimum cycle mean is then
    computed as the globally minimum cycle mean over all components. The computation is done iteratively.
    In each iteration the algorithm tries to update the current minimum cycle mean value.
    The number of iterations can be limited by the function paremeters.

    :param graph: The input graph
    :param iterations: maximum iterations
    :param tolerance: tolerance when comparing floating point values
    :returns: a tuple (weight, cycle). The cycle is returned as a :py:class:`.GraphPath` instance
    """
    mean, cycle = _backend.jgrapht_xx_cycles_mean_exec_howard(
        graph.handle, iterations, tolerance
    )
    return mean, _wrap_graphpath(graph, cycle) if cycle is not None else None
