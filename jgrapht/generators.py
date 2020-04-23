
import time

from . import jgrapht as backend
from .errors import raise_status, UnsupportedOperationError

def generate_barabasi_albert(graph, m0, m, n, seed=None): 

    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert(graph.handle, m0, m, n, seed);
    if err: 
        raise_status()


def generate_barabasi_albert_forest(graph, t, n, seed=None): 

    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert_forest(graph.handle, t, n, seed);
    if err: 
        raise_status()


def generate_complete(graph, n):
    """ Generates a complete graph of any size.

    A complete graph is a graph where every vertex shares an edge with every other vertex.
    If it is a directed graph, then edges must always exist in both directions.

    :param g: The graph to alter, which should be empty.
    :param n: The number of vertices.
    """ 
    err = backend.jgrapht_generate_complete(graph.handle, n)
    if err: 
        raise_status()


def generate_complete_bipartite(graph, a, b): 
    err = backend.jgrapht_generate_bipartite_complete(graph.handle, a, b)
    if err: 
        raise_status()


def generate_empty(graph, n):
    """Generate an empty graph of any size.
    
    The `empty graph <https://mathworld.wolfram.com/EmptyGraph.html>`_ is a graph 
    with a certain number of vertices and no edges.

    :param g: The graph to alter, which should be empty.
    :param n: The number of vertices.
    """
    err = backend.jgrapht_generate_empty(graph.handle, n)
    if err: 
        raise_status()




