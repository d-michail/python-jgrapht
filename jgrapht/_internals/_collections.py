from .. import backend

from ._wrappers import (
    _HandleWrapper,
    _JGraphTObjectIterator,
    _JGraphTIntegerIterator,
)

from collections.abc import (
    MutableSet,
    Collection,
    MutableMapping,
)


class _JGraphTIntegerSet(_HandleWrapper, MutableSet):
    """JGraphT Integer Set"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_set_linked_create()
            else:
                handle = backend.jgrapht_set_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_set_int_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_set_int_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_set_int_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTIntegerSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerSet(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerSetIterator(%r)" % self._handle

    
class _JGraphTIntegerList(_HandleWrapper, Collection):
    """JGraphT Integer List"""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_list_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_list_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_list_int_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_list_int_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_list_int_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTIntegerListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with integers."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerList(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerListIterator(%r)" % self._handle


class _JGraphTIntegerDoubleMap(_HandleWrapper, MutableMapping):
    """JGraphT Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_map_linked_create()
            else:
                handle = backend.jgrapht_map_create()
            owner = True
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_int_double_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_int_double_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try: 
            res = backend.jgrapht_map_int_double_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()
            pass

    def __contains__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_double_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_int_double_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        backend.jgrapht_map_int_double_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerDoubleMap(%r)" % self._handle


class _JGraphTIntegerIntegerMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with integer keys and integer values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_map_linked_create()
            else:
                handle = backend.jgrapht_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_int_int_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_int_int_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try:
            res = backend.jgrapht_map_int_int_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()

    def __contains__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_int_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_int_int_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_int_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerIntegerMap(%r)" % self._handle

