import pytest

from jgrapht._internals._collections import _JGraphTIntegerStringMap


def test_JGraphTIntegerStringMap():

    s = _JGraphTIntegerStringMap()

    s[5] = 'node 5'
    s[6] = 'κόμβος 6'

    assert len(s) == 2

    assert 5 in s
    assert 6 in s
    assert 7 not in s

    assert str(s[5]) == 'node 5'
    assert str(s[6]) == 'κόμβος 6'

