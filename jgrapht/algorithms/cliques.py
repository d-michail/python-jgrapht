from .. import backend
from .._internals._wrappers import _JGraphTLongSetIterator


def _clique_enumeration_alg(name, graph, *args):
    alg_method_name = "jgrapht_clique_exec_"
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise NotImplementedError("Algorithm not supported.")

    _, clique_it = alg_method(graph.handle, *args)

    return _JGraphTLongSetIterator(handle=clique_it)


def bron_kerbosch(graph, timeout=0):
    """Bron-Kerbosch maximal clique enumeration algorithm.

    Implementation of the Bron-Kerbosch clique enumeration algorithm as described in:
    
     * R. Samudrala and J. Moult. A graph-theoretic algorithm for comparative modeling of protein
       structure. Journal of Molecular Biology, 279(1):287--302, 1998.

    The algorithm first computes all maximal cliques and then returns the result to the user. A
    timeout (in seconds) can be set using the parameters.

    :param graph: The input graph which should be simple
    :param timeout: Timeout in seconds. No timeout if zero
    :returns: An iterator over maximal cliques
    """
    custom = [timeout]
    return _clique_enumeration_alg("bron_kerbosch", graph, *custom)


def bron_kerbosch_with_pivot(graph, timeout=0):
    r"""Bron-Kerbosch maximal clique enumeration algorithm with pivot.

    The pivoting follows the rule from the paper:
    
     * E. Tomita, A. Tanaka, and H. Takahashi. The worst-case time complexity for generating all
       maximal cliques and computational experiments. Theor. Comput. Sci. 363(1):28–42, 2006.

    where the authors show that using that rule guarantees that the Bron-Kerbosch algorithm has
    worst-case running time :math:`\mathcal{O}(3^{n/3})` where :math:`n` is the number of vertices
    of the graph, excluding time to write the output, which is worst-case optimal.
 
    The algorithm first computes all maximal cliques and then returns the result to the user. A
    timeout (in seconds) can be set using the parameters.

    :param graph: The input graph which should be simple
    :param timeout: Timeout in seconds. No timeout if zero
    :returns: An iterator over maximal cliques
    """
    custom = [timeout]
    return _clique_enumeration_alg("bron_kerbosch_pivot", graph, *custom)


def bron_kerbosch_with_degeneracy_ordering(graph, timeout=0):
    r"""Bron-Kerbosch maximal clique enumeration algorithm with pivot and degeneracy ordering.

    The algorithm is a variant of the Bron-Kerbosch algorithm which apart from the pivoting
    uses a degeneracy ordering of the vertices. The algorithm is described in 
     
      * David Eppstein, Maarten Löffler and Darren Strash. Listing All Maximal Cliques in Sparse
        Graphs in Near-Optimal Time. Algorithms and Computation: 21st International Symposium
        (ISSAC), 403--414, 2010.
 
    and has running time :math:`\mathcal{O}(d n 3^{d/3})` where :math:`n` is the number of
    vertices of the graph and :math:`d` is the degeneracy of the graph. The algorithm looks for
    a maximal clique parameterized by degeneracy, a frequently-used measure of the sparseness
    of a graph that is closely related to other common sparsity measures such as arboricity and
    thickness, and that has previously been used for other fixed-parameter problems.
 
    The algorithm first computes all maximal cliques and then returns the result to the user. A
    timeout (in seconds) can be set using the parameters.

    :param graph: The input graph which should be simple
    :param timeout: Timeout in seconds. No timeout if zero
    :returns: An iterator over maximal cliques
    """
    custom = [timeout]
    return _clique_enumeration_alg("bron_kerbosch_pivot", graph, *custom)
