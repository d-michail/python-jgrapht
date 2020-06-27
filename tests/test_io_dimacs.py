import pytest

from jgrapht import create_graph
from jgrapht.utils import create_vertex_supplier, create_edge_supplier

from jgrapht.io.exporters import write_dimacs, generate_dimacs
from jgrapht.io.importers import read_dimacs, parse_dimacs


def build_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(0, 6)
    g.add_edge(0, 7)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


def build_property_graph():
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        edge_supplier=create_edge_supplier(type='int')
    )

    for i in range(1, 11):
        g.add_vertex(i)

    g.add_edge(10, 1)
    g.add_edge(10, 2)
    g.add_edge(10, 3)
    g.add_edge(10, 4)
    g.add_edge(10, 5)
    g.add_edge(10, 6)
    g.add_edge(10, 7)
    g.add_edge(10, 8)
    g.add_edge(10, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    return g


dimacs_sp_expected = """c
c SOURCE: Generated using the JGraphT library
c
p sp 10 18
a 1 2
a 1 3
a 1 4
a 1 5
a 1 6
a 1 7
a 1 8
a 1 9
a 1 10
a 2 3
a 3 4
a 4 5
a 5 6
a 6 7
a 7 8
a 8 9
a 9 10
a 10 2
"""

dimacs_coloring_expected = """c
c SOURCE: Generated using the JGraphT library
c
p col 10 18
e 1 2
e 1 3
e 1 4
e 1 5
e 1 6
e 1 7
e 1 8
e 1 9
e 1 10
e 2 3
e 3 4
e 4 5
e 5 6
e 6 7
e 7 8
e 8 9
e 9 10
e 10 2
"""

dimacs_maxclique_expected = """c
c SOURCE: Generated using the JGraphT library
c
p edge 10 18
e 1 2
e 1 3
e 1 4
e 1 5
e 1 6
e 1 7
e 1 8
e 1 9
e 1 10
e 2 3
e 3 4
e 4 5
e 5 6
e 6 7
e 7 8
e 8 9
e 9 10
e 10 2
"""


dimacs_sp_expected2 = """c
c SOURCE: Generated using the JGraphT library
c
p sp 10 18
a 10 1
a 10 2
a 10 3
a 10 4
a 10 5
a 10 6
a 10 7
a 10 8
a 10 9
a 1 2
a 2 3
a 3 4
a 4 5
a 5 6
a 6 7
a 7 8
a 8 9
a 9 1
"""


dimacs_sp_expected100 = """c
c SOURCE: Generated using the JGraphT library
c
p sp 10 18
a 100 101
a 100 102
a 100 103
a 100 104
a 100 105
a 100 106
a 100 107
a 100 108
a 100 109
a 101 102
a 102 103
a 103 104
a 104 105
a 105 106
a 106 107
a 107 108
a 108 109
a 109 101
"""

def test_dimacs(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format="shortestpath")

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_sp_expected


def test_dimacs_with_custom_ids(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    def custom_id(id):
        return id+100

    write_dimacs(g, tmpfilename, format="shortestpath", export_vertex_id_cb=custom_id)

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_sp_expected100


def test_dimacs_with_custom_ids_bad_function(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    def custom_id(id):
        return str(id+100)

    with pytest.raises(TypeError):
        write_dimacs(g, tmpfilename, format="shortestpath", export_vertex_id_cb=custom_id)

    def custom_id2(id):
        return -id

    with pytest.raises(ValueError):
        write_dimacs(g, tmpfilename, format="shortestpath", export_vertex_id_cb=custom_id2)


def test_dimacs_coloring(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format="coloring")

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_coloring_expected


def test_dimacs_maxclique(tmpdir):
    g = build_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format="maxclique")

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_maxclique_expected


def test_dimacs_output_to_string():
    g = build_graph()

    out = generate_dimacs(g)

    assert out.splitlines() == dimacs_maxclique_expected.splitlines()


def test_read_dimacs_from_string(tmpdir):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def identity(x):
        return x

    parse_dimacs(g, dimacs_sp_expected, identity)

    assert g.vertices == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    again = generate_dimacs(g, format="shortestpath")
    assert again.splitlines() == dimacs_sp_expected.splitlines()


def test_read_dimacs_from_file(tmpdir):
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(dimacs_sp_expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
    )

    def identity(x):
        return x

    read_dimacs(g, tmpfilename, identity)

    assert g.vertices == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    again = generate_dimacs(g, format="shortestpath")
    assert again.splitlines() == dimacs_sp_expected.splitlines()


def test_read_dimacs_property_graph_from_file(tmpdir):
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)

    # write file json with escaped characters
    with open(tmpfilename, "w") as f:
        f.write(dimacs_sp_expected)

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    read_dimacs(g, tmpfilename)

    assert g.vertices == {'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9'}
    assert g.edge_tuple('e6') == ('v0', 'v7', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}


def test_read_dimacs_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    parse_dimacs(g, dimacs_sp_expected)

    assert g.vertices == {'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9'}
    assert g.edge_tuple('e6') == ('v0', 'v7', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}


def test_read_dimacs_property_graph_from_string():

    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        vertex_supplier=create_vertex_supplier(), 
        edge_supplier=create_edge_supplier()
    )

    def import_id_cb(id):
        return 'v{}'.format(id+1)

    parse_dimacs(g, dimacs_sp_expected, import_id_cb=import_id_cb)

    assert g.vertices == {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10'}
    assert g.edge_tuple('e6') == ('v1', 'v8', 1.0)
    assert g.vertex_attrs == {}
    assert g.edge_attrs == {}


def test_anyhashableg_dimacs(tmpdir):
    g = build_property_graph()
    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format="shortestpath")

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_sp_expected2


def test_anyhashableg_dimacs_increase_to_positive_id(tmpdir):
    g = create_graph(
        directed=False,
        allowing_self_loops=False,
        allowing_multiple_edges=False,
        weighted=True,
        any_hashable=True,
        edge_supplier=create_edge_supplier(type='int')
    )

    for i in range(0, 10):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(0, 5)
    g.add_edge(0, 6)
    g.add_edge(0, 7)
    g.add_edge(0, 8)
    g.add_edge(0, 9)

    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 1)

    def increase_vid(id):
        return id+1

    tmpfile = tmpdir.join("dimacs.out")
    tmpfilename = str(tmpfile)
    write_dimacs(g, tmpfilename, format="shortestpath", export_vertex_id_cb=increase_vid)

    with open(tmpfilename, "r") as f:
        contents = f.read()
        print(contents)

    assert contents == dimacs_sp_expected


def test_dimacs_output_to_string():
    g = build_graph()

    def custom_id(id):
        return id+1

    out = generate_dimacs(g, export_vertex_id_cb=custom_id)

    assert out.splitlines() == dimacs_maxclique_expected.splitlines()

    def custom_id_bad1(id):
        return str(id+1)

    with pytest.raises(TypeError):
        generate_dimacs(g, export_vertex_id_cb=custom_id_bad1)

    def custom_id_bad2(id):
        return -id

    with pytest.raises(ValueError):
        generate_dimacs(g, export_vertex_id_cb=custom_id_bad2)

