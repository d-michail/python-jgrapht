.. JGraphT documentation master file.

The JGraphT library
===================

Release v\ |version|.

Python bindings for the `jgrapht <https://crates.io/crates/jgrapht>`__ Rust crate.

JGraphT is a highly efficient graph library containing state-of-the-art graph data structures and
a multitude of sophisticated graph algorithms. It has been developed for many years in Java and is
used in production both in research and in industry. The ``jgrapht`` crate is its port to Rust, and the
|Bindings| is a native Python extension built on it with `PyO3 <https://pyo3.rs>`_. It needs no Java
virtual machine.

Backend version v\ |BackendVersion|.

Audience
--------

Anyone who needs graphs or networks in their everyday work: engineers and researchers from industry
or academia, who want a fast library with a broad set of algorithms and a Pythonic interface.

At a glance
-----------

* A mutable :class:`~jgrapht.Graph` whose vertices and edges are **any hashable objects**, and a
  compact immutable :class:`~jgrapht.SparseGraph` on the integers ``0..n-1``. Every algorithm works
  with both.
* About two hundred **algorithms**: shortest paths, spanning trees, flows and cuts, matchings,
  connectivity, cycles and tours, coloring, cliques, isomorphism, centrality, clustering, planarity,
  layouts and more.
* **Generators** for structured, random and famous graphs.
* **Reading and writing** CSV, DIMACS, DOT, GEXF, GML, graph6, GraphML, JSON, TSPLIB and more, with
  attributes.

.. code-block:: python

    import jgrapht as jg

    g = jg.Graph(weighted=True)
    for v in "abcd":
        g.add_vertex(v)
    g.add_edge("a", "b", weight=1.0)
    g.add_edge("b", "c", weight=2.0)
    g.add_edge("c", "d", weight=1.0)
    jg.shortest_path(g, "a", "d")   # GraphPath(vertices=['a', 'b', 'c', 'd'], weight=4.0)

Development
-----------

Development happens in the following places.

 * https://github.com/d-michail/python-jgrapht-rs
 * https://github.com/d-michail/jgrapht-rs
 * https://github.com/jgrapht/jgrapht


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: JGraphT

   install
   tutorials/index
   api/index
   license
   citing
   credits

.. toctree::
   :maxdepth: 2
   :caption: Example galleries

   auto_examples/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
