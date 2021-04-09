import ctypes

def _fallback_py_object_supplier():
    return object()


class _CallbackWrapper:

    def __init__(self, callback, callback_type):
        if callback is None:
            self._cb = None
            self._f = None
            self._f_ptr = 0
        else:
            self._cb = callback
            self._f = callback_type(callback)
            self._f_ptr = ctypes.cast(self._f, ctypes.c_void_p).value 

    @property
    def fptr(self):
        return self._f_ptr


def _create_py_object_supplier(supplier):
    """Create a callback wrapper around an object supplier. The wrapper 
    keeps a reference to the callback to avoid garbage collection. It also 
    provides the ctypes pointer for the callback.
    """
    if supplier is None:
        supplier = _fallback_py_object_supplier
    supplier_type = ctypes.CFUNCTYPE(ctypes.py_object)
    supplier_fptr_wrapper = _CallbackWrapper(
        supplier, supplier_type
    )
    return supplier_fptr_wrapper


def _create_wrapped_callback(callback, cfunctype):
    if callback is not None:
        # wrap the python callback with a ctypes function pointer
        f = cfunctype(callback)

        # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
        # we perform the reverse using typemaps on the SWIG layer
        f_ptr = ctypes.cast(f, ctypes.c_void_p).value

        # make sure to also return the callback to avoid garbage collection
        return (f_ptr, f)
    return (0, None)


def _create_wrapped_int_vertex_comparator_callback(callback):
    """Create a wrapper callback for a vertex comparator. This means
    that the function should accept two integers and return an integer.
    """
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_long_vertex_comparator_callback(callback):
    """Create a wrapper callback for a vertex comparator. This means
    that the function should accept two longs and return an integer.
    """
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)


def _create_wrapped_long_supplier_callback(callback):
    """Create a wrapper callback for a vertex/edge supplier callback. This means
    that the function should take no arguments and return a long.
    """
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_longlong)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)

