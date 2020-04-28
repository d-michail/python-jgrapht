from .. import backend
from .._errors import raise_status, UnsupportedOperationError
from .._wrappers import JGraphTLongSetIterator

def _clique_enumeration_alg(name, graph, *args):
    alg_method_name = 'jgrapht_clique_exec_'
    alg_method_name += name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")    

    err, clique_it = alg_method(graph.handle, *args)
    if err: 
        raise_status()

    return JGraphTLongSetIterator(handle=clique_it)


def bron_kerbosch(graph, timeout=0, pivot=True, degeneracy_ordering=True):
    custom = [ timeout ]
    if degeneracy_ordering:
        return _clique_enumeration_alg('bron_kerbosch_pivot_degeneracy_ordering', graph, *custom)
    elif pivot:
        return _clique_enumeration_alg('bron_kerbosch_pivot', graph, *custom)
    else:
        return _clique_enumeration_alg('bron_kerbosch', graph, *custom)