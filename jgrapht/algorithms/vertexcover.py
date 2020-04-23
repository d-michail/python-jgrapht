from .. import jgrapht
from .. import errors
from .. import iterator
from .. import util

def _vertexcover_alg(name, graph, vertex_weights=None):

    alg_method_name = 'jgrapht_vertexcover_exec_' + name
    if vertex_weights is not None: 
        alg_method_name += '_weighted'

    try:
        alg_method = getattr(jgrapht, alg_method_name)
    except AttributeError:
        if vertex_weights is not None: 
            raise errors.UnsupportedOperationError("Algorithm not supported. Maybe try without weights?")
        else:
            raise errors.UnsupportedOperationError("Algorithm not supported.")

    if vertex_weights is not None: 
        jgrapht_vertex_weights = util.JGraphTLongDoubleMap()
        for key, val in vertex_weights.items():
            jgrapht_vertex_weights[key] = val
        err, vc_handle = alg_method(graph.handle, jgrapht_vertex_weights.handle)
    else:
        err, vc_handle = alg_method(graph.handle)

    if err: 
        errors.raise_status()

    err, vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    if err:
        errors.raise_status()

    err, vc_vit_handle = jgrapht.jgrapht_vertexcover_create_vit(vc_handle)
    if err:
        errors.raise_status()

    vc_vertices = list(iterator.LongValueIterator(vc_vit_handle))

    jgrapht.jgrapht_destroy(vc_handle)
    if err:
        errors.raise_status()

    return (vc_weight, vc_vertices)


def vertexcover_greedy(graph, vertex_weights=None):
    return _vertexcover_alg('greedy', graph, vertex_weights)

def vertexcover_clarkson(graph, vertex_weights=None):
    return _vertexcover_alg('clarkson', graph, vertex_weights)

def vertexcover_edgebased(graph, vertex_weights=None):
    return _vertexcover_alg('edgebased', graph, vertex_weights)

def vertexcover_baryehuda_even(graph, vertex_weights=None):
    return _vertexcover_alg('baryehudaeven', graph, vertex_weights)

def vertexcover_exact(graph, vertex_weights=None):
    return _vertexcover_alg('exact', graph, vertex_weights)

