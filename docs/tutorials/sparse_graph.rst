.. _tutorials/sparse_graph:

.. currentmodule:: jgrapht

Sparse graph tutorial
=====================

The sparse graph is a special implementation of a graph with integer vertices and edges.
It has two main restrictions which are: 

  * the graph is unmodifiable and thus needs to be bulk-loaded, 
  * the vertices and edges are integers continously numbered in :math:`[0, n)` and 
    :math:`[0, m)` where :math:`n` and :math:`m` are the total number of vertices
    and edges respectively.

These two restrictions are translated to two main benefits which are:

  * the graph has small memory footprint, and 
  * the graph is usually much faster, mostly due to its cache-friendly representation on 
    modern machines.

From the above discussion it should be clear that they are best suited for static workloads
where the user needs to load a graph and run (once or multiple times) some complex algorithm. 
Note also that bulk-loading a sparse graph is usually much faster than adding edges one by 
one in the default graph.

Creating a sparse graph
-----------------------

Sparse graphs must be bulk-loaded using edge lists. 

.. nbplot::

  >>> import jgrapht
  >>> edgelist = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 5), (0, 4), (2, 6)]
  >>> g = jgrapht.create_sparse_graph(edgelist, 7, directed=True, weighted=False)

The first parameter is the list of tuples `(u,v)`. In case a weighted graph is requested, then
the tuples must be `(u,v,weight)`. Note that while sparse graphs are unmodifiable w.r.t. their
structure, the edge weights can be modified. The second parameter is the number of vertices in the
graph. Vertices always start from zero and increase continously. If the user does not provide one,
then it will be deduced by reading the edge list. Finally, the sparse graph representation always
allows self-loops and multiple-edges.



