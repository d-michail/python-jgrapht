import time
from .. import backend as _backend

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._clustering import _JGraphTClustering
from .._internals._anyhashableg_clustering import _AnyHashableGraphClustering


def k_spanning_tree(graph, k):
    r"""The k spanning tree clustering algorithm. 

    The algorithm finds a minimum spanning tree T using Prim's algorithm, then executes Kruskal's
    algorithm only on the edges of T until k trees are formed. The resulting trees are the final
    clusters. The total running time is :math:`\mathcal{O}(m + n \log n)`.
  
    The algorithm is strongly related to single linkage cluster analysis, also known as single-link
    clustering. For more information see: J. C. Gower and G. J. S. Ross. Minimum Spanning Trees and
    Single Linkage Cluster Analysis. Journal of the Royal Statistical Society. Series C (Applied
    Statistics), 18(1):54--64, 1969.

    :param graph: the graph. Needs to be undirected
    :param k: integer k, denoting the number of clusters
    :returns: a clustering as an instance of :py:class:`.Clustering`
    """
    handle = _backend.jgrapht_clustering_exec_k_spanning_tree(graph.handle, k)
    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphClustering(handle, graph)
    else:
        return _JGraphTClustering(handle)


def label_propagation(graph, max_iterations=None, seed=None):
    r"""Label propagation clustering.

    The algorithm is a near linear time algorithm capable of discovering communities in large graphs.
    It is described in detail in the following `paper <https://dx.doi.org/10.1103/PhysRevE.76.036106>`_:
     
      * Raghavan, U. N., Albert, R., and Kumara, S. (2007). Near linear time algorithm to detect
        community structures in large-scale networks. Physical review E, 76(3), 036106.

    As the paper title suggests the running time is close to linear. The algorithm runs in iterations,
    each of which runs in :math:`\mathcal{O}(n + m)` where :math:`n` is the number of vertices and
    :math:`m` is the number of edges. The authors found experimentally that in most cases, 95% of the
    nodes or more are classified correctly by the end of iteration five. See the paper for more details.

    The algorithm is randomized, meaning that two runs on the same graph may return different results.
    If the user requires deterministic behavior, a random generator seed can be provided as a parameter.

    :param graph: the graph. Needs to be undirected
    :param max_iterations: maximum number of iterations (None means no limit)
    :param seed: seed for the random number generator, if None then the system time is used
    :returns: a clustering as an instance of :py:class:`.Clustering`
    """
    if seed is None:
        seed = int(time.time())
    if max_iterations is None:
        max_iterations = 0
    args = [max_iterations, seed]

    handle = _backend.jgrapht_clustering_exec_label_propagation(graph.handle, *args)
    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphClustering(handle, graph)
    else:
        return _JGraphTClustering(handle)
