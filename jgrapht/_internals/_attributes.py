from .. import backend
from ._wrappers import _HandleWrapper


class _JGraphTAttributeStore(_HandleWrapper):
    """Attribute Store. Used to keep attributes for exporters."""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_store_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, element, key, value):
        backend.jgrapht_attributes_store_put_string_attribute(
            self._handle, element, key, value
        )

    def remove(self, element, key):
        backend.jgrapht_attributes_store_remove_attribute(
            self._handle, element, key
        )

    def __repr__(self):
        return "_JGraphTAttributeStore(%r)" % self._handle


class _JGraphTAttributesRegistry(_HandleWrapper):
    """Attribute Registry. Used to keep a list of registered attributes
    for exporters.
    """

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_attributes_registry_create()
        super().__init__(handle=handle, **kwargs)

    def put(self, name, category, type=None, default_value=None):
        backend.jgrapht_attributes_registry_register_attribute(
            self._handle, name, category, type, default_value
        )

    def remove(self, name, category):
        backend.jgrapht_attributes_registry_unregister_attribute(
            self._handle, name, category
        )

    def __repr__(self):
        return "_JGraphTAttributesRegistry(%r)" % self._handle
