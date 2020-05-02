
.. _graph:

The Graph Interface
*******************

.. currentmodule:: jgrapht

The main interface of the library is the :class:`Graph <jgrapht.types.Graph>`. All 
graph instances returned by the library follow this interface and almost all library methods revolve 
around it. Appropriate factory methods can be used to create graph instances for most of the use-cases. 
The default graph is capable of representing various different kind of graphs such as:

 *  **directed**: in directed graphs an edge :math:`(u,v)` is a directed pair of vertices
 *  **undirected**: in undirected graphs an edge :math:`{u,v}` is an unordered pair of vertices,
 *  with **self-loops**: self-loops are edges of the form :math:`(v,v)` where both endpoints are the same,
 *  graphs with **multiple-edges**: multiple-edges are edges :math:`e` and :math:`e` which have the exact same endpoints,
 *  **weighted** graphs: graphs where each edge is associated with a double value called its weight,
 *  **unweighted** graphs: graphs where the weight of each edge is 1.0

Creating graphs can be accomplished using the following factory method.  

.. autofunction:: jgrapht.create_graph

Graph
=====

.. autoclass:: jgrapht.types.Graph
   :inherited-members:
   :members:

Graph Type
==========

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.types.GraphType
   :inherited-members:

