from .. import backend
from collections import namedtuple
from collections.abc import Iterator

from ._wrappers import _JGraphTObjectIterator
from ._attrsg_wrappers import _AttributesGraphVertexIterator, _AttributesGraphEdgeIterator
from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerList,
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerIntegerMap,
)


class _AttributesGraphVertexSet(_JGraphTIntegerSet):
    """A vertex set for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AttributesGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_AttributesGraphVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AttributesGraphMutableVertexSet(_JGraphTIntegerMutableSet):
    """A vertex set for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AttributesGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def add(self, x):
        x = self._graph._vertex_hash_to_id[x]
        backend.jgrapht_set_int_add(self._handle, x)

    def discard(self, x):
        x = self._graph._vertex_hash_to_id[x]
        backend.jgrapht_set_int_remove(self._handle, x)

    def __repr__(self):
        return "_AttributesGraphMutableVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AttributesGraphEdgeSet(_JGraphTIntegerSet):
    """An edge set for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AttributesGraphEdgeIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._edge_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_AttributesGraphEdgeSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AttributesGraphVertexDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AttributesGraphVertexIterator(res, self._graph)

    def get(self, key, value=None):
        key = self._graph._vertex_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        return backend.jgrapht_map_int_double_get(self._handle, key)

    def __contains__(self, key):
        key = self._graph._vertex_hash_to_id[key]
        return backend.jgrapht_map_int_contains_key(self._handle, key)

    def __getitem__(self, key):
        key = self._graph._vertex_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        return backend.jgrapht_map_int_double_get(self._handle, key)

    def __repr__(self):
        return "_AttributesGraphVertexDoubleMap(%r)" % self._handle


class _AttributesGraphEdgeDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AttributesGraphEdgeIterator(res, self._graph)

    def get(self, key, value=None):
        key = self._graph._edge_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        return backend.jgrapht_map_int_double_get(self._handle, key)

    def __contains__(self, key):
        key = self._graph._edge_hash_to_id[key]
        return backend.jgrapht_map_int_contains_key(self._handle, key)

    def __getitem__(self, key):
        key = self._graph._edge_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        return backend.jgrapht_map_int_double_get(self._handle, key)

    def __repr__(self):
        return "_AttributesGraphEdgeDoubleMap(%r)" % self._handle


class _AttributesGraphVertexSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _AttributesGraphVertexSet(super().__next__(), self._graph)

    def __repr__(self):
        return "_AttributesGraphVertexSetIterator(%r)" % self._handle


class _AttributesGraphVertexIntegerMap(_JGraphTIntegerIntegerMap):
    """Attributes graph vertex map to integers"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AttributesGraphVertexIterator(res, self._graph)

    def get(self, key, value=None):
        key = self._graph._vertex_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            if value is not None:
                return value
            else:
                raise KeyError()
        res = backend.jgrapht_map_int_int_get(self._handle, key)
        return res

    def __contains__(self, key):
        key = self._graph._vertex_hash_to_id[key]
        return backend.jgrapht_map_int_contains_key(self._handle, key)

    def __getitem__(self, key):
        key = self._graph._vertex_hash_to_id[key]
        res = backend.jgrapht_map_int_contains_key(self._handle, key)
        if not res:
            raise KeyError()
        return backend.jgrapht_map_int_int_get(self._handle, key)

    def __repr__(self):
        return "_AttributesGraphVertexIntegerMap(%r)" % self._handle


class _AttributesGraphVertexList(_JGraphTIntegerList):
    """A vertex set for attributes graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _AttributesGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_list_int_contains(self._handle, x)

    def __repr__(self):
        return '_AttributesGraphVertexList(%r)' % self._handle


class _AttributesGraphVertexListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists of vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _AttributesGraphVertexList(super().__next__(), self._graph)

    def __repr__(self):
        return '_AttributesGraphVertexListIterator(%r)' % self._handle
