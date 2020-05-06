
.. _graph:

The Graph Interface
*******************

.. currentmodule:: jgrapht

The main interface of the library is the :class:`Graph <jgrapht.types.Graph>`. All 
graph instances returned by the library follow this interface and almost all library methods revolve 
around it. 

Creating graphs can be accomplished using the following factory method. During runtime the 
type of the graph can be queried using :py:meth:`.Graph.graph_type` which returns a 
:class:`GraphType <jgrapht.types.GraphType>` instance. This allows algorithms to adjust their 
behavior depending on the graph they are working on.

.. autofunction:: jgrapht.create_graph

Graph
=====

The graph interface contains all the necessary methods to query or modify the graph.

.. autoclass:: jgrapht.types.Graph
   :inherited-members:
   :members:

Graph Type
==========

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.types.GraphType
   :inherited-members:

