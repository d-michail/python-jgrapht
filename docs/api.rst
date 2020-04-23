.. _api:

Developer Interface
===================

.. module:: jgrapht

This part of the documentation covers all the interfaces.

Main Interface
--------------

As you might expect the main interface is the :class:`Graph <jgrapht.graph.Graph>`.

.. autoclass:: jgrapht.graph.Graph
   :inherited-members:
   :members:

The following methods allow the user to check for certain graph properties.

.. automodule:: jgrapht.graph
   :members: is_cubic, is_eulerian



The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.graph.GraphType
   :inherited-members:   


Graph Generators
----------------

.. automodule:: jgrapht.generators
   :members:

Spanning Algorithms
-------------------

.. automodule:: jgrapht.algorithms.mst
   :members: