.. _graph:

Graphs
******

.. currentmodule:: jgrapht

Two graph classes are available. Every algorithm accepts either. See the
:doc:`introduction` for what a graph is here, and the tutorials for :doc:`../tutorials/graph` and
:doc:`../tutorials/sparse_graph`.

* :class:`Graph` is mutable; both vertices and edges are arbitrary hashable
  Python objects. If no edge object is given to :meth:`Graph.add_edge`, a fresh
  integer is used.
* :class:`SparseGraph` is a compact, immutable graph on the integer vertices
  ``0..n`` whose edges are the integers ``0..m`` in input order (only edge
  weights can be changed).

.. _attributes:

Attributes
==========

A graph can store attributes for its vertices, its edges and for itself. They are dicts that you read
and change directly:

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph()
  >>> g.add_vertex('a'); g.add_vertex('b')
  True
  True
  >>> e = g.add_edge('a', 'b')
  >>> g.vertex_attrs['a']['color'] = 'red'
  >>> g.edge_attrs[e]['kind'] = 'road'
  >>> g.graph_attrs['name'] = 'demo'
  >>> g.vertex_attrs['a'], g.edge_attrs[e], g.graph_attrs
  ({'color': 'red'}, {'kind': 'road'}, {'name': 'demo'})

* ``graph.vertex_attrs[v]`` is the live ``dict`` of the vertex ``v``, and ``graph.edge_attrs[e]`` that
  of the edge ``e``. It is created empty the first time it is asked for, so storing a value is just
  ``graph.vertex_attrs[v]["key"] = value``. Asking for a vertex or edge that is not in the graph
  raises :class:`GraphError`. ``graph.graph_attrs`` is a ``dict``.
* ``vertex_attrs`` and ``edge_attrs`` are mappings of the vertices (edges) that *have* attributes:
  ``len``, ``in``, iteration, ``keys()``, ``values()``, ``items()`` and ``get`` only see those, while
  ``attrs[v]`` works for every vertex. ``attrs[v] = {...}`` replaces the attributes of ``v`` and
  ``del attrs[v]`` removes them.
* Removing a vertex or an edge removes its attributes. A :class:`SparseGraph` has them too, keyed by
  the vertex and edge numbers.
* The weight of an edge is not an attribute: use ``edge_weight`` and ``set_edge_weight``.
* Attributes are not used by the algorithms, but you can read them from callbacks, for example from
  an A\* heuristic.
* **Copies.** The functions that copy a graph (:func:`copy_graph`, :func:`induced_subgraph`,
  :func:`edge_subgraph`, :func:`as_undirected`, :func:`reverse_edges`, :func:`as_weighted`,
  :func:`as_unweighted`) copy the attribute dicts, so the result is independent of the original; the
  values are shared, not copied. :func:`graph_union` merges them, and where both graphs have the same
  attribute the value of the second graph is used. Graphs that algorithms and generators create start
  without attributes.
* **Read-only wrapper.** The attributes of an :func:`as_unmodifiable` graph are read-only: its
  dicts are ``types.MappingProxyType`` views.
* **Files and other packages.** Importers fill the attributes and exporters write them (see
  :doc:`io/index`), and :mod:`jgrapht.convert` copies them to and from NetworkX and pydot.

.. autoclass:: Graph
   :members:
   :special-members: __len__, __contains__, __iter__

.. autoclass:: SparseGraph
   :members:
   :special-members: __len__, __contains__

.. autoclass:: GraphPath
   :members:

.. autoexception:: GraphError
