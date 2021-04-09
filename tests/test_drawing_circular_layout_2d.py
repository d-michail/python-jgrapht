import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import IntegerSupplier
import jgrapht.algorithms.drawing as drawing


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_circular_layout(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    g.add_vertices_from(range(0, 4))
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)

    area = (0, 0, 2, 2)
    model = drawing.circular_layout_2d(g, area, 1.0)

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]

    assert locations == [
        (2.0, 1.0),
        (1.0, 2.0),
        (0.0, 1.0000000000000002),
        (0.9999999999999998, 0.0),
    ]


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_circular_layout_with_comparator(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )
    g.add_vertices_from(range(0, 4))
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)

    def vertex_comparator(v1, v2):
        if v1 > v2:
            return -1
        if v1 < v2:
            return 1
        return 0

    area = (0, 0, 2, 2)
    model = drawing.circular_layout_2d(
        g, area, 1.0, vertex_comparator_cb=vertex_comparator
    )

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]

    assert locations == [
        (0.9999999999999998, 0.0),
        (0.0, 1.0000000000000002),
        (1.0, 2.0),
        (2.0, 1.0),
    ]


def test_anyhashableg_circular_layout_with_comparator():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=False,
        backend=GraphBackend.REF_GRAPH
    )
    
    for i in range(0, 4):
        g.add_vertex(str(i))
    g.add_edge("0", "1")
    g.add_edge("1", "2")
    g.add_edge("2", "3")
    g.add_edge("3", "0")

    def vertex_comparator(v1, v2):
        if int(v1) > int(v2):
            return -1
        if int(v1) < int(v2):
            return 1
        return 0

    area = (0, 0, 2, 2)
    model = drawing.circular_layout_2d(
        g, area, 1.0, vertex_comparator_cb=vertex_comparator
    )

    assert model.area == area

    locations = [model.get_vertex_location(v) for v in g.vertices]

    assert locations == [
        (0.9999999999999998, 0.0),
        (0.0, 1.0000000000000002),
        (1.0, 2.0),
        (2.0, 1.0),
    ]
