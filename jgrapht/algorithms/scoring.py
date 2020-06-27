from .. import backend as _backend

from .._internals._collections import (
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerIntegerMap,
)

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_collections import (
    _AnyHashableGraphVertexDoubleMap,
    _AnyHashableGraphVertexIntegerMap,
)


def _wrap_result(graph, scores_handle):
    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphVertexDoubleMap(scores_handle, graph)
    else:
        return _JGraphTIntegerDoubleMap(scores_handle)


def alpha_centrality(
    graph,
    damping_factor=0.01,
    exogenous_factor=1.0,
    max_iterations=100,
    tolerance=0.0001,
):
    r"""Alpha centrality.

    See https://en.wikipedia.org/wiki/Alpha_centrality for a description of alpha centrality.

    This is a simple iterative implementation of which stops after a given number of iterations
    or if the centralityvalues between two iterations do not change more than a predefined value.

    Each iteration of the algorithm runs in linear time :math:`\mathcal{O}(n+m)` when :math:`n` is
    the number of nodes and :math:`m` the number of edges in the graph. The maximum number of
    iterations can be adjusted by the caller. 
    
    By adjusting the exogenous factor, users may compute either eigenvector centrality 
    (https://en.wikipedia.org/wiki/Eigenvector_centrality) or Katz centrality
    (https://en.wikipedia.org/wiki/Katz_centrality).

    :param graph: the graph
    :param damping_factor: the damping factor
    :param exogenous_factor: the exogenous factor
    :param max_iterations: maximum iterations
    :param tolerance: tolerance. The calculation will stop if the difference of centrality
       values between iterations change less than this value
    :returns: a dictionary from vertices to double values
    """
    custom = [damping_factor, exogenous_factor, max_iterations, tolerance]
    scores_handle = _backend.jgrapht_scoring_exec_custom_alpha_centrality(
        graph.handle, *custom
    )
    return _wrap_result(graph, scores_handle)


def betweenness_centrality(graph, incoming=False, normalize=False):
    r"""Betweenness centrality.
    
    For the definition see https://en.wikipedia.org/wiki/Betweenness_centrality. 

    The algorithm is based on:

     * Brandes, Ulrik (2001). "A faster algorithm for betweenness centrality". Journal of
       Mathematical Sociology. 25 (2): 163–177.

    Running time is :math:`\mathcal{O}(nm +n^2 \log n)` for weighted and :math:`\mathcal{O}(mn)` 
    for unweighted graphs.

    .. note :: if normalization is used, then the result is divided by :math:`(n-1) \cdot (n-2)` 
               where :math:`n` is the number of vertices in the graph

    :param graph: the graph
    :param normalize: whether to use normalization
    :returns: a dictionary from vertices to double values
    """
    custom = [normalize]
    scores_handle = _backend.jgrapht_scoring_exec_custom_betweenness_centrality(
        graph.handle, *custom
    )
    return _wrap_result(graph, scores_handle)


def closeness_centrality(graph, incoming=False, normalize=True):
    r"""Closeness centrality.

    Computes the closeness centrality of each vertex of a graph. The closeness
    of a vertex :math:`x` is defined as the reciprocal of the farness, that
    is :math:`H(x)= 1 / \sum_{y \neq x} d(x,y)`, where :math:`d(x,y)` is the shortest
    path distance from :math:`x` to :math:`y`. When normalization is used, the score is
    multiplied by :math:`n-1` where :math:`n` is the total number of vertices in the
    graph. For more details see https://en.wikipedia.org/wiki/Closeness_centrality
    and

      * Alex Bavelas. Communication patterns in task-oriented groups. J. Acoust. Soc. Am,
        22(6):725–730, 1950.
 
    This implementation computes by default the closeness centrality using outgoing paths and
    normalizes the scores. This behavior can be adjusted by the arguments.
 
    When the graph is disconnected, the closeness centrality score equals :math:`0` for all
    vertices. In the case of weakly connected digraphs, the closeness centrality of several
    vertices might be :math:`0`. See :py:meth:`~jgrapht.algorithms.scoring.harmonic_centrality`
    for a different approach in case of disconnected graphs.
    
    Shortest paths are computed either by using Dijkstra's algorithm or Floyd-Warshall depending
    on whether the graph has edges with negative edge weights. Thus, the running time is either
    :math:`\mathcal{O}(n (m + n \log n))` or :math:`\mathcal{O}(n^3)` respectively, where
    :math:`n` is the number of vertices and :math:`m` the number of edges of the graph.

    :param graph: the graph
    :param incoming: if True then the incoming edges are used instead of the outgoing
    :param normalize: whether to use normalization
    :returns: a dictionary from vertices to double values
    """
    custom = [incoming, normalize]
    scores_handle = _backend.jgrapht_scoring_exec_custom_closeness_centrality(
        graph.handle, *custom
    )
    return _wrap_result(graph, scores_handle)


def harmonic_centrality(graph, incoming=False, normalize=True):
    r"""Harmonic Centrality. The harmonic centrality of a vertex :math:`x` is defined as

    .. math:: 
    
      H(x)=\sum_{y \neq x} 1/d(x,y)

    where :math:`d(x,y)` is the shortest path
    distance from :math:`x` to :math:`y`. In case a
    distance :math:`d(x,y)` is equal to infinity, then :math:`1/d(x,y)=0`. When normalization is used the
    score is divided by :math:`n-1` where :math:`n` is the total number of vertices in the graph.
 
    For details see the following papers:

      * Yannick Rochat. Closeness centrality extended to unconnected graphs: The harmonic centrality
        index. Applications of Social Network Analysis, 2009.
      * Newman, Mark. 2003. The Structure and Function of Complex Networks. SIAM Review, 45(mars),
        167–256

    and https://en.wikipedia.org/wiki/Closeness_centrality.
 
    This implementation computes by default the centrality using outgoing paths and normalizes the
    scores. This behavior can be adjusted by the arguments.

    Shortest paths are computed either by using Dijkstra's algorithm or Floyd-Warshall depending on
    whether the graph has edges with negative edge weights. Thus, the running time is either
    :math:`\mathcal{O}(n (m + n \log n))` or :math:`\mathcal{O}(n^3)` respectively, where
    :math:`n` is the number of vertices and :math:`m` the number of edges of the graph.

    :param graph: the graph
    :param incoming: if True then the incoming edges are used instead of the outgoing
    :param normalize: whether to use normalization
    :returns: a dictionary from vertices to double values
    """
    custom = [incoming, normalize]
    scores_handle = _backend.jgrapht_scoring_exec_custom_harmonic_centrality(
        graph.handle, *custom
    )
    return _wrap_result(graph, scores_handle)


def pagerank(graph, damping_factor=0.85, max_iterations=100, tolerance=0.0001):
    r"""PageRank

    The `wikipedia <https://en.wikipedia.org/wiki/PageRank>`_ article contains a nice
    description of PageRank. The method can be found on the article: Sergey Brin and Larry Page: The
    Anatomy of a Large-Scale Hypertextual Web Search Engine. Proceedings of the 7th World-Wide Web
    Conference, Brisbane, Australia, April 1998. See also the following
    `page <http://infolab.stanford.edu/~backrub/google.html>`_.

    This is a simple iterative implementation of PageRank which stops after a given number of
    iterations or if the PageRank values between two iterations do not change more than a predefined
    value. The implementation uses the variant which divides by the number of nodes, thus forming a
    probability distribution over graph nodes.

    Each iteration of the algorithm runs in linear time :math:`\mathcal{O}(n+m)` when :math:`n` is
    the number of nodes and :math:`m` the number of edges of the graph. The maximum number of
    iterations can be adjusted by the caller.
 
    If the graph is a weighted graph, a weighted variant is used where the probability of following
    an edge e out of node :math:`v` is equal to the weight of :math:`e` over the sum of weights of
    all outgoing edges of :math:`v`.
    
    :param graph: the graph
    :param damping_factor: damping factor
    :param max_iterations: max iterations
    :param tolerance: tolerance. The calculation will stop if the difference of PageRank
       values between iterations change less than this value
    :returns: a dictionary from vertices to double values
    """
    custom = [damping_factor, max_iterations, tolerance]
    scores_handle = _backend.jgrapht_scoring_exec_custom_pagerank(graph.handle, *custom)
    return _wrap_result(graph, scores_handle)


def coreness(graph):
    r"""Computes the coreness of each vertex in an undirected graph.
 
    A :math:`k`-core of a graph :math:`G` is a maximal connected subgraph of :math:`G` in
    which all vertices have degree at least :math:`k`. Equivalently, it is one of the
    connected components of the subgraph of :math:`G` formed by repeatedly deleting all
    vertices of degree less than :math:`k`. A vertex :math:`u` has coreness :math:`c` if it
    belongs to a :math:`c`-core but not to any :math:`(c+1)`-core.

    If a non-empty :math:`k`-core exists, then, clearly, :math:`G` has
    `degeneracy <https://en.wikipedia.org/wiki/Degeneracy_(graph_theory)>`_ at least :math:`k`,
    and the degeneracy of :math:`G` is the largest :math:`k` for which :math:`G` has
    a :math:`k`-core.
 
    As described in the following paper

      * D. W. Matula and L. L. Beck. Smallest-last ordering and clustering and graph coloring
        algorithms. Journal of the ACM, 30(3):417--427, 1983.

    it is possible to find a vertex ordering of a finite graph :math:`G` that optimizes the
    coloring number of the ordering, in linear time, by using a bucket queue to repeatedly
    find and remove the vertex of smallest degree.

    :param graph: the graph
    :returns: a tuple containing the degeneracy and a dictionary from vertices to integer
      values (coreness of each vertex)
    """
    degeneracy, scores_handle = _backend.jgrapht_scoring_exec_coreness(graph.handle)

    if _is_anyhashable_graph(graph):
        return degeneracy, _AnyHashableGraphVertexIntegerMap(scores_handle, graph)
    else:
        return degeneracy, _JGraphTIntegerIntegerMap(scores_handle)


def clustering_coefficient(graph):
    r"""Clustering Coefficient.

    For definitions see https://en.wikipedia.org/wiki/Clustering_coefficient.

    Computes the local clustering coefficient for each vertex of a graph. It also computes 
    both the global and the average clustering coefficient.

    The global clustering coefficient is discussed in 

      * R. D. Luce and A. D. Perry (1949). "A method of matrix analysis of group structure".
        Psychometrika. 14 (1): 95–116. doi:10.1007/BF02289146 .
 
    The average local clustering coefficient was introduced in
    
      * D. J. Watts and Steven Strogatz (June 1998). "Collective dynamics of 'small-world'
        networks". Nature. 393 (6684): 440–442. doi:10.1038/30918

    Running time is :math:`\mathcal{O}(n + \Delta(G)^2)` where :math:`n` is the number of 
    vertices in the graph and :math:`\Delta(G)` is the maximum degree of any vertex.

    :param graph: the graph
    :returns: a tuple (global, avg, local coefficients dictionary)
    """
    (
        global_cc,
        avg_cc,
        cc_map_handle,
    ) = _backend.jgrapht_scoring_exec_clustering_coefficient(graph.handle)

    if _is_anyhashable_graph(graph):
        return global_cc, avg_cc, _AnyHashableGraphVertexDoubleMap(cc_map_handle, graph)
    else:
        return global_cc, avg_cc, _JGraphTIntegerDoubleMap(cc_map_handle)
