from .. import jgrapht as backend
from ..errors import raise_status, UnsupportedOperationError
from ..util import JGraphTLongSet


def _mst_alg(name, graph):
    alg_method_name = 'jgrapht_mst_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err, weight, mst_handle = alg_method(graph.handle)
    if err:
        raise_status()

    return weight, JGraphTLongSet(mst_handle)


def mst_kruskal(graph):
    return _mst_alg('kruskal', graph);


def mst_prim(graph):
    return _mst_alg('prim', graph);


def mst_boruvka(graph):
    return _mst_alg('boruvka', graph);
    