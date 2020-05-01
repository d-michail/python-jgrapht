import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath

def _export_to_file(name, graph, filename, *args):
    alg_method_name = 'jgrapht_export_file_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err = alg_method(graph.handle, filename, *args)
    if err:
        raise_status()


DIMACS_FORMATS = dict({ 'shortestpath': backend.DIMACS_FORMAT_SHORTEST_PATH, 
                   'maxclique': backend.DIMACS_FORMAT_MAX_CLIQUE, 
                   'coloring' : backend.DIMACS_FORMAT_COLORING 
})


def dimacs(graph, filename, format="shortestpath"):
    format = DIMACS_FORMATS.get(format, backend.DIMACS_FORMAT_SHORTEST_PATH)
    custom = [ format ]
    return _export_to_file('dimacs', graph, filename, *custom)


def gml(graph, filename, export_edge_weights, vertex_label_cb, edge_label_cb=None):

    # a ctypes callback prototype
    #callback_type = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_longlong)

    # wrap the python callback with a ctypes function pointer
    #f = callback_type(vertex_label_cb)

    # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
    #f_ptr = ctypes.cast(f, ctypes.c_void_p).value

    #print("Function pointer value: {}, type {}".format(f_ptr, type(f_ptr)))

    #err = backend.jgrapht_export_file_gml(graph.handle, filename, export_edge_weights, f_ptr, None)
    #if err:
    #    raise_status()

    pass

