from .. import backend as _backend

from .._internals._mapping import (
    _JGraphTGraphMappingIterator,
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
    if graph1._backend_type != graph2._backend_type: 
        raise TypeError("Graphs must use the same backend")

    exists, map_it_handle = _backend.jgrapht_xx_isomorphism_exec_vf2(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None

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
    if graph1._backend_type != graph2._backend_type: 
        raise TypeError("Graphs must use the same backend")

    exists, map_it_handle = _backend.jgrapht_xx_isomorphism_exec_vf2_subgraph(
        graph1.handle, graph2.handle
    )
    if not exists:
        return None

    return _JGraphTGraphMappingIterator(
        handle=map_it_handle, graph1=graph1, graph2=graph2
    )
