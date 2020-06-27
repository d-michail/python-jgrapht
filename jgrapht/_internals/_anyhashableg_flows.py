from .. import backend as _backend

from ..types import Flow, GomoryHuTree, EquivalentFlowTree

from ._wrappers import _HandleWrapper

from ._graphs import _JGraphTGraph
from ._anyhashableg import (
    _create_anyhashable_graph,
    _vertex_anyhashableg_to_g,
    _vertex_g_to_anyhashableg,
)
from ._anyhashableg_collections import _AnyHashableGraphEdgeDoubleMap

from ._flows import _JGraphTCut as _AnyHashableGraphCut


class _AnyHashableGraphFlow(_AnyHashableGraphEdgeDoubleMap, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(self, graph, handle, source, sink, value, **kwargs):
        self._source = source
        self._sink = sink
        self._value = value
        super().__init__(handle=handle, graph=graph, **kwargs)

    @property
    def source(self):
        """Source vertex in flow network."""
        return self._source

    @property
    def sink(self):
        """Sink vertex in flow network."""
        return self._sink

    @property
    def value(self):
        """Flow value."""
        return self._value

    def __repr__(self):
        return "_AnyHashableGraphFlow(%r)" % self._handle


class _AnyHashableGraphGomoryHuTree(_HandleWrapper, GomoryHuTree):
    """Gomory-Hu Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_cut_gomoryhu_tree(self.handle)
        tree_as_graph = _JGraphTGraph(tree_handle)

        # The resulting tree has the same vertices as the original graph. When using
        # any-hashable graphs, we have to explicitly copy here, to keep the same effect.
        res = _create_anyhashable_graph(
            directed=tree_as_graph.type.directed,
            allowing_self_loops=tree_as_graph.type.allowing_self_loops,
            allowing_multiple_edges=tree_as_graph.type.allowing_multiple_edges,
            weighted=tree_as_graph.type.weighted,
            vertex_supplier=self._graph.vertex_supplier,
            edge_supplier=self._graph.edge_supplier,
        )

        vertex_map = {}
        for vid in tree_as_graph.vertices:
            v = _vertex_g_to_anyhashableg(self._graph, vid)
            res.add_vertex(vertex=v)
            vertex_map[vid] = v

        for e in tree_as_graph.edges:
            s, t, w = tree_as_graph.edge_tuple(e)
            res.add_edge(vertex_map[s], vertex_map[t], weight=w)

        return res

    def min_cut(self):
        cut_value, cut_source_partition_handle = _backend.jgrapht_cut_gomoryhu_min_cut(
            self.handle
        )
        return _AnyHashableGraphCut(self._graph, cut_value, cut_source_partition_handle)

    def min_st_cut(self, s, t):
        s = _vertex_anyhashableg_to_g(self._graph, s)
        t = _vertex_anyhashableg_to_g(self._graph, t)
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_cut_gomoryhu_min_st_cut(self.handle, s, t)
        return _AnyHashableGraphCut(self._graph, cut_value, cut_source_partition_handle)

    def __repr__(self):
        return "_AnyHashableGraphGomoryHuTree(%r)" % self._handle


class _AnyHashableGraphEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_equivalentflowtree_tree(self.handle)
        tree_as_graph = _JGraphTGraph(tree_handle)

        # The resulting tree has the same vertices as the original graph. When using
        # any-hashable graphs, we have to explicitly copy here, to keep the same effect.
        res = _create_anyhashable_graph(
            directed=tree_as_graph.type.directed,
            allowing_self_loops=tree_as_graph.type.allowing_self_loops,
            allowing_multiple_edges=tree_as_graph.type.allowing_multiple_edges,
            weighted=tree_as_graph.type.weighted,
            vertex_supplier=self._graph.vertex_supplier,
            edge_supplier=self._graph.edge_supplier,
        )

        vertex_map = {}
        for vid in tree_as_graph.vertices:
            v = _vertex_g_to_anyhashableg(self._graph, vid)
            res.add_vertex(vertex=v)
            vertex_map[vid] = v

        for e in tree_as_graph.edges:
            s, t, w = tree_as_graph.edge_tuple(e)
            res.add_edge(vertex_map[s], vertex_map[t], weight=w)

        return res

    def max_st_flow_value(self, s, t):
        s = _vertex_anyhashableg_to_g(self._graph, s)
        t = _vertex_anyhashableg_to_g(self._graph, t)
        return _backend.jgrapht_equivalentflowtree_max_st_flow(self.handle, s, t)

    def __repr__(self):
        return "_AnyHashableGraphEquivalentFlowTree(%r)" % self._handle
