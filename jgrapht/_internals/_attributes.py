from .. import backend
from ._wrappers import _HandleWrapper, _JGraphTRefIterator
from . import _ref_utils, _ref_hashequals

from collections.abc import MutableMapping


class _JGraphTAttributeStore(_HandleWrapper):
    """Attribute Store.

    This attribute store is used by the exporters. Users
    provide attributes as strings which are automatically converted
    to UTF-8 encoded bytearrays and passed inside the Java context.
    """

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_xx_attributes_store_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, element, key, value):
        encoded_key = bytearray(key, encoding="utf-8")
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_is_attributes_store_put(
            self._handle, element, encoded_key, encoded_value
        )

    def remove(self, element, key):
        encoded_key = bytearray(key, encoding="utf-8")
        backend.jgrapht_ix_attributes_store_remove(self._handle, element, encoded_key)

    def __repr__(self):
        return "_JGraphTAttributeStore(%r)" % self._handle


class _JGraphTAttributesRegistry(_HandleWrapper):
    """Attribute Registry. Used to keep a list of registered attributes
    for the exporters.
    """

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_registry_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, name, category, attr_type=None, default_value=None):
        encoded_name = bytearray(name, encoding="utf-8")
        encoded_category = bytearray(category, encoding="utf-8")
        encoded_attr_type = (
            bytearray(attr_type, encoding="utf-8") if attr_type is not None else None
        )
        encoded_default_value = (
            bytearray(default_value, encoding="utf-8")
            if default_value is not None
            else None
        )
        backend.jgrapht_attributes_registry_register_attribute(
            self._handle,
            encoded_name,
            encoded_category,
            encoded_attr_type,
            encoded_default_value,
        )

    def remove(self, name, category):
        encoded_name = bytearray(name, encoding="utf-8")
        encoded_category = bytearray(category, encoding="utf-8")
        backend.jgrapht_attributes_registry_unregister_attribute(
            self._handle, encoded_name, encoded_category, None, None
        )

    def __repr__(self):
        return "_JGraphTAttributesRegistry(%r)" % self._handle


class _GraphAttributesMap(MutableMapping):
    """Map for graph attributes"""

    def __init__(self, handle, **kwargs):
        super().__init__(**kwargs)
        self._handle = handle
        self._keys_ref_counts = _ref_utils._SingleRefCount()
        self._values_ref_counts = _ref_utils._SingleRefCount()

    def __iter__(self):
        res = backend.jgrapht_xxrx_graph_attrs_keys_iterator(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        return backend.jgrapht_xxxx_graph_attrs_size(self._handle)

    __marker = object()

    def get(self, key, value=__marker):
        key_exists = self.__contains__(key)
        if not key_exists:
            if value is self.__marker:
                raise KeyError
            else:
                return value
        res_ptr = backend.jgrapht_xxrr_graph_attrs_get(self._handle, id(key))
        res = _ref_utils._swig_ptr_to_obj(res_ptr)
        return res

    def add(self, key, value):
        key_exists = self.__contains__(key)
        if key_exists:
            old_value_ptr = backend.jgrapht_xxrr_graph_attrs_get(self._handle, id(key))
            old_value = _ref_utils._swig_ptr_to_obj(old_value_ptr)
            self._keys_ref_counts.dec(key)
            self._values_ref_counts.dec(old_value)
        backend.jgrapht_xxrr_graph_attrs_put(self._handle, id(key), id(value))
        self._keys_ref_counts.inc(key)
        self._values_ref_counts.inc(value)

    def pop(self, key, defaultvalue=__marker):
        try:
            value_ptr = backend.jgrapht_xxrr_graph_attrs_remove(self._handle, id(key))
            value = _ref_utils._swig_ptr_to_obj(value_ptr)
            self._keys_ref_counts.dec(key)
            self._values_ref_counts.dec(value)
            return value
        except ValueError:
            if defaultvalue is self.__marker:
                raise KeyError()
            else:
                return defaultvalue

    def __contains__(self, key):
        return backend.jgrapht_xxrr_graph_attrs_contains(self._handle, id(key))

    def __getitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        value_ptr = backend.jgrapht_xxrr_graph_attrs_get(self._handle, id(key))
        value = _ref_utils._swig_ptr_to_obj(value_ptr)
        return value

    def __setitem__(self, key, value):
        key_exists = self.__contains__(key)
        if key_exists:
            old_value_ptr = backend.jgrapht_xxrr_graph_attrs_get(self._handle, id(key))
            old_value = _ref_utils._swig_ptr_to_obj(old_value_ptr)
            self._keys_ref_counts.dec(key)
            self._values_ref_counts.dec(old_value)
        backend.jgrapht_xxrr_graph_attrs_put(self._handle, id(key), id(value))
        self._keys_ref_counts.inc(key)
        self._values_ref_counts.inc(value)

    def __delitem__(self, key):
        key_exists = self.__contains__(key)
        if not key_exists:
            raise KeyError()
        value_ptr = backend.jgrapht_xxrr_graph_attrs_remove(self._handle, id(key))
        value = _ref_utils._swig_ptr_to_obj(value_ptr)
        self._keys_ref_counts.dec(key)
        self._values_ref_counts.dec(value)

    def clear(self):
        backend.jgrapht_xxxx_graph_attrs_clear(self._handle)
        self._keys_ref_counts.dec_all()
        self._values_ref_counts.dec_all()

    def __del__(self):
        self._keys_ref_counts.dec_all()
        self._values_ref_counts.dec_all()
        super().__del__()

    def __repr__(self):
        return "_GraphAttributesMap(%r)" % self._handle

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"
