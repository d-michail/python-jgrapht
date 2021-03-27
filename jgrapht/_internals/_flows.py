from .. import backend as _backend

from ..types import (
    Cut,
    Flow,
    GomoryHuTree,
    EquivalentFlowTree,
)

from ._wrappers import _HandleWrapper
from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTLongSet,
    _JGraphTIntegerDoubleMap,
    _JGraphTLongDoubleMap,
)
from ._anyhashableg import _is_anyhashable_graph
from ._anyhashableg_collections import _AnyHashableGraphVertexSet
from ._int_graphs import _JGraphTIntegerGraph
from ._long_graphs import _JGraphTLongGraph, _is_long_graph


class _JGraphTCut(Cut):
    """A graph cut."""

    def __init__(self, graph, capacity, source_partition_handle, **kwargs):
        super().__init__(**kwargs)
        self._graph = graph
        self._capacity = capacity
        if _is_anyhashable_graph(graph):
            self._source_partition = _AnyHashableGraphVertexSet(
                source_partition_handle, graph
            )
        elif _is_long_graph(graph):
            self._source_partition = _JGraphTLongSet(source_partition_handle)
        else:
            self._source_partition = _JGraphTIntegerSet(source_partition_handle)
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
        return "_JGraphTCut(%f, %r)" % (self.capacity, self.source_partition)

    def __str__(self):
        return str(self.edges)


class _JGraphTIntegerFlow(_JGraphTIntegerDoubleMap, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(self, handle, source, sink, value, **kwargs):
        self._source = source
        self._sink = sink
        self._value = value
        super().__init__(handle=handle, **kwargs)

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
        return "_JGraphTIntegerFlow(%r)" % self._handle


class _JGraphTLongFlow(_JGraphTLongDoubleMap, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(self, handle, source, sink, value, **kwargs):
        self._source = source
        self._sink = sink
        self._value = value
        super().__init__(handle=handle, **kwargs)

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
        return "_JGraphTLongFlow(%r)" % self._handle


class _JGraphTIntegerGomoryHuTree(_HandleWrapper, GomoryHuTree):
    """Gomory-Hu Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ii_cut_gomoryhu_tree(self.handle)
        return _JGraphTIntegerGraph(tree_handle)

    def min_cut(self):
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_xx_cut_gomoryhu_min_cut(self.handle)
        return _JGraphTCut(self._graph, cut_value, cut_source_partition_handle)

    def min_st_cut(self, s, t):
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_ix_cut_gomoryhu_min_st_cut(self.handle, s, t)
        return _JGraphTCut(self._graph, cut_value, cut_source_partition_handle)

    def __repr__(self):
        return "_JGraphTIntegerGomoryHuTree(%r)" % self._handle


class _JGraphTLongGomoryHuTree(_HandleWrapper, GomoryHuTree):
    """Gomory-Hu Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ll_cut_gomoryhu_tree(self.handle)
        return _JGraphTIntegerGraph(tree_handle)

    def min_cut(self):
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_xx_cut_gomoryhu_min_cut(self.handle)
        return _JGraphTCut(self._graph, cut_value, cut_source_partition_handle)

    def min_st_cut(self, s, t):
        (
            cut_value,
            cut_source_partition_handle,
        ) = _backend.jgrapht_lx_cut_gomoryhu_min_st_cut(self.handle, s, t)
        return _JGraphTCut(self._graph, cut_value, cut_source_partition_handle)

    def __repr__(self):
        return "_JGraphTLongGomoryHuTree(%r)" % self._handle


class _JGraphTIntegerEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ii_equivalentflowtree_tree(self.handle)
        return _JGraphTIntegerGraph(tree_handle)

    def max_st_flow_value(self, s, t):
        return _backend.jgrapht_ix_equivalentflowtree_max_st_flow(self.handle, s, t)

    def __repr__(self):
        return "_JGraphTIntegerEquivalentFlowTree(%r)" % self._handle


class _JGraphTLongEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ll_equivalentflowtree_tree(self.handle)
        return _JGraphTLongGraph(tree_handle)

    def max_st_flow_value(self, s, t):
        return _backend.jgrapht_lx_equivalentflowtree_max_st_flow(self.handle, s, t)

    def __repr__(self):
        return "_JGraphTLongEquivalentFlowTree(%r)" % self._handle