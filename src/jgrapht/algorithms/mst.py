from .. import jgrapht
from .. import errors
from .. import iterator

def mst_kruskal(graph):
    mst_handle = jgrapht.jgrapht_mst_exec_kruskal(graph.handle)
    errors.check_last_error()
    mst_weight = jgrapht.jgrapht_mst_get_weight(mst_handle)
    errors.check_last_error()
    eit = iterator.VertexOrEdgeIterator(jgrapht.jgrapht_mst_create_eit(mst_handle))
    mst_edges = list(eit)
    jgrapht.jgrapht_destroy(mst_handle)
    return (mst_weight, mst_edges)

def mst_prim(graph):
    mst_handle = jgrapht.jgrapht_mst_exec_prim(graph.handle)
    errors.check_last_error()
    mst_weight = jgrapht.jgrapht_mst_get_weight(mst_handle)
    errors.check_last_error()
    eit = iterator.VertexOrEdgeIterator(jgrapht.jgrapht_mst_create_eit(mst_handle))
    mst_edges = list(eit)
    jgrapht.jgrapht_destroy(mst_handle)
    return (mst_weight, mst_edges)