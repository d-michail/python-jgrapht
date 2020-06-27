import pytest

from jgrapht import create_graph
from jgrapht.utils import create_edge_supplier, create_vertex_supplier

from jgrapht.io.exporters import write_gml, generate_gml
from jgrapht.io.importers import read_gml, parse_gml


expected = """Creator "JGraphT GML Exporter"
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

expected2 = r"""Creator "JGraphT GML Exporter"
Version 1
graph
[
	label ""
	directed 1
	node
	[
		id 0
	]
	node
	[
		id 1
	]
	node
	[
		id 2
	]
	node
	[
		id 3
	]
	edge
	[
		source 0
		target 1
	]
	edge
	[
		source 0
		target 2
	]
	edge
	[
		source 0
		target 3
	]
	edge
	[
		source 2
		target 3
	]
]
"""

expected3 = r"""Creator "JGraphT GML Exporter"
Version 1
graph
[
	label ""
	directed 1
	node
	[
		id 0
	]
	node
	[
		id 1
	]
	edge
	[
		source 0
		target 1
	]
]
"""


expected4 = r"""Creator "JGraphT GML Exporter"
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
	]
	node
	[
		id 5
	]
	node
	[
		id 6
	]
	node
	[
		id 7
	]
	node
	[
		id 8
	]
	node
	[
		id 9
	]
	edge
	[
		source 0
		target 1
	]
	edge
	[
		source 0
		target 2
	]
	edge
	[
		source 0
		target 3
	]
	edge
	[
		source 0
		target 4
	]
	edge
	[
		source 0
		target 5
	]
	edge
	[
		source 0
		target 6
	]
	edge
	[
		source 0
		target 7
	]
	edge
	[
		source 0
		target 8
	]
	edge
	[
		source 0
		target 9
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
	]
	edge
	[
		source 3
		target 4
	]
	edge
	[
		source 4
		target 5
	]
	edge
	[
		source 5
		target 6
	]
	edge
	[
		source 6
		target 7
	]
	edge
	[
		source 7
		target 8
	]
	edge
	[
		source 8
		target 9
	]
	edge
	[
		source 9
		target 1
	]
]
"""

expected5 = r"""Creator "JGraphT GML Exporter"
Version 1
graph
[
	label ""
	directed 1
	node
	[
		id 0
		color "red"
	]
	node
	[
		id 2
	]
	edge
	[
		source 0
		target 2
		type "forward"
	]
	edge
	[
		source 2
		target 0
		type "backward"
	]
]
"""


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


def test_output_gml(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    v_labels = {
        0: {"label": "label 0"},
        1: {"label": "label 1"},
        2: {"label": "label 2"},
        3: {"label": "label 3"},
    }
    e_labels = {9: {"label": "edge 1-2"}}
    write_gml(g, tmpfilename, False, True, True, v_labels, e_labels)

    with open(tmpfilename, "r", encoding="utf-8") as f:
        contents = f.read()

    print(contents)

    assert contents == expected


def test_output_gml_without_automatic_labels(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    v_labels = {
        0: {"label": "label 0"},
        1: {"label": "label 1"},
        2: {"label": "label 2"},
        3: {"label": "label 3"},
    }
    e_labels = {9: {"label": "edge 1-2"}}
    write_gml(g, tmpfilename, False, False, False, v_labels, e_labels)

    with open(tmpfilename, "r", encoding="utf-8") as f:
        contents = f.read()

    print(contents)

    assert contents == expected4


def test_input_gml(tmpdir):
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def va_cb(vertex, attribute_name, attribute_value):
        print(
            "Vertex {}, attr {}, value {}".format(
                vertex, attribute_name, attribute_value
            )
        )
        if vertex == 2 and attribute_name == "label":
            assert attribute_value == "label 2"
        if vertex == 5 and attribute_name == "label":
            assert attribute_value == "5"

    def ea_cb(edge, attribute_name, attribute_value):
        print(
            "Edge {}, attr {}, value {}".format(edge, attribute_name, attribute_value)
        )
        if edge == 9 and attribute_name == "label":
            assert attribute_value == "edge 1-2"

    read_gml(g, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)


def test_input_gml_from_string(tmpdir):

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

    parse_gml(g, expected, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert v_attrs[2]["label"] == "label 2"
    assert v_attrs[5]["label"] == "5"
    assert e_attrs[9]["label"] == "edge 1-2"


def test_input_anyhashableg_gml_from_file(tmpdir):
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
		vertex_supplier=create_vertex_supplier(),
		edge_supplier=create_edge_supplier(),
    )

    read_gml(g, tmpfilename)

    assert g.vertices == {'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9'}



def test_input_gml_nocallbacks(tmpdir):
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    read_gml(g, tmpfilename)


def test_input_gml_from_string_create_new_vertices():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    input_string = "Version 1 graph [ directed 0 node [ id 5 ] node [ id 7 ] edge [ source 5 target 7 ] ]"

    parse_gml(g, input_string)

    assert g.vertices == set([0, 1])


def test_input_gml_from_string_preserve_ids():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    input_string = "Version 1 graph [ directed 0 node [ id 5 ] node [ id 7 ] edge [ source 5 target 7 ] ]"

    def identity(x):
        return x

    parse_gml(g, input_string, identity)

    assert g.vertices == set([5, 7])


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

    out = generate_gml(g)
    assert out.splitlines() == expected2.splitlines()


def test_input_gml_from_string_rename_ids(tmpdir):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def import_id(id):
        return id + 5

    parse_gml(g, expected3, import_id_cb=import_id)

    assert g.vertices == {5, 6}


def test_output_property_graph_to_string():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex(0)
    g.add_vertex(2)

    g.add_edge(0, 2, edge="e1")
    g.add_edge(2, 0, edge="e2")

    g.vertex_attrs[0]["color"] = "red"

    g.edge_attrs["e1"]["type"] = "forward"
    g.edge_attrs["e2"]["type"] = "backward"

    # test bad keys are ignores
    more_vertex_props = {1: {"color": "green"}}
    more_edge_props = {"e4": {"type": "forward"}}

    out = generate_gml(
        g, per_vertex_attrs_dict=more_vertex_props, per_edge_attrs_dict=more_edge_props
    )

    print(out)

    assert out.splitlines() == expected5.splitlines()


def test_read_gml_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    def import_id_cb(id):
        return "v{}".format(id + 1)

    parse_gml(g, expected, import_id_cb=import_id_cb)

    assert g.vertices == {"v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"}
    assert len(g.edges) == 18
    assert g.edge_tuple("e6") == ("v1", "v8", 1.0)
    assert g.vertex_attrs["v2"]["label"] == "label 1"
    assert g.edge_attrs["e15"]["label"] == "15"


def test_read_gml_property_graph_from_string_no_id_map():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    parse_gml(g, expected)

    assert g.vertices == {"v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"}
    assert len(g.edges) == 18
    assert g.edge_tuple("e6") == ("v0", "v7", 1.0)
    assert g.vertex_attrs["v1"]["label"] == "label 1"
    assert g.edge_attrs["e15"]["label"] == "15"


def test_output_bad_property_graph_to_string():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex('0')
    g.add_vertex('2')

    g.add_edge('0', '2', edge="e1")
    g.add_edge('2', '0', edge="e2")

    g.vertex_attrs['0']["color"] = "red"

    g.edge_attrs["e1"]["type"] = "forward"
    g.edge_attrs["e2"]["type"] = "backward"

    # test bad keys are ignores
    more_vertex_props = {1: {"color": "green"}}
    more_edge_props = {"e4": {"type": "forward"}}

    with pytest.raises(TypeError):
        out = generate_gml(
            g, per_vertex_attrs_dict=more_vertex_props, per_edge_attrs_dict=more_edge_props
        )


def test_output_bad_property_graph_to_string_with_convert():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex('0')
    g.add_vertex('2')

    g.add_edge('0', '2', edge="e1")
    g.add_edge('2', '0', edge="e2")

    g.vertex_attrs['0']["color"] = "red"

    g.edge_attrs["e1"]["type"] = "forward"
    g.edge_attrs["e2"]["type"] = "backward"

    # test bad keys are ignores
    more_vertex_props = {'1': {"color": "green"}}
    more_edge_props = {"e4": {"type": "forward"}}

    def convert(id): 
        return int(id)

    out = generate_gml(
        g, per_vertex_attrs_dict=more_vertex_props, per_edge_attrs_dict=more_edge_props, export_vertex_id_cb=convert
    )

    assert out.splitlines() == expected5.splitlines()


    def bad_convert(id):
        return -int(id)
    
    with pytest.raises(ValueError):
        out = generate_gml(
            g, per_vertex_attrs_dict=more_vertex_props, per_edge_attrs_dict=more_edge_props, export_vertex_id_cb=bad_convert
        )

def test_write_gml_with_bad_converter(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    v_labels = {
        0: {"label": "label 0"},
        1: {"label": "label 1"},
        2: {"label": "label 2"},
        3: {"label": "label 3"},
    }
    e_labels = {9: {"label": "edge 1-2"}}

    def bad_convert(id):
        return str(id)

    with pytest.raises(TypeError):
        write_gml(g, tmpfilename, False, True, True, v_labels, e_labels, export_vertex_id_cb=bad_convert)


def test_write_gml_with_bad_converter2(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    v_labels = {
        0: {"label": "label 0"},
        1: {"label": "label 1"},
        2: {"label": "label 2"},
        3: {"label": "label 3"},
    }
    e_labels = {9: {"label": "edge 1-2"}}

    def bad_convert(id):
        return -id

    with pytest.raises(ValueError):
        write_gml(g, tmpfilename, False, True, True, v_labels, e_labels, export_vertex_id_cb=bad_convert)
