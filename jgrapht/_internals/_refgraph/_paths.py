from ... import backend

from ...types import (
    GraphPath,
    SingleSourcePaths,
    MultiObjectiveSingleSourcePaths,
    AllPairsPaths,
)

from .._wrappers import _HandleWrapper, _JGraphTObjectIterator, _JGraphTLongIterator
from ._graphs import _is_refcount_graph, _map_ids_to_objs, _id_to_obj


class _RefCountGraphGraphPath(_HandleWrapper, GraphPath):
    """A class representing a graph path."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph
        (
            weight,
            start_vertex,
            end_vertex,
            eit,
        ) = backend.jgrapht_ll_handles_get_graphpath(self._handle)
        self._weight = weight
        self._start_vertex = _id_to_obj(start_vertex)
        self._end_vertex = _id_to_obj(end_vertex)
        self._edges = list(_map_ids_to_objs(_JGraphTLongIterator(eit)))

    @property
    def weight(self):
        """The weight of the path."""
        return self._weight

    @property
    def start_vertex(self):
        """The starting vertex of the path."""
        return self._start_vertex

    @property
    def end_vertex(self):
        """The ending vertex of the path."""
        return self._end_vertex

    @property
    def edges(self):
        """A list of edges of the path."""
        return self._edges

    @property
    def graph(self):
        return self._graph

    def __iter__(self):
        return self._edges.__iter__()

    def __repr__(self):
        return "_RefCountGraphGraphPath(%r)" % self._handle


class _RefCountGraphGraphPathIterator(_JGraphTObjectIterator):
    """A graph path iterator"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _RefCountGraphGraphPath(super().__next__(), self._graph)

    def __repr__(self):
        return "_RefCountGraphGraphPathIterator(%r)" % self._handle


class _RefCountGraphSingleSourcePaths(_HandleWrapper, SingleSourcePaths):
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
        gp = backend.jgrapht_ll_sp_singlesource_get_path_to_vertex(
            self._handle, id(target_vertex)
        )
        return _RefCountGraphGraphPath(gp, self._graph) if gp is not None else None

    def __repr__(self):
        return "_RefCountGraphSingleSourcePaths(%r)" % self._handle


class _RefCountGraphAllPairsPaths(_HandleWrapper, AllPairsPaths):
    """Wrapper class around the AllPairsPaths"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_path(self, source_vertex, target_vertex):
        gp = backend.jgrapht_ll_sp_allpairs_get_path_between_vertices(
            self._handle, id(source_vertex), id(target_vertex)
        )
        return _RefCountGraphGraphPath(gp, self._graph) if gp is not None else None

    def get_paths_from(self, source_vertex):
        singlesource = backend.jgrapht_ll_sp_allpairs_get_singlesource_from_vertex(
            self._handle, id(source_vertex)
        )
        return _RefCountGraphSingleSourcePaths(
            singlesource, self._graph, source_vertex
        )

    def __repr__(self):
        return "_RefCountGraphAllPairsPaths(%r)" % self._handle


class _RefCountGraphMultiObjectiveSingleSourcePaths(
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
        gp_it = (
            backend.jgrapht_ll_multisp_multiobjectivesinglesource_get_paths_to_vertex(
                self._handle, id(target_vertex)
            )
        )
        return _RefCountGraphGraphPathIterator(handle=gp_it, graph=self._graph)

    def __repr__(self):
        return "_RefCountGraphMultiObjectiveSingleSourcePaths(%r)" % self._handle


class _RefCountGraphContractionHierarchiesManyToMany(_HandleWrapper):
    """Many to many result with contraction hierarchies"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_path(self, source_vertex, target_vertex):
        gp = backend.jgrapht_ll_sp_manytomany_get_path_between_vertices(
            self._handle, id(source_vertex), id(target_vertex)
        )
        return _RefCountGraphGraphPath(gp, self._graph) if gp is not None else None

    def __repr__(self):
        return "_RefCountGraphContractionHierarchiesManyToMany(%r)" % self._handle
