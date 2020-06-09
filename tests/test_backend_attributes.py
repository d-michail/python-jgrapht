import pytest

from jgrapht._internals._attributes import (
    _JGraphTAttributeStore,
    _JGraphTAttributesRegistry,
)


def test_store():

    s = _JGraphTAttributeStore()

    s.put(0, 'color', 'red')
    s.put(1, 'color', 'blue')

    s.remove(0, 'color')

    repr(s)


def test_registry():

    s = _JGraphTAttributesRegistry()

    s.put('color', 'vertex', None, None)
    s.remove('color', 'vertex')

    repr(s)
