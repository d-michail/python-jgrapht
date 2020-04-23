from .. import jgrapht as backend
from ..errors import raise_status, UnsupportedOperationError
from ..util import JGraphTLongIterator

def _mst_alg(name, graph):
    alg_method_name = 'jgrapht_mst_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, mst_handle = alg_method(graph.handle)
    if err:
        raise_status()
    err, mst_weight = backend.jgrapht_mst_get_weight(mst_handle)
    if err:
        raise_status()
    err, eit_handle = backend.jgrapht_mst_create_eit(mst_handle)
    if err:
        raise_status()
    mst_edges = list(JGraphTLongIterator(eit_handle))
    err = backend.jgrapht_destroy(mst_handle)
    if err:
        raise_status()
    return (mst_weight, mst_edges)

def mst_kruskal(graph):
    return _mst_alg('kruskal', graph);

def mst_prim(graph):
    return _mst_alg('prim', graph);

def mst_boruvka(graph):
    return _mst_alg('boruvka', graph);
    