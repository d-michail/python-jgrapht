.. _tutorials/succinct_graph:

.. currentmodule:: jgrapht

Succinct graph tutorial
=======================

The succinct graph is a special implementation of a graph with integer vertices and edges.
It is a very compact representation which is very close to the theoretical lower-bound.
It has two main restrictions which are: 

  * the graph is unmodifiable and thus needs to be bulk-loaded, 
  * the vertices and edges are integers continously numbered in :math:`[0, n)` and 
    :math:`[0, m)` where :math:`n` and :math:`m` are the total number of vertices
    and edges respectively.

Compared with sparse graphs, it will be smaller but also a little bit slower. It 
is best suited for very large graphs and for static workloads
where the user needs to load a graph and run (once or multiple times) some complex algorithm.

Creating a succinct graph
-------------------------

Succinct graphs must be bulk-loaded using edge lists. 

.. nbplot::

  >>> import jgrapht
  >>> edgelist = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 5), (0, 4), (2, 6)]
  >>> g = jgrapht.create_succinct_graph(edgelist, 7, directed=True)

The first parameter is the list of tuples `(u,v)`. The second parameter is the number of vertices in the
graph. Vertices always start from zero and increase continously. If the user does not provide one,
then it will be deduced by reading the edge list. Finally, the succinct graph representation always
allows self-loops but does not support multiple-edges nor edge-weights.


