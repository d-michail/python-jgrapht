from . import backend
from ._errors import raise_status
from ._wrappers import JGraphTLongIterator

import time


def bfs_traversal(graph, start_vertex=None):
    """Create a breadth-first search (BFS) traversal vertex iterator.

    If a starting vertex is specified, the iteration will start there and will be limited to the 
    connected component that includes the vertex. If no starting vertex is specified, the iteration 
    will start at an artitrary vertex and will not be limited, that is, will be able to traverse the 
    whole graph.

    :param graph: The input graph
    :param start_vertex: Vertex to start the search or None to start from an arbitrary vertex
    :returns: A vertex iterator
    """
    if start_vertex is None:
        err, it = backend.jgrapht_traverse_create_bfs_from_all_vertices_vit(
            graph.handle
        )
    else:
        err, it = backend.jgrapht_traverse_create_bfs_from_vertex_vit(
            graph.handle, start_vertex
        )
    return JGraphTLongIterator(it) if not err else raise_status()


def lexicographic_bfs_traversal(graph):
    err, it = backend.jgrapht_traverse_create_lex_bfs_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def dfs_traversal(graph, start_vertex=None):
    """Create a depth-first search (DFS) traversal vertex iterator.

    If a starting vertex is specified, the iteration will start there and will be limited to the 
    connected component that includes the vertex. If no starting vertex is specified, the iteration 
    will start at an artitrary vertex and will not be limited, that is, will be able to traverse the 
    whole graph.

    :param graph: The input graph
    :param start_vertex: Vertex to start the search or None to start from an arbitrary vertex
    :returns: A vertex iterator
    """
    if start_vertex is None:
        err, it = backend.jgrapht_traverse_create_dfs_from_all_vertices_vit(
            graph.handle
        )
    else:
        err, it = backend.jgrapht_traverse_create_dfs_from_vertex_vit(
            graph.handle, start_vertex
        )
    return JGraphTLongIterator(it) if not err else raise_status()


def topological_order_traversal(graph):
    """A topological ordering iterator for a directed acyclic graph.

    A topological order is a permutation p of the vertices of a graph such that an edge
    (i,j) implies that i appears before j in p. For more information see 
    `wikipedia <https://en.wikipedia.org/wiki/Topological_sorting>`_ or
    `wolfram <https://mathworld.wolfram.com/TopologicalSort.html>`_.
 
    The iterator crosses components. The iterator will detect (at some point) if the graph is not
    a directed acyclic graph and raise an IllegalArgumentException.
 
    :param graph: The input graph. Must be a DAG.
    :returns: A vertex iterator
    """
    err, it = backend.jgrapht_traverse_create_topological_order_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def random_walk_traversal(
    graph, start_vertex, weighted=False, max_steps=0x7FFFFFFFFFFFFFFF, seed=None
):
    if seed is None:
        seed = int(time.time())
    err, it = backend.jgrapht_traverse_create_custom_random_walk_from_vertex_vit(
        graph.handle, start_vertex, weighted, max_steps, seed
    )
    return JGraphTLongIterator(it) if not err else raise_status()


def max_cardinality_traversal(graph):
    """A maximum cardinality search iterator for undirected graphs. 
    
    For every vertex in graph its cardinality is defined as the number of its neighbours,
    which have been already visited. The Iterator chooses the vertex with the maximum cardinality,
    breaking ties arbitrarily. 
    
    For more information of maximum cardinality search see:
    
    * Berry, A., Blair, J., Heggernes, P. et al.
      `Maximum Cardinality Search for Computing Minimal Triangulations <https://doi.org/10.1007/s00453-004-1084-3>`_,
      Algorithmica (2004) 39: 287.

    :param graph: The input graph (must be undirected)
    :returns: A vertex iterator 
    """
    err, it = backend.jgrapht_traverse_create_max_cardinality_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def degeneracy_ordering_traversal(graph):
    """A degeneracy ordering iterator.
 
    The degeneracy of a graph G is the smallest value d such that every nonempty subgraph of G
    contains a vertex of degree at most d. If a graph has degeneracy d, then it has a degeneracy
    ordering, an ordering such that each vertex has d or fewer neighbors that come later in the
    ordering. The iterator crosses components.
 
    The iterator treats the input graph as undirected even if the graph is directed. Moreover, it
    completely ignores self-loops, meaning that it operates as if self-loops do not contribute to the
    degree of a vertex.
    :param graph: The input graph
    :returns: A vertex iterator 
    """
    err, it = backend.jgrapht_traverse_create_degeneracy_ordering_vit(graph.handle)
    return JGraphTLongIterator(it) if not err else raise_status()


def closest_first_traversal(graph, start_vertex, radius=None):
    if radius is None:
        err, it = backend.jgrapht_traverse_create_closest_first_from_vertex_vit(
            graph.handle, start_vertex
        )
    else:
        err, it = backend.jgrapht_traverse_create_custom_closest_first_from_vertex_vit(
            graph.handle, start_vertex, radius
        )
    return JGraphTLongIterator(it) if not err else raise_status()
