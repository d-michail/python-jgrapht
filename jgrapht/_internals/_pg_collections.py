from .. import backend
from collections import namedtuple
from collections.abc import Iterator

from ._wrappers import _JGraphTObjectIterator
from ._pg_wrappers import _PropertyGraphVertexIterator, _PropertyGraphEdgeIterator
from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerList,
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerIntegerMap,
)


class _PropertyGraphVertexSet(_JGraphTIntegerSet):
    """A vertex set for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _PropertyGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_PropertyGraphVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _PropertyGraphMutableVertexSet(_JGraphTIntegerMutableSet):
    """A vertex set for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _PropertyGraphVertexIterator(res, self._graph)

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
        return "_PropertyGraphMutableVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _PropertyGraphEdgeSet(_JGraphTIntegerSet):
    """An edge set for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _PropertyGraphEdgeIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._edge_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_PropertyGraphEdgeSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _PropertyGraphVertexDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _PropertyGraphVertexIterator(res, self._graph)

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
        return "_PropertyGraphVertexDoubleMap(%r)" % self._handle


class _PropertyGraphEdgeDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _PropertyGraphEdgeIterator(res, self._graph)

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
        return "_PropertyGraphEdgeDoubleMap(%r)" % self._handle


class _PropertyGraphVertexSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _PropertyGraphVertexSet(super().__next__(), self._graph)

    def __repr__(self):
        return "_PropertyGraphVertexSetIterator(%r)" % self._handle


class _PropertyGraphVertexIntegerMap(_JGraphTIntegerIntegerMap):
    """Property graph vertex map to integers"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _PropertyGraphVertexIterator(res, self._graph)

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
        return "_PropertyGraphVertexIntegerMap(%r)" % self._handle


class _PropertyGraphVertexList(_JGraphTIntegerList):
    """A vertex set for property graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _PropertyGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_list_int_contains(self._handle, x)

    def __repr__(self):
        return '_PropertyGraphVertexList(%r)' % self._handle


class _PropertyGraphVertexListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists of vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _PropertyGraphVertexList(super().__next__(), self._graph)

    def __repr__(self):
        return '_PropertyGraphVertexListIterator(%r)' % self._handle
