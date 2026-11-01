"""
A house
=======

Place the vertices by hand: the positions are just a dictionary from vertex to ``(x, y)``.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.Graph()
for v in range(5):
    g.add_vertex(v)
for u, v in [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4)]:
    g.add_edge(u, v)

pos = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (0.5, 1.6)}

# %%
# The square is drawn in blue and the roof in red, by drawing the two sets of edges separately.

fig, ax = plt.subplots(figsize=(4, 4))
drawing.draw_edges(g, pos, ax, edges=[0, 1, 2, 3], edge_color="royalblue", edge_width=3)
drawing.draw_edges(g, pos, ax, edges=[4, 5], edge_color="tomato", edge_width=3)
drawing.draw_vertices(g, pos, ax, vertex_color="gold", border_color="black", vertex_size=500)
drawing.draw_vertex_labels(g, pos, ax)
ax.margins(0.15)
ax.set_axis_off()
plt.show()
