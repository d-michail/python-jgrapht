from .. import backend as _backend

from .._internals._planar import _JGraphTPlanarEmbedding
from .._internals._graphs import _JGraphTGraph

from .._internals._pg import (
    is_property_graph,
    _create_property_graph_subgraph,
)
from .._internals._pg_planar import _PropertyGraphPlanarEmbedding


def _planarity_alg(name, graph, *args):
    alg_method_name = "jgrapht_planarity_exec_"
    alg_method_name += name

    alg_method = getattr(_backend, alg_method_name)
    is_planar, embedding, kuratowski_subdivision = alg_method(graph.handle, *args)

    if is_planar:
        if is_property_graph(graph):
            return is_planar, _PropertyGraphPlanarEmbedding(embedding, graph)
        else:
            return is_planar, _JGraphTPlanarEmbedding(embedding)
    else:
        kuratowski_as_graph = _JGraphTGraph(handle=kuratowski_subdivision)
        if is_property_graph(graph):
            return is_planar, _create_property_graph_subgraph(graph, kuratowski_as_graph)
        else:
            return is_planar, kuratowski_as_graph


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
