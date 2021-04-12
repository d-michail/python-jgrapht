import pytest

from jgrapht import create_graph, GraphBackend
from jgrapht.utils import create_vertex_supplier, create_edge_supplier, IntegerSupplier

from jgrapht.io.exporters import (
    write_sparse6,
    write_graph6,
    generate_sparse6,
    generate_graph6,
)
from jgrapht.io.importers import read_graph6sparse6, parse_graph6sparse6


def build_graph(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(1, 3)

    return g


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_output_sparse6(tmpdir, backend):

    g = build_graph(backend)
    tmpfile = tmpdir.join("graph.s6")
    tmpfilename = str(tmpfile)

    write_sparse6(g, tmpfilename)

    # read back

    def va_cb(vertex, attribute_name, attribute_value):
        assert attribute_name == "ID"
        assert str(vertex) == attribute_value

    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )
    read_graph6sparse6(g1, tmpfilename, vertex_attribute_cb=va_cb)

    assert len(g1.vertices) == 4
    assert len(g1.edges) == 5


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_output_graph6(tmpdir, backend):
    g = build_graph(backend)
    tmpfile = tmpdir.join("graph.g6")
    tmpfilename = str(tmpfile)

    write_graph6(g, tmpfilename)

    # read back

    def va_cb(vertex, attribute_name, attribute_value):
        assert attribute_name == "ID"
        assert str(vertex) == attribute_value

    g1 = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )
    read_graph6sparse6(g1, tmpfilename, vertex_attribute_cb=va_cb)

    assert len(g1.vertices) == 4
    assert len(g1.edges) == 5


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_output_to_string(backend):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=True,
        weighted=False,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),
    )

    g.add_vertices_from(range(0, 4))

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(2, 3)

    out = generate_sparse6(g)
    assert out == ":Cca"

    out = generate_graph6(g)
    assert out == "Ct"


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_read_sparse6_property_graph_from_string(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    def import_id_cb(id):
        return "vv{}".format(id)

    parse_graph6sparse6(g, ":Cca", import_id_cb=import_id_cb)

    assert g.vertices == {"vv0", "vv1", "vv2", "vv3"}
    assert g.edge_tuple("e0") == ("vv0", "vv1", 1.0)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_read_sparse6_property_graph_from_string1(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=create_vertex_supplier(),
        edge_supplier=create_edge_supplier(),
    )

    parse_graph6sparse6(g, ":Cca")

    assert g.vertices == {"v0", "v1", "v2", "v3"}
    assert g.edge_tuple("e0") == ("v0", "v1", 1.0)



@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
        GraphBackend.INT_GRAPH,
        GraphBackend.LONG_GRAPH,
    ],
)
def test_read_sparse6_graph_from_string(backend):

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        edge_supplier=IntegerSupplier(),
        vertex_supplier=IntegerSupplier(),        
    )

    def import_id_cb(id):
        return int(id)

    parse_graph6sparse6(g, ":Cca", import_id_cb=import_id_cb)

    assert g.vertices == {0, 1, 2, 3}
    assert g.edge_tuple(0) == (0, 1, 1.0)


@pytest.mark.parametrize(
    "backend",
    [
        GraphBackend.REF_GRAPH,
    ],
)
def test_read_anyhashableg_sparse6_graph_from_file(tmpdir, backend):
    tmpfile = tmpdir.join("gml.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(":Cca")

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        backend=backend,
        vertex_supplier=create_vertex_supplier(type="int"),
        edge_supplier=create_edge_supplier(type="int"),
    )

    def import_id_cb(id):
        return int(id)

    read_graph6sparse6(g, tmpfilename, import_id_cb=import_id_cb)

    assert g.vertices == {0, 1, 2, 3}
    assert g.edge_tuple(0) == (0, 1, 1.0)
