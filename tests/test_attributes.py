import pytest

import jgrapht as jg


def labelled():
    g = jg.Graph(directed=True, weighted=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", edge="ab", weight=1.0)
    g.add_edge("b", "c", edge="bc", weight=2.0)
    g.add_edge("c", "d", edge="cd", weight=3.0)
    return g


def test_vertex_edge_and_graph_attributes_are_live_dicts():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    g.vertex_attrs["a"]["size"] = 3
    g.edge_attrs["ab"]["kind"] = "road"
    g.graph_attrs["name"] = "demo"
    assert g.vertex_attrs["a"] == {"color": "red", "size": 3}
    assert g.vertex_attrs["a"] is g.vertex_attrs["a"]  # the same live dict every time
    assert g.edge_attrs["ab"] == {"kind": "road"}
    assert g.graph_attrs == {"name": "demo"} and g.graph_attrs is g.graph_attrs


def test_mapping_methods_count_only_vertices_with_attributes():
    g = labelled()
    assert len(g.vertex_attrs) == 0 and list(g.vertex_attrs) == []
    g.vertex_attrs["b"]["x"] = 1
    g.vertex_attrs["a"]  # asking for the dict of a vertex does not count it
    g.vertex_attrs["c"]["y"] = 2
    assert len(g.vertex_attrs) == 2
    assert list(g.vertex_attrs) == ["b", "c"] == g.vertex_attrs.keys()
    assert g.vertex_attrs.values() == [{"x": 1}, {"y": 2}]
    assert g.vertex_attrs.items() == [("b", {"x": 1}), ("c", {"y": 2})]
    assert "b" in g.vertex_attrs and "a" not in g.vertex_attrs and "zzz" not in g.vertex_attrs
    assert g.vertex_attrs.get("a") is None and g.vertex_attrs.get("a", 7) == 7
    assert g.vertex_attrs.get("b") == {"x": 1}


def test_set_replaces_and_delete_removes():
    g = labelled()
    g.vertex_attrs["a"]["old"] = 1
    live = g.vertex_attrs["a"]
    g.vertex_attrs["a"] = {"new": 2}
    assert g.vertex_attrs["a"] == {"new": 2} and live is g.vertex_attrs["a"]
    del g.vertex_attrs["a"]
    assert "a" not in g.vertex_attrs and g.vertex_attrs["a"] == {}
    with pytest.raises(KeyError):
        del g.vertex_attrs["a"]
    with pytest.raises(TypeError):
        g.vertex_attrs["a"] = 5


def test_unknown_vertices_and_edges_are_errors():
    g = labelled()
    with pytest.raises(jg.GraphError):
        g.vertex_attrs["nope"]
    with pytest.raises(jg.GraphError):
        g.edge_attrs["nope"]
    with pytest.raises(jg.GraphError):
        g.vertex_attrs["nope"] = {}


def test_removing_a_vertex_or_edge_removes_its_attributes():
    g = labelled()
    g.vertex_attrs["b"]["x"] = 1
    g.edge_attrs["ab"]["x"] = 1
    g.edge_attrs["bc"]["x"] = 1
    g.edge_attrs["cd"]["x"] = 1
    g.remove_vertex("b")  # also removes the edges ab and bc
    assert len(g.vertex_attrs) == 0 and list(g.edge_attrs) == ["cd"]
    g.remove_edge("cd")
    assert len(g.edge_attrs) == 0
    g.add_vertex("b")  # a vertex added again starts without attributes
    assert g.vertex_attrs["b"] == {}


def test_the_weight_is_not_an_attribute():
    g = labelled()
    assert g.edge_attrs["ab"] == {} and g.edge_weight("ab") == 1.0


def test_sparse_graph_attributes():
    s = jg.SparseGraph(3, [(0, 1), (1, 2)], directed=True)
    s.vertex_attrs[0]["x"] = 1
    s.edge_attrs[1]["y"] = 2
    s.graph_attrs["name"] = "sparse"
    assert s.vertex_attrs.items() == [(0, {"x": 1})] and s.edge_attrs.items() == [(1, {"y": 2})]
    assert 0 in s.vertex_attrs and 2 not in s.vertex_attrs and 99 not in s.vertex_attrs
    with pytest.raises(jg.GraphError):
        s.vertex_attrs[3]
    with pytest.raises(jg.GraphError):
        s.edge_attrs[2]


def test_copies_have_independent_attribute_dicts():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    g.edge_attrs["ab"]["kind"] = "road"
    g.graph_attrs["name"] = "demo"
    c = jg.copy_graph(g)
    assert c.vertex_attrs["a"] == {"color": "red"} and c.edge_attrs["ab"] == {"kind": "road"}
    assert c.graph_attrs == {"name": "demo"}
    c.vertex_attrs["a"]["color"] = "blue"
    c.graph_attrs["name"] = "other"
    assert g.vertex_attrs["a"] == {"color": "red"} and g.graph_attrs == {"name": "demo"}
    values = [1, 2]
    g.vertex_attrs["a"]["list"] = values  # a shallow copy: the values are shared
    assert jg.copy_graph(g).vertex_attrs["a"]["list"] is values


def test_derived_graphs_keep_attributes():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    g.vertex_attrs["d"]["color"] = "blue"
    g.edge_attrs["ab"]["kind"] = "road"
    g.edge_attrs["cd"]["kind"] = "rail"
    s = jg.induced_subgraph(g, ["a", "b", "c"])
    assert s.vertex_attrs.items() == [("a", {"color": "red"})]
    assert s.edge_attrs.items() == [("ab", {"kind": "road"})]
    e = jg.edge_subgraph(g, ["cd"])
    assert sorted(e.vertex_attrs.keys()) == ["d"] and e.edge_attrs["cd"] == {"kind": "rail"}
    for derived in (jg.as_undirected(g), jg.reverse_edges(g), jg.as_unweighted(g), jg.as_weighted(g, 2.0)):
        assert derived.vertex_attrs["a"] == {"color": "red"}
        assert derived.edge_attrs["ab"] == {"kind": "road"}
    sp = jg.SparseGraph(3, [(0, 1)])
    sp.vertex_attrs[2]["z"] = 1
    sp.edge_attrs[0]["w"] = 1
    c = jg.copy_graph(sp)
    assert c.vertex_attrs[2] == {"z": 1} and c.edge_attrs[0] == {"w": 1}


def test_union_merges_attributes_with_graph2_winning():
    a = jg.Graph()
    b = jg.Graph()
    for g in (a, b):
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_edge(1, 2, edge="e")
    a.vertex_attrs[1].update(x=1, shared="a")
    b.vertex_attrs[1].update(y=2, shared="b")
    b.vertex_attrs[2]["only_b"] = True
    a.edge_attrs["e"]["k"] = "a"
    b.edge_attrs["e"]["m"] = "b"
    a.graph_attrs["name"] = "A"
    b.graph_attrs["extra"] = 1
    u = jg.graph_union(a, b)
    assert u.vertex_attrs[1] == {"x": 1, "y": 2, "shared": "b"}
    assert u.vertex_attrs[2] == {"only_b": True}
    assert u.edge_attrs["e"] == {"k": "a", "m": "b"}
    assert u.graph_attrs == {"name": "A", "extra": 1}
    assert a.vertex_attrs[1] == {"x": 1, "shared": "a"}  # the inputs are unchanged


def test_algorithm_results_start_without_attributes():
    g = jg.path_graph(4)
    g.vertex_attrs[0]["x"] = 1
    assert len(jg.complete_graph(3).vertex_attrs) == 0
    assert len(jg.generalized_petersen_graph(5, 2).graph_attrs) == 0


def test_unmodifiable_wrapper_exposes_read_only_attributes():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    g.graph_attrs["name"] = "demo"
    u = jg.as_unmodifiable(g)
    assert u.vertex_attrs["a"] == {"color": "red"} and u.graph_attrs == {"name": "demo"}
    assert len(u.vertex_attrs) == 1 and "a" in u.vertex_attrs
    with pytest.raises(TypeError):
        u.vertex_attrs["a"]["color"] = "blue"
    with pytest.raises(TypeError):
        u.graph_attrs["name"] = "x"
    with pytest.raises(TypeError):
        u.edge_attrs["ab"]["kind"] = 1
    with pytest.raises(jg.GraphError):
        u.vertex_attrs["a"] = {}
    with pytest.raises(jg.GraphError):
        del u.vertex_attrs["a"]
    assert u.vertex_attrs["b"] == {} and len(g.vertex_attrs) == 1  # reading creates nothing
    g.vertex_attrs["b"]["x"] = 1  # the owner's changes are visible
    assert u.vertex_attrs["b"] == {"x": 1}


def test_attributes_can_be_used_from_callbacks_during_an_algorithm():
    g = jg.Graph(weighted=True)
    for v in range(4):
        g.add_vertex(v)
        g.vertex_attrs[v]["x"] = v
    for v in range(3):
        g.add_edge(v, v + 1, weight=1.0)
    seen = []

    def heuristic(v, t):
        seen.append(g.vertex_attrs[v]["x"])  # reads (and could create) attributes mid-algorithm
        g.vertex_attrs[v]["visited"] = True
        return 0.0

    path = jg.astar_shortest_path(g, 0, 3, heuristic)
    assert path.vertices == [0, 1, 2, 3] and seen
    assert g.vertex_attrs[0]["visited"] is True


# ---- file formats ----

GRAPHML = """<?xml version="1.0"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="color" for="node" attr.name="color" attr.type="string"/>
  <key id="kind" for="edge" attr.name="kind" attr.type="string"/>
  <graph id="G" edgedefault="undirected">
    <node id="a"><data key="color">red</data></node>
    <node id="b"/>
    <edge source="a" target="b"><data key="kind">road</data></edge>
  </graph>
</graphml>"""


def test_importers_store_the_attributes_in_the_graph():
    g = jg.parse_graph(GRAPHML, "graphml")
    assert g.vertex_attrs["a"]["color"] == "red" and g.vertex_attrs["b"] == {"ID": "b"}
    assert g.edge_attrs.items() == [(0, {"kind": "road"})]
    assert dict(g.graph_attrs) == {}  # GraphML declares no graph attributes here
    s = jg.parse_graph(GRAPHML, "graphml", sparse=True)
    assert s.vertex_attrs[0]["color"] == "red" and s.edge_attrs[0] == {"kind": "road"}
    assert s.graph_attrs["vertex_ids"] == ["a", "b"]  # the identifiers of the file
    f = jg.parse_graph(GRAPHML, "graphml", vertex_factory=str.upper)
    assert f.vertices() == ["A", "B"] and f.vertex_attrs["A"]["color"] == "red"
    assert f.graph_attrs["vertex_ids"] == ["a", "b"]
    assert "vertex_ids" not in g.graph_attrs  # the vertices are the identifiers themselves


def test_the_attributes_option_is_gone_with_a_helpful_message():
    with pytest.raises(jg.GraphError, match="vertex_attrs"):
        jg.parse_graph(GRAPHML, "graphml", attributes=True)


def test_import_into_an_existing_graph_updates_its_attributes():
    g = jg.Graph()
    g.add_vertex("a")
    g.vertex_attrs["a"]["mine"] = 1
    jg.parse_graph(GRAPHML, "graphml", into=g)
    assert g.vertex_attrs["a"]["color"] == "red" and g.vertex_attrs["a"]["mine"] == 1


def test_exporters_write_the_stored_attributes():
    g = labelled()
    g.vertex_attrs["a"].update(color="red", size=3, ratio=0.5, flag=True)
    g.edge_attrs["ab"]["kind"] = "road"
    g.graph_attrs["title"] = "demo"
    for fmt in ("graphml", "gexf", "json"):
        kw = {"vertex_id": str} if fmt != "gexf" else {}
        back = jg.parse_graph(jg.graph_to_string(g, fmt, **kw), fmt)
        red = [a for a in back.vertex_attrs.values() if a.get("color") == "red"][0]
        assert red["size"] == 3 and red["ratio"] == 0.5 and red["flag"] is True
        assert [a["kind"] for a in back.edge_attrs.values() if "kind" in a] == ["road"]
    text = jg.graph_to_string(g, "graphml", vertex_id=str)
    assert jg.parse_graph(text, "graphml").graph_attrs["title"] == "demo"
    assert 'color="red"' in jg.graph_to_string(g, "dot", vertex_id=str)


def test_an_explicit_option_replaces_the_stored_attributes():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    text = jg.graph_to_string(g, "json", vertex_id=str, vertex_attributes={"b": {"color": "blue"}})
    back = jg.parse_graph(text, "json")
    assert back.vertex_attrs["b"] == {"color": "blue"} and "color" not in back.vertex_attrs["a"]
    empty = jg.parse_graph(jg.graph_to_string(g, "json", vertex_id=str, vertex_attributes={}), "json")
    assert all("color" not in a for a in empty.vertex_attrs.values())


def test_formats_without_attributes_ignore_the_stored_ones():
    g = labelled()
    g.vertex_attrs["a"]["color"] = "red"
    for fmt in ("csv", "dimacs", "graph6", "lemon"):
        assert "red" not in jg.graph_to_string(g, fmt)


def test_other_value_types_are_written_as_strings():
    g = labelled()
    g.vertex_attrs["a"]["tags"] = ["x", "y"]
    back = jg.parse_graph(jg.graph_to_string(g, "graphml", vertex_id=str), "graphml")
    assert back.vertex_attrs["a"]["tags"] == "['x', 'y']"


def test_a_round_trip_through_the_stores_keeps_the_attributes():
    g = jg.parse_graph(GRAPHML, "graphml")
    again = jg.parse_graph(jg.graph_to_string(g, "graphml", vertex_id=str), "graphml")
    assert again.vertex_attrs["a"]["color"] == "red"
    assert again.edge_attrs[0]["kind"] == "road"


def test_tsplib_information_is_a_graph_attribute_and_is_not_written_back():
    text = "NAME: sq\nTYPE: TSP\nDIMENSION: 3\nEDGE_WEIGHT_TYPE: EUC_2D\nNODE_COORD_SECTION\n1 0 0\n2 3 0\n3 3 4\nEOF\n"
    g = jg.parse_graph(text, "tsplib")
    assert g.graph_attrs["tsplib"]["name"] == "sq" and g.graph_attrs["tsplib"]["dimension"] == 3
    out = jg.graph_to_string(g, "graphml", vertex_id=str)
    assert "tsplib" not in out and "vertex_ids" not in out


def test_a_weight_that_was_read_is_not_also_an_attribute():
    text = "digraph { a -> b [weight=2.5, label=x]; }"
    weighted = jg.parse_graph(text, "dot", weighted=True)
    assert weighted.edge_weight(0) == 2.5 and weighted.edge_attrs[0] == {"label": "x"}
    plain = jg.parse_graph(text, "dot")  # unweighted: the weight stays an attribute
    assert not plain.weighted and plain.edge_attrs[0] == {"weight": "2.5", "label": "x"}
    # it is written back as a weight when asked, and the attribute of that name is not duplicated
    again = jg.parse_graph(jg.graph_to_string(weighted, "dot", edge_weights=True), "dot", weighted=True)
    assert again.edge_weight(0) == 2.5 and "weight" not in again.edge_attrs[0]
