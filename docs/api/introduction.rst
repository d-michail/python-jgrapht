
.. _introduction:

Introduction
************ 

.. currentmodule:: jgrapht
 
The JGraphT library is a highly efficient graph library containing state-of-the-art graph
data-structures as well as a multitude of sophisticated graph algorithms. It has been in development
for many years already and is currently used in production both in research and industry.
This interface to the library is a pure python/native package having no dependency on the JVM.
During the build process the backend JGraphT library is compiled as a shared library
and bundled inside the python package.

The |Project| library provides a *graph* data-structure capable of representing various different
kind of graphs/networks such as:

 *  **directed**: in directed graphs an edge :math:`(u,v)` is a directed pair of vertices,
 *  **undirected**: in undirected graphs an edge :math:`\{u,v\}` is an unordered pair of vertices,
 *  with **self-loops**: self-loops are edges of the form :math:`(v,v)` where both endpoints are the same,
 *  graphs with **multiple-edges**: multiple-edges are edges :math:`e = (u,v)` and :math:`e' = (u,v)`
    which have the exact same endpoints,
 *  **weighted** graphs: graphs where each edge is associated with a double value called its weight,
 *  **unweighted** graphs: graphs where the weight of each edge is 1.0 (uniform weight function)

A graph :math:`G(V,E)` contains vertices and edges. In |Project| both the vertices and the edges of 
the graph are represented using integers. Each edge :math:`e = (u,v)` is associated with

 * its two endpoints :math:`u` and :math:`v`, and
 * a double value called its weight.

All access to information about the graph happens using the graph object. 
Thus, given an edge, finding its source, target and weight can be performed using graph methods. Similarly, 
information about the vertices, such as its incident edges, can also be performed using corresponding 
graph methods.

When manipulating graphs, beside its structure (topology), users usually associate additional information
with the vertices and edges. Such vertex and edge *attributes*, are fully supported when exporting and 
importing graphs, by using callback functions. Storing such attributes, however, is not performed inside the
graph. The user is responsible to maintain external dictionaries with the vertex and edge identifier as
the key.

.. note::

  While this might seen like a restriction at first, it allows for several optimizations.
  Combined with the simplicity and power of dictionaries in Python, it should pose no real 
  restriction to the user, except possibly some aesthetic effect. Vertex and edge attributes are fully
  supported in exporters and importers.


