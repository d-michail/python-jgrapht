
.. _generators:

.. currentmodule:: jgrapht.generators

Generators
**********

This module contains functions which can generate graphs based on various famous models.
All these generators assume that the user has already created an empty graph and calls 
the generator with the graph as parameter. This means that the provided graph must be 
able to support the particular generator. For example if the generator creates self-loops, 
then the provided graph object must also support self-loops.

.. automodule:: jgrapht.generators
   :members:
