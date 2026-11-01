.. _derived:

Derived graphs
**************

.. currentmodule:: jgrapht

Functions that build a new graph from an existing one, keeping the vertex and edge objects:
copies, induced and edge subgraphs, unions, reversed and undirected versions, and re-weighted
versions. Each function returns a new, independent :class:`Graph`: later changes to the original
do not show up in the result, and changing the result does not change the original.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.complete_graph(5)
  >>> h = jg.induced_subgraph(g, [0, 1, 2])
  >>> h.edge_count()
  3
  >>> w = jg.as_weighted(h, 2.0)
  >>> w.weighted, w.edge_weight(0)
  (True, 2.0)
  >>> r = jg.reverse_edges(jg.path_graph(3, directed=True))
  >>> [(r.edge_source(e), r.edge_target(e)) for e in r.edges()]
  [(1, 0), (2, 1)]

Functions
=========

.. autofunction:: copy_graph
.. autofunction:: induced_subgraph
.. autofunction:: edge_subgraph
.. autofunction:: graph_union
.. autofunction:: as_undirected
.. autofunction:: reverse_edges
.. autofunction:: as_weighted
.. autofunction:: as_unweighted

Read-only wrapper
=================

Unlike the functions above, which return independent copies, a read-only wrapper holds a reference
to its graph and always shows its current state. It can be passed to every algorithm that takes a
single graph; functions that take two graphs do not accept it, so make a graph with
:func:`copy_graph` first.

.. autofunction:: as_unmodifiable
.. autoclass:: UnmodifiableGraph
