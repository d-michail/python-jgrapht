import pytest

from jgrapht import create_graph
from jgrapht.io.importers import read_gexf, parse_gexf

input1=r"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft"
    version="1.2" 
    xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <graph defaultedgetype="undirected">
        <nodes>
            <node id="1" label="1"/>
            <node id="2" label="2"/>
            <node id="3" label="3"/>
        </nodes>
        <edges>
            <edge id="1" source="2" target="3" />
            <edge id="0" source="1" target="2" />
            <edge id="2" source="3" target="1" />
        </edges>
        </graph>
</gexf>
"""

def test_input_gexf(tmpdir):
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)
    parse_gexf(g, input1, validate_schema=True)
    
    assert len(g.vertices()) == 3
    assert len(g.edges()) == 3


def test_input_gexf_with_renumbering(tmpdir):
    g = create_graph(directed=False, allowing_self_loops=False, allowing_multiple_edges=False, weighted=True)

    def import_id(x): 
        return int(x)+5

    parse_gexf(g, input1, import_id_cb=import_id, validate_schema=True)
    
    assert len(g.vertices()) == 3
    assert len(g.edges()) == 3

    assert not g.contains_vertex(1)
    assert g.contains_vertex(6)
