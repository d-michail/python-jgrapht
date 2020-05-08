.. _tutorial:

Tutorial
========

This guide will help you start using the library.

Creating a graph
----------------

Let us start by creating a graph::

  import jgrapht

  g = jgrapht.create_graph(directed=True, weighted=True)

The graph is a collection of vertices (aka nodes) and edges. In python-jgrapht vertices and
edges are always long integers.

Adding vertices
---------------

Vertices are added by calling method :py:meth:`.Graph.add_vertex` and providing the vertex
identifier as a parameter::

  g.add_vertex(0)

The method returns `True` if the vertex is added and `False` if the 
vertex was already a member of the graph. Multiple vertices can also be added using any
iterable::

  g.add_vertices_from([1, 2])

Now the graph should contain 3 vertices. You can find the number of vertices using::

  len(g.vertices())

The method :py:meth:`.Graph.vertices()` returns the set of vertices, which is also 
helpful in order to iterate over them::

  for v in g.vertices(): 
      print ('Vertex {}'.format(v))

Adding edges
------------

Edges are pair of vertices, either ordered or unordered, depending on the type of the graph. 
In python-jgrapht edges are also identified using long integers. These edge identifiers are 
automatically given to the edge when they are first added to the graph::

  e1 = g.add_edge(0, 1)

The call above creates a new edge from vertex 0 to vertex 1 and returns its identifier. Using this 
edge identifier we can retrieve the underlying information of the edge such as its source and its
target. While in undirected graphs there is no source or target, we use the same naming scheme
to keep a uniform interface. This is very helpful in order to implement algorithms which work both 
in directed and undirected graphs. Let us now read the edge source and target from the graph::

  print ('Edge {} has source {}'.format(e1, g.edge_source(e1)))
  print ('Edge {} has target {}'.format(e1, g.edge_target(e1)))

Graphs in python-jgrapht can be weighted or unweighted. In the case of unweighted graphs, method 
:py:meth:`.Graph.get_edge_weight()` always returns 1.0 . This allows algorithms designed for weighted 
graphs to also work in unweighted ones. Here is how to read the weight of an edge::

  print ('Edge {} has weight {}'.format(e, g.get_edge_weight(e1)))

If the graph is weighted, the edge weight can be adjusted using method :py:meth:`.Graph.set_edge_weight()`.
The user can also provide the weight directly when adding the edge to the graph::

  e2 = g.add_edge(1, 2, weight=10.0)

Care must be taken to not try to adjust the weight if the graph is unweighted. In such a case a 
:py:class:`.UnsupportedOperationError` is raised.

Edges can be iterated using the set returned by method :py:meth:`.Graph.edges()`::

  for e in g.edges(): 
      print ('Edge {} has source {}'.format(e, g.edge_source(e)))
      print ('Edge {} has target {}'.format(e, g.edge_target(e)))

Navigation
----------

When implementing graph algorithms one of the most common operation that is required is to 
find the neighbors of a vertex. 









TODO


