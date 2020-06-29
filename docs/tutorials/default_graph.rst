.. _tutorials/default_graph:

.. currentmodule:: jgrapht

Graph tutorial
==============

This guide will help you start using the library.

Creating a graph
----------------

Let us start by creating a graph, which is a collection of vertices (aka nodes) and edges. 
We will use the default graph which uses integers to represent vertices and edges.

.. nbplot::

  >>> import jgrapht
  >>> g = jgrapht.create_graph(directed=True, weighted=True, allowing_self_loops=False, allowing_multiple_edges=False)

This is the most general call. Sensible defaults are also provided, thus someone can create
a graph simply by calling :py:meth:`jgrapht.create_graph()`. 


Adding vertices
---------------

Vertices are added by calling method :py:meth:`.Graph.add_vertex`. The user can provide
explicitly the vertex identifier as a parameter:

.. nbplot::

  >>> g.add_vertex(0)

It is also possible to let the graph create automatically one:

.. nbplot::

  >>> g.add_vertex()

The newly created vertex identifier is returned by the call, in order to be used when 
adding edges. Multiple vertices can also be added using any iterable.

.. nbplot::

  >>> g.add_vertices_from([2, 3])

Vertex set
----------

Now the graph contains 4 vertices.  You can find how many vertices the graph contains using,

.. nbplot::

  >>> len(g.vertices)

The property :py:attr:`.Graph.vertices` returns the set of vertices, which is also 
helpful in order to iterate over them.

.. nbplot::

  >>> for v in g.vertices: 
  >>>     print ('Vertex {}'.format(v))


Adding edges
------------

Edges are pairs of vertices, either ordered or unordered, depending on whether the graph is
directed or undirected. In the default graph, edges are represented using integers.
These edges are automatically created by the graph.

.. nbplot::

  >>> e1 = g.add_edge(0, 1)

The call above creates a new edge from vertex 0 to vertex 1 and returns its representation.
Multiple edges can be created in one go by using,

.. nbplot::

  >>> g.add_edges_from([(0, 2), (1, 2)])

The method returns the newly created edges. Note also that it is possible to provide the edge
representation explicitly using,

.. nbplot::

  >>> g.add_edge(0, 1, edge=5)

In the example above we explicitly request to add edge `5` in the graph. If the graph already 
contains such an edge, the graph is not altered.


Edge information
----------------

Using the edge we can retrieve the underlying information of the edge such as its source
and its target. While in undirected graphs there is no source or target, we use the same naming scheme
to keep a uniform interface. This is very helpful in order to implement algorithms which work both 
in directed and undirected graphs. Let us now read the edge source and target from the graph,

.. nbplot::

  >>> print ('Edge {} has source {}'.format(e1, g.edge_source(e1)))
  >>> print ('Edge {} has target {}'.format(e1, g.edge_target(e1)))

Graphs can be weighted or unweighted. In the case of unweighted graphs, method 
:py:meth:`.Graph.get_edge_weight()` always returns 1.0 . This allows algorithms designed for weighted 
graphs to also work in unweighted ones. Here is how to read the weight of an edge,

.. nbplot::
  
  >>> print ('Edge {} has weight {}'.format(e1, g.get_edge_weight(e1)))

If the graph is weighted, the edge weight can be adjusted using method :py:meth:`.Graph.set_edge_weight()`.
The user can also provide the weight directly when adding the edge to the graph,

.. nbplot::

  >>> e2 = g.add_edge(1, 3, weight=10.0)

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

Graph types
-----------

The type of the graph can be queried during runtime using :py:attr:`.Graph.type` which
returns instances of :py:class:`.GraphType`. This allows algorithms to alter their behavior
based on the actual graph that they are running on. The following properties can be 
queried,

.. nbplot::
 >>> g.type.directed
 >>> g.type.undirected
 >>> g.type.weighted
 >>> g.type.allowing_multiple_edges
 >>> g.type.allowing_self_loops
 >>> g.type.modifiable

Now that we have seen a little bit how to create graphs, let us discuss what it means to 
contain self-loops or multiple-edges:

  * **self-loops** are edges which start at a vertex `v` and end at the same vertex `v`,
  * **multiple-edges** are edges which have the exact same endpoints.

Some algorithms are able to tolerate this, others do not. Thus, it is important to read the 
documentation of each algorithm in order to check whether such cases are tolerated. Some 
algorithms raise a :py:class:`ValueError` in case they detect that they are running on a 
graph that contains either self-loops or multiple-edges.

If the graph is constructed to not allow self-loops and/or multiple-edges, an attempt to 
add such an edge will also raise a :py:class:`ValueError`.

Finally, unmodifiable graphs are graphs which cannot be altered anymore. They can be constructed
using either function :py:meth:`.as_unmodifiable` or by using some other graph 
factory function, such as factory for sparse graphs, which we will discuss later on. 

Navigation
----------

When implementing graph algorithms one of the most common operation that is required is to 
find the neighbors of a vertex. Given a vertex `v` you can find the incident edges using
methods:

  * :py:meth:`.Graph.edges_of()`
  * :py:meth:`.Graph.inedges_of()`
  * :py:meth:`.Graph.outedges_of()`

The behavior of these methods strongly depend on whether the graph is directed or undirected.
If the graph is undirected all methods return the set of edges touching the vertex. For directed
graphs method :py:meth:`.Graph.outedges_of()` returns all outgoing edges from `v`, method 
:py:meth:`.Graph.inedges_of()` all incoming edges to `v` and method :py:meth:`.Graph.edges_of()` 
returns all edges either incoming or outgoing.  

Combining the above methods with the helper method :py:meth:`.Graph.opposite` which accepts an 
edge and one of its endpoints and returns the opposite vertex of that edge, results in the 
following classic pattern::

  v = 0
  for e in g.outedges_of(v):
      u = g.opposite(e, v)
      print ('Vertex {} is opposite {} in edge {}.format(u, v, e))

Similar behavior can be seen when using methods:

  * :py:meth:`.Graph.degree_of()`
  * :py:meth:`.Graph.indegree_of()`
  * :py:meth:`.Graph.outdegree_of()`

which return the vertex degrees. Again depending on directed or undirected the results might be 
different. We refer the reader to the documentation of each method for details.

BFS implementation example
--------------------------

Let us implement a breadth-first search using |Project| in order to get familiar with the library::

  def bfs(graph, source): 
      queue = []
      visited = set()

      queue.append(source)
      visited.add(source)

      while len(queue)>0: 
          v = queue.pop(0)
          yield v

          for e in graph.outedges_of(v):
              u = graph.opposite(e, v)
              if u not in visited:
                  visited.add(u)
                  queue.append(u)

This is just an example, the library contains full support for classic graph traversals.


