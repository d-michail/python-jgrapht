import time
import ctypes

from .. import backend
from ..exceptions import UnsupportedOperationError
from .._errors import raise_status
from .._wrappers import JGraphTLongIterator, JGraphTGraphPath, JGraphTAttributeStore


def read_gml(graph, filename, vertex_attribute_cb=None, edge_attribute_cb=None):

    # a ctypes callback prototype
    cb_type = ctypes.CFUNCTYPE(None, ctypes.c_longlong, ctypes.c_char_p, ctypes.c_char_p)
    
    # wrap the python callback with a ctypes function pointer
    vertex_f = cb_type(vertex_attribute_cb)
    edge_f = cb_type(edge_attribute_cb)

    # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
    vertex_f_ptr = ctypes.cast(vertex_f, ctypes.c_void_p).value
    edge_f_ptr = ctypes.cast(edge_f, ctypes.c_void_p).value

    err = backend.jgrapht_import_file_gml(graph.handle, filename, vertex_f_ptr, edge_f_ptr)
    if err:
        raise_status()

