# -*- coding: utf-8 -*-

"""
Draw A Simple Graph
===================

In this example we draw a graph using the Fruchterman-Reingold layout.You must have matplotlib installed for this to work.
"""

# %%
# Start by importing the package

import jgrapht
import jgrapht.drawing.draw_matplotlib as drawing
import matplotlib.pyplot as plt

# %%
# Creating a graph

g = jgrapht.create_graph(directed=False, weighted=True)

# %%
# Add some vertices

for i in range(0,10):
    g.add_vertex()

# %%
# and some edges

e1 = g.add_edge(0, 1)
e2 = g.add_edge(0, 2)
e3 = g.add_edge(0, 3)
e4 = g.add_edge(0, 4)
e5 = g.add_edge(0, 5)
e6 = g.add_edge(0, 6)
e7 = g.add_edge(0, 7)
e8 = g.add_edge(0, 8)
e9 = g.add_edge(0, 9)
e10 = g.add_edge(1, 2)

# %%
# Compute the position of the vertices
pos = drawing.layout(g, seed=10,pos_layout="fruchterman_reingold_layout")

# %%
# Draw the graph using the node labels and the edge labels
drawing.draw_jgrapht(g, position=pos, edge_label=True,axis=False)
plt.show()
