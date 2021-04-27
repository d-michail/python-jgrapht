from .. import backend
from . import _ref_utils
from collections import namedtuple
from collections.abc import Iterator
from enum import Enum


class GraphBackend(Enum):
    """Different backend graph implementations. Each backend exhibits different
       characteristics between performance and user-friendliness.
    """
    INT_GRAPH = 1
    LONG_GRAPH = 2
    REF_GRAPH = 3


class _HandleWrapper:
    """A handle wrapper. Keeps a handle to a backend object and cleans up
       on deletion.
    """
    def __init__(self, handle, **kwargs):
        self._handle = handle

    @property
    def handle(self):
        return self._handle

    def __del__(self):
        try: 
            backend.jgrapht_handles_destroy(self._handle)
        except (TypeError, AttributeError): 
            # ignore error if backend is unloaded before we cleanup
            # also ignore error if exception happens before superclass gets initialized
            pass

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


class _JGraphTExternalRef(_HandleWrapper):
    """A JGraphT external reference.
    
       This object maintains a handle to a ExternalRef class inside the JVM.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def get(self): 
        ptr, _, _ = backend.jgrapht_handles_get_ref(self._handle)
        return _ref_utils._swig_ptr_to_obj(ptr)

    def __repr__(self):
        return "_JGraphTExternalRef(%r)" % self._handle


class _JGraphTIntegerIterator(_HandleWrapper, Iterator):
    """Integer values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_i_it_next(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerIterator(%r)" % self._handle


class _JGraphTLongIterator(_HandleWrapper, Iterator):
    """Long values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_l_it_next(self._handle)

    def __repr__(self):
        return "_JGraphTLongIterator(%r)" % self._handle
        

class _JGraphTDoubleIterator(_HandleWrapper, Iterator):
    """Double values iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_d_it_next(self._handle)

    def __repr__(self):
        return "_JGraphTDoubleIterator(%r)" % self._handle


class _JGraphTEdgeIntegerTripleIterator(_HandleWrapper, Iterator):
    """An edge triple iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._edge_triple_class = namedtuple("Edge", ["source", "target", "weight"])

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()

        # read edge triple
        s, t, w = backend.jgrapht_iid_t_it_next(self._handle)

        # return a named tuple
        return self._edge_triple_class(source=s, target=t, weight=w)

    def __repr__(self):
        return "_JGraphTEdgeIntegerTripleIterator(%r)" % self._handle


class _JGraphTEdgeLongTripleIterator(_HandleWrapper, Iterator):
    """An edge triple iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._edge_triple_class = namedtuple("Edge", ["source", "target", "weight"])

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()

        # read edge triple
        s, t, w = backend.jgrapht_lld_t_it_next(self._handle)

        # return a named tuple
        return self._edge_triple_class(source=s, target=t, weight=w)

    def __repr__(self):
        return "_JGraphTEdgeLongTripleIterator(%r)" % self._handle


class _JGraphTEdgeStrTripleIterator(_HandleWrapper, Iterator):
    """An edge triple iterator"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._edge_triple_class = namedtuple("Edge", ["source", "target", "weight"])

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()

        # read edge triple
        s, t, w = backend.jgrapht_ssd_t_it_next(self._handle)

        # return a named tuple
        return self._edge_triple_class(source=str(s), target=str(t), weight=w)

    def __repr__(self):
        return "_JGraphTEdgeStrTripleIterator(%r)" % self._handle


class _JGraphTStringIterator(_HandleWrapper, Iterator):
    """A JGraphT string iterator.
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        handle = backend.jgrapht_x_it_next(self._handle)
        return str(_JGraphTString(handle=handle))

    def __repr__(self):
        return "_JGraphTStringIterator(%r)" % self._handle


class _JGraphTPtrIterator(_HandleWrapper, Iterator):
    """A JGraphT iterator. This iterator returns frontend objects
    resolved from references kept in the backend. 
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_r_it_next(self._handle)

    def __repr__(self):
        return "_JGraphTPtrIterator(%r)" % self._handle


class _JGraphTRefIterator(_HandleWrapper, Iterator):
    """A JGraphT iterator. This iterator returns frontend objects
    resolved from references kept in the backend. 
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        value = backend.jgrapht_r_it_next(self._handle)
        return _ref_utils._swig_ptr_to_obj(value)

    def __repr__(self):
        return "_JGraphTRefIterator(%r)" % self._handle


class _JGraphTObjectIterator(_HandleWrapper, Iterator):
    """A JGraphT iterator. This iterator returns handles to 
    backend objects. Note that someone should take the ownership 
    of these handles. 
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        res = backend.jgrapht_x_it_hasnext(self._handle)
        if not res:
            raise StopIteration()
        return backend.jgrapht_x_it_next(self._handle)

    def __repr__(self):
        return "_JGraphTObjectIterator(%r)" % self._handle


class _JGraphTThreadPool(_HandleWrapper):
    """A JGraphT thread pool executor. 
    """

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def shutdown(self, timeout_millis=10000):
        backend.jgrapht_executor_thread_pool_shutdown(self._handle, timeout_millis)

    def __repr__(self):
        return "_JGraphTThreadPool(%r)" % self._handle
