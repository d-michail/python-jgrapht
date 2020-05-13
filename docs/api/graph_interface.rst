
.. _graph:

The Graph
*********

.. currentmodule:: jgrapht

The main interface of the library is the :class:`Graph <jgrapht.types.Graph>`. All 
graph instances returned by the library follow this interface and almost all library methods revolve 
around it. The graph interface contains all the necessary methods to query or modify the graph.

.. autoclass:: jgrapht.types.Graph
   :inherited-members:
   :members:

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.types.GraphType
   :inherited-members:

