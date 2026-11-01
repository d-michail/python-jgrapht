.. _algorithms/isomorphism:

Isomorphism
***********

.. currentmodule:: jgrapht

Both graphs must be of the same kind (two :class:`Graph` objects of the same
directedness, or two :class:`SparseGraph` objects of the same directedness and
weighting). The VF2 matchers reject multigraphs, which includes every
:class:`SparseGraph`.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> a, b = jg.named_graph('petersen'), jg.generalized_petersen_graph(5, 2)
  >>> jg.is_isomorphic(a, b)
  True
  >>> jg.is_isomorphic(a, jg.ring_graph(10))
  False
  >>> len(jg.subgraph_isomorphisms(jg.complete_graph(4), jg.complete_graph(3)))
  24

Functions
=========

.. autofunction:: is_isomorphic
.. autofunction:: isomorphisms
.. autofunction:: is_subgraph_isomorphic
.. autofunction:: subgraph_isomorphisms
.. autofunction:: tree_isomorphism
.. autofunction:: forest_isomorphism
.. autofunction:: color_refinement_isomorphism
