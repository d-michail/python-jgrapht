from collections import defaultdict
from collections.abc import (
    Set,
    MutableMapping,
)

from .. import backend
from ..types import (
    Graph,
    GraphType,
    GraphEvent,
    PropertyGraph,
)

from ._graphs import create_graph as _create_graph
from ._views import _ListenableView
from ._collections import _JGraphTIntegerStringMap


class _PropertyGraph(Graph, PropertyGraph):
    """A graph view which allows the use of any hashable as vertex and edges.
    This is a wrapper around the default graph which has integer identifiers, 
    which means that there is a performance penalty involved. The graph also 
    supports properties (attributes) on graph vertices/edges and the graph 
    itself.

    This graphs does not directly wrap a backend graph, but it passes through 
    the handle which means that it is usable in all algorithms. The result 
    however will refer to the actual graph and not the property graph wrapper.
    """

    def __init__(self, graph, vertex_supplier=None, edge_supplier=None, **kwargs):
        """Initialize a property graph

        :param graph: the actual graph which we are wrapping. Must have integer 
          vertices and edges.
        :param vertex_supplier: function which returns new vertices on each call. If
          None then object instances are used.
        :param edge_supplier: function which returns new edge on each call. If
          None then object instances are used.
        """
        # setup structural events callback
        def structural_cb(element, event_type):
            self._structural_event_listener(element, event_type)

        self._graph = _ListenableView(graph)
        self._graph.add_listener(structural_cb)

        # initialize vertex maps
        self._vertex_hash_to_id = {}
        self._vertex_id_to_hash = {}
        self._vertex_hash_to_attrs = defaultdict(lambda: {})
        self._vertex_attrs = self._VertexAttributes(self, self._vertex_hash_to_attrs)

        # initialize edge maps
        self._edge_hash_to_id = {}
        self._edge_id_to_hash = {}
        self._edge_hash_to_attrs = defaultdict(lambda: {})
        self._edge_attrs = self._EdgeAttributes(self, self._edge_hash_to_attrs)

        # initialize graph maps
        self._graph_attrs = {}

        # initialize suppliers
        if vertex_supplier is None:
            vertex_supplier = lambda: object()
        self._vertex_supplier = vertex_supplier
        if edge_supplier is None:
            edge_supplier = lambda: object()
        self._edge_supplier = edge_supplier

    @property
    def handle(self):
        """Handle to the backend graph."""
        return self._graph.handle

    @property
    def type(self):
        return self._graph.type

    def add_vertex(self, v=None):
        if v is None:
            v = self._vertex_supplier()
            if v in self._vertex_hash_to_id:
                raise ValueError(
                    "Vertex supplier returns vertices already in the graph"
                )
        else:
            if v in self._vertex_hash_to_id:
                return v
        vid = self._graph.add_vertex()
        self._vertex_hash_to_id[v] = vid
        self._vertex_id_to_hash[vid] = v
        return v

    def remove_vertex(self, v):
        if v is None:
            raise ValueError("Vertex cannot be None")
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            return False
        self._graph.remove_vertex(vid)
        return True

    def contains_vertex(self, v):
        return v in self._vertex_hash_to_id

    def add_edge(self, u, v, e=None):
        if e is None:
            e = self._edge_supplier()
            if e in self._edge_hash_to_id:
                raise ValueError("Edge supplier returns edges already in the graph")
        else:
            if e in self._edge_hash_to_id:
                return e

        uid = self._vertex_hash_to_id.get(u)
        if uid is None:
            raise ValueError("Vertex {} not in graph".format(u))
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))

        eid = self._graph.add_edge(uid, vid)
        self._edge_hash_to_id[e] = eid
        self._edge_id_to_hash[eid] = e
        return e

    def remove_edge(self, e):
        if e is None:
            raise ValueError("Edge cannot be None")
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            return False
        self._graph.remove_edge(eid)
        return True

    def contains_edge(self, e):
        return e in self._edge_hash_to_id

    def contains_edge_between(self, u, v):
        uid = self._vertex_hash_to_id.get(u)
        if uid is None:
            raise ValueError("Vertex {} not in graph".format(u))
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        return self._graph.contains_edge_between(uid, vid)

    def degree_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        return self._graph.degree_of(vid)

    def indegree_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        return self._graph.indegree_of(vid)

    def outdegree_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        return self._graph.outdegree_of(vid)

    def edge_source(self, e):
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            raise ValueError("Edge {} not in graph".format(e))
        vid = self._graph.edge_source(eid)
        return self._vertex_id_to_hash[vid]

    def edge_target(self, e):
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            raise ValueError("Edge {} not in graph".format(e))
        vid = self._graph.edge_target(eid)
        return self._vertex_id_to_hash[vid]

    def get_edge_weight(self, e):
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            raise ValueError("Edge {} not in graph".format(e))
        return self._graph.get_edge_weight(eid)

    def set_edge_weight(self, e, weight):
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            raise ValueError("Edge {} not in graph".format(e))
        self._graph.set_edge_weight(eid, weight)

    @property
    def number_of_vertices(self):
        return len(self._vertex_hash_to_id)

    @property
    def vertices(self):
        return self._vertex_hash_to_id.keys()

    @property
    def number_of_edges(self):
        return len(self._edge_hash_to_id)

    @property
    def edges(self):
        return self._edge_hash_to_id.keys()

    def edges_between(self, u, v):
        uid = self._vertex_hash_to_id.get(u)
        if uid is None:
            raise ValueError("Vertex {} not in graph".format(u))
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))

        it = self._graph.edges_between(uid, vid)
        return self._create_edge_it(it)

    def edges_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        it = self._graph.edges_of(vid)
        return self._create_edge_it(it)

    def inedges_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        it = self._graph.inedges_of(vid)
        return self._create_edge_it(it)

    def outedges_of(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        it = self._graph.outedges_of(vid)
        return self._create_edge_it(it)

    @property
    def graph_props(self):
        return self._graph_attrs

    @property
    def vertex_props(self):
        return self._vertex_attrs

    @property
    def edge_props(self):
        return self._edge_attrs

    def __repr__(self):
        return "_PropertyGraph(%r)" % self._graph.handle

    def _create_edge_it(self, edge_id_it):
        """Transform an integer edge iteration into an edge iterator."""
        for eid in edge_id_it:
            yield self._edge_id_to_hash[eid]

    def _structural_event_listener(self, element, event_type):
        """Listener for removal events. This is needed, as removing
        a graph vertex might also remove edges.
        """
        if event_type == GraphEvent.VERTEX_REMOVED:
            v = self._vertex_id_to_hash.pop(element)
            self._vertex_hash_to_id.pop(v)
            self._vertex_hash_to_attrs.pop(v, None)
        elif event_type == GraphEvent.EDGE_REMOVED:
            e = self._edge_id_to_hash.pop(element)
            self._edge_hash_to_id.pop(e)
            self._edge_hash_to_attrs.pop(e, None)

    class _VertexAttributes(MutableMapping):
        """Wrapper around a dictionary to ensure vertex existence."""

        def __init__(self, graph, storage):
            self._graph = graph
            self._storage = storage

        def __getitem__(self, key):
            if key not in self._graph.vertices:
                raise ValueError("Vertex {} not in graph".format(key))
            return self._storage[key]

        def __setitem__(self, key, value):
            if key not in self._graph.vertices:
                raise ValueError("Vertex {} not in graph".format(key))
            self._storage[key] = value

        def __delitem__(self, key):
            if key not in self._graph.vertices:
                raise ValueError("Vertex {} not in graph".format(key))
            del self._storage[key]

        def __len__(self):
            return len(self._storage)

        def __iter__(self):
            return iter(self._storage)

        def __repr__(self):
            return "_PropertyGraph-VertexAttibutes(%r)" % repr(self._storage)

    class _EdgeAttributes(MutableMapping):
        """Wrapper around a dictionary to ensure edge existence."""

        def __init__(self, graph, storage):
            self._graph = graph
            self._storage = storage

        def __getitem__(self, key):
            if key not in self._graph.edges:
                raise ValueError("Edge {} not in graph".format(key))
            return self._storage[key]

        def __setitem__(self, key, value):
            if key not in self._graph.edges:
                raise ValueError("Edge {} not in graph".format(key))
            self._storage[key] = value

        def __delitem__(self, key):
            if key not in self._graph.edges:
                raise ValueError("Edge {} not in graph".format(key))
            del self._storage[key]

        def __len__(self):
            return len(self._storage)

        def __iter__(self):
            return iter(self._storage)

        def __repr__(self):
            return "_PropertyGraph-EdgeAttibutes(%r)" % repr(self._storage)


def is_property_graph(graph):
    """Check if a graph instance is a property graph."""
    return isinstance(graph, (_PropertyGraph, PropertyGraph))


def vertex_pg_to_g(graph, vertex):
    """Translate from a property graph vertex to a graph vertex."""
    if is_property_graph(graph):
        vertex = graph._vertex_hash_to_id[vertex]
    return vertex


def vertex_g_to_pg(graph, vertex):
    """Translate from a graph vertex to a property graph vertex."""
    if is_property_graph(graph):
        vertex = graph._vertex_id_to_hash[vertex]
    return vertex


def create_property_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a property graph.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edges on each call. If
        None then object instances are used.    
    :returns: a graph
    :rtype: :class:`~jgrapht.types.PropertyGraph`    
    """
    g = _create_graph(
        directed=directed,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
    )
    return _PropertyGraph(
        g, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )


def create_directed_property_graph(
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a directed property graph.

    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.        
    :returns: a graph
    :rtype: :class:`~jgrapht.types.PropertyGraph`    
    """
    return create_property_graph(
        directed=True,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
        vertex_supplier=vertex_supplier,
        edge_supplier=edge_supplier,
    )


def create_undirected_property_graph(
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create an undirected property graph.

    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.        
    :returns: a graph
    :rtype: :class:`~jgrapht.types.PropertyGraph`    
    """
    return create_property_graph(
        directed=False,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
        vertex_supplier=vertex_supplier,
        edge_supplier=edge_supplier,
    )
