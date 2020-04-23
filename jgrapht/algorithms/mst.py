from .. import jgrapht
from .. import errors
from .. import iterator

def _mst_alg(name, graph):
    alg_method_name = 'jgrapht_mst_exec_' + name

    try:
        alg_method = getattr(jgrapht, alg_method_name)
    except AttributeError:
        raise errors.UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, mst_handle = alg_method(graph.handle)
    if err:
        errors.raise_status()
    err, mst_weight = jgrapht.jgrapht_mst_get_weight(mst_handle)
    if err:
        errors.raise_status()
    err, eit_handle = jgrapht.jgrapht_mst_create_eit(mst_handle)
    if err:
        errors.raise_status()
    mst_edges = list(iterator.LongValueIterator(eit_handle))
    err = jgrapht.jgrapht_destroy(mst_handle)
    if err:
        errors.raise_status()
    return (mst_weight, mst_edges)

def mst_kruskal(graph):
    return _mst_alg('kruskal', graph);

def mst_prim(graph):
    return _mst_alg('prim', graph);

def mst_boruvka(graph):
    return _mst_alg('boruvka', graph);
    