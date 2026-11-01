.. _algorithms/index:

Algorithms
**********

.. currentmodule:: jgrapht

|Project| contains a large collection of graph algorithms. They are plain functions of the
:mod:`jgrapht` module, grouped here by family. Every function accepts a :class:`Graph` or a
:class:`SparseGraph`, and vertices and edges in results are the objects of the graph passed in.
Algorithms that come in several variants take the variant as a string, for example
``shortest_path(g, s, t, algorithm="bellman_ford")``.

.. toctree::
   :maxdepth: 1

   shortestpaths
   connectivity
   spanning
   cycles
   coloring
   clustering
   scoring
   linkprediction
   planar
   cuts
   matching
   flow
   isomorphism
   tour
   cliques
   decompositions
   drawing
   transformations
   graphclasses
