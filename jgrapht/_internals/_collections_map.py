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


class _JGraphTIntegerDoubleMap(_HandleWrapper, Mapping):
    """JGraphT Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_id_map_get(self._handle, key)
        return res

    def __contains__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_id_map_get(self._handle, key)
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
        backend.jgrapht_id_map_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_id_map_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        backend.jgrapht_id_map_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        backend.jgrapht_id_map_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerDoubleMutableMap(%r)" % self._handle


class _JGraphTIntegerIntegerMap(_HandleWrapper, Mapping):
    """JGraphT Map with integer keys and integer values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_ii_map_get(self._handle, key)
        return res

    def __contains__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_ii_map_get(self._handle, key)
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
        backend.jgrapht_ii_map_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_ii_map_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        backend.jgrapht_ii_map_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_ii_map_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerIntegerMutableMap(%r)" % self._handle


class _JGraphTIntegerStringMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with integer keys and string values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    __marker = object()

    def get(self, key, value=__marker):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res = backend.jgrapht_is_map_get(self._handle, key)
        return _JGraphTString(res)

    def add(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_is_map_put(self._handle, key, encoded_value)

    def pop(self, key, defaultvalue=__marker):
        try:
            res = backend.jgrapht_is_map_remove(self._handle, key)
            return _JGraphTString(res)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_is_map_get(self._handle, key)
        return _JGraphTString(res)

    def __setitem__(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_is_map_put(self._handle, key, encoded_value)

    def __delitem__(self, key):
        res = backend.jgrapht_ix_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_is_map_remove(self._handle, key)
        return _JGraphTString(res)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

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
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_li_map_get(self._handle, key)
        return res

    def __contains__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_lx_map_get(self._handle, key)
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
        backend.jgrapht_li_map_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_li_map_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        backend.jgrapht_li_map_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_li_map_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongIntegerMutableMap(%r)" % self._handle


class _JGraphTLongDoubleMap(_HandleWrapper, Mapping):
    """JGraphT Map"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_ld_map_get(self._handle, key)
        return res

    def __contains__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_ld_map_get(self._handle, key)
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
        backend.jgrapht_ld_map_put(self._handle, key, value)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            return backend.jgrapht_ld_map_remove(self._handle, key)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        backend.jgrapht_ld_map_put(self._handle, key, value)

    def __delitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        backend.jgrapht_ld_map_remove(self._handle, key)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongDoubleMutableMap(%r)" % self._handle


class _JGraphTLongStringMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with long keys and string values"""

    def __init__(self, handle=None, linked=True, **kwargs):
        if handle is None:
            if linked:
                handle = backend.jgrapht_xx_map_linked_create()
            else:
                handle = backend.jgrapht_xx_map_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    __marker = object()

    def get(self, key, value=__marker):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res = backend.jgrapht_ls_map_get(self._handle, key)
        return _JGraphTString(res)

    def add(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_ls_map_put(self._handle, key, encoded_value)

    def pop(self, key, defaultvalue=__marker):
        try:
            res = backend.jgrapht_ls_map_remove(self._handle, key)
            return _JGraphTString(res)
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_ls_map_get(self._handle, key)
        return _JGraphTString(res)

    def __setitem__(self, key, value):
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_ls_map_put(self._handle, key, encoded_value)

    def __delitem__(self, key):
        res = backend.jgrapht_lx_map_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        res = backend.jgrapht_ls_map_remove(self._handle, key)
        return _JGraphTString(res)

    def clear(self):
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongStringMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTRefIntegerMap(_HandleWrapper, Mapping):
    """JGraphT Map"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_ri_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __contains__(self, key):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        if not res:
            raise KeyError()
        res = backend.jgrapht_ri_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __repr__(self):
        return "_JGraphTRefIntegerMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTRefIntegerMutableMap(_JGraphTRefIntegerMap, MutableMapping):
    """JGraphT Mutable Map"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

    def add(self, key, value):
        key_exists = self.__contains__(key)
        backend.jgrapht_ri_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            e = backend.jgrapht_ri_map_remove(
                self._handle, id(key), self._hash_equals_resolver_handle
            )
            _ref_utils._dec_ref(key)
            return e
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        key_exists = self.__contains__(key)
        backend.jgrapht_ri_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    def __delitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        backend.jgrapht_ri_map_remove(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        _ref_utils._dec_ref(key)

    def clear(self):
        # Cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefIntegerMutableMap(%r)" % self._handle


class _JGraphTRefDoubleMap(_HandleWrapper, Mapping):
    """JGraphT Map"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    def get(self, key, value=None):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_rd_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __contains__(self, key):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __getitem__(self, key):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        if not res:
            raise KeyError()
        res = backend.jgrapht_rd_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __repr__(self):
        return "_JGraphTRefDoubleMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


class _JGraphTRefDoubleMutableMap(_JGraphTRefDoubleMap, MutableMapping):
    """JGraphT Mutable Map"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

    def add(self, key, value):
        key_exists = self.__contains__(key)
        backend.jgrapht_rd_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    __marker = object()

    def pop(self, key, defaultvalue=__marker):
        try:
            e = backend.jgrapht_rd_map_remove(
                self._handle, id(key), self._hash_equals_resolver_handle
            )
            _ref_utils._dec_ref(key)
            return e
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __setitem__(self, key, value):
        key_exists = self.__contains__(key)
        backend.jgrapht_rd_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    def __delitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        backend.jgrapht_rd_map_remove(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        _ref_utils._dec_ref(key)

    def clear(self):
        # Cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefDoubleMutableMap(%r)" % self._handle


class _JGraphTRefStringMap(_HandleWrapper, MutableMapping):
    """JGraphT Map with ref keys and string values"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_xx_map_keys_it_create(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        res = backend.jgrapht_xx_map_size(self._handle)
        return res

    __marker = object()

    def get(self, key, value=__marker):
        key_exists = self.__contains__(key)
        if not key_exists:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res = backend.jgrapht_rs_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return str(_JGraphTString(res))

    def add(self, key, value):
        key_exists = self.__contains__(key)
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_rs_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, encoded_value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    def pop(self, key, defaultvalue=__marker):
        try:
            res = backend.jgrapht_ls_map_remove(self._handle, key)
            _ref_utils._dec_ref(key)
            return str(_JGraphTString(res))
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        res = backend.jgrapht_rx_map_contains_key(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return res

    def __getitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        res = backend.jgrapht_rs_map_get(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        return str(_JGraphTString(res))

    def __setitem__(self, key, value):
        key_exists = self.__contains__(key)
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_rs_map_put(
            self._handle, id(key), self._hash_equals_resolver_handle, encoded_value
        )
        if not key_exists:
            _ref_utils._inc_ref(key)

    def __delitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        backend.jgrapht_rs_map_remove(
            self._handle, id(key), self._hash_equals_resolver_handle
        )
        _ref_utils._dec_ref(key)

    def clear(self):
        # Cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        backend.jgrapht_xx_map_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefStringMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"