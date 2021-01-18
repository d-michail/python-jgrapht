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
    r"""Edmonds blossom algorithm for maximum cardinality matching in general undirected graphs.

    A matching in a graph :math:`G(V,E)` is a subset of edges :math:`M` such that no two edges
    in :math:`M` have a vertex in common. A matching has at most :math:`\frac{1}{2}|V|` edges.
    A node :math:`v` in :math:`G` is matched by matching :math:`M` if :math:`M` contains an edge
    incident to :math:`v`. A matching is perfect if all nodes are matched. By definition, a perfect
    matching consists of exactly :math:`\frac{1}{2}|V|` edges. This algorithm will return a
    perfect matching if one exists. If no perfect matching exists, then the largest (non-perfect)
    matching is returned instead. In the special case that the input graph is bipartite, consider
    using :py:meth:`.bipartite_max_cardinality()` instead.

    To compute a maximum cardinality matching, at most :math:`n` augmenting path computations are
    performed. Each augmenting path computation takes :math:`\mathcal{O}(m \alpha(m,n))` time,
    where :math:`\alpha(m,n)` is the inverse of the Ackerman function, :math:`n` is the number of
    vertices, and :math:`m` the number of edges. This results in a total runtime complexity of
    :math:`\mathcal{O}(n m \alpha (m,n))`. In practice, the number of augmenting path computations
    performed is far smaller than :math:`n`, since an efficient heuristic (greedy maximum cardinality 
    matching algorithm)  is used to compute a near-optimal initial solution.

    The runtime complexity of this implementation could be improved to :math:`\mathcal{O}(nm)` when
    the UnionFind data structure used in this implementation is replaced by the linear-time set union
    data structure proposed in: Gabow, H.N., Tarjan, R.E. A linear-time algorithm for a special
    case of disjoint set union. Proc. Fifteenth Annual ACM Symposium on Theory of Computing, 1982,
    pp. 246-251.

    Edmonds' original algorithm first appeared in Edmonds, J. Paths, trees, and flowers. Canadian
    Journal of Mathematics 17, 1965, pp. 449-467, and had a runtime complexity of
    :math:`\mathcal{O}(n^4)`.

    This method utilizes two different implementation depending on whether the user adjusts the input
    parameter `dense`:

      * If `dense` is true then this implementation follows more closely the description provided in
        Tarjan, R.E. Data Structures and Network Algorithms. Society for Industrial and Applied
        Mathematics, 1983, chapter 9. In addition, the following sources were used for the
        implementation:

          * `Java implementation by John Mayfield <https://github.com/johnmay/beam/blob/master/core/src/main/java/uk/ac/ebi/beam/MaximumMatching.java>`_
          * `Java implementation by Keith Schwarz <http://www.keithschwarz.com/interesting/code/?dir=edmonds-matching>`_
          * `C++ implementation Boost library <https://www.boost.org/doc/libs/1_38_0/libs/graph/doc/maximum_matching.html>`_
          * Cook, W.J., Cunningham, W.H., Pulleyblank, W.R., Schrijver, A. Combinatorial Optimization. Wiley 1997, chapter 5
          * `Gabow, H.N. Data Structures for Weighted Matching and Extensions to b-matching and f-factors, 2016 <https://arxiv.org/pdf/1611.07541.pdf>`_

      * If `dense` is false then this is the algorithm and implementation described in the 
        `LEDA book <https://people.mpi-inf.mpg.de/~mehlhorn/LEDAbook.html>`_. See the LEDA Platform
        of Combinatorial and Geometric Computing, Cambridge University Press, 1999.
    
    For future reference, a more efficient algorithm than the one implemented here exists:
    Micali, S., Vazirani, V. An :math:`\mathcal{O}(\sqrt{n}m)` algorithm for finding maximum matching
    in general graphs. Proc. 21st Ann. Symp. on Foundations of Computer Science, IEEE, 1980, pp. 17–27.
    This is the most efficient algorithm known for computing maximum cardinality matchings in general
    graphs. More details on this algorithm can be found in:

      * `Presentation from Vazirani 'Dispelling an Old Myth about an Ancient Algorithm' <http://research.microsoft.com/apps/video/dl.aspx?id=171055>`_
      * `Vazirani, V. A Simplification of the MV Matching Algorithm and its Proof, 2013 <https://arxiv.org/abs/1210.4594>`_

    :param graph: the graph
    :param dense: whether to use the dense version or the sparse one
    :returns: an edge set corresponding to the matching
    """
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
    r"""The greedy algorithm for computing a maximum weight matching in an arbitrary graph.

    The algorithm runs in :math:`\mathcal{O}(m+m \log n)` where :math:`n` is the number of
    vertices and :math:`m` is the number of edges of the graph. This implementation accepts
    directed and undirected graphs which may contain self-loops and multiple (parallel) edges.
    There is no assumption on the edge weights, i.e. they can also be negative or zero.

    This algorithm can be run in two modes: with and without edge cost normalization. Without
    normalization, the algorithm first orders the edge set in non-increasing order of weights
    and then greedily constructs a maximal cardinality matching out of the edges with positive
    weight. A maximal cardinality matching (not to be confused with maximum cardinality) is a
    matching that cannot be increased in cardinality without removing an edge first. The
    resulting matching is guaranteed to be a 1/2-approximation.

    With normalization, the edges are sorted in non-increasing order of their normalized costs
    :math:`\frac{c(u,v)}{d(u)+d(v)}` instead, after which the algorithm proceeds in the same
    manner. Here, :math:`c(u,v)` is the cost of edge :math:`(u,v)`, and :math:`d(u)` resp
    :math:`d(v)` are the degrees of vertices :math:`u` resp :math:`v`. Running this algorithm
    in normalized mode often (but not always!) produces a better result than running the algorithm
    without normalization. Note however that the normalized version does NOT produce a
    1/2-approximation. See `this proof <https://mathoverflow.net/questions/269526/is-greedy-matching-algorithm-with-normalized-edge-weights-a-2-approximation/269760#269760>`_ for
    details. The runtime complexity remains the same, independent of whether normalization is used.

    For more information about approximation algorithms for the maximum weight matching problem
    in arbitrary graphs see: 
    
      * R. Preis, Linear Time 1/2-Approximation Algorithm for Maximum Weighted
        Matching in General Graphs. Symposium on Theoretical Aspects of Computer Science, 259-269, 1999
      * D.E. Drake, S. Hougardy, A Simple Approximation Algorithm for the Weighted Matching Problem,
        Information Processing Letters 85, 211-213, 2003

    :param graph: the graph
    :param normalize_edge_costs: whether to normalize edge costs
    :param tolerance: tolerance for floating point comparisons
    :returns: an edge set corresponding to the matching
    """
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

      * D.E. Drake, S. Hougardy, A Simple Approximation Algorithm for the Weighted Matching Problem, 
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
    """Compute maximum (perfect or not) weighted matchings in general graphs using the 
    blossom V algorithm.

    For more information about the algorithm see the following paper: Kolmogorov, V.
    Math. Prog. Comp. (2009) 1: 43. https://doi.org/10.1007/s12532-009-0002-8, and
    the original implementation: http://pub.ist.ac.at/~vnk/software/blossom5-v2.05.src.tar.gz

    :param graph: the graph
    :param perfect: whether to compute a perfect matching
    :returns: an edge set corresponding to the matching
    """
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
    """Compute minimm (perfect or not) weighted matchings in general graphs using the 
    blossom V algorithm.

    For more information about the algorithm see the following paper: Kolmogorov, V.
    Math. Prog. Comp. (2009) 1: 43. https://doi.org/10.1007/s12532-009-0002-8, and
    the original implementation: http://pub.ist.ac.at/~vnk/software/blossom5-v2.05.src.tar.gz

    :param graph: the graph
    :param perfect: whether to compute a perfect matching
    :returns: an edge set corresponding to the matching
    """    
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
    """The well-known Hopcroft Karp algorithm to compute a matching of maximum cardinality
    in a bipartite graph.

    The algorithm runs in :math:`\mathcal{O}(m \sqrt{n})` time. This implementation accepts
    undirected graphs which may contain self-loops and multiple edges. To compute a maximum
    cardinality matching in general (non-bipartite) graphs, use :py:meth:`.edmonds_max_cardinality()`
    instead.

    The Hopcroft-Karp matching algorithm computes augmenting paths of increasing length, until
    no augmenting path exists in the graph. At each iteration, the algorithm runs a Breadth-First
    Search from the exposed (free) vertices, until an augmenting path is found. Next, a Depth-First
    Search is performed to find all (vertex disjoint) augmenting paths of the same length.
    The matching is augmented along all discovered augmenting paths simultaneously.

    The original algorithm is described in: Hopcroft, John E.; Karp, Richard M. (1973), "An
    :math:`n^{5/2}` algorithm for maximum matchings in bipartite graphs", SIAM Journal on Computing
    2 (4): 225–231. A coarse overview of the algorithm is given
    in: http://en.wikipedia.org/wiki/Hopcroft-Karp_algorithm

    :param graph: the graph (must be bipartite)
    :returns: an edge set corresponding to the matching
    """
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
    """Kuhn-Munkres algorithm. 
    
    The Kuhn-Munkres (named in honor of Harold Kuhn and James Munkres) solving the assignment
    problem also known as the hungarian algorithm (in the honor of hungarian mathematicians
    Dénes König and Jenö Egerváry). It's running time is :math:`\mathcal{O}(n^3)` where :math:`n`
    are the number of vertices in the graph.

    The assignment problem is the following problem: Given a complete bipartite graph 
    :math:`G=(S,T;E)`, such that :math:`|S|=|T|`, and each edge has non-negative cost
    :math:`c(i, j)`, find a perfect matching of minimum cost.

    :param graph: the graph (must be bipartite)
    :param partition_a: a vertex set for one of the two vertices partitions
    :param partition_b: a vertex set for the other of the two vertices partitions
    :returns: an edge set corresponding to the matching
    """
    partition_a = _build_vertex_set(graph, partition_a)
    partition_b = _build_vertex_set(graph, partition_b)

    weight, m_handle = _backend.jgrapht_xx_matching_exec_bipartite_perfect_min_weight(
        graph.handle, partition_a.handle, partition_b.handle
    )
    return weight, _wrap_edge_set(graph, m_handle)
