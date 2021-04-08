from .. import backend as _backend

from ..types import (
    Cut,
    Flow,
    GomoryHuTree,
    EquivalentFlowTree,
)

from . import _callbacks, _ref_hashequals
from ._wrappers import _HandleWrapper, GraphBackend
from ._collections_set import (
    _JGraphTIntegerSet,
    _JGraphTLongSet,
)
from ._collections_map import (
    _JGraphTIntegerDoubleMap,
    _JGraphTLongDoubleMap,
    _JGraphTRefDoubleMap,
)
from ._int_graphs import _JGraphTIntegerGraph
from ._long_graphs import _JGraphTLongGraph
from ._ref_graphs import _JGraphTRefGraph
from ._ref_results import _jgrapht_ref_set_to_python_set


class _JGraphTCut(Cut):
    """A graph cut."""

    def __init__(self, graph, capacity, source_partition_handle, **kwargs):
        super().__init__(**kwargs)
        self._graph = graph
        self._capacity = capacity

        if graph._backend_type == GraphBackend.LONG_GRAPH:
            self._source_partition = _JGraphTLongSet(source_partition_handle)
        elif graph._backend_type == GraphBackend.INT_GRAPH:
            self._source_partition = _JGraphTIntegerSet(source_partition_handle)
        elif graph._backend_type == GraphBackend.REF_GRAPH:
            self._source_partition = _jgrapht_ref_set_to_python_set(
                source_partition_handle
            )
        else:
            raise ValueError("Not recognized graph backend")

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


class _JGraphTRefFlow(_JGraphTRefDoubleMap, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(
        self, handle, hash_equals_resolver_handle, source, sink, value, **kwargs
    ):
        self._source = source
        self._sink = sink
        self._value = value
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

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
        return "_JGraphTRefFlow(%r)" % self._handle


class _JGraphTIntegerGomoryHuTree(_HandleWrapper, GomoryHuTree):
    """Gomory-Hu Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ii_cut_gomoryhu_tree(self.handle, 0, 0)
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
        tree_handle = _backend.jgrapht_ll_cut_gomoryhu_tree(self.handle, 0, 0)
        return _JGraphTLongGraph(tree_handle)

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


class _JGraphTRefGomoryHuTree(_HandleWrapper, GomoryHuTree):
    """Gomory-Hu Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        vertex_supplier_fptr_wrapper = self._graph._vertex_supplier_fptr_wrapper
        edge_supplier_fptr_wrapper = self._graph._edge_supplier_fptr_wrapper
        hash_equals_wrapper = self._graph._hash_equals_wrapper

        tree_handle = _backend.jgrapht_rr_cut_gomoryhu_tree(
            self.handle,
            vertex_supplier_fptr_wrapper.fptr,
            edge_supplier_fptr_wrapper.fptr,
            hash_equals_wrapper.handle,
        )

        return _JGraphTRefGraph(
            tree_handle,
            vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
            hash_equals_wrapper=hash_equals_wrapper,
        )

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
        ) = _backend.jgrapht_rx_cut_gomoryhu_min_st_cut(
            self.handle, id(s), id(t), self._graph._hash_equals_wrapper.handle
        )
        return _JGraphTCut(self._graph, cut_value, cut_source_partition_handle)

    def __repr__(self):
        return "_JGraphTRefGomoryHuTree(%r)" % self._handle


class _JGraphTIntegerEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        tree_handle = _backend.jgrapht_ii_equivalentflowtree_tree(self.handle, 0, 0)
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
        tree_handle = _backend.jgrapht_ll_equivalentflowtree_tree(self.handle, 0, 0)
        return _JGraphTLongGraph(tree_handle)

    def max_st_flow_value(self, s, t):
        return _backend.jgrapht_lx_equivalentflowtree_max_st_flow(self.handle, s, t)

    def __repr__(self):
        return "_JGraphTLongEquivalentFlowTree(%r)" % self._handle


class _JGraphTRefEquivalentFlowTree(_HandleWrapper, EquivalentFlowTree):
    """An Equivalent Flow Tree."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def as_graph(self):
        vertex_supplier_fptr_wrapper = self._graph._vertex_supplier_fptr_wrapper
        edge_supplier_fptr_wrapper = self._graph._edge_supplier_fptr_wrapper
        hash_equals_wrapper = self._graph._hash_equals_wrapper

        tree_handle = _backend.jgrapht_rr_equivalentflowtree_tree(
            self.handle,
            vertex_supplier_fptr_wrapper.fptr,
            edge_supplier_fptr_wrapper.fptr,
            hash_equals_wrapper.handle,
        )

        return _JGraphTRefGraph(
            tree_handle,
            vertex_supplier_fptr_wrapper=vertex_supplier_fptr_wrapper,
            edge_supplier_fptr_wrapper=edge_supplier_fptr_wrapper,
            hash_equals_wrapper=hash_equals_wrapper,
        )

    def max_st_flow_value(self, s, t):
        return _backend.jgrapht_rx_equivalentflowtree_max_st_flow(
            self.handle, id(s), id(t), self._graph._hash_equals_wrapper.handle
        )

    def __repr__(self):
        return "_JGraphTRefEquivalentFlowTree(%r)" % self._handle
