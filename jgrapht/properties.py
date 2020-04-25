from . import jgrapht as backend
from .errors import raise_status

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
