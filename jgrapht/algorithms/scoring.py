from .. import jgrapht
from .. import errors
from .. import iterator
from .. import util

def _scoring_alg(name, graph, **kwargs):

    alg_method_name = 'jgrapht_scoring_exec_'
    if kwargs:
        alg_method_name += 'custom_'
    alg_method_name += name

    try:
        alg_method = getattr(jgrapht, alg_method_name)
    except AttributeError:
        raise errors.UnsupportedOperationError("Algorithm not supported.")    

    err, scores_handle = alg_method(graph.handle)
    if err: 
        errors.raise_status()

    return util.JGraphTLongDoubleMap(handle=scores_handle)


def scoring_harmonic_centrality(graph):
    return _scoring_alg('harmonic_centrality', graph)

def scoring_pagerank(graph):
    return _scoring_alg('pagerank', graph)


