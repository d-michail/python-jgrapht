# -*- coding: utf-8 -*-

"""
Draw a Directed Graph
=====================

In this example we draw a directed graph using the Fruchterman-Reingold layout.
You must have matplotlib installed for this to work.
"""

# %%
# Start by importing the package
import jgrapht
import jgrapht.drawing.draw_matplotlib as drawing
import matplotlib.pyplot as plt

# %%
# Creating a graph

g = jgrapht.create_graph(directed=True, weighted=True)

# %%
# Add some vertices

for i in range(0, 10):
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

# %%
# Compute the position of the vertices
positions = drawing.layout(g, seed=10, name="circular")

# %%
# Draw the graph using the node labels,arrows,node colormap,arrow line,arrow color,connection style and edge line width
drawing.draw_jgrapht(
    g,
    positions=positions,
    node_label=True,
    node_color=range(len(g.vertices)),
    node_cmap=plt.cm.Blues,
    edge_linewidth=4,
    arrow=True,
    arrow_color="orange",
    arrow_line="dotted",
    connection_style="arc3,rad=-0.3",
    axis=False,
)
plt.show()
