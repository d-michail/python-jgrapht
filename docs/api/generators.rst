.. _generators:

Generators
**********

.. currentmodule:: jgrapht

Generators build a new graph of a given family. Every generator returns a :class:`Graph` on the integer
vertices ``0..n-1`` (its edges are the integers ``0, 1, ...``) or, with ``sparse=True``, a
:class:`SparseGraph`. Those that can produce both kinds take ``directed=True`` for a directed graph.
See also the :doc:`generators tutorial <../tutorials/generators>`.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.gnm_random_graph(8, 10, seed=42)
  >>> len(g), g.edge_count()
  (8, 10)
  >>> s = jg.grid_graph(3, 3, sparse=True)
  >>> s
  SparseGraph(directed=False, weighted=False, vertices=9, edges=12)
  >>> jg.named_graph('petersen')
  Graph(directed=False, weighted=False, vertices=10, edges=15)

Structured graphs
=================

Graphs of a given shape: paths, cycles, stars, wheels, complete and complete bipartite graphs, grids, hypercubes and more; and graphs built from a weight matrix.

.. autofunction:: empty_graph
.. autofunction:: path_graph
.. autofunction:: ring_graph
.. autofunction:: star_graph
.. autofunction:: wheel_graph
.. autofunction:: complete_graph
.. autofunction:: complete_bipartite_graph
.. autofunction:: grid_graph
.. autofunction:: hypercube_graph
.. autofunction:: generalized_petersen_graph
.. autofunction:: windmill_graph
.. autofunction:: graph_from_weight_matrix
.. autofunction:: bipartite_graph_from_weight_matrix

Random graphs
=============

Random models. All take a ``seed`` for reproducible output.

.. autofunction:: gnp_random_graph
.. autofunction:: gnm_random_graph
.. autofunction:: barabasi_albert_graph
.. autofunction:: barabasi_albert_forest
.. autofunction:: scale_free_graph
.. autofunction:: directed_scale_free_graph
.. autofunction:: watts_strogatz_graph
.. autofunction:: prufer_tree
.. autofunction:: random_regular_graph
.. autofunction:: planted_partition_graph
.. autofunction:: kleinberg_small_world_graph
.. autofunction:: linearized_chord_diagram_graph
.. autofunction:: gnm_random_bipartite_graph
.. autofunction:: gnp_random_bipartite_graph

Famous graphs
=============

The 44 named graphs of the library (Petersen, Heawood, Frucht, the Zachary karate club, ...).

.. autofunction:: named_graph_names
.. autofunction:: named_graph

Flow instances
==============

Random flow problems (NETGEN). They return the graph with the data an algorithm needs.

.. autofunction:: maximum_flow_network
.. autofunction:: bipartite_matching_network
.. autofunction:: minimum_cost_flow_network

