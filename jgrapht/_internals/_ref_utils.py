import ctypes
import sys

_c_inc_ref = ctypes.pythonapi.Py_IncRef
_c_inc_ref.argtypes = [ctypes.py_object]
_c_dec_ref = ctypes.pythonapi.Py_DecRef
_c_dec_ref.argtypes = [ctypes.py_object]


def _inc_ref(obj):
    """Increase the reference count of an object by one."""
    _c_inc_ref(obj)


def _inc_ref_by_id(id):
    """Increase the reference count of an object given by its id."""
    _c_inc_ref(_id_to_obj(id))


def _dec_ref(obj):
    """Decrease the reference count of an object by one."""
    _c_dec_ref(obj)


def _dec_ref_by_id(id):
    """Decrease the reference count of an object given by its id."""
    _c_dec_ref(_id_to_obj(id))


def _ref_count(obj, normalize=True):
    """Get the reference count of an object"""
    count = sys.getrefcount(obj)
    if normalize:
        # remove function argument, getrefcount temporary reference and function stack
        return count - 3


def _id_to_obj(id):
    """Cast an id to an object. Note that this method if
    called on a non-existent object, will crash Python.
    """
    return ctypes.cast(id, ctypes.py_object).value


def _map_ids_to_objs(iterable):
    """Map an iterable of ids to an iterator of objects."""
    return map(lambda item_id: _id_to_obj(item_id), iterable)


def _swig_ptr_to_obj(swig_ptr):
    """Cast a Swig pointer to an object. Assumes that the swig pointer points
    to a valid python object. Otherwise Python will crash.
    """
    id = int(swig_ptr)
    return ctypes.cast(id, ctypes.py_object).value


def _id_comparator(a_id, b_id):
    """A comparator which accepts as input the ids of two python objects
    and compares them.
    """
    a = _id_to_obj(a_id)
    b = _id_to_obj(b_id)

    if a.__lt__(b):
        return -1
    if a.__eq__(b):
        return 0
    return 1


def _create_wrapped_id_comparator_callback(callback):
    if callback is not None:
        # wrap the comparator with a ctypes function pointer
        callback_type = ctypes.CFUNCTYPE(
            ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong
        )
        f = callback_type(callback)

        # get the function pointer of the ctypes wrapper by casting it to void* and taking its value
        # we perform the reverse using typemaps on the SWIG layer
        f_ptr = ctypes.cast(f, ctypes.c_void_p).value

        # make sure to also return the callback to avoid garbage collection
        return (f_ptr, f)
    else:
        return (0, None)


class _SingleRefCount:
    def __init__(self):
        self._objects = set()

    def inc(self, element):
        if element in self._objects:
            raise ValueError("Object is already kept")
        self._objects.add(element)

    def dec(self, element):
        self._objects.remove(element)

    def dec_all(self):
        self._objects.clear()
