from .. import backend as _backend

from .._internals._intgraph._planar import (
    _JGraphTIntegerPlanarEmbedding,
    _JGraphTLongPlanarEmbedding,
)
from .._internals._intgraph._int_graphs import _JGraphTIntegerGraph
from .._internals._intgraph._long_graphs import _JGraphTLongGraph, _is_long_graph
from .._internals._refgraph._graphs import _is_refcount_graph, _RefCountGraph, _inc_ref
from .._internals._refgraph._planar import _RefCountGraphPlanarEmbedding


def _planarity_alg(name, graph, *args):
    alg_method_name = "jgrapht_xx_planarity_exec_"
    alg_method_name += name

    alg_method = getattr(_backend, alg_method_name)
    is_planar, embedding, kuratowski_subdivision = alg_method(graph.handle, *args)

    if is_planar:
        if _is_refcount_graph(graph):
            return is_planar, _RefCountGraphPlanarEmbedding(embedding, graph)
        elif _is_long_graph(graph):
            return is_planar, _JGraphTLongPlanarEmbedding(embedding)
        else:
            return is_planar, _JGraphTIntegerPlanarEmbedding(embedding)
    else:
        if _is_refcount_graph(graph):
            res = _RefCountGraph(
                handle=kuratowski_subdivision,
                vertex_supplier_fptr_and_cb=None,
                edge_supplier_fptr_and_cb=None,
                with_attributes=False,
            )
            # Need to increment refcounts since the graph was created in the backend
            for v in res.vertices:
                _inc_ref(v)
            for e in res.edges:
                _inc_ref(e)
            return is_planar, res
        elif _is_long_graph(graph):
            return is_planar, _JGraphTLongGraph(
                handle=kuratowski_subdivision, with_attributes=False
            )
        else:
            return is_planar, _JGraphTIntegerGraph(
                handle=kuratowski_subdivision, with_attributes=False
            )


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
