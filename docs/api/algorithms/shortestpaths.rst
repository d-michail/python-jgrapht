
.. _algorithms/shortestpaths:

.. py:module:: jgrapht.algorithms.shortestpaths

Shortest Paths
**************

Representation
--------------

The shortest path module contains the following classes for the 
representation of the shortest path queries. All methods related to shortest paths
return instances from these classes.

.. autoclass:: GraphPath
   :members:

.. autoclass:: SingleSourcePaths
   :members:

.. autoclass:: AllPairsPaths
   :members:

Algorithms
----------

.. autofunction:: dijkstra

.. autofunction:: bfs

.. autofunction:: bellman_ford

.. autofunction:: johnson_allpairs

.. autofunction:: floyd_warshall_allpairs

