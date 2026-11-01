.. _algorithms/connectivity:

Connectivity and components
***************************

.. currentmodule:: jgrapht

Connected, weakly and strongly connected components, biconnected components, articulation
points and bridges, edge and vertex connectivity, and the condensation of a directed graph. The
dynamic connectivity structure for trees is at the end.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph()
  >>> for v in range(7):
  ...     _ = g.add_vertex(v)
  >>> for u, v in [(0, 1), (1, 2), (2, 0), (2, 3), (4, 5)]:
  ...     _ = g.add_edge(u, v)
  >>> jg.connected_components(g)
  [[0, 1, 2, 3], [4, 5], [6]]
  >>> jg.is_connected(g)
  False
  >>> jg.articulation_points(g)
  [2]
  >>> jg.bridges(g)
  [3, 4]
  >>> d = jg.Graph(directed=True)
  >>> for v in range(4):
  ...     _ = d.add_vertex(v)
  >>> for u, v in [(0, 1), (1, 0), (1, 2), (2, 3), (3, 2)]:
  ...     _ = d.add_edge(u, v)
  >>> jg.strongly_connected_components(d)
  [[2, 3], [0, 1]]

Functions
=========

Components and connectivity
---------------------------

.. autofunction:: is_connected
.. autofunction:: is_weakly_connected
.. autofunction:: is_strongly_connected
.. autofunction:: is_biconnected
.. autofunction:: articulation_points
.. autofunction:: bridges
.. autofunction:: biconnected_components
.. autofunction:: block_cut_tree
.. autofunction:: condensation
.. autofunction:: edge_connectivity
.. autofunction:: vertex_connectivity
.. autofunction:: is_k_edge_connected
.. autofunction:: is_k_vertex_connected

Related
-------

.. autofunction:: connected_component_of
.. autofunction:: path_exists
.. autofunction:: block_cutpoint_graph
.. autofunction:: connected_components
.. autofunction:: strongly_connected_components

Dynamic connectivity
--------------------

.. autoclass:: TreeDynamicConnectivity
   :members:

