
.. _graph_factories:

Graph Factories
***************

.. currentmodule:: jgrapht

Creating graphs can be accomplished using factory methods. During runtime the 
type of the graph can be queried using :py:attr:`.Graph.type` which returns a 
:class:`GraphType <jgrapht.types.GraphType>` instance. This allows algorithms to adjust their 
behavior depending on the graph they are working on.

The main factory method which creates graphs is :py:meth:`jgrapht.create_graph`. 
Depending on the given parameters different types of graphs can be represented. Most users 
should create graphs using this function:

.. autofunction:: jgrapht.create_graph

The following function creates a special *sparse* graph representation which has certain 
benefits and certain drawbacks. The benefits are that (a) it is much smaller w.r.t memory 
consumption and (b) it is also usually much faster. The drawbacks are that the sparse
representation (a) cannot be modified after construction and (b) is forces a user to 
use integer starting from 0 in a continuous range. Since modification is not possible, 
a user needs to provide both the number of vertices and all edges before hand.

.. autofunction:: jgrapht.create_sparse_graph



