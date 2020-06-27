import pytest

from jgrapht import create_graph
from jgrapht.utils import create_edge_supplier, create_vertex_supplier

from jgrapht.io.exporters import write_graphml, generate_graphml
from jgrapht.io.importers import read_graphml, parse_graphml


expected1 = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph edgedefault="directed">
        <node id="0"/>
        <node id="1"/>
        <node id="2"/>
        <node id="3"/>
        <edge source="0" target="1"/>
        <edge source="0" target="2"/>
        <edge source="0" target="3"/>
        <edge source="2" target="3"/>
    </graph>
</graphml>"""


expected2 = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <key id="edge_weight_key" for="edge" attr.name="weight" attr.type="double">
        <default>1.0</default>
    </key>
    <graph edgedefault="directed">
        <node id="0"/>
        <node id="1"/>
        <node id="2"/>
        <node id="3"/>
        <edge source="0" target="1">
            <data key="edge_weight_key">3.3</data>
        </edge>
        <edge source="0" target="2">
            <data key="edge_weight_key">4.4</data>
        </edge>
        <edge source="0" target="3"/>
        <edge source="2" target="3"/>
    </graph>
</graphml>"""


expected3 = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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


expected4 = r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
        <edge source="8" target="9">
            <data key="key0">48.5</data>
        </edge>
        <edge source="9" target="1">
            <data key="edge_weight_key">33.3</data>
        </edge>
    </graph>
</graphml>"""


def test_export_import(tmpdir):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
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
    g.add_edge(9, 1, weight=33.3)

    assert len(g.edges) == 18

    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    attrs = [("cost", "edge", "double", None), ("name", "node", "string", None)]

    v_dict = {0: {"name": "κόμβος 0"}, 1: {"name": "node 1"}}
    e_dict = {11: {"cost": "100.0"}, 17: {"cost": "48.5"}}

    write_graphml(
        g,
        tmpfilename,
        attrs=attrs,
        per_vertex_attrs_dict=v_dict,
        per_edge_attrs_dict=e_dict,
        export_edge_weights=True,
    )

    # read back

    g1 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
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

    read_graphml(
        g1,
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=False,
    )

    print(e_attrs)

    assert v_attrs[0]["name"] == "κόμβος 0"
    assert v_attrs[1]["name"] == "node 1"
    assert e_attrs[8]["weight"] == "1.0"
    assert e_attrs[11]["cost"] == "100.0"
    assert e_attrs[11]["weight"] == "1.0"
    assert e_attrs[17]["cost"] == "48.5"
    assert e_attrs[17]["weight"] == "33.3"

    assert g1.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g1.contains_edge_between(6, 7)
    assert not g1.contains_edge_between(6, 8)
    assert len(g1.edges) == 18

    assert g1.get_edge_weight(17) == 33.3

    # read back with simple
    g2 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
    )

    read_graphml(
        g2,
        tmpfilename,
        vertex_attribute_cb=va_cb,
        edge_attribute_cb=ea_cb,
        simple=True,
    )

    assert g2.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g2.contains_edge_between(6, 7)
    assert not g2.contains_edge_between(6, 8)
    assert len(g2.edges) == 18

    assert g2.get_edge_weight(17) == 33.3


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

    out = generate_graphml(g)

    assert out.splitlines() == expected1.splitlines()


def test_output_to_string_with_weights():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
    )

    g.add_vertices_from(range(0, 4))

    g.add_edge(0, 1, weight=3.3)
    g.add_edge(0, 2, weight=4.4)
    g.add_edge(0, 3)
    g.add_edge(2, 3)

    out = generate_graphml(g, export_edge_weights=True)

    assert out.splitlines() == expected2.splitlines()


def test_output_to_string_with_attrs():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
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
    g.add_edge(9, 1, weight=33.3)

    assert len(g.edges) == 18

    attrs = [("cost", "edge", "double", None), ("name", "node", "string", None)]

    v_dict = {0: {"name": "κόμβος 0"}, 1: {"name": "node 1"}}
    e_dict = {17: {"cost": "48.5"}}

    out = generate_graphml(
        g,
        attrs=attrs,
        per_vertex_attrs_dict=v_dict,
        per_edge_attrs_dict=e_dict,
        export_edge_weights=True,
    )

    assert out.splitlines() == expected3.splitlines()


def test_property_graph_output_to_string_with_attrs():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1, edge="e01")
    g.add_edge(0, 2, edge="e02")
    g.add_edge(0, 3, edge="e03")
    g.add_edge(0, 4, edge="e04")
    g.add_edge(0, 5, edge="e05")
    g.add_edge(0, 6, edge="e06")
    g.add_edge(0, 7, edge="e07")
    g.add_edge(0, 8, edge="e08")
    g.add_edge(0, 9, edge="e09")

    g.add_edge(1, 2, edge="e12")
    g.add_edge(2, 3, edge="e23")
    g.add_edge(3, 4, edge="e34")
    g.add_edge(4, 5, edge="e45")
    g.add_edge(5, 6, edge="e56")
    g.add_edge(6, 7, edge="e67")
    g.add_edge(7, 8, edge="e78")
    g.add_edge(8, 9, edge="e89")
    g.add_edge(9, 1, edge="e91")

    g.set_edge_weight("e91", 33.3)

    assert len(g.edges) == 18

    attrs = [("cost", "edge", "double", None), ("name", "node", "string", None)]

    v_dict = {0: {"name": "κόμβος 0"}, 1: {"name": "node 1"}}
    e_dict = {"e89": {"cost": "48.5"}}

    out = generate_graphml(
        g,
        attrs=attrs,
        per_vertex_attrs_dict=v_dict,
        per_edge_attrs_dict=e_dict,
        export_edge_weights=True,
    )

    assert out.splitlines() == expected4.splitlines()


def test_graph_from_string():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
    )

    def import_id_cb(id):
        return int(id)

    parse_graphml(
        g, expected2, import_id_cb=import_id_cb, validate_schema=True, simple=True
    )

    assert g.vertices == {0, 1, 2, 3}
    assert g.edges == {0, 1, 2, 3}

    assert g.get_edge_weight(1) == 4.4


def test_property_graph_from_string():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    def import_id_cb(id):
        return "vertex-{}".format(id)

    parse_graphml(
        g, expected2, import_id_cb=import_id_cb, validate_schema=True, simple=True
    )

    assert g.vertices == {"vertex-0", "vertex-1", "vertex-2", "vertex-3"}
    assert g.edges == {"e0", "e1", "e2", "e3"}

    assert g.edge_attrs["e1"]["weight"] == 4.4


def test_property_graph_from_string_without_importid():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    parse_graphml(g, expected2, validate_schema=True, simple=True)

    assert g.vertices == {"v0", "v1", "v2", "v3"}
    assert g.edges == {"e0", "e1", "e2", "e3"}

    assert g.edge_attrs == {
        "e0": {"source": "0", "target": "1"},
        "e1": {"source": "0", "target": "2"},
        "e2": {"source": "0", "target": "3"},
        "e3": {"source": "2", "target": "3"},
    }

    # check that we also see the weights, even if they do not appear in
    # the properties
    assert g.edge_attrs["e1"]["weight"] == 4.4

    # test weight changes also by set
    g.set_edge_weight("e1", 100.4)
    assert g.edge_attrs["e1"]["weight"] == 100.4


def test_property_graph_from_filename_without_importid(tmpdir):
    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected2)

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    read_graphml(g, tmpfilename, validate_schema=True, simple=True)

    assert g.vertices == {"v0", "v1", "v2", "v3"}
    assert g.edges == {"e0", "e1", "e2", "e3"}

    assert g.edge_attrs == {
        "e0": {"source": "0", "target": "1"},
        "e1": {"source": "0", "target": "2"},
        "e2": {"source": "0", "target": "3"},
        "e3": {"source": "2", "target": "3"},
    }

    # check that we also see the weights, even if they do not appear in
    # the properties
    assert g.edge_attrs["e1"]["weight"] == 4.4

    # test weight changes also by set
    g.set_edge_weight("e1", 100.4)
    assert g.edge_attrs["e1"]["weight"] == 100.4


def test_property_graph_from_filename_without_importid_no_simple(tmpdir):
    tmpfile = tmpdir.join("graphml.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected2)

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    read_graphml(g, tmpfilename, validate_schema=True, simple=False)

    assert g.vertices == {"v0", "v1", "v2", "v3"}
    assert g.edges == {"e0", "e1", "e2", "e3"}

    assert dict(g.edge_attrs) == {}

    # check that we also see the weights, even if they do not appear in
    # the properties
    assert g.edge_attrs["e1"]["weight"] == 4.4

    # test weight changes also by set
    g.set_edge_weight("e1", 100.4)
    assert g.edge_attrs["e1"]["weight"] == 100.4


def test_property_graph_non_weighted_from_string_without_importid():

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    parse_graphml(g, expected2, validate_schema=True, simple=True)

    assert g.vertices == {"v0", "v1", "v2", "v3"}
    assert g.edges == {"e0", "e1", "e2", "e3"}

    assert g.edge_attrs == {
        "e0": {"source": "0", "target": "1"},
        "e1": {"source": "0", "target": "2"},
        "e2": {"source": "0", "target": "3"},
        "e3": {"source": "2", "target": "3"},
    }

    # check that we also see the weights, even if they do not appear in
    # the properties
    assert g.edge_attrs["e1"]["weight"] == 1.0

    with pytest.raises(ValueError):
        g.edge_attrs["e1"]["weight"] = 2.0
