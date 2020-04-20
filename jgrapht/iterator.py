from . import jgrapht
from . import errors

class LongValueIterator: 
    """Long values iterator"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    def __iter__(self):
        return self

    def __next__(self):
        has_next = jgrapht.jgrapht_it_hasnext(self._handle)
        errors.raise_if_last_error()
        if not has_next: 
            raise StopIteration()
        e = jgrapht.jgrapht_it_next_long(self._handle)
        errors.raise_if_last_error()
        return e

    def __del__(self):
        if self._owner and jgrapht.jgrapht_is_thread_attached():
            errors.raise_if_last_error()
            jgrapht.jgrapht_destroy(self._handle) 
            errors.raise_if_last_error()


class DoubleValueIterator: 
    """Double values iterator"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    def __iter__(self):
        return self

    def __next__(self):
        has_next = jgrapht.jgrapht_it_hasnext(self._handle)
        errors.raise_if_last_error()
        if not has_next: 
            raise StopIteration()
        e = jgrapht.jgrapht_it_next_double(self._handle)
        errors.raise_if_last_error()
        return e

    def __del__(self):
        if self._owner and jgrapht.jgrapht_is_thread_attached():
            errors.raise_if_last_error()
            jgrapht.jgrapht_destroy(self._handle) 
            errors.raise_if_last_error()
