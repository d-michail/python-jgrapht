from . import jgrapht
from . import errors
from . import status
from . import iterator

class GraphVertexSet: 
    """Wrapper around the vertices of a JGraphT graph"""
    def __init__(self, handle=None):
        self._handle = handle

    def __iter__(self):
        err, res = jgrapht.jgrapht_graph_create_all_vit(self._handle)
        if err: 
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def __len__(self):
        err, res = jgrapht.jgrapht_graph_vertices_count(self._handle)
        if err: 
            errors.raise_status()
        return res

    def __contains__(self, v):
        err, res = jgrapht.jgrapht_graph_contains_vertex(self._handle, v)
        if err: 
            errors.raise_status()
        return res

class GraphEdgeSet: 
    """Wrapper around the edges of a JGraphT graph"""
    def __init__(self, handle=None):
        self._handle = handle

    def __iter__(self):
        err, res = jgrapht.jgrapht_graph_create_all_eit(self._handle)
        if err: 
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def __len__(self):
        err, res = jgrapht.jgrapht_graph_edges_count(self._handle)
        if err: 
            errors.raise_status()
        return res

    def __contains__(self, v):
        err, res = jgrapht.jgrapht_graph_contains_edge(self._handle, v)
        if err: 
            errors.raise_status()
        return res


class JGraphTLongSet:
    """JGraphT Long Set"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, res = jgrapht.jgrapht_set_linked_create()
            else: 
                err, res = jgrapht.jgrapht_set_create()
            if err: 
                errors.raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached() and self._owner:
            err = jgrapht.jgrapht_destroy(self._handle)
            if err:
                errors.raise_status() 

    @property
    def handle(self):
        return self._handle;

    def __iter__(self):
        err, res = jgrapht.jgrapht_set_it_create(self._handle)
        if err: 
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def __len__(self):
        err, res = jgrapht.jgrapht_set_size(self._handle)
        if err: 
            errors.raise_status()
        return res

    def add(self, x):
        err = jgrapht.jgrapht_set_long_add(self._handle, x)
        if err: 
            errors.raise_status()

    def remove(self, x):
        err, res = jgrapht.jgrapht_set_long_contains(self._handle, x)
        if err: 
            errors.raise_status()
        if not res: 
            raise KeyError()
        err = jgrapht.jgrapht_set_long_remove(self._handle, x)
        if err: 
            errors.raise_status()

    def discard(self, x):
        err, res = jgrapht.jgrapht_set_long_remove(self._handle, x)
        if err: 
            errors.raise_status()            

    def __contains__(self, x):
        err, res = jgrapht.jgrapht_set_long_contains(self._handle, x)
        if err: 
            errors.raise_status()
        return res

    def clear(self): 
        err, res = jgrapht.jgrapht_set_long_clear(self._handle)
        if err: 
            errors.raise_status()


class JGraphTLongDoubleMap:
    """JGraphT Map"""
    def __init__(self, handle=None, owner=True, linked=True):
        if handle is None:
            if linked: 
                err, res = jgrapht.jgrapht_map_linked_create()
            else: 
                err, res = jgrapht.jgrapht_map_create()
            if err: 
                errors.raise_status()
            self._handle = res
        else:
            self._handle = handle
        self._owner = owner

    def __del__(self):
        if jgrapht.jgrapht_is_thread_attached() and self._owner:
            err = jgrapht.jgrapht_destroy(self._handle)
            if err:
                errors.raise_status() 

    @property
    def handle(self):
        return self._handle;

    def __iter__(self):
        err, res = jgrapht.jgrapht_map_keys_it_create(self._handle)
        if err: 
            errors.raise_status()
        return iterator.LongValueIterator(res)

    def __len__(self):
        err, res = jgrapht.jgrapht_map_size(self._handle)
        if err: 
            errors.raise_status()
        return res

    def get(self, key, value=None):
        err, res = jgrapht.jgrapht_map_long_contains(self._handle, key)
        if err: 
            errors.raise_status()
        if not res: 
            if value is not None: 
                return value
            else: 
                raise KeyError()
        err, res = jgrapht.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            errors.raise_status()
        return res

    def add(self, key, value):
        err = jgrapht.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            errors.raise_status()

    def pop(self, key, defaultvalue):
        err, res = jgrapht.jgrapht_map_long_double_remove(self._handle, key)
        if err:
            if err == status.Status.ILLEGAL_ARGUMENT.value:
                # key not found in map
                jgrapht.jgrapht_clear_errno()
                if defaultvalue is not None:
                    return defaultvalue 
                else: 
                    raise KeyError()
            else:
                errors.raise_status()
        return res

    def __contains__(self, key):
        err, res = jgrapht.jgrapht_map_long_contains(self._handle, key)
        if err: 
            errors.raise_status()
        return res

    def __getitem__(self, key):
        err, res = jgrapht.jgrapht_map_long_contains(self._handle, key)
        if err: 
            errors.raise_status()
        if not res: 
            raise KeyError()
        err, res = jgrapht.jgrapht_map_long_double_get(self._handle, key)
        if err: 
            errors.raise_status()
        return res

    def __setitem__(self, key, value):
        err = jgrapht.jgrapht_map_long_double_put(self._handle, key, value)
        if err: 
            errors.raise_status()

    def __delitem__(self, key):
        err, res = jgrapht.jgrapht_map_long_contains(self._handle, key)
        if err: 
            errors.raise_status()
        if not res: 
            raise KeyError()
        err, res = jgrapht.jgrapht_map_long_double_remove(self._handle, key)
        if err: 
            errors.raise_status()

    def clear(self): 
        err, res = jgrapht.jgrapht_map_long_clear(self._handle)
        if err: 
            errors.raise_status()
