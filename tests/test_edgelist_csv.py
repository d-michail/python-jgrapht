import pytest

from jgrapht import create_graph
from jgrapht.io.edgelist import read_edgelist_csv, parse_edgelist_csv


def test_input_csv_from_string():

    input_string = """1,2
2,3
3,4
4,1
"""

    edgelist = parse_edgelist_csv(input_string)

    assert list(edgelist) == [('1', '2', 1.0), ('2', '3', 1.0), ('3', '4', 1.0), ('4', '1', 1.0)]


def test_input_csv_from_string_with_weights():

    input_string = """1,2,4.0
2,3,5.5
3,4,2.2
4,1,1.3
"""

    edgelist = parse_edgelist_csv(input_string, import_edge_weights=True)

    assert list(edgelist) == [('1', '2', 4.0), ('2', '3', 5.5), ('3', '4', 2.2), ('4', '1', 1.3)]


def test_input_csv_from_file(tmpdir):

    input_string = """1,2
2,3
3,4
4,1
"""

    tmpfile = tmpdir.join("csv.out")
    tmpfilename = str(tmpfile)

    with open(tmpfilename, "w") as f:
        f.write(input_string)

    edgelist = read_edgelist_csv(tmpfilename)

    assert list(edgelist) == [('1', '2', 1.0), ('2', '3', 1.0), ('3', '4', 1.0), ('4', '1', 1.0)]
