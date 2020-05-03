import time

from . import backend
from ._errors import raise_status


def barabasi_albert_graph(graph, m0, m, n, seed=None):
    """Barabási-Albert growth and preferential attachment graph generator.
 
    The generator is described in the paper: A.-L. Barabási and R. Albert. Emergence of scaling in
    random networks. Science, 286:509-512, 1999.
 
    The generator starts with a complete graph of :math:`m_0` nodes and grows the network by adding
    :math:`n - m_0` additional nodes. The additional nodes are added one by one and each of them is
    connected to :math:`m` previously added nodes, where the probability of connecting to a node is
    proportional to its degree.
 
    Note that the Barabàsi-Albert model is designed for undirected networks. Nevertheless, this
    generator also works with directed networks where the probabilities are proportional to the sum
    of incoming and outgoing degrees. For a more general discussion see the paper: M. E. J. Newman.
    The Structure and Function of Complex Networks. SIAM Rev., 45(2):167--256, 2003.

    :param graph: The graph to alter
    :param m0: Number of initial nodes
    :param m: Number of edges of each new node added during the network growth
    :param n: Final number of nodes
    :param seed: Seed for the random number generator. If None the system time is used
    :raise IllegalArgumentError: In case of invalid parameters
    """
    if seed is None:
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert(graph.handle, m0, m, n, seed)
    if err:
        raise_status()


def barabasi_albert_forest(graph, t, n, seed=None):
    """Barabási-Albert growth and preferential attachment forest generator.
 
    The general graph generator is described in the paper: A.-L. Barabási and R. Albert. Emergence of
    scaling in random networks. Science, 286:509-512, 1999.

    The generator starts with a :math:`t` isolated nodes and grows the network by adding
    :math:`n - t` additional nodes. The additional nodes are added one by one and each of them is
    connected to one previously added node, where the probability of connecting to a node is
    proportional to its degree.
 
    Note that this Barabàsi-Albert generator only works on undirected graphs.
    :param graph: The graph to alter. Must be undirected.
    :param t: Number of initial isolated nodes
    :param n: Final number of nodes
    :param seed: Seed for the random number generator. If None the system time is used
    :raise IllegalArgumentError: In case of invalid parameters    
    """
    if seed is None:
        seed = int(time.time())

    err = backend.jgrapht_generate_barabasi_albert_forest(graph.handle, t, n, seed)
    if err:
        raise_status()


def complete_graph(graph, n):
    """Generates a complete graph of any size.

    A complete graph is a graph where every vertex shares an edge with every other vertex.
    If it is a directed graph, then edges must always exist in both directions.

    :param graph: The graph to alter, which should be empty.
    :param n: The number of vertices.
    """
    err = backend.jgrapht_generate_complete(graph.handle, n)
    if err:
        raise_status()


def complete_bipartite_graph(graph, a, b):
    """Generate a complete bipartite graph.

    :param graph: The graph to alter.
    :param a: Size of the first partition.
    :param b: Size of the second partition.
    """
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
    r"""Create a random graph based on the :math:`G(n, M)` Erdős–Rényi model. 
 
    In the :math:`G(n, M)` model, a graph is chosen uniformly at random from the collection
    of all graphs which have :math:`n nodes and $M$ edges. For example, in the 
    :math:`G(3, 2)` model, each of the three possible graphs on three vertices and two edges
    are included with probability :math:`\frac{1}{3}`.
 
    The implementation creates the vertices and then randomly chooses an edge and tries to
    add it. If the add fails for any reason (an edge already exists and multiple edges are
    not allowed) it will just choose another and try again. The performance therefore varies
    significantly based on the probability of successfully constructing an acceptable edge.
 
    The implementation tries to guess the number of allowed edges based on the following. If
    self-loops or multiple edges are allowed and requested, the maximum number of edges is
    the maximum integer value. Otherwise the maximum for undirected graphs with :math:`n`
    vertices is :math:`\frac{n(n-1)}{2}` while for directed :math:`n(n-1)`.

    :param graph: The graph to alter.
    :param n: The number of nodes.
    :param m: The number of edges.
    :param loops: Whether to create self-loops.
    :param multiple_edges: Whether to create multiple edges.
    :param seed: Seed for the random number generator. If None then the system time is used.
    """
    if seed is None:
        seed = int(time.time())

    err = backend.jgrapht_generate_gnm_random(
        graph.handle, n, m, loops, multiple_edges, seed
    )
    if err:
        raise_status()


def gnp_random_graph(graph, n, p, loops=False, seed=None):
    r"""Create a random graph based on the :math:`G(n, p)$` Erdős–Rényi model.
 
    In the :math:`G(n, p)` model, a graph is constructed by connecting nodes randomly.
    Each edge is included in the graph with probability :math:`p` independent from every
    other edge. The complexity of the generator is :math:`\mathcal{O}(n^2)` where :math:`n`
    is the number of vertices.

    :param graph: The graph to alter.
    :param n: The number of nodes.
    :param p: Probability of edge existence.
    :param loops: Whether to create self-loops.
    :param seed: Seed for the random number generator. If None then the system time is used.
    """
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

    err = backend.jgrapht_generate_watts_strogatz(
        graph.handle, n, k, p, add_instead_of_rewire, seed
    )
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
