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
#
# TODO
#
#
