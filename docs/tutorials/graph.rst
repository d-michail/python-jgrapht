.. _tutorials/graph:

The Graph class
===============

.. currentmodule:: jgrapht

:class:`~jgrapht.Graph` is the general purpose graph. Vertices and edges can be any hashable
object, and the graph can be modified at any time.

Choosing the kind of graph
--------------------------

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.Graph(directed=True, weighted=True, allow_self_loops=False, allow_multiple_edges=False)
  >>> g.directed, g.weighted, g.allow_self_loops, g.allow_multiple_edges
  (True, True, False, False)

A graph that does not allow self-loops or multiple edges refuses them: adding such an edge raises
:class:`~jgrapht.GraphError` (for a duplicate edge, :meth:`~jgrapht.Graph.add_edge` returns ``None``).

Vertices
--------

.. code-block:: pycon

  >>> g.add_vertex('v0')
  True
  >>> g.add_vertex('v0')
  False
  >>> g.add_vertex(1)
  True
  >>> g.add_vertex(('tuple', 1))
  True
  >>> g.new_vertex()
  0
  >>> 'v0' in g, len(g)
  (True, 4)
  >>> g.vertices()
  ['v0', 1, ('tuple', 1), 0]

:meth:`~jgrapht.Graph.add_vertex` returns ``False`` for a vertex the graph already has.
:meth:`~jgrapht.Graph.new_vertex` creates a fresh integer vertex that is not yet in the graph and returns it.

Edges
-----

.. code-block:: pycon

  >>> e1 = g.add_edge('v0', 1, weight=3.0)
  >>> e2 = g.add_edge(1, ('tuple', 1), edge='my-edge', weight=1.5)
  >>> e1, e2
  (0, 'my-edge')
  >>> g.edge_source(e2), g.edge_target(e2), g.edge_weight(e2)
  (1, ('tuple', 1), 1.5)
  >>> g.set_edge_weight(e1, 4.0)
  >>> g.edge_weight(e1)
  4.0

An edge is identified by its object: by default a fresh integer, or anything hashable you give with
``edge=``. In a directed graph the order of the endpoints matters.

Incidence
---------

.. code-block:: pycon

  >>> g.out_edges_of(1), g.in_edges_of(1)
  (['my-edge'], [0])
  >>> g.out_degree_of('v0'), g.in_degree_of(1)
  (1, 1)
  >>> g.neighbors_of(1)
  ['v0', ('tuple', 1)]
  >>> g.edges_between('v0', 1)
  [0]

Removing
--------

.. code-block:: pycon

  >>> g.remove_edge(e1)
  True
  >>> g.remove_vertex(('tuple', 1))
  True
  >>> g
  Graph(directed=True, weighted=True, vertices=3, edges=0)

Removing a vertex removes its incident edges.

Attributes
----------

Vertices, edges and the graph itself can carry attributes: dicts that the library stores for you. See
:ref:`attributes` for the details.

.. code-block:: pycon

  >>> g.vertex_attrs['v0']['colour'] = 'red'
  >>> g.vertex_attrs[1].update(colour='blue', size=3)
  >>> g.graph_attrs['name'] = 'demo'
  >>> g.vertex_attrs['v0']
  {'colour': 'red'}
  >>> len(g.vertex_attrs)
  2

They are written by the exporters and set by the importers:

.. code-block:: pycon

  >>> text = jg.graph_to_string(g, 'json', vertex_id=str)
  >>> 'red' in text
  True
