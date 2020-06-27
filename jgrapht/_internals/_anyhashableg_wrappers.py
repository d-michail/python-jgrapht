from ._wrappers import _JGraphTIntegerIterator


class _AnyHashableGraphVertexIterator(_JGraphTIntegerIterator):
    """A vertex iterator."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        v = super().__next__()
        return self._graph._vertex_id_to_hash[v]

    def __repr__(self):
        return "_AnyHashableGraphVertexIterator(%r)" % self._handle


class _AnyHashableGraphEdgeIterator(_JGraphTIntegerIterator):
    """An edge iterator."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        e = super().__next__()
        return self._graph._edge_id_to_hash[e]

    def __repr__(self):
        return "_AnyHashableGraphEdgeIterator(%r)" % self._handle
