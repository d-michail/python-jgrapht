from ... import backend as _backend
from ...types import Cut, Flow, GomoryHuTree, EquivalentFlowTree
from ..._internals._wrappers import _HandleWrapper
from .._intgraph._int_graphs import _JGraphTIntegerGraph

from ._graphs import (
    _create_anyhashable_graph,
    _vertex_anyhashableg_to_g,
    _vertex_g_to_anyhashableg,
)

from ._collections import _AnyHashableGraphEdgeDoubleMap, _AnyHashableGraphVertexSet


class _AnyHashableGraphCut(Cut):
    """A graph cut."""

    def __init__(self, graph, capacity, source_partition_handle, **kwargs):
        super().__init__(**kwargs)
        self._graph = graph
        self._capacity = capacity
        self._source_partition = _AnyHashableGraphVertexSet(
            source_partition_handle, graph
        )
        self._target_partition = None
        self._edges = None

    @property
    def weight(self):
        return self._capacity

    @property
    def capacity(self):
        return self._capacity

    @property
    def source_partition(self):
        """Source partition vertex set."""
        return self._source_partition

    @property
    def target_partition(self):
        """Target partition vertex set."""
        self._lazy_compute()
        return self._target_partition

    @property
    def edges(self):
        """Target partition vertex set."""
        self._lazy_compute()
        return self._edges

    def _lazy_compute(self):
        if self._edges is not None:
            return

        self._target_partition = set(self._graph.vertices).difference(
            self._source_partition
        )

        self._edges = set()
        if self._graph.type.directed:
            for v in self._source_partition:
                for e in self._graph.outedges_of(v):
                    if self._graph.edge_target(e) not in self._source_partition:
                        self._edges.add(e)
        else:
            for e in self._graph.edges:
                s_in_s = self._graph.edge_source(e) in self._source_partition
                t_in_s = self._graph.edge_target(e) in self._source_partition
                if s_in_s ^ t_in_s:
                    self._edges.add(e)

    def __repr__(self):
        return "_AnyHashableGraphCut(%f, %r)" % (self.capacity, self.source_partition)

    def __str__(self):
        return str(self.edges)


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
        tree_handle = _backend.jgrapht_ii_cut_gomoryhu_tree(self.handle)
        tree_as_graph = _JGraphTIntegerGraph(tree_handle)

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
        cut_value, cut_source_partition_handle = _backend.jgrapht_xx_cut_gomoryhu_min_cut(
            self.handle
        )
        return _AnyHashableGraphCut(self._graph, cut_value, cut_source_partition_handle)

    def min_st_cut(self, s, t):
        s = _vertex_anyhashableg_to_g(self._graph, s)
        t = _vertex_anyhashableg_to_g(self._graph, t)
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_ii_cut_gomoryhu_min_st_cut(self.handle, s, t)
        return _AnyHashableGraphCut(self._graph, cut_value, cut_source_partition_handle)

    def __repr__(self):
        return "_AnyHashableGraphGomoryHuTree(%r)" % self._handle


class _AnyHashableGraphEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ii_equivalentflowtree_tree(self.handle)
        tree_as_graph = _JGraphTIntegerGraph(tree_handle)

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
        return _backend.jgrapht_ii_equivalentflowtree_max_st_flow(self.handle, s, t)

    def __repr__(self):
        return "_AnyHashableGraphEquivalentFlowTree(%r)" % self._handle
