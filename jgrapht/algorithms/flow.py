from .. import backend
from .._errors import raise_status, UnsupportedOperationError
from .._wrappers import JGraphTCut, JGraphTFlow

def _maxflow_alg(name, graph, source, sink, *args):

    alg_method_name = 'jgrapht_maxflow_exec_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError("Algorithm not supported.")    

    err, flow_value, flow_handle, cut_source_partition_handle = alg_method(graph.handle, source, sink, *args)
    if err: 
        raise_status()

    flow = JGraphTFlow(flow_handle, source, sink, flow_value)
    cut = JGraphTCut(graph, flow_value, cut_source_partition_handle)

    return flow, cut

def dinic(graph, source, sink):
    return _maxflow_alg('dinic', graph, source, sink)


def push_relabel(graph, source, sink):
    return _maxflow_alg('push_relabel', graph, source, sink)


def edmonds_karp(graph, source, sink):
    return _maxflow_alg('edmonds_karp', graph, source, sink)