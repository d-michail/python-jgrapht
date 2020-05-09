import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_dimacs, generate_dimacs


def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

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

    return g

dimacs_sp_expected = """c
c SOURCE: Generated using the JGraphT library
c
p sp 10 18
a 1 2
a 1 3
a 1 4
a 1 5
a 1 6
a 1 7
a 1 8
a 1 9
a 1 10
a 2 3
a 3 4
a 4 5
a 5 6
a 6 7
a 7 8
a 8 9
a 9 10
a 10 2
"""

dimacs_coloring_expected = """c
c SOURCE: Generated using the JGraphT library
c
p col 10 18
e 1 2
e 1 3
e 1 4
e 1 5
e 1 6
e 1 7
e 1 8
e 1 9
e 1 10
e 2 3
e 3 4
e 4 5
e 5 6
e 6 7
e 7 8
e 8 9
e 9 10
e 10 2
"""

dimacs_maxclique_expected = """c
c SOURCE: Generated using the JGraphT library
c
p edge 10 18
e 1 2
e 1 3
e 1 4
e 1 5
e 1 6
e 1 7
e 1 8
e 1 9
e 1 10
e 2 3
e 3 4
e 4 5
e 5 6
e 6 7
e 7 8
e 8 9
e 9 10
e 10 2
"""

def test_dimacs(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('dimacs.out')
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format='shortestpath')

    with open(tmpfilename, "r") as f: 
        contents = f.read()
        print (contents)
        
    assert contents == dimacs_sp_expected


def test_dimacs_coloring(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('dimacs.out')
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format='coloring')

    with open(tmpfilename, "r") as f: 
        contents = f.read()
        print (contents)
        
    assert contents == dimacs_coloring_expected


def test_dimacs_maxclique(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('dimacs.out')
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format='maxclique')

    with open(tmpfilename, "r") as f: 
        contents = f.read()
        print (contents)
        
    assert contents == dimacs_maxclique_expected


def test_dimacs_output_to_string(): 
    g = build_graph()

    out = generate_dimacs(g)

    assert out == dimacs_maxclique_expected
