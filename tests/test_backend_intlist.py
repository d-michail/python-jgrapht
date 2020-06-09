import pytest

import jgrapht._backend as _backend
from jgrapht._internals._collections import (
    _JGraphTIntegerList,
    _JGraphTIntegerMutableList,
)



def test_IntegerList():

    handle = _backend.jgrapht_list_create()
    _backend.jgrapht_list_int_add(handle, 5)
    _backend.jgrapht_list_int_add(handle, 7)
    _backend.jgrapht_list_int_add(handle, 9)

    s = _JGraphTIntegerList(handle=handle)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    assert list(s) == list([5, 7, 9])

    print(repr(s))
    print(s)


def test_IntegerMutableList():

    s = _JGraphTIntegerMutableList()

    s.add(5)
    s.add(7)
    s.add(9)

    assert len(s) == 3

    assert 5 in s
    assert 6 not in s
    assert 7 in s
    assert 8 not in s
    assert 9 in s

    s.discard(7)

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

    s.discard(17)

    assert set(s) == set([5, 9, 11, 13])

    s.clear()
    assert len(s) == 0

    str(s)
    repr(s)
