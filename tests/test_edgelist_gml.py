import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import read_edgelist_gml, parse_edgelist_gml

input1 = """Creator "JGraphT GML Exporter"
Version 1
graph
[
	label ""
	directed 0
	node
	[
		id 0
		label "label 0"
	]
	node
	[
		id 1
		label "label 1"
	]
	node
	[
		id 2
		label "label 2"
	]
	node
	[
		id 3
		label "label 3"
	]
	node
	[
		id 4
		label "4"
	]
	node
	[
		id 5
		label "5"
	]
	node
	[
		id 6
		label "6"
	]
	node
	[
		id 7
		label "7"
	]
	node
	[
		id 8
		label "8"
	]
	node
	[
		id 9
		label "9"
	]
	edge
	[
		source 0
		target 1
		label "0"
	]
	edge
	[
		source 0
		target 2
		label "1"
	]
	edge
	[
		source 0
		target 3
		label "2"
	]
	edge
	[
		source 0
		target 4
		label "3"
	]
	edge
	[
		source 0
		target 5
		label "4"
	]
	edge
	[
		source 0
		target 6
		label "5"
	]
	edge
	[
		source 0
		target 7
		label "6"
	]
	edge
	[
		source 0
		target 8
		label "7"
	]
	edge
	[
		source 0
		target 9
		label "8"
	]
	edge
	[
		source 1
		target 2
		label "edge 1-2"
	]
	edge
	[
		source 2
		target 3
		label "10"
	]
	edge
	[
		source 3
		target 4
		label "11"
	]
	edge
	[
		source 4
		target 5
		label "12"
	]
	edge
	[
		source 5
		target 6
		label "13"
	]
	edge
	[
		source 6
		target 7
		label "14"
	]
	edge
	[
		source 7
		target 8
		label "15"
	]
	edge
	[
		source 8
		target 9
		label "16"
	]
	edge
	[
		source 9
		target 1
		label "17"
	]
]
"""


def test_input_gml(tmpdir):
    tmpfile = tmpdir.join("gml.out")
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

    edgelist = read_edgelist_gml(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['1']["label"] == "label 1"
    assert v_attrs['2']["label"] == "label 2"

    print(e_attrs)

    assert e_attrs == {
        0: {"label": "0"},
        1: {"label": "1"},
        2: {"label": "2"},
        3: {"label": "3"},
        4: {"label": "4"},
        5: {"label": "5"},
        6: {"label": "6"},
        7: {"label": "7"},
        8: {"label": "8"},
        9: {"label": "edge 1-2"},
        10: {"label": "10"},
        11: {"label": "11"},
        12: {"label": "12"},
        13: {"label": "13"},
        14: {"label": "14"},
        15: {"label": "15"},
        16: {"label": "16"},
        17: {"label": "17"},
    }

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


def test_input_gml_no_attrs(tmpdir):
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(input1)

    edgelist = read_edgelist_gml(tmpfilename)

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


def test_input_gml_from_string_no_attrs(tmpdir):
    edgelist = parse_edgelist_gml(input1)

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


def test_input_gml_from_string(tmpdir):
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

    edgelist = parse_edgelist_gml(
        input1,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['1']["label"] == "label 1"
    assert v_attrs['2']["label"] == "label 2"

    assert e_attrs == {
        0: {"label": "0"},
        1: {"label": "1"},
        2: {"label": "2"},
        3: {"label": "3"},
        4: {"label": "4"},
        5: {"label": "5"},
        6: {"label": "6"},
        7: {"label": "7"},
        8: {"label": "8"},
        9: {"label": "edge 1-2"},
        10: {"label": "10"},
        11: {"label": "11"},
        12: {"label": "12"},
        13: {"label": "13"},
        14: {"label": "14"},
        15: {"label": "15"},
        16: {"label": "16"},
        17: {"label": "17"},
    }

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

def test_input_gml_from_string_with_identity(tmpdir):
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

    edgelist = parse_edgelist_gml(
        input1,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['1']["label"] == "label 1"
    assert v_attrs['2']["label"] == "label 2"

    assert e_attrs == {
        0: {"label": "0"},
        1: {"label": "1"},
        2: {"label": "2"},
        3: {"label": "3"},
        4: {"label": "4"},
        5: {"label": "5"},
        6: {"label": "6"},
        7: {"label": "7"},
        8: {"label": "8"},
        9: {"label": "edge 1-2"},
        10: {"label": "10"},
        11: {"label": "11"},
        12: {"label": "12"},
        13: {"label": "13"},
        14: {"label": "14"},
        15: {"label": "15"},
        16: {"label": "16"},
        17: {"label": "17"},
    }

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