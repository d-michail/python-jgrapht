from abc import ABC, abstractmethod
from collections.abc import Mapping
from .backend import GraphEvent


class GraphType:
    """Graph Type"""

    def __init__(
        self,
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        allowing_cycles=True,
        weighted=True,
        modifiable=True,
    ):
        self._directed = directed
        self._allowing_self_loops = allowing_self_loops
        self._allowing_multiple_edges = allowing_multiple_edges
        self._allowing_cycles = allowing_cycles
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
        """Tells if the graph is undirected.
        
        :returns: True if the graph is undirected, False otherwise.
        """
        return not self._directed

    @property
    def allowing_self_loops(self):
        """Tells if the graph allows self-loops. Self-loops are edges (u,v) where u = v.
        
        :returns: True if the graph allows self-loops, False otherwise.
        """
        return self._allowing_self_loops

    @property
    def allowing_multiple_edges(self):
        """Tells if the graph allows multiple edges. Multiple edges are edges 
        which have exactly the same endpoints.

        :returns: True if the graph allows multiple-edges, False otherwise.
        """
        return self._allowing_multiple_edges

    @property
    def weighted(self):
        """Tells if the graph is weighted or not.
        
        :returns: True if the graph is weighted, False otherwise.
        """
        return self._weighted

    @property
    def modifiable(self):
        """Tells if the graph is modifiable or not.
        
        :returns: True if the graph is modifiable, False otherwise.
        """
        return self._modifiable

    @property
    def allowing_cycles(self):
        """Tells if the graph allows cycles.
        
        :returns: True if the graph allows cycles, False otherwise.
        """
        return self._allowing_cycles

    def as_directed(self):
        """Return a directed version of this graph type.

        :returns: a directed version of this graph type
        """
        return GraphType(
            directed=True,
            allowing_self_loops=self._allowing_self_loops,
            allowing_multiple_edges=self._allowing_multiple_edges,
            allowing_cycles=self._allowing_cycles,
            weighted=self._weighted,
            modifiable=self._modifiable,
        )

    def as_undirected(self):
        """Return an undirected version of this graph type.

        :returns: an undirected version of this graph type
        """
        return GraphType(
            directed=False,
            allowing_self_loops=self._allowing_self_loops,
            allowing_multiple_edges=self._allowing_multiple_edges,
            allowing_cycles=self._allowing_cycles,
            weighted=self._weighted,
            modifiable=self._modifiable,
        )

    def as_weighted(self):
        """Return a weighted version of this graph type.

        :returns: a weighted version of this graph type
        """
        return GraphType(
            directed=self._directed,
            allowing_self_loops=self._allowing_self_loops,
            allowing_multiple_edges=self._allowing_multiple_edges,
            allowing_cycles=self._allowing_cycles,
            weighted=True,
            modifiable=self._modifiable,
        )

    def as_unweighted(self):
        """Return an unweighted version of this graph type.

        :returns: an unweighted version of this graph type
        """
        return GraphType(
            directed=self._directed,
            allowing_self_loops=self._allowing_self_loops,
            allowing_multiple_edges=self._allowing_multiple_edges,
            allowing_cycles=self._allowing_cycles,
            weighted=False,
            modifiable=self._modifiable,
        )

    def as_unmodifiable(self):
        """Return an unmodifiable version of this graph type.
        
        :returns: an unmodifiable version of this graph type
        """
        return GraphType(
            directed=self._directed,
            allowing_self_loops=self._allowing_self_loops,
            allowing_multiple_edges=self._allowing_multiple_edges,
            allowing_cycles=self._allowing_cycles,
            weighted=self._weighted,
            modifiable=False,
        )

    def __repr__(self):
        return "GraphType(%r,%r,%r,%r,%r,%r)" % (
            self._directed,
            self._allowing_self_loops,
            self._allowing_multiple_edges,
            self._allowing_cycles,
            self._weighted,
            self._modifiable,
        )

    def __str__(self):
        return "GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, allowing-cycles={}, weighted={}, modifiable={})".format(
            self._directed,
            self._allowing_self_loops,
            self._allowing_multiple_edges,
            self._allowing_cycles,
            self._weighted,
            self._modifiable,
        )


class GraphPath(ABC):
    """Interface for a graph path."""

    @abstractmethod
    def weight(self):
        """Weight of the path.

        :rtype: Double
        """
        pass

    @abstractmethod
    def start_vertex(self):
        """Starting vertex of the path."""
        pass

    @abstractmethod
    def end_vertex(self):
        """Ending vertex of the path."""
        pass

    @abstractmethod
    def edges(self):
        """Edges of the path.

        :rtype: :class:`collections.abc.Iterable`
        """
        pass

    @abstractmethod
    def graph(self):
        """The graph that this graph path refers to.

        :rtype: :class:`jgrapht.types.Graph`
        """
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @property
    def vertices(self):
        """Vertices of the path."""
        v_list = []

        if len(self.edges) == 0:
            start = self.start_vertex
            if start is not None and start == self.end_vertex:
                v_list.append(start)
            return v_list

        v = self.start_vertex
        v_list.append(v)
        for e in self.edges:
            v = self.graph.opposite(e, v)
            v_list.append(v)

        return v_list


class SingleSourcePaths(ABC):
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """

    @abstractmethod
    def source_vertex(self):
        """The source vertex."""
        pass

    @abstractmethod
    def get_path(self, target_vertex):
        """Get a path to a target vertex.

        :param target_vertex: The target vertex.
        :returns: a path from the source to the target vertex.
        """
        pass


class AllPairsPaths(ABC):
    """Paths between all pair of vertices. Used in all-pair shortest
    path algorithms in order to represent the result set.
    """

    @abstractmethod
    def get_path(self, source_vertex, target_vertex):
        """Get a path from a source vertex to a target vertex. 

        :param source_vertex: The source vertex
        :param target_vertex: The target vertex
        :returns: A path from the source vertex to the target vertex
        :rtype: :py:class:`.GraphPath`
        """
        pass

    @abstractmethod
    def get_paths_from(self, source_vertex):
        """Get all paths from a source vertex to all other vertices.

        :param source_vertex the source vertex
        :returns: a set of paths starting from a single source vertex
        :rtype: :py:class:`.SingleSourcePaths`
        """
        pass


class MultiObjectiveSingleSourcePaths(ABC):
    """A set of paths starting from a single source vertex.
    """

    @abstractmethod
    def source_vertex(self):
        """The source vertex."""
        pass

    @abstractmethod
    def get_paths(self, target_vertex):
        """Get the set of paths to the target vertex.

        :param target_vertex: The target vertex.
        :returns: an iterator over all paths from the source to the
          target vertex
        """
        pass


class Graph(ABC):
    """A graph."""

    @abstractmethod
    def type(self):
        """Query the graph :class:`type <.GraphType>`.

        :returns: the graph type.
        :rtype: :class:`GraphType <.GraphType>`
        """
        pass

    @abstractmethod
    def add_vertex(self, vertex=None):
        """Add a vertex to the graph.

        If the user does not provide explicitly an integer vertex identifier, a 
        new identifier is automatically created. If the user provides a vertex and the 
        vertex is already in the graph, then this method does nothing.

        :param vertex: an integer identifier for the vertex. If None then the graph
          will automatically create a new vertex identifier
        :returns: the newly created vertex identifier.
        :rtype: int
        """
        pass

    def add_vertices_from(self, vertices):
        """Add a list of vertices to the graph.

        :param vertices: a list of vertices
        :returns: a list of boolean values indicating whether each vertex is added to the graph
        :rtype: list of booleans
        """
        added = []
        for v in vertices:
            x = self.add_vertex(v)
            added.append(x)
        return added

    @abstractmethod
    def remove_vertex(self, v):
        """Remove a vertex from the graph.

        :param v: The vertex to remove
        """
        pass

    @abstractmethod
    def contains_vertex(self, v):
        """Check if a vertex is contained in the graph.

        :param v: the vertex
        :returns: true if the vertex is contained in the graph, False otherwise
        :rtype: boolean
        """
        pass

    @abstractmethod
    def add_edge(self, u, v, weight=None, edge=None):
        """Add an edge to the graph.

        If the user does not provide explicitly an integer edge identifier, a 
        new identifier is automatically created. If the user provides an edge and the 
        edge is already in the graph, then this method does nothing.

        :param u: the first endpoint (vertex) of the edge
        :param v: the second endpoint (vertex) of the edge
        :param weight: an optional weight to use for the edge. If the edge is already 
          present, its weight is not adjusted.
        :param edge: the integer edge identifier. If None then the graph will automatically
          create a new edge identifier
        :returns: the new edge identifier
        :rtype: int
        """
        pass

    def add_edges_from(self, edges):
        """Add all edges from an iterable.

        :param edges: any iterable of edges. Each edge is (u, v, weight, id) where possibly weight 
          and id are missing.
        :returns: list of added edge identifiers
        """
        created = []
        for u, v, *rest in edges:
            e = self.add_edge(u, v, *rest)
            created.append(e)
        return created

    @abstractmethod
    def remove_edge(self, e):
        """Remove an edge from the graph.

        :param e: the edge identifier to remove
        :returns: True if the edge was removed, False otherwise.
        :rtype: Boolean
        """
        pass

    @abstractmethod
    def contains_edge(self, e):
        """Check if an edge is contained in the graph.

        :param e: the edge identifier to check
        :returns: True if the edge belongs to the graph, False otherwise.
        :rtype: Boolean
        """
        pass

    @abstractmethod
    def contains_edge_between(self, u, v):
        """Check if an edge exists between two vertices.

        :param u: the first vertex
        :param v: the second vertex
        :returns: True if an edge between u and v exists, False otherwise.
        """
        pass

    def opposite(self, e, u):
        """Get the opposite vertex of an edge.

        :param e: the edge
        :param u: one endpoint of an edge
        :returns: the opposite vertex of the edge
        """
        a, b, _ = self.edge_tuple(e)
        if a == u:
            return b
        elif b == u:
            return a
        else:
            raise ValueError("Provided vertex is not an edge endpoint")

    @abstractmethod
    def degree_of(self, v):
        """Returns the degree of the specified vertex.

        A degree of a vertex in an undirected graph is the number of edges touching that vertex.
        Edges with same source and target vertices (self-loops) are counted twice.
        In directed graphs this method returns the sum of the "in degree" and the "out degree".
     
        :param v: vertex whose degree is to be calculated
        :returns: the degree of the specified vertex
        :raises ValueError: if the vertex is not found in the graph
        """
        pass

    @abstractmethod
    def indegree_of(self, v):
        """Returns the "in degree" of the specified vertex.
       
        The `indegree <https://mathworld.wolfram.com/Indegree.html>`_ of a vertex in a directed
        graph is the number of inward directed edges from that vertex.
        In the case of undirected graphs this method returns the number of edges touching the vertex.
        Edges with same source and target vertices (self-loops) are counted twice.
     
        :param v: vertex whose degree is to be calculated
        :returns: the degree of the specified vertex
        :raises ValueError: if the vertex is not found in the graph
        """
        pass

    @abstractmethod
    def outdegree_of(self, v):
        """Returns the "out degree" of the specified vertex.
      
        The `outdegree <https://mathworld.wolfram.com/Outdegree.html>`_ of a vertex in a directed
        graph is the number of outward directed edges from that vertex.
        In the case of undirected graphs this method returns the number of edges touching the vertex.
        Edges with same source and target vertices (self-loops) are counted twice.
     
        :param v: vertex whose degree is to be calculated
        :returns: the degree of the specified vertex
        :raises ValueError: if the vertex is not found in the graph
        """
        pass

    def edge_tuple(self, e):
        """Get an edge as a tuple.

        :param e: the edge
        :returns: the edge as (u, v, weight). If the graph is unweighted the 
            weight is always 1.0
        """
        if self.type.weighted:
            return self.edge_source(e), self.edge_target(e), self.get_edge_weight(e)
        else:
            return self.edge_source(e), self.edge_target(e), 1.0

    @abstractmethod
    def edge_source(self, e):
        """Get the source vertex of an edge.

        For directed graphs this method always returns the vertex from which the 
        edge originates. For undirected graphs, an arbitrary one of the two
        vertices, but always the same and always the opposite of what method 
        :meth:`edge_target` returns.

        :param e: the edge
        :returns: the source endpoint of the edge
        """
        pass

    @abstractmethod
    def edge_target(self, e):
        """Get the target vertex of an edge.

        For directed graphs this method always returns the vertex to which this
        edge points. For undirected graphs, an arbitrary one of the two
        vertices, but always the same and always the opposite of what method 
        :meth:`edge_source` returns.

        :param e: the edge
        :returns: the source endpoint of the edge
        """
        pass

    @abstractmethod
    def get_edge_weight(self, e):
        """Get the weight of an edge. 

        If the graph is unweighted, this method returns 1.0 in order to allow algorithms
        to also execute on them.

        :param e: the edge
        :returns: the weight of an edge
        :rtype: Double
        """
        pass

    @abstractmethod
    def set_edge_weight(self, e, weight):
        """Set the weight of an edge. 

        :param e: the edge
        :param weight: the weight
        :raises UnsupportedOperationError: in case the graph does not support weights
        """
        pass

    def number_of_vertices(self):
        """Get the number of vertices in the graph."""
        return len(self.vertices)

    @abstractmethod
    def vertices(self):
        """Graph vertex set."""
        pass

    def number_of_edges(self):
        """Get the number of edges in the graph."""
        return len(self.edges)

    @abstractmethod
    def edges(self):
        """Graph edge set."""
        pass

    @abstractmethod
    def edges_between(self, u, v):
        """Returns all edges between vertices u and v.

        :param u: the first endpoint
        :param v: the second endpoint
        :returns: all edges between vertices u and v.
        """
        pass

    @abstractmethod
    def edges_of(self, v):
        """Set of all edges touching vertex v.

        :param v: the vertex
        :returns: the set of all edges touching v.
        :raises ValueError: If the vertex is not in the graph.
        """
        pass

    @abstractmethod
    def inedges_of(self, v):
        """Set of all edges incoming into vertex v.

        In the case of undirected graphs this method returns all edges touching the
        vertex, thus, some of the returned edges may have their source and target
        vertices in the opposite order.

        :param v: the vertex
        :returns: the set of all edges incoming into v.
        :raises ValueError: If the vertex is not in the graph.
        """
        pass

    @abstractmethod
    def outedges_of(self, v):
        """Set of all edges outgoing from vertex v.

        In the case of undirected graphs this method returns all edges touching the
        vertex, thus, some of the returned edges may have their source and target
        vertices in the opposite order.

        :param v: the vertex
        :returns: the set of all edges outgoing from v.
        :raises ValueError: If the vertex is not in the graph.
        """
        pass

    def __str__(self):
        vertices = [str(v) for v in self.vertices]
        vertex_set = "{" + ", ".join(vertices) + "}"
        e_l_delim = "(" if self.type.directed else "{"
        e_r_delim = ")" if self.type.directed else "}"
        edges = [(e, *self.edge_tuple(e)) for e in self.edges]
        edges = [
            str(e) + "=" + e_l_delim + str(u) + "," + str(v) + e_r_delim
            for e, u, v, w in edges
        ]
        edge_set = "{" + ", ".join(edges) + "}"
        return "(" + vertex_set + ", " + edge_set + ")"


class Clustering(ABC):
    """A vertex clustering.
    """

    @abstractmethod
    def number_of_clusters(self):
        """Number of clusters."""
        pass

    @abstractmethod
    def ith_cluster(self, i):
        """Set of vertices comprising the i-th cluster. 
        """
        pass


class PlanarEmbedding(ABC):
    """A planar embedding. Represented as the edges ordered clockwise around the vertices.
    """

    @abstractmethod
    def edges_around(self, vertex):
        """Get edges around a vertex in clockwise order."""
        pass


class Flow(ABC, Mapping):
    """A network flow."""

    @abstractmethod
    def source(self):
        """Source vertex in flow network."""
        pass

    @abstractmethod
    def sink(self):
        """Sink vertex in flow network."""
        pass

    @property
    def value(self):
        """Flow value."""
        pass


class Cut(ABC):
    """A graph cut."""

    @abstractmethod
    def weight(self):
        """Cut edges total weight."""
        pass

    @abstractmethod
    def capacity(self):
        """Cut edges total capacity."""
        pass

    @abstractmethod
    def source_partition(self):
        """Source partition vertex set."""
        pass

    @abstractmethod
    def target_partition(self):
        """Target partition vertex set."""
        pass

    @abstractmethod
    def edges(self):
        """Edges crossing the cut."""
        pass


class GomoryHuTree(ABC):
    """A Gomory-Hu Tree."""

    @abstractmethod
    def as_graph(self):
        """Compute the Gomory-Hu tree as a graph.

        :returns: the Gomory-Hu tree as an instance of :py:class:`~jgrapht.types.Graph`
        """
        pass

    @abstractmethod
    def min_cut(self):
        """Compute the minimum cut of the graph.
        
        :returns: a cut as an instance of :py:class:`~jgrapht.types.Cut`        
        """
        pass

    @abstractmethod
    def min_st_cut(self, s, t):
        """Compute the minimum s-t cut.
        
        :returns: a cut as an instance of :py:class:`~jgrapht.types.Cut`        
        """
        pass


class EquivalentFlowTree(ABC):
    """An Equivalent Flow Tree."""

    @abstractmethod
    def as_graph(self):
        """Compute the equivalent flow tree as a graph."""
        pass

    @abstractmethod
    def max_st_flow_value(self, s, t):
        """Compute the maximum s-t flow value."""
        pass


class GraphMapping(ABC):
    """A graph mapping between two graphs g1 and g2."""

    @abstractmethod
    def vertex_correspondence(self, vertex, forward=True):
        """Get the corresponding vertex.
        
        :param vertex: the first vertex
        :param forward: if True the map is from g1 to g2, otherwise from g2 to g1
        :returns: the vertex on the other graph or None if it does not exist
        """
        pass

    @abstractmethod
    def edge_correspondence(self, edge, forward=True):
        """Get the corresponding edge.
        
        :param edge: the first edge
        :param forward: if True the map is from g1 to g2, otherwise from g2 to g1
        :returns: the edge on the other graph or None if it does not exist
        """
        pass

    @abstractmethod
    def vertices_correspondence(self, forward=True):
        """Get a dictionary with all the corresponding vertices.
        
        :param forward: if True the map is from g1 to g2, otherwise from g2 to g1
        :returns: a dictionary with keys vertices from one of the graphs and values vertices
          from the other graph
        """
        pass

    @abstractmethod
    def edges_correspondence(self, forward=True):
        """Get a dictionary with all the corresponding edges.
        
        :param forward: if True the map is from g1 to g2, otherwise from g2 to g1
        :returns: a dictionary with keys edges from one of the graphs and values edges
          from the other graph
        """
        pass


class ListenableGraph(ABC):
    """A listenable graph. The listener callbacks accept as the first parameter
    the vertex or edge of the graph and as second the event type which is
    :py:class:`~GraphEvent`.
    """

    @abstractmethod
    def add_listener(self, listener_cb):
        """Add a listener

        :returns: a handle for the listener
        """
        pass

    @abstractmethod
    def remove_listener(self, listener_handle):
        """Remove a listener

        :param listener_id: the listener handle returned when the listener was added
        """
        pass


class DirectedAcyclicGraph(ABC):
    """A directed acyclic graph."""

    @abstractmethod
    def descendants(self, vertex):
        """Get the descendants of a vertex

        :param vertex: vertex
        :returns: a vertex set
        """
        pass

    @abstractmethod
    def ancestors(self, vertex):
        """Get the ancestors of a vertex

        :param vertex: a vertex
        :returns: a vertex set
        """
        pass

    @abstractmethod
    def __iter__(self):
        """Get a topological order iterator"""
        pass


class AttributesGraph(ABC):
    """A graph which contains vertex/edge/graph attributes."""

    @abstractmethod
    def vertex_attrs(self):
        """Dictionary with vertex attributes."""
        pass

    @abstractmethod
    def edge_attrs(self):
        """Dictionary with edge attributes."""
        pass

    @abstractmethod
    def graph_attrs(self):
        """Dictionary with graph attributes."""
        pass


class LayoutModel2D(ABC):
    """A 2D Layout Model."""

    @abstractmethod
    def area(self):
        """The 2D drawable area."""
        pass

    @abstractmethod
    def get_vertex_location(self, vertex):
        """Get the location of a vertex."""
        pass

    @abstractmethod
    def set_vertex_location(self, vertex, point_2d):
        """Set the location of a vertex."""
        pass

    @abstractmethod
    def is_fixed(self, vertex, fixed):
        """Check if a vertex is fixed."""
        pass

    @abstractmethod
    def set_fixed(self, vertex, fixed):
        """Set the fixed status of a vertex."""
        pass
