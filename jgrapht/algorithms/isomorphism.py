from .. import backend as _backend

from .._internals._mapping import _JGraphTGraphMapping, _JGraphTGraphMappingIterator

from .._internals._anyhashableg import _is_anyhashable_graph
from .._internals._anyhashableg_mapping import (
    _AnyHashableGraphGraphMapping,
    _AnyHashableGraphMappingIterator,
)


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
    exists, map_it_handle = _backend.jgrapht_isomorphism_exec_vf2(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None

    if _is_anyhashable_graph(graph1) or _is_anyhashable_graph(graph2):
        return _AnyHashableGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
    else:
        return _JGraphTGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )


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
    exists, map_it_handle = _backend.jgrapht_isomorphism_exec_vf2_subgraph(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None

    if _is_anyhashable_graph(graph1) or _is_anyhashable_graph(graph2):
        return _AnyHashableGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
    else:
        return _JGraphTGraphMappingIterator(
            handle=map_it_handle, graph1=graph1, graph2=graph2
        )
