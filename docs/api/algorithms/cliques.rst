.. _algorithms/cliques:

Cliques, independent sets and covers
************************************

.. currentmodule:: jgrapht

Maximal and maximum cliques, independent sets, vertex covers, and the related notions for
chordal graphs, together with checkers for each property.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.named_graph('petersen')
  >>> len(jg.maximum_independent_set(g))
  4
  >>> len(jg.maximum_clique(g))
  2
  >>> len(jg.vertex_cover(g))
  2
  >>> len(list(jg.maximal_cliques(jg.complete_graph(5))))
  1

Functions
=========

.. autofunction:: maximal_cliques
.. autofunction:: maximum_clique
.. autofunction:: greedy_independent_set
.. autofunction:: maximum_independent_set
.. autofunction:: vertex_cover
.. autofunction:: is_vertex_cover
.. autofunction:: is_clique
.. autofunction:: is_independent_set
.. autofunction:: chordal_maximum_clique
.. autofunction:: chordal_maximum_independent_set
.. autofunction:: chordal_minimal_separators
.. autofunction:: clique_minimal_separator_decomposition
.. autoclass:: CliqueSeparatorDecomposition
   :members:
.. autofunction:: berge_certificate
.. autofunction:: number_of_triangles
.. autofunction:: count_triangles_among
