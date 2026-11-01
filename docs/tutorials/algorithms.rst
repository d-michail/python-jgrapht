.. _tutorials/algorithms:

Using algorithms
================

.. currentmodule:: jgrapht

Algorithms are module-level functions that take the graph as their first argument and work with
either graph class. This tutorial shows the conventions on a few examples.

Variants are strings
--------------------

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.grid_graph(4, 4)
  >>> jg.shortest_path(g, 0, 15).weight
  6.0
  >>> jg.shortest_path(g, 0, 15, algorithm='bidirectional_dijkstra').weight
  6.0
  >>> jg.coloring(g, algorithm='saturation_degree')
  (2, {7: 0, 12: 1, 8: 0, 13: 0, 15: 0, 10: 0, 11: 1, 1: 1, 3: 1, 4: 1, 9: 1, 6: 1, 5: 0, 2: 0, 0: 0, 14: 1})
  >>> jg.maximum_matching(g, algorithm='greedy').weight
  8.0

Result objects
--------------

Structured results are small objects with named attributes. A :class:`~jgrapht.GraphPath` has
``vertices``, ``edges`` and ``weight``; a flow has ``value`` and the flow on each edge; a matching its
``edges`` and ``weight``.

.. code-block:: pycon

  >>> path = jg.shortest_path(g, 0, 15)
  >>> path.vertices
  [0, 1, 5, 9, 10, 14, 15]
  >>> path.edges
  [0, 3, 10, 16, 19, 23]
  >>> m = jg.maximum_matching(g)
  >>> len(m.edges)
  8

Dictionaries and lists
----------------------

Per-vertex results are dictionaries keyed by vertex; collections of vertices are lists.

.. code-block:: pycon

  >>> pr = jg.pagerank(g)
  >>> round(sum(pr.values()), 6)
  1.0
  >>> jg.connected_components(g)
  [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
  >>> len(jg.articulation_points(g))
  0

Missing is None
---------------

.. code-block:: pycon

  >>> d = jg.path_graph(3, directed=True)
  >>> jg.shortest_path(d, 2, 0)
  >>> jg.negative_cycle(d, 0)

Weights
-------

Weighted graphs use the edge weights; unweighted graphs count every edge as 1. Algorithms that
need weights as an input of their own (flow capacities, supplies) say so in their documentation.

.. code-block:: pycon

  >>> w = jg.as_weighted(g, lambda e: 1.0 + e % 3)
  >>> jg.shortest_path(w, 0, 15).weight
  8.0

Callbacks
---------

Where a function takes a callable, exceptions propagate. An A\* heuristic for the grid, taking the
Manhattan distance between vertices numbered row by row:

.. code-block:: pycon

  >>> def manhattan(v, target):
  ...     return abs(v // 4 - target // 4) + abs(v % 4 - target % 4)
  >>> jg.astar_shortest_path(g, 0, 15, heuristic=manhattan).weight
  6.0
  >>> def broken(v, target):
  ...     raise RuntimeError('boom')
  >>> try:
  ...     jg.astar_shortest_path(g, 0, 15, heuristic=broken)
  ... except RuntimeError as e:
  ...     print('raised', e)
  raised boom

