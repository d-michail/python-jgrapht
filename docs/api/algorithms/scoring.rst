.. _algorithms/scoring:

Centrality and scores
*********************

.. currentmodule:: jgrapht

Vertex scores: degree, closeness, harmonic, betweenness, PageRank, eigenvector and Katz
centrality, coreness and clustering coefficients. Each returns a dict keyed by vertex.
:func:`betweenness_centrality` normalizes undirected graphs by the number of unordered pairs, so
a vertex on every shortest path scores 1, whereas :func:`exact_betweenness_centrality` divides by
``(n - 1)(n - 2)`` and tops out at one half; see their docstrings.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.star_graph(5)
  >>> jg.degree_centrality(g)
  {0: 4.0, 3: 1.0, 4: 1.0, 1: 1.0, 2: 1.0}
  >>> jg.betweenness_centrality(g)[0]
  1.0
  >>> {v: round(x, 3) for v, x in jg.closeness_centrality(g).items()}
  {2: 0.571, 4: 0.571, 3: 0.571, 1: 0.571, 0: 1.0}
  >>> jg.coreness(g)
  {1: 1, 2: 1, 3: 1, 4: 1, 0: 1}

Functions
=========

.. autofunction:: degree_centrality
.. autofunction:: closeness_centrality
.. autofunction:: harmonic_centrality
.. autofunction:: betweenness_centrality
.. autofunction:: edge_betweenness_centrality
.. autofunction:: exact_betweenness_centrality
.. autofunction:: pagerank
.. autofunction:: eigenvector_centrality
.. autofunction:: katz_centrality
.. autofunction:: coreness
.. autofunction:: local_clustering_coefficients
.. autofunction:: average_clustering_coefficient
.. autofunction:: global_clustering_coefficient
.. autofunction:: count_triangles
