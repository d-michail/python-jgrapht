.. _algorithms/matching:

Matching
********

.. currentmodule:: jgrapht

Maximum cardinality and maximum weight matchings in general and bipartite graphs, perfect
matchings and greedy approximations. Matchings are returned as :class:`Matching` objects with their
edges and weight. (For the cardinality algorithms the weight is the number of edges.)

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.ring_graph(6)
  >>> m = jg.maximum_matching(g)
  >>> len(m.edges), m.weight
  (3, 3.0)
  >>> jg.perfect_matching(g).weight
  3.0

Functions
=========

.. autofunction:: maximum_matching
.. autofunction:: weighted_matching
.. autofunction:: perfect_matching
.. autofunction:: bipartite_maximum_matching
.. autofunction:: bipartite_maximum_weight_matching
.. autofunction:: bipartite_minimum_weight_perfect_matching
.. autoclass:: Matching
   :members:
