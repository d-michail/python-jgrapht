# -*- coding: utf-8 -*-

"""
Shortest Paths using Dijkstra
=============================

In this example we create an undirected graph and compute single-source shortest 
paths using Dijkstra. The graph is constructed using the Barabasi-Albert model.
"""

# %%
# Start by importing the package

import jgrapht
import jgrapht.generators as gen
import jgrapht.algorithms.shortestpaths as sp
import random

# %%
# Creating a graph is done using the factory method.

g = jgrapht.create_graph(directed=False, weighted=True)


# %%
# We use the Barabasi-Albert generator to populate the graph. We start with the 
# complete graph of 3 vertices and reach 10 vertices. Each of the last 7 vertices 
# gets connected with the previous ones using preferential attachment.

gen.barabasi_albert(g, 3, 3, 10, seed=17)

# %%
# We also assign some random weights from [0, 100) to the edges. 

rng = random.Random(17)
for e in g.edges: 
    g.set_edge_weight(e, 100 * rng.random())

# %%
# Let us print the graph

print(g)

# %%
# Then, we execute Dijkstra starting from vertex 6.

tree = sp.dijkstra(g, source_vertex=6)

# %%
# The result represents all shortest paths starting from the source vertex. They 
# are instances of :py:class:`~jgrapht.types.SingleSourcePaths`. 
# To build specific paths to target vertices you call method :py:meth:`~jgrapht.types.SingleSourcePaths.get_path`.
# None is returned if no such path exists.

path = tree.get_path(8)


# %%
# Paths are instances of :py:class:`~jgrapht.types.GraphPath`. 

print('path start: {}'.format(path.start_vertex))
print('path end: {}'.format(path.end_vertex))
print('path edges: {}'.format(path.edges))
print('path vertices: {}'.format(path.vertices))
print('path weight: {}'.format(path.weight))


# %%
# Dijkstra's algorithm is faster in practice if you also know the target. In that
# case you can also perform a bidirectional search which usually results in faster 
# running times.

other_path = sp.dijkstra(g, source_vertex=4, target_vertex=7)

print('path start: {}'.format(other_path.start_vertex))
print('path end: {}'.format(other_path.end_vertex))
print('path edges: {}'.format(other_path.edges))
print('path vertices: {}'.format(other_path.vertices))
print('path weight: {}'.format(other_path.weight))


