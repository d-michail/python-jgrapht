from . import backend
from ._internals._errors import _raise_status


def diameter(graph):
    r"""Compute the `diameter <https://mathworld.wolfram.com/GraphDiameter.html>`_ of a graph. The  
    diameter of a graph is defined as :math:`\max_{v\in V}\epsilon(v)`, where :math:`\epsilon(v)`
    is the eccentricity of vertex :math:`v`. In other words, this method computes the 'longest
    shortest path'. Two special cases exist: (a) if the graph has no vertices, the diameter is 0,
    and (b) if the graph is disconnected, the diameter is positive infinity.

    :param graph: the input graph
    :returns: the graph diameter
    """
    err, res = backend.jgrapht_graph_metrics_diameter(graph.handle)
    return res if not err else _raise_status()


def radius(graph):
    r"""Compute the `radius <https://mathworld.wolfram.com/GraphRadius.html>`_ of a graph. 

    The radius of a graph is the minimum vertex eccentricity.

    .. note::
    
      If the graph has no vertices, the radius is zero. In case the graph is disconnected, the 
      radius is positive infinity.

    :param graph: the input graph
    :returns: the graph diameter
    """
    err, res = backend.jgrapht_graph_metrics_radius(graph.handle)
    return res if not err else _raise_status()


def girth(graph):
    r"""Compute the `girth <https://mathworld.wolfram.com/Girth.html>`_ of a graph. 

    The girth is the length of the shortest graph cycle (if any) in a graph. Acyclic graphs
    are considered to have infinite girth. For directed graphs, the length of the shortest 
    directed cycle is returned.

    This method invokes a breadth-first search from every vertex in the graph. Thus, its 
    runtime complexity is :math:`\mathcal{O}(n(m+n)) = \mathcal{O}(m n)`.

    :param graph: the input graph
    :returns: the graph girth
    """
    err, res = backend.jgrapht_graph_metrics_girth(graph.handle)
    return res if not err else _raise_status()


def count_triangles(graph):
    r"""Count the number of triangles in a graph.

    This is an :math:`\mathcal{O}(m^{3/2})` algorithm for counting the number of 
    triangles in an undirected graph.

    :param graph: the input graph. Must be undirected
    :returns: the number of triangles in the graph 
    :raises IllegalArgumentError: if the graph is not undirected
    """
    err, res = backend.jgrapht_graph_metrics_triangles(graph.handle)
    return res if not err else _raise_status()
