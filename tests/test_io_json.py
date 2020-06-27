import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_json, generate_json
from jgrapht.io.importers import read_json, parse_json


expected_escaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'

expected1_escaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 0"}],"edges":[]}'
expected1_unescaped = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"κόμβος 0"}],"edges":[]}'

expected2 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0"},{"id":"1"},{"id":"2"},{"id":"3"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"2","target":"3"}]}'
expected3 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"label 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'
expected4 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"v0"},{"id":"v1"},{"id":"v2"},{"id":"v3"}],"edges":[{"source":"v0","target":"v1"},{"source":"v0","target":"v2"},{"source":"v0","target":"v3"},{"source":"v2","target":"v3"}]}'
expected5 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"v0","color":"red"},{"id":"v1","color":"blue"},{"id":"v2"},{"id":"v3"}],"edges":[{"source":"v0","target":"v1","capacity":"100.0"},{"source":"v0","target":"v2","capacity":"20.0","type":"directed"},{"source":"v0","target":"v3"},{"source":"v2","target":"v3"}]}'


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(0, 6)
    g.add_edge(0, 7)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


def test_output_to_file_json(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    v_labels = {
        0: {"label": "κόμβος 0"},
        1: {"label": "label 1"},
        2: {"label": "label 2"},
        3: {"label": "label 3"},
    }
    e_labels = {9: {"label": "edge 1-2"}}
    write_json(g, tmpfilename, v_labels, e_labels)

    with open(tmpfilename, "r") as f:
        contents = f.read()

    assert contents == expected_escaped


def test_output_to_string():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
    )

    g.add_vertices_from(range(0, 4))

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(2, 3)

    out = generate_json(g)
    assert out.splitlines() == expected2.splitlines()


def test_output_to_string_with_labels():
    g = build_graph()

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
    )
    g.add_vertex(0)
    v_labels = {0: {"label": "κόμβος 0"}}

    out = generate_json(g, per_vertex_attrs_dict=v_labels)
    assert out.splitlines() == expected1_escaped.splitlines()


def test_input_json(tmpdir):
    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected_escaped)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

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

    read_json(g, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert v_attrs[0]["label"] == "κόμβος 0"
    assert v_attrs[1]["ID"] == "1"
    assert v_attrs[1]["label"] == "label 1"
    assert v_attrs[2]["label"] == "label 2"
    assert e_attrs[9]["label"] == "edge 1-2"


def test_input_json_nocallbacks(tmpdir):
    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(expected_escaped)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    read_json(g, tmpfilename)


def test_input_json_from_string_nocallbacks(tmpdir):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    parse_json(g, expected3)
    assert g.number_of_vertices == 10
    assert g.number_of_edges == 18


def test_input_json_from_string_create_new_vertices():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    input_string = r'{"version":"1","nodes":[{"id":"5"},{"id":"7"}],"edges":[{"source":"5","target":"7"}]}'
    parse_json(g, input_string)
    assert g.vertices == set([0, 1])


def test_input_json_from_string_preserve_ids():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    input_string = r'{"version":"1","nodes":[{"id":"5"},{"id":"7"}],"edges":[{"source":"5","target":"7"}]}'

    def import_id(file_id):
        return int(file_id)

    parse_json(g, input_string, import_id_cb=import_id)
    assert g.vertices == set([5, 7])


def test_input_from_string_with_labels():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def import_id(file_id):
        return int(file_id)

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

    parse_json(
        g, expected1_unescaped, import_id_cb=import_id, vertex_attribute_cb=va_cb
    )
    assert v_attrs[0]["label"] == "κόμβος 0"
    assert g.vertices == set([0])
    assert len(g.edges) == 0


def test_property_graph_output_to_string():
    pg = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    pg.add_vertex("v0")
    pg.add_vertex("v1")
    pg.add_vertex("v2")
    pg.add_vertex("v3")

    pg.add_edge("v0", "v1", edge="e01")
    pg.add_edge("v0", "v2", edge="e02")
    pg.add_edge("v0", "v3", edge="e03")
    pg.add_edge("v2", "v3", edge="e23")

    out = generate_json(pg)

    assert out.splitlines() == expected4.splitlines()


def test_property_graph_with_labels_output_to_string():
    pg = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    pg.add_vertex("v0")
    pg.add_vertex("v1")
    pg.add_vertex("v2")
    pg.add_vertex("v3")

    pg.add_edge("v0", "v1", edge="e01")
    pg.add_edge("v0", "v2", edge="e02")
    pg.add_edge("v0", "v3", edge="e03")
    pg.add_edge("v2", "v3", edge="e23")

    pg.vertex_attrs["v0"]["color"] = "red"
    pg.vertex_attrs["v1"]["color"] = "blue"

    pg.edge_attrs["e01"]["capacity"] = 100.0
    pg.edge_attrs["e02"]["capacity"] = 20.0

    extra_e_labels = {"e02": {"type": "directed"}}

    out = generate_json(pg, per_edge_attrs_dict=extra_e_labels)

    assert out.splitlines() == expected5.splitlines()


def test_property_graph_output_to_file_json(tmpdir):
    pg = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    pg.add_vertex("v0")
    pg.add_vertex("v1")
    pg.add_vertex("v2")
    pg.add_vertex("v3")

    pg.add_edge("v0", "v1", edge="e01")
    pg.add_edge("v0", "v2", edge="e02")
    pg.add_edge("v0", "v3", edge="e03")
    pg.add_edge("v2", "v3", edge="e23")

    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    write_json(pg, tmpfilename)

    with open(tmpfilename, "r") as f:
        contents = f.read()

    assert contents.splitlines() == expected4.splitlines()


def test_input_json_from_string_property_graph():
    class StringSupplier:
        def __init__(self, prefix):
            self._count = 0
            self._prefix = prefix

        def __call__(self):
            value = "{}{}".format(self._prefix, self._count)
            self._count += 1
            return value

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=StringSupplier("v"),
        edge_supplier=StringSupplier("e"),
    )
    input_string = r'{"version":"1","nodes":[{"id":"5"},{"id":"7"}],"edges":[{"source":"5","target":"7"}]}'

    def import_id_cb(file_id):
        return "vertex-{}".format(file_id)

    parse_json(g, input_string, import_id_cb=import_id_cb)
    assert g.vertices == set(["vertex-5", "vertex-7"])
    assert g.edges == set(["e0"])


def test_input_json_from_file_property_graph(tmpdir):
    class StringSupplier:
        def __init__(self, prefix):
            self._count = 0
            self._prefix = prefix

        def __call__(self):
            value = "{}{}".format(self._prefix, self._count)
            self._count += 1
            return value

    tmpfile = tmpdir.join("json.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected_escaped)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=StringSupplier("v"),
        edge_supplier=StringSupplier("e"),
    )

    def import_id_cb(file_id):
        return "myvertex-{}".format(file_id)

    read_json(g, tmpfilename, import_id_cb=import_id_cb)

    assert g.vertices == set(
        [
            "myvertex-0",
            "myvertex-1",
            "myvertex-2",
            "myvertex-3",
            "myvertex-4",
            "myvertex-5",
            "myvertex-6",
            "myvertex-7",
            "myvertex-8",
            "myvertex-9",
        ]
    )

    assert g.edges == set(
        [
            "e0",
            "e1",
            "e2",
            "e3",
            "e4",
            "e5",
            "e6",
            "e7",
            "e8",
            "e9",
            "e10",
            "e11",
            "e12",
            "e13",
            "e14",
            "e15",
            "e16",
            "e17",
        ]
    )

    print (g.vertex_attrs)
    print (g.edge_attrs)

    assert g.vertex_attrs["myvertex-0"]["label"] == "κόμβος 0"
    assert g.vertex_attrs["myvertex-1"]["ID"] == "1"
    assert g.vertex_attrs["myvertex-1"]["label"] == "label 1"
    assert g.vertex_attrs["myvertex-2"]["label"] == "label 2"
    assert g.edge_attrs["e9"]["label"] == "edge 1-2"
