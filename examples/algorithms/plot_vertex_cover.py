# -*- coding: utf-8 -*-

"""
Vertex Cover
============

In this example we demostrate how to find compute a vertex cover in
undirected graphs.
"""

# %%
# Start by importing the package.

import jgrapht
import jgrapht.algorithms.vertexcover as vc
import jgrapht.drawing.draw_matplotlib as drawing
import matplotlib.pyplot as plt

# %%
# We start by creating a "star" graph with a few additional edges.

g = jgrapht.create_graph(directed=False, weighted=False)

for i in range(11):
    g.add_vertex(i)

for i in range(10):
    g.add_edge(i, 10)

print(g)

# %%
# Then, we execute the 2 approximation algorithm of R. Bar-Yehuda and S. Even.

weight, vertex_cover = vc.baryehuda_even(g)

# %%
# The result is a tuple which contains whether the weight and the vertex cover.
# Although it failed to find the optimum which is 1.0, the returned solution is 
# at most twice the optimum.
# 
print('Vertex cover weight: {}'.format(weight))
print('Vertex cover: {}'.format(vertex_cover))


# %%
# Ploting the graph and separate color for the vertex cover vertices.
# component.
positions = drawing.layout(g, name="fruchterman_reingold", seed=17)

drawing.draw_jgrapht_vertices(g, positions=positions, vertex_list=vertex_cover, vertex_color='red')

non_vertex_cover = g.vertices - vertex_cover
drawing.draw_jgrapht_vertices(g, positions=positions, vertex_list=non_vertex_cover, vertex_color='gray')

drawing.draw_jgrapht_edges(g, positions=positions)

plt.show()
