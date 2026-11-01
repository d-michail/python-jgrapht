"""
GraphML import
==============

Read a graph from a GraphML document, with its edge weights and its attributes.
"""

import jgrapht as jg

graphml = """\
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="color" for="node" attr.name="color" attr.type="string"/>
  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>
  <graph id="G" edgedefault="undirected">
    <node id="a"><data key="color">red</data></node>
    <node id="b"><data key="color">green</data></node>
    <node id="c"><data key="color">green</data></node>
    <edge source="a" target="b"><data key="weight">1.5</data></edge>
    <edge source="b" target="c"><data key="weight">2.5</data></edge>
  </graph>
</graphml>
"""

# %%
# The vertices are the identifiers in the file, and ``weighted=True`` reads the edge weights.

g = jg.parse_graph(graphml, "graphml", weighted=True)
print(g.vertices(), [g.edge_weight(e) for e in g.edges()])

# %%
# The attributes of the file are stored in the graph. ``vertex_attrs`` and ``edge_attrs`` map a vertex
# or an edge to its attribute dict, and ``graph_attrs`` holds the attributes of the graph itself.

print(g.vertex_attrs["a"])
print(g.edge_attrs.items())

# %%
# They are ordinary dicts, so you can change them, and an exporter writes what is stored.

g.vertex_attrs["a"]["color"] = "blue"
print(jg.graph_to_string(g, "json", vertex_id=str))
