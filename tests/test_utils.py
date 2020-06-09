import pytest

import jgrapht.utils as utils

def test_integer_supplier():

    s = utils.IntegerSupplier()

    assert s() == 0
    assert s() == 1
    assert s() == 2
    assert s() == 3
    assert s() == 4

    s = utils.IntegerSupplier(start=5)

    assert s() == 5
    assert s() == 6
    assert s() == 7
    assert s() == 8
    assert s() == 9


def test_string_supplier():

    s = utils.StringSupplier()

    assert s() == '0'
    assert s() == '1'
    assert s() == '2'
    assert s() == '3'
    assert s() == '4'

    s = utils.StringSupplier(start=5)

    assert s() == '5'
    assert s() == '6'
    assert s() == '7'
    assert s() == '8'
    assert s() == '9'


    s = utils.StringSupplier(prefix='prefix', start=5)

    assert s() == 'prefix5'
    assert s() == 'prefix6'
    assert s() == 'prefix7'
    assert s() == 'prefix8'
    assert s() == 'prefix9'

def test_edge_supplier():

    es = utils.create_edge_supplier()

    assert es() == 'e0'
    assert es() == 'e1'
    assert es() == 'e2'

    es = utils.create_edge_supplier(prefix='edge')
    assert es() == 'edge0'
    assert es() == 'edge1'
    assert es() == 'edge2'

    es = utils.create_edge_supplier(type='int', prefix='edge')
    assert es() == 0
    assert es() == 1
    assert es() == 2

    es = utils.create_edge_supplier(type='int', start=3)
    assert es() == 3
    assert es() == 4
    assert es() == 5


def test_vertex_supplier():

    es = utils.create_vertex_supplier()

    assert es() == 'v0'
    assert es() == 'v1'
    assert es() == 'v2'

    es = utils.create_vertex_supplier(prefix='vertex')
    assert es() == 'vertex0'
    assert es() == 'vertex1'
    assert es() == 'vertex2'

    es = utils.create_vertex_supplier(type='int', prefix='vertex')
    assert es() == 0
    assert es() == 1
    assert es() == 2

    es = utils.create_vertex_supplier(type='int', start=3)
    assert es() == 3
    assert es() == 4
    assert es() == 5

