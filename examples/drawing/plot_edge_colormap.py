# -*- coding: utf-8 -*-

"""
Edge Colormap
=============================

Draw a graph with matplotlib, color by degree. You must have matplotlib and numpy for this to work.
"""

# %%
# Start by importing the package

import jgrapht.drawing.draw_matplotlibimport draw
import matplotlib.pyplot as plt
import numpy as np


# %%
# Creating a graph

g = jgrapht.create_graph(directed=False, weighted=True,)


# %%
# add vertex

g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()


# %%
# add edges

e1 = g.add_edge(0, 1)
e2 = g.add_edge(0, 2)
e3 = g.add_edge(0, 3)
e4 = g.add_edge(0, 4)
e5 = g.add_edge(0, 5)
e6 = g.add_edge(0, 6)
e7 = g.add_edge(0, 7)
e8 = g.add_edge(0, 8)
e9 = g.add_edge(0, 9)

# %%
# Draw the graph
pos = draw.layout(g, pos_layout="circular_layout")
draw.draw_jgrapht(
    g,
    position=pos,
    node_label=True,
    edge_linewidth=6,
    edge_cmap=plt.cm.Blues(np.linspace(0, 1, len(g.edges))),
)
plt.show()
