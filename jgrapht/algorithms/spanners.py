from .. import backend
from .._errors import raise_status
from ..util import JGraphTLongSet


def spanner_multiplicative_greedy(graph, k):
    r"""Greedy algorithm for :math:`(2k-1)`-multiplicative spanner construction (for any integer :math:`k \ge 1`.
 
    The spanner is guaranteed to contain :math:`\mathcal{O}(n^{1+1/k})` edges and the shortest path
    distance between any two vertices in the spanner is at most :math:`2k-1` times the corresponding
    shortest path distance in the original graph. Here :math:`n` denotes the number of vertices of
    the graph.
 
    The algorithm is described in: Althoefer, Das, Dobkin, Joseph, Soares. 
    `On Sparse Spanners of Weighted Graphs <https://doi.org/10.1007/BF02189308>`_. Discrete
    Computational Geometry 9(1):81-100, 1993.

    If the graph is unweighted the algorithm runs in :math:`\mathcal{O}(m n^{1+1/k})` time. Setting
    :math:`k` to infinity will result in a slow version of Kruskal's algorithm where cycle detection
    is performed by a BFS computation. In such a case use the implementation of Kruskal with
    union-find. Here :math:`n` and :math:`m` are the number of vertices and edges of the graph
    respectively.
 
    If the graph is weighted the algorithm runs in :math:`\mathcal{O}(m (n^{1+1/k} + n \log n))` time
    by using Dijkstra's algorithm. Edge weights must be non-negative.

    :param graph: The input graph
    :param k: integer
    :returns: tuple of the form (weight, spanner_edges)
    """
    err, weight, spanner = backend.jgrapht_spanner_exec_greedy_multiplicative(graph.handle, k)
    if err:
        raise_status()
    return weight, JGraphTLongSet(spanner)

