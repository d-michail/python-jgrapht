from .. import backend

from . import _ref_utils, _ref_hashequals
from ._wrappers import (
    _HandleWrapper,
    _JGraphTString,
    _JGraphTObjectIterator,
    _JGraphTIntegerIterator,
    _JGraphTLongIterator,
    _JGraphTEdgeLongTripleIterator,
    _JGraphTEdgeIntegerTripleIterator,
    _JGraphTEdgeStrTripleIterator,
    _JGraphTRefIterator,
    _JGraphTRefIterator,
)

from collections.abc import (
    Set,
    MutableSet,
    Collection,
    Mapping,
    MutableMapping,
    Iterable,
    Sized,
)


class _JGraphTIntegerList(_HandleWrapper, Collection):
    """JGraphT Integer List"""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_x_list_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_list_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_i_list_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTIntegerList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTIntegerMutableList(_JGraphTIntegerList):
    """JGraphT Integer List"""

    def __init__(self, handle=None, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_i_list_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_i_list_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_x_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerMutableList(%r)" % self._handle


class _JGraphTIntegerListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with integers."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerList(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerListIterator(%r)" % self._handle


class _JGraphTLongList(_HandleWrapper, Collection):
    """JGraphT Long List"""

    def __init__(self, handle=None, **kwargs):
        if handle is None:
            handle = backend.jgrapht_x_list_create()
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_list_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_l_list_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTLongList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTLongMutableList(_JGraphTLongList):
    """JGraphT Long List"""

    def __init__(self, handle=None, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_l_list_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_l_list_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_x_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongMutableList(%r)" % self._handle


class _JGraphTLongListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongList(super().__next__())

    def __repr__(self):
        return "_JGraphTLongListIterator(%r)" % self._handle


class _JGraphTRefList(_HandleWrapper, Collection):
    """JGraphT Ref List"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_list_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_r_list_contains(
            self._handle, id(x), self._hash_equals_resolver_handle
        )
        return res

    def __repr__(self):
        return "_JGraphTRefList(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"


class _JGraphTRefMutableList(_JGraphTRefList):
    """JGraphT Ref List"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

    def add(self, x):
        if backend.jgrapht_r_list_add(
            self._handle, id(x), self._hash_equals_resolver_handle
        ):
            _ref_utils._inc_ref(x)

    def discard(self, x):
        if backend.jgrapht_r_list_remove(
            self._handle, id(x), self._hash_equals_resolver_handle
        ):
            _ref_utils._dec_ref(x)

    def clear(self):
        # cleanup reference counts
        for x in self:
            _ref_utils._dec_ref(x)
        backend.jgrapht_x_list_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefMutableList(%r)" % self._handle


class _JGraphTRefListIterator(_JGraphTObjectIterator):
    """An iterator which returns lists with references."""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __next__(self):
        return _JGraphTRefList(
            handle=super().__next__(),
            hash_equals_resolver_handle=self._hash_equals_resolver_handle,
        )

    def __repr__(self):
        return "_JGraphTRefListIterator(%r)" % self._handle


class _JGraphTEdgeTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTEdgeIntegerTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_x_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


class _JGraphTEdgeLongTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTEdgeLongTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_x_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeLongTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


class _JGraphTEdgeStrTripleList(_HandleWrapper, Iterable, Sized):
    """JGraphT list which contains edge triples"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_list_it_create(self._handle)
        return _JGraphTEdgeStrTripleIterator(res)

    def __len__(self):
        return backend.jgrapht_x_list_size(self._handle)

    def __repr__(self):
        return "_JGraphTEdgeStrTripleList(%r)" % self._handle

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"

