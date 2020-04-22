from . import jgrapht
from . import errors
from . import iterator

class LongSet:
    """Graph Element Set"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None: 
            err, res = jgrapht.jgrapht_set_create()
            if err: 
                errors.raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached():
            err = jgrapht.jgrapht_destroy(self._handle)
            if err:
                errors.raise_status() 

    @property
    def handle(self):
        return self._handle;

    def __iter__(self):
        err, res = jgrapht.jgrapht_set_it_create(self._handle)
        if err: 
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def __len__(self):
        err, res = jgrapht.jgrapht_set_size(self._handle)
        if err: 
            errors.raise_status()
        return res

    def add(self, x):
        err = jgrapht.jgrapht_set_long_add(self._handle, x)
        if err: 
            errors.raise_status()

    def remove(self, x):
        err, res = jgrapht.jgrapht_set_long_contains(self._handle, x)
        if err: 
            errors.raise_status()
        if not res: 
            raise KeyError()
        err = jgrapht.jgrapht_set_long_remove(self._handle, x)
        if err: 
            errors.raise_status()

    def discard(self, x):
        err, res = jgrapht.jgrapht_set_long_remove(self._handle, x)
        if err: 
            errors.raise_status()            

    def __contains__(self, x):
        err, res = jgrapht.jgrapht_set_long_contains(self._handle, x)
        if err: 
            errors.raise_status()
        return res

    def clear(self): 
        err, res = jgrapht.jgrapht_set_long_clear(self._handle)
        if err: 
            errors.raise_status()
