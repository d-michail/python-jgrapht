import time

from . import backend
from ._errors import raise_status, UnsupportedOperationError

def barabasi_albert_graph(graph, m0, m, n, seed=None): 
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert(graph.handle, m0, m, n, seed)
    if err: 
        raise_status()


def barabasi_albert_forest(graph, t, n, seed=None): 
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert_forest(graph.handle, t, n, seed)
    if err: 
        raise_status()

def complete_graph(graph, n):
    """ Generates a complete graph of any size.

    A complete graph is a graph where every vertex shares an edge with every other vertex.
    If it is a directed graph, then edges must always exist in both directions.

    :param g: The graph to alter, which should be empty.
    :param n: The number of vertices.
    """ 
    err = backend.jgrapht_generate_complete(graph.handle, n)
    if err: 
        raise_status()


def complete_bipartite_graph(graph, a, b): 
    err = backend.jgrapht_generate_bipartite_complete(graph.handle, a, b)
    if err: 
        raise_status()


def empty_graph(graph, n):
    """Generate an empty graph of any size.
    
    The `empty graph <https://mathworld.wolfram.com/EmptyGraph.html>`_ is a graph 
    with a certain number of vertices and no edges.

    :param g: The graph to alter, which should be empty.
    :param n: The number of vertices.
    """
    err = backend.jgrapht_generate_empty(graph.handle, n)
    if err: 
        raise_status()


def gnm_random_graph(graph, n, m, loops=False, multiple_edges=False, seed=None):
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_gnm_random(graph.handle, n, m, loops, multiple_edges, seed)
    if err: 
        raise_status()


def gnp_random_graph(graph, n, p, loops=False, seed=None):
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_gnp_random(graph.handle, n, p, loops, seed)
    if err: 
        raise_status()


def ring_graph(graph, n):
    err = backend.jgrapht_generate_ring(graph.handle, n)
    if err: 
        raise_status()


def scalefree_graph(graph, n, seed=None):
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_scalefree(graph.handle, n, seed)
    if err: 
        raise_status()


def watts_strogatz_graph(graph, n, k, p, add_instead_of_rewire=False, seed=None):
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_watts_strogatz(graph.handle, n, k, p, add_instead_of_rewire, seed)
    if err: 
        raise_status()


def kleinberg_smallworld_graph(graph, n, p, q, r, seed=None):
    r"""Kleinberg's small-world graph generator.

    The generator is described in the paper: J. Kleinberg, The Small-World Phenomenon: An Algorithmic
    Perspective, in Proc. 32nd ACM Symp. Theory of Comp., 163-170, 2000.

    The basic structure is a a two-dimensional grid and allows for edges to be directed. It begins
    with a set of nodes (representing individuals in the social network) that are identified with the
    set of lattice points in an :math:`n \times n` square. For a universal constant :math:`p \geq 1`, 
    the node :math:`u` has a directed edge to every other node within lattice distance :math:`p`
    (these are its local contacts). For universal constants :math:`q \geq 0` and :math:`r \geq 0`,
    we also construct directed edges from :math:`u` to :math:`q` other nodes (the long-range contacts)
    using independent random trials; the i-th directed edge from :math:`u` has endpoint :math:`v` with
    probability proportional to :math:`1/d(u,v)^r` where :math:`d(u,v)` is the lattice distance
    from :math:`u` to :math:`v`.

    :param g: the graph to populate
    :param n: generate set of lattice points in a :math:`n` by :math:`n` square
    :param p: lattice distance for which each node is connected to every other node in the lattice (local connections)
    :param q: how many long-range contacts to add for each node
    :param r: probability distribution parameter which is a basic structural parameter measuring how widely "networked" the underlying society of nodes is
    :param seed: seed for the random number generator
    :raises IllegalArgumentError: in case of invalid parameters
    """
    if seed is None: 
        seed = int(time.time())

    err = backend.jgrapht_generate_kleinberg_smallworld(graph.handle, n, p, q, r, seed)
    if err: 
        raise_status()        