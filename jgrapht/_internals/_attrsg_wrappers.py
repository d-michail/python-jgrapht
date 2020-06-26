from .. import backend
from collections import namedtuple
from collections.abc import Iterator

from ._wrappers import _JGraphTIntegerIterator


class _AttributesGraphVertexIterator(_JGraphTIntegerIterator):
    """A vertex iterator for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        v = super().__next__()
        return self._graph._vertex_id_to_hash[v]

    def __repr__(self):
        return "_AttributesGraphVertexIterator(%r)" % self._handle


class _AttributesGraphEdgeIterator(_JGraphTIntegerIterator):
    """An edge iterator for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        e = super().__next__()
        return self._graph._edge_id_to_hash[e]

    def __repr__(self):
        return "_AttributesGraphEdgeIterator(%r)" % self._handle
