from .. import backend
from ._wrappers import _HandleWrapper


class _JGraphTAttributeStore(_HandleWrapper):
    """Attribute Store. 
    
    This attribute store is used by the exporters. Users 
    provide attributes as strings which are automatically converted
    to UTF-8 encoded bytearrays and passed inside the Java context. 
    """

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_store_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, element, key, value):
        encoded_key = bytearray(key, encoding="utf-8")
        encoded_value = bytearray(value, encoding="utf-8")
        backend.jgrapht_attributes_store_put_string_attribute(
            self._handle, element, encoded_key, encoded_value
        )

    def remove(self, element, key):
        encoded_key = bytearray(key, encoding="utf-8")
        backend.jgrapht_attributes_store_remove_attribute(
            self._handle, element, encoded_key
        )

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
