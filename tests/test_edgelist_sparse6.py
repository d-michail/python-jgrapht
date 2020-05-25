import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import (
    parse_edgelist_graph6sparse6,
    read_edgelist_graph6sparse6,
)

    # out = generate_sparse6(g)
    # assert out == ":Cca"

    # out = generate_graph6(g)
    # assert out == "Ct"


def test_input_sparse6_from_file(tmpdir):
    tmpfile = tmpdir.join("sparse6.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(":Cca")

    def import_id(id):
        return id

    edgelist = read_edgelist_graph6sparse6(tmpfilename, import_id_cb=import_id)

    assert list(edgelist) == [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (2, 3, 1.0)]


def test_input_sparse6_with_attrs_from_file(tmpdir):
    tmpfile = tmpdir.join("sparse6.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(":Cca")

    v_attrs = dict()
    e_attrs = dict()

    # test that you read back unescaped
    def va_cb(vertex, attribute_name, attribute_value):
        if vertex not in v_attrs:
            v_attrs[vertex] = {}
        v_attrs[vertex][attribute_name] = attribute_value

    def ea_cb(edge, attribute_name, attribute_value):
        if edge not in e_attrs:
            e_attrs[edge] = {}
        e_attrs[edge][attribute_name] = attribute_value

    def import_id(id):
        return id

    edgelist = read_edgelist_graph6sparse6(tmpfilename, import_id_cb=import_id, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert list(edgelist) == [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (2, 3, 1.0)]
    assert v_attrs == {}
    assert e_attrs == {}


def test_input_sparse6_from_string_with_attrs(tmpdir):
    v_attrs = dict()
    e_attrs = dict()

    # test that you read back unescaped
    def va_cb(vertex, attribute_name, attribute_value):
        if vertex not in v_attrs:
            v_attrs[vertex] = {}
        v_attrs[vertex][attribute_name] = attribute_value

    def ea_cb(edge, attribute_name, attribute_value):
        if edge not in e_attrs:
            e_attrs[edge] = {}
        e_attrs[edge][attribute_name] = attribute_value

    def import_id(id):
        return id

    edgelist = parse_edgelist_graph6sparse6(":Cca", import_id_cb=import_id, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert list(edgelist) == [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (2, 3, 1.0)]
    assert v_attrs == {}
    assert e_attrs == {}


def test_input_sparse6_from_string(tmpdir):

    def import_id(id):
        return id

    edgelist = parse_edgelist_graph6sparse6(":Cca", import_id_cb=import_id)

    print(edgelist)

    assert list(edgelist) == [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (2, 3, 1.0)]


def test_input_graph6_from_file(tmpdir):
    tmpfile = tmpdir.join("graph6.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write("Ct")

    def import_id(id):
        return id

    edgelist = read_edgelist_graph6sparse6(tmpfilename, import_id_cb=import_id)

    assert list(edgelist) == [(1, 0, 1.0), (2, 0, 1.0), (3, 0, 1.0), (3, 2, 1.0)]


def test_input_graph6_with_attrs_from_file(tmpdir):
    tmpfile = tmpdir.join("graph6.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write("Ct")

    v_attrs = dict()
    e_attrs = dict()

    # test that you read back unescaped
    def va_cb(vertex, attribute_name, attribute_value):
        if vertex not in v_attrs:
            v_attrs[vertex] = {}
        v_attrs[vertex][attribute_name] = attribute_value

    def ea_cb(edge, attribute_name, attribute_value):
        if edge not in e_attrs:
            e_attrs[edge] = {}
        e_attrs[edge][attribute_name] = attribute_value

    def import_id(id):
        return id

    edgelist = read_edgelist_graph6sparse6(tmpfilename, import_id_cb=import_id, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert list(edgelist) == [(1, 0, 1.0), (2, 0, 1.0), (3, 0, 1.0), (3, 2, 1.0)]
    assert v_attrs == {}
    assert e_attrs == {}


def test_input_graph6_from_string_with_attrs(tmpdir):
    v_attrs = dict()
    e_attrs = dict()

    # test that you read back unescaped
    def va_cb(vertex, attribute_name, attribute_value):
        if vertex not in v_attrs:
            v_attrs[vertex] = {}
        v_attrs[vertex][attribute_name] = attribute_value

    def ea_cb(edge, attribute_name, attribute_value):
        if edge not in e_attrs:
            e_attrs[edge] = {}
        e_attrs[edge][attribute_name] = attribute_value

    def import_id(id):
        return id

    edgelist = parse_edgelist_graph6sparse6("Ct", import_id_cb=import_id, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert list(edgelist) == [(1, 0, 1.0), (2, 0, 1.0), (3, 0, 1.0), (3, 2, 1.0)]
    assert v_attrs == {}
    assert e_attrs == {}


def test_input_graph6_from_string(tmpdir):

    def import_id(id):
        return id

    edgelist = parse_edgelist_graph6sparse6("Ct", import_id_cb=import_id)

    print(edgelist)

    assert list(edgelist) == [(1, 0, 1.0), (2, 0, 1.0), (3, 0, 1.0), (3, 2, 1.0)]


def test_input_graph6_no_import_cb(tmpdir):

    edgelist = parse_edgelist_graph6sparse6("Ct")

    print(edgelist)

    assert list(edgelist) == [(1, 0, 1.0), (2, 0, 1.0), (3, 0, 1.0), (3, 2, 1.0)]