"""Documents and expectations ported from the parity tests of ``jgrapht-io`` (themselves derived
from the JGraphT test suite), run through the Python API."""

from pathlib import Path

import pytest

import jgrapht as jg

from helpers import parse_graph

DATA = Path(__file__).parent / "data"


def edges_of(g):
    return sorted(
        (g.edge_source(e), g.edge_target(e)) if g.directed else tuple(sorted((g.edge_source(e), g.edge_target(e))))
        for e in g.edges()
    )


def nv(g):
    return len(list(g.vertices()))


# ---------------------------------------------------------------- DIMACS and graph6 fixtures


def test_dimacs_myciel3():
    g = jg.read_graph(DATA / "myciel3.col", "dimacs")
    assert (nv(g), g.edge_count()) == (11, 20) and not g.directed and not g.weighted
    assert sorted(g.vertices()) == list(range(1, 12))
    assert jg.girth(g) == 4  # triangle free


def test_dimacs_myciel3_weighted():
    g = jg.read_graph(DATA / "myciel3_weighted.col", "dimacs", weighted=True)
    assert sorted(g.edge_weight(e) for e in g.edges()) == [float(i) for i in range(1, 21)]
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights[(1, 2)] == 1.0 and weights[(10, 11)] == 20.0
    # without weights the file is read unweighted; the default weight applies when weighted but absent
    plain = jg.read_graph(DATA / "myciel3.col", "dimacs", weighted=True, default_weight=2.5)
    assert {plain.edge_weight(e) for e in plain.edges()} == {2.5}


def test_sparse6_fixture():
    g = jg.read_graph(DATA / "ellingham_horton78.s6", "graph6")
    assert (nv(g), g.edge_count()) == (78, 117)
    assert {g.degree_of(v) for v in g.vertices()} == {3}
    assert jg.is_bipartite(g)
    # re-encoding as sparse6 and reading it back gives the same graph
    h = jg.parse_graph(jg.graph_to_string(g, "graph6", variant="sparse6"), "graph6")
    assert edges_of(h) == edges_of(g)


@pytest.mark.parametrize(
    "text,n,m",
    [
        ("A_", 2, 1),
        ("Bw", 3, 3),
        ("C~", 4, 6),
        ("D~{", 5, 10),
        ("E~~w", 6, 15),
    ],
)
def test_graph6_known_graphs(text, n, m):
    g = jg.parse_graph(text, "graph6")
    assert (nv(g), g.edge_count()) == (n, m)
    assert jg.graph_to_string(g, "graph6").strip() == text


# ---------------------------------------------------------------- GraphML

GML_BASIC = '<graphml><graph edgedefault="undirected"><node id="1"/><node id="2"/><node id="3"/><edge source="1" target="2"/><edge source="3" target="1"/><edge source="2" target="3"/></graph></graphml>'
GML_WRONG_ORDER = '<graphml><graph edgedefault="undirected"><edge source="2" target="3"/><node id="1"/><node id="2"/><node id="3"/><edge source="1" target="2"/><edge source="3" target="1"/></graph></graphml>'
GML_ATTRS = '<graphml><key id="c" for="node" attr.name="color" attr.type="string"><default>yellow</default></key><key id="w" for="edge" attr.name="weight" attr.type="double"><default>3.0</default></key><graph edgedefault="undirected"><node id="n0"><data key="c">green</data></node><node id="n1"/><node id="n2"><data key="c">blue</data></node><edge id="e0" source="n0" target="n2"><data key="w">2.0</data></edge><edge source="n0" target="n1"><data key="w">1.0</data></edge><edge source="n1" target="n2"/></graph></graphml>'


def test_graphml_basic_and_order():
    g = jg.parse_graph(GML_BASIC, "graphml")
    assert (nv(g), g.edge_count()) == (3, 3) and sorted(g.vertices()) == ["1", "2", "3"]
    assert jg.parse_graph(GML_BASIC, "graphml", directed=True).directed
    # edges before nodes
    assert jg.parse_graph(GML_WRONG_ORDER, "graphml").edge_count() == 3


def test_graphml_pseudograph_and_prefix():
    g = jg.parse_graph(
        '<graphml><graph><node id="a"/><edge source="a" target="a"/><edge source="a" target="a"/></graph></graphml>',
        "graphml",
    )
    assert g.edge_count() == 2 and g.allow_self_loops and g.allow_multiple_edges
    g = jg.parse_graph('<g:graphml xmlns:g="x"><g:graph><g:node id="a"/></g:graph></g:graphml>', "graphml")
    assert list(g.vertices()) == ["a"]


def test_graphml_attributes_and_defaults():
    g, a = parse_graph(GML_ATTRS, "graphml", attributes=True)
    assert g.edge_count() == 3 and not g.directed
    assert a["vertices"]["n0"]["color"] == "green"
    assert a["vertices"]["n1"]["color"] == "yellow"  # the declared default
    assert a["vertices"]["n2"]["color"] == "blue"
    assert a["edges"][0]["weight"] == 2.0 and a["edges"][2]["weight"] == 3.0
    w = jg.parse_graph(GML_ATTRS, "graphml", weighted=True)
    weights = {(w.edge_source(e), w.edge_target(e)): w.edge_weight(e) for e in w.edges()}
    assert weights[("n0", "n2")] == 2.0 and weights[("n0", "n1")] == 1.0 and weights[("n1", "n2")] == 3.0


def test_graphml_custom_weight_name():
    text = GML_ATTRS.replace('attr.name="weight"', 'attr.name="cost"')
    g = jg.parse_graph(text, "graphml", weighted=True, edge_weight_attribute="cost")
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights[("n0", "n2")] == 2.0
    g = jg.parse_graph(text, "graphml", weighted=True)  # "weight" no longer matches anything
    assert {g.edge_weight(e) for e in g.edges()} == {1.0}


def test_graphml_export_markers():
    g = jg.path_graph(3)
    assert 'edgedefault="undirected"' in jg.graph_to_string(g, "graphml")
    assert 'edgedefault="directed"' in jg.graph_to_string(jg.path_graph(3, directed=True), "graphml")
    w = jg.as_weighted(g, 2.0)
    assert "edge_weight_key" in jg.graph_to_string(w, "graphml", edge_weights=True)
    assert "edge_weight_key" not in jg.graph_to_string(w, "graphml")
    text = jg.graph_to_string(g, "graphml", vertex_labels=True, edge_labels=True)
    assert "vertex_label_key" in text and "edge_label_key" in text


# ---------------------------------------------------------------- DOT


def dot(text, **kw):
    return parse_graph(text, "dot", **kw)


def test_dot_edge_chains_and_ports():
    g = dot("digraph { a--b--c; k:1--q:a:3--d:3 }")
    assert g.directed and g.edge_count() == 4 and "q" in g


def test_dot_subgraphs():
    g = dot(
        "digraph G { subgraph cluster0 { a0->a1->a2->a3 } subgraph cluster1 { b0->b1->b2->b3 } "
        "start->a0; start->b0; a1->b3; b2->a3; a3->a0; a3->end; b3->end }"
    )
    assert (nv(g), g.edge_count()) == (10, 13)
    g = dot("digraph { subgraph { a0->a1 } -> subgraph { b0->b1 } }")
    assert (nv(g), g.edge_count()) == (4, 6)
    g = dot("digraph { subgraph { a0->a1; subgraph { a00->a11 } } -> subgraph { b0->b1; subgraph { b00->b11 } } }")
    assert (nv(g), g.edge_count()) == (8, 20)
    assert dot("digraph { a0->{a00->a11}->b0->{b00->b11} }").edge_count() == 8
    assert dot("digraph { a0->{{{{a00->a11}}}}->b0->{{b00->b11}} }").edge_count() == 8


def test_dot_comments_and_empty_lists():
    assert dot("digraph { // first\n a0 -> /* middle */ a1; # last\n }").edge_count() == 1
    g = dot("digraph g { name=TEST; graph[] anyNodeWithAttributes[color=red]; anyNodeWithoutAttributes; anyNodeWithEmptyAttributes[] }")
    assert nv(g) == 3


def test_dot_scoped_defaults():
    g, a = dot(
        "digraph { node[color=gray]; a0->a1; subgraph { node[color=black]; a2->a3 }; a4[color=white]; a4->a5 }",
        attributes=True,
    )
    v = a["vertices"]
    assert (v["a0"]["color"], v["a2"]["color"], v["a4"]["color"], v["a5"]["color"]) == ("gray", "black", "white", "gray")
    g, a = dot(
        "digraph { edge[weight=5.0]; a0->a1; subgraph { edge[weight=2.0]; a2->a3 }; a4->a5[weight=15.0] }",
        attributes=True,
    )
    assert [a["edges"][i]["weight"] for i in range(3)] == ["5.0", "2.0", "15.0"]


def test_dot_unescaping():
    g, a = dot(
        'digraph { a0[name=myname]; a1[name="name with ; semicolon"]; a2[name="name with \\"internal\\" quotes"]; '
        'a3[name=<<h2>name ✅</h2>>]; a4[name=""] }',
        attributes=True,
    )
    v = a["vertices"]
    assert v["a0"]["name"] == "myname" and v["a1"]["name"] == "name with ; semicolon"
    assert v["a2"]["name"] == 'name with "internal" quotes'
    assert v["a3"]["name"] == "<h2>name ✅</h2>" and v["a4"]["name"] == ""
    g, a = dot('digraph { a[label=" /\\n "]; b[label="\\"Test\\""] }', attributes=True)
    assert a["vertices"]["a"]["label"] == " /\\n " and a["vertices"]["b"]["label"] == '"Test"'


def test_dot_html_labels_and_errors():
    g, a = dot("digraph { a0[name=<<h1/>>] }", attributes=True)
    assert a["vertices"]["a0"]["name"] == "<h1/>"
    with pytest.raises(jg.GraphError):
        dot("digraph { a0[name=< >> >] }")
    for bad in ["", "garbage", "digraph {", "graph { a -- }"]:
        with pytest.raises(jg.GraphError):
            dot(bad)


def test_dot_ids():
    assert nv(dot("graph { a1; _b; \"quoted id\"; 12 }")) == 4
    with pytest.raises(jg.GraphError):
        dot("graph { 1a }")
    g, a = dot("graph named { a -- b }", attributes=True)
    assert a["graph"]["ID"] == "named"


# ---------------------------------------------------------------- GML

GML = """graph [
 comment "Sample Graph" directed 1
 node [ id 1 ] node [ id 2 ] node [ id 3 ] node [ ]
 edge [ source 1 target 2 ] edge [ source 2 target 3 ] edge [ source 3 target 1 ]
]"""
GML_W = """graph [
 node [ id 1 ] node [ id 2 ] node [ id 3 ]
 edge [ source 1 target 2 weight 2.0 ] edge [ source 3 target 1 weight 3.0 ]
]"""


def test_gml_basic():
    g = jg.parse_graph(GML, "gml")
    assert g.directed and (nv(g), g.edge_count()) == (4, 3)
    g = jg.parse_graph(
        "graph [ node [ id 1 ] node [ id 2 ] node [ id 3 ] node [ ] edge [ source 1 target 2 ] edge [ source 1 target 2 ] "
        "edge [ source 1 target 2 ] edge [ source 2 target 3 ] edge [ source 3 target 1 ] edge [ source 1 target 1 ] "
        "edge [ source 2 target 2 ] ]",
        "gml",
        directed=True,
    )
    assert (nv(g), g.edge_count()) == (4, 7)


@pytest.mark.parametrize(
    "text",
    [
        GML_W,
        "# comment\n" + GML_W,
        "graph [ node [ id 1 ] node [ id 2 ] node [ id 3 ] edge [ source 1 target 2 weight 2.0 ] edge [ source 3 target 1 weight 3.0 ] ]",
    ],
)
def test_gml_weights(text):
    g = jg.parse_graph(text, "gml", weighted=True, directed=True)
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights == {(1, 2): 2.0, (3, 1): 3.0}


@pytest.mark.parametrize(
    "text",
    [
        "graph [ [ node ] ]",
        'graph [ node [ id "1" ] ]',
        'graph [ node [ id 1 ] node [ id 2 ] edge [ source "1" target 2 ] ]',
        'graph [ node [ id 1 ] node [ id 2 ] edge [ source 1 target "2" ] ]',
        'graph [ node [ id 1 ] node [ id 2 ] edge [ source 1 target 2 weight "2.0" ] ]',
    ],
)
def test_gml_errors(text):
    with pytest.raises(jg.GraphError):
        jg.parse_graph(text, "gml")


def test_gml_attributes():
    text = (
        'graph [ edge [ source 1 target 2 label "Edge 1-2" name "Name 12" ] node [ id 1 label "Node 1" ] '
        'node [ id 2 label "Node 2" ] node [ label "Node ?" ] ]'
    )
    g, a = parse_graph(text, "gml", attributes=True)
    assert a["vertices"][1]["label"] == "Node 1" and a["edges"][0]["name"] == "Name 12"
    text = (
        "graph [ edge [ source 1 target 2 frequency 6 customweight 7.5 ] node [ id 1 frequency 2 customweight 1.2 ] "
        "node [ id 2 frequency 3 customweight 2.1 ] ]"
    )
    g, a = parse_graph(text, "gml", attributes=True)
    assert a["vertices"][1]["frequency"] == 2 and isinstance(a["vertices"][1]["frequency"], int)
    assert a["edges"][0]["customweight"] == 7.5
    text = (
        "graph [ edge [ source 1 target 2 points [ x 1.0 y 2.0 ] ] node [ id 1 deep [ one [ one 1.0 two 2.0 ] ] ] "
        "node [ id 2 ] ]"
    )
    g, a = parse_graph(text, "gml", attributes=True)
    assert a["edges"][0]["points"] == "[ x 1.0 y 2.0 ]"


def test_gml_export_import_with_loop():
    g = jg.Graph(directed=True, weighted=True, allow_self_loops=True)
    for v in (1, 2, 3):
        g.add_vertex(v)
    for u, v, w in [(1, 2, 2.0), (2, 3, 3.0), (3, 3, 5.0)]:
        g.add_edge(u, v, weight=w)
    h = jg.parse_graph(jg.graph_to_string(g, "gml", edge_weights=True), "gml", weighted=True)
    assert (nv(h), h.edge_count()) == (3, 3) and h.directed
    assert sorted(h.edge_weight(e) for e in h.edges()) == [2.0, 3.0, 5.0]


# ---------------------------------------------------------------- GEXF

GEXF = '<gexf version="1.2"><graph defaultedgetype="undirected"><nodes><node id="1" label="1"/><node id="2" label="2"/><node id="3" label="3"/></nodes><edges><edge id="1" source="2" target="3"/><edge id="0" source="1" target="2"/><edge id="2" source="3" target="1"/></edges></graph></gexf>'
GEXF_ATTRS = '<gexf version="1.2"><graph defaultedgetype="directed"><attributes class="node"><attribute id="0" title="color" type="string"/><attribute id="1" title="city" type="liststring"/><attribute id="2" title="weight" type="double"/></attributes><attributes class="edge"><attribute id="0" title="length" type="double"/></attributes><nodes><node id="1"><attvalues><attvalue for="0" value="Red"/><attvalue for="1" value="Paris"/><attvalue for="2" value="100.0"/></attvalues></node><node id="2" label="2"/><node id="3"><attvalues><attvalue for="0" value="Black"/></attvalues></node></nodes><edges><edge id="1" source="2" target="3" weight="1.2"/><edge id="0" source="1" target="2" weight="0.1"><attvalues><attvalue for="0" value="333.0"/></attvalues></edge><edge id="2" source="3" target="1" weight="2.0"/></edges></graph></gexf>'


def test_gexf_basic():
    g, a = parse_graph(GEXF, "gexf", attributes=True)
    assert (nv(g), g.edge_count()) == (3, 3) and not g.directed
    assert a["vertices"]["1"]["label"] == "1" and a["vertices"]["1"]["ID"] == "1"
    meta = GEXF.replace("<graph", "<meta><creator>JGraphT</creator></meta><graph")
    assert jg.parse_graph(meta, "gexf").edge_count() == 3


def test_gexf_attributes_and_weights():
    g, a = parse_graph(GEXF_ATTRS, "gexf", weighted=True, attributes=True)
    assert g.directed and g.weighted
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights == {("2", "3"): 1.2, ("1", "2"): 0.1, ("3", "1"): 2.0}
    v = a["vertices"]
    assert v["1"]["color"] == "Red" and v["1"]["city"] == "Paris" and v["1"]["weight"] == 100.0
    assert v["3"]["color"] == "Black"
    assert 333.0 in [e.get("length") for e in a["edges"].values()]


def test_gexf_errors_and_nested():
    with pytest.raises(jg.GraphError):
        jg.parse_graph('<gexf><graph><node id="1"/></graph></gexf>', "gexf")
    nested = (
        '<gexf><graph><nodes><node id="1"><nodes><node id="4"/></nodes><edges><edge source="3" target="4"/></edges></node>'
        '<node id="2"/><node id="3"/></nodes><edges><edge source="2" target="3"/><edge source="1" target="2"/>'
        '<edge source="3" target="1"/></edges></graph></gexf>'
    )
    g = jg.parse_graph(nested, "gexf")
    assert (nv(g), g.edge_count()) == (3, 3) and "4" not in g


# ---------------------------------------------------------------- JSON

JSON = '{"nodes":[{"id":"1"},{"id":"2"},{"id":"3"},{"id":"4"}],"edges":[{"source":"1","target":"2"},{"source":"1","target":"3"}]}'
JSON_W = '{"nodes":[{"id":"1"},{"id":"2"},{"id":"3"},{"id":"4"}],"edges":[{"source":"1","target":"2","weight":2.0},{"source":"1","target":"3","weight":3.0},{"source":"2","target":"3"}]}'


def test_json_basic_and_weights():
    g = jg.parse_graph(JSON, "json", directed=True)
    assert (nv(g), g.edge_count()) == (4, 2)
    g = jg.parse_graph(JSON_W, "json", weighted=True, directed=True)
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights == {("1", "2"): 2.0, ("1", "3"): 3.0, ("2", "3"): 1.0}
    assert not jg.parse_graph(JSON_W, "json").weighted


def test_json_mixed_ids_and_errors():
    g = jg.parse_graph(
        '{"nodes":[{"id":1},{"id":"2"},{"id":"3"},{"id":4}],"edges":[{"source":1,"target":"2"},{"source":1,"target":3}]}',
        "json",
    )
    assert sorted(g.vertices()) == ["1", "2", "3", "4"] and g.edge_count() == 2
    for bad in [
        '{"nodes":[{"id":1},{"id":"2"},{"id":1}],"edges":[]}',
        '{"nodes":[{"id":1},{"id":2}],"edges":[{"target":2}]}',
        '{"nodes":[{"id":1},{"id":2}],"edges":[{"source":1}]}',
        "not json",
        "",
    ]:
        with pytest.raises(jg.GraphError):
            jg.parse_graph(bad, "json")


def test_json_typed_attributes():
    text = '{"nodes":[{"id":"1","label":"Label","int":4,"double":0.5,"boolean":true,"boolean1":false,"novalue":null}],"edges":null}'
    g, a = parse_graph(text, "json", attributes=True)
    v = a["vertices"]["1"]
    assert v["label"] == "Label" and v["int"] == 4 and v["double"] == 0.5
    assert v["boolean"] is True and v["boolean1"] is False and v["novalue"] is None
    assert g.edge_count() == 0


def test_json_custom_collections():
    text = '{"V":[{"id":"a"},{"id":"b"}],"E":[{"source":"a","target":"b"}]}'
    g = jg.parse_graph(text, "json", vertices_name="V", edges_name="E")
    assert edges_of(g) == [("a", "b")]


# ---------------------------------------------------------------- CSV

DIRECTED_EDGE_LIST = "1;2\n1;3\n3;1\n3;4\n4;5\n5;1\n"
DIRECTED_ADJACENCY = "1;2;3\n2\n3;1;4\n4;5\n5;1;2;3;4;5;5\n"
MATRIX = ";1;1;;\n;;;;\n1;;;1;\n;;;;1\n1;1;1;1;1\n"
MATRIX_ZERO = "0;1;1;0;0\n0;0;0;0;0\n1;0;0;1;0\n0;0;0;0;1\n1;1;1;1;1\n"
MATRIX_IDS = ";1;2;3;4;5\n1;;1;1;;\n2;;;;;\n3;1;;;1;\n4;;;;;1\n5;1;1;1;1;1\n"
MATRIX_IDS_ZERO = ";1;2;3;4;5\n1;0;1;1;0;0\n2;0;0;0;0;0\n3;1;0;0;1;0\n4;0;0;0;0;1\n5;1;1;1;1;1\n"
STANDARD = {(1, 2), (1, 3), (3, 1), (3, 4), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)}


def csv(text, variant, **kw):
    return jg.parse_graph(text, "csv", variant=variant, delimiter=";", directed=True, vertex_factory=int, **kw)


def test_csv_edge_and_adjacency_lists():
    g = csv(DIRECTED_EDGE_LIST, "edge_list")
    assert edges_of(g) == sorted([(1, 2), (1, 3), (3, 1), (3, 4), (4, 5), (5, 1)])
    g = csv(DIRECTED_ADJACENCY, "adjacency_list")
    # the loop 5;5 is listed twice and the graph is a multigraph
    assert nv(g) == 5 and g.edge_count() == 11
    assert set(edges_of(g)) == STANDARD


@pytest.mark.parametrize(
    "text,kw",
    [
        (MATRIX, {}),
        (MATRIX_ZERO, {"matrix_zero_when_no_edge": True}),
        (MATRIX_IDS, {"matrix_node_id": True}),
        (MATRIX_IDS_ZERO, {"matrix_node_id": True, "matrix_zero_when_no_edge": True}),
    ],
)
def test_csv_matrices(text, kw):
    g = csv(text, "matrix", **kw)
    assert nv(g) == 5 and set(edges_of(g)) == STANDARD
    assert g.edge_count() == len(STANDARD)


def test_csv_weights():
    text = ";1.0;13.0;;\n;;;;\n1.0;;;1.0;\n;;;;1.0\n1.0;1.0;53.0;1.0;1.0\n"
    g = csv(text, "matrix", weighted=True)
    weights = {(g.edge_source(e), g.edge_target(e)): g.edge_weight(e) for e in g.edges()}
    assert weights[(1, 3)] == 13.0 and weights[(5, 3)] == 53.0 and weights[(1, 2)] == 1.0


# ---------------------------------------------------------------- TSPLIB


def points_2d(kind):
    return (
        f"TYPE : TSP\nDIMENSION : 4\nEDGE_WEIGHT_TYPE : {kind}\nNODE_COORD_SECTION\n"
        "1 10.2 15.0\n2 14.2 15.0\n3  14.8    20.0\n4\t10.8\t\t20.0\nEOF\n"
    )


def points_3d(kind):
    return (
        f"TYPE : TSP\nDIMENSION : 4\nEDGE_WEIGHT_TYPE : {kind}\nNODE_COORD_SECTION\n"
        "1 10.0 15.0 3.7\n2 14.0 15.0 3.7\n3 14.0 20.0 3.7\n4 14.0 20.0 3.7\n"
    )


def tsp_distances(text):
    g, a = parse_graph(text, "tsplib", attributes=True)
    number = {v: n for v, n in a["tsplib"]["node_numbers"].items()}
    out = {}
    for e in g.edges():
        key = tuple(sorted((number[g.edge_source(e)], number[g.edge_target(e)])))
        out[key] = g.edge_weight(e)
    pairs = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert (nv(g), g.edge_count()) == (4, 6)
    return [out[p] for p in pairs], a["tsplib"]


@pytest.mark.parametrize(
    "text,expected,locations,distances",
    [
        (points_2d("EUC_2D"), [4, 7, 5, 5, 6, 4], True, True),
        (points_3d("EUC_3D"), [4, 6, 6, 5, 5, 0], False, False),
        (points_2d("MAX_2D"), [4, 5, 5, 5, 5, 4], True, False),
        (points_3d("MAX_3D"), [4, 5, 5, 5, 5, 0], False, False),
        (points_2d("MAN_2D"), [4, 10, 6, 6, 8, 4], True, True),
        (points_3d("MAN_3D"), [4, 9, 9, 5, 5, 0], False, False),
        (points_2d("CEIL_2D"), [4, 7, 6, 6, 7, 4], True, True),
        (points_2d("GEO"), [446, 727, 549, 541, 680, 446], True, True),
    ],
)
def test_tsplib_distances(text, expected, locations, distances):
    got, meta = tsp_distances(text)
    assert got == [float(x) for x in expected]
    assert meta["distinct_node_locations"] is locations
    assert meta["distinct_neighbor_distances"] is distances


def test_tsplib_metadata():
    text = (
        "NAME : theNameOfThisFile\nCOMMENT : The first line of the comment\nCOMMENT : A second line\nTYPE : TSP\n"
        "DIMENSION : 4\nEDGE_WEIGHT_TYPE : EUC_2D\nNODE_COORD_TYPE: THREED_COORDS\nCAPACITY : 7\n"
        "EDGE_WEIGHT_FORMAT: FULL_MATRIX\nEDGE_DATA_FORMAT: ADJ_LIST\nDISPLAY_DATA_TYPE  :   TWOD_DISPLAY\n"
        "NODE_COORD_SECTION\n1 10.2 15.0\nEOF\n"
    )
    g, a = parse_graph(text, "tsplib", attributes=True)
    m = a["tsplib"]
    assert nv(g) == 1
    assert m["name"] == "theNameOfThisFile" and m["type"] == "TSP" and m["dimension"] == 4 and m["capacity"] == 7
    assert m["comments"] == ["The first line of the comment", "A second line"]
    assert m["edge_weight_type"] == "EUC_2D" and m["edge_weight_format"] == "FULL_MATRIX"
    assert m["edge_data_format"] == "ADJ_LIST" and m["node_coord_type"] == "THREED_COORDS"
    assert m["display_data_type"] == "TWOD_DISPLAY"
    off_spec = text.replace("TYPE : TSP\n", "TYPE : TSP (Some comment)\n").replace("DIMENSION : 4", "DIMENSION : 4 (Comment)")
    off_spec = off_spec.replace("EUC_2D\n", "EUC_2D #use 2D edges\n").replace("CAPACITY : 7", "CAPACITY : 7 # note")
    m = parse_graph(off_spec, "tsplib", attributes=True)[1]["tsplib"]
    assert m["type"] == "TSP" and m["dimension"] == 4 and m["capacity"] == 7 and m["edge_weight_type"] == "EUC_2D"


def test_tsplib_embedded_tour():
    text = (
        "TYPE : TSP\nDIMENSION : 4\nEDGE_WEIGHT_TYPE : EUC_2D\nNODE_COORD_SECTION\n7 10.2 15.0\n2 14.2 15.0\n"
        "9 14.8 20.0\n4 10.8 20.0\nTOUR_SECTION\n9\n4\n7\n2\n-1\nEOF\n"
    )
    g, a = parse_graph(text, "tsplib", attributes=True)
    m = a["tsplib"]
    assert [m["node_numbers"][v] for v in m["tour"]] == [9, 4, 7, 2]
    assert m["coordinates"][0] == (10.2, 15.0)


@pytest.mark.parametrize(
    "text",
    [
        "TYPE : TSP\nTYPE : TSP\n",
        "DIMENSION : abc\n",
        "DIMENSION : 4\nEDGE_WEIGHT_TYPE : FANCY\n",
        "NODE_COORD_SECTION\n1 1 1\n",
        "DIMENSION : 2\nEDGE_WEIGHT_TYPE : EUC_2D\nNODE_COORD_SECTION\n1 1\n2 1 1\n",
    ],
)
def test_tsplib_errors(text):
    with pytest.raises(jg.GraphError):
        jg.parse_graph(text, "tsplib")


def test_tsplib_empty_document():
    g = jg.parse_graph("", "tsplib")
    assert nv(g) == 0 and g.weighted


INSTANCE = "DIMENSION : 4\nEDGE_WEIGHT_TYPE : EUC_2D\nNODE_COORD_SECTION\n7 10.2 15.0\n2 14.2 15.0\n9 14.8 20.0\n4 10.8 20.0\n"
TOUR = "TYPE : TSP\nDIMENSION : 4\nEDGE_WEIGHT_TYPE : EUC_2D\nTOUR_SECTION\n9\n4\n7\n2\n-1\nEOF\n"


def test_tsplib_standalone_tour():
    g, a = parse_graph(INSTANCE, "tsplib", attributes=True)
    tour = jg.parse_tsplib_tour(TOUR, INSTANCE)
    numbers = a["tsplib"]["node_numbers"]
    assert [numbers[v] for v in tour] == [9, 4, 7, 2]
    assert set(tour) == set(g.vertices())
    assert jg.parse_tsplib_tour("TYPE : TSP\nDIMENSION : 4\nEDGE_WEIGHT_TYPE : EUC_2D\n", INSTANCE) is None
    with pytest.raises(jg.GraphError):
        jg.parse_tsplib_tour(TOUR.replace("\n9\n", "\n99\n"), INSTANCE)
    with pytest.raises(jg.GraphError):
        jg.parse_tsplib_tour(TOUR, "not an instance TYPE")


def test_tsplib_tour_files(tmp_path):
    (tmp_path / "a.tsp").write_text(INSTANCE)
    (tmp_path / "a.tour").write_text(TOUR)
    assert jg.read_tsplib_tour(tmp_path / "a.tour", tmp_path / "a.tsp") == jg.parse_tsplib_tour(TOUR, INSTANCE)
    with open(tmp_path / "a.tour") as t, open(tmp_path / "a.tsp") as i:
        assert jg.read_tsplib_tour(t, i) == jg.parse_tsplib_tour(TOUR, INSTANCE)


def test_tsplib_geographic_distance():
    # the GEO distances of the parity test: nodes 1 and 2 of the 2d points are 446 km apart
    assert jg.tsplib_geographic_distance([10.2, 15.0], [14.2, 15.0]) == 446
    # the TSPLIB formula adds one kilometre, so even identical points are 1 apart
    assert jg.tsplib_geographic_distance([10.2, 15.0], [10.2, 15.0]) == 1
    with pytest.raises(jg.GraphError):
        jg.tsplib_geographic_distance([10.2], [14.2, 15.0])
