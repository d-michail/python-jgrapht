import pytest

pydot = pytest.importorskip("pydot")

from jgrapht import create_graph
from jgrapht.convert import to_pydot, from_pydot


def test_int_graph_to_pydot():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)

    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    g.add_edge(2, 3, weight=100.0)

    astext = str(to_pydot(g))

    expected="""graph G {
0;
1;
2;
3;
4;
5;
0 -- 1  [weight="1.0"];
1 -- 2  [weight="1.0"];
2 -- 0  [weight="1.0"];
3 -- 4  [weight="1.0"];
4 -- 5  [weight="1.0"];
5 -- 3  [weight="1.0"];
2 -- 3  [weight="100.0"];
}
"""
    assert expected.splitlines() == astext.splitlines()


def test_any_hashable_graph_to_pydot():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
        any_hashable=True
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "0")

    e34 = g.add_edge("3", "4")
    g.add_edge("4", "5")
    g.add_edge("5", "3")

    g.add_edge("2", "3", edge="e23_1", weight=100.0)
    g.add_edge("2", "3", edge="e23_2", weight=50.0)

    g.vertex_attrs["3"]["name"] = "shouldnowshowup"
    g.vertex_attrs["5"]["label"] = "v5"
    g.vertex_attrs["4"]["label"] = "v4"

    g.edge_attrs[e34]["name"] = "e34"
    g.edge_attrs[e34]["color"] = "red"

    astext = str(to_pydot(g))

    expected = """strict graph G {
0;
1;
2;
3;
4 [label=v4];
5 [label=v5];
0 -- 1;
1 -- 2;
2 -- 0;
3 -- 4  [color=red, name=e34];
4 -- 5;
5 -- 3;
2 -- 3;
2 -- 3;
}
"""

    assert expected.splitlines() == astext.splitlines()




def test_any_hashable_no_multiple_edges_graph_to_pydot():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "0")

    e34 = g.add_edge("3", "4")
    g.add_edge("4", "5")
    g.add_edge("5", "3")

    g.add_edge("2", "3", edge="e23")

    g.vertex_attrs["5"]["label"] = "v5"
    g.vertex_attrs["4"]["label"] = "v4"

    g.edge_attrs["e23"]["name"] = "e23"
    g.edge_attrs[e34]["name"] = "e34"

    astext = str(to_pydot(g))

    expected = """graph G {
0;
1;
2;
3;
4 [label=v4];
5 [label=v5];
0 -- 1;
1 -- 2;
2 -- 0;
3 -- 4  [name=e34];
4 -- 5;
5 -- 3;
2 -- 3  [name=e23];
}
"""

    assert expected.splitlines() == astext.splitlines()


def test_int_graph_from_pydot():

    graph_data = 'digraph G { 0; 1; 2; 0->1; 1->2 [weight=5.0]; }'
    graphs = pydot.graph_from_dot_data(graph_data)
    dotg = graphs[0]

    g = from_pydot(dotg)

    assert g.type.directed
    assert g.type.weighted

    assert g.number_of_vertices == 3
    assert g.number_of_edges == 2
    assert g.vertices == {"0", "1", "2"}

    all_edges = [e for e in g.edges]

    assert g.edge_source(all_edges[0]) == "0"
    assert g.edge_target(all_edges[0]) == "1"
    assert g.get_edge_weight(all_edges[0]) == 1.0

    assert g.edge_source(all_edges[1]) == "1"
    assert g.edge_target(all_edges[1]) == "2"
    assert g.get_edge_weight(all_edges[1]) == 5.0


def test_graph_default_styles_from_pydot():

    graph_data = 'graph G { 5; node [style=blue]; 6; 7; edge [style=red]; 5->6; 6->7; }'
    graphs = pydot.graph_from_dot_data(graph_data)
    dotg = graphs[0]

    g = from_pydot(dotg)

    assert not g.type.directed
    assert g.type.weighted

    assert g.number_of_vertices == 3
    assert g.number_of_edges == 2
    assert g.vertices == {"5", "6", "7"}

    assert g.graph_attrs == {'name': 'G', 'vertex': {'style': 'blue'}, 'edge': {'style': 'red'}}

