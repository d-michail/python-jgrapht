.. _traversals:

Traversals
**********

.. currentmodule:: jgrapht

Graph traversals return the vertices in visiting order: breadth-first and depth-first
search, lexicographic BFS, maximum cardinality and degeneracy orderings, and random walks. ``start``
is the vertex to begin from; without it the traversal covers every component.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.grid_graph(2, 3)
  >>> jg.bfs(g, 0)
  [0, 1, 3, 2, 4, 5]
  >>> jg.dfs(g, 0)
  [0, 1, 2, 5, 4, 3]
  >>> jg.bfs_depths(g, 0)
  {0: 0, 1: 1, 3: 1, 2: 2, 4: 2, 5: 3}
  >>> jg.degeneracy_ordering(g)
  ([0, 3, 1, 2, 4, 5], 2)

Functions
=========

.. autofunction:: bfs
.. autofunction:: bfs_depths
.. autofunction:: dfs
.. autofunction:: dfs_postorder
.. autofunction:: lex_bfs_order
.. autofunction:: maximum_cardinality_order
.. autofunction:: degeneracy_ordering
.. autofunction:: random_walk
