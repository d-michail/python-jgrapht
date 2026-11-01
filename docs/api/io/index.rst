.. _io/index:

Input and output
****************

.. currentmodule:: jgrapht

Graphs can be read from and written to files and strings, in the formats CSV, DIMACS, DOT, GEXF, GML,
graph6/sparse6/digraph6, GraphML and JSON, written as LEMON, sparse matrices and Visio CSV, and read
from TSPLIB. The format is chosen by name and configured with keyword options. **Unknown options, and
options a format cannot use, raise** :class:`GraphError`. See the :doc:`tutorial <../../tutorials/io>`
for worked examples.

* :doc:`importers` -- :func:`read_graph` and :func:`parse_graph`;
* :doc:`exporters` -- :func:`write_graph` and :func:`graph_to_string`;
* :doc:`events` -- streaming a document as events instead of building a graph;
* :doc:`tsplib` -- tour files and TSPLIB distances.

Formats
=======

======== ====== ====== ==========================================================================
Format   Read   Write  Notes
======== ====== ====== ==========================================================================
csv      yes    yes    ``variant``: ``edge_list``, ``adjacency_list`` (default), ``matrix``
dimacs   yes    yes    ``variant`` (write): ``max_clique`` (default), ``coloring``, ``shortest_path``
dot      yes    yes    attributes, graph id
gexf     yes    yes    attributes, metadata
gml      yes    yes    attributes, labels
graph6   yes    yes    graph6, sparse6 and digraph6 (``variant`` on write)
graphml  yes    yes    attributes, labels, weights
json     yes    yes    attributes, custom collection names
tsplib   yes    no     coordinate based instances, tours, always weighted
lemon    no     yes    LEMON graph format
matrix   no     yes    sparse adjacency / Laplacian matrices
visio    no     yes    Visio CSV
======== ====== ====== ==========================================================================

.. toctree::
   :maxdepth: 1
   :hidden:

   importers
   exporters
   events
   tsplib
