
.. _introduction:

Introduction
************ 

.. currentmodule:: jgrapht
 
The |Project| library is a highly efficient graph library containing state-of-the-art graph
data-structures as well as a multitude of sophisticated graph algorithms. It has been in development
for many years already and is currently used in production both in research and industry.

The |Bindings| is a pure python/native package having no dependency on the JVM. During the build
process the backend |Project| library is compiled as a shared library and bundled inside the python
package. It provides a *graph* data-structure capable of representing various different
kind of graphs/networks such as:

 *  **directed**: in directed graphs an edge :math:`(u,v)` is an ordered pair of vertices,
 *  **undirected**: in undirected graphs an edge :math:`\{u,v\}` is an unordered pair of vertices,
 *  with **self-loops**: self-loops are edges of the form :math:`(v,v)` where both endpoints are the same,
 *  graphs with **multiple-edges**: multiple-edges are edges :math:`e = (u,v)` and :math:`e' = (u,v)`
    which have the exact same endpoints,
 *  **weighted** graphs: graphs where each edge is associated with a double value called its weight,
 *  **unweighted** graphs: graphs where the weight of each edge is 1.0 (uniform weight function)

A graph :math:`G(V,E)` contains vertices and edges. Each edge :math:`e = (u,v)` is associated with

 * its two endpoints :math:`u` and :math:`v`, and
 * a double value called its weight.

Additionally, both vertices and edges are usually associated with information called attributes
or properties. All access to information about the graph happens using the graph object. 
Thus, given an edge, finding its source, target and weight can be performed using graph methods. Similarly, 
information about the vertices, such as its incident edges, can also be performed using corresponding 
graph methods.

The |Bindings| contains two main graph implementations which we describe next. Creating graphs of 
either category can be done using the :py:meth:`jgrapht.create_graph` factory method.

integer graphs
""""""""""""""

The *integer graph* is oriented torwards simplicity and performance. Its main characteristic is that 
vertices and edges are always integers. When manipulating graphs, beside its structure (topology),
users usually associate additional information with the vertices and edges. Such vertex and edge
attributes/properties, are fully supported when exporting and importing graphs, by using callback
functions. Storing such attributes/properties, however, is not performed inside the graph. The
user is responsible to maintain external dictionaries with the vertex and edge identifier as the key.
While this might seem like a restriction at first, it allows for several optimizations at the graph
level. Combined with the simplicity and power of dictionaries in Python, it should pose no real 
restriction to the user, except possibly some aesthetic effect. 

A special version of the integer graph which is also supported is the *sparse* graph. The sparse graph 
is a static variant which can only be bulk-loaded from a list of edges. Its benefits is that it is 
condiderably faster and less memory hungry, at the expense of not being modifiable. It is best suited 
for less dynamic workloads where the user creates a graph once and executes complex algorithms on it.

any-hashable graphs
"""""""""""""""""""
   
The *any-hashable graph* is a graph implementation which allows the use of any Python hashable as vertices 
or edges. Additionally, it provides support for maintaining the attributes/properties dictionaries 
inside the graph. During creation the user can provide a vertex and edge factory function (called vertex
supplier and edge supplier) which the graph can use whenever it needs to create new vertices or edges.
If not explicitly provided, the implementation uses object instances for all automatically created vertices
and edges. Importers and exporters automatically support graphs, by importing/exporting their associated
attributes.

.. note::
   Any-hashable graphs are implemented by wrapping the integer graph which means that they incur a performance 
   penalty compared to the integer graph.
   