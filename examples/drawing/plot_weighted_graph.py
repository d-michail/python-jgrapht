"""
A weighted graph
================

Write the weight on each edge, and show the shortest path.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.Graph(weighted=True)
for u, v, w in [(0, 1, 2.0), (0, 2, 6.0), (1, 2, 3.0), (1, 3, 7.0), (2, 3, 1.0), (3, 4, 2.0)]:
    for x in (u, v):
        g.add_vertex(x)
    g.add_edge(u, v, weight=w)

path = jg.shortest_path(g, 0, 4)
print(path)
on_path = set(path.edges)

pos = jg.circular_layout(g)
fig, ax = plt.subplots()
drawing.draw_edges(g, pos, ax, edge_color=lambda e: "crimson" if e in on_path else "gray", edge_width=2)
drawing.draw_vertices(g, pos, ax, vertex_color="white", border_color="black", vertex_size=450)
drawing.draw_vertex_labels(g, pos, ax)
drawing.draw_edge_labels(g, pos, ax)
ax.margins(0.1)
ax.set_axis_off()
plt.show()
