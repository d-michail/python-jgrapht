"""
JSON export
===========

Write a graph as JSON.
"""

import jgrapht as jg

g = jg.Graph(weighted=True)
for city in ["Athens", "Patras", "Volos"]:
    g.add_vertex(city)
g.add_edge("Athens", "Patras", weight=215.0)
g.add_edge("Athens", "Volos", weight=330.0)

# %%
# The vertices need identifiers, which are strings. Here the vertex names themselves are used.

text = jg.graph_to_string(g, "json", vertex_id=str, edge_weights=True)
print(text)

# %%
# Reading it back gives an equivalent graph.

h = jg.parse_graph(text, "json", weighted=True)
print(h.vertices(), [h.edge_weight(e) for e in h.edges()])

# %%
# Use :func:`~jgrapht.write_graph` to write to a file instead of a string.
