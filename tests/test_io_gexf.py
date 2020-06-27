import pytest

from jgrapht import create_graph
from jgrapht.utils import create_vertex_supplier, create_edge_supplier

from jgrapht.io.importers import read_gexf, parse_gexf
from jgrapht.io.exporters import write_gexf, generate_gexf


input1 = r"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft"
    version="1.2" 
    xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="undirected">
        <nodes>
            <node id="1" label="1"/>
            <node id="2" label="2"/>
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

expected1 = r"""<?xml version="1.0" encoding="UTF-8"?><gexf xmlns="http://www.gexf.net/1.2draft" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="directed">
        <nodes>
            <node id="v1" label="0"/>
            <node id="v2" label="1"/>
            <node id="v3" label="2"/>
        </nodes>
        <edges>
            <edge id="e12" source="v1" target="v2"/>
            <edge id="e13" source="v1" target="v3"/>
        </edges>
    </graph>
</gexf>
"""

expected2 = r"""<?xml version="1.0" encoding="UTF-8"?><gexf xmlns="http://www.gexf.net/1.2draft" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="directed">
        <attributes class="node">
            <attribute id="0" title="name" type="string"/>
        </attributes>
        <nodes>
            <node id="v1" label="0">
                <attvalues>
                    <attvalue for="0" value="v1"/>
                </attvalues>
            </node>
            <node id="v2" label="1">
                <attvalues>
                    <attvalue for="0" value="v2"/>
                </attvalues>
            </node>
            <node id="v3" label="2">
                <attvalues>
                    <attvalue for="0" value="v3"/>
                </attvalues>
            </node>
        </nodes>
        <edges>
            <edge id="e12" source="v1" target="v2"/>
            <edge id="e23" source="v2" target="v3"/>
        </edges>
    </graph>
</gexf>"""

def test_input_gexf(tmpdir):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    parse_gexf(g, input1, validate_schema=True)

    assert len(g.vertices) == 3
    assert len(g.edges) == 3


def test_input_gexf_with_renumbering(tmpdir):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def import_id(x):
        return int(x) + 5

    parse_gexf(g, input1, import_id_cb=import_id, validate_schema=True)

    assert len(g.vertices) == 3
    assert len(g.edges) == 3

    assert not g.contains_vertex(1)
    assert g.contains_vertex(6)


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

    tmpfile = tmpdir.join("gexf.out")
    tmpfilename = str(tmpfile)

    attrs = [("cost", "edge", "double", None), ("name", "node", "string", None)]

    v_dict = {0: {"name": "κόμβος 0"}, 1: {"name": "node 1"}}
    e_dict = {17: {"cost": "48.5"}}

    write_gexf(
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

    read_gexf(g1, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert v_attrs[0]["name"] == "κόμβος 0"
    assert v_attrs[1]["name"] == "node 1"
    assert e_attrs[17]["cost"] == "48.5"
    assert e_attrs[17]["weight"] == "33.3"
    assert e_attrs[17]["source"] == "9"
    assert e_attrs[17]["target"] == "1"
    assert e_attrs[17]["id"] == "17"

    assert g1.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g1.contains_edge_between(6, 7)
    assert not g1.contains_edge_between(6, 8)
    assert len(g1.edges) == 18

    assert g1.get_edge_weight(17) == 33.3


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

    out = generate_gexf(g)

    assert out.splitlines() == expected.splitlines()


def test_property_graph_output_to_string():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertices_from(['v1', 'v2', 'v3'])
    g.add_edge('v1', 'v2', edge='e12')
    g.add_edge('v2', 'v3', edge='e23')

    g.vertex_attrs['v1']['label'] = "0"
    g.vertex_attrs['v1']['name'] = "v1"
    g.vertex_attrs['v2']['label'] = "1"
    g.vertex_attrs['v2']['name'] = "v2"
    g.vertex_attrs['v3']['label'] = "2"
    g.vertex_attrs['v3']['name'] = "v3"

    out = generate_gexf(g, attrs=[('name', 'node', None, None)])

    assert out.splitlines() == expected2.splitlines()


def test_read_gexf_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    def import_id_cb(id):
        return 'v{}'.format(id)

    parse_gexf(g, expected2, import_id_cb=import_id_cb)

    print(g.vertices)
    print(g.edges)
    print(g.vertex_attrs)
    print(g.edge_attrs)

    assert g.vertices == {'vv1', 'vv2', 'vv3'}
    assert g.edges == {'e0', 'e1'}
    assert g.edge_tuple('e0') == ('vv1', 'vv2', 1.0)
    assert g.vertex_attrs['vv1']['label'] == '0'
    assert g.edge_attrs['e0']['id'] == 'e12'


def test_read_gexf_property_graph_from_string1():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    parse_gexf(g, expected2)

    print(g.vertices)
    print(g.edges)
    print(g.vertex_attrs)
    print(g.edge_attrs)

    assert g.vertices == {'v0', 'v1', 'v2'}
    assert g.edges == {'e0', 'e1'}
    assert g.edge_tuple('e0') == ('v0', 'v1', 1.0)
    assert g.vertex_attrs['v0']['label'] == '0'
    assert g.edge_attrs['e0']['id'] == 'e12'


def test_read_gexf_property_graph_from_file(tmpdir):
    tmpfile = tmpdir.join("gexf.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected2)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    def import_id_cb(id):
        return 'v{}'.format(id)

    read_gexf(g, tmpfilename, import_id_cb=import_id_cb)

    print(g.vertices)
    print(g.edges)
    print(g.vertex_attrs)
    print(g.edge_attrs)

    assert g.vertices == {'vv1', 'vv2', 'vv3'}
    assert g.edges == {'e0', 'e1'}
    assert g.edge_tuple('e0') == ('vv1', 'vv2', 1.0)
    assert g.vertex_attrs['vv1']['label'] == '0'
    assert g.edge_attrs['e0']['id'] == 'e12'
    