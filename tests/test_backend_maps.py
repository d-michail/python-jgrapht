import pytest

import jgrapht._backend as _backend

from jgrapht._internals import _ref_hashequals
from jgrapht._internals._collections_map import (
    _JGraphTIntegerStringMap,
    _JGraphTIntegerDoubleMap,
    _JGraphTIntegerDoubleMutableMap,
    _JGraphTIntegerIntegerMap,
    _JGraphTIntegerIntegerMutableMap,
    _JGraphTRefIntegerMap,
    _JGraphTRefIntegerMutableMap,    
    _JGraphTRefDoubleMap,
    _JGraphTRefDoubleMutableMap,
    _JGraphTRefStringMap,
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

    it = iter(s.items())
    x, y = next(it)
    assert x == 5
    assert str(y) == "node 5"
    x, y = next(it)
    assert x == 6
    assert str(y) == "κόμβος 6"


    assert str(s.get(5)) == "node 5"
    assert s.get(8, None) == None

    s.add(8, "node 8")
    assert str(s.get(8)) == "node 8"

    with pytest.raises(KeyError):
        s.__getitem__(10)

    assert str(s.pop(8)) == "node 8"
    assert s.pop(100, "notfound") == "notfound"


    s.add(200, "node 200")
    assert str(s.__delitem__(200)) == "node 200"
    with pytest.raises(KeyError):
        s.__delitem__(200)

    with pytest.raises(KeyError):
        s.get(7)

    with pytest.raises(KeyError):
        s.pop(7)

    assert str(s) == "{5: node 5, 6: κόμβος 6}"
    

    s.clear();    
    assert len(s) == 0

    another = _JGraphTIntegerStringMap(linked=False)
    assert len(another) == 0

    repr(another)


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

    with pytest.raises(KeyError):
        del s[1]

    repr(s)

    s.clear();
    assert len(s) == 0


def test_JGraphTIntegerIntegerMap():

    handle = _backend.jgrapht_xx_map_create()
    _backend.jgrapht_ii_map_put(handle, 1, 5)
    _backend.jgrapht_ii_map_put(handle, 2, 10)
    _backend.jgrapht_ii_map_put(handle, 3, 20)

    s = _JGraphTIntegerIntegerMap(handle)
    assert len(s) == 3

    assert 1 in s
    assert 2 in s
    assert 3 in s
    assert 4 not in s

    assert s[1] == 5
    assert s[2] == 10
    assert s[3] == 20

    keys = []
    for k in s:
        keys.append(k)
    assert keys == [1, 2, 3]

    assert s.get(1) == 5
    assert s.get(2, 200) == 10
    assert s.get(5, 200) == 200

    with pytest.raises(KeyError):
        s.get(4)

    with pytest.raises(KeyError):
        print(s[4])

    assert str(s) == "{1: 5, 2: 10, 3: 20}"

    repr(s)

    another = _JGraphTIntegerIntegerMap(linked=False)
    assert len(another) == 0


def test_JGraphTIntegerDoubleMap():

    s = _JGraphTIntegerDoubleMap(linked=False)
    assert len(s) == 0
    repr(s)



def test_JGraphTRefDoubleMutableMap():

    handle = _backend.jgrapht_xx_map_create()
    hash_equals_resolver_handle = _ref_hashequals._get_hash_equals_wrapper().handle

    s = _JGraphTRefDoubleMutableMap(
        handle=handle, hash_equals_resolver_handle=hash_equals_resolver_handle
    )

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

    o = object()
    s[o] = 199.0

    assert o in s
    assert s[o] == 199.0



def test_JGraphTRefIntegerMutableMap():

    handle = _backend.jgrapht_xx_map_create()
    hash_equals_resolver_handle = _ref_hashequals._get_hash_equals_wrapper().handle

    s = _JGraphTRefIntegerMutableMap(
        handle=handle, hash_equals_resolver_handle=hash_equals_resolver_handle
    )

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

    with pytest.raises(KeyError):
        del s[1]

    repr(s)

    s.clear()
    assert len(s) == 0

    o = object()
    s[o] = 199

    assert o in s
    assert s[o] == 199

    del s[o]
    assert o not in s


def test_JGraphTRefStringMutableMap():

    handle = _backend.jgrapht_xx_map_linked_create()
    hash_equals_resolver_handle = _ref_hashequals._get_hash_equals_wrapper().handle

    s = _JGraphTRefStringMap(
        handle=handle, hash_equals_resolver_handle=hash_equals_resolver_handle
    )

    o1 = object()
    s[o1] = "myobject"
    o2 = object()
    s[o2] = "second"
    o3 = object()

    assert o1 in s
    assert o2 in s
    assert o3 not in s
    assert s[o1] == "myobject"
    assert s[o2] == "second"

    assert len(s) == 2

    with pytest.raises(KeyError):
        del s[o3]

    keys = []
    for k in s:
        keys.append(k)
    assert keys == [o1, o2]
