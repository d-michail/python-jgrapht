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
