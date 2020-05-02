import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath, JGraphTAttributeStore

def _import_from_file(name, graph, filename, *args):
    alg_method_name = 'jgrapht_import_file_' + name

    try:
        alg_method = getattr(backend, alg_method_name)
    except AttributeError:
        raise UnsupportedOperationError('Algorithm {} not supported.'.format(name))

    err = alg_method(graph.handle, filename, *args)
    if err:
        raise_status()


def _create_wrapped_callback(callback):
    if callback is not None:
        # wrap the python callback with a ctypes function pointer
        f = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)(callback)

        # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
        # we perform the reverse using typemaps on the SWIG layer
    
        f_ptr = ctypes.cast(f, ctypes.c_void_p).value

        # make sure to also return the callback to avoid garbage collection
        return (f_ptr, f)
    return (0, None)

def read_dimacs(graph, filename): 
    return _import_from_file('dimacs', graph, filename)


def read_gml(graph, filename, vertex_attribute_cb=None, edge_attribute_cb=None):
    vertex_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb)
    edge_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb)

    args = [ vertex_f_ptr, edge_f_ptr ]
    return _import_from_file('gml', graph, filename, *args)


def read_json(graph, filename, vertex_attribute_cb=None, edge_attribute_cb=None):
    vertex_f_ptr, _ = _create_wrapped_callback(vertex_attribute_cb)
    edge_f_ptr, _ = _create_wrapped_callback(edge_attribute_cb)

    args = [ vertex_f_ptr, edge_f_ptr ]
    return _import_from_file('json', graph, filename, *args)
