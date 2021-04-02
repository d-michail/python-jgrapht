import pytest

import jgrapht._backend as _backend

from jgrapht._internals import _ref_hashequals
from jgrapht._internals._collections_set import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
    _JGraphTLongMutableSet,
    _JGraphTRefMutableSet,
)


def test_IntegerSet():

    handle = _backend.jgrapht_x_set_linked_create()
    _backend.jgrapht_i_set_add(handle, 5)
    _backend.jgrapht_i_set_add(handle, 7)
    _backend.jgrapht_i_set_add(handle, 9)

    s = _JGraphTIntegerSet(handle=handle)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    assert set(s) == set([5, 7, 9])

    print(repr(s))
    print(s)


def test_IntegerMutableSet():

    handle = _backend.jgrapht_x_set_create()
    s = _JGraphTIntegerMutableSet(handle=handle)

    s.add(5)
    s.add(7)
    s.add(9)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    s.remove(7)

    assert 5 in s
    assert 6 not in s
    assert 7 not in s
    assert 8 not in s
    assert 9 in s

    assert len(s) == 2

    s.add(11)
    s.add(13)

    assert len(s) == 4

    s.discard(17)
    assert len(s) == 4

    with pytest.raises(KeyError):
        s.remove(17)

    assert set(s) == set([5, 9, 11, 13])

    print(repr(s))
    print(s)


def test_IntegerMutableSet_linked():

    handle = _backend.jgrapht_x_set_linked_create()
    s = _JGraphTIntegerMutableSet(handle=handle)

    s.add(5)
    s.add(7)
    s.add(9)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    s.remove(7)

    assert 5 in s
    assert 6 not in s
    assert 7 not in s
    assert 8 not in s
    assert 9 in s

    assert len(s) == 2

    s.add(11)
    s.add(13)

    assert len(s) == 4

    s.discard(17)
    assert len(s) == 4

    with pytest.raises(KeyError):
        s.remove(17)

    assert set(s) == set([5, 9, 11, 13])

    s.clear()

    assert len(s) == 0

    assert repr(s) == "_JGraphTIntegerMutableSet(%r)" % (s.handle)


def test_LongMutableSet():

    handle = _backend.jgrapht_x_set_create()
    s = _JGraphTLongMutableSet(handle=handle)

    s.add(5)
    s.add(7)
    s.add(9)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    s.remove(7)

    assert 5 in s
    assert 6 not in s
    assert 7 not in s
    assert 8 not in s
    assert 9 in s

    assert len(s) == 2

    s.add(11)
    s.add(13)

    assert len(s) == 4

    s.discard(17)
    assert len(s) == 4

    with pytest.raises(KeyError):
        s.remove(17)

    assert set(s) == set([5, 9, 11, 13])

    print(repr(s))
    print(s)


def test_RefMutableSet():

    handle = _backend.jgrapht_x_set_linked_create()
    hash_equals_resolver_handle = _ref_hashequals._get_equals_hash_wrapper().handle

    s = _JGraphTRefMutableSet(
        handle=handle, hash_equals_resolver_handle=hash_equals_resolver_handle
    )

    s.add(5)
    s.add(7)
    s.add(9)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    s.remove(7)

    assert 5 in s
    assert 6 not in s
    assert 7 not in s
    assert 8 not in s
    assert 9 in s

    assert len(s) == 2

    s.add(11)
    s.add(13)

    assert len(s) == 4

    s.discard(17)
    assert len(s) == 4

    with pytest.raises(KeyError):
        s.remove(17)

    assert set(s) == set([5, 9, 11, 13])

    print(repr(s))
    print(s)
