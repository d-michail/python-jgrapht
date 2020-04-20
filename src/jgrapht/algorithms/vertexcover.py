from .. import jgrapht
from .. import errors
from .. import iterator

def vertexcover_greedy(graph):
    vc_handle = jgrapht.jgrapht_vertexcover_exec_greedy(graph.handle)
    errors.raise_if_last_error()
    vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    errors.raise_if_last_error()
    vit = iterator.LongValueIterator(jgrapht.jgrapht_vertexcover_create_vit(vc_handle))
    vc_vertices = list(vit)
    jgrapht.jgrapht_destroy(vc_handle)
    errors.raise_if_last_error()
    return (vc_weight, vc_vertices)

def vertexcover_clarkson(graph):
    vc_handle = jgrapht.jgrapht_vertexcover_exec_clarkson(graph.handle)
    errors.raise_if_last_error()
    vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    errors.raise_if_last_error()
    vit = iterator.LongValueIterator(jgrapht.jgrapht_vertexcover_create_vit(vc_handle))
    vc_vertices = list(vit)
    jgrapht.jgrapht_destroy(vc_handle)
    errors.raise_if_last_error()
    return (vc_weight, vc_vertices)

def vertexcover_edgebased(graph):
    vc_handle = jgrapht.jgrapht_vertexcover_exec_edgebased(graph.handle)
    errors.raise_if_last_error()
    vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    errors.raise_if_last_error()
    vit = iterator.LongValueIterator(jgrapht.jgrapht_vertexcover_create_vit(vc_handle))
    vc_vertices = list(vit)
    jgrapht.jgrapht_destroy(vc_handle)
    errors.raise_if_last_error()
    return (vc_weight, vc_vertices)

def vertexcover_baryehudaeven(graph):
    vc_handle = jgrapht.jgrapht_vertexcover_exec_baryehudaeven(graph.handle)
    errors.raise_if_last_error()
    vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    errors.raise_if_last_error()
    vit = iterator.LongValueIterator(jgrapht.jgrapht_vertexcover_create_vit(vc_handle))
    vc_vertices = list(vit)
    jgrapht.jgrapht_destroy(vc_handle)
    errors.raise_if_last_error()
    return (vc_weight, vc_vertices)

def vertexcover_exact(graph):
    vc_handle = jgrapht.jgrapht_vertexcover_exec_exact(graph.handle)
    errors.raise_if_last_error()
    vc_weight = jgrapht.jgrapht_vertexcover_get_weight(vc_handle)
    errors.raise_if_last_error()
    vit = iterator.LongValueIterator(jgrapht.jgrapht_vertexcover_create_vit(vc_handle))
    vc_vertices = list(vit)
    jgrapht.jgrapht_destroy(vc_handle)
    errors.raise_if_last_error()
    return (vc_weight, vc_vertices)
