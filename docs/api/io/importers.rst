
.. _io/importers:

Importers
*********

The available importers can be seen below. Each of them accepts a graph object as its 
first parameter. The user is expected to first construct the graph object and then call the 
importer. This means that the graph object must be able to support the input. If for 
example the input contains self-loops, then the graph object must also support self-loops.
This also means that reading an input file will result in different graphs if the graph 
is directed or undirected.  

.. automodule:: jgrapht.io.importers
   :members:

