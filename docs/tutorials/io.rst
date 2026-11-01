.. _tutorial-io:

Reading and writing graphs
**************************

Formats
=======

:func:`read_graph` and :func:`parse_graph` read a graph from a file or a string, and
:func:`write_graph` and :func:`graph_to_string` write one. :func:`import_formats` and
:func:`export_formats` list the supported formats; the :doc:`../api/io/index` page has the option
tables.

.. code-block:: python

    import jgrapht as jg

    g = jg.Graph(weighted=True)
    for v in "abc":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=2.0)
    g.add_edge("b", "c", weight=3.0)

    text = jg.graph_to_string(g, "graphml", vertex_id=str, edge_weights=True)
    h = jg.parse_graph(text, "graphml", weighted=True)

    jg.write_graph(g, "graph.graphml", "graphml", vertex_id=str, edge_weights=True)
    h = jg.read_graph("graph.graphml", "graphml", weighted=True)

Files can be given as names, ``pathlib.Path`` objects or open files.

Things to know
==============

* **Weights are off by default when reading.** Pass ``weighted=True`` to get a weighted graph with
  the weights of the file.
* **Vertex identifiers.** Files name their vertices with strings (or integers for DIMACS, GML and
  graph6); by default those are the vertices of the new graph. Use ``vertex_factory=int`` to
  convert them. Writing numbers the vertices ``1, 2, ...`` unless you give ``vertex_id``, for
  example ``vertex_id=str`` to keep the names. Identifiers must be distinct.
* **Direction** is read from the document where the format declares it; pass ``directed=`` to
  override it.
* **Sparse graphs.** ``sparse=True`` returns a :class:`SparseGraph`, whose vertices are the numbers
  ``0..n-1`` in order of appearance. Writing works for both graph classes.
* **Undirected CSV adjacency lists** list every edge from both ends, so reading one back gives
  parallel edges; use ``variant="edge_list"`` to round-trip.
* **graph6 and SparseGraph.** A :class:`SparseGraph` counts as a multigraph, which graph6 cannot
  represent; use ``variant="sparse6"``.

Attributes
==========

Importers store the attributes found in a file in the graph, and exporters write the attributes
stored in the graph (see :ref:`attributes`). A round trip therefore keeps them:

.. code-block:: python

    g.vertex_attrs["a"].update(color="red", size=3)
    g.edge_attrs[0]["kind"] = "road"
    g.graph_attrs["title"] = "demo"

    text = jg.graph_to_string(g, "graphml", vertex_id=str)
    h = jg.parse_graph(text, "graphml")
    h.graph_attrs                 # {'title': 'demo'}
    h.vertex_attrs["a"]           # {'ID': 'a', 'color': 'red', 'size': 3}
    h.edge_attrs[0]               # {'kind': 'road'}, edges are numbered 0, 1, ...

Formats with attributes (DOT, GEXF, GML, GraphML, JSON) write them; other formats ignore them. To
write other attributes, or none, pass ``vertex_attributes`` and ``edge_attributes`` as dicts or
functions returning dicts, and ``graph_attributes`` as a dict; an explicit option replaces the stored
attributes:

.. code-block:: python

    text = jg.graph_to_string(
        g,
        "graphml",
        vertex_id=str,
        vertex_attributes={"a": {"color": "blue"}},
        edge_attributes=lambda e: {"kind": "rail"},
        graph_attributes={"title": "other"},
    )

Values are written as ``bool``, ``int``, ``float`` or ``str``, and any other value as its ``str``. On
reading, values are converted to ``bool``, ``int``, ``float`` or ``str`` according to the type
declared in the document. With ``sparse=True`` or a ``vertex_factory``, the identifiers of the vertices
in the file are kept in ``h.graph_attrs["vertex_ids"]``. For TSPLIB files ``h.graph_attrs["tsplib"]``
holds the specification, the coordinates and the tour; neither is written back.

Errors
======

Malformed documents, unknown formats and unsupported options raise :class:`GraphError`; a missing
file raises ``OSError``. Exceptions raised by your own callbacks (``vertex_id``,
``vertex_factory``, attribute functions) propagate unchanged.
