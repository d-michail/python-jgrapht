from .. import backend

from ..types import GraphMapping

from ._wrappers import (
    _HandleWrapper,
    _JGraphTObjectIterator,
)

from ._pg import vertex_pg_to_g as _vertex_pg_to_g, vertex_g_to_pg as _vertex_g_to_pg
from ._pg import edge_pg_to_g as _edge_pg_to_g, edge_g_to_pg as _edge_g_to_pg


class _PropertyGraphGraphMapping(_HandleWrapper, GraphMapping):
    """A mapping between two graphs g1 and g2."""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def vertex_correspondence(self, vertex, forward=True):
        if forward:
            vertex = _vertex_pg_to_g(self._graph1, vertex)
        else:
            vertex = _vertex_pg_to_g(self._graph2, vertex)
        (
            exists,
            other,
        ) = backend.jgrapht_isomorphism_graph_mapping_vertex_correspondence(
            self._handle, vertex, forward
        )
        if not exists:
            return None

        if forward:
            return _vertex_g_to_pg(self._graph2, other)
        else:
            return _vertex_g_to_pg(self._graph1, other)

    def edge_correspondence(self, edge, forward=True):
        if forward:
            edge = _edge_pg_to_g(self._graph1, edge)
        else:
            edge = _edge_pg_to_g(self._graph2, edge)
        (
            exists,
            other,
        ) = backend.jgrapht_isomorphism_graph_mapping_edge_correspondence(
            self._handle, edge, forward
        )
        if not exists:
            return None

        if forward:
            return _edge_g_to_pg(self._graph2, other)
        else:
            return _edge_g_to_pg(self._graph1, other)

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
        return "_PropertyGraphGraphMapping(%r)" % self._handle


class _PropertyGraphMappingIterator(_JGraphTObjectIterator):
    """A graph mapping iterator"""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def __next__(self):
        item = super().__next__()
        return _PropertyGraphGraphMapping(item, self._graph1, self._graph2)

    def __repr__(self):
        return "_PropertyGraphMappingIterator(%r)" % self._handle
