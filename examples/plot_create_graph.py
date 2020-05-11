# -*- coding: utf-8 -*-

"""
Create Graph
============

This is a basic tutorial which shows how to use the python-jgrapht library.
"""

# %%
# Start by importing the package

import jgrapht

# %%
# Creating a graph is done using the factory method. You need to supply the basic
# characteristics of the graph such as whether it is directed or not, has weight or 
# not.

g = jgrapht.create_graph(directed=True, weighted=True)

# %%
# We can add vertices by providing their identifier. The method returns `True` if the 
# vertex was added, `False` otherwise. Identifiers of vertices and edges are always
# integers.

g.add_vertex(0)

# %%
# Adding multiple vertices together can also be performed,

g.add_vertices_from(range(1,5))

# %%
# Find out all the vertices in the graph by using the following method

print(g.vertices())

# %%
#
# TODO
#
#
