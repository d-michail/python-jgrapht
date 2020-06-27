import ctypes


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


def _create_wrapped_vertex_comparator_callback(callback):
    """Create a wrapper callback for a vertex comparator. This means
    that the function should accept two integers and return an integer.
    """
    if callback is not None:
        callback_ctype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
        return _create_wrapped_callback(callback, callback_ctype)
    else:
        return (0, None)
