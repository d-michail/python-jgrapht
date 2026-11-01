.. _drawing:

Drawing
*******

.. currentmodule:: jgrapht.drawing

The :mod:`jgrapht.drawing` module draws a graph with `matplotlib <https://matplotlib.org>`_. It takes
the positions of the vertices from a layout, such as :func:`~jgrapht.circular_layout` or
:func:`~jgrapht.fruchterman_reingold_layout`, and works with :class:`~jgrapht.Graph`,
:class:`~jgrapht.SparseGraph` and :func:`~jgrapht.as_unmodifiable` wrappers.

matplotlib is not installed with the package. Install it with ``pip install matplotlib``, or install
the package with the ``plot`` extra, ``pip install jgrapht[plot]``.

:func:`draw` does everything at once. :func:`draw_edges`, :func:`draw_vertices`,
:func:`draw_vertex_labels` and :func:`draw_edge_labels` draw the parts separately, for example to
give some vertices a different color or to draw onto a figure that you already have.

Example
=======

.. code-block:: python

  import matplotlib.pyplot as plt
  import jgrapht as jg
  from jgrapht import drawing

  g = jg.complete_bipartite_graph(2, 3)
  pos = jg.fruchterman_reingold_layout(g, seed=1)
  drawing.draw(g, pos, vertex_color="orange")
  plt.show()

Default positions
=================

If ``pos`` is omitted, a :func:`~jgrapht.fruchterman_reingold_layout` with a fixed seed is used, so
that repeated calls draw the same picture.

Self-loops and parallel edges
=============================

A self-loop is drawn as a ring around its vertex. Parallel edges are drawn on top of each other. When
a directed graph has edges in both directions between two vertices they are drawn as two curves.

Functions
=========

.. autofunction:: draw
.. autofunction:: draw_vertices
.. autofunction:: draw_edges
.. autofunction:: draw_vertex_labels
.. autofunction:: draw_edge_labels
