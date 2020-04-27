
.. _graph:

The Graph Interface
*******************

.. currentmodule:: jgrapht.graph

The main interface of the library is the :class:`Graph <jgrapht.graph.Graph>` and almost
all library methods revolve around it. This is the default graph which should be used in most
the use-cases. The default graph is capable of representing various different kind of graphs 
such as:

 *  **directed**: in directed graphs an edge :math:`(u,v)` is a directed pair of vertices
 *  **undirected**: in undirected graphs an edge :math:`{u,v}` is an unordered pair of vertices,
 *  with **self-loops**: self-loops are edges of the form :math:`(v,v)` where both endpoints are the same,
 *  graphs with **multiple-edges**: multiple-edges are edges :math:`e` and :math:`e` which have the exact same endpoints,
 *  **weighted** graphs: graphs where each edge is associated with a double value called its weight,
 *  **unweighted** graphs: graphs where the weight of each edge is 1.0

All the above can be represented by the following class using the appropriate constructor arguments.

Graph
=====

.. autoclass:: jgrapht.graph.Graph
   :inherited-members:
   :members:

Graph Type
==========

The :class:`.GraphType` is used to represent during runtime the properties of the graph.

.. autoclass:: jgrapht.graph.GraphType
   :inherited-members:

. autoclass:: jgrapht.graph.GraphPath
   :inherited-members:
