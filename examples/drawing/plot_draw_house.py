# -*- coding: utf-8 -*-

"""
Draw A House
=============================

Draw a graph with matplotlib. You must have matplotlib for this to work.
"""

# %%
# Start by importing the package

import jgrapht.drawing.draw_matplotlibimport draw
import matplotlib.pyplot as plt


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


# %%
# add edges

e1 = g.add_edge(0, 1)
e2 = g.add_edge(0, 2)
e3 = g.add_edge(1, 3)
e4 = g.add_edge(2, 3)
e5 = g.add_edge(2, 4)
e4 = g.add_edge(3, 4)

# %%
# Draw the nodes
pos = [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 2.0)]
draw.draw_nodes(g, position=pos, node_list=(0, 1, 2, 3), node_color="green")
draw.draw_nodes(g, position=pos, node_list=[4], node_color="red", node_shape="^")

# Draw the edges
draw.draw_edges(g, position=pos, edge_color="orange")
plt.tight_layout()
plt.show()
