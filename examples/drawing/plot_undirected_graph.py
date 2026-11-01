"""
An undirected graph
===================

Draw a graph, with and without labels, on the axes of your choice.
"""

import matplotlib.pyplot as plt

import jgrapht as jg
from jgrapht import drawing

g = jg.named_graph("frucht")
pos = jg.fruchterman_reingold_layout(g, seed=2)

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 5))
drawing.draw(g, pos, left)
drawing.draw(g, pos, right, labels=False, vertex_size=80, edge_width=2, edge_color="steelblue")
plt.show()
