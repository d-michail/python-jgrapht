import pytest

from jgrapht import create_graph
import jgrapht.properties as properties


def test_is_empty_graph():
    g = create_graph()
    assert properties.is_empty_graph(g)


def test_is_simple():
    g = create_graph(allowing_multiple_edges=True, allowing_self_loops=True)

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_simple(g)

    g.add_edge(1, 1)

    assert not properties.is_simple(g)


def test_has_self_loops():
    g = create_graph(allowing_multiple_edges=True, allowing_self_loops=True)

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.has_selfloops(g)

    g.add_edge(1, 1)

    assert properties.has_selfloops(g)


def test_has_multiple_edges():
    g = create_graph(allowing_multiple_edges=True, allowing_self_loops=True)

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.has_multipleedges(g)

    g.add_edge(1, 1)

    assert not properties.has_multipleedges(g)

    g.add_edge(1, 2)

    assert properties.has_multipleedges(g)


def test_is_complete():
    g = create_graph(
        directed=True, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)
    g.add_edge(2, 1)

    assert properties.is_complete(g)

    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_complete(g)


def test_is_weakly_connected():
    g = create_graph(
        directed=True, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_weakly_connected(g)

    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_weakly_connected(g)


def test_is_strongly_connected():
    g = create_graph(
        directed=True, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert not properties.is_strongly_connected(g)

    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_edge(1, 2)

    assert properties.is_strongly_connected(g)


def test_is_tree():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_tree(g)

    g.add_edge(3, 1)

    assert not properties.is_tree(g)


def test_is_forest():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_forest(g)

    g.add_edge(3, 1)

    assert not properties.is_forest(g)


def test_is_overfull():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert not properties.is_overfull(g)


def test_is_split():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    assert properties.is_split(g)


def test_is_bipartite():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)

    assert properties.is_bipartite(g)

    g.add_edge(3, 1)

    assert not properties.is_bipartite(g)


def test_is_cubic():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_cubic(g)


def test_is_eulerian():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_eulerian(g)


def test_is_chordal():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_chordal(g)


def test_is_weakly_chordal():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_weakly_chordal(g)


def test_is_triangle_free():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_trianglefree(g)


def test_is_perfect():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_perfect(g)


def test_is_planar():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert properties.is_planar(g)


def test_has_ore():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.has_ore(g)


def test_is_kuratowski_subdivision():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_kuratowski_subdivision(g)


def test_is_k33_subdivision():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_k33_subdivision(g)


def test_is_k5_subdivision():
    g = create_graph(
        directed=False, allowing_multiple_edges=True, allowing_self_loops=True
    )

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    g.add_edge(3, 1)

    assert not properties.is_k5_subdivision(g)
