from .. import backend

from ._wrappers import _JGraphTObjectIterator
from ._anyhashableg_wrappers import (
    _AnyHashableGraphVertexIterator,
    _AnyHashableGraphEdgeIterator,
)
from ._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTIntegerList,
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerIntegerMap,
)


class _AnyHashableGraphVertexSet(_JGraphTIntegerSet):
    """A vertex set for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AnyHashableGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_AnyHashableGraphVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AnyHashableGraphMutableVertexSet(_JGraphTIntegerMutableSet):
    """A vertex set for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AnyHashableGraphVertexIterator(res, self._graph)

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
        return "_AnyHashableGraphMutableVertexSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AnyHashableGraphEdgeSet(_JGraphTIntegerSet):
    """An edge set for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_set_it_create(self._handle)
        return _AnyHashableGraphEdgeIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._edge_hash_to_id[x]
        return backend.jgrapht_set_int_contains(self._handle, x)

    def __repr__(self):
        return "_AnyHashableGraphEdgeSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _AnyHashableGraphVertexDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AnyHashableGraphVertexIterator(res, self._graph)

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
        return "_AnyHashableGraphVertexDoubleMap(%r)" % self._handle


class _AnyHashableGraphEdgeDoubleMap(_JGraphTIntegerDoubleMap):
    """A vertex to double map for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AnyHashableGraphEdgeIterator(res, self._graph)

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
        return "_AnyHashableGraphEdgeDoubleMap(%r)" % self._handle


class _AnyHashableGraphVertexSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _AnyHashableGraphVertexSet(super().__next__(), self._graph)

    def __repr__(self):
        return "_AnyHashableGraphVertexSetIterator(%r)" % self._handle


class _AnyHashableGraphVertexIntegerMap(_JGraphTIntegerIntegerMap):
    """Attributes graph vertex map to integers"""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_map_keys_it_create(self._handle)
        return _AnyHashableGraphVertexIterator(res, self._graph)

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
        return "_AnyHashableGraphVertexIntegerMap(%r)" % self._handle


class _AnyHashableGraphVertexList(_JGraphTIntegerList):
    """A vertex set for any-hashable graphs."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __iter__(self):
        res = backend.jgrapht_list_it_create(self._handle)
        return _AnyHashableGraphVertexIterator(res, self._graph)

    def __contains__(self, x):
        x = self._graph._vertex_hash_to_id[x]
        return backend.jgrapht_list_int_contains(self._handle, x)

    def __repr__(self):
        return "_AnyHashableGraphVertexList(%r)" % self._handle


class _AnyHashableGraphVertexListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists of vertices."""

    def __init__(self, handle, graph, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._graph = graph

    def __next__(self):
        return _AnyHashableGraphVertexList(super().__next__(), self._graph)

    def __repr__(self):
        return "_AnyHashableGraphVertexListIterator(%r)" % self._handle
