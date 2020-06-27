
.. _graph_factories:

Graph Factories
***************

.. currentmodule:: jgrapht

Creating graphs can be accomplished using factory methods. During runtime the 
type of the graph can be queried using :py:attr:`.Graph.type` which returns a 
:py:class:`GraphType <jgrapht.types.GraphType>` instance. This allows algorithms to adjust their 
behavior depending on the graph they are working on.


Graph
^^^^^

The main factory function which creates graphs is :py:meth:`jgrapht.create_graph`. 
Depending on the given parameters different types of graphs can be represented. All graphs 
returned by this function are instances of :py:class:`jgrapht.types.Graph`.
Most users should create graphs using this function:

.. autofunction:: jgrapht.create_graph


Sparse Graph
^^^^^^^^^^^^

The following function creates a special *sparse* graph representation which has certain 
benefits and certain drawbacks. The benefits are that (a) it is much smaller w.r.t memory 
consumption and (b) it is also usually much faster. The drawbacks are that the sparse
representation (a) cannot be modified after construction and (b) is forces a user to 
use vertex and edges that are integers starting from 0 in a continuous range. Since modification
is not possible, a user needs to bulk-load the graph by providing both the number of vertices
and all edges before hand.

.. autofunction:: jgrapht.create_sparse_graph

A helper function :py:meth:`jgrapht.copy_to_sparse_graph` can help in order to create a sparse
graph from another graph. 

.. autofunction:: jgrapht.copy_to_sparse_graph

Building sparse graphs can be performed by using edge lists. See the section
:ref:`edge list importers <io/edgelist>`.



