import io

import pytest

import jgrapht as jg

from helpers import parse_graph

TSP = """NAME: sq
TYPE: TSP
COMMENT: square
DIMENSION: 4
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 0 0
2 0 3
3 4 3
4 4 0
EOF
"""


def labelled(directed=False, weighted=False):
    g = jg.Graph(directed=directed, weighted=weighted)
    for v in "abcd":
        g.add_vertex(v)
    for i, (u, v) in enumerate([("a", "b"), ("b", "c"), ("c", "d"), ("a", "c")]):
        g.add_edge(u, v, weight=float(i + 1) if weighted else None)
    return g


def edge_set(g):
    out = set()
    for e in g.edges():
        u, v = g.edge_source(e), g.edge_target(e)
        out.add((u, v) if g.directed else tuple(sorted((u, v))))
    return out


def test_format_lists():
    assert set(jg.import_formats()) == {
        "csv", "dimacs", "dot", "gexf", "gml", "graph6", "graphml", "json", "tsplib",
    }
    assert set(jg.export_formats()) == {
        "csv", "dimacs", "dot", "gexf", "gml", "graph6", "graphml", "json", "lemon", "matrix", "visio",
    }


@pytest.mark.parametrize("fmt", ["dot", "graphml", "json", "csv"])
@pytest.mark.parametrize("directed", [False, True])
def test_roundtrip_labelled(fmt, directed):
    g = labelled(directed=directed)
    variant = {"variant": "edge_list"} if fmt == "csv" else {}
    text = jg.graph_to_string(g, fmt, vertex_id=str, **variant)
    h = jg.parse_graph(text, fmt, directed=directed, **variant)
    assert h.directed == directed
    assert sorted(h.vertices()) == list("abcd")
    assert edge_set(h) == edge_set(g)


@pytest.mark.parametrize("fmt", ["gexf", "gml", "dimacs", "graph6"])
def test_roundtrip_numbered_formats(fmt):
    g = jg.grid_graph(3, 3)
    h = jg.parse_graph(jg.graph_to_string(g, fmt), fmt)
    assert (len(list(h.vertices())), h.edge_count()) == (9, 12)
    assert not h.directed
    assert sorted(len(h.edges_of(v)) for v in h.vertices()) == sorted(len(g.edges_of(v)) for v in g.vertices())


@pytest.mark.parametrize("fmt", ["graphml", "gexf", "gml", "json"])
def test_weights_roundtrip(fmt):
    g = labelled(directed=True, weighted=True)
    kw = {"edge_weights": True}
    if fmt in ("graphml", "json"):
        kw["vertex_id"] = str
    h = jg.parse_graph(jg.graph_to_string(g, fmt, **kw), fmt, weighted=True, directed=True)
    assert h.directed and h.weighted
    assert sorted(h.edge_weight(e) for e in h.edges()) == [1.0, 2.0, 3.0, 4.0]


def test_unweighted_by_default():
    g = labelled(weighted=True)
    text = jg.graph_to_string(g, "graphml", edge_weights=True, vertex_id=str)
    assert not jg.parse_graph(text, "graphml").weighted
    assert jg.parse_graph(text, "graphml", weighted=True).weighted


def test_directedness_is_detected():
    for fmt, kw in [("dot", {"vertex_id": str}), ("graphml", {"vertex_id": str}), ("gexf", {}), ("gml", {}), ("dimacs", {"variant": "shortest_path"})]:
        g = labelled(directed=True)
        if fmt in ("gexf", "gml", "dimacs"):
            g = jg.path_graph(4, directed=True)
        assert jg.parse_graph(jg.graph_to_string(g, fmt, **kw), fmt).directed, fmt
        g = jg.path_graph(4)
        kw = {k: v for k, v in kw.items() if k != "variant"}
        assert not jg.parse_graph(jg.graph_to_string(g, fmt, **kw), fmt).directed, fmt
    d = jg.path_graph(5, directed=True)
    assert jg.parse_graph(jg.graph_to_string(d, "graph6"), "graph6").directed
    # an explicit value wins
    text = jg.graph_to_string(jg.path_graph(3, directed=True), "gml")
    assert not jg.parse_graph(text, "gml", directed=False).directed


def test_vertex_factory_and_sparse():
    g = jg.path_graph(4)
    text = jg.graph_to_string(g, "csv", variant="edge_list", vertex_id=str)
    h = jg.parse_graph(text, "csv", variant="edge_list", vertex_factory=int)
    assert sorted(h.vertices()) == [0, 1, 2, 3]
    s = jg.parse_graph(text, "csv", variant="edge_list", sparse=True)
    assert isinstance(s, jg.SparseGraph)
    assert s.vertex_count() == 4 and s.edge_count() == 3
    with pytest.raises(jg.GraphError):
        jg.parse_graph(text, "csv", variant="edge_list", sparse=True, vertex_factory=int)
    with pytest.raises(jg.GraphError):  # two vertices collapse to one object
        jg.parse_graph(text, "csv", variant="edge_list", vertex_factory=lambda s: 0)
    with pytest.raises(ValueError):  # exceptions of the factory propagate
        jg.parse_graph(text, "csv", variant="edge_list", vertex_factory=lambda s: int("x"))


def test_sparse_weighted_import():
    g = labelled(weighted=True)
    text = jg.graph_to_string(g, "gml", edge_weights=True)
    s = jg.parse_graph(text, "gml", weighted=True, sparse=True)
    assert s.weighted
    assert sorted(s.edge_weight(e) for e in s.edges()) == [1.0, 2.0, 3.0, 4.0]


@pytest.mark.parametrize("sparse", [False, True])
def test_export_sparse_graphs(sparse):
    g = jg.grid_graph(2, 3, sparse=sparse)
    for fmt in jg.export_formats():
        if sparse and fmt == "graph6":
            # a SparseGraph is a multigraph by type, which graph6 cannot represent
            with pytest.raises(jg.GraphError):
                jg.graph_to_string(g, fmt)
            assert jg.graph_to_string(g, fmt, variant="sparse6")
            continue
        assert jg.graph_to_string(g, fmt)
    h = jg.parse_graph(jg.graph_to_string(g, "graphml"), "graphml")
    assert h.edge_count() == 7


def test_attributes_export_import():
    g = labelled(weighted=True)
    vattrs = {"a": {"color": "red", "n": 3, "x": 1.5, "ok": True}, "b": {"color": "blue"}}
    eattrs = lambda e: {"kind": "t", "idx": e}
    for fmt in ["graphml", "gexf", "json"]:
        kw = {"vertex_id": str} if fmt != "gexf" else {}
        text = jg.graph_to_string(g, fmt, vertex_attributes=vattrs, edge_attributes=eattrs, **kw)
        h = jg.parse_graph(text, fmt)
        names = {v: dict(a) for v, a in h.vertex_attrs.items()}
        if fmt == "gexf":  # numbered ids
            red = [a for a in names.values() if a.get("color") == "red"][0]
        else:
            red = names["a"]
        assert red["color"] == "red" and red["n"] == 3 and red["x"] == 1.5 and red["ok"] is True
        assert len(h.edge_attrs) == 4
        for i, a in h.edge_attrs.items():
            assert a["kind"] == "t" and a["idx"] == i


def test_graph_attributes_graphml_and_dot():
    g = labelled()
    text = jg.graph_to_string(g, "graphml", vertex_id=str, graph_attributes={"title": "demo", "year": 2026})
    h = jg.parse_graph(text, "graphml")
    assert h.graph_attrs["title"] == "demo" and h.graph_attrs["year"] == 2026
    text = jg.graph_to_string(g, "dot", vertex_id=str, graph_id="mygraph", vertex_attributes={"a": {"color": "red"}})
    h = jg.parse_graph(text, "dot")
    assert h.graph_attrs["ID"] == "mygraph"
    assert h.vertex_attrs["a"]["color"] == "red"


def test_dot_import_text():
    text = 'digraph G { a -> b [weight=2]; b -> c; c -> a; }'
    g = jg.parse_graph(text, "dot")
    assert g.directed and sorted(g.vertices()) == ["a", "b", "c"] and g.edge_count() == 3
    with pytest.raises(jg.GraphError):
        jg.parse_graph("digraph G { a -> ", "dot")


def test_gml_import_text():
    text = "graph [ directed 0 node [ id 1 label \"x\" ] node [ id 2 ] edge [ source 1 target 2 weight 3.5 ] ]"
    g = jg.parse_graph(text, "gml", weighted=True)
    assert sorted(g.vertices()) == [1, 2]
    assert g.vertex_attrs[1]["label"] == "x"
    assert [g.edge_weight(e) for e in g.edges()] == [3.5]


def test_csv_variants():
    g = jg.Graph(directed=True, weighted=True)
    for v in range(3):
        g.add_vertex(v)
    g.add_edge(0, 1, weight=2.0)
    g.add_edge(1, 2, weight=3.0)
    for variant in ["edge_list", "adjacency_list", "matrix"]:
        kw = {"matrix_node_id": True} if variant == "matrix" else {}
        text = jg.graph_to_string(g, "csv", variant=variant, edge_weights=True, vertex_id=str, **kw)
        h = jg.parse_graph(text, "csv", variant=variant, weighted=True, directed=True, vertex_factory=int, **kw)
        assert edge_set(h) == {(0, 1), (1, 2)}, variant
        assert sorted(h.edge_weight(e) for e in h.edges()) == [2.0, 3.0]
    text = jg.graph_to_string(g, "csv", variant="edge_list", delimiter=";", vertex_id=str)
    assert ";" in text and "," not in text
    h = jg.parse_graph(text, "csv", variant="edge_list", delimiter=";", directed=True)
    assert h.edge_count() == 2
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "csv", delimiter="ab")


def test_dimacs_variants():
    g = jg.path_graph(4, directed=True)
    text = jg.graph_to_string(g, "dimacs", variant="shortest_path", edge_weights=True)
    assert "p sp 4 3" in text
    h = jg.parse_graph(text, "dimacs", weighted=True, default_weight=7.0)
    assert h.directed and h.edge_count() == 3
    assert "p col" in jg.graph_to_string(jg.path_graph(3), "dimacs", variant="coloring")
    assert "p edge" in jg.graph_to_string(jg.path_graph(3), "dimacs")
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "dimacs", variant="nope")


def test_graph6_variants():
    k4 = jg.complete_graph(4)
    assert jg.graph_to_string(k4, "graph6").strip() == "C~"
    for variant in ["graph6", "sparse6"]:
        h = jg.parse_graph(jg.graph_to_string(k4, "graph6", variant=variant), "graph6")
        assert h.edge_count() == 6
    d = jg.complete_graph(3, directed=True)
    h = jg.parse_graph(jg.graph_to_string(d, "graph6"), "graph6")
    assert h.directed and h.edge_count() == 6
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(k4, "graph6", vertex_id=str)


def test_json_names_and_edge_ids():
    g = labelled()
    text = jg.graph_to_string(g, "json", vertex_id=str, edge_id=lambda e: f"e{e}", vertices_name="V", edges_name="E")
    assert '"V"' in text and '"E"' in text and '"e0"' in text
    h = jg.parse_graph(text, "json", vertices_name="V", edges_name="E")
    assert h.edge_count() == 4


def test_text_only_exporters():
    g = labelled(weighted=True)
    lemon = jg.graph_to_string(g, "lemon", edge_weights=True, vertex_id=str)
    assert "@nodes" in lemon and "@arcs" in lemon
    m = jg.graph_to_string(jg.path_graph(3), "matrix")
    assert len(m.strip().splitlines()) == 4
    assert jg.graph_to_string(jg.path_graph(3), "matrix", variant="laplacian")
    assert jg.graph_to_string(g, "visio", vertex_id=str)
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(jg.path_graph(3, directed=True), "matrix", variant="laplacian")


def test_gexf_options():
    g = labelled(weighted=True)
    text = jg.graph_to_string(g, "gexf", edge_weights=True, creator="me", description="d", keywords="k")
    assert "me" in text and 'weight="1' in text
    assert "<creator>" not in jg.graph_to_string(g, "gexf", meta=False)


def test_gml_options():
    g = labelled(weighted=True)
    text = jg.graph_to_string(
        g, "gml", edge_weights=True, vertex_labels=True, vertex_attributes={"a": {"label": "A", "k": 1}}
    )
    assert 'label "A"' in text and "weight" in text and "k 1" in text


def test_vertex_id_must_be_injective():
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(labelled(), "json", vertex_id=lambda v: "same")


def test_callback_errors_propagate():
    def boom(v):
        raise KeyError("boom")

    with pytest.raises(KeyError):
        jg.graph_to_string(labelled(), "json", vertex_id=boom)
    with pytest.raises(KeyError):
        jg.graph_to_string(labelled(), "graphml", vertex_attributes=boom)


def test_attribute_values_must_be_dicts():
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(labelled(), "graphml", vertex_attributes={"a": 3})


def test_files(tmp_path):
    g = labelled()
    path = tmp_path / "g.graphml"
    jg.write_graph(g, path, "graphml", vertex_id=str)
    h = jg.read_graph(path, "graphml")
    assert edge_set(h) == edge_set(g)
    jg.write_graph(g, str(path), "graphml", vertex_id=str)
    assert edge_set(jg.read_graph(str(path), "graphml")) == edge_set(g)
    with open(path, "rb") as f:
        assert edge_set(jg.read_graph(f, "graphml")) == edge_set(g)
    with open(path) as f:
        assert edge_set(jg.read_graph(f, "graphml")) == edge_set(g)
    buf = io.StringIO()
    jg.write_graph(g, buf, "json", vertex_id=str)
    assert edge_set(jg.read_graph(io.StringIO(buf.getvalue()), "json")) == edge_set(g)
    buf = io.BytesIO()
    jg.write_graph(g, buf, "json", vertex_id=str)
    assert edge_set(jg.parse_graph(buf.getvalue(), "json")) == edge_set(g)
    with pytest.raises(OSError):
        jg.read_graph(tmp_path / "missing.gml", "gml")
    with pytest.raises(TypeError):
        jg.read_graph(3, "gml")


def test_errors():
    with pytest.raises(jg.GraphError):
        jg.parse_graph("x", "nope")
    with pytest.raises(jg.GraphError):
        jg.parse_graph("x", "lemon")
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(jg.path_graph(2), "tsplib")
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(jg.path_graph(2), "json", bogus=1)
    with pytest.raises(jg.GraphError):
        jg.parse_graph("{}", "json", bogus=1)
    with pytest.raises(jg.GraphError):
        jg.parse_graph("not graphml at all <", "graphml")
    with pytest.raises(TypeError):
        jg.graph_to_string("graph", "json")


def test_tsplib():
    g = jg.parse_graph(TSP, "tsplib")
    assert g.weighted and not g.directed
    assert (len(list(g.vertices())), g.edge_count()) == (4, 6)
    assert jg.diameter(g) == 5.0
    meta = g.graph_attrs["tsplib"]
    assert meta["name"] == "sq" and meta["dimension"] == 4 and meta["edge_weight_type"] == "EUC_2D"
    assert meta["coordinates"][2] == (4.0, 3.0) and meta["node_numbers"][2] == 3
    assert meta["tour"] is None
    s = jg.parse_graph(TSP, "tsplib", sparse=True)
    assert s.weighted and s.edge_count() == 6


def test_generated_graphs_roundtrip():
    g = jg.gnm_random_graph(30, 60, seed=3)
    h = jg.parse_graph(jg.graph_to_string(g, "graphml"), "graphml", vertex_factory=int)
    assert sorted(h.vertices()) == list(range(1, 31))
    assert h.edge_count() == 60
    p = jg.named_graph("petersen")
    for fmt in ["gml", "gexf", "json", "dot", "graphml", "dimacs", "graph6"]:
        h = jg.parse_graph(jg.graph_to_string(p, fmt), fmt)
        assert h.edge_count() == 15, fmt
        assert jg.girth(h) == 5, fmt


# options a format cannot use are rejected, not ignored
UNSUPPORTED = [
    ("csv", "vertex_attributes"),
    ("csv", "edge_attributes"),
    ("csv", "graph_attributes"),
    ("csv", "edge_id"),
    ("csv", "graph_id"),
    ("dimacs", "vertex_attributes"),
    ("dimacs", "edge_id"),
    ("dot", "edge_id"),
    ("gexf", "graph_attributes"),
    ("gml", "vertex_id"),
    ("gml", "graph_attributes"),
    ("graph6", "vertex_id"),
    ("graph6", "vertex_attributes"),
    ("graphml", "graph_id"),
    ("json", "graph_attributes"),
    ("lemon", "vertex_attributes"),
    ("matrix", "edge_attributes"),
    ("visio", "edge_id"),
]


@pytest.mark.parametrize("fmt,option", UNSUPPORTED)
def test_unsupported_common_options_are_rejected(fmt, option):
    value = {"graph_id": "g"}.get(option, lambda x: "1" if option.endswith("_id") else {})
    with pytest.raises(jg.GraphError, match=option):
        jg.graph_to_string(jg.path_graph(3), fmt, **{option: value})


def test_supported_common_options_are_accepted():
    g = jg.path_graph(3)
    kw = {"vertex_id": str, "edge_id": str, "vertex_attributes": {}, "edge_attributes": {}, "graph_attributes": {}}
    allowed = {
        "csv": ["vertex_id"],
        "dimacs": ["vertex_id"],
        "dot": ["vertex_id", "vertex_attributes", "edge_attributes", "graph_attributes"],
        "gexf": ["vertex_id", "edge_id", "vertex_attributes", "edge_attributes"],
        "gml": ["edge_id", "vertex_attributes", "edge_attributes"],
        "graphml": list(kw),
        "json": ["vertex_id", "edge_id", "vertex_attributes", "edge_attributes"],
        "lemon": ["vertex_id"],
        "matrix": ["vertex_id"],
        "visio": ["vertex_id"],
    }
    for fmt, names in allowed.items():
        assert jg.graph_to_string(g, fmt, **{n: kw[n] for n in names}), fmt
    assert jg.graph_to_string(g, "dot", graph_id="g").startswith("strict graph g")


def quoted():
    g = jg.Graph(weighted=True, directed=True)
    for v in ['a "q"', "b\\c"]:
        g.add_vertex(v)
    g.add_edge('a "q"', "b\\c", edge="e", weight=2.5)
    return g


def test_lemon_escape_strings():
    g = quoted()
    plain = jg.graph_to_string(g, "lemon", vertex_id=str, edge_weights=True)
    assert 'a "q"\tb\\c\t2.5' in plain
    escaped = jg.graph_to_string(g, "lemon", vertex_id=str, edge_weights=True, escape_strings=True)
    assert '"a \\"q\\""\t"b\\\\c"\t2.5' in escaped
    assert "weight" not in jg.graph_to_string(g, "lemon", vertex_id=str)


def test_gml_escape_strings_and_labels():
    g = quoted()
    attrs = {'a "q"': {"label": 'x "y"\n'}}
    escaped = jg.graph_to_string(g, "gml", vertex_labels=True, vertex_attributes=attrs, escape_strings=True)
    assert 'label "x \\"y\\"\\n"' in escaped
    plain = jg.graph_to_string(g, "gml", vertex_labels=True, vertex_attributes=attrs)
    assert 'label "x "y"\n"' in plain  # unescaped: quote and newline written as they are
    # attributes that are given are written as custom attributes even without vertex_labels
    assert 'label "x' in jg.graph_to_string(g, "gml", vertex_attributes=attrs)
    labelled = jg.graph_to_string(g, "gml", edge_labels=True, edge_attributes={"e": {"label": "E1"}})
    assert 'label "E1"' in labelled


def test_gexf_edge_labels_and_types():
    g = quoted()
    kw = {"edge_attributes": {"e": {"label": "L"}}}
    text = jg.graph_to_string(g, "gexf", edge_labels=True, edge_types=True, **kw)
    assert 'type="directed" label="L"' in text
    plain = jg.graph_to_string(g, "gexf", **kw)
    assert "label=" not in plain.split("<edges>")[1] and "type=" not in plain.split("<edges>")[1]
    assert 'weight="2.5"' in jg.graph_to_string(g, "gexf", edge_weights=True)
    assert 'weight=' not in jg.graph_to_string(g, "gexf")


def test_gexf_registered_attribute_types():
    g = jg.path_graph(2)
    text = jg.graph_to_string(
        g, "gexf", vertex_attributes={0: {"n": 3, "x": 1.5, "ok": True, "s": "t"}, 1: {"n": 4}}
    )
    for name, kind in [("n", "integer"), ("x", "double"), ("ok", "boolean"), ("s", "string")]:
        assert f'title="{name}" type="{kind}"' in text
    h, a = parse_graph(text, "gexf", attributes=True)
    assert a["vertices"]["1"]["n"] == 3 and a["vertices"]["1"]["ok"] is True


def test_graphml_registered_attribute_types_and_mixed_numbers():
    g = jg.path_graph(3)
    text = jg.graph_to_string(
        g, "graphml", vertex_attributes={0: {"n": 3, "x": 1.5, "m": 1}, 1: {"m": 2.5}}
    )
    assert 'attr.name="n" attr.type="int"' in text
    assert 'attr.name="x" attr.type="double"' in text
    assert 'attr.name="m" attr.type="double"' in text  # int and float values merge to double
    h, a = parse_graph(text, "graphml", attributes=True)
    assert a["vertices"]["1"]["n"] == 3 and a["vertices"]["2"]["m"] == 2.5


def test_attribute_values_types_and_null():
    g = jg.path_graph(2)
    attrs = {0: {"big": 2**40, "none": None, "flag": False}}
    text = jg.graph_to_string(g, "json", vertex_attributes=attrs)
    h, a = parse_graph(text, "json", attributes=True)
    v = a["vertices"]["1"]
    assert v["big"] == 2**40 and v["none"] is None and v["flag"] is False


DIRECTED_DOCS = [
    ("dot", "digraph G { a -> b }"),
    ("dot", "DiGraph { a -> b }"),
    ("dot", "strict digraph { a -> b }"),
    ("dot", "// graph \n/* graph */ # graph\ndigraph graph_x { a -> b }"),
    ("gml", "graph [ directed 1 node [ id 1 ] ]"),
    ("gml", '# directed 0\ngraph [ comment "directed 0" node [ id 1 ] directed 1 ]'),
    ("graphml", '<graphml><graph edgedefault="directed"><node id="a"/></graph></graphml>'),
    ("graphml", "<graphml><graph\n  id='G'\n edgedefault = 'directed' ><node id='a'/></graph></graphml>"),
    ("graphml", '<!-- <graph edgedefault="undirected"> --><g:graphml xmlns:g="x"><g:graph g:edgedefault="directed"/></g:graphml>'),
    ("gexf", '<gexf version="1.2"><graph mode="static" defaultedgetype="directed"><nodes><node id="1"/></nodes></graph></gexf>'),
    ("dimacs", "c p edge 3 0\np sp 3 0\n"),
    ("graph6", "&AG\n"),
]

UNDIRECTED_DOCS = [
    ("dot", "graph G { a -- b }"),
    ("dot", "strict graph digraph_like { a -- b }"),
    ("dot", '/* digraph */ graph { a -- b }'),
    ("dot", 'graph { "digraph" -- b }'),
    ("gml", "graph [ directed 0 node [ id 1 ] ]"),
    ("gml", 'graph [ node [ id 1 label "directed 1" ] ]'),
    ("gml", "graph [ node [ id 1 ] edge [ source 1 target 1 directed 1 ] ]"),
    ("graphml", '<graphml><graph edgedefault="undirected"><node id="a"/></graph></graphml>'),
    ("graphml", '<graphml><graph><node id="a" title=\'edgedefault="directed"\'/></graph></graphml>'),
    ("graphml", '<graphml><!-- <graph edgedefault="directed"> --><graph edgedefault="undirected"/></graphml>'),
    ("gexf", '<gexf version="1.2"><graph defaultedgetype="undirected"><nodes><node id="1"/></nodes></graph></gexf>'),
    ("dimacs", "c p sp\np edge 3 0\n"),
    ("graph6", "A_\n"),
    ("graph6", ">>graph6<<A_\n"),
]


@pytest.mark.parametrize("fmt,text", DIRECTED_DOCS)
def test_directed_detection(fmt, text):
    assert jg.parse_graph(text, fmt).directed


@pytest.mark.parametrize("fmt,text", UNDIRECTED_DOCS)
def test_undirected_detection(fmt, text):
    assert not jg.parse_graph(text, fmt).directed


def test_graphml_declared_attribute_types_and_defaults():
    g = jg.path_graph(3)
    text = jg.graph_to_string(
        g,
        "graphml",
        vertex_attributes={0: {"n": 3}},
        vertex_attribute_types={"n": "long", "color": ("string", "blue"), "unused": "boolean"},
        edge_attribute_types={"cost": ("double", 1.5)},
        graph_attribute_types={"title": "string"},
        graph_attributes={"title": "demo"},
    )
    assert 'attr.name="n" attr.type="long"' in text
    assert 'attr.name="color" attr.type="string"' in text and "<default>blue</default>" in text
    assert 'attr.name="unused" attr.type="boolean"' in text
    assert 'attr.name="cost" attr.type="double"' in text and "<default>1.5</default>" in text
    h, a = parse_graph(text, "graphml", attributes=True)
    assert a["vertices"]["2"]["color"] == "blue" and a["vertices"]["1"]["n"] == 3
    assert a["edges"][0]["cost"] == 1.5
    assert a["graph"]["title"] == "demo"


def test_graphml_custom_label_and_weight_names():
    g = jg.as_weighted(jg.path_graph(2), 4.0)
    text = jg.graph_to_string(
        g,
        "graphml",
        edge_weights=True,
        vertex_labels=True,
        edge_labels=True,
        vertex_label_attribute="name",
        edge_label_attribute="tag",
        edge_weight_attribute="cost",
        vertex_attributes={0: {"name": "start"}},
        edge_attributes={0: {"tag": "t"}},
    )
    for name in ["name", "tag", "cost"]:
        assert f'attr.name="{name}"' in text
    assert 'attr.name="label"' not in text and 'attr.name="weight"' not in text
    h, a = parse_graph(text, "graphml", weighted=True, edge_weight_attribute="cost", attributes=True)
    assert h.edge_weight(0) == 4.0 and a["edges"][0]["tag"] == "t"
    assert a["vertices"]["1"]["name"] == "start"
    # a name that is declared as a regular attribute cannot be reused
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(
            g, "graphml", edge_weight_attribute="cost", edge_attribute_types={"cost": "double"}
        )


def test_gexf_declared_attribute_types():
    g = jg.path_graph(2)
    text = jg.graph_to_string(
        g,
        "gexf",
        vertex_attribute_types={"tags": "liststring", "home": "anyURI", "color": ("string", "red")},
        edge_attribute_types={"w": "float"},
    )
    for name, kind in [("tags", "liststring"), ("home", "anyURI"), ("color", "string"), ("w", "float")]:
        assert f'title="{name}" type="{kind}"' in text
    assert "<default>red</default>" in text
    with pytest.raises(jg.GraphError, match="unknown GEXF attribute type"):
        jg.graph_to_string(g, "gexf", vertex_attribute_types={"x": "bogus"})
    with pytest.raises(jg.GraphError, match="unknown attribute type"):
        jg.graph_to_string(g, "graphml", vertex_attribute_types={"x": "bogus"})
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "graphml", vertex_attribute_types=["n"])
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "json", vertex_attribute_types={"n": "int"})


def test_dot_subgraphs():
    g = jg.Graph()
    for v in "abcd":
        g.add_vertex(v)
    for u, v in [("a", "b"), ("b", "c"), ("c", "d")]:
        g.add_edge(u, v, edge=u + v)
    text = jg.graph_to_string(
        g,
        "dot",
        vertex_id=str,
        subgraphs={
            "cluster_1": {
                "vertices": ["a", "b"],
                "edges": ["ab"],
                "graph_attributes": {"label": "first"},
                "cluster_attributes": {"color": "red"},
            },
            "s2": {"vertices": ("c", "d")},
        },
    )
    block = text.split("subgraph cluster_1 {")[1].split("}")[0]
    assert "label=first;" in block and "a -- b;" in block and 'color="red"' in block
    assert text.index("subgraph cluster_1") < text.index("subgraph s2")
    assert "c;\n    d;" in text.split("subgraph s2 {")[1]
    # the output is valid DOT, and the graph itself is unchanged by the subgraphs
    h = jg.parse_graph(text, "dot")
    assert h.edge_count() == 3


def test_dot_subgraph_errors():
    g = labelled()
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "dot", subgraphs=[1])
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "dot", subgraphs={"s": {"nope": []}})
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "dot", subgraphs={"s": {"vertices": ["zzz"]}})
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "dot", subgraphs={"s": {"edges": ["zzz"]}})
    with pytest.raises(jg.GraphError):  # not a DOT identifier
        jg.graph_to_string(g, "dot", subgraphs={"not valid": {"vertices": ["a"]}})
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "json", subgraphs={"s": {}})


def test_gml_vertex_graphics():
    g = jg.path_graph(3)
    text = jg.graph_to_string(
        g, "gml", vertex_graphics={0: {"fill": "#FF0000", "w": 10.5, "h": 4}, 2: {"type": "oval"}}
    )
    assert 'graphics\n\t\t[\n\t\t\tfill "#FF0000"' in text
    assert "w 10.5" in text and "h 4" in text and 'type "oval"' in text
    assert text.count("graphics") == 3  # vertex 1 gets an empty block
    by_function = jg.graph_to_string(g, "gml", vertex_graphics=lambda v: {"fill": f"c{v}"})
    assert by_function.count("graphics") == 3 and 'fill "c1"' in by_function
    # the output is readable and keeps the attributes of the vertices
    h, a = parse_graph(text, "gml", attributes=True)
    assert nv_(h) == 3
    with pytest.raises(TypeError):
        jg.graph_to_string(g, "gml", vertex_graphics=3)
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "json", vertex_graphics={})


def nv_(g):
    return len(list(g.vertices()))


def test_import_into_existing_graph():
    g = jg.Graph()
    g.add_vertex("a")
    g.add_vertex("zzz")
    g.add_edge("a", "zzz", edge="old")
    text = jg.graph_to_string(labelled(), "json", vertex_id=str)
    result, attrs = parse_graph(text, "json", into=g, attributes=True)
    assert result is g
    assert sorted(g.vertices()) == ["a", "b", "c", "d", "zzz"]  # "a" was reused
    assert g.edge_count() == 5 and "old" in g.edges()
    assert set(attrs["edges"]) <= set(g.edges())  # keyed by the edges of g
    assert not g.weighted
    # a second import adds again; parallel edges need a graph that allows them
    with pytest.raises(jg.GraphError, match="rejected"):
        jg.parse_graph(text, "json", into=g)


def test_import_into_weighted_and_directed():
    g = jg.Graph(directed=True, weighted=True)
    text = jg.graph_to_string(labelled(directed=True, weighted=True), "gml", edge_weights=True)
    jg.parse_graph(text, "gml", into=g)  # direction and weights follow the graph
    assert g.directed and g.weighted
    assert sorted(g.edge_weight(e) for e in g.edges()) == [1.0, 2.0, 3.0, 4.0]
    with pytest.raises(jg.GraphError, match="direction"):
        jg.parse_graph(text, "gml", into=g, directed=False)
    with pytest.raises(jg.GraphError, match="not weighted"):
        jg.parse_graph(text, "gml", into=jg.Graph(directed=True), weighted=True)


def test_import_into_restrictions():
    text = jg.graph_to_string(labelled(), "json", vertex_id=str)
    with pytest.raises(jg.GraphError):
        jg.parse_graph(text, "json", into=jg.path_graph(2, sparse=True))
    with pytest.raises(jg.GraphError):
        jg.parse_graph(text, "json", into=jg.Graph(), sparse=True)
    g = jg.Graph(allow_self_loops=False)
    with pytest.raises(jg.GraphError, match="self-loops"):
        jg.parse_graph('{"nodes":[{"id":"x"}],"edges":[{"source":"x","target":"x"}]}', "json", into=g)
    # vertex_factory applies before the vertices are added
    g = jg.Graph()
    jg.parse_graph(text, "json", into=g, vertex_factory=str.upper)
    assert sorted(g.vertices()) == ["A", "B", "C", "D"]


def test_gexf_custom_ids():
    g = labelled()
    text = jg.graph_to_string(g, "gexf", vertex_id=lambda v: f"node-{v}", edge_id=lambda e: f"link-{e}")
    assert '<node id="node-a"' in text and 'id="link-0"' in text
    assert 'source="node-a" target="node-b"' in text
    h, a = parse_graph(text, "gexf", attributes=True)
    assert sorted(h.vertices()) == ["node-a", "node-b", "node-c", "node-d"]
    with pytest.raises(jg.GraphError):
        jg.graph_to_string(g, "gexf", vertex_id=lambda v: "same")


def test_digraph6_header():
    d = jg.complete_graph(3, directed=True)
    text = jg.graph_to_string(d, "graph6")
    assert text.startswith("&")
    for doc in (text, ">>digraph6<<" + text):
        h = jg.parse_graph(doc, "graph6")
        assert h.directed and h.edge_count() == 6
