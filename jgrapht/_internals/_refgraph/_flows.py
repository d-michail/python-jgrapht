from ... import backend as _backend

from ...types import (
    Cut,
    Flow,
    GomoryHuTree,
    EquivalentFlowTree,
)

from .._wrappers import _HandleWrapper
from .._collections import (
    _JGraphTLongSet,
    _JGraphTLongDoubleMap,
)
from .._refgraph._graphs import _is_refcount_graph, _map_ids_to_objs, _id_to_obj


class _RefCountGraphCut(Cut):
    """A graph cut."""

    def __init__(self, graph, capacity, source_partition_handle, **kwargs):
        super().__init__(**kwargs)
        self._graph = graph
        self._capacity = capacity
        self._source_partition = set(_map_ids_to_objs(_JGraphTLongSet(handle=source_partition_handle)))
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
        return "_RefCountGraphCut(%f, %r)" % (self.capacity, self.source_partition)

    def __str__(self):
        return str(self.edges)


class _RefCountGraphFlow(dict, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(self, handle, source, sink, value, **kwargs):
        super().__init__(**kwargs)
        self._source = source
        self._sink = sink
        self._value = value

        # Note: we take ownership of handle here
        for eid, f_value in _JGraphTLongDoubleMap(handle=handle).items():
            self[_id_to_obj(eid)] = f_value

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
        return "_RefCountGraphFlow(%r)" % self._handle


