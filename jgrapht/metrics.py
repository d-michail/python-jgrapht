from . import backend
from ._errors import raise_status


def diameter(graph):
    r"""Compute the `diameter <https://mathworld.wolfram.com/GraphDiameter.html>`_ of a graph. The  
    diameter of a graph is defined as :math:`\max_{v\in V}\epsilon(v)`, where :math:`\epsilon(v)`
    is the eccentricity of vertex :math:`v`. In other words, this method computes the 'longest
    shortest path'. Two special cases exist: (a) if the graph has no vertices, the diameter is 0,
    and (b) if the graph is disconnected, the diameter is positive infinity.

    :param graph: The input graph
    :returns: The graph diameter
    """
    err, res = backend.jgrapht_graph_metrics_diameter(graph.handle)
    return res if not err else raise_status()


def radius(graph):
    err, res = backend.jgrapht_graph_metrics_radius(graph.handle)
    return res if not err else raise_status()


def girth(graph):
    err, res = backend.jgrapht_graph_metrics_girth(graph.handle)
    return res if not err else raise_status()


def count_triangles(graph):
    err, res = backend.jgrapht_graph_metrics_triangles(graph.handle)
    return res if not err else raise_status()
