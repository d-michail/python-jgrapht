"""
Writing and reading a graph
===========================

Round trip a graph with attributes through several formats.
"""

# %%
# A small weighted graph with named vertices.

import jgrapht as jg

g = jg.Graph(weighted=True)
for v in ["a", "b", "c"]:
    g.add_vertex(v)
g.add_edge("a", "b", weight=1.5)
g.add_edge("b", "c", weight=2.5)

# %%
# Write it as GraphML, keeping the vertex names, the weights and a colour attribute.

text = jg.graph_to_string(
    g,
    "graphml",
    vertex_id=str,
    edge_weights=True,
    vertex_attributes={"a": {"colour": "red"}, "b": {"colour": "blue"}},
)
print(text)

# %%
# Read it back. ``weighted=True`` keeps the weights. The attributes found in the document are stored
# in the graph, in ``vertex_attrs``, ``edge_attrs`` and ``graph_attrs``.

h = jg.parse_graph(text, "graphml", weighted=True)
print(h)
print(h.vertex_attrs["a"])

# %%
# Other formats work the same way.

for fmt in ["gml", "json", "dot", "gexf"]:
    copy = jg.parse_graph(jg.graph_to_string(g, fmt, **({"vertex_id": str} if fmt in ("json", "dot") else {})), fmt)
    print(fmt, copy.edge_count())
