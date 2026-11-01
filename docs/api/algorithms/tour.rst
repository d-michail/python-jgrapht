.. _algorithms/tour:

Tours
*****

.. currentmodule:: jgrapht

Traveling salesman heuristics (nearest neighbor, greedy, insertion, Christofides, 2-opt),
exact Held-Karp, and Hamiltonian cycles and paths.

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.complete_graph(6)
  >>> tour = jg.traveling_salesman_tour(g)
  >>> len(tour.vertices)
  7
  >>> jg.hamiltonian_cycle(g) is not None
  True

Functions
=========

.. autofunction:: traveling_salesman_tour
.. autofunction:: hamiltonian_cycle
.. autofunction:: hamiltonian_path
.. autofunction:: improve_tour
