.. _algorithms/linkprediction:

Similarity and link prediction
******************************

.. currentmodule:: jgrapht

Link prediction scores between pairs of vertices (common neighbors, Jaccard, Adamic-Adar,
preferential attachment, ...), SimRank, and the tree edit distance.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.named_graph('petersen')
  >>> jg.link_score(g, 0, 1, 'common_neighbors')
  0.0
  >>> jg.predict_links(g, 0, 'common_neighbors')[:3]
  [(3, 1.0), (4, 1.0), (5, 1.0)]

Functions
=========

.. autofunction:: link_score
.. autofunction:: predict_links
.. autofunction:: simrank
.. autofunction:: tree_edit_distance
