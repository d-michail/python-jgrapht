
.. _interfaces:

Interfaces
**********

.. currentmodule:: jgrapht

Graph
^^^^^

The main interface of the library is the :class:`Graph <jgrapht.types.Graph>`. All 
graph instances returned by the library follow this interface and almost all library methods revolve 
around it. The graph interface contains all the necessary methods to query or modify a graph.

.. autoclass:: jgrapht.types.Graph
   :inherited-members:
   :members:

AttributesGraph
^^^^^^^^^^^^^^^

Some graph implementations are also attribute graphs which means that they can directly associate 
attributes/properties with the vertices and edges of the graph.

.. autoclass:: jgrapht.types.AttributesGraph
   :inherited-members:
   :members:

GraphType
^^^^^^^^^

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.types.GraphType
   :inherited-members:

DirectedAcyclicGraph
^^^^^^^^^^^^^^^^^^^^

A special type is available for directed acyclic graphs (DAGs).

.. autoclass:: jgrapht.types.DirectedAcyclicGraph
   :no-inherited-members:
   :members:
   :special-members:

   A directed acyclic graph (dag) has all the graph members and the following additional methods.

ListenableGraph
^^^^^^^^^^^^^^^

In case the user wants to listen on structural change events, a special type of listenable graph is 
also provided.

.. autoclass:: jgrapht.types.ListenableGraph
   :no-inherited-members:
   :members:

   A listenable graph has all the graph members and the following additional methods which 
   allow users to register and unregister listeners.

.. autoclass:: jgrapht.types.GraphEvent
   :members: