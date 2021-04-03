from .. import backend as _backend
from .._internals._wrappers import GraphBackend
from .._internals._results import (
    _unwrap_vertex,
)


def _linkprediction_alg(name, graph, u, v):
    cases = {
        GraphBackend.ANY_HASHABLE_GRAPH: "ix",
        GraphBackend.LONG_GRAPH: "lx",
        GraphBackend.INT_GRAPH: "ix",
        GraphBackend.REF_GRAPH: "rx",
    }
    graph_backend_type = cases[graph._backend_type]

    alg_method = getattr(
        _backend, "jgrapht_{}_link_prediction_exec_{}".format(graph_backend_type, name)
    )
    score = alg_method(graph.handle, _unwrap_vertex(graph, u), _unwrap_vertex(graph, v))
    return score


def adamic_adar_index(graph, u, v):
    """Compute the Adamic-Adar index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("adamic_adar_index", graph, u, v)


def common_neighbors(graph, u, v):
    """Compute the number of common neighbors.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("common_neighbors", graph, u, v)


def hub_depressed_index(graph, u, v):
    """Compute the Hub Depressed index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("hub_depressed_index", graph, u, v)


def hub_promoted_index(graph, u, v):
    """Compute the Hub Promoted index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("hub_promoted_index", graph, u, v)


def jaccard_coefficient(graph, u, v):
    """Compute the Jaccard coefficient.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("jaccard_coefficient", graph, u, v)


def leicht_holme_newman_index(graph, u, v):
    """Compute the Leicht-Holme-Newman index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("leicht_holme_newman_index", graph, u, v)


def preferential_attachment(graph, u, v):
    """Compute the preferential attachment index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("preferential_attachment", graph, u, v)


def resource_allocation_index(graph, u, v):
    """Compute the Resource Allocation index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("resource_allocation_index", graph, u, v)


def salton_index(graph, u, v):
    """Salton Index, also called the cosine similarity.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("salton_index", graph, u, v)


def sorensen_index(graph, u, v):
    """Compute the Sørensen index.

    :param graph: the graph
    :param u: a vertex
    :param v: a vertex
    :returns: the score
    """
    return _linkprediction_alg("sorensen_index", graph, u, v)
