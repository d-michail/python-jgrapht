.. _algorithms/transformations:

Transformations
***************

.. currentmodule:: jgrapht

Graph transformations that build a new graph: complement, line graph, transitive closure and
reduction, and edge contraction. For copies, subgraphs and unions see :doc:`../derived`.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.path_graph(4)
  >>> c = jg.complement(g)
  >>> c.edge_count()
  3
  >>> jg.line_graph(g).edge_count()
  2

Functions
=========

.. autofunction:: complement
.. autofunction:: line_graph
.. autofunction:: transitive_closure
.. autofunction:: transitive_reduction
.. autofunction:: contract_edge
