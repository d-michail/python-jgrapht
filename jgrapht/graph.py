from abc import ABC, abstractmethod
from copy import copy

from .errors import raise_status
from .util import GraphVertexSet, GraphEdgeSet
from .iterator import LongValueIterator
from . import jgrapht as backend

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


class JGraphTGraph(ABC):
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
        return self._handle;

    def add_vertex(self):
        """Add a new vertex to the graph.

        Vertices are automatically created and represented as longs.

        :returns: The new vertex.
        :rtype: long
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
        err, res = backend.jgrapht_graph_contains_vertex(self._handle, v)
        if err:
            raise_status()
        return res 

    def add_edge(self, u, v):
        err, res = backend.jgrapht_graph_add_edge(self._handle, u, v)
        if err:
            raise_status()
        return res 

    def remove_edge(self, e): 
        err, res = backend.jgrapht_graph_remove_edge(self._handle, e)
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

    def vertices(self):
        if self._vertex_set is None: 
            self._vertex_set = GraphVertexSet(self._handle)
        return self._vertex_set

    def edges(self): 
        if self._edge_set is None: 
            self._edge_set = GraphEdgeSet(self._handle)
        return self._edge_set

    def edges_between(self, u, v):
        err, res = backend.jgrapht_graph_create_between_eit(self._handle, u, v)
        if err:
            raise_status()
        return LongValueIterator(res)

    def edges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_eit(self._handle, v)
        if err:
            raise_status()
        return LongValueIterator(res)

    def inedges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        if err:
            raise_status()
        return LongValueIterator(res)    

    def outedges_of(self, v):
        err, res = backend.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        if err:
            raise_status()
        return LongValueIterator(res)


class Graph(JGraphTGraph):
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
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type;


class UnweightedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unweighted(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=False,
            modifiable=graph.graph_type.modifiable)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type

class UndirectedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_undirected(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=False,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=graph.graph_type.modifiable)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type

class UnmodifiableGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_unmodifiable(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)

        self._graph_type = GraphType(directed=graph.graph_type.directed,
            allowing_self_loops=graph.graph_type.allowing_self_loops,
            allowing_multiple_edges=graph.graph_type.allowing_multiple_edges,
            weighted=graph.graph_type.weighted,
            modifiable=False)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


class EdgeReversedGraphView(JGraphTGraph):

    def __init__(self, graph):
        err, res = backend.jgrapht_graph_as_edgereversed(graph.handle)
        if err:
            raise_status()

        super().__init__(res, True)
        self._graph_type = copy(graph.graph_type)

        # Keep a reference to avoid gargage collection. This is important since the
        # same picture is maintained inside the JVM.
        self._graph = graph

    @property
    def graph_type(self):
        """Query the graph type.

        :returns: The graph type.
        """
        return self._graph_type


def as_unweighted(graph):
    """Create an unweighted view of a graph"""
    return UnweightedGraphView(graph)


def as_undirected(graph):
    """Create an undirected view of a graph"""
    return UndirectedGraphView(graph)


def as_unmodifiable(graph):
    """Create an unmodifiable view of a graph"""
    return UnmodifiableGraphView(graph)


def as_edgereversed(graph):
    """Create an edge reversed view of a graph"""
    return EdgeReversedGraphView(graph)

