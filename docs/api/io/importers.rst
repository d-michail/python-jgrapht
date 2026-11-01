.. _io/importers:

Reading graphs
**************

.. currentmodule:: jgrapht

:func:`read_graph` reads a file (a name, a path or an open file) and :func:`parse_graph` a string. Both
return a new graph. The attributes found in the file are stored in the graph, in ``vertex_attrs``,
``edge_attrs`` and ``graph_attrs`` (see :ref:`attributes`).

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.parse_graph('digraph { a -> b [weight=2]; b -> c }', 'dot', weighted=True)
  >>> g, g.directed
  (Graph(directed=True, weighted=True, vertices=3, edges=2), True)
  >>> h = jg.parse_graph('digraph { a [color=red]; a -> b }', 'dot')
  >>> h.vertex_attrs['a']
  {'ID': 'a', 'color': 'red'}
  >>> jg.parse_graph('1,2\n2,3\n', 'csv', variant='edge_list', vertex_factory=int)
  Graph(directed=False, weighted=False, vertices=3, edges=2)
  >>> jg.import_formats()
  ['csv', 'dimacs', 'dot', 'gexf', 'gml', 'graph6', 'graphml', 'json', 'tsplib']

Functions
=========

.. autofunction:: read_graph
.. autofunction:: parse_graph
.. autofunction:: import_formats

Options
=======

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Option
     - Meaning
   * - ``directed``
     - Build a directed graph. By default taken from the document where the format declares it
       (DOT, GML, GraphML, GEXF, DIMACS, digraph6), otherwise ``False``.
   * - ``weighted``
     - Read edge weights. **Default** ``False``: the result is unweighted and weights in the file
       are ignored. TSPLIB is always weighted.
   * - ``sparse``
     - Return a :class:`SparseGraph` (vertices ``0..n-1``).
   * - ``vertex_factory``
     - Function applied to each vertex identifier of the file.
   * - ``into``
     - Add the vertices and edges of the file to this :class:`Graph` instead of building a new
       one, and return it. Its direction and weightedness are used; an edge it does not allow
       (self-loop, parallel edge) raises :class:`GraphError` after the elements before it have been
       added. The attributes of the file are added to those of the graph, and the attributes of an edge are
       keyed by the edge object the graph assigned.
   * - ``variant``
     - CSV: ``edge_list``, ``adjacency_list``, ``matrix``.
   * - ``delimiter``
     - CSV: a single character (default ``,``).
   * - ``matrix_node_id``
     - CSV matrix: the first row and column hold vertex ids.
   * - ``matrix_zero_when_no_edge``
     - CSV matrix: ``0`` marks a missing edge instead of an empty field.
   * - ``default_weight``
     - DIMACS: weight of edges without one (default ``1.0``).
   * - ``edge_weight_attribute``
     - GraphML: name of the attribute holding the weight.
   * - ``vertices_name``, ``edges_name``
     - JSON: the members holding the vertex and edge arrays.
   * - ``schema_validation``
     - GraphML, GEXF: accepted for compatibility (default ``True``); the Rust parser does not
       validate against the XML schema yet, so the flag has no effect.
