.. _algorithms/decompositions:

Decompositions and trees
************************

.. currentmodule:: jgrapht

Tree decompositions and treewidth, heavy-path decomposition (with vertex depths, where roots have
depth 0), the Dulmage-Mendelsohn decomposition and lowest common ancestors.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> jg.treewidth(jg.grid_graph(3, 3))
  3
  >>> t = jg.path_graph(5)
  >>> d = jg.heavy_path_decomposition(t, 0)
  >>> d.depth
  {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

Functions
=========

Tree decompositions
-------------------

.. autofunction:: tree_decomposition
.. autofunction:: treewidth
.. autofunction:: heavy_path_decomposition
.. autoclass:: HeavyPathDecomposition
   :members:
.. autofunction:: dulmage_mendelsohn_decomposition

Trees
-----

.. autofunction:: lowest_common_ancestors
.. autofunction:: all_lowest_common_ancestors

