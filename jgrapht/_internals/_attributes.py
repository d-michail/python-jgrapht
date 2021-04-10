from .. import backend
from .. import GraphBackend
from ._wrappers import _HandleWrapper, _JGraphTRefIterator
from . import _ref_utils, _ref_hashequals

from collections.abc import MutableMapping


class _JGraphTAttributeStore(_HandleWrapper):
    """Attribute Store.

    This attribute store is used by the exporters. Users
    provide attributes as strings which are automatically converted
    to UTF-8 encoded bytearrays and passed inside the Java context.
    """
    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def put(self, element, key, value):
        encoded_key = bytearray(key, encoding="utf-8")
        encoded_value = bytearray(value, encoding="utf-8")
        if self._graph._backend_type == GraphBackend.INT_GRAPH:
            backend.jgrapht_is_attributes_store_put(
                self._handle, element, encoded_key, encoded_value
            )
        elif self._graph._backend_type == GraphBackend.LONG_GRAPH:
            backend.jgrapht_ls_attributes_store_put(
                self._handle, element, encoded_key, encoded_value
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            backend.jgrapht_rs_attributes_store_put(
                self._handle,
                id(element),
                self._graph._hash_equals_wrapper.handle,
                encoded_key,
                encoded_value,
            )
        else:
            raise ValueError("Not recognized backend")

    def remove(self, element, key):
        encoded_key = bytearray(key, encoding="utf-8")
        if self._graph._backend_type == GraphBackend.INT_GRAPH:
            backend.jgrapht_ix_attributes_store_remove(
                self._handle, element, encoded_key
            )
        elif self._graph._backend_type == GraphBackend.LONG_GRAPH:
            backend.jgrapht_lx_attributes_store_remove(
                self._handle, element, encoded_key
            )
        elif self._graph._backend_type == GraphBackend.REF_GRAPH:
            backend.jgrapht_rx_attributes_store_remove(
                self._handle,
                id(element),
                self._graph._hash_equals_wrapper.handle,
                encoded_key,
            )
        else:
            raise ValueError("Not recognized backend")

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


class _VertexAttributes(MutableMapping):
    """Wrapper around a dictionary to ensure vertex existence."""

    def __init__(self, graph, storage):
        self._graph = graph
        self._storage = storage

    def __getitem__(self, key):
        if key not in self._graph.vertices:
            raise ValueError("Vertex {} not in graph".format(key))
        return self._storage[key]

    def __setitem__(self, key, value):
        if key not in self._graph.vertices:
            raise ValueError("Vertex {} not in graph".format(key))
        self._storage[key] = value

    def __delitem__(self, key):
        if key not in self._graph.vertices:
            raise ValueError("Vertex {} not in graph".format(key))
        del self._storage[key]

    def _unsafe_delitem(self, key):
        self._storage.pop(key, None)

    def __len__(self):
        return len(self._storage)

    def __iter__(self):
        return iter(self._storage)

    def __repr__(self):
        return "_VertexAttributes(%r)" % repr(self._storage)

    def __str__(self):
        items = []
        for v in self._graph.vertices:
            items.append("{}: {}".format(v, self._storage[v]))
        return "{" + ", ".join(items) + "}"


class _EdgeAttributes(MutableMapping):
    """Wrapper around a dictionary to ensure edge existence."""

    def __init__(self, graph, storage):
        self._graph = graph
        self._storage = storage

    def __getitem__(self, key):
        if key not in self._graph.edges:
            raise ValueError("Edge {} not in graph".format(key))
        return _PerEdgeWeightAwareDict(self._graph, key, self._storage[key])

    def __setitem__(self, key, value):
        if key not in self._graph.edges:
            raise ValueError("Edge {} not in graph".format(key))
        self._storage[key] = value

    def __delitem__(self, key):
        if key not in self._graph.edges:
            raise ValueError("Edge {} not in graph".format(key))
        del self._storage[key]

    def _unsafe_delitem(self, key):
        self._storage.pop(key, None)

    def __len__(self):
        return len(self._storage)

    def __iter__(self):
        return iter(self._storage)

    def __repr__(self):
        return "_AnyHashableGraph-EdgeAttributes(%r)" % repr(self._storage)

    def __str__(self):
        items = []
        for e in self._graph.edges:
            items.append("{}: {}".format(e, self._storage[e]))
        return "{" + ", ".join(items) + "}"


class _PerEdgeWeightAwareDict(MutableMapping):

    """A dictionary view which knows about the special key weight and delegates
    to the graph. This is only a view."""

    def __init__(self, graph, edge, storage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._graph = graph
        self._edge = edge
        self._storage = storage

    def __getitem__(self, key):
        if key == "weight":
            return self._graph.get_edge_weight(self._edge)
        else:
            return self._storage[key]

    def __setitem__(self, key, value):
        if key == "weight":
            if not isinstance(value, (float)):
                raise TypeError("Weight is not a floating point number")
            self._graph.set_edge_weight(self._edge, value)
        else:
            self._storage[key] = value

    def __delitem__(self, key):
        if key == "weight":
            self._graph.set_edge_weight(self._edge, 1.0)
        else:
            del self._storage[key]

    def __len__(self):
        return len(self._storage)

    def __iter__(self):
        return iter(self._storage)

    def __repr__(self):
        return "_PerEdgeWeightAwareDict(%r, %r, %r)" % (
            repr(self._graph),
            repr(self._edge),
            repr(self._storage),
        )

    def __str__(self):
        return str(self._storage)
