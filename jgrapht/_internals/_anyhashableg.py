from collections import defaultdict
from collections.abc import (
    Set,
    MutableMapping,
)
import copy

from .. import backend
from ..types import (
    Graph,
    GraphEvent,
    AttributesGraph,
    DirectedAcyclicGraph,
    ListenableGraph,
)
from ..utils import IntegerSupplier

from ._graphs import (
    _create_int_graph as _create_int_graph,
    _create_int_dag as _create_int_dag,
    _create_sparse_int_graph as _create_sparse_int_graph,
)
from ._views import (
    _ListenableView,
    _UnweightedGraphView,
    _UndirectedGraphView,
    _UnmodifiableGraphView,
    _EdgeReversedGraphView,
    _WeightedView,
    _MaskedSubgraphView,
)
from ._anyhashableg_collections import (
    _AnyHashableGraphVertexSet,
    _AnyHashableGraphVertexIterator,
    _AnyHashableGraphEdgeIterator,
)


class _AnyHashableGraph(Graph, AttributesGraph, ListenableGraph):
    """A graph which allows the use of any hashable as vertex and edges.
    
    This is a wrapper around the default graph which has integer identifiers, 
    which means that there is a performance penalty involved. The graph also 
    supports attributes on graph vertices/edges and the graph itself.

    This graph does not directly wrap a backend graph, but it passes through 
    the handle which means that it is usable in all algorithms. The result 
    however will refer to the actual graph and not the any-hashable graph wrapper which
    means that it needs to be translated back when returning from the call.
    Most algorithms do such a check and perform the translation automatically.
    """

    def __init__(
        self, graph, vertex_supplier=None, edge_supplier=None, copy_from=None, **kwargs
    ):
        """Initialize an any-hashable graph

        :param graph: the actual graph which we are wrapping. Must have integer 
          vertices and edges.
        :param vertex_supplier: function which returns new vertices on each call. If
          None then object instances are used.
        :param edge_supplier: function which returns new edge on each call. If
          None then object instances are used.
        :param copy_from: copy from another graph
        """
        self._graph = graph
        self._vertex_set = None
        self._edge_set = None

        # setup structural events callback
        def structural_cb(element, event_type):
            self._structural_event_listener(element, event_type)

        self._listenable_graph = _ListenableView(graph)
        self._listenable_graph.add_listener(structural_cb)
        self._user_listeners = []

        if copy_from is not None:
            # copy suppliers
            self._vertex_supplier = copy_from._vertex_supplier
            self._edge_supplier = copy_from._edge_supplier

            # copy vertex maps
            self._vertex_hash_to_id = copy_from._vertex_hash_to_id
            self._vertex_id_to_hash = copy_from._vertex_id_to_hash
            self._vertex_hash_to_attrs = copy_from._vertex_hash_to_attrs
            self._vertex_attrs = self._VertexAttributes(
                self, self._vertex_hash_to_attrs
            )

            # copy edge maps
            self._edge_hash_to_id = copy_from._edge_hash_to_id
            self._edge_id_to_hash = copy_from._edge_id_to_hash
            self._edge_hash_to_attrs = copy_from._edge_hash_to_attrs
            self._edge_attrs = self._EdgeAttributes(self, self._edge_hash_to_attrs)

            # initialize graph maps
            self._graph_attrs = copy_from._graph_attrs

        else:
            # initialize suppliers
            if vertex_supplier is None:
                vertex_supplier = lambda: object()
            self._vertex_supplier = vertex_supplier
            if edge_supplier is None:
                edge_supplier = lambda: object()
            self._edge_supplier = edge_supplier

            # initialize vertex maps
            self._vertex_hash_to_id = {}
            self._vertex_id_to_hash = {}
            self._vertex_hash_to_attrs = defaultdict(lambda: {})
            self._vertex_attrs = self._VertexAttributes(
                self, self._vertex_hash_to_attrs
            )

            # initialize edge maps
            self._edge_hash_to_id = {}
            self._edge_id_to_hash = {}
            self._edge_hash_to_attrs = defaultdict(lambda: {})
            self._edge_attrs = self._EdgeAttributes(self, self._edge_hash_to_attrs)

            # initialize graph maps
            self._graph_attrs = {}

    @property
    def handle(self):
        # Handle to the backend graph. We return the listenable graph
        # in order to track any changes, happening outside the graph.
        return self._listenable_graph.handle

    @property
    def type(self):
        return self._graph.type

    @property
    def vertex_supplier(self):
        """The vertex supplier."""
        return self._vertex_supplier

    @property
    def edge_supplier(self):
        """The edge supplier."""
        return self._edge_supplier

    def add_vertex(self, vertex=None):
        if vertex is not None and vertex in self.vertices:
            return vertex
        vid = self._graph.add_vertex()
        vertex = self._add_new_vertex(vid, vertex)
        for listener in self._user_listeners:
            listener(vertex, GraphEvent.VERTEX_ADDED)
        return vertex

    def remove_vertex(self, v):
        if v is None:
            raise ValueError("Vertex cannot be None")
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            return False
        # Call on listenable graph, as it might remove edges also.
        self._listenable_graph.remove_vertex(vid)
        return True

    def contains_vertex(self, v):
        return v in self.vertices

    def add_edge(self, u, v, weight=None, edge=None):
        if edge is not None and edge in self.edges:
            return edge

        eid = self._graph.add_edge(self._get_vertex_id(u), self._get_vertex_id(v))
        edge = self._add_new_edge(eid, edge)

        for listener in self._user_listeners:
            listener(edge, GraphEvent.EDGE_ADDED)

        if weight is not None:
            self._listenable_graph.set_edge_weight(eid, weight)

        return edge

    def remove_edge(self, e):
        if e is None:
            raise ValueError("Edge cannot be None")
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            return False
        self._listenable_graph.remove_edge(eid)
        return True

    def contains_edge(self, e):
        return e in self.edges

    def contains_edge_between(self, u, v):
        return self._listenable_graph.contains_edge_between(
            self._get_vertex_id(u), self._get_vertex_id(v)
        )

    def degree_of(self, v):
        return self._listenable_graph.degree_of(self._get_vertex_id(v))

    def indegree_of(self, v):
        return self._listenable_graph.indegree_of(self._get_vertex_id(v))

    def outdegree_of(self, v):
        return self._listenable_graph.outdegree_of(self._get_vertex_id(v))

    def edge_source(self, e):
        vid = self._listenable_graph.edge_source(self._get_edge_id(e))
        return self._vertex_id_to_hash[vid]

    def edge_target(self, e):
        vid = self._listenable_graph.edge_target(self._get_edge_id(e))
        return self._vertex_id_to_hash[vid]

    def get_edge_weight(self, e):
        return self._listenable_graph.get_edge_weight(self._get_edge_id(e))

    def set_edge_weight(self, e, weight):
        self._listenable_graph.set_edge_weight(self._get_edge_id(e), weight)

    @property
    def number_of_vertices(self):
        return len(self.vertices)

    @property
    def vertices(self):
        if self._vertex_set is None:
            self._vertex_set = self._AnyHashableGraphVertexSet(self)
        return self._vertex_set

    @property
    def number_of_edges(self):
        return len(self.edges)

    @property
    def edges(self):
        if self._edge_set is None:
            self._edge_set = self._AnyHashableGraphEdgeSet(self)
        return self._edge_set

    def edges_between(self, u, v):
        it = self._listenable_graph.edges_between(
            self._get_vertex_id(u), self._get_vertex_id(v)
        )
        return self._create_edge_it(it)

    def edges_of(self, v):
        it = self._listenable_graph.edges_of(self._get_vertex_id(v))
        return self._create_edge_it(it)

    def inedges_of(self, v):
        it = self._listenable_graph.inedges_of(self._get_vertex_id(v))
        return self._create_edge_it(it)

    def outedges_of(self, v):
        it = self._listenable_graph.outedges_of(self._get_vertex_id(v))
        return self._create_edge_it(it)

    @property
    def graph_attrs(self):
        return self._graph_attrs

    @property
    def vertex_attrs(self):
        return self._vertex_attrs

    @property
    def edge_attrs(self):
        return self._edge_attrs

    def add_listener(self, listener_cb):
        self._user_listeners.append(listener_cb)
        return listener_cb

    def remove_listener(self, listener_cb):
        self._user_listeners.remove(listener_cb)

    def __repr__(self):
        return "_AnyHashableGraph(%r)" % self._graph.handle

    def _get_vertex_id(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        return vid

    def _get_edge_id(self, e):
        eid = self._edge_hash_to_id.get(e)
        if eid is None:
            raise ValueError("Edge {} not in graph".format(e))
        return eid

    def _create_edge_it(self, edge_id_it):
        """Transform an integer edge iteration into an edge iterator."""
        for eid in edge_id_it:
            yield self._edge_id_to_hash[eid]

    def _add_new_vertex(self, vid, vertex=None):
        if vertex is None:
            vertex = self._vertex_supplier()
        if vertex in self._vertex_hash_to_id:
            raise ValueError("Vertex supplier returns vertices already in the graph")
        self._vertex_hash_to_id[vertex] = vid
        self._vertex_id_to_hash[vid] = vertex
        return vertex

    def _add_new_edge(self, eid, edge=None):
        if edge is None:
            edge = self._edge_supplier()
        if edge in self._edge_hash_to_id:
            raise ValueError("Edge supplier returns edges already in the graph")
        self._edge_hash_to_id[edge] = eid
        self._edge_id_to_hash[eid] = edge
        return edge

    def _remove_vertex(self, vid):
        v = self._vertex_id_to_hash.pop(vid)
        self._vertex_hash_to_id.pop(v)
        self._vertex_hash_to_attrs.pop(v, None)
        return v

    def _remove_edge(self, eid):
        e = self._edge_id_to_hash.pop(eid)
        self._edge_hash_to_id.pop(e)
        self._edge_hash_to_attrs.pop(e, None)
        return e

    def _structural_event_listener(self, element, event_type):
        """Listener for removal events. This is needed, as removing
        a graph vertex might also remove edges.
        """
        # perform changes in the any-hashable graph
        if event_type == GraphEvent.VERTEX_ADDED:
            self._add_new_vertex(element)
            for listener in self._user_listeners:
                listener(self._vertex_id_to_hash[element], event_type)
        elif event_type == GraphEvent.VERTEX_REMOVED:
            v = self._remove_vertex(element)
            for listener in self._user_listeners:
                listener(v, event_type)
        elif event_type == GraphEvent.EDGE_ADDED:
            self._add_new_edge(element)
            for listener in self._user_listeners:
                listener(self._edge_id_to_hash[element], event_type)
        elif event_type == GraphEvent.EDGE_REMOVED:
            e = self._remove_edge(element)
            for listener in self._user_listeners:
                listener(e, event_type)
        elif event_type == GraphEvent.EDGE_WEIGHT_UPDATED:
            e = self._edge_id_to_hash[element]
            for listener in self._user_listeners:
                listener(e, event_type)

    class _AnyHashableGraphVertexSet(Set):
        def __init__(self, graph):
            self._graph = graph
            self._handle = graph.handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_vit(self._handle)
            return _AnyHashableGraphVertexIterator(res, self._graph)

        def __len__(self):
            return backend.jgrapht_graph_vertices_count(self._handle)

        def __contains__(self, v):
            v = self._graph._vertex_hash_to_id.get(v)
            if v is None:
                return False
            # important to do both checks here, as some views might share
            # the _vertex_hash_to_id dictionary
            return backend.jgrapht_graph_contains_vertex(self._handle, v)

        def __repr__(self):
            return "_AnyHashableGraphVertexSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)    

    class _AnyHashableGraphEdgeSet(Set):
        def __init__(self, graph):
            self._graph = graph
            self._handle = graph.handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_eit(self._handle)
            return _AnyHashableGraphEdgeIterator(res, self._graph)

        def __len__(self):
            return backend.jgrapht_graph_edges_count(self._handle)

        def __contains__(self, e):
            e = self._graph._edge_hash_to_id.get(e)
            if e is None:
                return False
            # important to do both checks here, as some views might share
            # the _edge_hash_to_id dictionary
            return backend.jgrapht_graph_contains_edge(self._handle, e)

        def __repr__(self):
            return "_AnyHashableGraphEdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

        @classmethod
        def _from_iterable(cls, it):
            return set(it)    

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
            return "_AnyHashableGraph-VertexAttributes(%r)" % repr(self._storage)

        def __str__(self):
            items = []
            for v in self._graph.vertices:
                items.append("{}: {}".format(v, self._storage[v]))
            return "{" + ", ".join(items) + "}"

    class _EdgeAttributes(MutableMapping):
        """Wrapper around a dictionary to ensure edge existence."""

        def __init__(self, graph, storage):
            self._graph = graph
            self._storage = storage

        def __getitem__(self, key):
            if key not in self._graph.edges:
                raise ValueError("Edge {} not in graph".format(key))
            return self._graph._PerEdgeWeightAwareDict(
                self._graph, key, self._storage[key]
            )

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
            return "_AnyHashableGraph-EdgeAttributes(%r)" % repr(self._storage)

        def __str__(self):
            items = []
            for e in self._graph.edges:
                items.append("{}: {}".format(e, self._storage[e]))
            return "{" + ", ".join(items) + "}"

    class _PerEdgeWeightAwareDict(MutableMapping):
        """A dictionary view which knows about the special key weight and delegates
        to the graph. This is only a view."""

        def __init__(self, graph, edge, storage, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._graph = graph
            self._edge = edge
            self._storage = storage

        def __getitem__(self, key):
            if key == "weight":
                return self._graph.get_edge_weight(self._edge)
            else:
                return self._storage[key]

        def __setitem__(self, key, value):
            if key == "weight":
                if not isinstance(value, (float)):
                    raise TypeError("Weight is not a floating point number")
                self._graph.set_edge_weight(self._edge, value)
            else:
                self._storage[key] = value

        def __delitem__(self, key):
            if key == "weight":
                self._graph.set_edge_weight(self._edge, 1.0)
            else:
                del self._storage[key]

        def __len__(self):
            return len(self._storage)

        def __iter__(self):
            return iter(self._storage)

        def __repr__(self):
            return "_PerEdgeWeightAwareDict(%r, %r, %r)" % (
                repr(self._graph),
                repr(self._edge),
                repr(self._storage),
            )

        def __str__(self):
            return str(self._storage)


class _AnyHashableDirectedAcyclicGraph(_AnyHashableGraph, DirectedAcyclicGraph):
    """The directed acyclic graph wrapper."""

    def __init__(self, graph, vertex_supplier=None, edge_supplier=None, **kwargs):
        """Initialize an any-hashable dag

        :param graph: the actual graph which we are wrapping. Must have integer 
          vertices and edges.
        :param vertex_supplier: function which returns new vertices on each call. If
          None then object instances are used.
        :param edge_supplier: function which returns new edge on each call. If
          None then object instances are used.
        """
        super().__init__(
            graph=graph,
            vertex_supplier=vertex_supplier,
            edge_supplier=edge_supplier,
            **kwargs
        )

    def descendants(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        set_handle = backend.jgrapht_graph_dag_vertex_descendants(self.handle, vid)
        return _AnyHashableGraphVertexSet(set_handle, self)

    def ancestors(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))
        set_handle = backend.jgrapht_graph_dag_vertex_ancestors(self.handle, vid)
        return _AnyHashableGraphVertexSet(set_handle, self)

    def __iter__(self):
        it_handle = backend.jgrapht_graph_dag_topological_it(self.handle)
        return _AnyHashableGraphVertexIterator(it_handle, self)


class _MaskedSubgraphAnyHashableGraph(_AnyHashableGraph):
    """A masked subgraph any-hashable graph."""

    def __init__(
        self,
        graph,
        vertex_supplier,
        edge_supplier,
        copy_from,
        vertex_mask_cb,
        edge_mask_cb,
        **kwargs
    ):
        assert isinstance(
            graph, _MaskedSubgraphView
        ), "Can only be used with a masked subgraph backend"

        super().__init__(graph, vertex_supplier, edge_supplier, copy_from)
        self._vertex_mask_cb = vertex_mask_cb
        self._edge_mask_cb = edge_mask_cb

    def add_vertex(self, vertex=None):
        raise ValueError("this graph is unmodifiable")

    def remove_vertex(self, v):
        raise ValueError("this graph is unmodifiable")

    def contains_vertex(self, v):
        return v in self.vertices and not self._vertex_mask_cb(v)

    def add_edge(self, u, v, weight=None, edge=None):
        raise ValueError("this graph is unmodifiable")

    def remove_edge(self, e):
        raise ValueError("this graph is unmodifiable")

    def contains_edge(self, e):
        return e in self.edges and not self._edge_mask_cb(e)

    def __repr__(self):
        return "_MaskedSubgraphAnyHashableGraph(%r)" % self._graph.handle

    def _get_vertex_id(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None or self._vertex_mask_cb(v):
            raise ValueError("Vertex {} not in graph".format(v))
        return vid

    def _get_edge_id(self, e):
        eid = self._edge_hash_to_id.get(e)
        if eid is None or self._edge_mask_cb(e):
            raise ValueError("Edge {} not in graph".format(e))
        return eid


def _create_anyhashable_graph_subgraph(anyhashable_graph, subgraph):
    """Create an any hashable graph subgraph.

    This function create an any-hashable graph with the identical structure as the
    subgraph (which is a default graph with integer vertices/edges). The assumption
    is that the subgraph is an actual subgraph of the backing graph of the any-hashable
    graph. In other words, for each integer vertex or edge in the subgraph, the 
    any-hashable graph contains a corresponding vertex or edge.
    
    The new any-hashable graph uses the same vertices and edges that the any-hashable graph
    is using and has the same structure as the subgraph. However, its backing graph 
    is a copy and therefore might have different integer vertices/edges.

    :param anyhashable_graph: the any-hashable graph from which to copy vertices and edges
    :param subgraph: the subgraph (must be a backend _JGraphTGraph)
    """
    res = _create_anyhashable_graph(
        directed=subgraph.type.directed,
        allowing_self_loops=subgraph.type.allowing_self_loops,
        allowing_multiple_edges=subgraph.type.allowing_multiple_edges,
        weighted=subgraph.type.weighted,
        vertex_supplier=anyhashable_graph.vertex_supplier,
        edge_supplier=anyhashable_graph.edge_supplier,
    )

    vertex_map = {}
    for vid in subgraph.vertices:
        v = _vertex_g_to_anyhashableg(anyhashable_graph, vid)
        res.add_vertex(vertex=v)
        res.vertex_attrs[v] = copy.copy(anyhashable_graph.vertex_attrs[v])
        vertex_map[vid] = v

    weighted = subgraph.type.weighted
    for eid in subgraph.edges:
        e = _edge_g_to_anyhashableg(anyhashable_graph, eid)
        s, t, w = subgraph.edge_tuple(eid)
        if weighted:
            res.add_edge(vertex_map[s], vertex_map[t], weight=w, edge=e)
        else:
            res.add_edge(vertex_map[s], vertex_map[t], edge=e)
        res.edge_attrs[e] = copy.copy(anyhashable_graph.edge_attrs[e])

    return res


def _as_unweighted_anyhashable_graph(anyhashable_graph):
    """Create an unweighted view of an any-hashable graph."""
    graph = anyhashable_graph._graph
    unweighted_graph = _UnweightedGraphView(graph)

    unweighted_anyhashable_graph = _AnyHashableGraph(
        unweighted_graph, copy_from=anyhashable_graph
    )

    return unweighted_anyhashable_graph


def _as_undirected_anyhashable_graph(anyhashable_graph):
    """Create an undirected view of an any-hashable graph."""
    graph = anyhashable_graph._graph
    undirected_graph = _UndirectedGraphView(graph)

    undirected_anyhashable_graph = _AnyHashableGraph(
        undirected_graph, copy_from=anyhashable_graph
    )

    return undirected_anyhashable_graph


def _as_unmodifiable_anyhashable_graph(anyhashable_graph):
    """Create an unmodifiable view of an any-hashable graph."""
    graph = anyhashable_graph._graph
    unmodifiable_graph = _UnmodifiableGraphView(graph)

    unmodifiable_anyhashable_graph = _AnyHashableGraph(
        unmodifiable_graph, copy_from=anyhashable_graph
    )

    return unmodifiable_anyhashable_graph


def _as_edgereversed_anyhashable_graph(anyhashable_graph):
    """Create an edge reversed view of an any-hashable graph."""
    graph = anyhashable_graph._graph
    edgereversed_graph = _EdgeReversedGraphView(graph)

    edgereversed_anyhashable_graph = _AnyHashableGraph(
        edgereversed_graph, copy_from=anyhashable_graph
    )

    return edgereversed_anyhashable_graph


def _as_weighted_anyhashable_graph(
    anyhashable_graph, edge_weight_cb, cache_weights, write_weights_through
):
    """Create a weighted view of an any-hashable graph."""
    if edge_weight_cb is not None:

        def actual_edge_weight_cb(e):
            e = _edge_g_to_anyhashableg(anyhashable_graph, e)
            return edge_weight_cb(e)

    else:
        actual_edge_weight_cb = None

    graph = anyhashable_graph._graph
    weighted_graph = _WeightedView(
        graph, actual_edge_weight_cb, cache_weights, write_weights_through
    )

    weighted_anyhashable_graph = _AnyHashableGraph(
        weighted_graph, copy_from=anyhashable_graph
    )
    return weighted_anyhashable_graph


def _as_masked_subgraph_anyhashable_graph(
    anyhashable_graph, vertex_mask_cb, edge_mask_cb=None
):
    """ Create a masked subgraph view of an any-hashable graph."""

    def actual_vertex_mask_cb(v):
        v = _vertex_g_to_anyhashableg(anyhashable_graph, v)
        return vertex_mask_cb(v)

    if edge_mask_cb is not None:

        def actual_edge_mask_cb(e):
            e = _edge_g_to_anyhashableg(anyhashable_graph, e)
            return edge_mask_cb(e)

    else:
        actual_edge_mask_cb = None

    graph = anyhashable_graph._graph
    masked_subgraph = _MaskedSubgraphView(
        graph, actual_vertex_mask_cb, actual_edge_mask_cb
    )

    masked_subgraph_anyhashable_graph = _MaskedSubgraphAnyHashableGraph(
        masked_subgraph,
        vertex_supplier=None,
        edge_supplier=None,
        copy_from=anyhashable_graph,
        vertex_mask_cb=vertex_mask_cb,
        edge_mask_cb=edge_mask_cb,
    )

    return masked_subgraph_anyhashable_graph


def _is_anyhashable_graph(graph):
    """Check if a graph instance is an any-hashable graph.
    
    :param graph: the graph
    :returns: True if the graph is an any-hashable graph, False otherwise.
    """
    return isinstance(graph, (_AnyHashableGraph))


def _vertex_anyhashableg_to_g(graph, vertex):
    """Translate from an any-hashable graph vertex to a graph vertex."""
    if _is_anyhashable_graph(graph):
        return graph._vertex_hash_to_id[vertex] if vertex is not None else None
    return vertex


def _vertex_g_to_anyhashableg(graph, vertex):
    """Translate from a graph vertex to an any-hashable graph vertex."""
    if _is_anyhashable_graph(graph):
        return graph._vertex_id_to_hash[vertex] if vertex is not None else None
    return vertex


def _edge_anyhashableg_to_g(graph, edge):
    """Translate from an any-hashable graph edge to a graph edge."""
    if _is_anyhashable_graph(graph):
        return graph._edge_hash_to_id[edge] if edge is not None else None
    return edge


def _edge_g_to_anyhashableg(graph, edge):
    """Translate from a graph edge to an any-hashable graph edge."""
    if _is_anyhashable_graph(graph):
        return graph._edge_id_to_hash[edge] if edge is not None else None
    return edge


def _create_anyhashable_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a graph with any hashable as a vertex or edge.

    :param directed: if True the graph will be directed, otherwise undirected
    :param allowing_self_loops: if True the graph will allow the addition of self-loops
    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edges on each call. If
        None then object instances are used.    
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph` and :class:`~jgrapht.types.AttributesGraph`
    """
    g = _create_int_graph(
        directed=directed,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
    )
    return _AnyHashableGraph(
        g, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )


def _create_anyhashable_dag(
    allowing_multiple_edges=False,
    weighted=True,
    vertex_supplier=None,
    edge_supplier=None,
):
    """Create a directed acyclic any-hashable graph.

    :param allowing_multiple_edges: if True the graph will allow multiple-edges
    :param weighted: if True the graph will be weighted, otherwise unweighted
    :param vertex_supplier: function which returns new vertices on each call. If
        None then object instances are used.
    :param edge_supplier: function which returns new edge on each call. If
        None then object instances are used.        
    :returns: a graph
    :rtype: :class:`~jgrapht.types.DirectedAcyclicGraph` and :class:`~jgrapht.types.Graph` and :class:`~jgrapht.types.AttributesGraph`
    """
    g = _create_int_dag(
        allowing_multiple_edges=allowing_multiple_edges, weighted=weighted
    )
    return _AnyHashableDirectedAcyclicGraph(
        g, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )


def _create_sparse_anyhashable_graph(
    edgelist, directed=True, weighted=True, vertex_supplier=None, edge_supplier=None,
):
    """Create a sparse any-hashable graph.

    A sparse graph uses a CSR (compressed-sparse-rows) representation. The result is
    lower memory consumption and very efficient and cache-friendly representation on
    recent machines.

    Their main drawback is that they are not modifiable after construction.

    .. note :: Sparse graphs cannot be modified after construction. They are best suited
       for executing algorithms which do not need to modify the graph after loading.

    .. note :: While the graph structure is unmodifiable, the edge weights can be
      adjusted.

    Sparse graphs can always support self-loops and multiple-edges.

    :param edgelist: list of tuple (u,v) or (u,v,weight) for weighted graphs
    :param directed: whether the graph will be directed or undirected
    :param weighted: whether the graph will be weighted or not
    :returns: a graph
    :rtype: :class:`~jgrapht.types.Graph`
    """
    # Transform edge list from hashable to ints
    next_int = IntegerSupplier()
    vertex_hash_to_id = defaultdict(lambda: next_int())
    int_edgelist = list()
    if weighted:
        for v, u, w in edgelist:
            int_edgelist.append((vertex_hash_to_id[v], vertex_hash_to_id[u], w))
    else:
        for v, u, *w in edgelist:
            int_edgelist.append((vertex_hash_to_id[v], vertex_hash_to_id[u]))

    # Create graph
    sparse_int_graph = _create_sparse_int_graph(
        int_edgelist, num_of_vertices=len(vertex_hash_to_id), directed=directed, weighted=weighted
    )
    g = _AnyHashableGraph(
        sparse_int_graph, vertex_supplier=vertex_supplier, edge_supplier=edge_supplier
    )

    # Record mapping of existing vertices
    for vhash, vid in vertex_hash_to_id.items():
        g._vertex_hash_to_id[vhash] = vid
        g._vertex_id_to_hash[vid] = vhash

    # Record mapping of existing edges
    for eid in range(0, len(int_edgelist)):
        ehash = g._edge_supplier()
        g._edge_hash_to_id[ehash] = eid
        g._edge_id_to_hash[eid] = ehash

    return g


def _copy_to_sparse_anyhashable_graph(graph):
    """Copy an any-hashable graph to a sparse any-hashable graph.

    .. note :: Sparse graphs are unmodifiable. Attempting to alter one will result in
      an error being raised. Attributes and edge weights can be modified.

    :param graph: the input graph
    :returns: a sparse graph
    :rtype: :class:`jgrapht.types.Graph`
    """
    if len(graph.vertices) == 0:
        raise ValueError("Graph with no vertices")

    # transform edge list from hashable to ints
    next_int = IntegerSupplier()
    vertex_hash_to_id = defaultdict(lambda: next_int())
    int_edgelist = list()
    edgelist = [graph.edge_tuple(e) for e in graph.edges]
    if graph.type.weighted:
        for v, u, w in edgelist:
            int_edgelist.append((vertex_hash_to_id[v], vertex_hash_to_id[u], w))
    else:
        for v, u, *w in edgelist:
            int_edgelist.append((vertex_hash_to_id[v], vertex_hash_to_id[u]))

    # create graph
    sparse_int_graph = _create_sparse_int_graph(
        int_edgelist, num_of_vertices=len(vertex_hash_to_id), directed=graph.type.directed, weighted=graph.type.weighted
    )
    sparse = _AnyHashableGraph(
        sparse_int_graph, vertex_supplier=graph._vertex_supplier, edge_supplier=graph._edge_supplier
    )

    # record mapping of existing vertices and copy attributes
    for vhash, vid in vertex_hash_to_id.items():
        sparse._vertex_hash_to_id[vhash] = vid
        sparse._vertex_id_to_hash[vid] = vhash
        for k, v in graph.vertex_attrs[vhash].items():
            sparse.vertex_attrs[vhash][k] = v

    # record mapping of existing edges and copy attributes
    for ehash, eid in zip(graph.edges, range(0, len(graph.edges))):
        sparse._edge_hash_to_id[ehash] = eid
        sparse._edge_id_to_hash[eid] = ehash
        for k, v in graph.edge_attrs[ehash].items():
            sparse.edge_attrs[ehash][k] = v
    
    for k, v in graph.graph_attrs.items():
        sparse.graph_attrs[k] = v

    return sparse

