"""
A directed graph
================

Edges of a directed graph are drawn as arrows. Edges in both directions are drawn as two curves, and
a self-loop as a ring.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.Graph(directed=True, allow_self_loops=True)
for v in range(5):
    g.add_vertex(v)
for u, v in [(0, 1), (1, 0), (1, 2), (2, 3), (3, 1), (3, 4), (4, 4)]:
    g.add_edge(u, v)

pos = jg.circular_layout(g)
drawing.draw(g, pos, vertex_color="lightsteelblue", arrows=True)
plt.show()

# %%
# The strongly connected components, one color each.

colors = {}
for color, component in zip(["tomato", "seagreen", "royalblue", "gold"], jg.strongly_connected_components(g)):
    for v in component:
        colors[v] = color
drawing.draw(g, pos, vertex_color=colors)
plt.show()
