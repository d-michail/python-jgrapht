from abc import ABC, abstractmethod


class GraphType:
    """Graph Type"""

    def __init__(
        self,
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        modifiable=True,
    ):
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

        :returns True if the graph allows multiple-edges, False otherwise.
        """
        return self._allowing_multiple_edges

    @property
    def weighted(self):
        """Tells if the graph is weighted or not.
        
        :returns True if the graph is weighted, False otherwise.
        """
        return self._weighted

    @property
    def modifiable(self):
        """Tells if the graph is modifiable or not.
        
        :returns True if the graph is modifiable, False otherwise.
        """
        return self._modifiable

    def __repr__(self):
        return {
            "directed": self._directed,
            "allowing_self_loops": self._allowing_self_loops,
            "allowing_multiple_edges": self._allowing_multiple_edges,
            "weighted": self._weighted,
            "modifiable": self._modifiable,
        }

    def __str__(self):
        return "GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, weighted={}, modifiable={})".format(
            self._directed,
            self._allowing_self_loops,
            self._allowing_multiple_edges,
            self._weighted,
            self._modifiable,
        )


class GraphPath(ABC):
    """Interface for a graph path."""

    def __init__(self):
        pass

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
    def __iter__(self):
        pass


class SingleSourcePaths(ABC):
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """

    def __init__(self):
        pass

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

    def __init__(self):
        pass

    @abstractmethod
    def get_path(self, source_vertex, target_vertex):
        """Get a path from a source vertex to a target vertex. 

        :param source_vertex: The source vertex
        :param target_vertex: The target vertex
        :returns: A path from the source vertex to the target vertex
        :rtype: :class:`.GraphPath`
        """
        pass

    @abstractmethod
    def get_paths_from(self, source_vertex):
        pass


class Graph(ABC):
    """A graph."""

    def __init__(self):
        pass

    @abstractmethod
    def graph_type(self):
        """Query the graph :class:`type <.GraphType>`.

        :returns: The graph type.
        :rtype: :class:`GraphType <.GraphType>`
        """
        pass

    @abstractmethod
    def add_vertex(self):
        """Add a new vertex to the graph.

        Vertices are automatically created and represented as longs.

        :returns: The new vertex identifier.
        :rtype: Long
        """
        pass

    @abstractmethod
    def remove_vertex(self, v):
        """Remove a vertex from the graph.

        :param v: The vertex to remove
        """
        pass

    @abstractmethod
    def contains_vertex(self, v):
        """Check if a vertex is contained in the graph.

        :param v: The vertex
        :returns: True if the vertex is contained in the graph, False otherwise
        :rtype: boolean
        """
        pass

    @abstractmethod
    def add_edge(self, u, v, weight=None):
        """Adds an edge to the graph.

        Edges are automatically created and represented as longs.

        :param u: The first endpoint (vertex) of the edge
        :param v: The second endpoint (vertex) of the edge
        :returns: The new edge identifier
        :rtype: Long
        """
        pass

    @abstractmethod
    def remove_edge(self, e):
        """Remove an edge from the graph.

        :param e: The edge identifier to remove
        """
        pass

    @abstractmethod
    def contains_edge(self, e):
        """Check if an edge is contained in the graph.

        :param e: The edge identifier to check
        :returns: True if the edge belongs to the graph, False otherwise.
        :rtype: Boolean
        """
        pass

    @abstractmethod
    def contains_edge_between(self, u, v):
        pass

    @abstractmethod
    def degree_of(self, v):
        """Returns the degree of the specified vertex.

        A degree of a vertex in an undirected graph is the number of edges touching that vertex.
        Edges with same source and target vertices (self-loops) are counted twice.
        In directed graphs this method returns the sum of the "in degree" and the "out degree".
     
        :param v: vertex whose degree is to be calculated
        :returns: the degree of the specified vertex
        :raises IllegalArgumentError: if the vertex is not found in the graph
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
        :raises IllegalArgumentError: if the vertex is not found in the graph
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
        :raises IllegalArgumentError: if the vertex is not found in the graph
        """
        pass

    def edge_endpoints(self, e):
        """Get both endpoints of an edge as a tuple.

        :param e: the edge
        :returns: the edge endpoints as a (u,v) tuple
        """
        return self.edge_source(e), self.edge_target(e)

    @abstractmethod
    def edge_source(self, e):
        pass

    @abstractmethod
    def edge_target(self, e):
        pass

    @abstractmethod
    def get_edge_weight(self, e):
        pass

    @abstractmethod
    def set_edge_weight(self, e, weight):
        pass

    def number_of_vertices(self):
        return len(self.vertices())

    @abstractmethod
    def vertices(self):
        pass

    def number_of_edges(self):
        return len(self.edges())

    @abstractmethod
    def edges(self):
        pass

    @abstractmethod
    def edges_between(self, u, v):
        pass

    @abstractmethod
    def edges_of(self, v):
        pass

    @abstractmethod
    def inedges_of(self, v):
        pass

    @abstractmethod
    def outedges_of(self, v):
        pass


class Clustering(ABC):
    """A vertex clustering.
    """

    def __init__(self):
        pass

    @abstractmethod
    def number_of_clusters(self):
        """Number of clusters."""
        pass

    @abstractmethod
    def ith_cluster(self, i):
        pass
