from . import jgrapht
from . import status
from . import errors
from . import iterator
from . import util

class GraphType: 
    """Graph Type"""
    def __init__(self, directed, allowing_self_loops, allowing_multiple_edges, weighted):
        self._directed = directed
        self._allowing_self_loops = allowing_self_loops
        self._allowing_multiple_edges = allowing_multiple_edges
        self._weighed = weighted

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
        return self._allowing_self_loops

    @property
    def allowing_multiple_edges(self):
        return self._allowing_multiple_edges

    @property
    def weighted(self):
        return self._weighted

    def __repr__(self):
        return { 'directed':self._directed, 
                 'allowing_self_loops':self._allowing_self_loops, 
                 'allowing_multiple_edges':self._allowing_multiple_edges, 
                 'weighted': self._weighted }

    def __str__(self):
        return 'GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, weighted={})' \
            .format(self._directed, self._allowing_self_loops, self._allowing_multiple_edges, self._weighed)


class Graph:
    """The main graph class"""
    def __init__(self, directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True):
        status, handle = jgrapht.jgrapht_graph_create(directed, allowing_self_loops, allowing_multiple_edges, weighted)
        errors.raise_status()
        self._handle = handle
        self._graph_type = GraphType(directed, allowing_self_loops, allowing_multiple_edges, weighted)
        self._vertex_set = None
        self._edge_set = None

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached():
            err = jgrapht.jgrapht_destroy(self._handle)
            if err:
                errors.raise_status() 

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type;

    @property
    def handle(self):
        return self._handle;

    def add_vertex(self):
        """Add a new vertex to the graph.

        Vertices are automatically created and represented as longs.

        :returns: The new vertex.
        :rtype: long
        """
        err, v = jgrapht.jgrapht_graph_add_vertex(self._handle)
        if err:
            errors.raise_status()
        return v

    def remove_vertex(self, v):
        """Remove a vertex from the graph.

        :param v: The vertex to remove
        """
        err = jgrapht.jgrapht_graph_remove_vertex(self._handle, v)
        if err:
            errors.raise_status()

    def contains_vertex(self, v):
        err, res = jgrapht.jgrapht_graph_contains_vertex(self._handle, v)
        if err:
            errors.raise_status()
        return res 

    def add_edge(self, u, v):
        err, res = jgrapht.jgrapht_graph_add_edge(self._handle, u, v)
        if err:
            errors.raise_status()
        return res 

    def remove_edge(self, e): 
        err, res = jgrapht.jgrapht_graph_remove_edge(self._handle, e)
        if err:
            errors.raise_status()

    def contains_edge(self, e):
        err, res = jgrapht.jgrapht_graph_contains_edge(self._handle, e)
        if err:
            errors.raise_status()
        return res

    def contains_edge_between(self, u, v): 
        err, res = jgrapht.jgrapht_graph_contains_edge_between(self._handle, u, v)
        if err:
            errors.raise_status()
        return res

    def degree_of(self, v):
        err, res = jgrapht.jgrapht_graph_degree_of(self._handle, v)
        if err:
            errors.raise_status()
        return res     

    def indegree_of(self, v):
        err, res = jgrapht.jgrapht_graph_indegree_of(self._handle, v)
        if err:
            errors.raise_status()
        return res

    def outdegree_of(self, v):
        err, res = jgrapht.jgrapht_graph_outdegree_of(self._handle, v)
        if err:
            errors.raise_status()
        return res

    def edge_source(self, e):
        err, res = jgrapht.jgrapht_graph_edge_source(self._handle, e)
        if err:
            errors.raise_status()
        return res

    def edge_target(self, e):
        err, res = jgrapht.jgrapht_graph_edge_target(self._handle, e)
        if err:
            errors.raise_status()
        return res

    def get_edge_weight(self, e): 
        err, res = jgrapht.jgrapht_graph_get_edge_weight(self._handle, e)
        if err:
            errors.raise_status()
        return res

    def set_edge_weight(self, e, weight):
        err = jgrapht.jgrapht_graph_set_edge_weight(self._handle, e, weight)
        if err:
            errors.raise_status()

    def vertices(self):
        if self._vertex_set is None: 
            self._vertex_set = util.GraphVertexSet(self._handle)
        return self._vertex_set

    def edges(self): 
        if self._edge_set is None: 
            self._edge_set = util.GraphEdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        err, res = jgrapht.jgrapht_graph_create_between_eit(self._handle, u, v)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def edges_of(self, v):
        err, res = jgrapht.jgrapht_graph_vertex_create_eit(self._handle, v)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def inedges_of(self, v):
        err, res = jgrapht.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)    

    def outedges_of(self, v):
        err, res = jgrapht.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        if err:
            errors.raise_status()
        return iterator.LongValueIterator(res)
            