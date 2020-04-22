from .. import jgrapht
from .. import errors
from .. import iterator

def mst_kruskal(graph):
    err, mst_handle = jgrapht.jgrapht_mst_exec_kruskal(graph.handle)
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


def mst_prim(graph):
    err, mst_handle = jgrapht.jgrapht_mst_exec_prim(graph.handle)
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