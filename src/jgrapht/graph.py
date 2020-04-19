from . import jgrapht
from . import status
from . import errors
from . import iterator

class GraphType: 
    """Graph Type"""
    def __init__(self, directed, allowing_self_loops, allowing_multiple_edges, weighted):
        self.__directed = directed
        self.__allowing_self_loops = allowing_self_loops
        self.__allowing_multiple_edges = allowing_multiple_edges
        self.__weighed = weighted

    @property
    def directed(self):
        return self.__directed

    @property
    def undirected(self):
        return not self.__directed    

    @property
    def allowing_self_loops(self):
        return self.__allowing_self_loops

    @property
    def allowing_multiple_edges(self):
        return self.__allowing_multiple_edges

    @property
    def weighted(self):
        return self.__weighted

    def __repr__(self):
        return { 'directed':self.__directed, 
                 'allowing_self_loops':self.__allowing_self_loops, 
                 'allowing_multiple_edges':self.__allowing_multiple_edges, 
                 'weighted': self.__weighted }

    def __str__(self):
        return 'GraphType(directed={}, allowing-self-loops={}, allowing-multiple-edges={}, weighted={})' \
            .format(self.__directed, self.__allowing_self_loops, self.__allowing_multiple_edges, self.__weighed)


class Graph:
    """The main graph class"""
    def __init__(self, directed=True, allowing_self_loops=True, allowing_multiple_edges=True, weighted=True):
        self.__handle = jgrapht.jgrapht_graph_create(directed, allowing_self_loops, allowing_multiple_edges, weighted)
        self.__graph_type = GraphType(directed, allowing_self_loops, allowing_multiple_edges, weighted)
        errors.check_last_error()

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached():
            errors.check_last_error()
            jgrapht.jgrapht_destroy(self.__handle) 
            errors.check_last_error()

    @property
    def graph_type(self):
        return self.__graph_type;

    @property
    def handle(self):
        return self.__handle;    

    def add_vertex(self):
        v = jgrapht.jgrapht_graph_add_vertex(self.__handle)
        errors.check_last_error()
        return v

    def remove_vertex(self, vertex):
        res = jgrapht.jgrapht_graph_remove_vertex(self.__handle, vertex)
        errors.check_last_error()
        return res 

    def contains_vertex(self, vertex):
        res = jgrapht.jgrapht_graph_contains_vertex(self.__handle, vertex)
        errors.check_last_error()
        return res 

    def vertices_count(self):
        res = jgrapht.jgrapht_graph_vertices_count(self.__handle)
        errors.check_last_error()        
        return res 

    def add_edge(self, source, target):
        e = jgrapht.jgrapht_graph_add_edge(self.__handle, source, target)
        errors.check_last_error()
        return e

    def remove_edge(self, edge): 
        res = jgrapht.jgrapht_graph_remove_edge(self.__handle, edge)
        errors.check_last_error()
        return res

    def contains_edge(self, edge):
        res = jgrapht.jgrapht_graph_contains_edge(self.__handle, edge)
        errors.check_last_error()
        return res

    def contains_edge_between(self, source, target): 
        res = jgrapht.jgrapht_graph_contains_edge_between(self.__handle, source, target)
        errors.check_last_error()
        return res     

    def edges_count(self):
        res = jgrapht.jgrapht_graph_edges_count(self.__handle)
        errors.check_last_error()        
        return res     

    def degree_of(self, vertex):
        res = jgrapht.jgrapht_graph_degree_of(self.__handle, vertex)
        errors.check_last_error()        
        return res     

    def indegree_of(self, vertex):
        res = jgrapht.jgrapht_graph_indegree_of(self.__handle, vertex)
        errors.check_last_error()        
        return res

    def outdegree_of(self, vertex):
        res = jgrapht.jgrapht_graph_outdegree_of(self.__handle, vertex)
        errors.check_last_error()        
        return res

    def edge_source(self, edge):
        res = jgrapht.jgrapht_graph_edge_source(self.__handle, edge)
        errors.check_last_error()
        return res

    def edge_target(self, edge):
        res = jgrapht.jgrapht_graph_edge_target(self.__handle, edge)
        errors.check_last_error()
        return res

    def get_edge_weight(self, edge): 
        res = jgrapht.jgrapht_graph_get_edge_weight(self.__handle, edge)
        errors.check_last_error()
        return res

    def set_edge_weight(self, edge, weight): 
        jgrapht.jgrapht_graph_set_edge_weight(self.__handle, edge, weight)
        errors.check_last_error()

    def vertices(self): 
        handle = jgrapht.jgrapht_graph_create_all_vit(self.__handle)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)

    def edges(self): 
        handle = jgrapht.jgrapht_graph_create_all_eit(self.__handle)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)

    def edges_between(self, source, target):
        handle = jgrapht.jgrapht_graph_create_between_eit(self.__handle)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)

    def edges_of(self, vertex):
        handle = jgrapht.jgrapht_graph_vertex_create_eit(self.__handle, vertex)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)

    def inedges_of(self, vertex):
        handle = jgrapht.jgrapht_graph_vertex_create_in_eit(self.__handle, vertex)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)    

    def outedges_of(self, vertex):
        handle = jgrapht.jgrapht_graph_vertex_create_out_eit(self.__handle, vertex)
        errors.check_last_error()
        return iterator.VertexOrEdgeIterator(handle)    