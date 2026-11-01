.. _algorithms/coloring:

Coloring
********

.. currentmodule:: jgrapht

Vertex colorings by greedy, largest-degree-first, smallest-degree-last, saturation-degree and
exact backtracking algorithms, and a checker for proper colorings. A coloring is returned as
``(number_of_colors, {vertex: color})``.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.named_graph('petersen')
  >>> count, colors = jg.coloring(g)
  >>> count
  3
  >>> jg.is_proper_coloring(g, colors)
  True

Functions
=========

.. autofunction:: coloring
.. autofunction:: is_proper_coloring
