import pytest

import jgrapht._backend as _backend

from jgrapht._internals._collections import (
    _JGraphTIntegerSet,
    _JGraphTIntegerMutableSet,
)


def test_IntegerSet():

    handle = _backend.jgrapht_set_linked_create()
    _backend.jgrapht_set_int_add(handle, 5)
    _backend.jgrapht_set_int_add(handle, 7)
    _backend.jgrapht_set_int_add(handle, 9)

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

    s = _JGraphTIntegerMutableSet(linked=False)

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

    s = _JGraphTIntegerMutableSet(linked=True)

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

    assert repr(s) == '_JGraphTIntegerMutableSet(%r)' % (s.handle)

