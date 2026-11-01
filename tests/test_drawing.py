import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import jgrapht as jg  # noqa: E402
from jgrapht import drawing  # noqa: E402


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


def weighted_digraph():
    g = jg.Graph(directed=True, weighted=True, allow_self_loops=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", edge="ab", weight=1.5)
    g.add_edge("b", "a", edge="ba", weight=2.0)
    g.add_edge("b", "c", edge="bc", weight=3.0)
    g.add_edge("c", "c", edge="cc", weight=1.0)
    return g


def test_draw_vertices_places_one_marker_per_vertex(ax):
    g = jg.path_graph(4)
    pos = jg.circular_layout(g)
    markers = drawing.draw_vertices(g, pos, ax)
    assert len(markers.get_offsets()) == 4
    drawing.draw_vertices(g, pos, ax, vertices=[0, 1])
    assert len(ax.collections[-1].get_offsets()) == 2


def test_draw_vertices_colors(ax):
    g = jg.path_graph(3)
    pos = jg.circular_layout(g)
    drawing.draw_vertices(g, pos, ax, vertex_color={0: "red", 1: "green", 2: "blue"})
    drawing.draw_vertices(g, pos, ax, vertex_color=lambda v: "red" if v else "blue")
    drawing.draw_vertices(g, pos, ax, vertex_color=[0.0, 0.5, 1.0], cmap="viridis")


def test_draw_edges_undirected_and_directed(ax):
    g = jg.path_graph(4)
    artists = drawing.draw_edges(g, jg.circular_layout(g), ax)
    assert len(artists) == 1 and len(artists[0].get_segments()) == 3
    d = weighted_digraph()
    artists = drawing.draw_edges(d, jg.circular_layout(d), ax)
    # three arrows (one pair is curved) and a ring for the self-loop
    assert sum(type(a).__name__ == "FancyArrowPatch" for a in artists) == 3
    assert len(artists) == 4


def test_draw_edges_colors_and_subsets(ax):
    g = jg.path_graph(3)
    pos = jg.circular_layout(g)
    drawing.draw_edges(g, pos, ax, edge_color={0: "red"}, edge_style="dashed")
    assert len(drawing.draw_edges(g, pos, ax, edges=[1])[0].get_segments()) == 1
    assert drawing.draw_edges(jg.empty_graph(3), None, ax) == []


def test_labels(ax):
    d = weighted_digraph()
    pos = jg.circular_layout(d)
    texts = drawing.draw_vertex_labels(d, pos, ax)
    assert {v: t.get_text() for v, t in texts.items()} == {v: v for v in "abcd"}
    texts = drawing.draw_vertex_labels(d, pos, ax, labels={"a": "first"})
    assert list(texts) == ["a"] and texts["a"].get_text() == "first"
    texts = drawing.draw_edge_labels(d, pos, ax)
    assert texts["ab"].get_text() == "1.5"
    texts = drawing.draw_edge_labels(d, pos, ax, labels=lambda e: e.upper())
    assert texts["bc"].get_text() == "BC"
    plain = jg.path_graph(3)
    assert drawing.draw_edge_labels(plain, None, ax)[0].get_text() == "0"


def test_draw_all_graph_kinds(ax):
    returned = drawing.draw(weighted_digraph(), ax=ax, edge_labels=True, vertex_color="orange")
    assert returned is ax
    for g in (
        jg.SparseGraph(4, [(0, 1), (1, 2)]),
        jg.SparseGraph(3, [(0, 1)], directed=True),
        jg.as_unmodifiable(jg.path_graph(3)),
        jg.complete_graph(4),
    ):
        fig, other = plt.subplots()
        drawing.draw(g, jg.circular_layout(g), other, labels=False)
        plt.close(fig)


def test_default_positions_are_deterministic(ax):
    g = jg.complete_graph(4)
    first = drawing.draw_vertices(g, None, ax).get_offsets().copy()
    second = drawing.draw_vertices(g, None, ax).get_offsets().copy()
    assert (first == second).all()


def test_missing_position_is_an_error(ax):
    g = jg.path_graph(3)
    with pytest.raises(ValueError):
        drawing.draw(g, {0: (0, 0), 1: (1, 1)}, ax)


def test_uses_current_axes_by_default():
    fig, current = plt.subplots()
    assert drawing.draw(jg.path_graph(3)) is current
    plt.close(fig)
