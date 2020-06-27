import pytest

from jgrapht import create_graph
import jgrapht.algorithms.drawing as drawing


def test_fr_layout():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
    )
    g.add_vertices_from(range(0, 5))
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(4, 2)
    g.add_edge(4, 3)

    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (6.404667487801095, 5.92187255236391),
        (3.8420346757193844, 4.882804644873968),
        (4.8938975276225305, 2.3242758825770364),
        (7.446344340409231, 3.388120451778693),
        (5.651036062420804, 4.13103626560845),
    ]


    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_layout_2d(g, area)
    assert model.area == area
    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]
    assert len(locations) == 5


def test_fr_layout_indexed():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
    )
    g.add_vertices_from(range(0, 5))
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(4, 2)
    g.add_edge(4, 3)

    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_indexed_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (4.725218032924005, 3.9732829503535427),
        (4.728709956380587, 3.9791561961012207),
        (4.723631541658893, 3.9780496186190404),
        (4.723099507642359, 3.9730366244091533),
        (4.7277641668738415, 3.974929737653007),
    ]


def test_anyhashableg_fr_layout():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    for i in range(0, 5):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "3")
    g.add_edge("3", "0")
    g.add_edge("4", "0")
    g.add_edge("4", "1")
    g.add_edge("4", "2")
    g.add_edge("4", "3")

    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (6.404667487801095, 5.92187255236391),
        (3.8420346757193844, 4.882804644873968),
        (4.8938975276225305, 2.3242758825770364),
        (7.446344340409231, 3.388120451778693),
        (5.651036062420804, 4.13103626560845),
    ]


def test_anyhashableg_fr_layout_indexed():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )
    g.add_vertices_from(range(0, 5))
    g.add_edge(0, 1, edge='0')
    g.add_edge(1, 2, edge='1')
    g.add_edge(2, 3, edge='2')
    g.add_edge(3, 0, edge='3')
    g.add_edge(4, 0, edge='4')
    g.add_edge(4, 1, edge='5')
    g.add_edge(4, 2, edge='6')
    g.add_edge(4, 3, edge='7')

    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_indexed_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]

    assert locations == [
        (4.725218032924005, 3.9732829503535427),
        (4.728709956380587, 3.9791561961012207),
        (4.723631541658893, 3.9780496186190404),
        (4.723099507642359, 3.9730366244091533),
        (4.7277641668738415, 3.974929737653007),
    ]


    area = (0, 0, 10, 10)
    model = drawing.fruchterman_reingold_indexed_layout_2d(g, area)
    assert model.area == area
    locations = [model.get_vertex_location(v) for v in g.vertices]
    locations = [(x, y) for x, y in locations]
    assert len(locations) == 5
