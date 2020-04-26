from . import backend
from ._errors import raise_status, Status

class JGraphTLongIterator: 
    """Long values iterator"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    def __iter__(self):
        return self

    def __next__(self):
        err, res = backend.jgrapht_it_hasnext(self._handle)
        if err: 
            raise_status()
        if not res: 
            raise StopIteration()
        err, res = backend.jgrapht_it_next_long(self._handle)
        if err: 
            raise_status()
        return res

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle)
            if err: 
                raise_status() 


class JGraphTDoubleIterator: 
    """Double values iterator"""
    def __init__(self, handle, owner=True):
        self._handle = handle
        self._owner = owner

    def __iter__(self):
        return self

    def __next__(self):
        err, res = backend.jgrapht_it_hasnext(self._handle)
        if err: 
            raise_status()
        if not res: 
            raise StopIteration()
        err, res = backend.jgrapht_it_next_double(self._handle)
        if err: 
            raise_status()
        return res

    def __del__(self):
        if self._owner and backend.jgrapht_is_thread_attached():
            err = backend.jgrapht_destroy(self._handle) 
            if err: 
                raise_status() 


class JGraphTLongSet:
    """JGraphT Long Set"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, res = backend.jgrapht_set_linked_create()
            else: 
                err, res = backend.jgrapht_set_create()
            if err: 
                raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if backend.jgrapht_is_thread_attached() and self._owner:
            err = backend.jgrapht_destroy(self._handle)
            if err:
                raise_status() 

    @property
    def handle(self):
        return self._handle

    def __iter__(self):
        err, res = backend.jgrapht_set_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_set_size(self._handle)
        if err: 
            raise_status()
        return res

    def add(self, x):
        err, _ = backend.jgrapht_set_long_add(self._handle, x)
        if err: 
            raise_status()

    def remove(self, x):
        err, res = backend.jgrapht_set_long_contains(self._handle, x)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err = backend.jgrapht_set_long_remove(self._handle, x)
        if err: 
            raise_status()

    def discard(self, x):
        err = backend.jgrapht_set_long_remove(self._handle, x)
        if err: 
            raise_status()            

    def __contains__(self, x):
        err, res = backend.jgrapht_set_long_contains(self._handle, x)
        if err: 
            raise_status()
        return res

    def clear(self): 
        err = backend.jgrapht_set_clear(self._handle)
        if err: 
            raise_status()


class JGraphTLongDoubleMap:
    """JGraphT Map"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, res = backend.jgrapht_map_linked_create()
            else: 
                err, res = backend.jgrapht_map_create()
            if err: 
                raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if backend.jgrapht_is_thread_attached() and self._owner:
            err = backend.jgrapht_destroy(self._handle)
            if err:
                raise_status() 

    @property
    def handle(self):
        return self._handle

    def __iter__(self):
        err, res = backend.jgrapht_map_keys_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_map_size(self._handle)
        if err: 
            raise_status()
        return res

    def get(self, key, value=None):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            if value is not None: 
                return value
            else: 
                raise KeyError()
        err, res = backend.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def add(self, key, value):
        err = backend.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            raise_status()

    def pop(self, key, defaultvalue):
        err, res = backend.jgrapht_map_long_double_remove(self._handle, key)
        if err:
            if err == Status.ILLEGAL_ARGUMENT.value:
                # key not found in map
                backend.jgrapht_clear_errno()
                if defaultvalue is not None:
                    return defaultvalue 
                else: 
                    raise KeyError()
            else:
                raise_status()
        return res

    def __contains__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        return res

    def __getitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def __setitem__(self, key, value):
        err = backend.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            raise_status()

    def __delitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_double_remove(self._handle, key)
        if err: 
            raise_status()

    def clear(self): 
        err = backend.jgrapht_map_clear(self._handle)
        if err: 
            raise_status()


class JGraphTLongLongMap:
    """JGraphT Map with long keys and long values"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, res = backend.jgrapht_map_linked_create()
            else: 
                err, res = backend.jgrapht_map_create()
            if err: 
                raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if backend.jgrapht_is_thread_attached() and self._owner:
            err = backend.jgrapht_destroy(self._handle)
            if err:
                raise_status() 

    @property
    def handle(self):
        return self._handle

    def __iter__(self):
        err, res = backend.jgrapht_map_keys_it_create(self._handle)
        if err: 
            raise_status()
        return JGraphTLongIterator(res)

    def __len__(self):
        err, res = backend.jgrapht_map_size(self._handle)
        if err: 
            raise_status()
        return res

    def get(self, key, value=None):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            if value is not None: 
                return value
            else: 
                raise KeyError()
        err, res = backend.jgrapht_map_long_long_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def add(self, key, value):
        err = backend.jgrapht_map_long_long_put(self._handle, key, value)
        if err: 
            raise_status()

    def pop(self, key, defaultvalue):
        err, res = backend.jgrapht_map_long_long_remove(self._handle, key)
        if err:
            if err == Status.ILLEGAL_ARGUMENT.value:
                # key not found in map
                backend.jgrapht_clear_errno()
                if defaultvalue is not None:
                    return defaultvalue 
                else: 
                    raise KeyError()
            else:
                raise_status()
        return res

    def __contains__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        return res

    def __getitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_long_get(self._handle, key)
        if err: 
            raise_status()
        return res

    def __setitem__(self, key, value):
        err = backend.jgrapht_map_long_long_put(self._handle, key, value)
        if err: 
            raise_status()

    def __delitem__(self, key):
        err, res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if err: 
            raise_status()
        if not res: 
            raise KeyError()
        err, res = backend.jgrapht_map_long_long_remove(self._handle, key)
        if err: 
            raise_status()

    def clear(self): 
        err = backend.jgrapht_map_clear(self._handle)
        if err: 
            raise_status()


