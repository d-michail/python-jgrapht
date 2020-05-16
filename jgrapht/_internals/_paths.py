from .. import backend
from ..types import (
    GraphPath,
    SingleSourcePaths,
    AllPairsPaths,
)
from ._wrappers import (
    _HandleWrapper,
    _JGraphTIntegerIterator,
    _JGraphTObjectIterator,
)


class _JGraphTGraphPath(_HandleWrapper, GraphPath):
    """A class representing a graph path."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
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

    def __iter__(self):
        self._cache()
        return self._edges.__iter__()

    def _cache(self):
        if self._edges is not None:
            return

        (weight, start_vertex, end_vertex, eit,) = backend.jgrapht_graphpath_get_fields(
            self._handle
        )

        self._weight = weight
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self._edges = list(_JGraphTIntegerIterator(eit))

    def __repr__(self):
        return "_JGraphTGraphPath(%r)" % self._handle


class _JGraphTGraphPathIterator(_JGraphTObjectIterator):
    """A graph path iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTGraphPath(super().__next__())

    def __repr__(self):
        return "_JGraphTGraphPathIterator(%r)" % self._handle


class _JGraphTSingleSourcePaths(_HandleWrapper, SingleSourcePaths):
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """

    def __init__(self, handle, source_vertex, **kwargs):
        super().__init__(handle=handle, **kwargs)
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
        gp = backend.jgrapht_sp_singlesource_get_path_to_vertex(
            self._handle, target_vertex
        )
        return _JGraphTGraphPath(gp) if gp is not None else None

    def __repr__(self):
        return "_JGraphTSingleSourcePaths(%r)" % self._handle


class _JGraphTAllPairsPaths(_HandleWrapper, AllPairsPaths):
    """Wrapper class around the AllPairsPaths"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def get_path(self, source_vertex, target_vertex):
        gp = backend.jgrapht_sp_allpairs_get_path_between_vertices(
            self._handle, source_vertex, target_vertex
        )
        return _JGraphTGraphPath(gp) if gp is not None else None

    def get_paths_from(self, source_vertex):
        singlesource = backend.jgrapht_sp_allpairs_get_singlesource_from_vertex(
            self._handle, source_vertex
        )
        return _JGraphTSingleSourcePaths(singlesource, source_vertex)

    def __repr__(self):
        return "_JGraphTAllPairsPaths(%r)" % self._handle
