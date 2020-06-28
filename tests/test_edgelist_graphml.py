import pytest

from jgrapht import create_graph

from jgrapht.io.edgelist import read_edgelist_graphml, parse_edgelist_graphml

input3 = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <key id="edge_weight_key" for="edge" attr.name="weight" attr.type="double">
        <default>1.0</default>
    </key>
    <key id="key0" for="edge" attr.name="cost" attr.type="double"/>
    <key id="key1" for="node" attr.name="name" attr.type="string"/>
    <graph edgedefault="directed">
        <node id="0">
            <data key="key1">κόμβος 0</data>
        </node>
        <node id="1">
            <data key="key1">node 1</data>
        </node>
        <node id="2"/>
        <node id="3"/>
        <node id="4"/>
        <node id="5"/>
        <node id="6"/>
        <node id="7"/>
        <node id="8"/>
        <node id="9"/>
        <edge source="0" target="1"/>
        <edge source="0" target="2"/>
        <edge source="0" target="3"/>
        <edge source="0" target="4"/>
        <edge source="0" target="5"/>
        <edge source="0" target="6"/>
        <edge source="0" target="7"/>
        <edge source="0" target="8"/>
        <edge source="0" target="9"/>
        <edge source="1" target="2"/>
        <edge source="2" target="3"/>
        <edge source="3" target="4"/>
        <edge source="4" target="5"/>
        <edge source="5" target="6"/>
        <edge source="6" target="7"/>
        <edge source="7" target="8"/>
        <edge source="8" target="9"/>
        <edge source="9" target="1">
            <data key="edge_weight_key">33.3</data>
            <data key="key0">48.5</data>
        </edge>
    </graph>
</graphml>"""


def test_input3_graphml(tmpdir):
    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w", encoding='utf-8') as f:
        f.write(input3)

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

    edgelist = read_edgelist_graphml(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=False,
    )

    assert v_attrs == {'0': {"name": "κόμβος 0"}, '1': {"name": "node 1"}}

    assert e_attrs == {
        0: {"weight": "1.0"},
        1: {"weight": "1.0"},
        2: {"weight": "1.0"},
        3: {"weight": "1.0"},
        4: {"weight": "1.0"},
        5: {"weight": "1.0"},
        6: {"weight": "1.0"},
        7: {"weight": "1.0"},
        8: {"weight": "1.0"},
        9: {"weight": "1.0"},
        10: {"weight": "1.0"},
        11: {"weight": "1.0"},
        12: {"weight": "1.0"},
        13: {"weight": "1.0"},
        14: {"weight": "1.0"},
        15: {"weight": "1.0"},
        16: {"weight": "1.0"},
        17: {"weight": "33.3", "cost": "48.5"},
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
        ('9', '1', 33.3),
    ]


def test_input3_graphml_simple(tmpdir):
    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w", encoding='utf-8') as f:
        f.write(input3)

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

    edgelist = read_edgelist_graphml(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=True,
    )

    assert v_attrs == {
        '0': {"id": "0", "name": "κόμβος 0"},
        '1': {"id": "1", "name": "node 1"},
        '2': {"id": "2"},
        '3': {"id": "3"},
        '4': {"id": "4"},
        '5': {"id": "5"},
        '6': {"id": "6"},
        '7': {"id": "7"},
        '8': {"id": "8"},
        '9': {"id": "9"},
    }

    assert e_attrs == {
        0: {"source": "0", "target": "1"},
        1: {"source": "0", "target": "2"},
        2: {"source": "0", "target": "3"},
        3: {"source": "0", "target": "4"},
        4: {"source": "0", "target": "5"},
        5: {"source": "0", "target": "6"},
        6: {"source": "0", "target": "7"},
        7: {"source": "0", "target": "8"},
        8: {"source": "0", "target": "9"},
        9: {"source": "1", "target": "2"},
        10: {"source": "2", "target": "3"},
        11: {"source": "3", "target": "4"},
        12: {"source": "4", "target": "5"},
        13: {"source": "5", "target": "6"},
        14: {"source": "6", "target": "7"},
        15: {"source": "7", "target": "8"},
        16: {"source": "8", "target": "9"},
        17: {"source": "9", "target": "1", "cost": "48.5", "weight": "33.3"},
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


def test_input3_from_string_graphml(tmpdir):
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

    edgelist = parse_edgelist_graphml(
        input3,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=False,
    )

    assert v_attrs == {'0': {"name": "κόμβος 0"}, '1': {"name": "node 1"}}

    assert e_attrs == {
        0: {"weight": "1.0"},
        1: {"weight": "1.0"},
        2: {"weight": "1.0"},
        3: {"weight": "1.0"},
        4: {"weight": "1.0"},
        5: {"weight": "1.0"},
        6: {"weight": "1.0"},
        7: {"weight": "1.0"},
        8: {"weight": "1.0"},
        9: {"weight": "1.0"},
        10: {"weight": "1.0"},
        11: {"weight": "1.0"},
        12: {"weight": "1.0"},
        13: {"weight": "1.0"},
        14: {"weight": "1.0"},
        15: {"weight": "1.0"},
        16: {"weight": "1.0"},
        17: {"weight": "33.3", "cost": "48.5"},
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
        ('9', '1', 33.3),
    ]


def test_input3_from_string_graphml_simple(tmpdir):
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

    edgelist = parse_edgelist_graphml(
        input3,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=True,
    )

    assert v_attrs == {
        '0': {"id": "0", "name": "κόμβος 0"},
        '1': {"id": "1", "name": "node 1"},
        '2': {"id": "2"},
        '3': {"id": "3"},
        '4': {"id": "4"},
        '5': {"id": "5"},
        '6': {"id": "6"},
        '7': {"id": "7"},
        '8': {"id": "8"},
        '9': {"id": "9"},
    }
    
    assert e_attrs == {
        0: {"source": "0", "target": "1"},
        1: {"source": "0", "target": "2"},
        2: {"source": "0", "target": "3"},
        3: {"source": "0", "target": "4"},
        4: {"source": "0", "target": "5"},
        5: {"source": "0", "target": "6"},
        6: {"source": "0", "target": "7"},
        7: {"source": "0", "target": "8"},
        8: {"source": "0", "target": "9"},
        9: {"source": "1", "target": "2"},
        10: {"source": "2", "target": "3"},
        11: {"source": "3", "target": "4"},
        12: {"source": "4", "target": "5"},
        13: {"source": "5", "target": "6"},
        14: {"source": "6", "target": "7"},
        15: {"source": "7", "target": "8"},
        16: {"source": "8", "target": "9"},
        17: {"source": "9", "target": "1", "cost": "48.5", "weight": "33.3"},
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


def test_input3_from_string_graphml_no_attrs(tmpdir):
    edgelist = parse_edgelist_graphml(
        input3,
        simple=False,
    )

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
        ('9', '1', 33.3),
    ]


def test_input3_graphml_no_attrs(tmpdir):
    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w", encoding='utf-8') as f:
        f.write(input3)

    edgelist = read_edgelist_graphml(
        tmpfilename,
        simple=False,
    )

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
        ('9', '1', 33.3),
    ]