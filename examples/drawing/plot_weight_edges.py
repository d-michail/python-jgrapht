# -*- coding: utf-8 -*-

"""
Weighted Graph
=============================

An example using Graph as a weighted . You must have matplotlib  for this to work.
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
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()
g.add_vertex()


# %%
# add edges

e1 = g.add_edge(0, 1, weight=0.5)
e2 = g.add_edge(0, 2, weight=0.4)
e3 = g.add_edge(0, 3, weight=0.6)
e4 = g.add_edge(0, 4, weight=0.8)
e5 = g.add_edge(0, 5, weight=0.1)
e6 = g.add_edge(0, 6, weight=1)
e7 = g.add_edge(0, 7, weight=0.9)
e8 = g.add_edge(0, 8, weight=0.2)
e9 = g.add_edge(0, 9, weight=0.7)

# %%
# create list of edges depending on their weights
weight_large = [e for e in g.edges if g.get_edge_weight(e) > 0.5]
weight_small = [e for e in g.edges if g.get_edge_weight(e) <= 0.5]


# %%
# Draw the nodes
pos = draw.layout(g, pos_layout="fruchterman_reingold_indexed_layout")
draw.draw_nodes(g, position=pos)

# Draw the edges
draw.draw_edges(
    g,
    position=pos,
    edge_list=weight_large,
    edge_color="red",
    edge_title="weight>0.5",
    line_style="dashed",
)
draw.draw_edges(
    g,
    position=pos,
    edge_list=weight_small,
    edge_color="orange",
    edge_title="weight<=0.5",
)

# Draw the labels
draw.draw_labels(g, position=pos)
draw.draw_edge_labels(g, position=pos, draw_edge_weights=True)

plt.show()
