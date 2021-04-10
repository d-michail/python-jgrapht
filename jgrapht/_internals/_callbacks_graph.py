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


def _create_import_id_wrapper(graph, callback, integer_input_ids=False):
    if callback is None:
        return _callbacks._CallbackWrapper(callback, callback_type=None)

    if integer_input_ids:
        if graph._backend_type == GraphBackend.INT_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
        elif graph._backend_type == GraphBackend.LONG_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_longlong)
        elif graph._backend_type == GraphBackend.REF_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(
                ctypes.ctypes.py_object, ctypes.c_longlong
            )
        else:
            raise ValueError("Backend type invalid")
        return _callbacks._CallbackWrapper(callback, callback_ctype)
    else:
        if graph._backend_type == GraphBackend.INT_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        elif graph._backend_type == GraphBackend.LONG_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_char_p)
        elif graph._backend_type == GraphBackend.REF_GRAPH:
            callback_ctype = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.c_char_p)
        else:
            raise ValueError("Backend type invalid")

        # We wrap in order to decode string representation.
        # There is no SWIG layer here, as the capi calls us directly
        # using a function pointer. This means that the arguments
        # are bytearrays.
        def decoder_callback(id):
            decoded_id = id.decode(encoding="utf-8")
            return callback(decoded_id)

        return _callbacks._CallbackWrapper(decoder_callback, callback_ctype)


def _create_attribute_callback_wrapper(graph, callback):
    if callback is None:
        return _callbacks._CallbackWrapper(callback, callback_type=None)

    if graph._backend_type == GraphBackend.INT_GRAPH:
        id_type = ctypes.c_int
    elif graph._backend_type == GraphBackend.LONG_GRAPH:
        id_type = ctypes.c_longlong
    elif graph._backend_type == GraphBackend.REF_GRAPH:
        id_type = ctypes.py_object
    else:
        raise ValueError("Backend type invalid")

    callback_ctype = ctypes.CFUNCTYPE(
        None, id_type, ctypes.c_char_p, ctypes.c_char_p
    )

    # We wrap in order to decode string representation.
    # There is no SWIG layer here, as the capi calls us directly
    # using a function pointer. This means that the arguments
    # are bytearrays.
    def decoder_callback(id, key, value):
        decoded_key = key.decode(encoding="utf-8")
        decoded_value = value.decode(encoding="utf-8")
        callback(id, decoded_key, decoded_value)

    return _callbacks._CallbackWrapper(decoder_callback, callback_ctype)    


def _create_notify_id_callback_wrapper(graph, callback):
    if callback is None:
        return _callbacks._CallbackWrapper(callback, callback_type=None)

    if graph._backend_type == GraphBackend.INT_GRAPH:
        id_type = ctypes.c_int
    elif graph._backend_type == GraphBackend.LONG_GRAPH:
        id_type = ctypes.c_longlong
    elif graph._backend_type == GraphBackend.REF_GRAPH:
        id_type = ctypes.py_object
    else:
        raise ValueError("Backend type invalid")

    callback_ctype = ctypes.CFUNCTYPE(None, id_type)
    return _callbacks._CallbackWrapper(callback, callback_ctype)    
