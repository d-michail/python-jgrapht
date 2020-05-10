from .. import backend
from ..types import (
    GraphType,
    GraphPath,
    SingleSourcePaths,
    AllPairsPaths,
    Graph,
    Clustering,
    PlanarEmbedding,
    Flow,
    Cut,
    GraphMapping,
)
from collections.abc import (
    Iterator,
    MutableSet,
    Set,
    MutableMapping,
    Collection,
)


class _HandleWrapper:
    """A handle wrapper. Keeps a handle to a backend object and cleans up
       on deletion.
    """

    def __init__(self, handle, **kwargs):
        self._handle = handle
        super().__init__()

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        if backend.jgrapht_isolate_is_attached():
            backend.jgrapht_handles_destroy(self._handle)

    def __repr__(self):
        return "_HandleWrapper(%r)" % self._handle


class _JGraphTLongIterator(_HandleWrapper, Iterator):
    """Long values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_long(self._handle)
        return res

    def __repr__(self):
        return "_JGraphTLongIterator(%r)" % self._handle


class _JGraphTDoubleIterator(_HandleWrapper, Iterator):
    """Double values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_double(self._handle)
        return res

    def __repr__(self):
        return "_JGraphTDoubleIterator(%r)" % self._handle


class _JGraphTGraphPathIterator(_HandleWrapper, Iterator):
    """A graph path iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_object(self._handle)
        return _JGraphTGraphPath(res)

    def __repr__(self):
        return "_JGraphTGraphPathIterator(%r)" % self._handle


class _JGraphTLongSet(_HandleWrapper, MutableSet):
    """JGraphT Long Set"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_set_linked_create()
            else:
                handle = backend.jgrapht_set_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_set_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_set_long_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_set_long_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTLongSetIterator(_HandleWrapper, Iterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_object(self._handle)
        return _JGraphTLongSet(handle=res)

    def __repr__(self):
        return "_JGraphTLongSetIterator(%r)" % self._handle


class _JGraphTLongListIterator(_HandleWrapper, Iterator):
    """An iterator which returns lists with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_object(self._handle)
        return _JGraphTLongList(handle=res)

    def __repr__(self):
        return "_JGraphTLongListIterator(%r)" % self._handle



class _JGraphTLongDoubleMap(_HandleWrapper, MutableMapping):
    """JGraphT Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_map_linked_create()
            else:
                handle = backend.jgrapht_map_create()
            owner = True
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_long_double_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_long_double_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try: 
            res = backend.jgrapht_map_long_double_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()
            pass

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_double_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_long_double_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        backend.jgrapht_map_long_double_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongDoubleMap(%r)" % self._handle


class _JGraphTLongLongMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with long keys and long values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_map_linked_create()
            else:
                handle = backend.jgrapht_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_long_long_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_long_long_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try:
            res = backend.jgrapht_map_long_long_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_long_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_long_long_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_long_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongLongMap(%r)" % self._handle


class _JGraphTLongList(_HandleWrapper, Collection):
    """JGraphT Long List"""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_list_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_list_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_list_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_list_long_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_list_long_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTGraphPath(_HandleWrapper, GraphPath):
    """A class representing a graph path."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
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

        (
            weight,
            start_vertex,
            end_vertex,
            eit,
        ) = backend.jgrapht_graphpath_get_fields(self._handle)

        self._weight = weight
        self._start_vertex = start_vertex
        self._end_vertex = end_vertex
        self._edges = list(_JGraphTLongIterator(eit))

    def __repr__(self):
        return "_JGraphTGraphPath(%r)" % self._handle


class _JGraphTSingleSourcePaths(_HandleWrapper, SingleSourcePaths):
    """A set of paths starting from a single source vertex.
    
    This class represents the whole shortest path tree from a single source vertex
    to all other vertices in the graph.
    """

    def __init__(self, handle, source_vertex, **kwargs):
        super().__init__(handle=handle, **kwargs)
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
        gp = backend.jgrapht_sp_singlesource_get_path_to_vertex(
            self._handle, target_vertex
        )
        return _JGraphTGraphPath(gp) if gp is not None else None

    def __repr__(self):
        return "_JGraphTSingleSourcePaths(%r)" % self._handle


class _JGraphTAllPairsPaths(_HandleWrapper, AllPairsPaths):
    """Wrapper class around the AllPairsPaths"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def get_path(self, source_vertex, target_vertex):
        gp = backend.jgrapht_sp_allpairs_get_path_between_vertices(
            self._handle, source_vertex, target_vertex
        )
        return _JGraphTGraphPath(gp) if gp is not None else None

    def get_paths_from(self, source_vertex):
        singlesource = backend.jgrapht_sp_allpairs_get_singlesource_from_vertex(
            self._handle, source_vertex
        )
        return _JGraphTSingleSourcePaths(singlesource, source_vertex)

    def __repr__(self):
        return "_JGraphTAllPairsPaths(%r)" % self._handle


class _JGraphTGraph(_HandleWrapper, Graph):
    """The actual graph implementation."""

    def __init__(
        self,
        handle=None,
        directed=True,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        **kwargs
    ):
        creating_graph = handle is None
        if creating_graph:
            handle = backend.jgrapht_graph_create(
                directed, allowing_self_loops, allowing_multiple_edges, weighted
            )
        super().__init__(handle=handle, **kwargs)

        self._vertex_set = None
        self._edge_set = None

        if not creating_graph:
            # read attributes from backend
            directed = backend.jgrapht_graph_is_directed(self._handle)
            allowing_self_loops = backend.jgrapht_graph_is_allowing_selfloops(
                self._handle
            )
            allowing_multiple_edges = backend.jgrapht_graph_is_allowing_multipleedges(self._handle)
            weighted = backend.jgrapht_graph_is_weighted(self._handle)

        self._graph_type = GraphType(
            directed, allowing_self_loops, allowing_multiple_edges, weighted
        )

    @property
    def graph_type(self):
        return self._graph_type

    def add_vertex(self, vertex):
        res = backend.jgrapht_graph_add_given_vertex(self._handle, vertex)
        return res

    def remove_vertex(self, v):
        backend.jgrapht_graph_remove_vertex(self._handle, v)

    def contains_vertex(self, v):
        res = backend.jgrapht_graph_contains_vertex(self._handle, v)
        return res

    def create_edge(self, u, v, weight=None):
        res = backend.jgrapht_graph_add_edge(self._handle, u, v)
        if weight is not None:
            self.set_edge_weight(res, weight)
        return res

    def add_edge(self, u, v, edge, weight=None):
        added = backend.jgrapht_graph_add_given_edge(self._handle, u, v, edge)
        if added and weight is not None: 
            self.set_edge_weight(edge, weight)
        return added

    def remove_edge(self, e):
        res = backend.jgrapht_graph_remove_edge(self._handle, e)
        return res

    def contains_edge(self, e):
        res = backend.jgrapht_graph_contains_edge(self._handle, e)
        return res

    def contains_edge_between(self, u, v):
        res = backend.jgrapht_graph_contains_edge_between(self._handle, u, v)
        return res

    def degree_of(self, v):
        res = backend.jgrapht_graph_degree_of(self._handle, v)
        return res

    def indegree_of(self, v):
        res = backend.jgrapht_graph_indegree_of(self._handle, v)
        return res

    def outdegree_of(self, v):
        res = backend.jgrapht_graph_outdegree_of(self._handle, v)
        return res

    def edge_source(self, e):
        res = backend.jgrapht_graph_edge_source(self._handle, e)
        return res

    def edge_target(self, e):
        res = backend.jgrapht_graph_edge_target(self._handle, e)
        return res

    def get_edge_weight(self, e):
        res = backend.jgrapht_graph_get_edge_weight(self._handle, e)
        return res

    def set_edge_weight(self, e, weight):
        backend.jgrapht_graph_set_edge_weight(self._handle, e, weight)

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
        res = backend.jgrapht_graph_create_between_eit(self._handle, u, v)
        return _JGraphTLongIterator(res)

    def edges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def inedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_in_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    def outedges_of(self, v):
        res = backend.jgrapht_graph_vertex_create_out_eit(self._handle, v)
        return _JGraphTLongIterator(res)

    class _VertexSet(Set):
        """Wrapper around the vertices of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_vit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            res = backend.jgrapht_graph_vertices_count(self._handle)
            return res

        def __contains__(self, v):
            res = backend.jgrapht_graph_contains_vertex(self._handle, v)
            return res

        def __repr__(self):
            return "_JGraphTGraph-VertexSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

    class _EdgeSet(Set):
        """Wrapper around the edges of a JGraphT graph"""

        def __init__(self, handle=None):
            self._handle = handle

        def __iter__(self):
            res = backend.jgrapht_graph_create_all_eit(self._handle)
            return _JGraphTLongIterator(res)

        def __len__(self):
            res = backend.jgrapht_graph_edges_count(self._handle)
            return res

        def __contains__(self, v):
            res = backend.jgrapht_graph_contains_edge(self._handle, v)
            return res

        def __repr__(self):
            return "_JGraphTGraph-EdgeSet(%r)" % self._handle

        def __str__(self):
            return "{" + ", ".join(str(x) for x in self) + "}"

    def __repr__(self):
        return "_JGraphTGraph(%r)" % self._handle


def create_graph(
    directed=True,
    allowing_self_loops=False,
    allowing_multiple_edges=False,
    weighted=True,
):
    """Create a graph.

    :param directed: If True the graph will be directed, otherwise undirected.
    :param allowing_self_loops: If True the graph will allow the addition of self-loops.
    :param allowing_multiple_edges: If True the graph will allow multiple-edges.
    :param weighted: If True the graph will be weighted, otherwise unweighted.
    :returns: A graph
    :rtype: :class:`type <.types.Graph>`
    """
    return _JGraphTGraph(
        directed=directed,
        allowing_self_loops=allowing_self_loops,
        allowing_multiple_edges=allowing_multiple_edges,
        weighted=weighted,
    )


class _JGraphTAttributeStore(_HandleWrapper):
    """Attribute Store. Used to keep attributes for exporters."""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_store_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, element, key, value):
        backend.jgrapht_attributes_store_put_string_attribute(
            self._handle, element, key, value
        )

    def remove(self, element, key):
        backend.jgrapht_attributes_store_remove_attribute(
            self._handle, element, key
        )

    def __repr__(self):
        return "_JGraphTAttributeStore(%r)" % self._handle


class _JGraphTAttributesRegistry(_HandleWrapper):
    """Attribute Registry. Used to keep a list of registered attributes
    for exporters.
    """

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_registry_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, name, category, type=None, default_value=None):
        backend.jgrapht_attributes_registry_register_attribute(
            self._handle, name, category, type, default_value
        )

    def remove(self, name, category):
        backend.jgrapht_attributes_registry_unregister_attribute(
            self._handle, name, category
        )

    def __repr__(self):
        return "_JGraphTAttributesRegistry(%r)" % self._handle


class _JGraphTClustering(_HandleWrapper, Clustering):
    """A vertex clustering."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def number_of_clusters(self):
        res = backend.jgrapht_clustering_get_number_clusters(self._handle)
        return res

    def ith_cluster(self, i):
        res = backend.jgrapht_clustering_ith_cluster_vit(self._handle, i)
        return _JGraphTLongIterator(res)

    def __repr__(self):
        return "_JGraphTClustering(%r)" % self._handle


class _JGraphTFlow(_JGraphTLongDoubleMap, Flow):
    """Flow representation as a map from edges to double values."""

    def __init__(self, handle, source, sink, value, **kwargs):
        self._source = source
        self._sink = sink
        self._value = value
        super().__init__(handle=handle, **kwargs)

    @property
    def source(self):
        """Source vertex in flow network."""
        return self._source

    @property
    def sink(self):
        """Sink vertex in flow network."""
        return self._sink

    @property
    def value(self):
        """Flow value."""
        return self._value

    def __repr__(self):
        return "_JGraphTFlow(%r)" % self._handle


class _JGraphTCut(Cut):
    """A graph cut."""

    def __init__(self, graph, capacity, source_partition_handle, **kwargs):
        super().__init__(**kwargs)
        self._graph = graph
        self._capacity = capacity
        self._source_partition = _JGraphTLongSet(source_partition_handle)
        self._target_partition = None
        self._edges = None

    @property
    def weight(self):
        return self._capacity

    @property
    def capacity(self):
        return self._capacity

    @property
    def source_partition(self):
        """Source partition vertex set."""
        return self._source_partition

    @property
    def target_partition(self):
        """Target partition vertex set."""
        self._lazy_compute()
        return self._target_partition

    @property
    def edges(self):
        """Target partition vertex set."""
        self._lazy_compute()
        return self._edges

    def _lazy_compute(self):
        if self._edges is not None:
            return

        self._target_partition = set(self._graph.vertices()).difference(
            self._source_partition
        )

        self._edges = set()
        if self._graph.graph_type.directed:
            for v in self._source_partition:
                for e in self._graph.outedges_of(v):
                    if self._graph.edge_target(e) not in self._source_partition:
                        self._edges.add(e)
        else:
            for e in self._graph.edges():
                s_in_s = self._graph.edge_source(e) in self._source_partition
                t_in_s = self._graph.edge_target(e) in self._source_partition
                if s_in_s ^ t_in_s:
                    self._edges.add(e)

    def __repr__(self):
        return "_JGraphTCut(%r)" % self._handle


class _JGraphTPlanarEmbedding(_HandleWrapper, PlanarEmbedding):
    """A JGraphT wrapped planar embedding."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def edges_around(self, vertex):
        res = backend.jgrapht_planarity_embedding_edges_around_vertex(
            self._handle, vertex
        )
        return list(_JGraphTLongIterator(res))

    def __repr__(self):
        return "_JGraphTPlanarEmbedding(%r)" % self._handle


class _JGraphTString(_HandleWrapper):
    """A JGraphT string."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __str__(self):
        res = backend.jgrapht_handles_get_ccharpointer(self._handle)
        return str(res)

    def __repr__(self):
        return "_JGraphTString(%r)" % self._handle


class _JGraphTGraphMapping(_HandleWrapper,GraphMapping):
    """A JGraphT mapping between two graphs g1 and g2."""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def vertex_correspondence(self, vertex, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_isomorphism_graph_mapping_vertex_correspondence(
            self._handle, vertex, forward
        )
        return other if exists else None

    def edge_correspondence(self, edge, forward=True):
        (
            exists,
            other,
        ) = backend.jgrapht_isomorphism_graph_mapping_edge_correspondence(
            self._handle, edge, forward
        )
        return other if exists else None

    def vertices_correspondence(self, forward=True):
        vertices = self._graph1.vertices if forward else self._graph2.vertices
        result = dict()
        for v in vertices():
            result[v] = self.vertex_correspondence(v, forward=forward)
        return result    

    def edges_correspondence(self, forward=True):
        edges = self._graph1.edges if forward else self._graph2.edges
        result = dict()
        for e in edges():
            result[e] = self.edge_correspondence(e, forward=forward)
        return result

    def __repr__(self):
        return "_JGraphTGraphMapping(%r)" % self._handle


class _JGraphTGraphMappingIterator(_HandleWrapper, Iterator):
    """A graph mapping iterator"""

    def __init__(self, handle, graph1, graph2, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph1 = graph1
        self._graph2 = graph2

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        res = backend.jgrapht_it_next_object(self._handle)
        return _JGraphTGraphMapping(res, self._graph1, self._graph2)

    def __repr__(self):
        return "_JGraphTGraphMappingIterator(%r)" % self._handle