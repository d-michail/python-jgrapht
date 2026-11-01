.. _algorithms/flow:

Flow
****

.. currentmodule:: jgrapht

Maximum flow (Dinic, Edmonds-Karp, push-relabel, Boykov-Kolmogorov) with edge weights as
capacities, and minimum-cost flow with integer supplies and capacities.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(directed=True, weighted=True)
  >>> for v in 'stab':
  ...     _ = g.add_vertex(v)
  >>> for u, v, c in [('s', 'a', 3.0), ('s', 'b', 2.0), ('a', 'b', 1.0), ('a', 't', 2.0), ('b', 't', 3.0)]:
  ...     _ = g.add_edge(u, v, weight=c)
  >>> flow = jg.maximum_flow(g, 's', 't')
  >>> flow.value
  5.0
  >>> jg.maximum_flow(g, 's', 't', algorithm='push_relabel').value
  5.0

Functions
=========

.. autofunction:: maximum_flow
.. autoclass:: MaximumFlow
   :members:
.. autofunction:: minimum_cost_flow
.. autoclass:: MinimumCostFlow
   :members:
