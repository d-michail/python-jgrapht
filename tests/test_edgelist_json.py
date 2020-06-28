import pytest

from jgrapht.io.edgelist import read_edgelist_json, parse_edgelist_json

expected_escaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'

expected1_escaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 0"}],"edges":[]}'
expected1_unescaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"κόμβος 0"}],"edges":[]}'

expected2 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0"},{"id":"1"},{"id":"2"},{"id":"3"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"2","target":"3"}]}'
expected3 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"label 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'


def test_input_json(tmpdir):
    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected_escaped)

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

    edgelist = read_edgelist_json(
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['0']["label"] == "κόμβος 0"
    assert v_attrs['3']["label"] == "label 3"
    assert e_attrs[9]["label"] == "edge 1-2"

    repr(edgelist)

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


def test_input_json_no_attrs(tmpdir):
    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected_escaped)

    edgelist = read_edgelist_json(tmpfilename)

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


def test_input_json_no_attrs_from_string():
    edgelist = parse_edgelist_json(expected_escaped)

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


def test_input_json_from_string():

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

    edgelist = parse_edgelist_json(
        expected_escaped,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
    )

    assert v_attrs['0']["label"] == "κόμβος 0"
    assert v_attrs['3']["label"] == "label 3"
    assert e_attrs[9]["label"] == "edge 1-2"

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
