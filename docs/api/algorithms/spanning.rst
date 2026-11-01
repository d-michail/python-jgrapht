.. _algorithms/spanning:

Spanning trees
**************

.. currentmodule:: jgrapht

Minimum spanning trees (Kruskal, Prim, Boruvka), minimum and maximum arborescences of directed
graphs, Steiner trees, capacitated spanning trees and spanners.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(weighted=True)
  >>> for v in 'abcde':
  ...     _ = g.add_vertex(v)
  >>> for u, v, w in [('a', 'b', 1.0), ('b', 'c', 2.0), ('a', 'c', 5.0), ('c', 'd', 1.0), ('d', 'e', 3.0)]:
  ...     _ = g.add_edge(u, v, weight=w)
  >>> weight, edges = jg.minimum_spanning_tree(g)
  >>> weight, sorted(edges)
  (7.0, [0, 1, 3, 4])
  >>> jg.minimum_spanning_tree(g, algorithm='prim')[0]
  7.0

Functions
=========

.. autofunction:: minimum_spanning_tree
.. autofunction:: minimum_arborescence_tree
.. autofunction:: maximum_arborescence_tree
.. autofunction:: steiner_tree
.. autofunction:: steiner_tree_weight
.. autofunction:: capacitated_minimum_spanning_tree
.. autoclass:: CapacitatedSpanningTree
   :members:
.. autofunction:: cyclic_exchange_augmentation
.. autofunction:: greedy_multiplicative_spanner
