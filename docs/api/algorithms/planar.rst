.. _algorithms/planar:

Planarity
*********

.. currentmodule:: jgrapht

Planarity testing with the Boyer-Myrvold algorithm. A planar graph comes with an embedding, a
non-planar one with a Kuratowski subdivision as the certificate.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> jg.is_planar(jg.grid_graph(3, 3))
  True
  >>> jg.is_planar(jg.complete_graph(5))
  False
  >>> jg.is_planar(jg.complete_bipartite_graph(3, 3))
  False

Functions
=========

.. autofunction:: is_planar
.. autofunction:: planar_embedding
.. autofunction:: kuratowski_subdivision
