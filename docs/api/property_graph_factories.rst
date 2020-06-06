
.. _property_graph_factories:

Property Graph Factories
************************

.. currentmodule:: jgrapht

Property Graph
^^^^^^^^^^^^^^

Property graphs are graphs which (a) can have any hashable as vertices and edges, and (b) 
can associate attributes/properties with the vertices and edges. Property graphs need to 
be able to create new objects for vertices and edges. This is accomplished by providing 
two functions called *vertex supplier* and *edge supplier*. If not provided by the user, 
the default implementation creates instances of :py:class:`object`.

The main factory function which creates property graphs is :py:meth:`jgrapht.create_property_graph`. 
Depending on the given parameters different types of graphs can be represented. All graphs 
returned by this function are instances of :py:class:`jgrapht.types.Graph` and 
:py:class:`jgrapht.types.PropertyGraph`. 

 .. autofunction:: jgrapht.create_property_graph

Helper factory functions :py:meth:`jgrapht.create_directed_property_graph` and 
:py:meth:`jgrapht.create_undirected_property_graph` provide the same functionality restricted for
directed and undirected graphs.

.. autofunction:: jgrapht.create_directed_property_graph
.. autofunction:: jgrapht.create_undirected_property_graph


Directed Acyclic Property Graph (DAG)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A directed acyclic graph is a directed graph with no cycles. The following function creates
such a graph with dynamically enforces the property and maintains a topological ordering 
of the vertices. The returned graph is iterable and returns topological ordering iterators.
All graphs 
returned by this function are instances of :py:class:`jgrapht.types.Graph`,
:py:class:`jgrapht.types.PropertyGraph` and :py:class:`jgrapht.types.DirectedAcyclicGraph`.

.. autofunction:: jgrapht.create_property_dag
