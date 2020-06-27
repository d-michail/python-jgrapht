from .. import backend

from ..types import (
    GraphPath,
    SingleSourcePaths,
    MultiObjectiveSingleSourcePaths,
    AllPairsPaths,
)

from ._wrappers import _HandleWrapper, _JGraphTObjectIterator

from ._anyhashableg import _vertex_anyhashableg_to_g
from ._anyhashableg_wrappers import _AnyHashableGraphEdgeIterator


class _AnyHashableGraphGraphPath(_HandleWrapper, GraphPath):
    """A class representing a graph path."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph
        self._weight = None
        self._start_vertex = None
        self._end_vertex = None
        self._edges = None

    @property
    def weight(self):
        """The weight of the path."""
        self._cache()
        return self._weight

    @property
    def start_vertex(self):
        """The starting vertex of the path."""
        self._cache()
        return self._start_vertex

    @property
    def end_vertex(self):
        """The ending vertex of the path."""
        self._cache()
        return self._end_vertex

    @property
    def edges(self):
        """A list of edges of the path."""
        self._cache()
        return self._edges

    @property
    def graph(self):
        return self._graph

    def __iter__(self):
        self._cache()
        return self._edges.__iter__()

    def _cache(self):
        if self._edges is not None:
            return

        weight, start_vertex, end_vertex, eit = backend.jgrapht_handles_get_graphpath(
            self._handle
        )

        self._weight = weight
        self._start_vertex = self._graph._vertex_id_to_hash[start_vertex]
        self._end_vertex = self._graph._vertex_id_to_hash[end_vertex]
        self._edges = list(_AnyHashableGraphEdgeIterator(eit, self._graph))

    def __repr__(self):
        return "_AnyHashableGraphGraphPath(%r)" % self._handle


class _AnyHashableGraphGraphPathIterator(_JGraphTObjectIterator):
    """A graph path iterator"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _AnyHashableGraphGraphPath(super().__next__(), self._graph)

    def __repr__(self):
        return "_AnyHashableGraphGraphPathIterator(%r)" % self._handle


class _AnyHashableGraphSingleSourcePaths(_HandleWrapper, SingleSourcePaths):
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """

    def __init__(self, handle, graph, source_vertex, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph
        self._source_vertex = source_vertex

    @property
    def source_vertex(self):
        """The source vertex"""
        return self._source_vertex

    def get_path(self, target_vertex):
        """Get a path to a target vertex.

        :param target_vertex: The target vertex.
        :returns: a path from the source to the target vertex.
        """
        target_vertex = _vertex_anyhashableg_to_g(self._graph, target_vertex)
        gp = backend.jgrapht_sp_singlesource_get_path_to_vertex(
            self._handle, target_vertex
        )
        return _AnyHashableGraphGraphPath(gp, self._graph) if gp is not None else None

    def __repr__(self):
        return "_AnyHashableGraphSingleSourcePaths(%r)" % self._handle


class _AnyHashableGraphAllPairsPaths(_HandleWrapper, AllPairsPaths):
    """Wrapper class around the AllPairsPaths"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_path(self, source_vertex, target_vertex):
        source_vertex = _vertex_anyhashableg_to_g(self._graph, source_vertex)
        target_vertex = _vertex_anyhashableg_to_g(self._graph, target_vertex)

        gp = backend.jgrapht_sp_allpairs_get_path_between_vertices(
            self._handle, source_vertex, target_vertex
        )
        return _AnyHashableGraphGraphPath(gp, self._graph) if gp is not None else None

    def get_paths_from(self, source_vertex):
        source_vertex = _vertex_anyhashableg_to_g(self._graph, source_vertex)
        singlesource = backend.jgrapht_sp_allpairs_get_singlesource_from_vertex(
            self._handle, source_vertex
        )
        return _AnyHashableGraphSingleSourcePaths(
            singlesource, self._graph, source_vertex
        )

    def __repr__(self):
        return "_AnyHashableGraphAllPairsPaths(%r)" % self._handle


class _AnyHashableGraphMultiObjectiveSingleSourcePaths(
    _HandleWrapper, MultiObjectiveSingleSourcePaths
):
    """A set of paths starting from a single source vertex. This is the 
    multi objective case, where for each target vertex we might have a set of paths.
    """

    def __init__(self, handle, graph, source_vertex, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph
        self._source_vertex = source_vertex

    @property
    def source_vertex(self):
        """The source vertex"""
        return self._source_vertex

    def get_paths(self, target_vertex):
        target_vertex = _vertex_anyhashableg_to_g(self._graph, target_vertex)
        gp_it = backend.jgrapht_multisp_multiobjectivesinglesource_get_paths_to_vertex(
            self._handle, target_vertex
        )
        return _AnyHashableGraphGraphPathIterator(handle=gp_it, graph=self._graph)

    def __repr__(self):
        return "_AnyHashableGraphMultiObjectiveSingleSourcePaths(%r)" % self._handle
