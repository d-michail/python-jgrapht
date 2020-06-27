import pytest

import re

from jgrapht import create_graph
from jgrapht.utils import create_vertex_supplier, create_edge_supplier

from jgrapht.io.exporters import write_dot, generate_dot
from jgrapht.io.importers import read_dot, parse_dot


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)

    return g


def test_output_dot(tmpdir):

    g = build_graph()
    tmpfile = tmpdir.join("dot.out")
    tmpfilename = str(tmpfile)

    v_dict = {
        0: {"name": "name 0"},
        1: {"name": "name 1"},
        2: {"name": "name 2"},
    }

    e_dict = {0: {"label": "ακμή 1-2"}}

    write_dot(g, tmpfilename, per_vertex_attrs_dict=v_dict, per_edge_attrs_dict=e_dict)

    # read back

    def ea_cb(edge, attribute_name, attribute_value):
        if edge == 0:
            if attribute_name == "label":
                assert attribute_value == "ακμή 1-2"

    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    read_dot(g1, tmpfilename, edge_attribute_cb=ea_cb)

    assert len(g1.vertices) == 3
    assert len(g1.edges) == 3


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

    out = generate_dot(g)

    assert (
        out.splitlines()
        == "digraph G {\n  0;\n  1;\n  2;\n  3;\n  0 -> 1;\n  0 -> 2;\n  0 -> 3;\n  2 -> 3;\n}\n".splitlines()
    )



def test_property_graph_output_to_string():
    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex('v1')
    g.add_vertex('v2')
    g.add_edge('v1', 'v2', edge='e12')

    g.vertex_attrs['v1']['color'] = 'red'
    g.vertex_attrs['v2']['color'] = 'blue'
    g.edge_attrs['e12']['capacity'] = 5.0

    out = generate_dot(g)

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    assert out.splitlines() == expected.splitlines()


def test_read_dot_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    def import_id_cb(id):
        return 'v{}'.format(id)

    parse_dot(g, expected, import_id_cb=import_id_cb)

    assert g.vertices == {'vv1', 'vv2'}
    assert g.edge_tuple('e0') == ('vv1', 'vv2', 1.0)
    assert g.vertex_attrs['vv1']['color'] == 'red'
    assert g.vertex_attrs['vv2']['color'] == 'blue'
    assert g.edge_attrs['e0']['capacity'] == '5.0'


def test_read_dot_property_graph_from_string1():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    parse_dot(g, expected)

    assert g.vertices == {'v0', 'v1'}
    assert g.edge_tuple('e0') == ('v0', 'v1', 1.0)
    assert g.vertex_attrs['v0']['color'] == 'red'
    assert g.vertex_attrs['v1']['color'] == 'blue'
    assert g.edge_attrs['e0']['capacity'] == '5.0'


def test_read_dot_property_graph_from_filename(tmpdir):
    tmpfile = tmpdir.join("dot.out")
    tmpfilename = str(tmpfile)

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    read_dot(g, tmpfilename)

    assert g.vertices == {'v0', 'v1'}
    assert g.edge_tuple('e0') == ('v0', 'v1', 1.0)
    assert g.vertex_attrs['v0']['color'] == 'red'
    assert g.vertex_attrs['v1']['color'] == 'blue'
    assert g.edge_attrs['e0']['capacity'] == '5.0'


def test_read_dot_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    def import_id(id):
        print(id)
        m = re.match(r'v([0-9]+)', id)
        vid = int(m.group(1))
        return vid

    parse_dot(g, expected, import_id_cb=import_id)

    assert g.vertices == {1, 2}
    assert g.edge_tuple(0) == (1, 2, 1.0)
