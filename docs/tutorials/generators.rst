.. _tutorials/generators:

Generating graphs
=================

.. currentmodule:: jgrapht

Generators build a new graph of a given family. Each returns a :class:`~jgrapht.Graph` on the vertices
``0..n-1`` or, with ``sparse=True``, a :class:`~jgrapht.SparseGraph`. Random generators take a
``seed`` so that results can be reproduced.

Structured graphs
-----------------

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.complete_graph(5)
  >>> len(g), g.edge_count()
  (5, 10)
  >>> jg.ring_graph(6, directed=True).edge_count()
  6
  >>> jg.hypercube_graph(3).edge_count()
  12
  >>> jg.grid_graph(3, 4).edge_count()
  17

Random graphs
-------------

.. code-block:: pycon

  >>> a = jg.gnm_random_graph(10, 15, seed=1)
  >>> b = jg.gnm_random_graph(10, 15, seed=1)
  >>> sorted(a.edges()) == sorted(b.edges())
  True
  >>> jg.barabasi_albert_graph(3, 2, 20, seed=7).edge_count()
  37
  >>> jg.watts_strogatz_graph(20, 4, 0.2, seed=3).edge_count()
  40
  >>> jg.random_regular_graph(10, 3, seed=5).degree_of(0)
  3

Famous graphs
-------------

:func:`~jgrapht.named_graph_names` lists the 44 named graphs.

.. code-block:: pycon

  >>> jg.named_graph_names()[:5]
  ['bidiakis_cube', 'blanusa_first_snark', 'blanusa_second_snark', 'brinkmann', 'bucky_ball']
  >>> p = jg.named_graph('petersen')
  >>> len(p), p.edge_count(), jg.girth(p)
  (10, 15, 5)

Flow instances
--------------

The NETGEN generators produce random flow problems. They return the graph together with what an
algorithm needs, here the sources and sinks of a maximum flow problem; the edge weights are the
capacities.

.. code-block:: pycon

  >>> g, sources, sinks = jg.maximum_flow_network(20, 60, 50, min_capacity=1, max_capacity=10, seed=5)
  >>> g.directed, g.weighted
  (True, True)
  >>> jg.maximum_flow(g, sources[0], sinks[0]).value >= 0
  True

