"""
Connected components
====================

Find the components of an undirected graph, and the strongly connected components of a directed one.
"""

# %%
# A graph with three components: a triangle, a path and an isolated vertex.

import jgrapht as jg

g = jg.Graph()
for v in range(8):
    g.add_vertex(v)
for u, v in [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5)]:
    g.add_edge(u, v)

print(jg.connected_components(g))
print(jg.is_connected(g))

# %%
# Articulation points and bridges tell where the graph is fragile.

print(jg.articulation_points(g))
print(jg.bridges(g))

# %%
# For a directed graph the strongly connected components are the maximal sets of mutually
# reachable vertices. The condensation collapses each component to a vertex.

d = jg.Graph(directed=True)
for v in range(5):
    d.add_vertex(v)
for u, v in [(0, 1), (1, 0), (1, 2), (2, 3), (3, 2), (3, 4)]:
    d.add_edge(u, v)

print(jg.strongly_connected_components(d))
