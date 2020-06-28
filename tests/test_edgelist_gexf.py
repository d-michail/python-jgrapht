import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import read_edgelist_gexf, parse_edgelist_gexf


input1 = r"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft"
    version="1.2" 
    xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="undirected">
        <nodes>
            <node id="1" label="κόμβος 1"/>
            <node id="2" label="mylabel 2"/>
            <node id="3" label="3"/>
        </nodes>
        <edges>
            <edge id="1" source="2" target="3" />
            <edge id="0" source="1" target="2" />
            <edge id="2" source="3" target="1" />
        </edges>
        </graph>
</gexf>
"""

expected = r"""<?xml version="1.0" encoding="UTF-8"?><gexf xmlns="http://www.gexf.net/1.2draft" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="directed">
        <nodes>
            <node id="0" label="0"/>
            <node id="1" label="1"/>
            <node id="2" label="2"/>
            <node id="3" label="3"/>
        </nodes>
        <edges>
            <edge id="0" source="0" target="1"/>
            <edge id="1" source="0" target="2"/>
            <edge id="2" source="0" target="3"/>
            <edge id="3" source="2" target="3"/>
        </edges>
    </graph>
</gexf>
"""


def test_input_gexf(tmpdir):
    tmpfile = tmpdir.join("gexf.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w", encoding='utf-8') as f:
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

    edgelist = read_edgelist_gexf(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['1']["label"] == "κόμβος 1"
    assert v_attrs['2']["label"] == "mylabel 2"

    assert e_attrs == {
        0: {"id": "1", "source": "2", "target": "3"},
        1: {"id": "0", "source": "1", "target": "2"},
        2: {"id": "2", "source": "3", "target": "1"},
    }

    assert list(edgelist) == [('2', '3', 1), ('1', '2', 1), ('3', '1', 1)]


def test_input_gexf_no_attrs(tmpdir):
    tmpfile = tmpdir.join("gexf.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w", encoding='utf-8') as f:
        f.write(input1)

    edgelist = read_edgelist_gexf(tmpfilename)

    assert list(edgelist) == [('2', '3', 1), ('1', '2', 1), ('3', '1', 1)]


def test_input_gexf_from_string_no_attrs(tmpdir):
    edgelist = parse_edgelist_gexf(input1)

    assert list(edgelist) == [('2', '3', 1), ('1', '2', 1), ('3', '1', 1)]


def test_input_gexf_from_string(tmpdir):
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

    edgelist = parse_edgelist_gexf(
        input1,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['1']["label"] == "κόμβος 1"
    assert v_attrs['2']["label"] == "mylabel 2"

    assert e_attrs == {
        0: {"id": "1", "source": "2", "target": "3"},
        1: {"id": "0", "source": "1", "target": "2"},
        2: {"id": "2", "source": "3", "target": "1"},
    }

    assert list(edgelist) == [('2', '3', 1), ('1', '2', 1), ('3', '1', 1)]
