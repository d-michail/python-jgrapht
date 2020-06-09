import pytest

from jgrapht._internals._collections import (
    _JGraphTIntegerStringMap,
    _JGraphTIntegerDoubleMutableMap,
    _JGraphTIntegerIntegerMutableMap,
)


def test_JGraphTIntegerStringMap():

    s = _JGraphTIntegerStringMap()

    s[5] = "node 5"
    s[6] = "κόμβος 6"

    assert len(s) == 2

    assert 5 in s
    assert 6 in s
    assert 7 not in s

    assert str(s[5]) == "node 5"
    assert str(s[6]) == "κόμβος 6"


def test_JGraphTIntegerDoubleMutableMap():

    s = _JGraphTIntegerDoubleMutableMap()

    s[0] = 5.0
    s[1] = 15.0

    s.add(3, 150.0)

    assert len(s) == 3

    assert 0 in s
    assert 1 in s
    assert 2 not in s
    assert 3 in s

    assert s[0] == 5.0
    assert s[1] == 15.0
    assert s[3] == 150.0

    keys = []
    for k in s:
        keys.append(k)
    assert keys == [0, 1, 3]

    assert s.get(0) == 5.0
    assert s.get(2, 200.0) == 200.0

    with pytest.raises(KeyError):
        s.get(2)

    with pytest.raises(KeyError):
        print(s[2])

    assert str(s) == "{0: 5.0, 1: 15.0, 3: 150.0}"

    assert s.pop(3) == 150.0
    assert s.pop(12, 17.0) == 17.0

    with pytest.raises(KeyError):
        assert s.pop(12)

    del s[1]
    assert 1 not in s


def test_JGraphTIntegerIntegerMutableMap():

    s = _JGraphTIntegerIntegerMutableMap()

    s[0] = 5
    s[1] = 15

    s.add(3, 150)

    assert len(s) == 3

    assert 0 in s
    assert 1 in s
    assert 2 not in s
    assert 3 in s

    assert s[0] == 5
    assert s[1] == 15
    assert s[3] == 150

    keys = []
    for k in s:
        keys.append(k)
    assert keys == [0, 1, 3]

    assert s.get(0) == 5
    assert s.get(2, 200) == 200

    with pytest.raises(KeyError):
        s.get(2)

    with pytest.raises(KeyError):
        print(s[2])

    assert str(s) == "{0: 5, 1: 15, 3: 150}"

    assert s.pop(3) == 150
    assert s.pop(12, 17) == 17

    with pytest.raises(KeyError):
        assert s.pop(12)

    del s[1]
    assert 1 not in s
