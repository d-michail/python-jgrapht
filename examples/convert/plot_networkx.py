"""
NetworkX
========

Convert a graph to NetworkX and back. NetworkX is an optional dependency.
"""

import networkx as nx

import jgrapht as jg
from jgrapht.convert import from_nx, to_nx

# %%
# Start from a NetworkX graph and convert it. The nodes become the vertices of the new graph, and
# weights are kept.

n = nx.Graph(name="roads")
n.add_node("Athens", population=3_150_000)
n.add_edge("Athens", "Patras", weight=215.0)
n.add_edge("Athens", "Larissa", weight=350.0)
n.add_edge("Larissa", "Volos", weight=60.0)
n.add_edge("Patras", "Volos", weight=450.0)

g = from_nx(n)
print(g)

# %%
# The attributes of the nodes, of the edges and of the graph are copied to ``vertex_attrs``,
# ``edge_attrs`` and ``graph_attrs``. The edge weight is not an attribute.

print(g.vertex_attrs["Athens"], g.graph_attrs)

# %%
# Run an algorithm of this package on it.

path = jg.shortest_path(g, "Athens", "Volos")
print(path.vertices, path.weight)

# %%
# Convert the graph back, for example to use a NetworkX algorithm or to draw it.

back = to_nx(g)
print(sorted(back.edges(data="weight")))
print(nx.shortest_path(back, "Athens", "Volos", weight="weight"))
