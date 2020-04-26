from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from ..util import JGraphTLongSet

def _mst_alg(name, graph):
    alg_method_name = 'jgrapht_mst_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, weight, mst_handle = alg_method(graph.handle)
    if err:
        raise_status()

    return weight, JGraphTLongSet(mst_handle)


def mst_kruskal(graph):
    r"""Compute the minimum spanning tree using `Kruskal's algorithm <https://en.wikipedia.org/wiki/Kruskal's_algorithm>`_.

    
    If the given graph is connected it computes the minimum spanning tree, otherwise it computes
    the minimum spanning forest. The algorithm runs in time :math:`\mathcal{O}(m \log m)` or
    :math:`\mathcal{O}(m \log n)` in case multiple edges are not allowed and thus :math:`m \le n^2`.
    Here :math:`n` is the number of vertices and :math:`m` the number of edges of the graph.

    :param graph: The input graph
    :returns: A tuple (weight, mst) 
    """
    return _mst_alg('kruskal', graph)

def mst_prim(graph):
    r"""Compute the minimum spanning tree using `Prim's algorithm <https://en.wikipedia.org/wiki/Prim's_algorithm>`_.

    The algorithm was developed by Czech mathematician V. Jarník and later independently by computer scientist
    Robert C. Prim and rediscovered by E. Dijkstra. This implementation uses a Fibonacci Heap in order to 
    achieve a running time of :math:`\mathcal{O}(m+n\log n)` where :math:`n` is the number of vertices and 
    :math:`m` the number of edges of the graph.

    :param graph: The input graph
    :returns: A tuple (weight, mst) 
    """
    return _mst_alg('prim', graph)


def mst_boruvka(graph):
    r"""Compute the minimum spanning tree using `Borůvka's algorithm <https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm>`_.

    This implementation uses a union-find data structure (with union by rank and path compression
    heuristic) in order to track components. In graphs where edges have identical weights, edges with
    equal weights are ordered lexicographically. The running time is :math:`\mathcal{O}((m+n) \log n)` under the
    assumption that the union-find uses path-compression.
    Here :math:`n` is the number of vertices and :math:`m` the number of edges of the graph.

    :param graph: The input graph
    :returns: A tuple (weight, mst) 
    """
    return _mst_alg('boruvka', graph)
    