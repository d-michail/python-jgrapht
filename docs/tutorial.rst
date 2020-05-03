.. _tutorial:

Tutorial
========

This guide will help you start using the library.

Creating a graph
----------------

Let us start by creating a graph::

  import jgrapht
  g = jgrapht.create_graph(directed=True, weighted=True)

The graph is a collection of nodes and edges. In python-jgrapht vertices and edges are 
always long integers.

Adding nodes
------------

Nodes can be added by calling::

  g.add_vertex()

The method returns the newly created vertex. The vertices are long integers starting from zero. 








TODO


