from .. import backend
from .._internals._errors import _raise_status, UnsupportedOperationError
from .._internals._wrappers import _JGraphTPlanarEmbedding, _JGraphTGraph


def _planarity_alg(name, graph, *args):
    alg_method_name = "jgrapht_planarity_exec_"
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")

    err, is_planar, embedding, kuratowski_subdivision = alg_method(graph.handle, *args)
    if err:
        _raise_status()

    if is_planar:
        return is_planar, _JGraphTPlanarEmbedding(embedding)
    else:
        return is_planar, _JGraphTGraph(handle=kuratowski_subdivision)


def boyer_myrvold(graph):
    """The Boyer-Myrvold planarity testing algorithm.

    :param graph: the graph
    :returns: a tuple whose first element is whether the graph is planar. The second is 
              either an embedding (:py:class:`.PlanarEmbedding`) or a Kuratowski subgraph.
    """
    return _planarity_alg("boyer_myrvold", graph)


def is_planar(graph):
    """The Boyer-Myrvold planarity testing algorithm.

    :param graph: the graph
    :returns: a tuple whose first element is whether the graph is planar. The second is 
              either an embedding (:py:class:`.PlanarEmbedding`) or a Kuratowski subgraph.
    """
    return boyer_myrvold(graph)
