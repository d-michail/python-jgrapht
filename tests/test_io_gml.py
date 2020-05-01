import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import gml


expected="""Creator "JGraphT GML Exporter"
Version 1
graph
[
	label ""
	directed 0
	node
	[
		id 0
		label "label 0"
	]
	node
	[
		id 1
		label "label 1"
	]
	node
	[
		id 2
		label "κόμβος 2"
	]
	node
	[
		id 3
		label "κόμβος 3"
	]
	node
	[
		id 4
		label "4"
	]
	node
	[
		id 5
		label "5"
	]
	node
	[
		id 6
		label "6"
	]
	node
	[
		id 7
		label "7"
	]
	node
	[
		id 8
		label "8"
	]
	node
	[
		id 9
		label "9"
	]
	edge
	[
		source 0
		target 1
		label "0"
	]
	edge
	[
		source 0
		target 2
		label "1"
	]
	edge
	[
		source 0
		target 3
		label "2"
	]
	edge
	[
		source 0
		target 4
		label "3"
	]
	edge
	[
		source 0
		target 5
		label "4"
	]
	edge
	[
		source 0
		target 6
		label "5"
	]
	edge
	[
		source 0
		target 7
		label "6"
	]
	edge
	[
		source 0
		target 8
		label "7"
	]
	edge
	[
		source 0
		target 9
		label "8"
	]
	edge
	[
		source 1
		target 2
		label "ακμή 1-2"
	]
	edge
	[
		source 2
		target 3
		label "10"
	]
	edge
	[
		source 3
		target 4
		label "11"
	]
	edge
	[
		source 4
		target 5
		label "12"
	]
	edge
	[
		source 5
		target 6
		label "13"
	]
	edge
	[
		source 6
		target 7
		label "14"
	]
	edge
	[
		source 7
		target 8
		label "15"
	]
	edge
	[
		source 8
		target 9
		label "16"
	]
	edge
	[
		source 9
		target 1
		label "17"
	]
]
"""



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
    tmpfile = tmpdir.join('gml.out')
    tmpfilename = str(tmpfile)

    v_labels = { 0: 'label 0', 1: 'label 1', 2: 'κόμβος 2', 3: 'κόμβος 3' }
    e_labels = { 9: 'ακμή 1-2' }
    gml(g, tmpfilename, False, v_labels, e_labels)

    with open(tmpfilename, "r") as f: 
        contents = f.read()

    assert contents == expected


