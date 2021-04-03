from .. import backend
from ..types import (
    GraphPath,
    SingleSourcePaths,
    MultiObjectiveSingleSourcePaths,
    AllPairsPaths,
    ManyToManyPaths,
)
from ._wrappers import (
    GraphBackend,
    _HandleWrapper,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
    _JGraphTObjectIterator,
    _JGraphTRefIterator,
)
from ._int_graphs import _is_int_graph
from ._long_graphs import _is_long_graph
from ._ref_graphs import _is_ref_graph
from . import _ref_utils


class _JGraphTGraphPath(_HandleWrapper, GraphPath):
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

        if self._graph._backend_type == GraphBackend.INT_GRAPH:
            (
                weight,
                start_vertex,
                end_vertex,
                eit,
            ) = backend.jgrapht_ix_handles_get_graphpath(self._handle)
            self._edges = list(_JGraphTIntegerIterator(eit))
        elif self._graph._backend_type == GraphBackend.LONG_GRAPH:
            (
                weight,
                start_vertex,
                end_vertex,
                eit,
            ) = backend.jgrapht_lx_handles_get_graphpath(self._handle)
            self._edges = list(_JGraphTLongIterator(eit))
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            (
                weight,
                start_vertex_ptr,
                end_vertex_ptr,
                eit,
            ) = backend.jgrapht_rr_handles_get_graphpath(self._handle)
            start_vertex = _ref_utils._swig_ptr_to_obj(start_vertex_ptr)
            end_vertex = _ref_utils._swig_ptr_to_obj(end_vertex_ptr)
            self._edges = list(_JGraphTRefIterator(eit))
        else:
            raise TypeError("Not supported graph type")

        self._weight = weight
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex

    def __repr__(self):
        return "_JGraphTGraphPath(%r)" % self._handle


class _JGraphTGraphPathIterator(_JGraphTObjectIterator):
    """A graph path iterator"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _JGraphTGraphPath(super().__next__(), self._graph)

    def __repr__(self):
        return "_JGraphTGraphPathIterator(%r)" % self._handle


class _JGraphTSingleSourcePaths(_HandleWrapper, SingleSourcePaths):
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
        if self._graph._backend_type == GraphBackend.LONG_GRAPH:
            gp = backend.jgrapht_lx_sp_singlesource_get_path_to_vertex(
                self._handle, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.INT_GRAPH:
            gp = backend.jgrapht_ix_sp_singlesource_get_path_to_vertex(
                self._handle, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            gp = backend.jgrapht_rx_sp_singlesource_get_path_to_vertex(
                self._handle, id(target_vertex)
            )
        else:
            raise TypeError("Not supported graph type")
        return _JGraphTGraphPath(gp, self._graph) if gp is not None else None

    def __repr__(self):
        return "_JGraphTSingleSourcePaths(%r)" % self._handle


class _JGraphTAllPairsPaths(_HandleWrapper, AllPairsPaths):
    """Wrapper class around the AllPairsPaths"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_path(self, source_vertex, target_vertex):
        if self._graph._backend_type == GraphBackend.LONG_GRAPH:
            gp = backend.jgrapht_lx_sp_allpairs_get_path_between_vertices(
                self._handle, source_vertex, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.INT_GRAPH:
            gp = backend.jgrapht_ix_sp_allpairs_get_path_between_vertices(
                self._handle, source_vertex, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            gp = backend.jgrapht_rx_sp_allpairs_get_path_between_vertices(
                self._handle, id(source_vertex), id(target_vertex)
            )
        else:
            raise TypeError("Not supported graph type")
        return _JGraphTGraphPath(gp, self._graph) if gp is not None else None

    def get_paths_from(self, source_vertex):
        if self._graph._backend_type == GraphBackend.LONG_GRAPH:
            singlesource = backend.jgrapht_lx_sp_allpairs_get_singlesource_from_vertex(
                self._handle, source_vertex
            )
        elif self._graph._backend_type == GraphBackend.INT_GRAPH:
            singlesource = backend.jgrapht_ix_sp_allpairs_get_singlesource_from_vertex(
                self._handle, source_vertex
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            singlesource = backend.jgrapht_rx_sp_allpairs_get_singlesource_from_vertex(
                self._handle, id(source_vertex)
            )            
        else:
            raise TypeError("Not supported graph type")
        return _JGraphTSingleSourcePaths(singlesource, self._graph, source_vertex)

    def __repr__(self):
        return "_JGraphTAllPairsPaths(%r)" % self._handle


class _JGraphTMultiObjectiveSingleSourcePaths(
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
        if self._graph._backend_type == GraphBackend.LONG_GRAPH:
            gp_it = backend.jgrapht_lx_multisp_multiobjectivesinglesource_get_paths_to_vertex(
                self._handle, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.INT_GRAPH:
            gp_it = backend.jgrapht_ix_multisp_multiobjectivesinglesource_get_paths_to_vertex(
                self._handle, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            gp_it = backend.jgrapht_rx_multisp_multiobjectivesinglesource_get_paths_to_vertex(
                self._handle, id(target_vertex)
            )            
        else:
            raise TypeError("Not supported graph type")
        return _JGraphTGraphPathIterator(handle=gp_it, graph=self._graph)

    def __repr__(self):
        return "_JGraphTMultiObjectiveSingleSourcePaths(%r)" % self._handle


class _JGraphTContractionHierarchies(_HandleWrapper):
    """Wrapper class around contraction hierarchies"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __repr__(self):
        return "_JGraphTContractionHierarchies(%r)" % self._handle


class _JGraphTContractionHierarchiesManyToMany(_HandleWrapper, ManyToManyPaths):
    """Many to many result with contraction hierarchies"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def get_path(self, source_vertex, target_vertex):
        if self._graph._backend_type == GraphBackend.LONG_GRAPH:
            gp = backend.jgrapht_lx_sp_manytomany_get_path_between_vertices(
                self._handle, source_vertex, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.INT_GRAPH:
            gp = backend.jgrapht_ix_sp_manytomany_get_path_between_vertices(
                self._handle, source_vertex, target_vertex
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            gp = backend.jgrapht_rx_sp_manytomany_get_path_between_vertices(
                self._handle, id(source_vertex), id(target_vertex)
            )   
        else:
            raise TypeError("Not supported graph type")
        return _JGraphTGraphPath(gp, self._graph) if gp is not None else None

    def __repr__(self):
        return "_JGraphTContractionHierarchiesManyToMany(%r)" % self._handle
