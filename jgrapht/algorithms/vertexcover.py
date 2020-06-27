from .. import backend as _backend

from .._internals._collections import (
    _JGraphTIntegerDoubleMutableMap,
    _JGraphTIntegerSet,
)

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_collections import _AnyHashableGraphVertexSet


def _copy_vertex_weights(graph, vertex_weights):
    jgrapht_vertex_weights = _JGraphTIntegerDoubleMutableMap()
    if _is_anyhashable_graph(graph):
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[graph._vertex_hash_to_id[key]] = val
    else:
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[key] = val
    return jgrapht_vertex_weights


def _vertexcover_alg(name, graph, vertex_weights=None):
    alg_method_name = "jgrapht_vertexcover_exec_" + name
    if vertex_weights is not None:
        alg_method_name += "_weighted"
    alg_method = getattr(_backend, alg_method_name)

    if vertex_weights is not None:
        jgrapht_vertex_weights = _copy_vertex_weights(graph, vertex_weights)
        weight, vc_handle = alg_method(graph.handle, jgrapht_vertex_weights.handle)
    else:
        weight, vc_handle = alg_method(graph.handle)

    if _is_anyhashable_graph(graph):
        return weight, _AnyHashableGraphVertexSet(vc_handle, graph)
    else:
        return weight, _JGraphTIntegerSet(vc_handle)


def greedy(graph, vertex_weights=None):
    r"""A greedy algorithm for the vertex cover problem.

    At each iteration the algorithm picks the vertex :math:`v` with 
    the minimum ration of weight over degree. Afterwards it removes all 
    its incident edges and recurses.

    Its running time is :math:`\mathcal{O}(m \log n)`. The implementation
    supports both the uniform and the weighted case where the graph vertices
    have weights.

    :param graph: the input graph. It must be undirected. Self-loops and multiple edges
                  are allowed
    :param vertex_weights: an optional dictionary of vertex weights
    :returns: a tuple (weight, vertex set)
    """
    return _vertexcover_alg("greedy", graph, vertex_weights)


def clarkson(graph, vertex_weights=None):
    r"""Compute a vertex cover using the 2-opt algorithm of Clarkson.

    The algorithm runs in time :math:`\mathcal{O}(m \log n)` and is a 2-approximation
    which means that the solution is guaranteed to be at most twice the optimum.
    
    For more information see the following paper:

    Clarkson, Kenneth L. A modification of the greedy algorithm for vertex cover.
    Information Processing Letters 16.1 (1983): 23-25.

    :param graph: the input graph. It must be undirected. Self-loops and multiple edges
                are allowed
    :param vertex_weights: an optional dictionary of vertex weights
    :returns: a tuple (weight, vertex set)
    """
    return _vertexcover_alg("clarkson", graph, vertex_weights)


def edgebased(graph):
    r"""A 2-opt algorithm for the minimum vertex cover.

    This is a 2-approximation algorithm with running time :math:`\mathcal{O}(m)`.

    :param graph: the input graph. It must be undirected. Self-loops and multiple edges
                are allowed
    :returns: a tuple (weight, vertex set)
    """
    return _vertexcover_alg("edgebased", graph)


def baryehuda_even(graph, vertex_weights=None):
    r"""The 2-opt algorithm for a minimum weighted vertex cover by R. Bar-Yehuda and S. Even.

    This is a 2-approximation algorithm with running time :math:`\mathcal{O}(m)`.

    :param graph: the input graph. It must be undirected. Self-loops and multiple edges
                are allowed
    :param vertex_weights: an optional dictionary of vertex weights
    :returns: a tuple (weight, vertex set)
    """
    return _vertexcover_alg("baryehudaeven", graph, vertex_weights)


def exact(graph, vertex_weights=None):
    r"""Compute a vertex cover exactly using a recursive algorithm.

    At each recursive step the algorithm picks a vertex and either includes in the 
    cover or it includes all of its neighbors. To speed up the algorithm, memoization
    and a bounding procedure is also used.

    Can solve instances with around 150-200 vertices to optimality.
    
    :param graph: the input graph. It must be undirected
    :param vertex_weights: an optional dictionary of vertex weights
    :returns: a tuple (weight, vertex set)
    """
    return _vertexcover_alg("exact", graph, vertex_weights)
