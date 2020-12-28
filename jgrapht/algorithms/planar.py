from .. import backend as _backend

from jgrapht._internals._intgraph._planar import (
    _JGraphTIntegerPlanarEmbedding,
    _JGraphTLongPlanarEmbedding,
)
from jgrapht._internals._intgraph._int_graphs import _JGraphTIntegerGraph
from jgrapht._internals._intgraph._long_graphs import _JGraphTLongGraph, _is_long_graph

from jgrapht._internals._mapgraph._graphs import (
    _is_anyhashable_graph,
    _create_anyhashable_graph_subgraph,
)
from jgrapht._internals._mapgraph._planar import _AnyHashableGraphPlanarEmbedding


def _planarity_alg(name, graph, *args):
    alg_method_name = "jgrapht_xx_planarity_exec_"
    alg_method_name += name

    alg_method = getattr(_backend, alg_method_name)
    is_planar, embedding, kuratowski_subdivision = alg_method(graph.handle, *args)

    if is_planar:
        if _is_anyhashable_graph(graph):
            return is_planar, _AnyHashableGraphPlanarEmbedding(embedding, graph)
        elif _is_long_graph(graph):
            return is_planar, _JGraphTLongPlanarEmbedding(embedding)
        else:
            return is_planar, _JGraphTIntegerPlanarEmbedding(embedding)
    else:
        if _is_anyhashable_graph(graph):
            kuratowski_as_graph = _JGraphTIntegerGraph(handle=kuratowski_subdivision)
            return (
                is_planar,
                _create_anyhashable_graph_subgraph(graph, kuratowski_as_graph),
            )
        elif _is_long_graph(graph):
            return is_planar, _JGraphTLongGraph(handle=kuratowski_subdivision)
        else:
            return is_planar, _JGraphTIntegerGraph(handle=kuratowski_subdivision)


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
