# -*- coding: utf-8 -*-

"""
PageRank
========

In this example we create a directed graph and compute PageRank. The graph
is the same as in the `wikipedia <https://en.wikipedia.org/wiki/PageRank>`_.

.. image :: https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/PageRanks-Example.jpg/1024px-PageRanks-Example.jpg 

"""

# %%
# Start by importing the package

import jgrapht
import jgrapht.algorithms.scoring as scoring

# %%
# Creating a graph is done using the factory method. By default graphs are directed
# and weighted.

g = jgrapht.create_graph()

# %%
# We can add vertices by providing their identifier. The method returns `True` if the 
# vertex was added, `False` otherwise. Identifiers of vertices and edges are always
# integers.

for v in range(0, 11):
    g.add_vertex(v)

# %% 
# Our graph's vertex set now looks like

print (g.vertices())

# %%
# We also add the edges

g.create_edge(1, 2)
g.create_edge(2, 1)
g.create_edge(3, 0)
g.create_edge(3, 1)
g.create_edge(4, 1)
g.create_edge(4, 3)
g.create_edge(4, 5)
g.create_edge(5, 1)
g.create_edge(5, 4)
g.create_edge(6, 1)
g.create_edge(6, 4)
g.create_edge(7, 1)
g.create_edge(7, 4)
g.create_edge(8, 1)
g.create_edge(8, 4)
g.create_edge(9, 4)
g.create_edge(10, 4)

# %%
# We now have the following edges

print(g.edges())

# %%
# Execute Pagerank using
pagerank = scoring.pagerank(g)

# %%
# The returned object is a dictionary from vertices to floating point values.
# Let us store it in a list

result = [pagerank[v] for v in g.vertices()]
print(result)

# %%
#
