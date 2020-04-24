.. _api:

Developer Interface
===================

.. module:: jgrapht

This part of the documentation covers all the interfaces.

The Graph Interface
-------------------

As you might expect the main interface is the :class:`Graph <jgrapht.graph.Graph>` and almost
all library methods revolve around it. This is the default graph which should be used in most 
the use cases. 

.. autoclass:: jgrapht.graph.Graph
   :inherited-members:
   :members:

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.graph.GraphType
   :inherited-members:   

Graph Properties
----------------

The following methods allow the user to check for certain graph properties.

.. automodule:: jgrapht.graph
   :members: is_cubic, is_eulerian

Graph Metrics
-------------

Certain graph metrics such as the diameter of a graph can be computed using the following methods.

.. automodule:: jgrapht.metrics
   :members:

Graph Traversal 
---------------

.. automodule:: jgrapht.traversal
   :members:


Graph Generators
----------------

.. automodule:: jgrapht.generators
   :members:

Spanning Algorithms
-------------------

.. automodule:: jgrapht.algorithms.mst
   :members:
