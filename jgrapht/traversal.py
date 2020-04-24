
from . import jgrapht as backend
from .errors import raise_status
from .util import JGraphTLongIterator

import time

def bfs_traversal(graph, start_vertex=None):
    """Create a breadth-first search (BFS) traversal vertex iterator.

    If a starting vertex is specified, the iteration will start there and will be limited to the 
    connected component that includes the vertex. If no starting vertex is specified, the iteration 
    will start at an artitrary vertex and will not be limited, that is, will be able to traverse the 
    whole graph.

    :param graph: The input graph
    :param start_vertex: Vertex to start the search or None to start from an arbitrary vertex.
    """
    if start_vertex is None:
        err, it = backend.jgrapht_traverse_create_bfs_from_all_vertices_vit(graph.handle)
    else:
        err, it = backend.jgrapht_traverse_create_bfs_from_vertex_vit(graph.handle, start_vertex)
    return JGraphTLongIterator(it) if not err else raise_status()


def lexicographic_bfs_traversal(graph):
    err, it = backend.jgrapht_traverse_create_lex_bfs_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def dfs_traversal(graph, start_vertex=None):
    if start_vertex is None:
        err, it = backend.jgrapht_traverse_create_dfs_from_all_vertices_vit(graph.handle)
    else:
        err, it = backend.jgrapht_traverse_create_dfs_from_vertex_vit(graph.handle, start_vertex)
    return JGraphTLongIterator(it) if not err else raise_status()


def topological_order_traversal(graph):
    err, it = backend.jgrapht_traverse_create_topological_order_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def random_walk_traversal(graph, start_vertex, weighted=False, max_steps=0x7fffffffffffffff, seed=None):
    if seed is None: 
        seed = int(time.time())
    err, it = backend.jgrapht_traverse_create_custom_random_walk_from_vertex_vit(graph.handle, start_vertex, weighted, max_steps, seed)
    return JGraphTLongIterator(it) if not err else raise_status()


def max_cardinality_traversal(graph):
    err, it = backend.jgrapht_traverse_create_max_cardinality_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def degeneracy_ordering_traversal(graph):
    err, it = backend.jgrapht_traverse_create_degeneracy_ordering_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def closest_first_traversal(graph, start_vertex, radius=None):
    if radius is None: 
        err, it = backend.jgrapht_traverse_create_closest_first_from_vertex_vit(graph.handle, start_vertex)
    else:
        err, it = backend.jgrapht_traverse_create_custom_closest_first_from_vertex_vit(graph.handle, start_vertex, radius)
    return JGraphTLongIterator(it) if not err else raise_status()        

