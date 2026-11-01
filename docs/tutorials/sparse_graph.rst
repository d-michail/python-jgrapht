.. _tutorials/sparse_graph:

The SparseGraph class
=====================

.. currentmodule:: jgrapht

:class:`~jgrapht.SparseGraph` is a compact, immutable graph. It has two restrictions:

* the graph cannot be modified, so it is **bulk-loaded** from an edge list;
* vertices are the integers ``0..n-1`` and edges the integers ``0..m-1``, numbered in the order of
  the edge list.

In return it uses little memory and is usually faster, because its representation is friendly to
modern caches. It is the right choice when you load a graph once and run algorithms on it.

Creating a sparse graph
-----------------------

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
  >>> g = jg.SparseGraph(5, edges, directed=True)
  >>> g
  SparseGraph(directed=True, weighted=False, vertices=5, edges=5)

The first argument is the number of vertices. For a weighted graph give the weights, one per edge.

.. code-block:: pycon

  >>> w = jg.SparseGraph(5, edges, directed=True, weights=[1.0, 4.0, 2.0, 1.0, 3.0])
  >>> w.weighted
  True
  >>> jg.shortest_path(w, 0, 4)
  GraphPath(vertices=[0, 1, 3, 4], weight=6.0)

Queries
-------

Queries return integers, and the edge ``i`` is the ``i``-th pair of the edge list.

.. code-block:: pycon

  >>> g.vertex_count(), g.edge_count()
  (5, 5)
  >>> g.edge_source(3), g.edge_target(3)
  (2, 3)
  >>> g.out_edges_of(0)
  [0, 1]
  >>> g.neighbors_of(3)
  [4, 1, 2]

The only mutation is changing a weight:

.. code-block:: pycon

  >>> w.set_edge_weight(0, 10.0)
  >>> jg.shortest_path(w, 0, 4).edges
  [1, 3, 4]

From and to other graphs
------------------------

.. code-block:: pycon

  >>> h = jg.Graph(directed=True)
  >>> for v in range(3):
  ...     _ = h.add_vertex(v)
  >>> _ = h.add_edge(0, 1); _ = h.add_edge(1, 2)
  >>> jg.parse_graph(jg.graph_to_string(h, 'csv', variant='edge_list', vertex_id=str), 'csv',
  ...                variant='edge_list', directed=True, sparse=True, vertex_factory=None)
  SparseGraph(directed=True, weighted=False, vertices=3, edges=2)

Readers take ``sparse=True`` to build a sparse graph directly, and every generator accepts
``sparse=True``. Because a sparse graph is a multigraph by type, algorithms that insist on simple
graphs (VF2 isomorphism, graph6 export, ...) reject it; see their documentation.

