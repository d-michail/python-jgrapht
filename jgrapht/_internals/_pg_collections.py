from .. import backend
from collections import namedtuple
from collections.abc import Iterator

from ._pg_wrappers import _PropertyGraphVertexIterator
from ._collections import _JGraphTIntegerSet, _JGraphTIntegerDoubleMap


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

    def __str__(self):
        items = ["{}: {}".format(k, v) for k, v in self.items()]
        return "{" + ", ".join(items) + "}"
