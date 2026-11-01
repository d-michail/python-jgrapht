.. _algorithms/drawing:

Layouts
*******

.. currentmodule:: jgrapht

Two-dimensional layouts that assign coordinates to vertices (circular, random,
Fruchterman-Reingold). To draw a graph with these positions see :doc:`../drawing`, or pass them to
any other plotting package.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.ring_graph(4)
  >>> pos = jg.circular_layout(g)
  >>> {v: (round(x, 2), round(y, 2)) for v, (x, y) in pos.items()}
  {3: (-0.0, -1.0), 0: (1.0, 0.0), 1: (0.0, 1.0), 2: (-1.0, 0.0)}

Functions
=========

.. autofunction:: circular_layout
.. autofunction:: random_layout
.. autofunction:: layout_2d
.. autofunction:: rescale_layout
.. autofunction:: fruchterman_reingold_layout
