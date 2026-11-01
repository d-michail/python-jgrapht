.. _algorithms/graphclasses:

Graph classes, centers and dense subgraphs
******************************************

.. currentmodule:: jgrapht

Recognition of graph classes (perfect, weakly chordal, ...), k-center, and densest subgraphs.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.named_graph('petersen')
  >>> jg.is_perfect(g)
  False
  >>> jg.is_perfect(jg.complete_graph(5))
  True

Functions
=========

.. autofunction:: k_center
.. autofunction:: densest_subgraph
.. autofunction:: gon_k_center
.. autofunction:: is_perfect
.. autofunction:: odd_hole_or_antihole
.. autofunction:: is_weakly_chordal
.. autofunction:: weak_chordality_certificate
