.. _algorithms/clustering:

Clustering
**********

.. currentmodule:: jgrapht

Community detection and graph clustering (label propagation, greedy modularity, Girvan-Newman,
k-spanning-tree clustering) and the modularity measure. Clusterings are lists of vertex lists.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.named_graph('zachary_karate_club')
  >>> clusters = jg.greedy_modularity_clustering(g)
  >>> len(clusters)
  3
  >>> round(jg.modularity(g, clusters), 3)
  0.381

Functions
=========

.. autofunction:: label_propagation_clustering
.. autofunction:: k_spanning_tree_clustering
.. autofunction:: girvan_newman_clustering
.. autofunction:: greedy_modularity_clustering
.. autofunction:: modularity
