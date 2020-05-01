import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import gml


def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    for _ in range(0, 10):
        g.add_vertex()

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
    


#def vertex_to_label(v): 
#    return "label {}".format(v)

#def test_gml(tmpdir):
#    g = build_graph()
    #tmpfile = tmpdir.join('gml.out')
    #tmpfilename = str(tmpfile)

    #gml(g, tmpfilename, False, vertex_to_label)
#    gml(g, "foo.gml", False, vertex_to_label)

#    with open(tmpfilename, "r") as f: 
#        contents = f.read()
#        print (contents)
        
#    assert contents == dimacs_sp_expected


