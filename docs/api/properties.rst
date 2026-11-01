.. _properties:

Structural properties
*********************

.. currentmodule:: jgrapht

Predicates and small certificates for structural properties: forests and trees, simple and
complete graphs, bipartiteness (with a partition), DAGs (with a topological order), and a few
special classes.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.complete_bipartite_graph(2, 3)
  >>> jg.is_bipartite(g), jg.is_tree(g), jg.is_complete(g)
  (True, False, False)
  >>> jg.bipartite_partition(g)
  ([0, 1], [2, 3, 4])
  >>> d = jg.path_graph(4, directed=True)
  >>> jg.is_dag(d), jg.topological_sort(d)
  (True, [0, 1, 2, 3])

Functions
=========

.. autofunction:: is_forest
.. autofunction:: is_tree
.. autofunction:: has_self_loops
.. autofunction:: has_multiple_edges
.. autofunction:: is_simple
.. autofunction:: is_complete
.. autofunction:: is_triangle_free
.. autofunction:: is_cubic
.. autofunction:: is_split
.. autofunction:: is_bipartite
.. autofunction:: bipartite_partition
.. autofunction:: is_dag
.. autofunction:: topological_sort
