"""
Draw a graph
============

Draw a small graph with :func:`jgrapht.drawing.draw`, which needs the vertex positions from a layout.
"""

# %%
# Build a graph. The famous graphs can be created by name.

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("petersen")

# %%
# A layout gives every vertex an ``(x, y)`` position. Here the vertices are placed by a
# force-directed layout; the seed makes the picture repeatable.

pos = jg.fruchterman_reingold_layout(g, seed=1)
drawing.draw(g, pos)
plt.show()

# %%
# Without labels and with another color and size, on a figure of your choice.

fig, ax = plt.subplots(figsize=(4, 4))
drawing.draw(g, pos, ax, labels=False, vertex_color="orange", vertex_size=150)
plt.show()
