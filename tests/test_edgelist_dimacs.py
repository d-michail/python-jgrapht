import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import read_edgelist_dimacs, parse_edgelist_dimacs


input1 = """c
c SOURCE: Generated using the JGraphT library
c
p sp 10 18
a 1 2
a 1 3
a 1 4
a 1 5
a 1 6
a 1 7
a 1 8
a 1 9
a 1 10
a 2 3
a 3 4
a 4 5
a 5 6
a 6 7
a 7 8
a 8 9
a 9 10
a 10 2
"""


def test_input_dimacs_from_file_with_attrs(tmpdir):
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(input1)

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

    edgelist = read_edgelist_dimacs(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs == {}
    assert e_attrs == {}

    print([(u,v,w) for u,v,w in edgelist])

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]

def test_input_dimacs_from_file_no_attrs(tmpdir):
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(input1)

    edgelist = read_edgelist_dimacs(tmpfilename)

    print([(u,v,w) for u,v,w in edgelist])

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]


def test_input_dimacs_from_string_no_attrs(tmpdir):

    edgelist = parse_edgelist_dimacs(input1)

    print([(u,v,w) for u,v,w in edgelist])

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]


def test_input_dimacs_from_string(tmpdir):
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

    edgelist = parse_edgelist_dimacs(
        input1,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    print([(u,v,w) for u,v,w in edgelist])

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]

