.. _convert:

Conversions
***********

.. currentmodule:: jgrapht.convert

The :mod:`jgrapht.convert` module converts graphs to and from `NetworkX <https://networkx.org>`_
and `pydot <https://github.com/pydot/pydot>`_ (the Python interface to Graphviz DOT). Only the
structure, the edge weights and the attributes (:ref:`attributes`) are converted. The attributes of
the vertices, edges and graph correspond to the attributes of the nodes, edges and graph in NetworkX
and pydot. An edge weight is not an attribute of a jgrapht graph, so the attribute called
``weight`` is the edge weight on the other side. The attribute dicts are copied, never shared.

Neither package is installed with this one. Install them with ``pip install networkx`` and
``pip install pydot``, or install the package with the ``networkx`` or ``pydot`` extra, for example
``pip install jgrapht[networkx]``.

Example
=======

.. code-block:: pycon

  >>> import networkx as nx
  >>> import jgrapht as jg
  >>> from jgrapht.convert import from_nx, to_nx
  >>> g = from_nx(nx.petersen_graph())
  >>> jg.girth(g)
  5
  >>> to_nx(g).number_of_edges()
  15

A graph can be turned into DOT text, or into an image if Graphviz is installed:

.. code-block:: pycon

  >>> from jgrapht.convert import to_pydot
  >>> dot = to_pydot(jg.path_graph(3))
  >>> dot.write_png("path.png")  # needs Graphviz

NetworkX
========

pydot
=====

See :func:`to_pydot` and :func:`from_pydot` below.

Functions
=========

.. autofunction:: to_nx
.. autofunction:: from_nx
.. autofunction:: to_pydot
.. autofunction:: from_pydot
