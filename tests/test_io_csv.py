import pytest

from jgrapht import create_graph
from jgrapht.io.importers import parse_csv, read_csv
from jgrapht.io.exporters import write_csv, generate_csv

def test_input_csv_from_string_create_new_vertices():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    input_string = """1,2
2,3
3,4
4,1
"""

    print (set(g.vertices)) 
    parse_csv(g, input_string)
    print (set(g.vertices)) 
    print (set(g.edges)) 
    assert g.vertices == set([0, 1, 2, 3])


def test_input_csv_from_string_preserve_ids():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    input_string = """1,2
2,3
3,4
4,1
"""

    def import_id(file_id): 
        return int(file_id)

    parse_csv(g, input_string, import_id_cb=import_id)
    print (set(g.vertices)) 
    print (set(g.edges)) 
    assert g.vertices == set([1, 2, 3, 4])


def test_export_import(tmpdir):

    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=False)

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
    g.create_edge(9, 1)

    assert len(g.edges) == 18

    tmpfile = tmpdir.join('csv.out')
    tmpfilename = str(tmpfile)

    write_csv(g, tmpfilename)

    # read back 

    g1 = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=False)

    read_csv(g1, tmpfilename)

    assert g1.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert g1.contains_edge_between(6, 7)
    assert not g1.contains_edge_between(6, 8)
    assert len(g1.edges) == 18


def test_output_to_string(): 
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=False)

    g.add_vertices_from(range(0,4))

    g.create_edge(0, 1)
    g.create_edge(0, 2)
    g.create_edge(0, 3)
    g.create_edge(2, 3)

    out = generate_csv(g)

    assert out.splitlines() == ['0,1,2,3', '1', '2,3', '3']
