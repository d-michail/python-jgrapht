"""
Minimum spanning tree
=====================

Connect all the vertices of a weighted graph as cheaply as possible, using Prim's algorithm.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

# %%
# A network of towns and the cost of laying a cable between them.

g = jg.Graph(weighted=True)
links = [
    ("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7),
    ("C", "E", 5), ("D", "E", 15), ("D", "F", 6), ("E", "F", 8), ("E", "G", 9), ("F", "G", 11),
]
for u, v, cost in links:
    for x in (u, v):
        g.add_vertex(x)
    g.add_edge(u, v, edge=f"{u}{v}", weight=float(cost))

# %%
# The result is the total weight and the edges of the tree. Kruskal's and Boruvka's algorithms
# are available as ``"kruskal"`` and ``"boruvka"``.

total, tree = jg.minimum_spanning_tree(g, "prim")
print(total, sorted(tree))

# %%
# Draw the graph with the tree edges highlighted.

pos = jg.circular_layout(g)
fig, ax = plt.subplots()
drawing.draw_edges(
    g,
    pos,
    ax,
    edge_color=lambda e: "seagreen" if e in set(tree) else "lightgray",
    edge_width=3,
)
drawing.draw_vertices(g, pos, ax, vertex_color="white", border_color="black", vertex_size=500)
drawing.draw_vertex_labels(g, pos, ax)
drawing.draw_edge_labels(g, pos, ax)
ax.margins(0.1)
ax.set_axis_off()
plt.show()
