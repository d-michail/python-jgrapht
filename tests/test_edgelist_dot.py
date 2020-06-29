import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import read_edgelist_dot, parse_edgelist_dot

input1 = """digraph G {\n  0 [label="node 0"];\n  1;\n  2;\n  3;\n  0 -> 1 [cost="33.0"];\n  0 -> 2;\n  0 -> 3;\n  2 -> 3;\n}\n"""

def test_input_dot(tmpdir):
    tmpfile = tmpdir.join("dot.out")
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

    edgelist = read_edgelist_dot(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs == {'0': {'label': 'node 0'}}
    assert e_attrs == {0: {'cost': '33.0'}}

    assert list(edgelist) == [('0','1',1.0), ('0','2',1.0), ('0','3',1.0), ('2','3',1.0)]


def test_input_dot_no_attrs(tmpdir):
    tmpfile = tmpdir.join("dot.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(input1)

    edgelist = read_edgelist_dot(tmpfilename)

    assert list(edgelist) == [('0','1',1.0), ('0','2',1.0), ('0','3',1.0), ('2','3',1.0)]


def test_input_dot_from_string_no_attrs(tmpdir):
    edgelist = parse_edgelist_dot(input1)

    assert list(edgelist) == [('0','1',1.0), ('0','2',1.0), ('0','3',1.0), ('2','3',1.0)]


def test_input_dot_from_string(tmpdir):
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

    edgelist = parse_edgelist_dot(
        input1,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs == {'0': {'label': 'node 0'}}
    assert e_attrs == {0: {'cost': '33.0'}}

    assert list(edgelist) == [('0','1',1.0), ('0','2',1.0), ('0','3',1.0), ('2','3',1.0)]

