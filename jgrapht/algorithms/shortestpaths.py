from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from ..graph import GraphPath


class SingleSourcePaths: 
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """
    def __init__(self, handle, source_vertex, owner=True):
        self._handle = handle
        self._owner = owner
        self._source_vertex = source_vertex

    @property
    def handle(self):
        return self._handle

    @property
    def source_vertex(self):
        """The source vertex"""
        return self._source_vertex

    def get_path(self, target_vertex):
        """Get a path to a target vertex.

        :param target_vertex: The target vertex.
        :returns: a path from the source to the target vertex.
        """
        err, gp = backend.jgrapht_sp_singlesource_get_path_to_vertex(self._handle, target_vertex)
        if err: 
            raise_status()
        return GraphPath(gp)

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle)
            if err: 
                raise_status() 


class AllPairsPaths: 
    """Wrapper class around the AllPairsPaths"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    @property
    def handle(self):
        return self._handle

    def get_path(self, source_vertex, target_vertex):
        err, gp = backend.jgrapht_sp_allpairs_get_path_between_vertices(self._handle, source_vertex, target_vertex)
        if err: 
            raise_status()
        return GraphPath(gp)

    def get_paths_from(self, source_vertex):
        err, singlesource = backend.jgrapht_sp_allpairs_get_singlesource_from_vertex(self._handle, source_vertex)
        if err: 
            raise_status()
        return SingleSourcePaths(singlesource, source_vertex)

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle)
            if err: 
                raise_status()



def _sp_singlesource_alg(name, graph, source_vertex):
    alg_method_name = 'jgrapht_sp_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, handle = alg_method(graph.handle, source_vertex)
    if err:
        raise_status()

    return SingleSourcePaths(handle, source_vertex)


def _sp_between_alg(name, graph, source_vertex, target_vertex):
    alg_method_name = 'jgrapht_sp_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, handle = alg_method(graph.handle, source_vertex, target_vertex)
    if err:
        raise_status()

    return GraphPath(handle)


def _sp_allpairs_alg(name, graph):
    alg_method_name = 'jgrapht_sp_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, handle = alg_method(graph.handle)
    if err:
        raise_status()

    return AllPairsPaths(handle)
    


def dijkstra(graph, source_vertex, target_vertex=None, use_bidirectional=True):
    """Dijkstra's algorithm to compute single-source shortest paths. 

    This implementation uses a pairing heap in order to order the edge relaxations.

    :param source_vertex: The source vertex.
    :param target_vertex: The target vertex. If None then shortest paths to all vertices are computed 
           and returns as an instance of `:py:class:.SingleSourcePaths`.
    :param use_bidirectional: Only valid if a target vertex is supplied. In this case the search is 
           bidirectional.
    :returns: Either a `:py:class.GraphPath` or `:py:class:.SingleSourcePaths`.
    """
    if target_vertex is None:
        return _sp_singlesource_alg('dijkstra_get_singlesource_from_vertex', graph, source_vertex)
    else:
        if use_bidirectional:
            return _sp_between_alg('bidirectional_dijkstra_get_path_between_vertices', graph, source_vertex, target_vertex)
        else:
            return _sp_between_alg('dijkstra_get_path_between_vertices', graph, source_vertex, target_vertex)

def bellman_ford(graph, source_vertex):
    return _sp_singlesource_alg('bellmanford_get_singlesource_from_vertex', graph, source_vertex)

def bfs(graph, source_vertex):
    return _sp_singlesource_alg('bfs_get_singlesource_from_vertex', graph, source_vertex)

def johnson_allpairs(graph):
    return _sp_allpairs_alg('johnson_get_allpairs', graph)
    
def floyd_warshall_allpairs(graph):
    return _sp_allpairs_alg('floydwarshall_get_allpairs', graph)    