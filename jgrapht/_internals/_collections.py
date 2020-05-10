from .. import backend

from ._wrappers import (
    _HandleWrapper,
    _JGraphTObjectIterator,
    _JGraphTLongIterator,
)

from collections.abc import (
    MutableSet,
    Collection,
    MutableMapping,
)


class _JGraphTLongSet(_HandleWrapper, MutableSet):
    """JGraphT Long Set"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_set_linked_create()
            else:
                handle = backend.jgrapht_set_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_set_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_set_long_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_set_long_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTLongSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongSet(super().__next__())

    def __repr__(self):
        return "_JGraphTLongSetIterator(%r)" % self._handle

    
class _JGraphTLongList(_HandleWrapper, Collection):
    """JGraphT Long List"""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_list_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_list_size(self._handle)
        return res

    def add(self, x):
        backend.jgrapht_list_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_list_long_remove(self._handle, x)

    def __contains__(self, x):
        res = backend.jgrapht_list_long_contains(self._handle, x)
        return res

    def clear(self):
        backend.jgrapht_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTLongListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongList(super().__next__())

    def __repr__(self):
        return "_JGraphTLongListIterator(%r)" % self._handle


class _JGraphTLongDoubleMap(_HandleWrapper, MutableMapping):
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
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_long_double_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_long_double_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try: 
            res = backend.jgrapht_map_long_double_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()
            pass

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_double_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_long_double_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        backend.jgrapht_map_long_double_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongDoubleMap(%r)" % self._handle


class _JGraphTLongLongMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with long keys and long values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_map_linked_create()
            else:
                handle = backend.jgrapht_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_long_long_get(self._handle, key)
        return res

    def add(self, key, value):
        backend.jgrapht_map_long_long_put(self._handle, key, value)

    def pop(self, key, defaultvalue):
        try:
            res = backend.jgrapht_map_long_long_remove(self._handle, key)
            return res
        except ValueError:
            if defaultvalue is not None:
                return defaultvalue
            else:
                raise KeyError()

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_long_get(self._handle, key)
        return res

    def __setitem__(self, key, value):
        backend.jgrapht_map_long_long_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_long_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongLongMap(%r)" % self._handle

