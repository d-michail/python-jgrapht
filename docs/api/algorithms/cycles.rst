.. _algorithms/cycles:

Cycles
******

.. currentmodule:: jgrapht

Cycle detection and enumeration, cycle bases, Eulerian cycles, the Chinese postman problem,
minimum mean cycles, and chordal graphs (perfect elimination orders and holes).

Example
=======

.. code-block:: pycon

  >>> import jgrapht as jg
  >>> g = jg.ring_graph(5)
  >>> jg.has_cycle(g)
  True
  >>> jg.is_eulerian(g)
  True
  >>> jg.eulerian_cycle(g).vertices
  [4, 0, 1, 2, 3, 4]
  >>> jg.cycle_basis(g)
  [[1, 2, 3, 4, 0]]
  >>> len(jg.simple_cycles(jg.complete_graph(4, directed=True)))
  20

Functions
=========

.. autofunction:: has_cycle
.. autofunction:: vertices_on_cycles
.. autofunction:: simple_cycles
.. autofunction:: cycle_basis
.. autofunction:: cycle_to_path
.. autofunction:: is_eulerian
.. autofunction:: eulerian_cycle
.. autofunction:: chinese_postman
.. autofunction:: minimum_mean_cycle
.. autofunction:: is_chordal
.. autofunction:: perfect_elimination_order
.. autofunction:: chordal_hole
