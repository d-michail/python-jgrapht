import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_json
from jgrapht.io.importers import read_json

expected="""{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"label 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}"""


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


def test_output_json(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('json.out')
    tmpfilename = str(tmpfile)

    v_labels = { 0: { 'label': 'label 0'  }, 
	             1: { 'label': 'label 1'  }, 
				 2: { 'label': 'label 2' }, 
				 3: { 'label': 'label 3' } }
    e_labels = { 9: { 'label': 'edge 1-2' } }
    write_json(g, tmpfilename, v_labels, e_labels)

    with open(tmpfilename, "r") as f: 
        contents = f.read()

    print("contents")
    print(contents)
    print("vs")
    print("expected")
    print(expected)

    assert contents == expected


def test_input_json(tmpdir):
	tmpfile = tmpdir.join('json.out')
	tmpfilename = str(tmpfile)

	with open(tmpfilename, "w") as f: 
		f.write(expected)

	g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

	def va_cb(vertex, attribute_name, attribute_value):
		print('Vertex {}, attr {}, value {}'.format(vertex, attribute_name.decode(), attribute_value.decode()))
		if vertex == 2 and attribute_name.decode() == 'label': 
			assert attribute_value.decode() == 'label 2'
		if vertex == 5 and attribute_name.decode() == 'label': 
			assert attribute_value.decode() == '5'	

	def ea_cb(edge, attribute_name, attribute_value):
		print('Edge {}, attr {}, value {}'.format(edge, attribute_name.decode(), attribute_value.decode()))
		if edge == 9 and attribute_name.decode() == 'label': 
			assert attribute_value.decode() == 'edge 1-2'

	read_json(g, tmpfilename, va_cb, ea_cb)


def test_input_json_nocallbacks(tmpdir):
	tmpfile = tmpdir.join('json.out')
	tmpfilename = str(tmpfile)

	with open(tmpfilename, "w") as f: 
		f.write(expected)

	g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

	read_json(g, tmpfilename)
    