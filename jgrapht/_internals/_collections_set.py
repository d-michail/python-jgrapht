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


class _JGraphTIntegerSet(_HandleWrapper, Set):
    """JGraphT Integer Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_set_it_create(self._handle)
        return _JGraphTIntegerIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_i_set_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTIntegerSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTIntegerMutableSet(_JGraphTIntegerSet, MutableSet):
    """JGraphT Integer Mutable Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_i_set_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_i_set_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_x_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTIntegerMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTIntegerSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTIntegerSet(super().__next__())

    def __repr__(self):
        return "_JGraphTIntegerSetIterator(%r)" % self._handle


class _JGraphTLongSet(_HandleWrapper, Set):
    """JGraphT Long Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __iter__(self):
        res = backend.jgrapht_x_set_it_create(self._handle)
        return _JGraphTLongIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_l_set_contains(self._handle, x)
        return res

    def __repr__(self):
        return "_JGraphTLongSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTLongMutableSet(_JGraphTLongSet, MutableSet):
    """JGraphT Long Mutable Set"""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def add(self, x):
        backend.jgrapht_l_set_add(self._handle, x)

    def discard(self, x):
        backend.jgrapht_l_set_remove(self._handle, x)

    def clear(self):
        backend.jgrapht_x_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTLongMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTLongSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with longs."""

    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def __next__(self):
        return _JGraphTLongSet(super().__next__())

    def __repr__(self):
        return "_JGraphTLongSetIterator(%r)" % self._handle


class _JGraphTRefSet(_HandleWrapper, Set):
    """JGraphT Ref Set"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __iter__(self):
        res = backend.jgrapht_x_set_it_create(self._handle)
        return _JGraphTRefIterator(res)

    def __len__(self):
        res = backend.jgrapht_x_set_size(self._handle)
        return res

    def __contains__(self, x):
        res = backend.jgrapht_r_set_contains(
            self._handle, id(x), self._hash_equals_resolver_handle
        )
        return res

    def __repr__(self):
        return "_JGraphTRefSet(%r)" % self._handle

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self) + "}"

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTRefMutableSet(_JGraphTRefSet, MutableSet):
    """JGraphT Ref Mutable Set"""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(
            handle=handle,
            hash_equals_resolver_handle=hash_equals_resolver_handle,
            **kwargs
        )

    def add(self, x):
        backend.jgrapht_r_set_add(
            self._handle, id(x), self._hash_equals_resolver_handle
        )

    def discard(self, x):
        backend.jgrapht_r_set_remove(
            self._handle, id(x), self._hash_equals_resolver_handle
        )

    def clear(self):
        backend.jgrapht_x_set_clear(self._handle)

    def __repr__(self):
        return "_JGraphTRefMutableSet(%r)" % self._handle

    @classmethod
    def _from_iterable(cls, it):
        return set(it)


class _JGraphTRefSetIterator(_JGraphTObjectIterator):
    """An iterator which returns sets with refs."""

    def __init__(self, handle, hash_equals_resolver_handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._hash_equals_resolver_handle = hash_equals_resolver_handle

    def __next__(self):
        return _JGraphTRefSet(
            handle=super().__next__(),
            hash_equals_resolver_handle=self._hash_equals_resolver_handle,
        )

    def __repr__(self):
        return "_JGraphTRefSetIterator(%r)" % self._handle
