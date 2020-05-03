from .. import backend
from .._errors import raise_status, UnsupportedOperationError
from .._wrappers import JGraphTPlanarEmbedding, JGraphTGraph


def _planarity_alg(name, graph, *args):
    alg_method_name = "jgrapht_planarity_exec_"
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")

    err, is_planar, embedding, kuratowski_subdivision = alg_method(graph.handle, *args)
    if err:
        raise_status()

    if is_planar: 
        return is_planar, JGraphTPlanarEmbedding(embedding)
    else: 
        return is_planar, JGraphTGraph(handle=kuratowski_subdivision)


def boyer_myrvold(graph):
    return _planarity_alg('boyer_myrvold', graph)


def is_planar(graph):
    return boyer_myrvold(graph)
