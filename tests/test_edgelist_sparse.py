import pytest

from jgrapht import create_sparse_graph
from jgrapht.io.edgelist import parse_edgelist_json

input1 = r'{"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"0","label":"\u03BA\u03CC\u03BC\u03B2\u03BF\u03C2 0"},{"id":"1","label":"label 1"},{"id":"2","label":"label 2"},{"id":"3","label":"label 3"},{"id":"4"},{"id":"5"},{"id":"6"},{"id":"7"},{"id":"8"},{"id":"9"}],"edges":[{"source":"0","target":"1"},{"source":"0","target":"2"},{"source":"0","target":"3"},{"source":"0","target":"4"},{"source":"0","target":"5"},{"source":"0","target":"6"},{"source":"0","target":"7"},{"source":"0","target":"8"},{"source":"0","target":"9"},{"source":"1","target":"2","label":"edge 1-2"},{"source":"2","target":"3"},{"source":"3","target":"4"},{"source":"4","target":"5"},{"source":"5","target":"6"},{"source":"6","target":"7"},{"source":"7","target":"8"},{"source":"8","target":"9"},{"source":"9","target":"1"}]}'



def test_graph_sparse_weighted():
    edgelist = parse_edgelist_json(input1)

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]

    edgelist = [(int(s), int(t), w) for s, t, w in edgelist]

    g = create_sparse_graph(edgelist, 10, directed=True)

    print(g)

    assert g.type.directed
    assert g.type.weighted

    assert g.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    edgelist2 = []
    for e in g.edges:
        edgelist2.append(g.edge_tuple(e))
    assert edgelist2 == list(edgelist)

    # sparse graphs cannot be modified
    with pytest.raises(ValueError):
        g.add_edge(0, 5)


def test_graph_sparse_weighted_no_vertex_count():
    edgelist = parse_edgelist_json(input1)

    assert list(edgelist) == [
        ('0', '1', 1.0),
        ('0', '2', 1.0),
        ('0', '3', 1.0),
        ('0', '4', 1.0),
        ('0', '5', 1.0),
        ('0', '6', 1.0),
        ('0', '7', 1.0),
        ('0', '8', 1.0),
        ('0', '9', 1.0),
        ('1', '2', 1.0),
        ('2', '3', 1.0),
        ('3', '4', 1.0),
        ('4', '5', 1.0),
        ('5', '6', 1.0),
        ('6', '7', 1.0),
        ('7', '8', 1.0),
        ('8', '9', 1.0),
        ('9', '1', 1.0),
    ]

    edgelist = [(int(s), int(t), w) for s, t, w in edgelist]

    g = create_sparse_graph(edgelist, directed=True)

    print(g)

    assert g.type.directed
    assert g.type.weighted

    assert g.vertices == set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    edgelist2 = []
    for e in g.edges:
        edgelist2.append(g.edge_tuple(e))
    assert edgelist2 == list(edgelist)

    # sparse graphs cannot be modified
    with pytest.raises(ValueError):
        g.add_edge(0, 5)