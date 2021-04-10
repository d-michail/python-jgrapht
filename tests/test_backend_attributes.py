import pytest

from jgrapht import create_graph, GraphBackend
import jgrapht._backend as _backend

from jgrapht._internals._attributes import (
    _JGraphTAttributeStore,
    _JGraphTAttributesRegistry,
)


def test_store_int_graph():

    g = create_graph(backend=GraphBackend.INT_GRAPH)
    handle = _backend.jgrapht_xx_attributes_store_create()
    s = _JGraphTAttributeStore(handle=handle, graph=g)

    s.put(0, 'color', 'red')
    s.put(1, 'color', 'blue')

    s.remove(0, 'color')

    repr(s)


def test_store_ref_graph():

    g = create_graph(backend=GraphBackend.REF_GRAPH)
    handle = _backend.jgrapht_xx_attributes_store_create()
    s = _JGraphTAttributeStore(handle=handle, graph=g)

    s.put("0", 'color', 'red')
    s.put("1", 'color', 'blue')

    s.remove("0", 'color')

    repr(s)


def test_registry():

    s = _JGraphTAttributesRegistry()

    s.put('color', 'vertex', None, None)
    s.remove('color', 'vertex')

    repr(s)
