import pytest

import jgrapht as jg

CSV_EDGES = "a,b\nb,c\n"
JSON = '{"nodes":[{"id":"a","x":1},{"id":"b"}],"edges":[{"source":"a","target":"b","weight":2.5}]}'
GRAPHML = '<graphml><key id="c" for="node" attr.name="color" attr.type="string"/><graph><node id="a"><data key="c">red</data></node><node id="b"/><edge source="a" target="b"/></graph></graphml>'
GEXF = '<gexf version="1.2"><graph defaultedgetype="undirected"><nodes><node id="1"/><node id="2"/></nodes><edges><edge source="1" target="2"/></edges></graph></gexf>'
DOC = {
    "csv": CSV_EDGES,
    "dimacs": "p edge 3 2\ne 1 2\ne 2 3\n",
    "graph6": "Bw",
    "json": JSON,
    "graphml": GRAPHML,
    "graphml_edge_list": GRAPHML,
    "gexf": GEXF,
}
OPTIONS = {"csv": {"variant": "edge_list"}}


def test_event_formats():
    assert set(jg.event_formats()) == set(DOC)


@pytest.mark.parametrize("fmt", sorted(DOC))
def test_events_are_framed_and_match_callback(fmt):
    events = jg.parse_events(DOC[fmt], fmt, **OPTIONS.get(fmt, {}))
    assert events[0] == ("start",) and events[-1] == ("end",)
    seen = []
    assert jg.parse_events(DOC[fmt], fmt, seen.append, **OPTIONS.get(fmt, {})) is None
    assert seen == events


def test_csv_events():
    assert jg.parse_events(CSV_EDGES, "csv", variant="edge_list") == [
        ("start",),
        ("vertex", "a"),
        ("vertex", "b"),
        ("edge", ("a", "b", None)),
        ("vertex", "c"),
        ("edge", ("b", "c", None)),
        ("end",),
    ]
    events = jg.parse_events("a;b;2\n", "csv", variant="edge_list", delimiter=";", weighted=True)
    assert ("edge", ("a", "b", 2.0)) in events
    matrix = jg.parse_events(";1\n1;\n", "csv", variant="matrix", delimiter=";")
    assert [e for e in matrix if e[0] == "edge"]


def test_dimacs_events_and_numbering():
    text = "p edge 3 2\ne 1 2\ne 2 3\n"
    assert jg.parse_events(text, "dimacs") == [
        ("start",),
        ("vertex_count", 3),
        ("edge_count", 2),
        ("edge", (1, 2, None)),
        ("edge", (2, 3, None)),
        ("end",),
    ]
    zero = jg.parse_events(text, "dimacs", zero_based_numbering=True)
    assert ("edge", (0, 1, None)) in zero
    weighted = jg.parse_events("p edge 2 1\ne 1 2 7.5\n", "dimacs")
    assert ("edge", (1, 2, 7.5)) in weighted


def test_graph6_events():
    events = jg.parse_events("Bw", "graph6")  # the triangle
    assert ("vertex_count", 3) in events
    assert [v for k, v in (e for e in events if e[0] == "vertex")] == [0, 1, 2]
    assert sorted(e[1] for e in events if e[0] == "edge") == [(1, 0), (2, 0), (2, 1)]


def test_json_events_and_names():
    events = jg.parse_events(JSON, "json")
    assert ("vertex_with_attributes", "a", {"x": 1}) in events
    assert ("edge_with_attributes", ("a", "b", 2.5), {"weight": 2.5}) in events
    custom = '{"V":[{"id":"a"}],"E":[]}'
    assert ("vertex_with_attributes", "a", {}) in jg.parse_events(
        custom, "json", vertices_name="V", edges_name="E"
    )


def test_graphml_and_gexf_events():
    events = jg.parse_events(GRAPHML, "graphml")
    assert ("vertex", "a") in events
    assert ("vertex_attribute", "a", "color", "red") in events
    assert ("vertex_attribute", "a", "ID", "a") in events
    assert ("edge", ("a", "b", None)) in events
    assert jg.parse_events(GRAPHML, "graphml_edge_list") == [("start",), ("edge", (0, 1, None)), ("end",)]
    events = jg.parse_events(GEXF, "gexf")
    assert ("edge", ("1", "2", None)) in events
    weighted = GRAPHML.replace("<key", '<key id="w" for="edge" attr.name="cost" attr.type="double"/><key', 1).replace(
        '<edge source="a" target="b"/>', '<edge source="a" target="b"><data key="w">4.5</data></edge>'
    )
    events = jg.parse_events(weighted, "graphml", edge_weight_attribute="cost")
    assert ("edge", ("a", "b", 4.5)) in events


def test_callback_errors_stop_the_import():
    seen = []

    def callback(event):
        seen.append(event[0])
        if event[0] == "vertex":
            raise KeyError("stop")

    with pytest.raises(KeyError):
        jg.parse_events(CSV_EDGES, "csv", callback, variant="edge_list")
    assert seen == ["start", "vertex"]


def test_events_from_files(tmp_path):
    path = tmp_path / "g.csv"
    path.write_text(CSV_EDGES)
    assert jg.read_events(path, "csv", variant="edge_list") == jg.parse_events(CSV_EDGES, "csv", variant="edge_list")
    with open(path, "rb") as f:
        assert jg.read_events(f, "csv", variant="edge_list")[-1] == ("end",)
    with pytest.raises(OSError):
        jg.read_events(tmp_path / "missing", "csv")


def test_event_errors():
    with pytest.raises(jg.GraphError, match="no event-driven importer"):
        jg.parse_events("graph {}", "dot")
    with pytest.raises(jg.GraphError):
        jg.parse_events("x", "csv", bogus=1)
    with pytest.raises(jg.GraphError):
        jg.parse_events("e 1 2\n", "dimacs")  # no problem line
    with pytest.raises(jg.GraphError):
        jg.parse_events("{", "json")


def test_schema_validation_switch():
    # accepted for GraphML and GEXF (read and events); the Rust parser does not validate yet
    for fmt, doc in [("graphml", GRAPHML), ("gexf", GEXF)]:
        for flag in (True, False):
            assert jg.parse_graph(doc, fmt, schema_validation=flag).edge_count() == 1
            assert jg.parse_events(doc, fmt, schema_validation=flag)[-1] == ("end",)
    assert jg.parse_events(GRAPHML, "graphml_edge_list", schema_validation=False)
    for fmt, doc in [("json", JSON), ("csv", CSV_EDGES)]:
        with pytest.raises(jg.GraphError):
            jg.parse_graph(doc, fmt, schema_validation=True)
        with pytest.raises(jg.GraphError):
            jg.parse_events(doc, fmt, schema_validation=True)
