"""
Colors and labels
=================

Color the vertices by the connected component they belong to, and write the weights on the edges.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.Graph(weighted=True)
for u, v, w in [("a", "b", 1.5), ("b", "c", 2.0), ("a", "c", 4.0), ("d", "e", 3.0)]:
    for x in (u, v):
        g.add_vertex(x)
    g.add_edge(u, v, weight=w)
g.add_vertex("f")

# %%
# Give each connected component its own color. A dictionary from vertex to color is enough.

palette = ["tomato", "mediumseagreen", "royalblue", "gold"]
color = {}
for i, component in enumerate(jg.connected_components(g)):
    for v in component:
        color[v] = palette[i]

pos = jg.circular_layout(g)
drawing.draw(g, pos, vertex_color=color, edge_labels=True)
plt.show()

# %%
# The parts can also be drawn one at a time, to style them separately. Here the shortest path
# between two vertices is highlighted.

path = jg.shortest_path(g, "a", "c")
on_path = set(path.edges)
fig, ax = plt.subplots()
drawing.draw_edges(
    g,
    pos,
    ax,
    edge_color=lambda e: "crimson" if e in on_path else "lightgray",
    edge_width=2.5,
)
drawing.draw_vertices(g, pos, ax, vertex_color=color)
drawing.draw_vertex_labels(g, pos, ax)
drawing.draw_edge_labels(g, pos, ax)
ax.set_axis_off()
plt.show()
