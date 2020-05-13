
.. _algorithms/flow:

Flows
*****

Algorithms
----------


We are given a weighted directed or undirected graph :math:`G(V,E)`. Each edge :math:`e \in E` has 
an associated non-negative capacity :math:`c_e \ge 0`. The maximum flow problem involves 
finding a feasible flow :math:`f: E \mapsto \mathbb{R}_{0+}` of maximum value.
A flow is feasible if:

 * the flow :math:`f(e)` of an edge :math:`e` does not exceed its capacity, and 
 * for each vertex except the source and sink, the sum of incoming flows is equal to the sum 
   of outgoing flows.

Computing maximum s-t flows and minimum s-t cuts can be performed using the following 
functions.

.. autofunction:: jgrapht.algorithms.flow.max_st_flow

.. autofunction:: jgrapht.algorithms.flow.min_st_cut

When the user requires more advanced control over the selected 
algorithm, the following functions are provided.

.. automodule:: jgrapht.algorithms.flow
   :members: push_relabel, dinic, edmonds_karp

Types
-----

Flows are represented using instances of the following class.

.. autoclass:: jgrapht.types.Flow
   :members:

   This is a dictionary from edges to double values.   
