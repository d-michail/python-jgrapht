# -*- coding: utf-8 -*-

"""
Labels And Colors
=============================

Draw a graph with matplotlib, color by degree. You must have matplotlib  for this to work.
"""

# %%
# Start by importing the package

import jgrapht
import draw
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
# Draw the nodes
pos = draw.layout(g, pos_layout="fruchterman_reingold_indexed_layout")
draw.draw_nodes(g, position=pos, node_list=(0, 1, 2, 3, 4), node_title="green nodes")
draw.draw_nodes(
    g, position=pos, node_list=(5, 6, 7, 8, 9), node_color="red", node_title="red nodes"
)

# Draw the edges
draw.draw_edges(
    g,
    position=pos,
    edge_list=(0, 1, 2, 3, 4),
    edge_color="orange",
    edge_title="orange edges",
)
draw.draw_edges(
    g,
    position=pos,
    edge_list=(5, 6, 7, 8, 9),
    edge_color="blue",
    edge_title="blue edges",
)

# Draw the labels
draw.draw_labels(
    g, position=pos, node_names=("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
)
draw.draw_edge_labels(
    g, position=pos, edge_names=("a", "b", "c", "d", "e", "f", "g", "h", "i")
)

plt.show()
