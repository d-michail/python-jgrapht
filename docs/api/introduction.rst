
.. _introduction:

Introduction
************ 

.. currentmodule:: jgrapht
 
The JGraphT library is a highly efficient graph library containing both graph data-structures as 
well as a multitude of sophisticated graph algorithms. It has been in development for over 10 
years and is currently used in production both in research and industry. While the original library
is written in Java, this library has no dependency on the JVM. Instead during the build process
a shared library is constructed and bundled inside the python package.

The python-jgrapht library provides a graph data-structure capable of representing various different
kind of graphs such as:

 *  **directed**: in directed graphs an edge :math:`(u,v)` is a directed pair of vertices
 *  **undirected**: in undirected graphs an edge :math:`{u,v}` is an unordered pair of vertices,
 *  with **self-loops**: self-loops are edges of the form :math:`(v,v)` where both endpoints are the same,
 *  graphs with **multiple-edges**: multiple-edges are edges :math:`e` and :math:`e` which have the exact same endpoints,
 *  **weighted** graphs: graphs where each edge is associated with a double value called its weight,
 *  **unweighted** graphs: graphs where the weight of each edge is 1.0

The vertices of the graph are long integers, not necessarily in a continuous range, unless explicitly specified. The
edges of the graph are also long integers and each such edge is associated with two endpoints, its source and its target,
and one double value called its weight. All access to information about the graph happens using the graph object. 
Thus, given an edge, finding its source, target and weight can be performed using the corresponding graph methods.
Similarly given a vertex, access to its incident edges can be performed using the corresponding graph methods.
The graph interface follows closely the design of the Java interface. 

It is very common for users to maintain additional vertex and edge attributes. Since this can be easily accomplished
using dictionaries, the graph contains no internal support. On the other hand, full support for such additional 
attributes is provided by all graph importers and exporters. Thus, when reading from or writing to files, vertex and 
edge attributes are read and written using callback functions.
