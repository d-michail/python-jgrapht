import pytest

from jgrapht import create_graph
from jgrapht.io.importers import parse_csv


def test_input_csv_from_string_create_new_vertices():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    input_string = """1,2
2,3
3,4
4,1
"""

    print (set(g.vertices())) 
    parse_csv(g, input_string)
    print (set(g.vertices())) 
    print (set(g.edges())) 
    assert g.vertices() == set([0, 1, 2, 3])


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
    print (set(g.vertices())) 
    print (set(g.edges())) 
    assert g.vertices() == set([1, 2, 3, 4])


