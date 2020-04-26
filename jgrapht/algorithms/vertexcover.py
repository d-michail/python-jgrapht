from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from ..util import JGraphTLongDoubleMap, JGraphTLongSet


def _vertexcover_alg(name, graph, vertex_weights=None):

    alg_method_name = 'jgrapht_vertexcover_exec_' + name
    if vertex_weights is not None: 
        alg_method_name += '_weighted'

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        if vertex_weights is not None: 
            raise UnsupportedOperationError("Algorithm not supported. Maybe try without weights?")
        else:
            raise UnsupportedOperationError("Algorithm not supported.")

    if vertex_weights is not None: 
        jgrapht_vertex_weights = JGraphTLongDoubleMap()
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[key] = val
        err, weight, vc_handle = alg_method(graph.handle, jgrapht_vertex_weights.handle)
    else:
        err, weight, vc_handle = alg_method(graph.handle)

    if err: 
        raise_status()

    return weight, JGraphTLongSet(vc_handle)


def greedy(graph, vertex_weights=None):
    return _vertexcover_alg('greedy', graph, vertex_weights)


def clarkson(graph, vertex_weights=None):
    return _vertexcover_alg('clarkson', graph, vertex_weights)


def edgebased(graph, vertex_weights=None):
    return _vertexcover_alg('edgebased', graph, vertex_weights)


def baryehuda_even(graph, vertex_weights=None):
    return _vertexcover_alg('baryehudaeven', graph, vertex_weights)


def exact(graph, vertex_weights=None):
    return _vertexcover_alg('exact', graph, vertex_weights)

