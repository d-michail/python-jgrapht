from . import backend
from .types import GraphType, GraphPath, SingleSourcePaths, AllPairsPaths, Graph
from ._errors import raise_status
from collections.abc import Iterator, MutableSet


class HandleWrapper:
    """A handle wrapper"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle)
            if err: 
                raise_status() 


class JGraphTLongIterator(HandleWrapper, Iterator): 
    """Long values iterator"""
    def __init__(self, handle, owner=True):
        super().__init__(handle, owner)

    def __next__(self):
        err, res = backend.jgrapht_it_hasnext(self._handle)
        if err: 
            raise_status()
        if not res: 
            raise StopIteration()
        err, res = backend.jgrapht_it_next_long(self._handle)
        if err: 
            raise_status()
        return res


class JGraphTDoubleIterator(HandleWrapper, Iterator): 
    """Double values iterator"""
    def __init__(self, handle, owner=True):
        super().__init__(handle, owner)

    def __next__(self):
        err, res = backend.jgrapht_it_hasnext(self._handle)
        if err: 
            raise_status()
        if not res: 
            raise StopIteration()
        err, res = backend.jgrapht_it_next_double(self._handle)
        if err: 
            raise_status()
        return res


class JGraphTLongSet(HandleWrapper, MutableSet):
    """JGraphT Long Set"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, handle = backend.jgrapht_set_linked_create()
            else: 
                err, handle = backend.jgrapht_set_create()
            if err: 
                raise_status()
            owner=True
        super().__init__(handle, owner)

    def __iter__(self):
        err, res = backend.jgrapht_set_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_set_size(self._handle)
        if err: 
            raise_status()
        return res

    def add(self, x):
        err, _ = backend.jgrapht_set_long_add(self._handle, x)
        if err: 
            raise_status()

    def discard(self, x):
        err = backend.jgrapht_set_long_remove(self._handle, x)
        if err: 
            raise_status()            

    def __contains__(self, x):
        err, res = backend.jgrapht_set_long_contains(self._handle, x)
        if err: 
            raise_status()
        return res

    def clear(self): 
        err = backend.jgrapht_set_clear(self._handle)
        if err: 
            raise_status()


class JGraphTLongSetIterator(HandleWrapper, Iterator): 
    """An iterator which returns sets with longs."""
    def __init__(self, handle, owner=True):
        super().__init__(handle, owner)

    def __next__(self):
        err, res = backend.jgrapht_it_hasnext(self._handle)
        if err: 
            raise_status()
        if not res: 
            raise StopIteration()
        err, res = backend.jgrapht_it_next_object(self._handle)
        if err: 
            raise_status()
        return JGraphTLongSet(handle=res)


class JGraphTLongDoubleMap(HandleWrapper):
    """JGraphT Map"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, handle = backend.jgrapht_map_linked_create()
            else: 
                err, handle = backend.jgrapht_map_create()
            if err: 
                raise_status()
            owner = True
        super().__init__(handle, owner)                

    def __iter__(self):
        err, res = backend.jgrapht_map_keys_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_map_size(self._handle)
        if err: 
            raise_status()
        return res

    def get(self, key, value=None):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            if value is not None: 
                return value
            else: 
                raise KeyError()
        err, res = backend.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def add(self, key, value):
        err = backend.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            raise_status()

    def pop(self, key, defaultvalue):
        err, res = backend.jgrapht_map_long_double_remove(self._handle, key)
        if err:
            if err == backend.STATUS_ILLEGAL_ARGUMENT:
                # key not found in map
                backend.jgrapht_clear_errno()
                if defaultvalue is not None:
                    return defaultvalue 
                else: 
                    raise KeyError()
            else:
                raise_status()
        return res

    def __contains__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        return res

    def __getitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def __setitem__(self, key, value):
        err = backend.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            raise_status()

    def __delitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_double_remove(self._handle, key)
        if err: 
            raise_status()

    def clear(self): 
        err = backend.jgrapht_map_clear(self._handle)
        if err: 
            raise_status()


class JGraphTLongLongMap(HandleWrapper):
    """JGraphT Map with long keys and long values"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, handle = backend.jgrapht_map_linked_create()
            else: 
                err, handle = backend.jgrapht_map_create()
            if err: 
                raise_status()
            owner = True
        super().__init__(handle, owner)                

    def __iter__(self):
        err, res = backend.jgrapht_map_keys_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_map_size(self._handle)
        if err: 
            raise_status()
        return res

    def get(self, key, value=None):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            if value is not None: 
                return value
            else: 
                raise KeyError()
        err, res = backend.jgrapht_map_long_long_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def add(self, key, value):
        err = backend.jgrapht_map_long_long_put(self._handle, key, value)
        if err: 
            raise_status()

    def pop(self, key, defaultvalue):
        err, res = backend.jgrapht_map_long_long_remove(self._handle, key)
        if err:
            if err == backend.STATUS_ILLEGAL_ARGUMENT:
                # key not found in map
                backend.jgrapht_clear_errno()
                if defaultvalue is not None:
                    return defaultvalue 
                else: 
                    raise KeyError()
            else:
                raise_status()
        return res

    def __contains__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        return res

    def __getitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_long_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def __setitem__(self, key, value):
        err = backend.jgrapht_map_long_long_put(self._handle, key, value)
        if err: 
            raise_status()

    def __delitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_long_remove(self._handle, key)
        if err: 
            raise_status()

    def clear(self): 
        err = backend.jgrapht_map_clear(self._handle)
        if err: 
            raise_status()


class JGraphTGraphPath(HandleWrapper, GraphPath): 
    """A class representing a graph path."""
    def __init__(self, handle, owner=True):
        super().__init__(handle, owner)
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

        err, weight, start_vertex, end_vertex, eit = backend.jgrapht_graphpath_get_fields(self._handle)
        if err:
            raise_status()

        self._weight = weight
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self._edges = list(JGraphTLongIterator(eit))

        backend.jgrapht_destroy(eit)
        if err:
            raise_status()            


class JGraphTSingleSourcePaths(HandleWrapper, SingleSourcePaths): 
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """
    def __init__(self, handle, source_vertex, owner=True):
        super().__init__(handle, owner)
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
        err, gp = backend.jgrapht_sp_singlesource_get_path_to_vertex(self._handle, target_vertex)
        if err: 
            raise_status()
        return JGraphTGraphPath(gp)


class JGraphTAllPairsPaths(HandleWrapper, AllPairsPaths): 
    """Wrapper class around the AllPairsPaths"""
    def __init__(self, handle, owner=True):
        super().__init__(handle, owner)

    def get_path(self, source_vertex, target_vertex):
        err, gp = backend.jgrapht_sp_allpairs_get_path_between_vertices(self._handle, source_vertex, target_vertex)
        if err: 
            raise_status()
        return JGraphTGraphPath(gp)

    def get_paths_from(self, source_vertex):
        err, singlesource = backend.jgrapht_sp_allpairs_get_singlesource_from_vertex(self._handle, source_vertex)
        if err: 
            raise_status()
        return JGraphTSingleSourcePaths(singlesource, source_vertex)


class JGraphTGraph(HandleWrapper, Graph):
    """The main graph class"""
    def __init__(self, handle=None, owner=True, directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True):
        if handle is None: 
            err, handle = backend.jgrapht_graph_create(directed, allowing_self_loops, allowing_multiple_edges, weighted)
            if err:
                raise_status()
            owner = True
        super().__init__(handle, owner)
        self._vertex_set = None
        self._edge_set = None
        self._graph_type = GraphType(directed, allowing_self_loops, allowing_multiple_edges, weighted)

    @property
    def graph_type(self):
        """Query the graph :class:`type <.GraphType>`.

        :returns: The graph type.
        :rtype: :class:`GraphType <.GraphType>`
        """
        return self._graph_type

    def add_vertex(self):
        """Add a new vertex to the graph.

        Vertices are automatically created and represented as longs.

        :returns: The new vertex identifier.
        :rtype: Long
        """
        err, v = backend.jgrapht_graph_add_vertex(self._handle)
        if err:
            raise_status()
        return v

    def remove_vertex(self, v):
        """Remove a vertex from the graph.

        :param v: The vertex to remove
        """
        err = backend.jgrapht_graph_remove_vertex(self._handle, v)
        if err:
            raise_status()

    def contains_vertex(self, v):
        """Check if a vertex is contained in the graph.

        :param v: The vertex
        :returns: True if the vertex is contained in the graph, False otherwise
        :rtype: boolean
        """
        err, res = backend.jgrapht_graph_contains_vertex(self._handle, v)
        if err:
            raise_status()
        return res 

    def add_edge(self, u, v, weight = None):
        """Adds an edge to the graph.

        Edges are automatically created and represented as longs.

        :param u: The first endpoint (vertex) of the edge
        :param v: The second endpoint (vertex) of the edge
        :returns: The new edge identifier
        :rtype: Long
        """
        err, res = backend.jgrapht_graph_add_edge(self._handle, u, v)
        if err:
            raise_status()

        if weight is not None: 
            self.set_edge_weight(res, weight)

        return res 

    def remove_edge(self, e):
        err, _ = backend.jgrapht_graph_remove_edge(self._handle, e)
        if err:
            raise_status()

    def contains_edge(self, e):
        err, res = backend.jgrapht_graph_contains_edge(self._handle, e)
        if err:
            raise_status()
        return res

    def contains_edge_between(self, u, v): 
        err, res = backend.jgrapht_graph_contains_edge_between(self._handle, u, v)
        if err:
            raise_status()
        return res

    def degree_of(self, v):
        err, res = backend.jgrapht_graph_degree_of(self._handle, v)
        if err:
            raise_status()
        return res     

    def indegree_of(self, v):
        err, res = backend.jgrapht_graph_indegree_of(self._handle, v)
        if err:
            raise_status()
        return res

    def outdegree_of(self, v):
        err, res = backend.jgrapht_graph_outdegree_of(self._handle, v)
        if err:
            raise_status()
        return res

    def edge_source(self, e):
        err, res = backend.jgrapht_graph_edge_source(self._handle, e)
        if err:
            raise_status()
        return res

    def edge_target(self, e):
        err, res = backend.jgrapht_graph_edge_target(self._handle, e)
        if err:
            raise_status()
        return res

    def get_edge_weight(self, e): 
        err, res = backend.jgrapht_graph_get_edge_weight(self._handle, e)
        if err:
            raise_status()
        return res

    def set_edge_weight(self, e, weight):
        err = backend.jgrapht_graph_set_edge_weight(self._handle, e, weight)
        if err:
            raise_status()

    def number_of_vertices(self):
        return len(self.vertices())

    def vertices(self):
        if self._vertex_set is None: 
            self._vertex_set = self._VertexSet(self._handle)
        return self._vertex_set

    def number_of_edges(self):
        return len(self.edges())

    def edges(self): 
        if self._edge_set is None: 
            self._edge_set = self._EdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        err, res = backend.jgrapht_graph_create_between_eit(self._handle, u, v)
        if err:
            raise_status()
        return JGraphTLongIterator(res)

    def edges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_eit(self._handle, v)
        if err:
            raise_status()
        return JGraphTLongIterator(res)

    def inedges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        return JGraphTLongIterator(res) if not err else raise_status()

    def outedges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        return JGraphTLongIterator(res) if not err else raise_status()

    class _VertexSet: 
        """Wrapper around the vertices of a JGraphT graph"""
        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            err, res = backend.jgrapht_graph_create_all_vit(self._handle)
            if err: 
                raise_status()
            return JGraphTLongIterator(res)

        def __len__(self):
            err, res = backend.jgrapht_graph_vertices_count(self._handle)
            if err: 
                raise_status()
            return res

        def __contains__(self, v):
            err, res = backend.jgrapht_graph_contains_vertex(self._handle, v)
            if err: 
                raise_status()
            return res

    class _EdgeSet: 
        """Wrapper around the edges of a JGraphT graph"""
        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            err, res = backend.jgrapht_graph_create_all_eit(self._handle)
            if err: 
                raise_status()
            return JGraphTLongIterator(res)

        def __len__(self):
            err, res = backend.jgrapht_graph_edges_count(self._handle)
            if err: 
                raise_status()
            return res

        def __contains__(self, v):
            err, res = backend.jgrapht_graph_contains_edge(self._handle, v)
            if err: 
                raise_status()
            return res


def create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True):
    """Create a graph.

    :param directed: If True the graph will be directed, otherwise undirected.
    :param allowing_self_loops: If True the graph will allow the addition of self-loops.
    :param allowing_multiple_edges: If True the graph will allow multiple-edges.
    :param weighted: If True the graph will be weighted, otherwise unweighted.
    :returns: A graph
    :rtype: :class:`type <.types.AbstractGraph>`
    """
    return JGraphTGraph(directed=directed, 
        allowing_self_loops=allowing_self_loops, 
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted
    )


class JGraphTAttributeStore(HandleWrapper):
    """Attribute Store. Used to keep attributes for exporters."""
    def __init__(self, handle=None, owner=True):
        if handle is None:
            err, handle = backend.jgrapht_attributes_store_create()
            if err: 
                raise_status()
            owner = True
        super().__init__(handle, owner)                

    def put(self, element, key, value):
        err = backend.jgrapht_attributes_store_put_string_attribute(self._handle, element, key, value)
        if err: 
            raise_status()

    def remove(self, element, key):
        err = backend.jgrapht_attributes_store_remove_attribute(self._handle, element, key)
        if err: 
            raise_status()
            


