from .. import backend as _backend

from .._internals._intgraph._int_graphs import _is_int_graph
from .._internals._intgraph._mapping import (
    _JGraphTLongGraphMappingIterator,
    _JGraphTIntegerGraphMappingIterator,
)
from .._internals._intgraph._long_graphs import _is_long_graph
from .._internals._refgraph._graphs import _is_refcount_graph
from .._internals._refgraph._mapping import _RefCountGraphGraphMappingIterator


def _wrap_result(graph1, graph2, map_it_handle):
    if _is_refcount_graph(graph1) and _is_refcount_graph(graph2):
        return _RefCountGraphGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
    elif _is_long_graph(graph1) and _is_long_graph(graph2):
        return _JGraphTLongGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
    elif _is_int_graph(graph1) and _is_int_graph(graph2):
        return _JGraphTIntegerGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
    else:
        raise TypeError("Isomorphism can only be tested against same backend graphs")


def vf2(graph1, graph2):
    r"""The VF2 algorithm for detection of isomorphism between two graphs.

      * Cordella et al. A (sub)graph isomorphism algorithm for matching large graphs
        (2004), DOI:10.1109/TPAMI.2004.75

    This implementation of the VF2 algorithm does not support graphs with multiple-edges.

    .. note :: Graph mappings are represented using :py:class:`.GraphMapping` instances

    :param graph1: the first graph
    :param graph2: the second graph
    :returns: an iterator over graph mappings if the graphs are isomorphic, otherwise None
    """
    exists, map_it_handle = _backend.jgrapht_xx_isomorphism_exec_vf2(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None
    return _wrap_result(graph1, graph2, map_it_handle)


def vf2_subgraph(graph1, graph2):
    r"""The VF2 algorithm for detection of subgraph isomorphism between two graphs.

      * Cordella et al. A (sub)graph isomorphism algorithm for matching large graphs
        (2004), DOI:10.1109/TPAMI.2004.75

    This implementation of the VF2 algorithm does not support graphs with multiple-edges.

    .. note :: Graph mappings are represented using :py:class:`.GraphMapping` instances

    .. warning :: This algorithm only finds isomorphisms between a smaller graph and all
      `induced subgraphs <http://mathworld.wolfram.com/Vertex-InducedSubgraph.html>`_ of a
      larger graph. It does **not** find isomorphisms between the smaller graph and arbitrary
      subgraphs of the larger graph.

    :param graph1: the first graph
    :param graph2: the second graph
    :returns: an iterator over graph mappings if the graphs are isomorphic, otherwise None
    """
    exists, map_it_handle = _backend.jgrapht_xx_isomorphism_exec_vf2_subgraph(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None
    return _wrap_result(graph1, graph2, map_it_handle)
