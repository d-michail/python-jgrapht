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

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)

    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    g.add_edge(2, 3)

    return g


def test_random_layout():
    g = build_graph()

    area = (0, 0, 10, 20)
    model = drawing.random_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]

    assert locations == [
        (7.323115139597316, 13.947409567214994),
        (0.8295611145017068, 16.324729022114614),
        (0.443859375038691, 4.794732258729857),
        (7.07454821689446, 13.189673845180147),
        (8.58996580616418, 0.0750948516482719),
        (4.416485026111072, 16.991675942396792),
    ]


    area = (0, 0, 10, 20)
    model = drawing.random_layout_2d(g, area)
    assert model.area == area
    locations = [model.get_vertex_location(v) for v in g.vertices]
    assert len(locations) == 6


def build_anyhashableg_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        any_hashable=True,
    )

    for i in range(0, 6):
        g.add_vertex(str(i))

    g.add_edge("0", "1")
    g.add_edge("0", "2")
    g.add_edge("1", "2")

    g.add_edge("3", "4")
    g.add_edge("3", "5")
    g.add_edge("4", "5")

    g.add_edge("2", "3")

    return g


def test_anyhashableg_random_layout():
    g = build_anyhashableg_graph()

    area = (0, 0, 10, 20)
    model = drawing.random_layout_2d(g, area, seed=17)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]

    assert locations == [
        (7.323115139597316, 13.947409567214994),
        (0.8295611145017068, 16.324729022114614),
        (0.443859375038691, 4.794732258729857),
        (7.07454821689446, 13.189673845180147),
        (8.58996580616418, 0.0750948516482719),
        (4.416485026111072, 16.991675942396792),
    ]

