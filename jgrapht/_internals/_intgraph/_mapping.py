from jgrapht import backend
from jgrapht.types import GraphMapping
from jgrapht._internals._wrappers import (
    _HandleWrapper,
    _JGraphTObjectIterator,
)


class _JGraphTIntegerGraphMapping(_HandleWrapper, GraphMapping):
    """A JGraphT mapping between two graphs g1 and g2."""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def vertex_correspondence(self, vertex, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_ii_isomorphism_graph_mapping_vertex_correspondence(
            self._handle, vertex, forward
        )
        return other if exists else None

    def edge_correspondence(self, edge, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_ii_isomorphism_graph_mapping_edge_correspondence(
            self._handle, edge, forward
        )
        return other if exists else None

    def vertices_correspondence(self, forward=True):
        vertices = self._graph1.vertices if forward else self._graph2.vertices
        result = dict()
        for v in vertices:
            result[v] = self.vertex_correspondence(v, forward=forward)
        return result

    def edges_correspondence(self, forward=True):
        edges = self._graph1.edges if forward else self._graph2.edges
        result = dict()
        for e in edges:
            result[e] = self.edge_correspondence(e, forward=forward)
        return result

    def __repr__(self):
        return "_JGraphTIntegerGraphMapping(%r)" % self._handle


class _JGraphTIntegerGraphMappingIterator(_JGraphTObjectIterator):
    """A graph mapping iterator"""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def __next__(self):
        return _JGraphTIntegerGraphMapping(super().__next__(), self._graph1, self._graph2)

    def __repr__(self):
        return "_JGraphTIntegerGraphMappingIterator(%r)" % self._handle


class _JGraphTLongGraphMapping(_HandleWrapper, GraphMapping):
    """A JGraphT mapping between two graphs g1 and g2."""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def vertex_correspondence(self, vertex, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_ll_isomorphism_graph_mapping_vertex_correspondence(
            self._handle, vertex, forward
        )
        return other if exists else None

    def edge_correspondence(self, edge, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_ll_isomorphism_graph_mapping_edge_correspondence(
            self._handle, edge, forward
        )
        return other if exists else None

    def vertices_correspondence(self, forward=True):
        vertices = self._graph1.vertices if forward else self._graph2.vertices
        result = dict()
        for v in vertices:
            result[v] = self.vertex_correspondence(v, forward=forward)
        return result

    def edges_correspondence(self, forward=True):
        edges = self._graph1.edges if forward else self._graph2.edges
        result = dict()
        for e in edges:
            result[e] = self.edge_correspondence(e, forward=forward)
        return result

    def __repr__(self):
        return "_JGraphTLongGraphMapping(%r)" % self._handle


class _JGraphTLongGraphMappingIterator(_JGraphTObjectIterator):
    """A graph mapping iterator"""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def __next__(self):
        return _JGraphTLongGraphMapping(super().__next__(), self._graph1, self._graph2)

    def __repr__(self):
        return "_JGraphTLongGraphMappingIterator(%r)" % self._handle
