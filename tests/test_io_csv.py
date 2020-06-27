import pytest

from jgrapht import create_graph
from jgrapht.utils import create_vertex_supplier, create_edge_supplier

from jgrapht.io.importers import parse_csv, read_csv
from jgrapht.io.exporters import write_csv, generate_csv


def test_input_csv_from_string_create_new_vertices():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    input_string = """1,2
2,3
3,4
4,1
"""

    print(set(g.vertices))
    parse_csv(g, input_string)
    print(set(g.vertices))
    print(set(g.edges))
    assert g.vertices == set([0, 1, 2, 3])


def test_input_csv_from_string_preserve_ids():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    input_string = """1,2
2,3
3,4
4,1
"""

    def import_id(file_id):
        return int(file_id)

    parse_csv(g, input_string, import_id_cb=import_id)
    print(set(g.vertices))
    print(set(g.edges))
    assert g.vertices == set([1, 2, 3, 4])


def test_export_import(tmpdir):

    g = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
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

    assert len(g.edges) == 18

    tmpfile = tmpdir.join("csv.out")
    tmpfilename = str(tmpfile)

    write_csv(g, tmpfilename)

    # read back

    g1 = create_graph(
        directed=True,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
    )

    read_csv(g1, tmpfilename)

    assert g1.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g1.contains_edge_between(6, 7)
    assert not g1.contains_edge_between(6, 8)
    assert len(g1.edges) == 18


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

    out = generate_csv(g)

    assert out.splitlines() == ["0,1,2,3", "1", "2,3", "3"]


def test_read_csv_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    input_string = """1,2
2,3
3,4
4,1
"""

    def import_id_cb(id):
        return 'v{}'.format(int(id)+1)

    parse_csv(g, input_string, import_id_cb=import_id_cb)

    print (g.vertices)

    assert g.vertices == {'v2', 'v3', 'v4', 'v5'}
    assert g.edge_tuple('e2') == ('v4', 'v5', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}


def test_read_csv_property_graph_from_string1():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    input_string = """1,2
2,3
3,4
4,1
"""

    parse_csv(g, input_string)

    print (g.vertices)

    assert g.vertices == {'v0', 'v1', 'v2', 'v3'}
    assert g.edge_tuple('e2') == ('v2', 'v3', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}


def test_read_csv_property_graph_from_file(tmpdir):
    tmpfile = tmpdir.join("csv.out")
    tmpfilename = str(tmpfile)

    input_string = """1,2
2,3
3,4
4,1
"""

    with open(tmpfilename, "w") as f:
        f.write(input_string)

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
        return 'v{}'.format(int(id)+1)

    read_csv(g, tmpfilename, import_id_cb=import_id_cb)

    print (g.vertices)

    assert g.vertices == {'v2', 'v3', 'v4', 'v5'}
    assert g.edge_tuple('e2') == ('v4', 'v5', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}
