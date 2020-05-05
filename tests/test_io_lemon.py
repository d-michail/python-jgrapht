import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_lemon


def build_graph():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

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

    return g

lemon_expected = """#Creator: JGraphT Lemon (LGF) Exporter
#Version: 1

@nodes
label
0
1
2
3
4
5
6
7
8
9

@arcs
		-
0	1
0	2
0	3
0	4
0	5
0	6
0	7
0	8
0	9
1	2
2	3
3	4
4	5
5	6
6	7
7	8
8	9
9	1

"""


def test_lemon(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('lemon.out')
    tmpfilename = str(tmpfile)
    write_lemon(g, tmpfilename)

    with open(tmpfilename, "r") as f: 
        contents = f.read()
        print (contents)
        
    assert contents == lemon_expected


