import pytest

from jgrapht._internals._collections import _JGraphTLongSet

def test_longset():

    s = _JGraphTLongSet()

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

def test_longset_linked():

    s = _JGraphTLongSet(linked=True)

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

