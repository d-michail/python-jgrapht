.. _io/exporters:

Writing graphs
**************

.. currentmodule:: jgrapht

:func:`write_graph` writes a file (a name, a path or an open file) and :func:`graph_to_string` returns a string.
Vertices are numbered ``1, 2, ...`` unless you give ``vertex_id``, for example ``vertex_id=str`` to
keep their names.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.path_graph(3)
  >>> print(jg.graph_to_string(g, 'csv', variant='edge_list'))
  1,2
  2,3
  >>> print(jg.graph_to_string(g, 'dot', vertex_id=str))
  strict graph G {
    0;
    1;
    2;
    0 -- 1;
    1 -- 2;
  }
  >>> print(jg.graph_to_string(g, 'graph6'))
  Bg
  >>> jg.export_formats()
  ['csv', 'dimacs', 'dot', 'gexf', 'gml', 'graph6', 'graphml', 'json', 'lemon', 'matrix', 'visio']

Functions
=========

.. autofunction:: write_graph
.. autofunction:: graph_to_string
.. autofunction:: export_formats

Options
=======

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Option
     - Formats
   * - ``vertex_id``
     - csv, dimacs, dot, gexf, graphml, json, lemon, matrix, visio
   * - ``edge_id``
     - gexf, gml, graphml, json
   * - ``vertex_attributes``, ``edge_attributes``
     - dot, gexf, gml, graphml, json
   * - ``graph_attributes``
     - dot, graphml
   * - ``graph_id``
     - dot
   * - ``subgraphs``
     - dot: a dict from subgraph name to a dict with the optional keys ``vertices``, ``edges``,
       ``graph_attributes`` and ``cluster_attributes``. Names must be valid DOT identifiers
       (``cluster_...`` for Graphviz clusters). The exporter also writes a statement carrying the
       cluster attributes, so reading the output back adds a vertex with the subgraph's name.
   * - ``edge_weights``
     - csv, dimacs, dot (as attribute ``weight``), gexf, gml, graphml, json (as attribute
       ``weight``), lemon
   * - ``vertex_attribute_types``, ``edge_attribute_types``
     - graphml, gexf: declare attribute types and defaults (see below)
   * - ``graph_attribute_types``
     - graphml
   * - ``vertex_label_attribute``, ``edge_label_attribute``, ``edge_weight_attribute``
     - graphml: names of the attributes used for labels and weights
   * - ``vertex_graphics``
     - gml: a dict or function giving the attributes written in each vertex's ``graphics`` block
       (``x``, ``y``, ``w``, ``h``, ``fill``, ...)
   * - ``vertex_labels``
     - gml, graphml
   * - ``edge_labels``
     - gexf, gml, graphml
   * - ``variant``
     - csv, dimacs, graph6, matrix
   * - ``delimiter``, ``matrix_node_id``, ``matrix_zero_when_no_edge``
     - csv
   * - ``edge_types``, ``meta``, ``creator``, ``keywords``, ``description``
     - gexf
   * - ``escape_strings``
     - gml, lemon
   * - ``vertices_name``, ``edges_name``
     - json

Stored attributes
=================

The formats that support attributes write the attributes stored in the graph (``vertex_attrs``,
``edge_attrs`` and ``graph_attrs``, see :ref:`attributes`) when the options ``vertex_attributes``,
``edge_attributes`` and ``graph_attributes`` are not given. Giving an option replaces the stored
attributes of that kind. A value that is not a ``bool``, ``int``, ``float`` or ``str`` is written as its
``str``. The other formats ignore stored attributes.

Declaring attribute types
=========================

GraphML and GEXF declare the type of every attribute. By default the type is inferred from the
values given (``bool`` is ``boolean``, ``int`` is ``int`` or ``long``, ``float`` is ``double``,
``str`` is ``string``; integers and floats of one attribute merge to ``double``). To declare types
explicitly, or to declare attributes with a default value that no vertex or edge sets, pass a dict
from attribute name to a type name or to a pair ``(type name, default)``:

.. code-block:: python

    jg.graph_to_string(
        g,
        "graphml",
        vertex_attribute_types={"color": ("string", "blue"), "rank": "long"},
        edge_attribute_types={"cost": ("double", 1.0)},
    )

GraphML types are ``boolean``, ``int``, ``long``, ``float``, ``double`` and ``string``; GEXF types
are ``boolean``, ``integer``, ``long``, ``float``, ``double``, ``string``, ``liststring`` and
``anyURI``. Values equal to the declared default are not written.
