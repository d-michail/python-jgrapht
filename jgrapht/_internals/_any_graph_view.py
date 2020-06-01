from .. import backend
from ..types import (
    Graph,
    GraphType,
    GraphEvent,
    PropertyGraph,
)
from ..views import as_listenable
from collections.abc import Set


class _JGraphTAnyGraphView(Graph, PropertyGraph):
    """A graph view which allows the use of any hashable as vertex and edges.
    This is a wrapper around the default graph which has integer identifiers, 
    which means that there is a performance penalty involved.
    """

    def __init__(self, graph, **kwargs):
        # setup structural events callback
        def structural_cb(element, event_type):
            self._structural_event_listener(element, event_type)

        self._graph = as_listenable(graph)
        self._graph.add_listener(structural_cb)

        # initialize maps from hashable to graph
        self._vertex_hash_to_id = {}
        self._vertex_id_to_hash = {}
        self._vertex_hash_to_attrs = {}
        self._edge_hash_to_id = {}
        self._edge_id_to_hash = {}
        self._edge_hash_to_attrs = {}
        self._graph_attrs = {}

    @property
    def type(self):
        return self._graph.type

    def add_vertex(self, v):
        if v in self._vertex_hash_to_id:
            return
        vid = self._graph.add_vertex()
        self._vertex_hash_to_id[v] = vid
        self._vertex_hash_to_attrs[v] = {}
        self._vertex_id_to_hash[vid] = v

    def remove_vertex(self, v):
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            return False
        self._graph.remove_vertex(vid)
        return True

    def contains_vertex(self, v):
        return v in self._vertex_hash_to_id

    def add_edge(self, u, v, e):
        if e in self._edge_hash_to_id:
            return False

        uid = self._vertex_hash_to_id.get(u)
        if uid is None:
            raise ValueError("Vertex {} not in graph".format(u))
        vid = self._vertex_hash_to_id.get(v)
        if vid is None:
            raise ValueError("Vertex {} not in graph".format(v))

        eid = self._graph.add_edge(uid, vid)
        self._edge_hash_to_id[e] = eid
        self._edge_hash_to_attrs[e] = {}
        self._edge_id_to_hash[eid] = e
        return True

    def remove_edge(self, e):
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

    def _create_edge_it(self, edge_id_it):
        for eid in edge_id_it:
            yield self._edge_id_to_hash[eid]

    def _structural_event_listener(self, element, event_type):
        # cleanup
        if event_type == GraphEvent.VERTEX_REMOVED:
            v = self._vertex_id_to_hash.pop(element)
            self._vertex_hash_to_id.pop(v)
            self._vertex_hash_to_attrs.pop(v)
        elif event_type == GraphEvent.EDGE_REMOVED:
            e = self._edge_id_to_hash.pop(element)
            self._edge_hash_to_id.pop(e)
            self._edge_hash_to_attrs.pop(e)

    def __repr__(self):
        return "_JGraphTAnyGraphView(%r)" % self._graph.handle
