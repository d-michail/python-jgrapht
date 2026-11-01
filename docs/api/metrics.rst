.. _metrics:

Metrics
*******

.. currentmodule:: jgrapht

Distance based metrics: eccentricities, diameter, radius, center, periphery and girth.
Weighted graphs use the edge weights; the metrics of a disconnected graph are infinite.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.path_graph(5)
  >>> jg.diameter(g), jg.radius(g)
  (4.0, 2.0)
  >>> jg.graph_center(g)
  [2]
  >>> jg.eccentricities(g)
  {0: 4.0, 1: 3.0, 2: 2.0, 3: 3.0, 4: 4.0}
  >>> jg.girth(jg.named_graph('petersen'))
  5

Functions
=========

.. autofunction:: diameter
.. autofunction:: radius
.. autofunction:: eccentricities
.. autofunction:: graph_center
.. autofunction:: tree_center
.. autofunction:: graph_periphery
.. autofunction:: graph_pseudo_periphery
.. autofunction:: girth
