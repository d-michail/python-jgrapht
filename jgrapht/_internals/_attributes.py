from .. import backend

from collections import Mapping, MutableMapping

from ._wrappers import (
    _JGraphTStringIterator,
    _JGraphTLongIterator,
    _JGraphTIntegerIterator,
)
from ._refcount import _id_to_obj, _dec_ref_by_id, _inc_ref, _map_ids_to_objs


class _IntegerVertexAttributesView(MutableMapping):
    """A view for an integer vertex attributes."""

    def __init__(self, handle, vertex, vertex_id):
        self._handle = handle
        self._vertex = vertex
        self._vertex_id = vertex_id

    def __getitem__(self, key):
        self._assert_vertex()
        encoded_key = bytearray(key, encoding="utf-8")
        res = backend.jgrapht_ii_graph_attrs_vertex_get_long(
            self._handle, self._vertex_id, encoded_key
        )
        if res is None:
            raise KeyError("Key {} not found".format(key))
        return _id_to_obj(res)

    def __setitem__(self, key, value):
        self._assert_vertex()
        encoded_key = bytearray(key, encoding="utf-8")
        try:
            old_value_id = backend.jgrapht_ii_graph_attrs_vertex_get_long(
                self._handle, self._vertex_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
        except ValueError:
            # key not found, ignore
            pass
        value_id = id(value)
        _inc_ref(value)
        backend.jgrapht_ii_graph_attrs_vertex_put_long(
            self._handle, self._vertex_id, encoded_key, value_id
        )

    def __delitem__(self, key):
        self._assert_vertex()
        try:
            encoded_key = bytearray(key, encoding="utf-8")
            old_value_id = backend.jgrapht_ii_graph_attrs_vertex_get_long(
                self._handle, self._vertex_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
            backend.jgrapht_ii_graph_attrs_vertex_remove(
                self._handle, self._vertex_id, encoded_key
            )
        except ValueError:
            # key not found, ignore
            pass

    def __len__(self):
        return backend.jgrapht_ii_graph_attrs_vertex_size(self._handle, self._vertex_id)

    def __iter__(self):
        it = backend.jgrapht_ii_graph_attrs_vertex_keys_iterator(
            self._handle, self._vertex_id
        )
        return _JGraphTStringIterator(handle=it)

    def __repr__(self):
        return "_IntegerVertexAttributesView(%r)" % repr(self._handle)

    def _assert_vertex(self):
        if not backend.jgrapht_ii_graph_contains_vertex(self._handle, self._vertex_id):
            raise ValueError("Vertex {} not in graph".format(self._vertex))


class _LongVertexAttributesView(MutableMapping):
    """A view for a long vertex attributes."""

    def __init__(self, handle, vertex, vertex_id):
        self._handle = handle
        self._vertex = vertex
        self._vertex_id = vertex_id

    def __getitem__(self, key):
        self._assert_vertex()
        encoded_key = bytearray(key, encoding="utf-8")
        res = backend.jgrapht_ll_graph_attrs_vertex_get_long(
            self._handle, self._vertex_id, encoded_key
        )
        if res is None:
            raise KeyError("Key {} not found".format(key))
        return _id_to_obj(res)

    def __setitem__(self, key, value):
        self._assert_vertex()
        encoded_key = bytearray(key, encoding="utf-8")
        try:
            old_value_id = backend.jgrapht_ll_graph_attrs_vertex_get_long(
                self._handle, self._vertex_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
        except ValueError:
            # key not found, ignore
            pass
        value_id = id(value)
        _inc_ref(value)
        backend.jgrapht_ll_graph_attrs_vertex_put_long(
            self._handle, self._vertex_id, encoded_key, value_id
        )

    def __delitem__(self, key):
        self._assert_vertex()
        try:
            encoded_key = bytearray(key, encoding="utf-8")
            old_value_id = backend.jgrapht_ll_graph_attrs_vertex_get_long(
                self._handle, self._vertex_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
            backend.jgrapht_ll_graph_attrs_vertex_remove(
                self._handle, self._vertex_id, encoded_key
            )
        except ValueError:
            # key not found, ignore
            pass

    def __len__(self):
        return backend.jgrapht_ll_graph_attrs_vertex_size(self._handle, self._vertex_id)

    def __iter__(self):
        it = backend.jgrapht_ll_graph_attrs_vertex_keys_iterator(
            self._handle, self._vertex_id
        )
        return _JGraphTStringIterator(handle=it)

    def __repr__(self):
        return "_LongVertexAttributesView(%r)" % repr(self._handle)

    def _assert_vertex(self):
        if not backend.jgrapht_ll_graph_contains_vertex(self._handle, self._vertex_id):
            raise ValueError("Vertex {} not in graph".format(self._vertex))


class _PerIntegerVertexAttributes(Mapping):
    """A dictionary view with all vertices attributes for int vertices."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, vertex):
        vertex_id = vertex
        if not backend.jgrapht_ii_graph_contains_vertex(self._handle, vertex_id):
            raise KeyError("Vertex {} does not exist".format(vertex))
        return _IntegerVertexAttributesView(self._handle, vertex, vertex_id)

    def __len__(self):
        return backend.jgrapht_ii_graph_vertices_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _JGraphTIntegerIterator(handle=it_handle)

    def __repr__(self):
        return "_PerIntegerVertexAttributes(%r)" % repr(self._handle)


class _PerLongVertexAttributes(Mapping):
    """A dictionary view with all vertices attributes for long vertices."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, vertex):
        vertex_id = vertex
        if not backend.jgrapht_ll_graph_contains_vertex(self._handle, vertex_id):
            raise KeyError("Vertex {} does not exist".format(vertex))
        return _LongVertexAttributesView(self._handle, vertex, vertex_id)

    def __len__(self):
        return backend.jgrapht_ll_graph_vertices_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _JGraphTLongIterator(handle=it_handle)

    def __repr__(self):
        return "_PerLongVertexAttributes(%r)" % repr(self._handle)


class _PerRefLongVertexAttributes(Mapping):
    """A dictionary view with all vertices attributes for any hashable vertices."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, vertex):
        vertex_id = id(vertex)
        if not backend.jgrapht_ll_graph_contains_vertex(self._handle, vertex_id):
            raise KeyError("Vertex {} does not exist".format(vertex))
        return _LongVertexAttributesView(self._handle, vertex, vertex_id)

    def __len__(self):
        return backend.jgrapht_ll_graph_vertices_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _map_ids_to_objs(_JGraphTLongIterator(handle=it_handle))

    def __repr__(self):
        return "_PerRefLongVertexAttributes(%r)" % repr(self._handle)


class _IntegerEdgeAttributesView(MutableMapping):
    """A view for an integer edge attributes."""

    def __init__(self, handle, edge, edge_id):
        self._handle = handle
        self._edge = edge
        self._edge_id = edge_id

    def __getitem__(self, key):
        self._assert_edge()
        encoded_key = bytearray(key, encoding="utf-8")
        res = backend.jgrapht_ii_graph_attrs_edge_get_long(
            self._handle, self._edge_id, encoded_key
        )
        if res is None:
            raise KeyError("Key {} not found".format(key))
        return _id_to_obj(res)

    def __setitem__(self, key, value):
        self._assert_edge()
        encoded_key = bytearray(key, encoding="utf-8")
        try:
            old_value_id = backend.jgrapht_ii_graph_attrs_edge_get_long(
                self._handle, self._edge_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
        except ValueError:
            # key not found, ignore
            pass
        value_id = id(value)
        _inc_ref(value)
        backend.jgrapht_ii_graph_attrs_edge_put_long(
            self._handle, self._edge_id, encoded_key, value_id
        )

    def __delitem__(self, key):
        self._assert_edge()
        try:
            encoded_key = bytearray(key, encoding="utf-8")
            old_value_id = backend.jgrapht_ii_graph_attrs_edge_get_long(
                self._handle, self._edge_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
            backend.jgrapht_ii_graph_attrs_edge_remove(self._handle, self._edge_id, encoded_key)
        except ValueError:
            # key not found, ignore
            pass

    def __len__(self):
        return backend.jgrapht_ii_graph_attrs_edge_size(self._handle, self._edge_id)

    def __iter__(self):
        it = backend.jgrapht_ii_graph_attrs_edge_keys_iterator(
            self._handle, self._edge_id
        )
        return _JGraphTStringIterator(handle=it)

    def __repr__(self):
        return "_IntegerEdgeAttributesView(%r)" % repr(self._handle)

    def _assert_edge(self):
        if not backend.jgrapht_ii_graph_contains_edge(self._handle, self._edge_id):
            raise ValueError("Edge {} not in graph".format(self._edge))


class _LongEdgeAttributesView(MutableMapping):
    """A view for a long edge attributes."""

    def __init__(self, handle, edge, edge_id):
        self._handle = handle
        self._edge = edge
        self._edge_id = edge_id

    def __getitem__(self, key):
        self._assert_edge()
        encoded_key = bytearray(key, encoding="utf-8")
        res = backend.jgrapht_ll_graph_attrs_edge_get_long(
            self._handle, self._edge_id, encoded_key
        )
        if res is None:
            raise KeyError("Key {} not found".format(key))
        return _id_to_obj(res)

    def __setitem__(self, key, value):
        self._assert_edge()
        encoded_key = bytearray(key, encoding="utf-8")
        try:
            old_value_id = backend.jgrapht_ll_graph_attrs_edge_get_long(
                self._handle, self._edge_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
        except ValueError:
            # key not found, ignore
            pass
        value_id = id(value)
        _inc_ref(value)
        backend.jgrapht_ll_graph_attrs_edge_put_long(
            self._handle, self._edge_id, encoded_key, value_id
        )

    def __delitem__(self, key):
        self._assert_edge()
        try:
            encoded_key = bytearray(key, encoding="utf-8")
            old_value_id = backend.jgrapht_ll_graph_attrs_edge_get_long(
                self._handle, self._edge_id, encoded_key
            )
            _dec_ref_by_id(old_value_id)
            backend.jgrapht_ll_graph_attrs_edge_remove(self._handle, self._edge_id, encoded_key)
        except ValueError:
            # key not found, ignore
            pass

    def __len__(self):
        return backend.jgrapht_ll_graph_attrs_edge_size(self._handle, self._edge_id)

    def __iter__(self):
        it = backend.jgrapht_ll_graph_attrs_edge_keys_iterator(
            self._handle, self._edge_id
        )
        return _JGraphTStringIterator(handle=it)

    def __repr__(self):
        return "_LongEdgeAttributesView(%r)" % repr(self._handle)

    def _assert_edge(self):
        if not backend.jgrapht_ll_graph_contains_edge(self._handle, self._edge_id):
            raise ValueError("Edge {} not in graph".format(self._edge))


class _PerIntegerEdgeAttributes(Mapping):
    """A dictionary view with all edge attributes for integer edges."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, edge):
        edge_id = edge
        if not backend.jgrapht_ii_graph_contains_edge(self._handle, edge_id):
            raise KeyError("Edge {} does not exist".format(edge))
        return _IntegerEdgeAttributesView(self._handle, edge, edge_id)

    def __len__(self):
        return backend.jgrapht_ii_graph_edges_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _JGraphTIntegerIterator(handle=it_handle)

    def __repr__(self):
        return "_PerIntegerEdgeAttributes(%r)" % repr(self._handle)


class _PerLongEdgeAttributes(Mapping):
    """A dictionary view with all edge attributes for long edges."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, edge):
        edge_id = edge
        if not backend.jgrapht_ll_graph_contains_edge(self._handle, edge_id):
            raise KeyError("Edge {} does not exist".format(edge))
        return _LongEdgeAttributesView(self._handle, edge, edge_id)

    def __len__(self):
        return backend.jgrapht_ll_graph_edges_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _JGraphTLongIterator(handle=it_handle)

    def __repr__(self):
        return "_PerLongEdgeAttributes(%r)" % repr(self._handle)


class _PerRefLongEdgeAttributes(Mapping):
    """A dictionary view with all edge attributes for any hashable edges."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, edge):
        edge_id = id(edge)
        if not backend.jgrapht_ll_graph_contains_edge(self._handle, edge_id):
            raise KeyError("Edge {} does not exist".format(edge))
        return _LongEdgeAttributesView(self._handle, edge, edge_id)

    def __len__(self):
        return backend.jgrapht_ll_graph_edges_count(self._handle)

    def __iter__(self):
        it_handle = backend.jgrapht_xx_graph_create_all_vit(self._handle)
        return _map_ids_to_objs(_JGraphTLongIterator(handle=it_handle))

    def __repr__(self):
        return "_PerRefLongEdgeAttributes(%r)" % repr(self._handle)


class _GraphAttributesMapping(MutableMapping):
    """A mapping for a graph attributes."""

    def __init__(self, handle):
        self._handle = handle

    def __getitem__(self, key):
        encoded_key = bytearray(key, encoding="utf-8")
        res = backend.jgrapht_xx_graph_attrs_get_long(self._handle, encoded_key)
        if res is None:
            raise KeyError("Key {} not found".format(key))
        return _id_to_obj(res)

    def __setitem__(self, key, value):
        encoded_key = bytearray(key, encoding="utf-8")
        try:
            old_value_id = backend.jgrapht_xx_graph_attrs_get_long(self._handle, encoded_key)
            _dec_ref_by_id(old_value_id)
        except ValueError:
            # key not found, ignore
            pass
        value_id = id(value)
        _inc_ref(value)
        backend.jgrapht_xx_graph_attrs_put_long(self._handle, encoded_key, value_id)

    def __delitem__(self, key):
        try:
            encoded_key = bytearray(key, encoding="utf-8")
            old_value_id = backend.jgrapht_xx_graph_attrs_get_long(self._handle, encoded_key)
            _dec_ref_by_id(old_value_id)
            backend.jgrapht_xx_graph_attrs_remove(self._handle, encoded_key)
        except ValueError:
            # key not found, ignore
            pass

    def __len__(self):
        return backend.jgrapht_xx_graph_attrs_size(self._handle)

    def __iter__(self):
        it = backend.jgrapht_xx_graph_attrs_keys_iterator(self._handle)
        return _JGraphTStringIterator(handle=it)

    def __repr__(self):
        return "_GraphAttributesMapping(%r)" % repr(self._handle)
