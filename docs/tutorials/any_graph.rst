.. _tutorials/any_graph:

.. currentmodule:: jgrapht

Any-hashable graph tutorial
===========================

The |Bindings| allow the creation of graphs which can have any Python hashable as vertices and edges.
Such graphs also provide explicit support for associating attributes/properties with vertices and edges 
in the graph.


Creating a graph with any hashable as vertices and edges
--------------------------------------------------------

.. nbplot::

  >>> import jgrapht
  >>> g = jgrapht.create_graph(directed=True, 
  >>>                          weighted=True, 
  >>>                          allowing_self_loops=False, 
  >>>                          allowing_multiple_edges=False, 
  >>>                          any_hashable=True)

The factory function accepts two additional parameters, called `vertex_supplier` and `edge_supplier`. These are callable instances
whose job is to return a new object whenever the graph wants to create a vertex or an edge. When not explicitly provided, the 
default implementation creates new :py:class:`object` instances. A few basic suppliers are also provided in :py:mod:`jgrapht.utils`, but 
any callable can do the job.

Adding vertices
---------------

Vertices are added by calling method :py:meth:`.Graph.add_vertex`. The user can provide
explicitly the vertex as a parameter:

.. nbplot::

  >>> g.add_vertex('v0')

It is also possible to let the graph create automatically one. This will be done using the vertex supplier 
associated with the graph.

.. nbplot::

  >>> obj = g.add_vertex()

The newly created vertex is returned by the call, in order to be used when adding edges. In this 
case it will be an instance of :py:class:`object`. Let us add two more string vertices: 

.. nbplot::

  >>> g.add_vertex('v1')
  >>> g.add_vertex('v2')

Vertex set
----------

Now the graph contains 4 vertices. You can find how many vertices the graph contains using,

.. nbplot::

  >>> len(g.vertices)

The property :py:attr:`.Graph.vertices` returns the set of vertices, which is also 
helpful in order to iterate over them.

.. nbplot::

  >>> for v in g.vertices: 
  >>>     print ('Vertex {}'.format(v))

The above should print three string vertices and one object instance.

Adding edges
------------

Edges are pairs of vertices, either ordered or unordered, depending on whether the graph is
directed or undirected. In the propert graph, edges can be any hashable. If not explicitly provided
the edge is automatically created by the graph using the edge supplier.

.. nbplot::

  >>> e1 = g.add_edge('v0', 'v1')

The call above creates a new edge from vertex 'v0' to vertex 'v2' and returns it.
Multiple edges can be created in one go by using,

.. nbplot::

  >>> g.add_edges_from([('v0', 'v2'), ('v0', obj)])

The method returns the newly created edges. Note also that it is possible to provide the edge
representation explicitly using,

.. nbplot::

  >>> g.add_edge('v2', obj, edge='e1')

In the example above we explicitly request to add edge `e1` in the graph. If the graph already 
contains such an edge, the graph is not altered.


Edge information
----------------

Using the edge we can retrieve the underlying information of the edge such as its source
and its target. While in undirected graphs there is no source or target, we use the same naming scheme
to keep a uniform interface. This is very helpful in order to implement algorithms which work both 
in directed and undirected graphs. Let us now read the edge source and target from the graph,

.. nbplot::

  >>> print ('Edge {} has source {}'.format('e1', g.edge_source('e1')))
  >>> print ('Edge {} has target {}'.format('e1', g.edge_target('e1')))

Graphs can be weighted or unweighted. In the case of unweighted graphs, method 
:py:meth:`.Graph.get_edge_weight()` always returns 1.0 . This allows algorithms designed for weighted 
graphs to also work in unweighted ones. Here is how to read the weight of an edge,

.. nbplot::
  
  >>> print ('Edge {} has weight {}'.format(e1, g.get_edge_weight('e1')))

If the graph is weighted, the edge weight can be adjusted using method :py:meth:`.Graph.set_edge_weight()`.
The user can also provide the weight directly when adding the edge to the graph,

.. nbplot::

  >>> e2 = g.add_edge(obj, 'v2', weight=10.0)

Care must be taken to not try to adjust the weight if the graph is unweighted. In such a case a 
:py:class:`ValueError` is raised.


Edge set
--------

Edges can be iterated using the set returned by :py:attr:`.Graph.edges`,

.. nbplot::

  >>> for e in g.edges: 
  >>>     print ('Edge {} has source {}'.format(e, g.edge_source(e)))
  >>>     print ('Edge {} has target {}'.format(e, g.edge_target(e)))

The same effect can be performed using the helper method :py:meth:`.Graph.edge_tuple()` which 
returns a tuple containing the source, the target, and the weight of the edge. If
the graph is unweighted, the weight returned is always 1.0.

.. nbplot::

  >>> for e in g.edges: 
  >>>     print ('Edge {}'.format(g.edge_tuple(e)))

Finding the number of edges can be performed by executing,

.. nbplot::

  >>> len(g.edges)

Graph attributes
----------------

Besides the graph structure, users can associate attributes/properties with the graph itself, with 
the vertices and the edges. All such graphs follow the :py:class:`jgrapht.types.AttributesGraph`
interface. It defines three dictionaries keyed using the correspoding graph elements which perform
the necessary type checking in order to ensure existence.

Let us associate a label with each vertex of the graph:

.. nbplot::

  >>> g.vertex_attrs['v0']['label'] = 'vertex 0'
  >>> g.vertex_attrs['v1']['label'] = 'vertex 1'
  >>> g.vertex_attrs['v2']['label'] = 'vertex 2'
  >>> g.vertex_attrs[obj]['label'] = 'object vertex'

The same can be done with the edges: 

.. nbplot::

  >>> for e in g.edges:
  >>>     g.edge_attrs[e]['label'] = str(e)

The special attribute/property `weight` for the edges is respected. This means that writing this 
attribute requires the graph to be weighted.

.. nbplot::

  >>> print(g.edge_attrs[e2]['weight'])
  >>> g.edge_attrs[e2]['weight'] = 16.0

Attributes/properties are respected on all importers and exporters (whose format supports attributes/properties).
