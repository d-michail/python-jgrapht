.. _algorithms/shortestpaths:

Shortest paths
**************

.. currentmodule:: jgrapht

Single-pair, single-source and all-pairs shortest paths, with the classic algorithms
selectable by name (``"dijkstra"``, ``"bellman_ford"``, ``"floyd_warshall"``, ``"johnson"``,
``"bidirectional_dijkstra"``, ``"delta_stepping"``, ...). Paths are returned as :class:`GraphPath`
objects, distances as dicts keyed by vertex. Unreachable targets give ``None`` rather than an
infinite weight. Also here: A\* with a Python heuristic, k shortest paths, disjoint paths,
contraction hierarchies and transit-node routing for many queries, and multi-objective paths.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(weighted=True)
  >>> for v in 'abcde':
  ...     _ = g.add_vertex(v)
  >>> for u, v, w in [('a', 'b', 1.0), ('b', 'c', 2.0), ('a', 'c', 5.0), ('c', 'd', 1.0), ('d', 'e', 3.0)]:
  ...     _ = g.add_edge(u, v, weight=w)
  >>> path = jg.shortest_path(g, 'a', 'e')
  >>> path.vertices, path.edges, path.weight
  (['a', 'b', 'c', 'd', 'e'], [0, 1, 3, 4], 7.0)
  >>> jg.single_source_distances(g, 'a')
  {'d': 4.0, 'b': 1.0, 'a': 0.0, 'e': 7.0, 'c': 3.0}
  >>> jg.k_shortest_paths(g, 'a', 'e', 2)
  [GraphPath(vertices=['a', 'b', 'c', 'd', 'e'], weight=7.0), GraphPath(vertices=['a', 'c', 'd', 'e'], weight=9.0)]
  >>> jg.shortest_path(g, 'e', 'a', algorithm='bellman_ford').weight
  7.0
  >>> jg.astar_shortest_path(g, 'a', 'e', heuristic=lambda v, t: 0.0).weight
  7.0

Functions
=========

.. autofunction:: shortest_path
.. autofunction:: single_source_distances
.. autofunction:: all_pairs_distances
.. autofunction:: astar_shortest_path
.. autofunction:: single_source_paths
.. autofunction:: negative_cycle
.. autofunction:: alt_shortest_path
.. autofunction:: bidirectional_astar_shortest_path
.. autofunction:: batch_shortest_paths
.. autofunction:: many_to_many_shortest_paths
.. autofunction:: multi_objective_shortest_paths
.. autofunction:: closest_first
.. autofunction:: k_shortest_paths
.. autofunction:: k_disjoint_shortest_paths
.. autofunction:: all_directed_paths
.. autofunction:: count_dag_paths
