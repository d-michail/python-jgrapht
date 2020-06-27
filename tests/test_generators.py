import pytest

from jgrapht import create_graph
import jgrapht.generators as generators


def test_barabasi_albert():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.barabasi_albert(g, 10, 5, 100)
    assert len(g.vertices) == 100


def test_barabasi_albert_forest():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.barabasi_albert_forest(g, 10, 100)
    assert len(g.vertices) == 100


def test_complete():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.complete_graph(g, 10)
    assert len(g.vertices) == 10

def test_complete_property_graph():

    # Test that changes performed by the generators in the 
    # backend graph are propagated to the property graph.

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
    )

    generators.complete_graph(g, 10)
    assert len(g.vertices) == 10


def test_complete_bipartite():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.complete_bipartite_graph(g, 10, 10)
    assert len(g.vertices) == 20


def test_empty():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.empty_graph(g, 10)
    assert len(g.vertices) == 10


def test_gnm_random():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.gnm_random_graph(g, 10, 30)
    assert len(g.vertices) == 10


def test_gnp_random():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.gnp_random_graph(g, 10, 0.2)
    assert len(g.vertices) == 10


def test_ring():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.ring_graph(g, 10)
    assert len(g.vertices) == 10


def test_scalefree():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.scalefree_graph(g, 10)
    assert len(g.vertices) == 10


def test_watts_strogatz():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.watts_strogatz_graph(g, 10, 2, 0.1)
    assert len(g.vertices) == 10


def test_kleinberg_smallworld():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.kleinberg_smallworld_graph(g, 10, 2, 2, 1)
    assert len(g.vertices) == 100


def test_complement():
    g_source = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    g_source.add_vertex(0)
    g_source.add_vertex(1)
    g_source.add_vertex(2)
    g_source.add_edge(0, 1)
    g_source.add_edge(0, 2)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    generators.complement_graph(g, g_source)

    assert g.vertices == {0, 1, 2}
    assert g.edges == {0}
    assert g.edge_tuple(0) == (1, 2, 1.0)


def test_generalized_petersen():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.generalized_petersen(g, 10, 4)
    assert len(g.vertices) == 20


def test_grid():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.grid(g, 10, 4)
    assert len(g.vertices) == 40


def test_hypercube():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.hypercube(g, 4)
    assert len(g.vertices) == 16


def test_linear():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.linear(g, 10)
    assert len(g.vertices) == 10


def test_random_regular():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.random_regular(g, 10, 3, 17)
    assert len(g.vertices) == 10


def test_random_regular_no_seed():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.random_regular(g, 10, 3)
    assert len(g.vertices) == 10


def test_star():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.star(g, 10)
    assert len(g.vertices) == 10


def test_wheel():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.wheel(g, 10, False)
    assert len(g.vertices) == 10


def test_windmill():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    generators.windmill(g, 3, 3, dutch=False)
    assert len(g.vertices) == 7


def test_linearized_chord_diagram():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )
    generators.linearized_chord_diagram(g, 100, 3, 17)
    assert len(g.vertices) == 100

    # test that error is raised if the graph does not support self loops and multiple edges
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    with pytest.raises(ValueError):
        generators.linearized_chord_diagram(g, 100, 3, 17)


def test_linearized_chord_diagram_no_seed():
    g = create_graph(
        directed=False,
        allowing_self_loops=True,
        allowing_multiple_edges=True,
        weighted=True,
    )
    generators.linearized_chord_diagram(g, 100, 3)
    assert len(g.vertices) == 100
