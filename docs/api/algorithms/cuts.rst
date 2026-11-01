.. _algorithms/cuts:

Cuts
****

.. currentmodule:: jgrapht

Minimum s-t cuts, global minimum cuts (Stoer-Wagner), Gomory-Hu trees and minimum odd cuts.
s-t cuts are returned as :class:`MinimumCut` objects; the Stoer-Wagner cut as ``(weight, one_side)``.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(weighted=True)
  >>> for v in 'abcde':
  ...     _ = g.add_vertex(v)
  >>> for u, v, w in [('a', 'b', 1.0), ('b', 'c', 2.0), ('a', 'c', 5.0), ('c', 'd', 1.0), ('d', 'e', 3.0)]:
  ...     _ = g.add_edge(u, v, weight=w)
  >>> weight, side = jg.stoer_wagner_minimum_cut(g)
  >>> weight, sorted(side)
  (1.0, ['d', 'e'])
  >>> cut = jg.minimum_st_cut(g, 'a', 'e')
  >>> cut
  MinimumCut(capacity=1.0, cut_edges=1)

Functions
=========

.. autofunction:: minimum_st_cut
.. autofunction:: stoer_wagner_minimum_cut
.. autofunction:: gomory_hu_tree
.. autofunction:: equivalent_flow_tree
.. autofunction:: minimum_odd_cut
.. autoclass:: MinimumCut
   :members:
