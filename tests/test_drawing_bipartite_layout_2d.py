import pytest

from jgrapht import create_graph
import jgrapht.algorithms.drawing as drawing


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
    )

    for i in range(0, 6):
        g.add_vertex(i)

    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(1, 3)
    g.add_edge(1, 5)
    g.add_edge(2, 3)
    g.add_edge(2, 4)

    return g


def build_anyhashable_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    g.add_vertex("0")
    g.add_vertex("1")
    g.add_vertex("2")
    g.add_vertex("3")
    g.add_vertex("4")
    g.add_vertex("5")

    g.add_edge("0", "3", edge="0")
    g.add_edge("0", "4", edge="1")
    g.add_edge("0", "5", edge="2")
    g.add_edge("1", "3", edge="3")
    g.add_edge("1", "5", edge="4")
    g.add_edge("2", "3", edge="5")
    g.add_edge("2", "4", edge="6")

    return g


def test_two_layered_bipartite_layout():
    g = build_graph()

    area = (0, 0, 10, 10)
    model = drawing.two_layered_bipartite_layout_2d(g, area)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (0.0, 0.0),
        (0.0, 5.0),
        (0.0, 10.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (10.0, 10.0),
    ]


def test_anyhashable_two_layered_bipartite_layout():
    g = build_anyhashable_graph()

    area = (0, 0, 10, 10)
    model = drawing.two_layered_bipartite_layout_2d(g, area)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (0.0, 0.0),
        (0.0, 5.0),
        (0.0, 10.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (10.0, 10.0),
    ]



def test_two_layered_bipartite_layout_with_comparator():
    g = build_graph()

    area = (0, 0, 10, 10)

    def vcomp(u, v):
        if u < v:
            return 1
        if u > v:
            return -1
        return 0

    model = drawing.two_layered_bipartite_layout_2d(g, area, vertex_comparator_cb=vcomp)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (0.0, 10.0),
        (0.0, 5.0),
        (0.0, 0.0),
        (10.0, 10.0),
        (10.0, 5.0),
        (10.0, 0.0),
    ]


def test_two_layered_bipartite_layout_horizontal():
    g = build_graph()

    area = (0, 0, 10, 10)
    model = drawing.two_layered_bipartite_layout_2d(g, area, vertical=False)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (0.0, 0.0),
        (5.0, 0.0),
        (10.0, 0.0),
        (0.0, 10.0),
        (5.0, 10.0),
        (10.0, 10.0),
    ]


def test_two_layered_bipartite_layout_with_partition():
    g = build_graph()
    partition = [3, 4, 5]

    area = (0, 0, 10, 10)
    model = drawing.two_layered_bipartite_layout_2d(g, area, partition_a=partition)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]
    print(locations)

    assert locations == [
        (10.0, 0.0),
        (10.0, 5.0),
        (10.0, 10.0),
        (0.0, 0.0),
        (0.0, 5.0),
        (0.0, 10.0),
    ]


def test_barycenter_greedy_two_layered_bipartite_layout():
    g = build_graph()

    area = (0, 0, 10, 10)
    model = drawing.barycenter_greedy_two_layered_bipartite_layout_2d(g, area)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    print(locations)

    assert locations == [
        (0.0, 0.0),
        (0.0, 5.0),
        (0.0, 10.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (10.0, 10.0),
    ]


def test_median_greedy_two_layered_bipartite_layout():
    g = build_graph()

    area = (0, 0, 10, 10)
    model = drawing.median_greedy_two_layered_bipartite_layout_2d(g, area)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    print(locations)

    assert locations == [
        (0.0, 0.0),
        (0.0, 5.0),
        (0.0, 10.0),
        (10.0, 0.0),
        (10.0, 5.0),
        (10.0, 10.0),
    ]