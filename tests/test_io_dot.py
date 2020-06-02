import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_dot, generate_dot
from jgrapht.io.importers import read_dot, parse_dot
from jgrapht.views import as_property_graph


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
    )

    g = as_property_graph(g)

    g.add_vertex('v1')
    g.add_vertex('v2')
    g.add_edge('v1', 'v2', edge='e12')

    g.vertex_props['v1']['color'] = 'red'
    g.vertex_props['v2']['color'] = 'blue'
    g.edge_props['e12']['capacity'] = 5.0

    out = generate_dot(g)

    expected=r"""digraph G {
  v1 [ color="red" ];
  v2 [ color="blue" ];
  v1 -> v2 [ capacity="5.0" ];
}
"""

    assert out.splitlines() == expected.splitlines()
