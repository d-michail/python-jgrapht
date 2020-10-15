from .. import backend
from collections import namedtuple
from collections.abc import Iterator


class _HandleWrapper:
    """A handle wrapper. Keeps a handle to a backend object and cleans up
       on deletion.
    """

    def __init__(self, handle, **kwargs):
        self._handle = handle
        super().__init__()

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        if backend.jgrapht_is_initialized():
            backend.jgrapht_handles_destroy(self._handle)

    def __repr__(self):
        return "_HandleWrapper(%r)" % self._handle


class _JGraphTString(_HandleWrapper):
    """A JGraphT string.
    
       This object maintains a handle to a string inside the JVM.
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __str__(self):
        # SWIG automatically converts the ccharpointer in utf-8
        # coming from the capi to a python string
        return backend.jgrapht_handles_get_ccharpointer(self._handle)

    def __repr__(self):
        return "_JGraphTString(%r)" % self._handle


class _JGraphTIntegerIterator(_HandleWrapper, Iterator):
    """Integer values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_it_next_int(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerIterator(%r)" % self._handle


class _JGraphTDoubleIterator(_HandleWrapper, Iterator):
    """Double values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_it_next_double(self._handle)

    def __repr__(self):
        return "_JGraphTDoubleIterator(%r)" % self._handle


class _JGraphTEdgeTripleIterator(_HandleWrapper, Iterator):
    """An edge triple iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._edge_triple_class = namedtuple("Edge", ["source", "target", "weight"])

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()

        # read edge triple
        s, t, w = backend.jgrapht_it_next_edge_triple(self._handle)

        # return a named tuple
        return self._edge_triple_class(source=s, target=t, weight=w)

    def __repr__(self):
        return "_JGraphTEdgeTripleIterator(%r)" % self._handle


class _JGraphTEdgeStrTripleIterator(_HandleWrapper, Iterator):
    """An edge triple iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._edge_triple_class = namedtuple("Edge", ["source", "target", "weight"])

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()

        # read edge triple
        s, t, w = backend.jgrapht_it_next_str_edge_triple(self._handle)

        # return a named tuple
        return self._edge_triple_class(source=str(s), target=str(t), weight=w)

    def __repr__(self):
        return "_JGraphTEdgeStrTripleIterator(%r)" % self._handle



class _JGraphTObjectIterator(_HandleWrapper, Iterator):
    """A JGraphT iterator. This iterator returns handles to 
    backend objects. 
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_it_next_object(self._handle)

    def __repr__(self):
        return "_JGraphTObjectIterator(%r)" % self._handle
