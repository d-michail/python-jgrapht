
.. _property_graph_factories:

Property Graph Factories
************************

.. currentmodule:: jgrapht

Property graphs are graphs which (a) can have any hashable as vertices and edges, and (b) 
can associate attributes/properties with the vertices and edges. 

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

