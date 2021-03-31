from .. import backend

from . import _ref_utils, _ref_hashequals
from ._wrappers import (
    _HandleWrapper,
    _JGraphTString,
    _JGraphTObjectIterator,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
    _JGraphTEdgeLongTripleIterator,
    _JGraphTEdgeIntegerTripleIterator,
    _JGraphTEdgeStrTripleIterator,
    _JGraphTRefIterator,
    _JGraphTRefDirectIterator,
)

from collections.abc import (
    Set,
    MutableSet,
    Collection,
    Mapping,
    MutableMapping,
    Iterable,
    Sized,
)


class _JGraphTIntegerSet(_HandleWrapper, Set):
    """JGraphT Integer Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_set_int_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTIntegerSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTIntegerMutableSet(_JGraphTIntegerSet, MutableSet):
    """JGraphT Integer Mutable Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_set_int_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_set_int_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return MutableSet(it)


class _JGraphTIntegerSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerSet(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerSetIterator(%r)" % self._handle


class _JGraphTLongSet(_HandleWrapper, Set):
    """JGraphT Long Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_set_long_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTLongSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTLongMutableSet(_JGraphTLongSet, MutableSet):
    """JGraphT Long Mutable Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_set_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_set_long_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return MutableSet(it)


class _JGraphTLongSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongSet(super().__next__())

    def __repr__(self):
        return "_JGraphTLongSetIterator(%r)" % self._handle


class _JGraphTRefSet(_HandleWrapper, Set):
    """JGraphT Ref Set"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _JGraphTRefDirectIterator(res)

    def __len__(self):
        res = backend.jgrapht_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_set_ref_contains_direct(
            self._handle, id(x), self._hash_equals_resolver_handle
        )
        return res

    def __repr__(self):
        return "_JGraphTRefSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTRefMutableSet(_JGraphTRefSet, MutableSet):
    """JGraphT Ref Mutable Set"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

    def add(self, x):
        if backend.jgrapht_set_ref_add_direct(
            self._handle, id(x), self._hash_equals_resolver_handle
        ):
            _ref_utils._inc_ref(x)

    def discard(self, x):
        if backend.jgrapht_set_ref_remove_direct(
            self._handle, id(x), self._hash_equals_resolver_handle
        ):
            _ref_utils._dec_ref(x)

    def clear(self):
        # cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        backend.jgrapht_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return MutableSet(it)

    def __del__(self):
        # Cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        super().__del__()


class _JGraphTRefSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with refs."""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __next__(self):
        return _JGraphTRefSet(
            handle=super().__next__(),
            hash_equals_resolver_handle=self._hash_equals_resolver_handle,
        )

    def __repr__(self):
        return "_JGraphTRefSetIterator(%r)" % self._handle


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

    def __contains__(self, x):
        res = backend.jgrapht_list_int_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTIntegerList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTIntegerMutableList(_JGraphTIntegerList):
    """JGraphT Integer List"""

    def __init__(self, handle=None, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_list_int_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_list_int_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerMutableList(%r)" % self._handle


class _JGraphTIntegerListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with integers."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerList(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerListIterator(%r)" % self._handle


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

    def __contains__(self, x):
        res = backend.jgrapht_list_long_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTLongList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTLongMutableList(_JGraphTLongList):
    """JGraphT Long List"""

    def __init__(self, handle=None, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_list_long_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_list_long_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongMutableList(%r)" % self._handle


class _JGraphTLongListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongList(super().__next__())

    def __repr__(self):
        return "_JGraphTLongListIterator(%r)" % self._handle


class _JGraphTIntegerDoubleMap(_HandleWrapper, Mapping):
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

    def __contains__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_double_get(self._handle, key)
        return res

    def __repr__(self):
        return "_JGraphTIntegerDoubleMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTIntegerDoubleMutableMap(_JGraphTIntegerDoubleMap, MutableMapping):
    """JGraphT Mutable Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        super().__init__(handle=handle, linked=linked, **kwargs)

    def add(self, key, value):
        backend.jgrapht_map_int_double_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_map_int_double_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

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
        return "_JGraphTIntegerDoubleMutableMap(%r)" % self._handle


class _JGraphTIntegerIntegerMap(_HandleWrapper, Mapping):
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

    def __contains__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_int_get(self._handle, key)
        return res

    def __repr__(self):
        return "_JGraphTIntegerIntegerMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTIntegerIntegerMutableMap(_JGraphTIntegerIntegerMap, MutableMapping):
    """JGraphT Mutable Map with integer keys and integer values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        super().__init__(handle=handle, linked=linked, **kwargs)

    def add(self, key, value):
        backend.jgrapht_map_int_int_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_map_int_int_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

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
        return "_JGraphTIntegerIntegerMutableMap(%r)" % self._handle


class _JGraphTIntegerStringMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with integer keys and string values"""

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

    __marker = object()

    def get(self, key, value=__marker):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res = backend.jgrapht_map_int_string_get(self._handle, key)
        return _JGraphTString(res)

    def add(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_map_int_string_put(self._handle, key, encoded_value)

    def pop(self, key, defaultvalue=__marker):
        try:
            res = backend.jgrapht_map_int_string_remove(self._handle, key)
            return _JGraphTString(res)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_string_get(self._handle, key)
        return _JGraphTString(res)

    def __setitem__(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_map_int_string_put(self._handle, key, encoded_value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_int_string_remove(self._handle, key)
        return _JGraphTString(res)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerStringMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTLongIntegerMap(_HandleWrapper, Mapping):
    """JGraphT Map with long keys and integer values"""

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
        res = backend.jgrapht_map_long_int_get(self._handle, key)
        return res

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_int_get(self._handle, key)
        return res

    def __repr__(self):
        return "_JGraphTLongIntegerMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTLongIntegerMutableMap(_JGraphTLongIntegerMap, MutableMapping):
    """JGraphT Mutable Map with long keys and integer values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        super().__init__(handle=handle, linked=linked, **kwargs)

    def add(self, key, value):
        backend.jgrapht_map_long_int_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_map_long_int_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        backend.jgrapht_map_long_int_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_int_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongIntegerMutableMap(%r)" % self._handle


class _JGraphTLongDoubleMap(_HandleWrapper, Mapping):
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

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_double_get(self._handle, key)
        return res

    def __repr__(self):
        return "_JGraphTLongDoubleMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTLongDoubleMutableMap(_JGraphTLongDoubleMap, MutableMapping):
    """JGraphT Mutable Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        super().__init__(handle=handle, linked=linked, **kwargs)

    def add(self, key, value):
        backend.jgrapht_map_long_double_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_map_long_double_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

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
        return "_JGraphTLongDoubleMutableMap(%r)" % self._handle


class _JGraphTLongStringMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with long keys and string values"""

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

    __marker = object()

    def get(self, key, value=__marker):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res = backend.jgrapht_map_long_string_get(self._handle, key)
        return _JGraphTString(res)

    def add(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_map_long_string_put(self._handle, key, encoded_value)

    def pop(self, key, defaultvalue=__marker):
        try:
            res = backend.jgrapht_map_long_string_remove(self._handle, key)
            return _JGraphTString(res)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_string_get(self._handle, key)
        return _JGraphTString(res)

    def __setitem__(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_map_long_string_put(self._handle, key, encoded_value)

    def __delitem__(self, key):
        res = backend.jgrapht_map_long_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_map_long_string_remove(self._handle, key)
        return _JGraphTString(res)

    def clear(self):
        backend.jgrapht_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongStringMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTEdgeTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTEdgeTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


class _JGraphTEdgeLongTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTEdgeLongTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeLongTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


class _JGraphTEdgeStrTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _JGraphTEdgeStrTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeStrTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"
