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
        err, res = jgrapht.jgrapht_it_hasnext(self._handle)
        if err: 
            errors.raise_status()
        if not res: 
            raise StopIteration()
        err, res = jgrapht.jgrapht_it_next_long(self._handle)
        if err: 
            errors.raise_status()
        return res

    def __del__(self):
        if self._owner and jgrapht.jgrapht_is_thread_attached():
            err = jgrapht.jgrapht_destroy(self._handle)
            if err: 
                errors.raise_status() 


class DoubleValueIterator: 
    """Double values iterator"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    def __iter__(self):
        return self

    def __next__(self):
        err, res = jgrapht.jgrapht_it_hasnext(self._handle)
        if err: 
            errors.raise_status()
        if not res: 
            raise StopIteration()
        err, res = jgrapht.jgrapht_it_next_double(self._handle)
        if err: 
            errors.raise_status()
        return res

    def __del__(self):
        if self._owner and jgrapht.jgrapht_is_thread_attached():
            err = jgrapht.jgrapht_destroy(self._handle) 
            if err: 
                errors.raise_status() 
