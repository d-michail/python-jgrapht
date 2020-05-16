import pytest

from jgrapht import create_graph

from jgrapht.io.exporters import write_graphml, generate_graphml
from jgrapht.io.importers import read_graphml, parse_graphml

expected1=r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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


expected2=r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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


expected3=r"""<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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

def test_export_import(tmpdir):

    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    for i in range(0, 10):
        g.add_vertex(i)

    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(0, 4)
    g.create_edge(0, 5)
    g.create_edge(0, 6)
    g.create_edge(0, 7)
    g.create_edge(0, 8)
    g.create_edge(0, 9)

    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 6)
    g.create_edge(6, 7)
    g.create_edge(7, 8)
    g.create_edge(8, 9)
    g.create_edge(9, 1, weight=33.3)

    assert len(g.edges()) == 18

    tmpfile = tmpdir.join('graphml.out')
    tmpfilename = str(tmpfile)

    attrs = [('cost', 'edge', 'double', None), ('name', 'node', 'string', None)]

    v_dict = { 
        0: { 'name': 'κόμβος 0' }, 
	    1: { 'name': 'node 1'   } 
    }
    e_dict = {
        17: {
            'cost': '48.5'
        }
    }

    write_graphml(g, tmpfilename, attrs=attrs, per_vertex_attrs_dict=v_dict, per_edge_attrs_dict=e_dict, export_edge_weights=True)

    # read back 

    g1 = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    def va_cb(vertex, attribute_name, attribute_value):
        print('Vertex {}, attr {}, value {}'.format(vertex, attribute_name, attribute_value))
        if vertex == 0:
            if attribute_name == 'name':
                assert attribute_value == 'κόμβος 0'
        if vertex == 1:
            if attribute_name == 'name': 
                assert attribute_value == 'node 1'

    def ea_cb(edge, attribute_name, attribute_value):
        print('Edge {}, attr {}, value {}'.format(edge, attribute_name, attribute_value))
        if edge == 17: 
            if attribute_name == 'cost': 
                assert attribute_value == '48.5'
            if attribute_name == 'weight': 
                assert attribute_value == '33.3'
            if attribute_name == 'source': 
                assert attribute_value == '9'
            if attribute_name == 'target': 
                assert attribute_value == '1'
            if attribute_name == 'id': 
                assert attribute_value == '17'                

    read_graphml(g1, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)

    assert g1.vertices() == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g1.contains_edge_between(6, 7)
    assert not g1.contains_edge_between(6, 8)
    assert len(g1.edges()) == 18

    assert g1.get_edge_weight(17) == 33.3

    # read back with non simple
    g2 = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    read_graphml(g2, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb, simple=False)

    assert g2.vertices() == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g2.contains_edge_between(6, 7)
    assert not g2.contains_edge_between(6, 8)
    assert len(g2.edges()) == 18

    assert g2.get_edge_weight(17) == 33.3



def test_output_to_string(): 
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=False)

    g.add_vertices_from(range(0,4))

    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(2, 3)

    out = generate_graphml(g)

    assert out.splitlines() == expected1.splitlines()


def test_output_to_string_with_weights(): 
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    g.add_vertices_from(range(0,4))

    g.create_edge(0, 1, weight=3.3)
    g.create_edge(0, 2, weight=4.4)
    g.create_edge(0, 3)
    g.create_edge(2, 3)

    out = generate_graphml(g, export_edge_weights=True)

    assert out.splitlines() == expected2.splitlines()


def test_output_to_string_with_attrs():

    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=True)

    for i in range(0, 10):
        g.add_vertex(i)

    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(0, 4)
    g.create_edge(0, 5)
    g.create_edge(0, 6)
    g.create_edge(0, 7)
    g.create_edge(0, 8)
    g.create_edge(0, 9)

    g.create_edge(1, 2)
    g.create_edge(2, 3)
    g.create_edge(3, 4)
    g.create_edge(4, 5)
    g.create_edge(5, 6)
    g.create_edge(6, 7)
    g.create_edge(7, 8)
    g.create_edge(8, 9)
    g.create_edge(9, 1, weight=33.3)

    assert len(g.edges()) == 18

    attrs = [('cost', 'edge', 'double', None), ('name', 'node', 'string', None)]

    v_dict = { 
        0: { 'name': 'κόμβος 0' }, 
	    1: { 'name': 'node 1'   } 
    }
    e_dict = {
        17: {
            'cost': '48.5'
        }
    }

    out = generate_graphml(g, attrs=attrs, per_vertex_attrs_dict=v_dict, per_edge_attrs_dict=e_dict, export_edge_weights=True)

    assert out.splitlines() == expected3.splitlines()

