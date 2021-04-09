import ctypes

from .. import GraphBackend
from . import _callbacks


def _create_vertex_comparator_wrapper(graph, callback):
    if callback is None:
        return _callbacks._CallbackWrapper(callback, callback_type=None)

    if graph._backend_type == GraphBackend.INT_GRAPH:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
    elif graph._backend_type == GraphBackend.LONG_GRAPH:
        callback_ctype = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong
        )
    elif graph._backend_type == GraphBackend.REF_GRAPH:
        callback_ctype = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.py_object, ctypes.py_object
        )
    else:
        raise ValueError("Backend type invalid")

    return _callbacks._CallbackWrapper(callback, callback_ctype)

