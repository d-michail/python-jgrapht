from abc import ABC, abstractmethod
from copy import copy

from . import backend
from ._errors import raise_status
from ._wrappers import JGraphTLongIterator

class GraphType: 
    """Graph Type"""
    def __init__(self, directed=True, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True, modifiable=True):
        self._directed = directed
        self._allowing_self_loops = allowing_self_loops
        self._allowing_multiple_edges = allowing_multiple_edges
        self._weighted = weighted
        self._modifiable = modifiable

    @property
    def directed(self):
        """Check if the graph is directed.

        :returns: True if the graph is directed, False otherwise.
        """
        return self._directed

    @property
    def undirected(self):
        """Check if the graph is undirected.
        
        :returns: True if the graph is undirected, False otherwise.
        """
        return not self._directed    

    @property
    def allowing_self_loops(self):
        """Check if the graph allows self-loops.

        Self-loops are edges (u,v) where u = v.
        
        :returns: True if the graph allows self-loops, False otherwise.
        """
        return self._allowing_self_loops

    @property
    def allowing_multiple_edges(self):
        return self._allowing_multiple_edges

    @property
    def weighted(self):
        return self._weighted

    @property
    def modifiable(self):
        return self._modifiable    

    def __repr__(self):
        return { 'directed':self._directed, 
                 'allowing_self_loops':self._allowing_self_loops, 
                 'allowing_multiple_edges':self._allowing_multiple_edges, 
                 'weighted': self._weighted,
                 'modifiable': self._modifiable
        }

    def __str__(self):
        return 'GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, weighted={}, modifiable={})' \
            .format(self._directed, self._allowing_self_loops, self._allowing_multiple_edges, self._weighted, self._modifiable)


class _JGraphTGraph(ABC):
    def __init__(self, handle, owner):
        self._handle = handle
        self._owner = owner
        self._vertex_set = None
        self._edge_set = None

    def __del__(self):
        if backend.jgrapht_is_thread_attached() and self._owner:
            err = backend.jgrapht_destroy(self._handle)
            if err:
                raise_status()    

    @abstractmethod
    def graph_type(self):
        pass

    @property
    def handle(self):
        return self._handle

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
        """Remove an edge from the graph.

        :param e: The edge identifier to remove
        """ 
        err, _ = backend.jgrapht_graph_remove_edge(self._handle, e)
        if err:
            raise_status()

    def contains_edge(self, e):
        """Check if an edge is contained in the graph.

        :param e: The edge identifier to check
        :returns: True if the edge belongs to the graph, False otherwise.
        :rtype: Boolean
        """ 
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

    def edge_endpoints(self, e):
        """Get both endpoints of an edge as a tuple.

        :param e: the edge
        :returns: the edge endpoints as a (u,v) tuple
        """
        return self.edge_source(e), self.edge_target(e)

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


class Graph(_JGraphTGraph):
    """The main graph class"""
    def __init__(self, handle=None, owner=True, directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True):
        if handle is None: 
            err, handle = backend.jgrapht_graph_create(directed, allowing_self_loops, allowing_multiple_edges, weighted)
            if err:
                raise_status()

        super().__init__(handle, owner)
        self._graph_type = GraphType(directed, allowing_self_loops, allowing_multiple_edges, weighted)

    @property
    def graph_type(self):
        """Query the graph :class:`type <.GraphType>`.

        :returns: The graph type.
        :rtype: :class:`GraphType <.GraphType>`
        """
        return self._graph_type


class GraphPath: 
    """A class representing a graph path."""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner
        self._weight = None
        self._start_vertex = None
        self._end_vertex = None
        self._edges = None

    @property
    def handle(self):
        return self._handle

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

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle)
            if err: 
                raise_status() 

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
