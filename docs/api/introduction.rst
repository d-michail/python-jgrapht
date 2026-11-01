.. _introduction:

Introduction
************

.. currentmodule:: jgrapht

|Project| is a library of graph data structures and algorithms. This package, the |Bindings|, is
a native Python extension backed by the `jgrapht <https://crates.io/crates/jgrapht>`__ Rust crate, a
port of the Java `JGraphT <https://jgrapht.org>`_ library; it needs no Java virtual machine.
The API reference is organised as follows:

* :doc:`graph` -- the two graph classes, paths and errors;
* :doc:`generators` -- structured, random and named graphs, and flow instances;
* :doc:`derived` -- copies, subgraphs, unions and other derived graphs;
* :doc:`traversals`, :doc:`properties` and :doc:`metrics`;
* :doc:`algorithms/index` -- one page per family of algorithms;
* :doc:`io/index` -- reading and writing graph files;
* :doc:`drawing` -- drawing graphs with matplotlib;
* :doc:`convert` -- converting to and from NetworkX.

What a graph is
===============

A graph :math:`G = (V, E)` has vertices and edges. In this library a graph can be

* **directed**, where an edge :math:`(u, v)` is an ordered pair, or **undirected**, where an edge
  :math:`\{u, v\}` is an unordered pair;
* **weighted**, where each edge carries a floating point weight, or **unweighted**, where all
  weights are 1.0;
* allowed to contain **self-loops** :math:`(v, v)` and **multiple edges** between the same
  endpoints, or not.

All information about the graph is queried through the graph object: given an edge you ask the
graph for its source, target and weight; given a vertex, for its incident edges.

Two graph classes
=================

:class:`Graph`
  A mutable graph whose vertices and edges are **any hashable Python objects**: strings, numbers,
  tuples, your own objects. If you add an edge without giving it an object, the graph uses a fresh
  integer. You choose the flags when you create it (``directed``, ``weighted``,
  ``allow_self_loops``, ``allow_multiple_edges``).

:class:`SparseGraph`
  An immutable, compact graph on the integer vertices ``0..n-1`` and the integer edges ``0..m-1``,
  numbered in the order of the edge list it was built from. It is smaller and faster, and best
  suited to loading a graph once and running algorithms on it. Only edge weights can change. It
  always allows self-loops and multiple edges.

Every algorithm accepts either class and returns vertices and edges as the objects of the graph you
passed in.

Attributes
==========

Neither class stores vertex or edge attributes; keep them in dictionaries keyed by the vertex or
edge, which is what Python does well. Attributes are supported when :doc:`reading and writing graph
files <io/index>`: you pass dictionaries or functions when exporting, and ask for a dictionary of
attributes when importing.

Results
=======

Algorithms return plain Python values (dicts, lists, tuples) or small result objects:
:class:`GraphPath`, :class:`Matching`, :class:`MaximumFlow`, :class:`MinimumCut` and a few others.
Something that does not exist is ``None``, never an infinite weight or a sentinel: an unreachable
vertex, a missing path, a graph with no cycle.

Errors and callbacks
====================

Failures reported by the library (a vertex that is not in the graph, a graph of the wrong kind for
an algorithm, malformed input) raise :class:`GraphError`, a subclass of :class:`ValueError`. Some
functions take Python callbacks, for example an A\* heuristic, isomorphism predicates or the
attribute functions of the exporters. An exception raised inside a callback stops the algorithm and
is re-raised, unchanged, to the caller.

Where to go next
================

The :doc:`tutorials <../tutorials/index>` build graphs step by step, and the gallery of
:doc:`examples <../auto_examples/index>` shows complete programs.
