import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_sparse6, write_graph6
from jgrapht.io.importers import read_graph6sparse6



def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    g.add_vertex()
    g.add_vertex()
    g.add_vertex()
    g.add_vertex()

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(1, 3)

    return g


def test_output_sparse6(tmpdir):

    g = build_graph()
    tmpfile = tmpdir.join('graph.s6')
    tmpfilename = str(tmpfile)

    write_sparse6(g, tmpfilename)

    # read back 

    def va_cb(vertex, attribute_name, attribute_value):
        name = attribute_name.decode()
        value = attribute_value.decode()
        assert name == 'ID'
        assert str(vertex) == value

    g1 = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    read_graph6sparse6(g1, tmpfilename, vertex_attribute_cb=va_cb)

    assert len(g1.vertices()) == 4
    assert len(g1.edges()) == 5


def test_output_graph6(tmpdir):

    g = build_graph()
    tmpfile = tmpdir.join('graph.g6')
    tmpfilename = str(tmpfile)

    write_graph6(g, tmpfilename)

    # read back 

    def va_cb(vertex, attribute_name, attribute_value):
        name = attribute_name.decode()
        value = attribute_value.decode()
        assert name == 'ID'
        assert str(vertex) == value


    g1 = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    read_graph6sparse6(g1, tmpfilename, vertex_attribute_cb=va_cb)

    assert len(g1.vertices()) == 4
    assert len(g1.edges()) == 5

