from collections.abc import Set

from .. import backend

import ctypes
from . import _callbacks
from ._wrappers import _HandleWrapper

__hash_equals_wrapper = None
__hash_fptr_wrapper = None
__equals_fptr_wrapper = None


def _get_hash_fptr_wrapper():
    global __hash_fptr_wrapper
    if __hash_fptr_wrapper is None:
        hash_type = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.py_object)
        __hash_fptr_wrapper = _callbacks._CallbackWrapper(hash, hash_type)
    return __hash_fptr_wrapper


def _hash_lookup(o):
    return _get_hash_fptr_wrapper().fptr


def _get_equals_fptr_wrapper():
    global __equals_fptr_wrapper
    if __equals_fptr_wrapper is None:

        def _equals(o1, o2):
            return o1 == o2

        equals_type = ctypes.CFUNCTYPE(
            ctypes.c_long, ctypes.py_object, ctypes.py_object
        )
        __equals_fptr_wrapper = _callbacks._CallbackWrapper(_equals, equals_type)
    return __equals_fptr_wrapper


def _equals_lookup(o):
    return _get_equals_fptr_wrapper().fptr


class _HashEqualsWrapper(_HandleWrapper):
    
    def __init__(self):
        self._hash_lookup_fptr_wrapper = _callbacks._CallbackWrapper(
            _hash_lookup, ctypes.CFUNCTYPE(ctypes.c_long, ctypes.py_object)
        )
        self._equals_lookup_fptr_wrapper = _callbacks._CallbackWrapper(
            _equals_lookup, ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.py_object)
        )

        handle = backend.jgrapht_rr_graph_hash_equals_resolver_create(
            self._hash_lookup_fptr_wrapper.fptr, self._equals_lookup_fptr_wrapper.fptr
        )

        super().__init__(handle)


def _get_hash_equals_wrapper():
    global __hash_equals_wrapper
    if __hash_equals_wrapper is None:
        __hash_equals_wrapper = _HashEqualsWrapper()
    return __hash_equals_wrapper