import pytest

from jgrapht import create_graph
from jgrapht.io.exporters import write_json, generate_json
from jgrapht.io.importers import read_json, parse_json

expected=r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"label 0"},{"id":"1","label":"label 1"},{"id":"2","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'

expected2=r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0"},{"id":"1"},{"id":"2"},{"id":"3"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"2","target":"3"}]}'

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


def test_output_json(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join('json.out')
    tmpfilename = str(tmpfile)

    v_labels = { 0: { 'label': 'label 0'  }, 
	             1: { 'label': 'label 1'  }, 
				 2: { 'label': 'κόμβος 2' }, 
				 3: { 'label': 'label 3' } }
    e_labels = { 9: { 'label': 'edge 1-2' } }
    write_json(g, tmpfilename, v_labels, e_labels)

    with open(tmpfilename, "r") as f: 
        contents = f.read()

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
			assert attribute_value.decode() == 'κόμβος 2'
		if vertex == 5 and attribute_name.decode() == 'label': 
			assert attribute_value.decode() == '5'	

	def ea_cb(edge, attribute_name, attribute_value):
		print('Edge {}, attr {}, value {}'.format(edge, attribute_name.decode(), attribute_value.decode()))
		if edge == 9 and attribute_name.decode() == 'label': 
			assert attribute_value.decode() == 'edge 1-2'

	read_json(g, tmpfilename, vertex_attribute_cb=va_cb, edge_attribute_cb=ea_cb)


def test_input_json_nocallbacks(tmpdir):
	tmpfile = tmpdir.join('json.out')
	tmpfilename = str(tmpfile)

	with open(tmpfilename, "w") as f: 
		f.write(expected)

	g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

	read_json(g, tmpfilename)


def test_input_json_from_string_nocallbacks(tmpdir):

    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    parse_json(g, expected)
    assert g.number_of_vertices() == 10
    assert g.number_of_edges() == 18


def test_input_json_from_string_create_new_vertices():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    input_string=r'{"version":"1","nodes":[{"id":"5"},{"id":"7"}],"edges":[{"source":"5","target":"7"}]}'
    parse_json(g, input_string) 
    assert g.vertices() == set([0, 1])


def test_input_json_from_string_preserve_ids():
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    input_string=r'{"version":"1","nodes":[{"id":"5"},{"id":"7"}],"edges":[{"source":"5","target":"7"}]}'

    def import_id(file_id): 
        return int(file_id)

    parse_json(g, input_string, import_id_cb=import_id) 
    assert g.vertices() == set([5, 7])

def test_output_to_string(): 
    g = create_graph(directed=True, allowing_self_loops=False, allowing_multiple_edges=True, weighted=False)

    g.add_vertices_from(range(0,4))

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(2, 3)

    out = generate_json(g)
    assert out == expected2
