from abc import ABC, abstractmethod
from copy import copy

from . import jgrapht as backend
from .errors import raise_status
from .util import GraphVertexSet, GraphEdgeSet
from .util import JGraphTLongIterator

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

    def add_edge(self, u, v):
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
        return res 

    def remove_edge(self, e):
        """Remove an edge from the graph.

        :param e: The edge identifier to remove
        """ 
        err, res = backend.jgrapht_graph_remove_edge(self._handle, e)
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
        """Query the graph :class:`type <.GraphType>`.

        :returns: The graph type.
        :rtype: :class:`GraphType <.GraphType>`
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

def is_empty_graph(graph):
    err, res = backend.jgrapht_graph_test_is_empty(graph.handle)
    return res if not err else raise_status()

def is_simple(graph):
    err, res = backend.jgrapht_graph_test_is_simple(graph.handle)
    return res if not err else raise_status()

def has_selfloops(graph):
    err, res = backend.jgrapht_graph_test_has_selfloops(graph.handle)
    return res if not err else raise_status()

def has_multipleedges(graph):
    err, res = backend.jgrapht_graph_test_has_multipleedges(graph.handle)
    return res if not err else raise_status()

def is_complete(graph):
    err, res = backend.jgrapht_graph_test_is_complete(graph.handle)
    return res if not err else raise_status()

def is_weakly_connected(graph):
    err, res = backend.jgrapht_graph_test_is_weakly_connected(graph.handle)
    return res if not err else raise_status()

def is_strongly_connected(graph):
    err, res = backend.jgrapht_graph_test_is_strongly_connected(graph.handle)
    return res if not err else raise_status()

def is_tree(graph):
    err, res = backend.jgrapht_graph_test_is_tree(graph.handle)
    return res if not err else raise_status()

def is_forest(graph):
    err, res = backend.jgrapht_graph_test_is_forest(graph.handle)
    return res if not err else raise_status()    

def is_overfull(graph):
    err, res = backend.jgrapht_graph_test_is_overfull(graph.handle)
    return res if not err else raise_status()    

def is_split(graph):
    err, res = backend.jgrapht_graph_test_is_split(graph.handle)
    return res if not err else raise_status()

def is_bipartite(graph):
    err, res = backend.jgrapht_graph_test_is_bipartite(graph.handle)
    return res if not err else raise_status()

def is_cubic(graph):
    """Check whether a graph is `cubic <https://mathworld.wolfram.com/CubicGraph.html>`_.

    A graph is `cubic <https://mathworld.wolfram.com/CubicGraph.html>`_ if all vertices have
    degree equal to three.

    :param graph: The input graph
    :returns: True if the graph is cubic, False otherwise.
    """
    err, res = backend.jgrapht_graph_test_is_cubic(graph.handle)
    return res if not err else raise_status()

def is_eulerian(graph):
    """Check whether a graph is `Eulerian <https://mathworld.wolfram.com/EulerianGraph.html>`_.

    An `Eulerian <https://mathworld.wolfram.com/EulerianGraph.html>`_ graph is a graph containing
    an `Eulerian cycle <https://mathworld.wolfram.com/EulerianCycle.html>`_.

    :param graph: The input graph
    :returns: True if the graph is Eulerian, False otherwise.
    """
    err, res = backend.jgrapht_graph_test_is_eulerian(graph.handle)
    return res if not err else raise_status()

def is_chordal(graph):
    err, res = backend.jgrapht_graph_test_is_chordal(graph.handle)
    return res if not err else raise_status()

def is_weakly_chordal(graph):
    err, res = backend.jgrapht_graph_test_is_weakly_chordal(graph.handle)
    return res if not err else raise_status()

def has_ore(graph):
    err, res = backend.jgrapht_graph_test_has_ore(graph.handle)
    return res if not err else raise_status()    

def is_trianglefree(graph):
    err, res = backend.jgrapht_graph_test_is_trianglefree(graph.handle)
    return res if not err else raise_status()

def is_perfect(graph):
    err, res = backend.jgrapht_graph_test_is_perfect(graph.handle)
    return res if not err else raise_status()

def is_planar(graph):
    err, res = backend.jgrapht_graph_test_is_planar(graph.handle)
    return res if not err else raise_status()

def is_kuratowski_subdivision(graph):
    err, res = backend.jgrapht_graph_test_is_kuratowski_subdivision(graph.handle)
    return res if not err else raise_status()

def is_k33_subdivision(graph):
    err, res = backend.jgrapht_graph_test_is_k33_subdivision(graph.handle)
    return res if not err else raise_status()

def is_k5_subdivision(graph):
    err, res = backend.jgrapht_graph_test_is_k5_subdivision(graph.handle)
    return res if not err else raise_status()
