"""
Vertex colormap
===============

Color the vertices by a number, here the degree, with a matplotlib colormap.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.barabasi_albert_graph(3, 2, 40, seed=4)
pos = jg.fruchterman_reingold_layout(g, seed=1)

degrees = [g.degree_of(v) for v in g.vertices()]

fig, ax = plt.subplots()
drawing.draw_edges(g, pos, ax, edge_color="lightgray")
markers = drawing.draw_vertices(g, pos, ax, vertex_color=degrees, cmap="viridis", vertex_size=150)
fig.colorbar(markers, ax=ax, label="degree")
ax.set_axis_off()
plt.show()
