"""
Edge colormap
=============

Color the edges by a number, here the edge weight, with a matplotlib colormap.
"""

import random

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.Graph(weighted=True)
rng = random.Random(5)
n = 12
for v in range(n):
    g.add_vertex(v)
for v in range(n):
    g.add_edge(v, (v + 1) % n, weight=rng.uniform(1, 10))
    g.add_edge(v, (v + 3) % n, weight=rng.uniform(1, 10))

pos = jg.circular_layout(g)
weights = [g.edge_weight(e) for e in g.edges()]

fig, ax = plt.subplots()
drawing.draw_edges(g, pos, ax, edge_color=weights, edge_cmap="plasma", edge_width=3)
drawing.draw_vertices(g, pos, ax, vertex_color="white", border_color="black")
drawing.draw_vertex_labels(g, pos, ax)
ax.margins(0.1)
ax.set_axis_off()
plt.show()
